import unittest
import logging
from structure.nodes import *


class Node2D_Test(unittest.TestCase):
    def test_init(self):
        id = 1
        x = 1000.
        z = 4000.
        label = 'test'
        nd = Node2D(id, x, z, label)
        self.assertEqual(id, nd.id)
        self.assertEqual(x, nd.x)
        self.assertEqual(z, nd.z)
        self.assertEqual(label, nd.label)

    def test_from_str(self):
        string = ['  1    1.E3    4.E3   ',
                  '2    1.E3    4.E3   ',
                  '  3    1.E3    4.E3',
                  '4    1.E3    4.E3',
                  '\t5    1.E3    4.E3',
                  '\t6\t1.E3\t4.E3',
                  '7\t1.E3\t4.E3']
        for s in string:
            vals = s.split()
            id = int(vals[0])
            x = float(vals[1])
            z = float(vals[2])
            nd = Node2D.from_str(s)
            self.assertEqual(id, nd.id)
            self.assertEqual(x, nd.x)
            self.assertEqual(z, nd.z)

    def test_coor(self):
        id = 1
        x = 1000.
        z = 4000.
        label = 'test'
        nd = Node2D(id, x, z, label)
        self.assertEqual([x, z], nd.coor())


class Nodes2D_Test(unittest.TestCase):
    def test_init(self):
        nds = Nodes2D()
        self.assertEqual(nds.count(), 0)
        self.assertEqual(len(nds.objects), 0)
        # self.assertEqual(len(nds.iid.keys()), 0)

    def test_from_str(self):
        string = ['  1    1.E3    4.E3   ',
                  '2    1.E3    4.E3   :     test_2',
                  '  3    1.E3    4.E3',
                  '4    1.E3    4.E3:     "test 4"',
                  '\t5    1.E3    4.E3',
                  '\t6\t1.E3\t4.E3\t:\ttest_6',
                  '7\t1.E3\t4.E3']
        nds = Nodes2D.from_str('\n'.join(string))
        self.assertEqual(nds.count(), 7)

    def test_stat(self):
        nds = Nodes2D(id=1, label='test')
        for i in range(2):
            nds.add((i + 1) * 1000, i * 1000.0, 0., f'test_{i + 1:n}')
        num, minid, maxid = nds.stat()
        self.assertEqual(num, 2)
        self.assertEqual(minid, 1000)
        self.assertEqual(maxid, 2000)

    def test_add(self):
        id = 1
        x = 1000.
        z = 4000.
        label = 'test'
        nds = Nodes2D()
        nds.add(id, x, z, label)
        nd = nds.objects[0]
        self.assertEqual(id, nd.id)
        self.assertEqual(x, nd.x)
        self.assertEqual(z, nd.z)
        self.assertEqual(label, nd.label)

    def test_check_duplicates(self):
        nds = Nodes2D()
        nds.add(1, 1000.0, 1000.0)
        with self.assertRaises(DuplicateIDError):
            nds.add(1, 1000.0, 1000.0)

    def test_distance(self):
        nds = Nodes2D()
        nds.add(1, 0., 0.)
        nds.add(2, 4., 3.)
        self.assertEqual(nds.distance(1, 2), 5.)

    def test_get(self):
        nds = Nodes2D()
        id = 1000000
        nds.add(id, 0., 0.)
        nds.add(id + 1, 0., 0.)
        nds.add(id + 2, 0., 0.)
        self.assertEqual(nds.get(id + 1).id, id + 1)

    def test_str(self):
        nds = Nodes2D(id=1, label='test')
        for i in range(2):
            nds.add(i + 1, i * 1000.0, 0., f'test_{i + 1:n}')
        expected_result = """$NODE TYPE = Node2D
         1      0.0000E+00      0.0000E+00  : test_1
         2      1.0000E+03      0.0000E+00  : test_2
"""
        self.assertEqual(str(nds), expected_result)

    def test_repr(self):
        nds = Nodes2D(id=1, label='all nodes')
        for i in range(2):
            nds.add(i + 1, i * 1000.0, 0., f'test_{i + 1:n}')
        expected_result = """Nodes2D(id=1, label='all nodes')
Nodes2D.getID(1)._add_obj(Node2D(id=1, x=0.0000E+00, z=0.0000E+00, label='test_1'))
Nodes2D.getID(1)._add_obj(Node2D(id=2, x=1.0000E+03, z=0.0000E+00, label='test_2'))"""
        self.assertEqual(repr(nds), expected_result)


if __name__ == '__main__':
    logger = logging.getLogger()
    logger.disabled = True
    logging.disable(logging.FATAL)

    unittest.main(verbosity=3)
