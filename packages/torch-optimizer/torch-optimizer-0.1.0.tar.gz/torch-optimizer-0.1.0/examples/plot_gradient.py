import math

import numpy as np
import torch
from torch.autograd import Variable

import matplotlib.pyplot as plt
import torch_optimizer as optim
from hyperopt import fmin, hp, tpe


def rosenbrock(tensor):
    x, y = tensor
    return (1 - x) ** 2 + 100 * (y - x ** 2) ** 2


def beale(tensor):
    x, y = tensor
    f = (
        (1.5 - x + x * y) ** 2
        + (2.25 - x + x * y ** 2) ** 2
        + (2.625 - x + x * y ** 3) ** 2
    )
    return f


def sphere(tensor):
    x, y = tensor
    f = x ** 2 + y ** 2
    return f


def rastrigin(tensor):
    x, y = tensor
    A = 10
    f = (
        A * 2
        + (x ** 2 - A * torch.cos(x * math.pi * 2))
        + (y ** 2 - A * torch.cos(y * math.pi * 2))
    )
    return f


def rastrigin_numpy(tensor):
    x, y = tensor
    A = 10
    f = (
        A * 2
        + (x ** 2 - A * np.cos(x * math.pi * 2))
        + (y ** 2 - A * np.cos(y * math.pi * 2))
    )
    return f


def plot_rosenbrok(func, grad_iter, minimum, optimizer_name):
    x = np.linspace(-2, 2, 250)
    y = np.linspace(-1, 3, 250)
    X, Y = np.meshgrid(x, y)
    Z = func([X, Y])

    iter_x, iter_y = grad_iter[0, :], grad_iter[1, :]

    fig = plt.figure(figsize=(16, 8))

    # Surface plot
    ax = fig.add_subplot(1, 2, 1, projection='3d')
    ax.plot_surface(
        X,
        Y,
        Z,
        rstride=5,
        cstride=5,
        cmap='jet',
        # alpha=0.4,
        edgecolor='none',
    )
    ax.plot(
        iter_x,
        iter_y,
        rosenbrock([iter_x, iter_y]),
        color='r',
        marker='*',
        alpha=0.4,
    )
    ax.plot([1], [1], [0], 'gD')

    ax.view_init(45, 280)
    ax.set_xlabel('x')
    ax.set_ylabel('y')

    # Contour plot
    ax = fig.add_subplot(1, 2, 2)
    ax.contour(X, Y, Z, 90, cmap='jet')
    ax.plot(iter_x, iter_y, color='r', marker='x', alpha=0.4)
    # ax.plot(iter_x, iter_y, color='r', alpha=0.4)

    ax.set_title(f'{optimizer_name} with {len(iter_x)} iterations')
    plt.plot(*minimum, 'gD')
    plt.savefig(f'{optimizer_name}.png')


initial_state = (-2, 2)
minimum = (1, 1)


def execute_steps(
    func, initial_state, optimizer_class, optimizer_config, num_iter=500
):
    x = Variable(torch.Tensor(initial_state), requires_grad=True)
    optimizer = optimizer_class([x], **optimizer_config)
    steps = []
    steps = np.zeros((2, num_iter + 1))
    steps[:, 0] = np.array(initial_state)
    for i in range(1, num_iter + 1):
        optimizer.zero_grad()
        f = func(x)
        f.backward(retain_graph=True)
        optimizer.step()
        steps[:, i] = x.detach().numpy()
    return steps


def plot_rosenbrok_contour(grad_iter, optimizer_name='optimizer'):
    x = np.linspace(-2, 2, 250)
    y = np.linspace(-1, 3, 250)
    minimum = (1.0, 1.0)

    X, Y = np.meshgrid(x, y)
    Z = rosenbrock([X, Y])

    iter_x, iter_y = grad_iter[0, :], grad_iter[1, :]

    fig = plt.figure(figsize=(8, 8))

    # Contour plot
    ax = fig.add_subplot(1, 1, 1)
    ax.contour(X, Y, Z, 90, cmap='jet')
    ax.plot(iter_x, iter_y, color='r', marker='x', alpha=0.4)
    # ax.plot(iter_x, iter_y, color='r', alpha=0.4)

    ax.set_title(f'{optimizer_name} with {len(iter_x)} iterations')
    plt.plot(*minimum, 'gD')
    plt.show()


def plot_beale(grad_iter, optimizer_name='optimizer'):
    x = np.linspace(-4.5, 4.5, 250)
    y = np.linspace(-4.5, 4.5, 250)
    minimum = (3.0, 0.5)

    X, Y = np.meshgrid(x, y)
    Z = beale([X, Y])

    iter_x, iter_y = grad_iter[0, :], grad_iter[1, :]

    fig = plt.figure(figsize=(8, 8))

    # Contour plot
    ax = fig.add_subplot(1, 1, 1)
    ax.contour(X, Y, Z, 250, cmap='jet')
    ax.plot(iter_x, iter_y, color='r', marker='x', alpha=0.4)
    # ax.plot(iter_x, iter_y, color='r', alpha=0.4)

    ax.set_title(f'{optimizer_name} with {len(iter_x)} iterations')
    plt.plot(*minimum, 'gD')
    plt.show()


def plot_rastrigin(grad_iter, optimizer_name, lr):
    x = np.linspace(-4.5, 4.5, 250)
    y = np.linspace(-4.5, 4.5, 250)
    minimum = (0, 0)

    X, Y = np.meshgrid(x, y)
    Z = rastrigin_numpy([X, Y])

    iter_x, iter_y = grad_iter[0, :], grad_iter[1, :]

    fig = plt.figure(figsize=(8, 8))

    ax = fig.add_subplot(1, 1, 1)
    ax.contour(X, Y, Z, 20, cmap='jet')
    ax.plot(iter_x, iter_y, color='r', marker='x')

    ax.set_title(f'{optimizer_name} with {len(iter_x)} iterations, lr={lr:.6}')
    plt.plot(*minimum, 'gD')
    plt.plot(iter_x[-1], iter_y[-1], 'rD')
    plt.savefig(f'rastrigin_{optimizer_name}.png')


def optimize(optimizer_class, params):
    lr = params['lr']
    plt.style.use('seaborn-white')

    initial_state = (-2.0, 3.5)
    optimizer_config = dict(lr=lr)
    num_iter = 100
    optimizer_class = optimizer_class
    steps = execute_steps(
        rastrigin, initial_state, optimizer_class, optimizer_config, num_iter
    )
    plot_rastrigin(steps, optimizer_class.__name__, lr)
    return steps


optimizers = [
    optim.AccSGD,
    optim.AdaBound,
    optim.AdaMod,
    optim.DiffGrad,
    optim.Lamb,
    optim.RAdam,
    optim.SGDW,
    optim.Yogi,
]


def f():
    seed = 2
    accsgd_space = {'lr': hp.loguniform('lr', -8, 0.7)}

    def objective_rastrigin(lr):
        print(lr)
        initial_state = (-2.0, 3.5)
        minimum = (0, 0)
        initial_state = (-2.0, 3.5)
        optimizer_config = dict(lr=lr['lr'])
        num_iter = 100
        optimizer_class = optim.Yogi
        steps = execute_steps(
            rastrigin,
            initial_state,
            optimizer_class,
            optimizer_config,
            num_iter,
        )
        print(steps[0][-1], steps[1][-1])
        return (steps[0][-1] - minimum[0]) ** 2 + (
            steps[1][-1] - minimum[1]
        ) ** 2

    best = fmin(
        fn=objective_rastrigin,
        space=accsgd_space,
        algo=tpe.suggest,
        max_evals=200,
        rstate=np.random.RandomState(seed),
    )
    print(best)

    optimize(best)


f()
