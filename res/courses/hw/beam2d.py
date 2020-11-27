# Beam cantilever

import math
import numpy as np
from scipy import linalg

import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)6s *%(levelname).1s* %(message)s', datefmt='%H%M%S')


def beam2d_t(x1: np.ndarray, x2: np.ndarray):
    """
    function computes transformation matrix (GCS -> LCS) of beam in 2d
    (Rl = T * Rg)
    In:
        x1 - coordinates of start of element [x1, z1]
        x2 - coordinates of end of element [x1, z1]
    Out:
        t  - beam transformation matrix in 2D (6, 6)
    """
    logging.debug(f'beam2d_t({x1}, {x2})')
    length = math.sqrt((x2[0] - x1[0]) ** 2 + (x2[1] - x1[1]) ** 2)
    c = (x2[0] - x1[0]) / length
    s = (x2[1] - x1[1]) / length

    t = np.asarray([[c, s, 0.0, 0.0, 0.0, 0.0],
                    [-s, c, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, c, s, 0.0],
                    [0.0, 0.0, 0.0, -s, c, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0, 1.0]],
                   dtype=float)

    return t


def beam2d_stiffness_lcs(l: float, EA: float, EI: float):
    """
    Function to compute stiffness matrix of beam element in LCS (Kirchhoff, 2D)
    In:
        l  - length of element
        EA - Youngs Modulus times section Area
        EI - Youngs Modulus times Moment of Inertia
    Out:
        ke - element stiffness matrix in 2D (6, 6)
    """
    logging.debug(f'beam2d_stiffness_lcs({l}, {EA}, {EI})')
    l2 = l * l
    l3 = l2 * l
    ke = np.asarray([[EA / l, 0.0, 0.0, -EA / l, 0.0, 0.0],
                     [0.0, 12.0 * EI / l3, -6.0 * EI / l2, 0.0, -12.0 * EI / l3, -6.0 * EI / l2],
                     [0.0, -6.0 * EI / l2, 4.0 * EI / l, 0.0, 6.0 * EI / l2, 2.0 * EI / l],
                     [-EA / l, 0.0, 0.0, EA / l, 0.0, 0.0],
                     [0.0, -12.0 * EI / l3, 6.0 * EI / l2, 0.0, 12.0 * EI / l3, 6.0 * EI / l2],
                     [0.0, -6.0 * EI / l2, 2.0 * EI / l, 0.0, 6.0 * EI / l2, 4.0 * EI / l]],
                    dtype=float)

    return ke


def beam2d_stiffness(x1: np.ndarray, x2: np.ndarray, EA: float, EI: float):
    """
    Function to compute stiffness matrix of beam element in GCS (Kirchhoff, 2D)
    In:
        x1 - coordinates of start of element [x1, z1]
        x2 - coordinates of end of element [x1, z1]
        EA - Youngs Modulus times section Area
        EI - Youngs Modulus times Moment of Inertia
    Out:
        ke - element stiffness matrix in 2D (6, 6)
    """
    logging.debug(f'beam2d_stiffness({x1}, {x2}, {EA}, {EI})')
    length = math.sqrt((x2[0] - x1[0]) ** 2 + (x2[1] - x1[1]) ** 2)
    # local element stiffness
    kl = beam2d_stiffness_lcs(length, EA, EI)
    # transformation matrix
    t = beam2d_t(x1, x2)

    # transformation LCS -> GCS
    ke = t.T @ kl @ t

    return ke


def assemble(lm: np.ndarray, K: np.ndarray, ke: np.ndarray, eID: int):
    """
    Function for localisation of element stiffness matrix into
    global stiffness matrix
    In:
        lm  - array of code numbers
        K   - global stiffness matrix
        ke  - element stiffness matrix
        eID - element ID (1 based)
    Out:
        K   - global stiffness matrix
    """
    logging.debug(f'assemble() element {eID}')
    ndof = ke.shape[0]
    for i in range(ndof):
        ia = lm[eID - 1][i]
        if ia != 0:
            for j in range(ndof):
                ja = lm[eID - 1][j]
                if ja != 0:
                    K[ia - 1][ja - 1] += ke[i][j]


def beam2d():
    logging.debug(f'beam2d()')
    # array of coordinates
    xz = np.asarray([[0.0, 0.0],
                     [3.0, 0.0],
                     [6.0, 0.0]], dtype=float)

    # array of code numbers
    lm = np.asarray([[1, 2, 3, 4, 5, 6],
                     [4, 5, 6, 7, 8, 9]], dtype=int)

    # number of elements
    nelem = 2

    # property values
    EA = 1.0
    EI = 1.0

    # preparation of load vector, stiffness matrix, displacement vector
    f = np.zeros((9, 1), dtype=float)
    K = np.zeros((9, 9), dtype=float)
    u = np.zeros((9, 1), dtype=float)

    # creation of local stiffness matrix
    ke1 = beam2d_stiffness(xz[0][:], xz[1][:], EA, EI)
    logging.debug(f'ke1:\n{ke1}')
    ke2 = beam2d_stiffness(xz[1][:], xz[2][:], EA, EI)
    logging.debug(f'ke2:\n{ke2}')

    # localisation
    assemble(lm, K, ke1, 1)
    assemble(lm, K, ke2, 2)
    logging.debug(f'K:\n{K}')

    # load vector
    f[7] = 1.0
    logging.debug(f'f:\n{f}')

    # solving the displacements
    # print(f'K[3:, 3:] shape {K[3:, 3:].shape}')
    u[3:] = linalg.solve(K[3:, 3:], f[3:])
    logging.debug(f'u:\n{u}')

    # reactions
    # f[:3] = K[:3, 3:].dot(u[3:])
    f[:3] = K[:3, 3:] @ u[3:]
    logging.debug(f'f:\n{f}')

    # element displacements
    u1 = u[lm[0, :] - 1]
    logging.debug(f'u1:\n{u1}')
    u2 = u[lm[1, :] - 1]
    logging.debug(f'u2:\n{u2}')


if __name__ == '__main__':
    logging.debug(f'{__file__} started')
    beam2d()
