import unittest
import logging
from structure.nodes import *


class Node_Test(unittest.TestCase):
    def test_init(self):
        id = 1
        x = 1000.
        z = 4000.
        label = 'test'
        nd = Node(id, [x, z], label)
        self.assertEqual(id, nd.id)
        self.assertEqual(x, nd.coor[0])
        self.assertEqual(z, nd.coor[1])
        self.assertEqual(label, nd.label)

    def test_coor(self):
        id = 1
        x = 1000.
        z = 4000.
        label = 'test'
        nd = Node(id, [x, z], label)
        self.assertEqual([x, z], nd.coor)

    def test_repr(self):
        id = 1
        x = 1000.
        z = 4000.
        label = 'test'
        nd = Node(id, [x, z], label)
        nd2 = eval(repr(nd).replace('id=1', 'id=2'))
        self.assertEqual(nd.coor, nd2.coor)


class Nodes_Test(unittest.TestCase):
    def test_init(self):
        nds = Nodes()
        self.assertEqual(nds.count(), 0)
        self.assertEqual(len(nds.objects), 0)

    def test_stat(self):
        nds = Nodes(id=1, label='test')
        for i in range(2):
            nds.add((i + 1) * 1000, [i * 1000.0, 0.], f'test_{i + 1:n}')
        num, minid, maxid = nds.stat()
        self.assertEqual(num, 2)
        self.assertEqual(minid, 1000)
        self.assertEqual(maxid, 2000)

    def test_add(self):
        id = 1
        x = 1000.
        z = 4000.
        label = 'test'
        nds = Nodes()
        nds.add(id, [x, z], label)
        nd = nds.objects[0]
        self.assertEqual(id, nd.id)
        self.assertEqual(x, nd.coor[0])
        self.assertEqual(z, nd.coor[1])
        self.assertEqual(label, nd.label)

    def test_check_duplicates(self):
        nds = Nodes()
        nds.add(1, [1000.0, 1000.0])
        with self.assertRaises(DuplicateIDError):
            nds.add(1, [1000.0, 1000.0])

    def test_distance(self):
        nds = Nodes()
        nds.add(1, [0., 0.])
        nds.add(2, [4., 3.])
        self.assertEqual(nds.distance(1, 2), 5.)

    def test_get(self):
        nds = Nodes()
        id = 1000000
        nds.add(id, [0., 0.])
        nds.add(id + 1, [0., 0.])
        nds.add(id + 2, [0., 0.])
        self.assertEqual(nds.get(id + 1).id, id + 1)

    def test_str(self):
        nds = Nodes(id=1, label='test')
        for i in range(2):
            nds.add(i + 1, [i * 1000.0, 0.], f'test_{i + 1:n}')
        expected_result = """$NODE TYPE = Node
         1      0.0000E+00      0.0000E+00  : test_1
         2      1.0000E+03      0.0000E+00  : test_2
"""
        self.assertEqual(str(nds), expected_result)

    def test_repr(self):
        nds = Nodes(id=1, label='all nodes')
        for i in range(2):
            nds.add(i + 1, [i * 1000.0, 0.], f'test_{i + 1:n}')
        expected_result = """Nodes(id=1, label='all nodes')
Nodes.getID(1)._add_object(Node(id=1, coors=[ 0.0000E+00, 0.0000E+00], label='test_1'))
Nodes.getID(1)._add_object(Node(id=2, coors=[ 1.0000E+03, 0.0000E+00], label='test_2'))"""
        self.assertEqual(repr(nds), expected_result)
        str = repr(nds).split('\n')
        nds2 = eval(str[0].replace('id=1', 'id=2').replace('all nodes', 'test nodes'))
        for i in range(1, len(str)):
            eval(str[i].replace('getID(1)', 'getID(2)').replace('id=', 'id=10'))
        self.assertEqual(nds.count(), nds2.count())
        nodes1 = nds.objects
        nodes2 = nds2.objects
        for i in range(len(nodes1)):
            self.assertEqual(nodes1[i].coor, nodes2[i].coor)


if __name__ == '__main__':
    logger = logging.getLogger()
    logger.disabled = True
    logging.disable(logging.FATAL)

    unittest.main(verbosity=3)
