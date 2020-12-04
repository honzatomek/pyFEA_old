import math
import logging
from misc.misc import format_eng, Data
from misc.errors import *


logger = logging.getLogger()


class Node2D(Data):
    """
    Parent class for all Nodes
    """
    _ids = set()
    _instances = set()
    _counter = 0

    @classmethod
    def from_str(cls, string: str):
        """
        Constructor for parsing string into a new instance of Node
        :param string:  String with data separated by ' ': 'NodeID  X  Z [Label]'
        :return:        Node object
        """
        input_string = string.strip(' ')
        while '  ' in input_string:
            input_string = input_string.replace('  ', ' ')
        vals = [s.strip(' ') for s in input_string.split()]
        if len(vals) < 3:
            raise AttributeError(f'String {string} must contain at least NodeID, X-Coor, Z-Coor')
        elif len(vals) == 3:
            id = int(vals[0])
            x = float(vals[1])
            z = float(vals[2])
            label = None
        else:
            id = int(vals[0])
            x = float(vals[1])
            z = float(vals[2])
            label = str(vals[3]).strip("'")

        return cls(id, x, z, label)

    def __init__(self, id: int, x: float, z: float, label: str = None):
        """
        Node initialization
        :param id:    Unique Node ID
        :param label: Optional Node Label, max 16 chars, rest will be cropped
        """
        self.x = x
        self.z = z
        super(Node2D, self).__init__(id, label)

    def __del__(self):
        # del self.x
        # del self.z
        super(Node2D, self).__del__()

    def __repr__(self):
        if self.label is not None:
            return f'{type(self).__name__}(id={self.id:n}, x={format_eng(self.x):s},' \
                   f' z={format_eng(self.z):s}, label="{self.label:s}")'
        else:
            return f'{type(self).__name__}(id={self.id:n}, x={format_eng(self.x):s},' \
                   f' z={format_eng(self.z):s})'

    def __str__(self):
        message = f' {self.id:9n} {format_eng(self.x):s} {format_eng(self.z):s}'
        if self.label is not None:
            if ' ' in self.label:
                message += f" '{self.label:32s}'"
            else:
                message += f' {self.label:32s}'
        return message

    def coor(self):
        return [self.x, self.z]


class Nodes2D:
    """
    Class template for collection of Node objects
    """
    @classmethod
    def from_str(cls, string: str):
        lines = string.split('\n')
        nodes = cls()
        for line in lines:
            nodes.node.append(Node2D.from_str(line))
            nodes.count += 1
            nodes.iid.setdefault(nodes.node[-1].id, nodes.count - 1)
        return nodes

    def __init__(self):
        self.node = []   # Node objects
        self.iid = {}    # dictionary of Node IDs {external ID: internal ID}
        self.count = 0

    def __str__(self):
        message = '\n$NODE'
        for node in self.node:
            message += '\n' + str(node)
        return message

    def __repr__(self):
        return 'Nodes: %d, minID = %d, maxID = %d' % self.stat()

    def stat(self):
        return self.count, min(self.iid.keys()), max(self.iid.keys())

    def add(self, id: int, x: float, z: float, label: str = None):
        self.node.append(Node2D(id, x, z, label))
        self.count += 1
        self.iid.setdefault(id, self.count)

    def getID(self, ndID: int):
        return self.node[self.iid[ndID] - 1]

    def distance(self, ndID1: int, ndID2: int):
        nd1 = self.node[self.iid[ndID1] - 1]
        nd2 = self.node[self.iid[ndID2] - 1]
        distance = math.sqrt((nd2.x - nd1.x) ** 2. + (nd2.z - nd1.z) ** 2.)
        return distance


if __name__ == '__main__':
    nd0 = Node2D.from_str('    10   5000.0    -30.0E+03   test2')
    print(nd0)
    print(repr(nd0))
    nd = Node2D(1, 1000.0, 2000.0, 'test')
    print(nd)
    nd2 = eval(repr(nd))
    print(nd2)
    nd4 = Node2D.from_str('    10   5000.0    -30.0E+03   test2')
    print(nd4)
    print(repr(nd4))

    nds = Nodes2D.from_str('  1    1.E3   2.E3   \n  200001   3.E3   4.E3')
    print(nds)
    print(repr(nds))

    duplIDs = set()
    for i in range(50):
        duplIDs.add(i)
    duplIDs = list(duplIDs)
    tmp = '\n'.join([''.join(['{0:10n}'.format(d) for d in duplIDs[i: i + 8]]) for i in range(0, len(duplIDs), 8)])
    pass
