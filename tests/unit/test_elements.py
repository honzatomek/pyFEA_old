import unittest
import logging

from misc.errors import *
from structure.nodes import *
from structure.elements import *
from structure.materials import *
from structure.properties import *


class Element_Test(unittest.TestCase):
    def test_dupl_id(self):
        nds = Nodes2D()
        for i in range(3):
            nds.add(i + 1, i * 500., 0.)
        m = LinearElastic(1, 'steel', 7.85E-9, 210.0E6, 0.3, 1.2E-5)
        p = CrossSectionBeam2D(1, 'beam', 2124.0, 3492243.0, 72755.0, 756.0, 0.0)
        els = Elements()
        with self.assertRaises(DuplicateIDError):
            for i in range(2):
                els.add_Bar2D(1, m.id, p.id, (i + 1, i + 2),
                              [0, 0, 0], [0, 0, 0])

    def test_mixed_elements_count(self):
        nds = Nodes2D()
        for i in range(4):
            nds.add(i + 1, i * 500., 0.)
        m = LinearElastic(1, 'steel', 7.85E-9, 210.0E6, 0.3, 1.2E-5)
        p = CrossSectionBeam2D(1, 'beam', 2124.0, 3492243.0, 72755.0, 756.0, 0.0)
        els = Elements()
        els.add_Bar2D(1, m.id, p.id, (1, 2),
                      [0, 0, 0], [0, 0, 0])
        els.add_Bar2D(2, m.id, p.id, (2, 3),
                      [0, 0, 0], [0, 0, 0])
        els.add_Rod2D(3, m.id, p.id, (3, 4))
        self.assertTrue(Bar2D.instances() == 2)
        self.assertTrue(Rod2D.instances() == 1)
        # print(str(els))
        # print(repr(els))


class Bar2D_Test(unittest.TestCase):
    def test_stiffness(self):
        nds = Nodes2D()
        for i in range(11):
            nds.add(i + 1, i * 100., 0.)
        m = LinearElastic(1, 'steel', 7.85E-9, 210.0E6, 0.3, 1.2E-5)
        p = CrossSectionBeam2D(1, 'beam', 2124.0, 3492243.0, 72755.0, 756.0, 0.0)
        els = Elements()
        for i in range(10):
            els.add_Bar2D(i + 1, m.id, p.id, (i + 1, i + 2),
                          [0, 0, 0], [0, 0, 0])
        for i in range(10):
            ke = els.get(i + 1).stiffness_gcs()
            self.assertTrue((ke == ke.T).all(),
                            msg=f'Stiffness Matrix of Element {i + 1} must be symmetric.')
            self.assertTrue(np.linalg.det(ke) == 0.,
                            msg=f'Stiffness matrix of element {i + 1} must be positive definite.')

    def test_mass(self):
        nds = Nodes2D()
        for i in range(11):
            nds.add(i + 1, i * 100., 0.)
        m = LinearElastic(1, 'steel', 7.85E-9, 210.0E6, 0.3, 1.2E-5)
        p = CrossSectionBeam2D(1, 'beam', 2124.0, 3492243.0, 72755.0, 756.0, 0.0)
        els = Elements()
        for i in range(10):
            els.add_Bar2D(i + 1, m.id, p.id, (i + 1, i + 2),
                          [0, 0, 0], [0, 0, 0])
        mi = {'Lumped': 1., 'Consistent': 0., 'Lumped-Consistent': 0.5}
        for i in range(10):
            for j, mass_type in enumerate(mi.keys()):
                me = els.get(i + 1).mass_gcs(mi[mass_type])
                # numerical symmetry
                self.assertTrue((me == me.T).all(),
                                msg=f'{mass_type} Mass Matrix of Element {i + 1} must be symmetric.')
                # positive semi-definiteness
                self.assertTrue(np.linalg.det(me) >= 0.,
                                msg=f'{mass_type} Mass matrix of element {i + 1} must be positive semi-definite.')
                # check linear momentum
                mass = els.get(i + 1).length() * (els.get(i + 1).mat.ro * els.get(i + 1).prop.A + els.get(i + 1).prop.nsm)
                ua = np.array([1., 0., 0., 1., 0., 0.])
                self.assertAlmostEqual(ua @ me @ ua.T, mass,
                                       msg=f'{mass_type} Mass Matrix of element {i + 1} '
                                           f'must conserve linear momentum in x direction.')
                wa = np.array([0., 1., 0., 0., 1., 0.])
                self.assertAlmostEqual(wa @ me @ wa.T, mass,
                                       msg=f'{mass_type} Mass Matrix of element {i + 1}'
                                           f' must conserve linear momentum in z direction.')
                uwa = np.array([1., 1., 0., 1., 1., 0.]) * math.sqrt(2.) / 2
                self.assertAlmostEqual(uwa @ me @ uwa.T, mass,
                                       msg=f'{mass_type} Mass Matrix of element {i + 1}'
                                           f' must conserve linear momentum in x + z direction.')
                # physical symmetry
                el1 = els.get(i + 1)
                me1 = mi[mass_type] * el1.mass_lumped_lcs() + (1. - mi[mass_type]) * el1.mass_consistent_lcs()
                el2 = Bar2D(100001 + i + 100 * j, el1.mID, el1.pID, el1.nodes, el1.releases[0], el1.releases[1])
                me2 = mi[mass_type] * el2.mass_lumped_lcs() + (1. - mi[mass_type]) * el2.mass_consistent_lcs()
                self.assertTrue((me1 == me2).all(),
                                msg=f'{mass_type} Mass matrix of element nd1->nd2 must be same as of element nd2->nd1')


class Rod2D_Test(unittest.TestCase):
    def test_stiffness(self):
        nds = Nodes2D()
        for i in range(11):
            nds.add(i + 1, i * 100., 0.)
        m = LinearElastic(1, 'steel', 7.85E-9, 210.0E6, 0.3, 1.2E-5)
        p = CrossSectionBeam2D(1, 'beam', 2124.0, 3492243.0, 72755.0, 756.0, 0.0)
        els = Elements()
        for i in range(10):
            els.add_Rod2D(i + 1, m.id, p.id, (i + 1, i + 2))
        for i in range(10):
            ke = els.get(i + 1).stiffness_gcs()
            self.assertTrue((ke == ke.T).all(),
                            msg=f'Stiffness Matrix of Element {i + 1} must be symmetric.')
            self.assertTrue(np.linalg.det(ke) == 0.,
                            msg=f'Stiffness matrix of element {i + 1} must be positive definite.')

    def test_mass(self):
        nds = Nodes2D()
        for i in range(11):
            nds.add(i + 1, i * 100., 0.)
        m = LinearElastic(1, 'steel', 7.85E-9, 210.0E6, 0.3, 1.2E-5)
        p = CrossSectionBeam2D(1, 'beam', 2124.0, 3492243.0, 72755.0, 756.0, 0.0)
        els = Elements()
        for i in range(10):
            els.add_Rod2D(i + 1, m.id, p.id, (i + 1, i + 2))
        mi = {'Lumped': 1., 'Consistent': 0., 'Lumped-Consistent': 0.5}
        for i in range(10):
            for j, mass_type in enumerate(mi.keys()):
                me = els.get(i + 1).mass_gcs(mi[mass_type])
                # numerical symmetry
                self.assertTrue((me == me.T).all(),
                                msg=f'{mass_type} Mass Matrix of Element {i + 1} must be symmetric.')
                # positive semi-definiteness
                self.assertTrue(np.linalg.det(me) >= 0.,
                                msg=f'{mass_type} Mass matrix of element {i + 1} must be positive semi-definite.')
                # check linear momentum
                mass = els.get(i + 1).length() * (els.get(i + 1).mat.ro * els.get(i + 1).prop.A + els.get(i + 1).prop.nsm)
                ua = np.array([1., 0., 0., 1., 0., 0.])
                self.assertAlmostEqual(ua @ me @ ua.T, mass,
                                       msg=f'{mass_type} Mass Matrix of element {i + 1} must conserve linear momentum in x direction.')
                # physical symmetry
                el1 = els.get(i + 1)
                me1 = mi[mass_type] * el1.mass_lumped_lcs() + (1. - mi[mass_type]) * el1.mass_consistent_lcs()
                el2 = Rod2D(100001 + i + 100 * j, el1.mID, el1.pID, el1.nodes)
                me2 = mi[mass_type] * el2.mass_lumped_lcs() + (1. - mi[mass_type]) * el2.mass_consistent_lcs()
                self.assertTrue((me1 == me2).all(),
                                msg=f'{mass_type} Mass matrix of element nd1->nd2 must be same as of element nd2->nd1')


if __name__ == '__main__':
    logger = logging.getLogger()
    logger.disabled = True
    logging.disable(logging.FATAL)
    unittest.main(verbosity=3)
