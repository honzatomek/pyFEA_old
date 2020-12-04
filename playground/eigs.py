import numpy as np
from scipy import linalg

if __name__ == '__main__':
    """
    transform generalised eigenvalue problem [K]{v} = w^2[M]{v}
    to standard eigenvalue problem [A]{x} = lambda {x}
    using Cholseky decomposition of [M] = [L] [L]T
    then                      [K]{v} = w^2[M]{v}
    becomes                   [K]{v} = w^2 [L] [L]T {v}
    and finally  [L]-1 [K] [L]-T {v} = w^2 {v}
    """
    M = np.array([[2., 1., 0., 0.],
                  [1., 4., 1., 0.],
                  [0., 1., 4., 1.],
                  [0., 0., 1., 2.]], dtype=float)
    K = np.array([[1., -1., 0., 0.],
                  [-1., 2., -1., 0.],
                  [0., -1., 2., -1.],
                  [0., 0., -1., 1.]], dtype=float)

    # Cholesky decomposition
    L = linalg.cholesky(M, lower=True)

    # Inverse of lower triangular matrix
    L1 = linalg.inv(L)

    # scipy exact solution
    eigs1, evec1 = linalg.eigh(K, M)

    # solution using decomposition
    eigs2, evec2 = linalg.eigh(L1 @ K @ L1.T)

    # check results
    diff = eigs1 - eigs2
    check = np.abs(diff) < 0.00001
    assert check.all()

    pass
