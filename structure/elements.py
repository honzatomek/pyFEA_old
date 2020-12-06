import math
import logging
import numpy as np

from misc.misc import format_eng, Data
from misc.errors import *
from structure.nodes import *
from structure.materials import *
from structure.properties import *


logger = logging.getLogger()


class Element(Data):
    _ids = set()
    _instances = set()
    _counter = 0

    def __init__(self, id: int, matID: int, propID: int, label: str = None):
        self.mID = matID
        self.pID = propID
        super(Element, self).__init__(id, label)

    def __del__(self):
        # del self.mID
        # del self.pID
        super(Element, self).__del__()

    def __str__(self):
        message = f' {self.id:9n} {self.mID:9n} {self.pID:9n}'
        if self.label is not None:
            if ' ' in self.label:
                message += f" '{self.label:s}'"
            else:
                message += f' {self.label:s}'
        return message

    def __repr__(self):
        if self.label is not None:
            return f"{type(self).__name__:s}(id={self.id:n}, matID={self.mID:n}, " \
                   f"propID={self.pID:n}, label='{self.label:s}')"
        else:
            return f"{type(self).__name__:s}(id={self.id:n}, matID={self.mID:n}, " \
                   f"propID={self.pID:n})"

    @property
    def prop(self):
        return Property.getID(self.pID)

    @property
    def mat(self):
        return Material.getID(self.mID)


class Rod2D(Element):
    """
    Linear Rod Element in 2D
    :param id:       Unique Element ID
    :param matID:    Material Object
    :param propID:   Property Object
    :param endA:     Node2D object of element start
    :param endB:     Node2D object of element end
    """
    _counter = 0

    def __init__(self, id: int, matID: int, propID: int, endA: int, endB: int, label: str = None):
        super(Rod2D, self).__init__(id, matID, propID, label)
        self.endA = endA
        self.endB = endB

    def __del__(self):
        # del self.endA
        # del self.endB
        super(Rod2D, self).__del__()

    def __str__(self):
        message = f' {self.id:9n} {self.mID:9n} {self.pID:9n} {self.endA:9n} {self.endB:9n}'
        if self.label is not None:
            if ' ' in self.label:
                message += f" '{self.label:s}'"
            else:
                message += f' {self.label:s}'
        return message

    def __repr__(self):
        message = f'{type(self).__name__:s}(id={self.id:n}, matID={self.mID:n}, ' \
                  f'propID={self.pID:n}, endA={self.endA:n}, endB={self.endB:n}'
        if self.label is not None:
            message += f", label='{self.label:s}')"
        else:
            message += ')'
        return message

    @property
    def ndA(self):
        return Node2D.getID(self.endA)

    @property
    def ndB(self):
        return Node2D.getID(self.endB)

    def length(self):
        x1 = self.ndA.coor()
        x2 = self.ndB.coor()
        length = math.sqrt((x2[0] - x1[0]) ** 2. + (x2[1] - x1[1]) ** 2.)
        return length

    def transmatrix(self):
        """
        Function computes transformation matrix (GCS -> LCS) of beam in 2d
        (Rl = T * Rg)
        :return:   t  - beam transformation matrix in 2D (6, 6)
        """
        x1 = self.ndA.coor()
        x2 = self.ndB.coor()
        length = math.sqrt((x2[0] - x1[0]) ** 2. + (x2[1] - x1[1]) ** 2.)
        c = (x2[0] - x1[0]) / length
        s = (x2[1] - x1[1]) / length

        tt = np.array([[c, s, 0.],
                       [-s, c, 0.],
                       [0., 0., 1.]], dtype=float)

        t = np.zeros((6, 6), dtype=float)
        t[:3, :3] = tt
        t[3:, 3:] = tt

        return t

    def stiffness_lcs(self):
        """
        Returns Rod2D element stiffness matrix in LCS (2D)
        :return: kl - element stiffness matrix in LCS
        """
        l = self.length()
        EA = self.mat.E * self.prop.A
        kuu = EA / l * np.array([[1., -1.],
                                 [-1., 1.]], dtype=float)

        kl = np.zeros((6, 6), dtype=float)
        kl[[0, 3], [[0], [3]]] = kuu

        return kl

    def stiffness_gcs(self):
        """
        Returns Element stiffness matrix in GCS (2D)
        :return: ke - element stiffness matrix in GCS
        """
        # element stiffness matrix in LCS
        kl = self.stiffness_lcs()
        # element transformation matrix LCS -> GCS
        t = self.transmatrix()
        # transformation LCS -> GCS
        ke = t.T @ kl @ t

        return ke

    def mass_lumped_lcs(self):
        """
        Function to compute lumped mass matrix of Rod element in LCS (2D)
        :return: mll - Rod element lumped mass matrix in LCS 2D (6, 6)
        """
        # structural mass
        sm = self.mat.ro * self.prop.A * self.length()
        # nonstructural mass
        nm = self.length() * self.prop.nsm
        # local lumped element mass matrix
        mll = np.zeros((6, 6), dtype=float)
        mll[0][0] = (sm + nm) / 2.
        mll[3][3] = (sm + nm) / 2.
        return mll

    def mass_consistent_lcs(self):
        """
        Function to compute consistent mass matrix of Rod2D element in LCS (2D)
        :return: mcl - Rod2D element lumped mass matrix in LCS 2D (6, 6)
        """
        # structural mass
        sm = self.mat.ro * self.prop.A * self.length()
        # nonstructural mass
        nm = self.length() * self.prop.nsm
        # local consistent element mass matrix
        m11 = (sm + nm) * np.array([[1. / 3., 1. / 6.],
                                    [1. / 6., 1. / 3.]], dtype=float)

        mcl = np.zeros((6, 6), dtype=float)
        mcl[[0, 3], [[0], [3]]] = m11

        return mcl

    def mass_gcs(self, mi: float = 0.5):
        """
        Returns Element Mass matrix in GCS (2D)
        :param mi:  weighted average coefficient for lumped and consistent mass matrix (1.0 = lumped, 0.0 = consistent)
        :return: ke - element mass matrix in GCS
        """
        ml = (1. - mi) * self.mass_consistent_lcs() + mi * self.mass_lumped_lcs()
        t = self.transmatrix()
        # transformation LCS -> GCS
        me = t.T @ ml @ t

        return me


class Bar2D(Rod2D):
    """
    Bar Element, linear interpolation (Kirchhoff, 2D)
    """
    _counter = 0

    def __init__(self, id: int, matID: int, propID: int, endA: int, endB: int,
                 releaseA: list = [0, 0, 0], releaseB: list = [0, 0, 0]):
        """
        Bar 2D Element initialization
        :param id:       Unique Element ID
        :param material: Material Object
        :param property: Property Object
        :param endA:     Node2D object of element start
        :param endB:     Node2D object of element end
        :param releaseA: Element releases at start
        :param releaseB: Element releases at end
        """
        super(Bar2D, self).__init__(id, matID, propID, endA, endB)
        self.rA = releaseA
        self.rB = releaseB

    def __del__(self):
        # self.rA = None
        # self.rB = None
        # del self.rA
        # del self.rB
        super(Bar2D, self).__del__()

    def __str__(self):
        message = f' {self.id:9n} {self.mID:9n} {self.pID:9n} {self.endA:9n} {self.endB:9n}'
        message += ''.join([f' {self.rA[i]:5n}' for i in range(len(self.rA))])
        message += ''.join([f' {self.rB[i]:5n}' for i in range(len(self.rB))])
        if self.label is not None:
            if ' ' in self.label:
                message += f" '{self.label:s}'"
            else:
                message += f' {self.label:s}'
        return message

    def __repr__(self):
        message = f'{type(self).__name__:s}(id={self.id:n}, matID={self.mID:n}, ' \
                  f'propID={self.pID:n}, endA={self.endA:n}, endB={self.endB:n}'
        message += f", releaseA=[{', '.join([str(d) for d in self.rA]):s}]"
        message += f", releaseB=[{', '.join([str(d) for d in self.rB]):s}]"
        if self.label is not None:
            message += f", label='{self.label:s}')"
        else:
            message += ')'
        return message

    def stiffness_lcs(self):
        """
        Returns Bar2D element stiffness matrix in LCS (Kirchhoff, 2D)
        :return: kl - element stiffness matrix in LCS
        """
        l = self.length()
        l2 = l * l
        l3 = l2 * l
        EA = self.mat.E * self.prop.A
        EI = self.mat.E * self.prop.Iyy
        kuu = EA / l * np.array([[1., -1.],
                                 [-1., 1.]], dtype=float)
        kww = EI / l3 * np.array([[12., -12.],
                                  [-12., 12.]], dtype=float)
        kwf = EI / l2 * np.array([[-6., -6.],
                                  [6., 6.]], dtype=float)
        kff = EI / l * np.array([[4., 2.],
                                 [2., 4.]], dtype=float)

        kl = np.zeros((6, 6), dtype=float)
        kl[[0, 3], [[0], [3]]] = kuu
        kl[[1, 4], [[1], [4]]] = kww
        kl[[1, 4], [[2], [5]]] = kwf
        kl[[2, 5], [[1], [4]]] = kwf.T
        kl[[2, 5], [[2], [5]]] = kff

        return kl

    def mass_lumped_lcs(self):
        """
        Function to compute lumped mass matrix of bar element in LCS (2D)
        :return: mll - bar element lumped mass matrix in LCS 2D (6, 6)
        """
        # structural mass
        sm = self.prop.A * self.length() * self.mat.ro
        # nonstructural mass
        nm = self.length() * self.prop.nsm
        # local lumped element mass matrix
        mll = (sm + nm) / 2. * np.eye(6, dtype=float)
        mll[2][2] = 0.
        mll[5][5] = 0.
        return mll

    def mass_consistent_lcs(self):
        """
        Function to compute consistent mass matrix of bar element in LCS (2D)
        :return: mcl - bar element lumped mass matrix in LCS 2D (6, 6)
        """
        # structural mass
        sm = self.prop.A * self.length() * self.mat.ro
        # nonstructural mass
        nm = self.length() * self.prop.nsm
        # local consistent element mass matrix
        m11 = (sm + nm) * np.array([[1. / 3., 1. / 6.],
                                    [1. / 6., 1. / 3.]], dtype=float)

        mcl = np.zeros((6, 6), dtype=float)
        mcl[[0, 3], [[0], [3]]] = m11
        mcl[[1, 4], [[1], [4]]] = m11

        return mcl

    def beam_mass_consistent_lcs(self):
        """
        Function to compute consistent mass matrix of bar element in LCS (2D)
        :return: mcl - beam element lumped mass matrix in LCS 2D (6, 6)
        """
        # structural mass
        sm = self.prop.A * self.length() * self.mat.ro
        # nonstructural mass
        nm = self.length() * self.prop.nsm
        # local consistent element mass matrix
        muu = (sm + nm) * np.array([[1. / 3., 1. / 6.],
                                    [1. / 6., 1. / 3.]], dtype=float)
        mww = (sm + nm) / 420. * np.array([[156., 54.],
                                           [54., 156.]], dtype=float)
        mwf = (sm + nm) * self.length() / 420. * np.array([[22., -13.],
                                                           [-13., -22.]], dtype=float)
        mff = (sm + nm) * (self.length() ** 2) * np.array([[4., -3.],
                                                           [-3., 4.]], dtype=float)

        mcl = np.zeros((6, 6), dtype=float)
        mcl[[0, 3], [[0], [3]]] = muu
        mcl[[1, 4], [[1], [4]]] = mww
        mcl[[1, 4], [[2], [5]]] = mwf
        mcl[[2, 5], [[1], [4]]] = mwf.T
        mcl[[2, 5], [[2], [5]]] = mff

        return mcl


class Elements:
    """
    Class for collection of Element objects
    """
    def __init__(self):
        self.element = []   # Element objects
        self.iid = {}       # dictionary of Element IDs {external ID: internal ID}
        self.count = 0

    def __str__(self):
        elems_by_type = {}
        for element in self.element:
            if type(element).__name__ not in elems_by_type.keys():
                elems_by_type.setdefault(type(element).__name__, [element])
            else:
                elems_by_type[type(element).__name__].append(element)
        message = ''
        for element_type in elems_by_type.keys():
            message += '\n$ELEMENT TYPE = {0:s}'.format(element_type)
            for element in elems_by_type[element_type]:
                message += '\n' + str(element)
            message += '\n'
        return message

    def __repr__(self):
        return 'Elements: %d, minID = %d, maxID = %d' % self.stat()

    def add_bar2D(self, id: int, matID: int, propID: int,
                  endA: int, endB: int, releaseA: list, releaseB: list):
        self.element.append(Bar2D(id, matID, propID, endA, endB, releaseA, releaseB))
        self.count += 1
        self.iid.setdefault(id, self.count)

    def add_rod2D(self, id: int, matID: int, propID: int,
                  endA: int, endB: int):
        self.element.append(Rod2D(id, matID, propID, endA, endB))
        self.count += 1
        self.iid.setdefault(id, self.count)

    def stat(self):
        return self.count, min(self.iid.keys()), max(self.iid.keys())

    def check_duplicates(self):
        logging.info(f'{self.__class__.__name__}.check()')
        setOfIDs = set()
        duplIDs = set()
        for element in self.element:
            if element.id in setOfIDs:
                duplIDs.add(element.id)
            else:
                setOfIDs.add(element.id)
        if len(duplIDs) > 0:
            duplIDs = list(duplIDs)
            tmp = '\n        '.join([''.join(['{0:10n}'.format(d) for d in duplIDs[i: i + 8]]) for i in range(0, len(duplIDs), 8)])
            logging.error('Duplicate Element IDs found:\n{0}'.format(tmp))
            raise IndexError('Duplicate Element IDs found.')
        logging.info('Element IDs checked: OK')
        return False


if __name__ == '__main__':
    nds = Nodes2D()
    for i in range(3):
        nds.add(i + 1, i * 500., 0.)
    print(str(nds))
    m = LinearElastic(1, 'steel', 7.85E-9, 210.0E6, 0.3, 1.2E-5)
    print(str(m))
    p = CrossSectionBeam2D(1, 'beam', 2124.0, 3492243.0, 72755.0, 756.0, 0.0)
    print(str(p))
    els = Elements()
    for i in range(2):
        els.add_rod2D(i + 101, m.id, p.id, i + 1, i + 2)
        els.add_bar2D(i + 1, m.id, p.id, i + 1, i + 2,
                      [0, 0, 0], [0, 0, 0])
    print(str(els))
    pass