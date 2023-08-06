import pytest
from torch.optim.optimizer import Optimizer

import torch_optimizer as optim


@pytest.mark.parametrize('optimizer_name', ['yogi', 'Yogi', 'YoGi'])
def test_returns_optimizer_cls(optimizer_name):
    optimizer_cls = optim.get(optimizer_name)
    assert issubclass(optimizer_cls, Optimizer)
    assert optimizer_cls.__name__.lower() == optimizer_name.lower()


@pytest.mark.parametrize('optimizer_name', ['foo', 'bar'])
def test_raises(optimizer_name):
    with pytest.raises(ValueError):
        optim.get(optimizer_name)
