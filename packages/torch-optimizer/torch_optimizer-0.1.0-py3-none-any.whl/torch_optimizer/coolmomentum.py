import torch
from torch.optim.optimizer import Optimizer

from .types import OptFloat, OptLossClosure, Params

__all__ = ('CoolMomentum',)


class CoolMomentum(Optimizer):
    r"""Implements CoolMomentum Optimizer Algorithm.
    It has been proposed in `CoolMomentum: A Method for Stochastic
    Optimization by Langevin Dynamics with Simulated Annealing`__.

    Example:
        >>> import torch_optimizer as optim
        >>> optimizer = optim.CoolMomentum(model.parameters(), lr=0.01)
        >>> optimizer.zero_grad()
        >>> loss_fn(model(input), target).backward()
        >>> optimizer.step()

    __ https://arxiv.org/abs/2005.14605

    Note:
        Reference code: https://github.com/borbysh/coolmomentum
    """

    def __init__(
        self,
        params: Params,
        lr: float = 1e-3,
        momentum: float = 0,
        weight_decay: float = 0,
        beta: float = 1.0,
    ):
        if lr <= 0.0:
            raise ValueError('Invalid learning rate: {}'.format(lr))
        if momentum < 0.0:
            raise ValueError('Invalid momentum value: {}'.format(momentum))
        if weight_decay < 0:
            raise ValueError(
                'Invalid weight_decay value: {}'.format(weight_decay)
            )
        if beta <= 0.0:
            raise ValueError('Invalid beta parameter: {}'.format(beta))

        defaults = dict(
            lr=lr,
            momentum=momentum,
            weight_decay=weight_decay,
            beta=beta,
            beta_power=beta,
        )
        super(CoolMomentum, self).__init__(params, defaults)

    def step(self, closure: OptLossClosure = None) -> OptFloat:
        r"""Performs a single optimization step.

        Arguments:
            closure: A closure that reevaluates the model and returns the loss.
        """
        loss = None
        if closure is not None:
            loss = closure()

        for group in self.param_groups:
            weight_decay = group['weight_decay']
            momentum = group['momentum']
            beta = group['beta']
            beta_power = group['beta_power']
            group['beta_power'] = group['beta_power'] * beta
            ro = 1 - (1 - momentum) / beta_power
            ro = max(ro, 0)
            lrn = group['lr'] * (1 + ro) / 2

            for p in group['params']:
                if p.grad is None:
                    continue
                d_p = p.grad
                if weight_decay != 0:
                    d_p = d_p.add(p, alpha=weight_decay)
                param_state = self.state[p]
                if 'momentum_buffer' not in param_state:
                    buf = param_state['momentum_buffer'] = torch.clone(
                        d_p
                    ).detach()
                else:
                    buf = param_state['momentum_buffer']
                    buf.mul_(ro).add_(d_p, alpha=-lrn)
                d_p = buf
                p.data.add_(d_p)
        return loss
