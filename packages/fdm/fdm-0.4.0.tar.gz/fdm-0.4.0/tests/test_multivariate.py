import numpy as np
import pytest

from fdm import central_fdm, gradient, jvp, jacobian, hvp
from fdm.multivariate import _get_at_index
from .util import approx


def test_get_index():
    with pytest.raises(RuntimeError):
        _get_at_index(np.array(1), 1)


def test_gradient_vector_argument():
    m = central_fdm(10, 1)

    for a, x in zip(
        [np.random.randn(), np.random.randn(3), np.random.randn(3, 3)],
        [np.random.randn(), np.random.randn(3), np.random.randn(3, 3)],
    ):

        def f(y):
            return np.sum(a * y * y)

        approx(2 * a * x, gradient(f, m)(x))


def test_jvp():
    m = central_fdm(10, 1)
    a = np.random.randn(3, 3)

    def f(x):
        return np.matmul(a, x)

    x = np.random.randn(3)
    v = np.random.randn(3)
    approx(jvp(f, v, m)(x), np.matmul(a, v))


def test_jvp_directional():
    m = central_fdm(10, 1)
    a = np.random.randn(3)

    def f(x):
        return np.sum(a * x)

    x = np.random.randn(3)
    v = np.random.randn(3)
    approx(np.sum(gradient(f, m)(x) * v), jvp(f, v, m)(x))


def test_jacobian():
    m = central_fdm(10, 1)
    a = np.random.randn(3, 3)

    def f(x):
        return np.matmul(a, x)

    x = np.random.randn(3)
    approx(jacobian(f, m)(x), a)


def test_hvp():
    m_jac = central_fdm(10, 1, adapt=1)
    m_dir = central_fdm(10, 1, adapt=0)
    a = np.random.randn(3, 3)

    def f(x):
        return 0.5 * np.matmul(x, np.matmul(a, x))

    x = np.random.randn(3)
    v = np.random.randn(3)
    approx(
        hvp(f, v, jac_method=m_jac, dir_method=m_dir)(x),
        np.matmul(0.5 * (a + a.T), v)[None, :],
    )
