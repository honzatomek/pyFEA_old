# From: https://codereview.stackexchange.com/q/19088
# Theory: http://ciprian-zavoianu.blogspot.com/2009/01/project-bandwidth-reduction.html
# Scipy followup: https://scicomp.stackexchange.com/questions/24817/applying-the-result-of-cuthill-mckee-in-scipy
# Scipy: https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csgraph.reverse_cuthill_mckee.html#scipy.sparse.csgraph.reverse_cuthill_mckee
# Matplotlib plot sparse matrix: https://matplotlib.org/3.1.1/gallery/images_contours_and_fields/spy_demos.html#sphx-glr-gallery-images-contours-and-fields-spy-demos-py

import matplotlib.pyplot as plt
import numpy as np
from scipy.sparse import csr_matrix, csc_matrix
from scipy.sparse.csgraph import reverse_cuthill_mckee, breadth_first_order


def getDegree(Graph):
    """
    find the degree of each node. That is the number
    of neighbours or connections.
    (number of non-zero elements) in each row minus 1.
    Graph is a Cubic Matrix.
    """
    degree = [0]*Graph.shape[0]
    for row in range(Graph.shape[0]):
        degree[row] = len(np.flatnonzero(Graph[row]))-1
    return degree


def getAdjacency(Mat):
    """
    return the adjacncy matrix for each node
    """
    adj = [0]*Mat.shape[0]
    for i in range(Mat.shape[0]):
        q = np.flatnonzero(Mat[i])
        q = list(q)
        q.pop(q.index(i))
        adj[i] = q
    return adj


def RCM_loop(deg, start, adj, pivots, R):
    """
    Reverse Cuthil McKee ordering of an adjacency Matrix
    """
    digar = np.array(deg)
    # use np.where here to get indecies of minimums
    if start not in R:
        R.append(start)
    Q = adj[start]
    for idx, item in enumerate(Q):
        if item not in R:
            R.append(item)
    Q = adj[R[-1]]
    if set(Q).issubset(set(R)) and len(R) < len(deg) :
        p = pivots[0]
        pivots.pop(0)
        return RCM_loop(deg, p, adj, pivots, R)
    elif len(R) < len(deg):
        return RCM_loop(deg, R[-1], adj, pivots, R)
    else:
        R.reverse()
        return R


def test_data():
    A = np.diag(np.ones(8))
    nzc = [[4], [2, 5, 7], [1, 4], [6], [0, 2], [1, 7], [3], [1, 5]]

    for i in range(len(nzc)):
        for j in nzc[i]:
            A[i, j] = 1
    return A


def test_script(A: np.ndarray):
    """
    test the RCM loop
    """
    print('Script solution:')

    print(A)
    # define the Result queue
    R = ["C"] * A.shape[0]
    adj = getAdjacency(A)
    degree = getDegree(A)
    digar = np.array(degree)
    pivots = list(np.where(digar == digar.min())[0])
    inl = []
    perm = np.array(RCM_loop(degree, 0, adj, pivots, inl))
    print(degree)
    print(adj)
    print("solution:", list(perm))
    print("correct:", [6, 3, 7, 5, 1, 2, 4, 0])
    # B = A[perm, perm]
    B = np.array(A)
    for i in range(B.shape[0]):
        B[:, i] = B[perm, i]
    for i in range(B.shape[0]):
        B[i, :] = B[i, perm]
    print(B)
    return csr_matrix(B), perm


def test_csr(A: np.ndarray):
    print('SciPy CSR solution:')

    print(A)
    A = csr_matrix(A)
    perm = reverse_cuthill_mckee(A, False)
    print("solution:", list(perm))
    print("correct:", [6, 3, 7, 5, 1, 2, 4, 0])
    B = A[np.ix_(perm, perm)]
    print(B.todense())
    return B, perm


def test_csc(A: np.ndarray):
    print('SciPy CSC solution:')

    print(A)
    A = csc_matrix(A)
    perm = reverse_cuthill_mckee(A, False)
    print("solution:", list(perm))
    print("correct:", [6, 3, 7, 5, 1, 2, 4, 0])
    B = A[np.ix_(perm, perm)]
    print(B.A)
    return B, perm


def test_breadth_first(A: np.ndarray, index: int = 0):
    print('SciPy breadth first solution:')
    print(A)

    A = csc_matrix(A)
    perm = breadth_first_order(A, index, directed=False, return_predecessors=False)
    print("solution:", list(perm))
    print("correct:", [6, 3, 7, 5, 1, 2, 4, 0])
    B = A[np.ix_(perm, perm)]
    print(B.todense())
    return B, perm


def plot_results():
    cases = [test_script, test_csc]
    fig, axs = plt.subplots(len(cases), 2)

    for i, case in enumerate(cases):
        A = test_data()
        B, perm = case(A)
        axs[i, 0].spy(csc_matrix(A))  # ,markersize=5, precision=0.1)
        axs[i, 1].spy(B, color='red', marker="s")

    plt.show()


if __name__ == '__main__':
    # test()
    # test2()
    plot_results()
