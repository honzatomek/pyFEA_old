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

    t = np.array([[c, s, 0.0, 0.0, 0.0, 0.0],
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
    ke = np.array([[EA / l, 0.0, 0.0, -EA / l, 0.0, 0.0],
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


def beam2d_load(x1: np.ndarray, x2: np.ndarray, fx=0.0: float, fz=0.0: float, my=0.0: float):
    """
    Function computes element load vector from distributed elemental load (2D)
    In:
        x1 - coordinates of start of element [x1, z1]
        x2 - coordinates of end of element [x1, z1]
        fx - element axial distributed load (positive = x1 -> x2)
        fz - element transversal distributed load (positive = if x1 -> x2 = left to right
             then fz+ = bottom to top)
        my - element distributed moment load (positive = if x1 -> x2 = left to right then
             my+ = counter clockwise), not yet implemented
    Out:
        f  - element load vector in 2D
    """
    logging.debug(f'beam2d_load({x1}, {x2}, {fx}, {fz}, {my})')
    length = math.sqrt((x2[0] - x1[0]) ** 2 + (x2[1] - x1[1]) ** 2)
    # load vector in LCS
    fl = np.array([fx * length / 2.0,
                   -fz * length / 2.0,
                   1 / 12 * fz * length * length,
                   fx * l,
                   - fz * length / 2.0,
                   - 1 / 12 * fz * length * length],
                  dtype=float)
    # transformation matrix
    t = beam2d_t(x1, x2)

    f = t.T @ fl

    return f


def beam2d_temp(EA=0.0: float, a=0.0: float, t=0.0: float, t0=0.0: float):
    """
    Function computes the load vector from uniform thermal load on beam in 2D
    In:
        EA - Youngs Modulus times section Area
        a  - Longitudiinal thermal expansion coefficient
        t  - uniform thermal load on beam element
        t0 - base temperature value
    Out:
        f  - load vector from uniform thermal load on beam in 2D GCS
    """
    logging.debug(f'beam2d_temp({EA}, {a}, {t}, {t0})')
    fl = np.array([-EA * a * (t - t0),
                   0.0,
                   0.0,
                   EA * a * (t - t0),
                   0.0,
                   0.0],
                  dtype=float)
    # transformation matrix
    t = beam2d_t(x1, x2)

    # f = t.T.dot(fl)
    f = t.T @ fl

    return f


def beam2d_initialstress(x1: np.ndarray, x2: np.ndarray, N=0.0: float):
    """
    Function computes the matrix of beam initial stresses for use in stability
    (Kirchhoff, 2D)
    In:
        x1 - coordinates of start of element [x1, z1]
        x2 - coordinates of end of element [x1, z1]
        N  - axial force in element
    Out:
        ks - matrix of element initial stresses in GCS (6, 6)
    """
    logging.debug(f'beam2d_initialstress({x1}, {x2}, {N})')
    length = math.sqrt((x2[0] - x1[0]) ** 2 + (x2[1] - x1[1]) ** 2)
    l = length
    l2 = l * l
    # initial stress matrix in LCS
    kl = (N / l) * np.array([[0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                             [0.0, 6.0 / 5.0, -l / 10.0, 0.0, -6.0 / 5.0, -l / 10.0],
                             [0.0, -l / 10.0, 2.0 * l2 / 15.0, 0.0 , l / 10.0, -l2 / 30.0],
                             [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                             [0.0, -6.0 / 5.0, l / 10.0, 0.0, 6.0 / 5.0, l / 10.0],
                             [0.0, -l / 10.0, -l2 / 30.0, 0.0 , l / 10.0, 2.0 * l2 / 15.0],
                            dtype=float)
    kl[0][0] = min(abs(kl[1][1]), abs(kl[2][2])) / 1000.0
    kl[0][3] = -kl[0][0]
    kl[3][0] = kl[0][3]
    kl[3][3] = kl[0][0]
    # transformation matrix
    t = beam2d_t(x1, x2)
    # initial stress matrix in GCS
    # ks = t.T.dot(kl.dot(t))
    ks = t.T @ kl @ t

    return ks


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


def assemble_load(lm: np.ndarray, f: np.ndarray, fe: np.ndarray, eID: int):
    """
    Function to assemble global load vector in GCS
    In:
        lm  - array of code numbers
        f   - global load vector
        fe  - element load vector
        eID - element ID (1 based)
    Out:
        f   - global load vector
    """
    logging.debug(f'assemble_load() element {eID}')
    ndof = f.shape[0]
    for i in range(ndof):
        ia = lm[eID - 1][i]
        if ia != 0:
            f[ia - 1][0] += fe[i][0]


def beam2d_postpro(x1: np.ndarray, x2, np.ndarray, EA: float, EI: float, u: np.ndarray):
    """
    Function to get element inner forces in LCS (2D)
    In:
        x1 - coordinates of start of element [x1, z1]
        x2 - coordinates of end of element [x1, z1]
        EA - Youngs Modulus times section Area
        EI - Youngs Modulus times Moment of Inertia
        u  - vector of beam end displacements in GCS (2D)
    Out:
        s  - vector of beam inner forces in LCS (2D)
    """
    logging.debug(f'beam2d_postpro({x1}, {x2}, {EA}, {EI}, {u})')
    length = math.sqrt((x2[0] - x1[0]) ** 2 + (x2[1] - x1[1]) ** 2)
    # local element stiffness matrix
    kl = beam2d_stiffness_lcs(length, EA, EI)
    # transformation matrix
    t = beam2d_t(x1, x2)

    # s = kl.dot(t.dot(u))
    s = kl @ t @ u

    return s


def beam2d():
    logging.debug(f'beam2d()')
    # array of coordinates
    xz = np.array([[0.0, 0.0],
                   [3.0, 0.0],
                   [6.0, 0.0]], dtype=float)

    # array of code numbers
    lm = np.array([[1, 2, 3, 4, 5, 6],
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
    ke1 = beam2d_stiffness(xz[0], xz[1], EA, EI)
    logging.debug(f'ke1:\n{ke1}')
    ke2 = beam2d_stiffness(xz[1], xz[2], EA, EI)
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

    # element inner forces
    s1 = beam2d_postpro(xz[0], xz[1], EA, EI, u1)
    logging.debug(f's1:\n{s1}')
    s2 = beam2d_postpro(xz[1], xz[2], EA, EI, u2)
    logging.debug(f's2:\n{s2}')


if __name__ == '__main__':
    logging.debug(f'{__file__} started')
    beam2d()
