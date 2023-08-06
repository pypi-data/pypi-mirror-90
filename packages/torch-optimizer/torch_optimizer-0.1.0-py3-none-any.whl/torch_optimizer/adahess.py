import math
from copy import deepcopy

import torch
import torch.optim


class AdaHessian(torch.optim.Optimizer):
    """Implements AdamHess algorithm."""

    def __init__(
        self,
        params,
        lr=1e-3,
        betas=(0.9, 0.999),
        eps=1e-8,
        weight_decay=0,
        block_length=1,
        hessian_power=1,
        single_gpu=False,
    ):
        defaults = dict(lr=lr, betas=betas, eps=eps, weight_decay=weight_decay)
        super(AdaHessian, self).__init__(params, defaults)

        self.block_length = block_length
        self.single_gpu = single_gpu
        self.hessian_power = hessian_power

    def get_trace(self, gradsH):
        """
        compute the Hessian vector product with v, at the current gradient
        point or compute the gradient of <gradsH,v>.
        :param v: a list of torch tensors
        :param gradsH: a list of torch variables
        :return: a list of torch tensors
        """

        params = self.param_groups[0]['params']
        params = list(filter(lambda x: x.requires_grad, params))

        v = [torch.randint_like(p, high=2) for p in params]

        for v_i in v:
            v_i[v_i < 0.5] = -1
            v_i[v_i >= 0.5] = 1

        hvs = torch.autograd.grad(
            gradsH, params, grad_outputs=v, only_inputs=True, retain_graph=True
        )

        hutchinson_trace = []
        for hv, vi in zip(hvs, v):
            param_size = hv.size()
            if len(param_size) <= 1:  # for Bias and LN
                tmp_output = torch.abs(hv * vi) + 0.0
                hutchinson_trace.append(tmp_output)
            elif len(param_size) == 2:  # Matrix
                tmp_output1 = torch.abs((hv * vi + 0.0)).view(
                    -1, self.block_length
                )  # faltten to the N times self.block_length
                tmp_output2 = torch.abs(torch.sum(tmp_output1, dim=[1])).view(
                    -1
                ) / float(self.block_length)
                tmp_output3 = tmp_output2.repeat_interleave(
                    self.block_length
                ).view(param_size)
                hutchinson_trace.append(tmp_output3)

        return hutchinson_trace

    def step(self, gradsH=None, closure=None):
        """Performs a single optimization step.

        Arguments:
            closure (callable, optional): A closure that reevaluates the model
                and returns the loss.
        """
        loss = None
        if closure is not None:
            loss = closure()

        hut_trace = self.get_trace(gradsH)

        for group in self.param_groups:
            for i, p in enumerate(group['params']):
                if p.grad is None:
                    continue
                # grad = p.grad.data.float()
                grad = deepcopy(gradsH[i].data.float())

                if grad.is_sparse:
                    raise RuntimeError(
                        'AdaHessian does not support sparse gradients, please'
                        ' consider SparseAdam instead'
                    )

                p_data_fp32 = p.data.float()

                state = self.state[p]

                # State initialization
                if len(state) == 0:
                    state['step'] = 0
                    # Exponential moving average of gradient values
                    state['exp_avg'] = torch.zeros_like(p_data_fp32)
                    # Exponential moving average of squared gradient values
                    state['exp_hessian_diag_sq'] = torch.zeros_like(
                        p_data_fp32
                    )
                else:
                    state['exp_avg'] = state['exp_avg'].type_as(p_data_fp32)
                    state['exp_hessian_diag_sq'] = state[
                        'exp_hessian_diag_sq'
                    ].type_as(p_data_fp32)

                exp_avg, exp_hessian_diag_sq = (
                    state['exp_avg'],
                    state['exp_hessian_diag_sq'],
                )

                beta1, beta2 = group['betas']

                state['step'] += 1

                # Decay the first and second moment running average coefficient
                exp_avg.mul_(beta1).add_(1 - beta1, grad)
                exp_hessian_diag_sq.mul_(beta2).addcmul_(
                    1 - beta2, hut_trace[i], hut_trace[i]
                )

                bias_correction1 = 1 - beta1 ** state['step']
                bias_correction2 = 1 - beta2 ** state['step']

                if self.hessian_power < 1:
                    denom = (
                        (
                            exp_hessian_diag_sq.sqrt()
                            / math.sqrt(bias_correction2)
                        )
                        ** self.hessian_power
                    ).add_(group['eps'])
                else:
                    denom = (
                        exp_hessian_diag_sq.sqrt()
                        / math.sqrt(bias_correction2)
                    ).add_(group['eps'])

                step_size = group['lr'] / bias_correction1

                # do weight decay
                if group['weight_decay'] != 0:
                    p_data_fp32.add_(
                        -group['weight_decay'] * group['lr'], p_data_fp32
                    )

                p_data_fp32.addcdiv_(-step_size, exp_avg, denom)

                p.data.copy_(p_data_fp32)

        return loss
