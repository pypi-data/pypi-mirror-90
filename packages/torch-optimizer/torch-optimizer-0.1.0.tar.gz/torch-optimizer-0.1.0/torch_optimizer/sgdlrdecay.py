from typing import Callable, Dict

import torch
from torch.optim.optimizer import Optimizer

from .types import OptFloat, OptLossClosure, Params, State

__all__ = ('SGDLRDecay',)


DecayFunc = Callable[[float, int, float], float]


def _exp(lr: float, t: int, alpha: float) -> float:
    return lr * (alpha ** t)


def _1t(lr: float, t: int, alpha: float) -> float:
    return lr / (1.0 + alpha * t)


def _sqrt(lr: float, t: int, alpha: float) -> float:
    return lr / (1.0 + alpha * (t ** 0.5))


class SGDLRDecay(Optimizer):
    r"""Implements stochastic gradient descent with several step size
    decay schemes.

    It has been proposed in `Exponential Step Sizes for Non-Convex
    Optimization`__.

    Arguments:
        params: iterable of parameters to optimize or dicts defining
            parameter groups
        lr: initial learning rate (default: 1e-3)
        scheme: the decay scheme, currently only supports 'exp', 't', 'sqrt'
        alpha: decay factor.
        momentum: momentum factor (default: 0).
        weight_decay: weight decay (L2 penalty) (default: 0).
        dampening: dampening for momentum (default: 0).
        nesterov: enables Nesterov momentum (default: False).

    __ https://arxiv.org/abs/2002.05273

    Note:
        Reference code: https://github.com/zhenxun-zhuang/SGD-Exponential-Stepsize  # noqa
    """

    def __init__(
        self,
        params: Params,
        lr: float = 1e-3,
        scheme: str = 'exp',
        alpha: float = 0.999,
        momentum: float = 0.0,
        dampening: float = 0.0,
        weight_decay: float = 0.0,
        nesterov: bool = False,
    ) -> None:
        if lr <= 0.0:
            raise ValueError(f'Invalid learning rate: {lr}')
        if alpha <= 0.0:
            raise ValueError(f'Invalid alpha value: {alpha}')
        if momentum < 0.0:
            raise ValueError(f'Invalid momentum value: {momentum}')
        if weight_decay < 0.0:
            raise ValueError(f'Invalid weight_decay value: {weight_decay}')
        if scheme not in ('exp', '1t', 'sqrt'):
            raise ValueError(f'Invalid scheme value: {scheme}')

        defaults = dict(
            lr=lr,
            alpha=alpha,
            scheme=scheme,
            momentum=momentum,
            dampening=dampening,
            weight_decay=weight_decay,
            nesterov=nesterov,
        )
        if nesterov and (momentum <= 0 or dampening != 0):
            raise ValueError(
                'Nesterov momentum requires a momentum and zero dampening'
            )
        super(SGDLRDecay, self).__init__(params, defaults)

        self._schemes: Dict[str, DecayFunc] = {
            'exp': _exp,
            '1t': _1t,
            'sqrt': _sqrt,
        }

    def __setstate__(self, state: State) -> None:
        super(SGDLRDecay, self).__setstate__(state)
        for group in self.param_groups:
            group.setdefault('nesterov', False)

    def step(self, closure: OptLossClosure = None) -> OptFloat:
        """Performs a single optimization step.

        Arguments:
            closure: A closure that reevaluates the model and returns the loss.
        """
        loss = None
        if closure is not None:
            loss = closure()

        for group in self.param_groups:
            weight_decay = group['weight_decay']
            momentum = group['momentum']
            dampening = group['dampening']
            nesterov = group['nesterov']
            alpha = group['alpha']
            lr = group['lr']
            decay_func = self._schemes[group['scheme']]

            for p in group['params']:
                if p.grad is None:
                    continue

                param_state = self.state[p]
                if len(param_state) == 0:
                    param_state['step'] = 0
                param_state['step'] += 1
                d_p = p.grad.data
                if weight_decay != 0:
                    d_p.add_(weight_decay, p.data)
                if momentum != 0:
                    if 'momentum_buffer' not in param_state:
                        buf = param_state['momentum_buffer'] = torch.clone(
                            d_p
                        ).detach()
                    else:
                        buf = param_state['momentum_buffer']
                        buf.mul_(momentum).add_(1 - dampening, d_p)
                    if nesterov:
                        d_p = d_p.add(momentum, buf)
                    else:
                        d_p = buf

                setep_size = decay_func(lr, param_state['step'], alpha)
                p.data.add_(-setep_size, d_p)
        return loss
