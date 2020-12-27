# From: https://codereview.stackexchange.com/q/19088
# Theory: http://ciprian-zavoianu.blogspot.com/2009/01/project-bandwidth-reduction.html
# Scipy followup: https://scicomp.stackexchange.com/questions/24817/applying-the-result-of-cuthill-mckee-in-scipy
# Scipy: https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csgraph.reverse_cuthill_mckee.html#scipy.sparse.csgraph.reverse_cuthill_mckee
# Matplotlib plot sparse matrix: https://matplotlib.org/3.1.1/gallery/images_contours_and_fields/spy_demos.html#sphx-glr-gallery-images-contours-and-fields-spy-demos-py

import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import reverse_cuthill_mckee


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


def test():
    """
    test the RCM loop
    """
    print('Script solution:')
    A = np.diag(np.ones(8))
    nzc = [[4], [2, 5, 7], [1, 4], [6], [0, 2], [1, 7], [3], [1, 5]]

    for i in range(len(nzc)):
        for j in nzc[i]:
            A[i, j] = 1
    print(A)
    # define the Result queue
    R = ["C"] * A.shape[0]
    adj = getAdjacency(A)
    degree = getDegree(A)
    digar = np.array(degree)
    pivots = list(np.where(digar == digar.min())[0])
    inl = []
    Res = np.array(RCM_loop(degree, 0, adj, pivots, inl))
    print(degree)
    print(adj)
    print("solution:", list(Res))
    print("correct:", [6, 3, 7, 5, 1, 2, 4, 0])
    # B = A[Res, Res]
    B = np.array(A)
    for i in range(B.shape[0]):
        B[:, i] = B[Res, i]
    for i in range(B.shape[0]):
        B[i, :] = B[i, Res]
    print(B)
    return csr_matrix(A), csr_matrix(B)


def test2():
    print('SciPy solution:')
    A = np.diag(np.ones(8))
    nzc = [[4], [2, 5, 7], [1, 4], [6], [0, 2], [1, 7], [3], [1, 5]]

    for i in range(len(nzc)):
        for j in nzc[i]:
            A[i, j] = 1
    print(A)

    A = csr_matrix(A)
    Res = reverse_cuthill_mckee(A, False)
    print("solution:", list(Res))
    print("correct:", [6, 3, 7, 5, 1, 2, 4, 0])
    B = A[np.ix_(Res, Res)]
    print(B.todense())
    return A, B


def plot_results():
    import matplotlib.pyplot as plt
    import numpy as np

    fig, axs = plt.subplots(2, 2)
    ax1 = axs[0, 0]
    ax2 = axs[0, 1]
    ax3 = axs[1, 0]
    ax4 = axs[1, 1]

    x = np.random.randn(20, 20)
    A1, B1 = test()
    A2, B2 = test2()

    # ax1.spy(A1, markersize=5)
    ax1.spy(A1)
    ax2.spy(B1)

    ax3.spy(A2)
    ax4.spy(B2)

    plt.show()


if __name__ == '__main__':
    # test()
    # test2()
    plot_results()
