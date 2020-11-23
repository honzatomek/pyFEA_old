# Beam cantilever
"""
Finite ELement Analysis of Beam structure in 2D (xz), Element formulation based on Kirchhoff equations
"""

import os, sys
import math
import argparse
from configparser import ConfigParser
import numpy as np
from scipy import linalg

import logging

BASIC_FORMAT = logging.Formatter('%(message)s')
ADVANCED_FORMAT = logging.Formatter('%(asctime)6s *%(levelname).1s* %(message)s', datefmt='%H%M%S')

logging.basicConfig(level=logging.INFO, format='%(asctime)6s *%(levelname).1s* %(message)s', datefmt='%H%M%S')
# logging.basicConfig()


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
    logging.info(f'call beam2d_t()')
    logging.debug(f'call beam2d_t({x1}, {x2})')
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


def beam2d_stiffness_lcs(l: float = 0.0, EA: float = 0.0, EI: float = 0.0):
    """
    Function to compute stiffness matrix of beam element in LCS (Kirchhoff, 2D)
    In:
        l  - length of element
        EA - Youngs Modulus times section Area
        EI - Youngs Modulus times Moment of Inertia
    Out:
        ke - element stiffness matrix in 2D (6, 6)
    """
    logging.info(f'call beam2d_stiffness_lcs()')
    logging.debug(f'call beam2d_stiffness_lcs({l}, {EA}, {EI})')
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


def beam2d_stiffness(x1: np.ndarray, x2: np.ndarray, EA: float = 0.0, EI: float = 0.0):
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
    logging.info(f'call beam2d_stiffness()')
    logging.debug(f'call beam2d_stiffness({x1}, {x2}, {EA}, {EI})')
    length = math.sqrt((x2[0] - x1[0]) ** 2 + (x2[1] - x1[1]) ** 2)
    # local element stiffness
    kl = beam2d_stiffness_lcs(length, EA, EI)
    # transformation matrix
    t = beam2d_t(x1, x2)

    # transformation LCS -> GCS
    ke = t.T @ kl @ t

    return ke


def beam2d_load(x1: np.ndarray, x2: np.ndarray, fx: float = 0.0, fz: float = 0.0, my: float = 0.0):
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
    logging.info(f'call beam2d_load()')
    logging.debug(f'call beam2d_load({x1}, {x2}, {fx}, {fz}, {my})')
    length = math.sqrt((x2[0] - x1[0]) ** 2 + (x2[1] - x1[1]) ** 2)
    # load vector in LCS
    fl = np.array([fx * length / 2.0,
                   -fz * length / 2.0,
                   1 / 12 * fz * length * length,
                   fx * length,
                   - fz * length / 2.0,
                   - 1 / 12 * fz * length * length],
                  dtype=float)
    # transformation matrix
    t = beam2d_t(x1, x2)

    f = t.T @ fl

    return f


def beam2d_temp(x1: np.ndarray, x2: np.ndarray, EA: float = 0.0, a: float = 0.0, t: float = 0.0, t0: float = 0.0):
    """
    Function computes the load vector from uniform thermal load on beam in 2D
    In:
        x1 - coordinates of start of element [x1, z1]
        x2 - coordinates of end of element [x1, z1]
        EA - Youngs Modulus times section Area
        a  - Longitudiinal thermal expansion coefficient
        t  - uniform thermal load on beam element
        t0 - base temperature value
    Out:
        f  - load vector from uniform thermal load on beam in 2D GCS
    """
    logging.info(f'call beam2d_temp()')
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


def beam2d_initialstress(x1: np.ndarray, x2: np.ndarray, N: float = 0.0):
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
    logging.info(f'call beam2d_initialstress()')
    logging.debug(f'call beam2d_initialstress({x1}, {x2}, {N})')
    length = math.sqrt((x2[0] - x1[0]) ** 2 + (x2[1] - x1[1]) ** 2)
    l = length
    l2 = l * l
    # initial stress matrix in LCS
    kl = (N / l) * np.array([[0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                             [0.0, 6.0 / 5.0, -l / 10.0, 0.0, -6.0 / 5.0, -l / 10.0],
                             [0.0, -l / 10.0, 2.0 * l2 / 15.0, 0.0 , l / 10.0, -l2 / 30.0],
                             [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                             [0.0, -6.0 / 5.0, l / 10.0, 0.0, 6.0 / 5.0, l / 10.0],
                             [0.0, -l / 10.0, -l2 / 30.0, 0.0 , l / 10.0, 2.0 * l2 / 15.0]],
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
    logging.info(f'call assemble() element {eID}')
    logging.debug(f'call assemble({lm}, {K}, {ke}, {eID})')
    ndof = ke.shape[0]
    for i in range(ndof):
        ia = lm[eID - 1][i]
        if ia != 0:
            for j in range(ndof):
                ja = lm[eID - 1][j]
                if ja != 0:
                    K[ia - 1][ja - 1] += ke[i][j]
    # K[lm[eID - 1] - 1, :][:, lm[eID - 1] - 1] += ke


def assemble_load_nodal(lmn: np.ndarray, fn: np.ndarray):
    """
    Function to assemble nodal loads into global right side vector
    :param lmn:  node DOF localisation matrix
    :param fn:   array of nodal loads [lpatID, ndID, Fx, Fz, My]
    :return:
    """
    f = np.zeros((lmn.max(), 1), dtype=float)
    for fi in fn:
        lpat = int(f[0])
        ndID = int(f[1])
        for i in range(lmn[ndID - 1].shape[0]):
            f[lmn[ndID - 1][i] - 1] = fi[i + 2]

    return f


def assemble_load_elemental(lme: np.ndarray, f: np.ndarray, fe: np.ndarray, eID: int):
    """
    Function to assemble global load vector in GCS
    In:
        lme - array of code numbers
        f   - global load vector
        fe  - element load vector
        eID - element ID (1 based)
    Out:
        f   - global load vector
    """
    logging.info(f'call assemble_load() element {eID}')
    logging.debug(f'call assemble_load({lme}, {f}, {fe}, {eID})')
    ndof = f.shape[0]
    for i in range(ndof):
        ia = lme[eID - 1][i]
        if ia != 0:
            f[ia - 1][0] += fe[i][0]


def beam2d_postpro(x1: np.ndarray, x2: np.ndarray, u: np.ndarray, EA: float = 0.0, EI: float = 0.0):
    """
    Function to get element inner forces in LCS (2D)
    In:
        x1 - coordinates of start of element [x1, z1]
        x2 - coordinates of end of element [x1, z1]
        u  - vector of beam end displacements in GCS (2D)
        EA - Youngs Modulus times section Area
        EI - Youngs Modulus times Moment of Inertia
    Out:
        s  - vector of beam inner forces in LCS (2D)
    """
    logging.info(f'call beam2d_postpro()')
    logging.debug(f'call beam2d_postpro({x1}, {x2}, {u}, {EA}, {EI})')
    length = math.sqrt((x2[0] - x1[0]) ** 2 + (x2[1] - x1[1]) ** 2)
    # local element stiffness matrix
    kl = beam2d_stiffness_lcs(length, EA, EI)
    # transformation matrix
    t = beam2d_t(x1, x2)

    # s = kl.dot(t.dot(u))
    s = kl @ t @ u

    return s


def localisation_matrix(nd: np.ndarray, el: np.ndarray, cs: np.ndarray):
    logging.info(f'call localisation_matrix()')
    logging.debug(f'call localisation_matrix({nd}, {el}, {cs})')
    ndofs = 0
    ncdofs = 0
    lmn = np.zeros((nd.shape[0], 3), dtype=int)
    lme = np.zeros((el.shape[0], el.shape[1] * 3), dtype=int)

    # process constrained DOFs first
    for c in cs:
        for i, dof in enumerate(c[1:]):
            if dof == 1:
                ndofs += 1
                lmn[c[0] - 1][i] = ndofs
    ncdofs = ndofs

    # then process elements
    for i in range(el.shape[0]):
        for j in range(el.shape[1]):
            for k in range(lmn.shape[1]):
                if lmn[el[i][j] - 1][k] == 0:
                    ndofs += 1
                    lmn[el[i][j] - 1][k] = ndofs
                    lme[i][j * 3 + k] = ndofs
                else:
                    lme[i][j * 3 + k] = lmn[el[i][j] - 1][k]

    return ndofs, ncdofs, lmn, lme


def logging_array(title: str, arr: np.ndarray, header_list: list, dtype: list = None, short: bool = False):
    """
    Function to print numpy ndarray to logger, int is printed as %8n, float as %16.5f
    In:
        arr - numpy ndarray to be printed
    """
    fmth = []
    fmtv = []
    if dtype is None:
        fmth.append('  {0:^8s}')
        fmtv.append('  {0:8n}')
        for i, val in enumerate(arr[0]):
            if 'int' in type(val).__name__:
                fmth.append(' {0:^8s}')
                fmtv.append(' {0:8n}')
            elif 'float' in type(val).__name__:
                if short:
                    fmth.append(' {0:^10s}')
                    fmtv.append(' {0:10.3e}')
                else:
                    fmth.append(' {0:^16s}')
                    fmtv.append(' {0:16.5f}')
            else:
                fmth.append(' {0:^16s}')
                fmtv.append(' {0:16s}')
    else:
        for dt in dtype:
            if dt == 'int':
                fmth.append(' {0:^8s}')
                fmtv.append(' {0:8n}')
            elif dt == 'float':
                fmth.append(' {0:^16s}')
                fmtv.append(' {0:16.5f}')
            else:
                fmth.append(' {0:^16s}')
                fmtv.append(' {0:16s}')
            fmth[0] = ' ' + fmth[0]
            fmtv[0] = ' ' + fmtv[0]

    header = '\n' + ''.join([fmth[i].format(header_list[i]) for i in range(len(header_list))])
    delimit = '\n ' + (len(header) - 1) * '-'

    message = delimit
    message += header.rstrip(' ')
    message += delimit
    for i in range(arr.shape[0]):
        message += '\n' + fmtv[0].format(i + 1) + ''.join([fmtv[j + 1].format(arr[i][j]) for j in range(arr.shape[1])])
    message += delimit
    logging.info(f' >>> {title}:\n{message}\n')


def logging_table(title: str, arr: list, fmt: str = '8n'):
    """
    Function to print 2D array of 2 columns to logger
    In:
        arr - 2D list to print [name, value]
        fmt - format of value, default = 8n
    """
    fmtv = '  {0:16s} = {1:' + fmt + '}'
    message = ['']
    for i in range(len(arr)):
        message.append(fmtv.format(arr[i][0], arr[i][1]))
    delimit = ' ' + len(message[1]) * '-'
    message[0] = delimit
    message.append(delimit)
    message = '\n' + '\n'.join(message)
    logging.info(f' >>> {title}:\n{message}\n')


def load_dat(file: str, dtype: type = float):
    """
    Function to load dat file as numpy array
    """
    logging.info(f'read {file} as {dtype.__name__}')
    try:
        m = np.loadtxt(file, ndmin=2, dtype=dtype, comments=('#'))
        return m
    except Exception as e:
        logging.exception(f'Failed reading {file}')


def beam2d(structure_directory: str = 'console'):
    logging.info('call beam2d()')
    cfg = ConfigParser()
    cfg.read(os.path.join(os.path.dirname(__file__), f'structures/{structure_directory}/g.ini'))
    solver = cfg['DEFAULT']['solver']

    # array of node coordinates
    nd = load_dat(os.path.join(os.path.dirname(__file__), f'structures/{structure_directory}/nd.dat'), dtype=float)
    nnode = nd.shape[0]
    logging.debug(f'nd:\n{nd}')
    logging_array('Node Coordinates', nd, ['nID', 'x', 'z'])

    # array of element connectivity
    el = load_dat(os.path.join(os.path.dirname(__file__), f'structures/{structure_directory}/el.dat'), dtype=int)
    nelem = el.shape[0]
    logging.debug(f'el:\n{el}')
    logging_array('Element Connectivity', el, ['eID', 'nd1', 'nd2'])

    # array of suppressed nodes
    cs = load_dat(os.path.join(os.path.dirname(__file__), f'structures/{structure_directory}/cs.dat'), dtype=int)
    logging_array('Nodal constraints', cs, ['cID', 'nID', 'Cx', 'Cz', 'Cy'])

    # array of nodal loads
    fn = load_dat(os.path.join(os.path.dirname(__file__), f'structures/{structure_directory}/fn.dat'))
    logging_array('Nodal loads', fn, ['ldID', 'lpatID', 'nID', 'Fx', 'Fz', 'My'],
                  dtype=['int', 'int', 'int', 'float', 'float', 'float'])

    # DOF localisation matrices
    ndofs, ncdofs, lmn, lme = localisation_matrix(nd, el, cs)
    logging.debug(f'lmn:\n{lmn}')
    logging_array('Node DOF numbers', lmn, ['nID', 'dofX', 'dofZ', 'dofFi'])
    logging.debug(f'lme:\n{lme}')
    logging_array('Element DOF numbers', lme, ['eID', 'dofX1', 'dofZ1', 'dofFi1', 'dofX2', 'dofZ2', 'dofFi2'])

    # model info
    logging_table('Model info', [['nodes', nnode], ['elements', nelem], ['dofs', ndofs], ['dofs constrained', ncdofs]])

    # load vector
    # f = load_dat(os.path.join(os.path.dirname(__file__), f'structures/{structure_directory}/f.dat'), dtype=float)
    f = assemble_load_nodal(lmn, fn)
    # f = np.zeros((ndofs, 1), dtype=float)
    logging.debug(f'f:\n{f}')
    logging_array('Right side vector', f, ['dofID', 'F'])

    # property values
    EA = 1.0
    EI = 1.0

    # preparation of load vector, stiffness matrix, displacement vector
    K = np.zeros((ndofs, ndofs), dtype=float)
    u = np.zeros((ndofs, 1), dtype=float)

    # creation of local stiffness matrix and localisation
    ke = []
    for i in range(nelem):
        # ke.append(beam2d_stiffness(xz[i, :2], xz[i, 2:], EA, EI))
        ke.append(beam2d_stiffness(nd[el[i][0] - 1], nd[el[i][1] - 1], EA, EI))
        logging.debug(f'ke{i + 1}:\n{ke[i]}')
        # localisation
        assemble(lme, K, ke[i], i + 1)
    logging.debug(f'K:\n{K}')
    tmp = ['DOF']
    tmp.extend(['{0:n}'.format(i) for i in range(ndofs)])
    logging_array('Stiffness Matrix', K, tmp, short=True)
    del tmp

    # solving the displacements
    u[ncdofs:] = linalg.solve(K[ncdofs:, ncdofs:], f[ncdofs:])
    # logging.info(f'u:\n{u}')
    logging_array('Resulting displacements', u, ['dofID', 'du'])

    # reactions
    f[:ncdofs] = K[:ncdofs, ncdofs:] @ u[ncdofs:]
    logging.info(f'f:\n{f}')
    logging_array('Resulting reactions', f[:ncdofs], ['dofID', 'R'])

    # element displacements
    ue = []
    for i in range(nelem):
        ue.append(u[lme[i, :] - 1])
        logging.info(f'u{i + 1}:\n{ue[i]}')

    # element inner forces
    se = []
    for i in range(nelem):
        se.append(beam2d_postpro(nd[el[i][0] - 1], nd[el[i][1] - 1], ue[i], EA, EI))
        logging.info(f'se{i + 1}:\n{se[i]}')


if __name__ == '__main__':
    logger = logging.getLogger()
    # logger_handler = logging.StreamHandler()
    # logger.addHandler(logger_handler)
    logger_handler = logger.handlers[0]
    logger_handler.setFormatter(ADVANCED_FORMAT)
    logger_handler.setLevel(logging.INFO)

    logging.info(f'{__file__} started')
    parser = argparse.ArgumentParser()
    parser.add_argument('structure', type=str, help='directory name of structure from ./structures directory')

    args = parser.parse_args()

    beam2d(args.structure)
