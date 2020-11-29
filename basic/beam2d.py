# python FEM for 2D beams
"""
Finite ELement Analysis of Beam structure in 2D (xz), Element formulation based on Kirchhoff equations
"""

import os, sys
import math
import argparse
import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
from configparser import ConfigParser
import numpy as np
from scipy import linalg
from scipy.sparse import linalg as sclinalg

import logging

BASIC_FORMAT = logging.Formatter('%(message)s')
ADVANCED_FORMAT = logging.Formatter('%(asctime)6s *%(levelname).1s* %(message)s', datefmt='%H%M%S')

logging.basicConfig(level=logging.INFO, format='%(asctime)6s *%(levelname).1s* %(message)s', datefmt='%H%M%S')
# logging.basicConfig()


def beam2d_t(x1: np.ndarray, x2: np.ndarray):
    """
    Function computes transformation matrix (GCS -> LCS) of beam in 2d
    (Rl = T * Rg)
    :param x1: Coordinates of start of element [x1, z1]
    :param x2: Coordinates of end of element [x1, z1]
    :return:   t  - beam transformation matrix in 2D (6, 6)
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


def beam2d_stiffness_lcs(l: float = 0.0, A: float = 1.0, I: float = 1.0, E: float = 1.0):
    """
    Function to compute stiffness matrix of beam element in LCS (Kirchhoff, 2D)
    :param l: length of element
    :param A: Section Area
    :param I: Moment of Inertia
    :param E: Youngs Modulus
    :return:  ke = beam element stiffness matrix in LCS 2D (6, 6)
    """
    logging.info(f'call beam2d_stiffness_lcs()')
    logging.debug(f'call beam2d_stiffness_lcs({l}, {A}, {I}, {E})')
    l2 = l * l
    l3 = l2 * l
    EA = E * A
    EI = E * I
    ke = np.array([[EA / l, 0.0, 0.0, -EA / l, 0.0, 0.0],
                   [0.0, 12.0 * EI / l3, -6.0 * EI / l2, 0.0, -12.0 * EI / l3, -6.0 * EI / l2],
                   [0.0, -6.0 * EI / l2, 4.0 * EI / l, 0.0, 6.0 * EI / l2, 2.0 * EI / l],
                   [-EA / l, 0.0, 0.0, EA / l, 0.0, 0.0],
                   [0.0, -12.0 * EI / l3, 6.0 * EI / l2, 0.0, 12.0 * EI / l3, 6.0 * EI / l2],
                   [0.0, -6.0 * EI / l2, 2.0 * EI / l, 0.0, 6.0 * EI / l2, 4.0 * EI / l]],
                  dtype=float)

    return ke


def beam2d_stiffness(x1: np.ndarray, x2: np.ndarray, A: float = 1.0, I: float = 1.0, E: float = 1.0):
    """
    Function to compute stiffness matrix of beam element in GCS (Kirchhoff, 2D)
    :param x1: Coordinates of start of element [x1, z1]
    :param x2: Coordinates of end of element [x1, z1]
    :param A:  Section Area
    :param I:  Moment of Inertia
    :param E:  Youngs Modulus
    :return:   ke - beam element stiffness matrix in GCS 2D (6, 6)
    """
    logging.info(f'call beam2d_stiffness()')
    logging.debug(f'call beam2d_stiffness({x1}, {x2}, {A}, {I}, {E})')
    length = math.sqrt((x2[0] - x1[0]) ** 2 + (x2[1] - x1[1]) ** 2)
    EA = E * A
    EI = E * I
    # local element stiffness
    kl = beam2d_stiffness_lcs(length, EA, EI)
    # transformation matrix
    t = beam2d_t(x1, x2)

    # transformation LCS -> GCS
    ke = t.T @ kl @ t

    return ke


def beam2d_stiffness_timoshenko_lcs(l: float = 1.0, A: float = 1.0, I: float = 1.0, E: float = 1.0,
                                    nu: float = 0.3, k: float = (5.0 / 6.0)):
    """
    Element stiffness matrix of beam element (Timoshenko, 2D)
    axial + bending 1 integration point, shear 2 integration points, reduced integration
    due to shear locking
    :param l:  Element length
    :param A:  Cross section area
    :param E:  Young's Modulus
    :param nu: Poisson's ratio
    :param k:  Timoshenko shear correction coefficient (5/6 = rectangular section, 6/7 = circular section)
    :return:   ke - shear part of element stiffness matrix in 2D
    """
    logging.info(f'call beam2d_stiffness_timoshenko_lcs()')
    logging.debug(f'call beam2d_stiffness_timoshenko_lcs({l}, {A}, {E}, {nu}, {k})')
    G = E / (2 * (1 + nu))
    kuu = np.array([[1, -1], [-1, 1]], dtype=float) * E * A / l
    kww = np.array([[1, -1], [-1, 1]], dtype=float) * k * G * A / l
    kwf = np.array([[-0.5, -0.5], [0.5, 0.5]], dtype=float) * k * G * A
    # kff = np.array([[1, -1], [-1, 1]], dtype=float) * E * I / l \
    #       + np.array([[1 / 3, 1 / 6], [1 / 6, 1 / 3]], dtype=float) * k * G * A * l  # full integration
    kff = np.array([[1, -1], [-1, 1]], dtype=float) * E * I / l \
          + np.array([[1 / 4, 1 / 4], [1 / 4, 1 / 4]], dtype=float) * k * G * A * l    # reduced integration

    ke = np.zeros((6, 6), dtype=float)
    ke[[0, 3], [[0], [3]]] += kuu
    ke[[1, 4], [[1], [4]]] += kww
    ke[[1, 4], [[2], [5]]] += kwf.T
    ke[[2, 5], [[1], [4]]] += kwf
    ke[[2, 5], [[2], [5]]] += kff

    return ke


def beam2d_stiffness_timoshenko(x1: np.ndarray, x2: np.ndarray,
                                A: float = 1.0, I: float = 1.0, E: float = 1.0, nu: float = 0.3):
    """
    Function to compute stiffness matrix of beam element in GCS (Timoshenko, 2D)
    :param x1: Coordinates of start of element [x1, z1]
    :param x2: Coordinates of end of element [x1, z1]
    :param A:  Section Area
    :param I:  Moment of Inertia
    :param E:  Young's Modulus
    :param nu: Poison's ratio
    :return:   ke - beam element stiffness matrix in GCS 2D (6, 6)
    """
    logging.info(f'call beam2d_stiffness_timoshenko()')
    logging.debug(f'call beam2d_stiffness_timoshenko({x1}, {x2}, {A}, {I}, {E}, {nu})')
    length = math.sqrt((x2[0] - x1[0]) ** 2 + (x2[1] - x1[1]) ** 2)
    EA = E * A
    EI = E * I
    # local element stiffness
    # kl = beam2d_stiffness_timoshenko_axial(length, A, E) \
    #      + beam2d_stiffness_timoshenko_bending(length, I, E) \
    #      + beam2d_stiffness_timoshenko_shear(length, A, E, nu, 5.0 / 6.0)
    kl = beam2d_stiffness_timoshenko_lcs(length, A, I, E, nu, 5.0 / 6.0)
    # transformation matrix
    t = beam2d_t(x1, x2)

    # transformation LCS -> GCS
    ke = t.T @ kl @ t

    return ke


def beam2d_mass_lumped(L: float = 1.0, A: float = 1.0, ro: float = 1.0, nsm: float = 0.0):
    """
    Function to compute lumped mass matrix of beam element in LCS (2D)
    :param L:   Element Length
    :param A:   Section Area
    :param ro:  Element Material Density
    :param nsm: Nonstructural Mass per unit length
    :return:    mle - beam element lumped mass matrix in LCS 2D (6, 6)
    """
    logging.info(f'call beam2d_mass_lumped()')
    logging.debug(f'call beam2d_mass_lumped({L}, {A}, {ro}, {nsm})')
    # structural mass
    sm = A * L * ro
    # nonstructural mass
    nm = L * nsm
    # local lumped element mass matrix
    mle = np.eye(6, dtype=float) * (sm + nm) / 2
    mle[2][2] = 0.0
    mle[5][5] = 0.0

    return mle


def beam2d_mass_consistent(L: float = 1.0, A: float = 1.0, ro: float = 1.0, nsm: float = 0.0):
    """
    Function to compute consistent mass matrix of beam element in LCS (2D)
    :param L:   Element Length
    :param A:   Section Area
    :param ro:  Element Material Density
    :param nsm: Nonstructural Mass per unit length
    :return:    mce - beam element consistent mass matrix in LCS 2D (6, 6)
    """
    logging.info(f'call beam2d_mass_consistent()')
    logging.debug(f'call beam2d_mass_consistent({L}, {A}, {ro}, {nsm})')
    # structural mass
    sm = A * L * ro
    # nonstructural mass
    nm = L * nsm
    # local lumped element mass matrix
    mce = np.zeros((6, 6), dtype=float)
    mce = np.array([[140.0, 0.0, 0.0, 70.0, 0.0, 0.0],
                    [0.0, 156.0, 22.0 * L, 0.0, 54.0, -13.0 * L],
                    [0.0, 22.0 * L, 4.0 * (L ** 2.0), 0.0, 13.0 * L, -3.0 * (L ** 2.0)],
                    [70.0, 0.0, 0.0, 140.0, 0.0, 0.0],
                    [0.0, 54.0, 13.0 * L, 0.0, 156.0, -22.0 * L],
                    [0.0, -13.0 * L, -3.0 * (L ** 2), 0.0, -22.0 * L, 4.0 * (L ** 2.0)]], dtype=float)
    mce *= (sm + nm) / 420.0

    return mce


def beam2d_mass(x1: np.ndarray, x2: np.ndarray, A: float = 1.0, ro: float = 1.0, nsm: float = 0.0, mi: float = 0.5):
    """
    Function to compute mass matrix of beam element in GCS (2D)
    :param x1:  Coordinates of start of element [x1, z1]
    :param x2:  Coordinates of end of element [x1, z1]
    :param A:   Section Area
    :param ro:  Element Material Density
    :param nsm: Nonstructural Mass
    :param mi:  Consistent to Lumped Mass Matrix ratio M = (1 - mi) * Mc + mi * Ml
    :return:    me - beam element mass matrix in GCS 2D (6, 6)
    """
    logging.info(f'call beam2d_mass()')
    logging.debug(f'call beam2d_mass({x1}, {x2}, {A}, {ro}, {nsm})')
    length = math.sqrt((x2[0] - x1[0]) ** 2 + (x2[1] - x1[1]) ** 2)
    # get mass in LCS
    ml = (1.0 - mi) * beam2d_mass_consistent(length, A, ro, nsm) + mi * beam2d_mass_lumped(length, A, ro, nsm)
    # transformation matrix
    t = beam2d_t(x1, x2)

    # transformation LCS -> GCS
    me = t.T @ ml @ t

    return me


def beam2d_load(x1: np.ndarray, x2: np.ndarray, fx: float = 0.0, fz: float = 0.0):
    """
    Function computes element load vector from distributed elemental load (2D)
    :param x1: Coordinates of start of element [x1, z1]
    :param x2: Coordinates of end of element [x1, z1]
    :param fx: Element axial distributed load (positive = x1 -> x2)
    :param fz: Element transversal distributed load (positive = if x1 -> x2 = left to right
    :return:   fe - element load vector in GCS 2D (6, 1)
    """
    logging.info(f'call beam2d_load()')
    logging.debug(f'call beam2d_load({x1}, {x2}, {fx}, {fz})')
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
    # load vector in GCS
    fe = t.T @ fl

    return fe


def beam2d_temp(x1: np.ndarray, x2: np.ndarray, A: float = 1.0, E: float = 1.0, a: float = 1.0, t: float = 0.0, t0: float = 0.0):
    """
    Function computes the load vector from uniform thermal load on beam in 2D
    :param x1: Coordinates of start of element [x1, z1]
    :param x2: Coordinates of end of element [x1, z1]
    :param A:  Section Area
    :param E:  Youngs Modulus
    :param a:  Longitudinal Thermal expansion coefficient
    :param t:  Uniform thermal load on beam element
    :param t0: Base Temperature
    :return:   fe - load vector from uniform thermal load on beam in 2D GCS (6, 1)
    """
    logging.info(f'call beam2d_temp()')
    logging.debug(f'beam2d_temp({A}, {E}, {a}, {t}, {t0})')
    EA = E * A
    # load vector in LCS
    fl = np.array([-EA * a * (t - t0),
                   0.0,
                   0.0,
                   EA * a * (t - t0),
                   0.0,
                   0.0],
                  dtype=float)
    # transformation matrix
    t = beam2d_t(x1, x2)
    # load vector in GCS
    # fe = t.T.dot(fl)
    fe = t.T @ fl

    return fe


def beam2d_initialstress(x1: np.ndarray, x2: np.ndarray, N: float = 0.0):
    """
    Function computes the matrix of beam initial stresses for use in stability
    (Kirchhoff, 2D)
    :param x1: Coordinates of start of element [x1, z1]
    :param x2: Coordinates of end of element [x1, z1]
    :param N:  Axial force in element
    :return:   ks - matrix of element initial stresses in GCS (6, 6)
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
    Function for localisation of element matrix into global matrix
    :param lm:  Array of code numbers
    :param K:   Global matrix
    :param ke:  Element matrix
    :param eID: Element ID (1 based)
    :return:    K - Global stiffness matrix
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


def assemble_load_nodal(f: np.ndarray, lmn: np.ndarray, fn: np.ndarray):
    """
    Function to assemble nodal loads into global right side vector
    :param f:    Global load vector
    :param lmn:  Node DOF localisation matrix
    :param fn:   Array of nodal loads [lpatID, ndID, Fx, Fz, My]
    :return:     f - right side vector of nodal loads
    """
    for fi in fn:
        lpat = int(fi[0])
        ndID = int(fi[1])
        for i in range(lmn[ndID - 1].shape[0]):
            f[lmn[ndID - 1][i] - 1] = fi[i + 2]


def assemble_load_elemental(lme: np.ndarray, f: np.ndarray, fe: np.ndarray, eID: int):
    """
    Function to assemble global load vector in GCS
    :param lme: Array of code numbers
    :param f:   Global load vector (edited by function)
    :param fe:  Element load vector
    :param eID: Element ID (1 based)
    :return: None
    """
    logging.info(f'call assemble_load() element {eID}')
    logging.debug(f'call assemble_load({lme}, {f}, {fe}, {eID})')
    ndof = fe.shape[0]
    for i in range(ndof):
        ia = lme[eID - 1][i]
        if ia != 0:
            f[ia - 1] += fe[i]


def beam2d_postpro(x1: np.ndarray, x2: np.ndarray, u: np.ndarray, A: float = 1.0, I: float = 1.0, E: float = 1.0):
    """
    Function to get element inner forces in LCS (2D)
    :param x1: coordinates of start of element [x1, z1]
    :param x2: coordinates of end of element [x1, z1]
    :param u:  vector of beam end displacements in GCS (2D)
    :param A:  Section Area
    :param I:  Moment of Inertia
    :param E:  Youngs Modulus
    :return:   s - vector of beam inner forces in LCS (2D)
    """
    logging.info(f'call beam2d_postpro()')
    logging.debug(f'call beam2d_postpro({x1}, {x2}, {u}, {A}, {I}, {E})')
    length = math.sqrt((x2[0] - x1[0]) ** 2 + (x2[1] - x1[1]) ** 2)
    EA = E * A
    EI = E * I
    # local element stiffness matrix
    kl = beam2d_stiffness_lcs(length, EA, EI)
    # transformation matrix
    t = beam2d_t(x1, x2)

    # s = kl.dot(t.dot(u))
    s = kl @ t @ u

    return s


def localisation_matrix(nd: np.ndarray, el: np.ndarray, cs: np.ndarray):
    """
    Function to create nodal and elemental localisation matrix
    :param nd: Array of nodes
    :param el: Array of elements
    :param cs: Array of constraints
    :return:   ndofs  - number of DOFs total
               ncdofs - number of DOFs constrained
               lmn    - node to DOF localisation matrix
               lme    - elemental localisation matrix
               lmd    - DOF to node localisation matrix
    """
    logging.info(f'call localisation_matrix()')
    logging.debug(f'call localisation_matrix({nd}, {el}, {cs})')
    ndofs = 0
    lmn = np.zeros((nd.shape[0], 3), dtype=int)
    lme = np.zeros((el.shape[0], 6), dtype=int)
    lmd = []

    # process constrained DOFs first
    for c in cs:
        nID = c[0]
        for i, dof in enumerate(c[1:]):
            if dof == 1:
                ndofs += 1
                lmn[nID - 1][i] = ndofs
                lmd.append([nID, i + 1])
    ncdofs = ndofs

    # then process elements
    for i in range(el.shape[0]):
        for j in range(2):
            for k in range(3):
                if lmn[el[i][j + 2] - 1][k] == 0:
                    ndofs += 1
                    lmn[el[i][j + 2] - 1][k] = ndofs
                    lme[i][j * 3 + k] = ndofs
                    lmd.append([el[i][j + 2], k + 1])
                # process element releases (add DOF)
                elif el[i][4 + j * 3 + k] == 1:
                    ndofs += 1
                    lme[i][j * 3 + k] = ndofs
                    lmd.append([el[i][j + 2], k + 1])
                else:
                    lme[i][j * 3 + k] = lmn[el[i][j + 2] - 1][k]

    lmd = np.array(lmd, dtype=int)

    return ndofs, ncdofs, lmn, lme, lmd


def format_norm(value, format_spec):
    return format_spec.format(value)


def format_eng(value, format_spec: str = ' {0:9.3f}E{1:+03n}'):
    try:
        if value == 0.0:
            return format_spec.format(0.0, 0)
        exponent = int(math.log10(abs(value)))
        exponent = exponent - exponent % 3
        mantissa = value / (10 ** exponent)
        return format_spec.format(mantissa, exponent)
    except OverflowError as e:
        logging.exception(e)
        return str('{0:' + str(len(format_eng(1.1, format_spec))) + 'n}').format(np.infty)
    except ValueError as e:
        logging.exception(e)
        return str('{0:' + str(len(format_eng(1.1, format_spec))) + 'n}').format(np.nan)


def logging_array(title: str, arr: np.ndarray, header_list: list, dtype: list = None, eng: bool = False):
    """
    Function to print numpy ndarray to logger, int is printed as %8n, float as %16.5f, row number is printed
    also, 1 based.
    :param title:       Data Title to be printed
    :param arr:         2D Data Array
    :param header_list: List of Column Names
    :param dtype:       List of column types for print (str/int/float/eng) eng is  for engineering format 1.0E+03
    :param eng:         True/False, if True, floats are printed in engineering format %8.3fE%+03d, False %16.5f
    :return: None
    """
    fmth = []
    fmtv = []
    if dtype is None:
        fmth.append('  {0:^8s}')
        fmtv.append([format_norm, '  {0:8n}'])
        for i, val in enumerate(arr[0]):
            if 'int' in type(val).__name__:
                fmth.append(' {0:^8s}')
                fmtv.append([format_norm, ' {0:8n}'])
            elif 'float' in type(val).__name__:
                if eng:
                    fmth.append(' {0:^12s}')
                    fmtv.append([format_eng, ' {0:8.3f}E{1:+03n}'])
                else:
                    fmth.append(' {0:^16s}')
                    fmtv.append([format_norm, ' {0:16.5f}'])
            else:
                fmth.append(' {0:^16s}')
                fmtv.append([format_norm, ' {0:16s}'])
    else:
        for dt in dtype:
            if dt == 'int':
                fmth.append(' {0:^8s}')
                fmtv.append([format_norm, ' {0:8n}'])
            elif dt == 'float':
                if eng:
                    fmth.append(' {0:^12s}')
                    fmtv.append([format_eng, ' {0:8.3f}E{1:+03n}'])
                else:
                    fmth.append(' {0:^10s}')
                    fmtv.append([format_norm, ' {0:10.1f}'])
            elif dt == 'eng':
                fmth.append(' {0:^12s}')
                fmtv.append([format_eng, ' {0:8.3f}E{1:+03n}'])
            elif dt == 'str':
                fmth.append(' {0:^16s}')
                fmtv.append([format_norm, ' {0:16s}'])
            else:
                if 'E' in dt:
                    length = len(format_eng(1.1, dt))
                    fmtv.append([format_eng, dt])
                else:
                    length = len(dt.format(1.1))
                    fmtv.append([format_norm, dt])
                fmth.append(' {0:^' + str(length) + 's}')
            fmth[0] = ' ' + fmth[0]
            fmtv[0][1] = ' ' + fmtv[0][1]

    if type(header_list[0]) == list:
        header = ''
        for hl in header_list:
            header += '\n' + ''.join([fmth[i].format(hl[i]) for i in range(len(hl))])
            delimit = '\n ' + (len(header) - 1) * '-'
            header = header.rstrip(' ')
    else:
        header = '\n' + ''.join([fmth[i].format(header_list[i]) for i in range(len(header_list))])
        delimit = '\n ' + (len(header) - 1) * '-'
        header = header.rstrip(' ')

    message = delimit
    message += header
    message += delimit
    for i in range(arr.shape[0]):
        message += '\n' + fmtv[0][0](i + 1, fmtv[0][1]) \
                   + ''.join([fmtv[j + 1][0](arr[i][j], fmtv[j + 1][1]) for j in range(arr.shape[1])])
    message += delimit
    logging.info(f' >>> {title}:\n{message}\n')


def logging_table(title: str, arr: list, fmt: str = '8n'):
    """
    Function to print 2D array of 2 columns to logger
    :param title: Data Title to be printed
    :param arr:   2-column array of data to be printed
    :param fmt:   Python print format specifier (usually in curly brackets) for 2nd column, {0:8n} -> 8n
    :return:      None
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
    :param file:  Filename to read
    :param dtype: Data type of returned numpy array
    :return:      Numpy Array of read Data
    """
    logging.info(f'read {file}')
    try:
        m = np.loadtxt(file, ndmin=2, dtype=dtype, comments=('#'))
        return m
    except Exception as e:
        logging.exception(f'Failed reading {file}')


class Geometry(tk.Frame):
    def __init__(self, root, width: float = 1600.0, height: float = 968.0, title: str = 'pyFEA Geoplot'):
        super().__init__()
        self.root = root
        self.title = title
        self.canvas = None
        self.lines = []
        self.displacement = []
        self.disp_scale = 1.0
        self.deformed = False
        self.width = width
        self.height = height
        self.margin = (self.width / 20, self.height / 20)
        self.timesteps = 20
        self.timestep = -1
        self.step = 1
        self.curves = []
        self.bg = None
        self.initUI()

    def initUI(self):
        self.master.title(self.title)
        self.pack(fill=tk.BOTH, expand=tk.YES)

        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)

        self.draw_background()

        self.master.bind('<Configure>', self.resize)

    def draw_background(self):
        # steps = int(self.height)
        steps = min(int(self.height), 100)
        from_color = (0.0, 0.0, 0.0)
        to_color = (0.0, 0.0, 255.0)

        r = from_color[0]
        g = from_color[1]
        b = from_color[2]

        dr = float(to_color[0] - r) / steps
        dg = float(to_color[1] - g) / steps
        db = float(to_color[2] - b) / steps

        img_height = int(self.height)
        img_width = int(self.width)

        image = Image.new("RGB", (img_width, img_height), "#FFFFFF")
        draw = ImageDraw.Draw(image)

        for i in range(steps):
            r, g, b = r + dr, g + dg, b+ db
            y0 = int(float(img_height * i) / steps)
            y1 = int(float(img_height * (i + 1)) / steps)

            draw.rectangle((0, y0, img_width, y1), fill=(int(r), int(g), int(b)))

        self.gradient_photoimage = ImageTk.PhotoImage(image)

        self.bg = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.gradient_photoimage)

        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)

    def resize(self, event):
        self.width = event.width
        self.height = event.height
        self.margin = (self.width / 20, self.height / 20)
        self.canvas.delete(self.bg)
        self.canvas.bg = None
        self.draw_background()
        self.replot()

    def add_line(self, x1: np.ndarray, x2: np.ndarray, dash=None):
        self.lines.append([x1[0], x1[1], x2[0], x2[1], dash])

    def add_line_displacement(self, x1: np.ndarray, x2: np.ndarray):
        self.displacement.append([x1[0], x1[1], x2[0], x2[1]])

    def replot(self, animation_scale: float = 1.0):
        # self.canvas.delete('all')
        # self.draw_background()
        for curve in self.curves:
            self.canvas.delete(curve)
        self.curves = []
        self.plot_lines(deformed=self.deformed, disp_scale=self.disp_scale, animation_scale=animation_scale)

    def animate(self):
        self.timestep += self.step
        if self.timestep == self.timesteps:
            self.step = -1
        elif self.timestep == 0:
            self.step = 1
        scale = -1.0 + 2.0 / self.timesteps * self.timestep
        self.replot(scale)
        self.after(100, self.animate)

    def plot_lines(self, deformed: bool = False, disp_scale: float = 1.0, animation_scale: float = 1.0):
        self.lines = np.array(self.lines, dtype=object)
        self.displacement = np.array(self.displacement, dtype=float)
        self.deformed = deformed
        self.disp_scale = disp_scale
        # extents = (xmin, xmax, zmin, zmax)
        if deformed:
            extents = (min(np.min(self.lines[:, [0, 2]] + self.displacement[:, [0, 2]] * self.disp_scale),
                           np.min(self.lines[:, [0, 2]] - self.displacement[:, [0, 2]] * self.disp_scale)),
                       max(np.max(self.lines[:, [0, 2]] + self.displacement[:, [0, 2]] * self.disp_scale),
                           np.max(self.lines[:, [0, 2]] - self.displacement[:, [0, 2]] * self.disp_scale)),
                       min(np.min(self.lines[:, [1, 3]] + self.displacement[:, [1, 3]] * self.disp_scale),
                           np.min(self.lines[:, [1, 3]] - self.displacement[:, [1, 3]] * self.disp_scale)),
                       max(np.max(self.lines[:, [1, 3]] + self.displacement[:, [1, 3]] * self.disp_scale),
                           np.max(self.lines[:, [1, 3]] - self.displacement[:, [1, 3]] * self.disp_scale)))
        else:
            extents = (np.min(self.lines[:, [0, 2]]), np.max(self.lines[:, [0, 2]]),
                       np.min(self.lines[:, [1, 3]]), np.max(self.lines[:, [1, 3]]))
        scale = [(extents[1] - extents[0]) / (self.width - 2 * self.margin[0]),
                 (extents[3] - extents[2]) / (self.height - 2 * self.margin[1])]
        scale = [1.0 if s == 0.0 else s for s in scale]
        scale = [1 / s for s in scale]
        scale = min(scale)
        center = (self.width / 2, self.height / 2)
        s = self.disp_scale * animation_scale
        for i in range(len(self.lines)):
            line = self.lines[i]
            d = self.displacement[i]

            if self.deformed:
                tmp = scale * (line[0] - (extents[1] + extents[0]) / 2) + center[0]
                x1 = scale * (line[0] + d[0] * s - (extents[1] + extents[0]) / 2) + center[0]
                z1 = self.height - (scale * (line[1] + d[1] * s - (extents[3] + extents[2]) / 2) + center[1])
                x2 = scale * (line[2] + d[2] * s - (extents[1] + extents[0]) / 2) + center[0]
                z2 = self.height - (scale * (line[3] + d[3] * s - (extents[3] + extents[2]) / 2) + center[1])
            else:
                x1 = scale * (line[0] - (extents[1] + extents[0]) / 2) + center[0]
                z1 = self.height - (scale * (line[1] - (extents[3] + extents[2]) / 2) + center[1])
                x2 = scale * (line[2] - (extents[1] + extents[0]) / 2) + center[0]
                z2 = self.height - (scale * (line[3] - (extents[3] + extents[2]) / 2) + center[1])
            self.curves.append(self.canvas.create_line(x1, z1, x2, z2, dash=line[4],
                                                       fill='#{0:02x}{1:02x}{2:02x}'.format(255, 255, 255)))
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)


def plot_geometry(nd: np.ndarray, el: np.ndarray):
    root = tk.Tk()
    # root.geometry('1600x968+300+300')
    geometry = Geometry(root)

    for eID in range(1, el.shape[0] + 1):
        nd1 = el[eID - 1][2]
        nd2 = el[eID - 1][3]
        geometry.add_line(nd[nd1 - 1], nd[nd2 - 1])

    geometry.plot_lines()

    root.mainloop()


def plot_deformed(nd: np.ndarray, el: np.ndarray, ue: np.ndarray):
    root = tk.Tk()
    # root.geometry('1600x968+300+300')
    geometry = Geometry(root)
    scale = [0.0, 0.0]
    try:
        scale[0] = np.max(np.abs(ue)) / (np.max(nd[:, 0]) - np.min(nd[:, 0])) * 10.0
    except ZeroDivisionError as e:
        scale[0] = 1.0
    try:
        scale[1] = np.max(np.abs(ue)) / (np.max(nd[:, 1]) - np.min(nd[:, 1])) * 10.0
    except ZeroDivisionError as e:
        scale[1] = 1.0
    scale = 1 / min(scale)

    eig = 3
    for eID in range(1, el.shape[0] + 1):
        nd1 = nd[el[eID - 1][2] - 1]
        nd2 = nd[el[eID - 1][3] - 1]
        geometry.add_line(nd1, nd2)
        u1 = ue[eID - 1][:2, eig - 1]
        u2 = ue[eID - 1][3:5, eig - 1]
        geometry.add_line_displacement(u1, u2)

    geometry.plot_lines(deformed=True, disp_scale=scale)
    geometry.animate()

    root.mainloop()


def beam2d(structure_directory: str = 'console'):
    logging.debug(f'call beam2d({structure_directory})')
    cfg = ConfigParser()
    cfg.read(os.path.join(structure_directory, 'g.ini'))
    solver = cfg['DEFAULT']['solver']
    logging.info(f'\n\n\tStarting {solver} analysis of {structure_directory}\n\n')

    # array of node coordinates
    nd = load_dat(os.path.join(structure_directory, 'nd.dat'), dtype=float)
    nnode = nd.shape[0]
    logging.debug(f'nd:\n{nd}')
    logging_array('Node Coordinates', nd, ['nID', 'x', 'z'])

    # array of element connectivity
    el = load_dat(os.path.join(structure_directory, 'el.dat'), dtype=int)
    nelem = el.shape[0]
    logging.debug(f'el:\n{el}')
    logging_array('Element Connectivity', el,
                  ['eID', 'mID', 'pID', 'nd1', 'nd2', 'Rx1', 'Rz1', 'Rfi1', 'Rx2', 'Rz2', 'Rfi2'])

    # array of materials
    mt = load_dat(os.path.join(structure_directory, 'mt.dat'), dtype=float)
    logging.debug(f'mt:\n{mt}')
    logging_array('Materials', mt, ['mID', 'ro', 'E', 'nu', 'alpha'])

    # array of properties
    pt = load_dat(os.path.join(structure_directory, 'pt.dat'), dtype=float)
    logging.debug(f'pt:\n{pt}')
    logging_array('Properties', mt, ['pID', 'A', 'I', 'W', 'Ash'])

    # array of suppressed nodes
    cs = load_dat(os.path.join(structure_directory, 'cs.dat'), dtype=int)
    logging_array('Nodal constraints', cs, ['cID', 'nID', 'Cx', 'Cz', 'Cy'])

    # array of nodal loads
    fn = load_dat(os.path.join(structure_directory, 'fn.dat'))
    logging_array('Nodal loads', fn, ['ldID', 'lpatID', 'nID', 'Fx', 'Fz', 'My'],
                  dtype=['int', 'int', 'int', 'float', 'float', 'float'])

    # array of elemental loads
    fe = load_dat(os.path.join(structure_directory, 'fe.dat'))
    if fe is not None:
        logging_array('Elemental loads', fe, ['ldID', 'lpatID', 'eID', 'fx', 'fz', 'dt'],
                      dtype=['int', 'int', 'int', 'float', 'float', 'float'])

    # DOF localisation matrices
    ndofs, ncdofs, lmn, lme, lmd = localisation_matrix(nd, el, cs)
    logging.debug(f'lmn:\n{lmn}')
    logging_array('Node DOF numbers', lmn, ['nID', 'dofX', 'dofZ', 'dofFi'])
    logging.debug(f'lmd:\n{lmd}')
    logging_array('DOF numbers to Node', lmd, ['dofID', 'nID', 'dir'])
    logging.debug(f'lme:\n{lme}')
    logging_array('Element DOF numbers', lme, ['eID', 'dofX1', 'dofZ1', 'dofFi1', 'dofX2', 'dofZ2', 'dofFi2'])

    # model info
    logging_table('Model info', [['nodes', nnode], ['elements', nelem], ['dofs', ndofs], ['dofs constrained', ncdofs]])

    if solver == 'linear static':
        # load vector
        f = np.zeros((ndofs, 1))
        if fn is not None:
            assemble_load_nodal(f, lmn, fn)
        if fe is not None:
            for i in range(fe.shape[0]):
                eID = int(fe[i][1])
                assemble_load_elemental(lme, f, beam2d_load(nd[el[eID - 1][2] - 1],
                                                            nd[el[eID - 1][3] - 1],
                                                            fe[i][2], fe[i][3]), eID)
                assemble_load_elemental(lme, f, beam2d_temp(nd[el[eID - 1][2] - 1], nd[el[eID - 1][3] - 1],
                                                            pt[el[eID - 1][1] - 1][0], mt[el[eID - 1][0] - 1][1],
                                                            mt[el[eID - 1][0] - 1][2], fe[i][4]), eID)
        logging.debug(f'f:\n{f}')
        logging_array('Right side vector', f, ['dofID', 'F'])

        # preparation of load vector, stiffness matrix, displacement vector
        K = np.zeros((ndofs, ndofs), dtype=float)
        u = np.zeros((ndofs, 1), dtype=float)

        # creation of local stiffness matrix and localisation
        for i in range(nelem):
            assemble(lme, K, beam2d_stiffness(nd[el[i][2] - 1], nd[el[i][3] - 1],
                                              pt[el[i][1] - 1][0], pt[el[i][1] - 1][1],
                                              mt[el[i][0] - 1][1]), i + 1)
            # assemble(lme, K, beam2d_stiffness_timoshenko(nd[el[i][2] - 1], nd[el[i][3] - 1],
            #                                              pt[el[i][1] - 1][0], pt[el[i][1] - 1][1],
            #                                              mt[el[i][0] - 1][1], mt[el[i][0] - 1][2]), i + 1)
        logging.debug(f'K:\n{K}')
        tmp = ['DOF']
        tmp.extend(['{0:n}'.format(i) for i in range(ndofs)])
        logging_array('Stiffness Matrix', K, tmp, eng=True)
        del tmp

        # solving the displacements
        u[ncdofs:] = linalg.solve(K[ncdofs:, ncdofs:], f[ncdofs:])
        logging.debug(f'u:\n{u}')
        logging_array('Resulting displacements', u, ['dofID', 'du'])

        ndu = u[lmn - 1].reshape((-1, 3))
        logging.debug(f'ndu:\n{ndu}')
        logging_array('Nodal displacements', ndu, ['nID', 'dX', 'dZ', 'dFi'])

        # reactions
        f[:ncdofs] = K[:ncdofs, ncdofs:] @ u[ncdofs:]
        logging.debug(f'f:\n{f}')
        logging_array('Resulting reactions', f[:ncdofs], ['dofID', 'R'])
        r = np.zeros((cs.shape[0], lmn.shape[1] + 1))
        for i in range(cs.shape[0]):
            r[i][0] = cs[i][0]
            for j in range(cs[i][1:].shape[0]):
                if cs[i][j + 1] == 1:
                    r[i][j + 1] = f[lmn[cs[i][0] - 1][j] - 1]
                else:
                    r[i][j + 1] = np.NaN
        logging.debug(f'r:\n{r}')
        logging_array('Nodal reactions', r, ['cID', 'nID', 'Fx', 'Fz', 'My'], eng=True)

        # element displacements
        ue = u[lme - 1].reshape((nelem, lme.shape[1]))
        logging.debug(f'ue:\n{ue}')
        logging_array('Elemental displacements', ue, ['eID', 'dX1', 'dZ1', 'dFi1', 'dX2', 'dZ2', 'dFi2'], eng=True)

        # element inner forces
        se = np.zeros((nelem, 6))
        for i in range(nelem):
            se[i] = beam2d_postpro(nd[el[i][2] - 1], nd[el[i][3] - 1], ue[i],
                                   pt[el[i][1] - 1][0], pt[el[i][1] - 1][1],
                                   mt[el[i][0] - 1][1])
        logging.debug(f'se:\n{se}')
        logging_array('Element Inner Forces', se, ['eID', 'N1', 'Q1', 'M1', 'N2', 'Q2', 'M2'], eng=True)

        return ndu, r, ue, se

    elif solver == 'eigenvalues':
        # preparation of  stiffness matrix, mass matrix, displacement vector
        K = np.zeros((ndofs, ndofs), dtype=float)
        M = np.zeros((ndofs, ndofs), dtype=float)
        u = np.zeros((ndofs, ndofs - ncdofs), dtype=float)

        # creation of local stiffness matrix and localisation
        for i in range(nelem):
            assemble(lme, K, beam2d_stiffness(nd[el[i][2] - 1], nd[el[i][3] - 1],
                                              pt[el[i][1] - 1][0], pt[el[i][1] - 1][1],
                                              mt[el[i][0] - 1][1]), i + 1)
            # assemble(lme, K, beam2d_stiffness_timoshenko(nd[el[i][2] - 1], nd[el[i][3] - 1],
            #                                              pt[el[i][1] - 1][0], pt[el[i][1] - 1][1],
            #                                              mt[el[i][0] - 1][1], mt[el[i][0] - 1][2]), i + 1)
        logging.debug(f'K:\n{K}')
        tmp = ['DOF']
        tmp.extend(['{0:n}'.format(i) for i in range(ndofs)])
        logging_array('Stiffness Matrix', K, tmp, eng=True)
        del tmp

        # creation of local mass matrix and localisation
        for i in range(nelem):
            assemble(lme, M, beam2d_mass(nd[el[i][2] - 1], nd[el[i][3] - 1],
                                         pt[el[i][1] - 1][0], mt[el[i][0] - 1][0], mi=0.5), i + 1)
        logging.debug(f'M:\n{M}')
        tmp = ['DOF']
        tmp.extend(['{0:n}'.format(i) for i in range(ndofs)])
        logging_array('Mass Matrix', M, tmp, eng=True)
        del tmp

        if solver in cfg.sections():
            # solving the eigenvalues and eigenshapes - only first N, up to ndofs-1
            if 'modes' in cfg[solver].keys():
                number_of_eigenvalues = int(cfg[solver]['modes'])
                u = np.zeros((ndofs, number_of_eigenvalues))
                eigenvalue, u[ncdofs:, :] = sclinalg.eigsh(K[ncdofs:, ncdofs:], number_of_eigenvalues,
                                                           M[ncdofs:, ncdofs:], which='SM')
            # # solving the eigenvalues and eigenshapes - all of them
            else:
                eigenvalue, u[ncdofs:, :] = linalg.eigh(K[ncdofs:, ncdofs:], M[ncdofs:, ncdofs:])

        logging.debug(f'eigenvalues:\n{eigenvalue}')
        logging.debug(f'eigenvectors:\n{u}')
        logging.info(f' >>> Eigenvalues found: {eigenvalue.shape[0]}')
        # eigenvalue = np.real(eigenvalue)
        idx = np.flip(eigenvalue.argsort()[::-1])
        eigenvalue = eigenvalue[idx].reshape((eigenvalue.shape[0], 1))
        u = u[:, idx]
        del idx
        omega = np.sqrt(eigenvalue)
        eigenfrequency = omega / (2.0 * math.pi)

        # normalise shapes to 1
        u *= 1.0 / np.max(np.abs(u), axis=0)

        tmp = np.hstack((eigenvalue, omega, eigenfrequency))

        logging_array('Resulting Eigenvalues', tmp, ['Mode ID', 'Lambda', 'Omega', 'Freq'],
                      ['int', 'eng', 'eng', 'float'])
        # logging_array('Resulting Eigenvalues:', tmp, ['Mode ID', u'\u03bb'.encode('utf-8'), 'Circular Frequency', 'Eigenfrequency'],
        #               ['int', 'eng', 'eng', 'float'])
        del tmp

        tmp = [['Mode']]
        tmp[0].extend([' {0:^11s}'.format('{0:n}'.format(i + 1)) for i in range(eigenfrequency.shape[0])])
        tmp.append(['DOF'])
        tmp[1].extend([' {0:^11s}'.format('{0:.2f} Hz'.format(eigenfrequency[i][0])) for i in range(eigenfrequency.shape[0])])
        logging_array('Eigenshapes', u, tmp, eng=True)
        del tmp

        ue = u[lme - 1]

        if solver in cfg.sections():
            if 'plot' in cfg[solver].keys():
                if 'geometry' in [s.strip() for s in cfg[solver]['plot'].split(',')]:
                    plot_geometry(nd, el)
                if 'deformed' in  [s.strip() for s in cfg[solver]['plot'].split(',')]:
                    plot_deformed(nd, el, ue)

        return eigenfrequency, u


if __name__ == '__main__':
    logger = logging.getLogger()
    # logger_handler = logging.StreamHandler()
    # logger.addHandler(logger_handler)
    logger_handler = logger.handlers[0]
    logger_handler.setFormatter(ADVANCED_FORMAT)
    logger_handler.setLevel(logging.INFO)

    logging.info(f'{__file__} started')
    parser = argparse.ArgumentParser()
    parser.add_argument('structure', type=str, help='directory name of the structure')

    args = parser.parse_args()

    beam2d(args.structure)
