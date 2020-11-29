import math
import logging
from misc.misc import format_eng


class Node:
    """
    Parent class for all Nodes
    """
    @classmethod
    def from_str(cls, string: str):
        """
        Template constructor for parsing string into a new instance of Node
        :param string:  String with data 'NodeID [Label]' delimited by spaces
        :return:        Node object
        """
        input_string = string.strip(' ')
        while '  ' in input_string:
            input_string = input_string.replace('  ', ' ')
        vals = [s.strip(' ') for s in input_string.split()]
        if len(vals) == 0:
            raise AttributeError(f'String {string} must contain at least Node ID number')
        elif len(vals) == 1:
            id = int(vals[0])
            label = None
        else:
            id = int(vals[0])
            label = str(vals[1])

        return cls(id, label)

    def __init__(self, id: int, label: str = None):
        """
        Node initialization
        :param id:    Unique Node ID
        :param label: Optional Node Label, max 16 chars, rest will be cropped
        """
        self.id = int(id)
        self.label = str(label)[:16]
        pass

    def __repr__(self):
        return f'{self.__class__.__name__}(id={self.id}, label="{self.label}")'

    def __str__(self):
        return f' {self.id:9n}' \
               + (self.label if self.label is not None else '')

    def coor(self):
        return None


class Node2D(Node):
    """
    Node in 2D
    """
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
            label = str(vals[3])

        return cls(id, x, z, label)

    def __init__(self, id: int, x: float, z: float, label: str = None):
        """
        2D Node initialization
        :param id:        Unique Node ID
        :param x:         X-Coordinate
        :param z:         Z-Coordinate
        :param label:     Optional Node label, max 16 chars, rest will be cropped
        """
        super().__init__(id, label)
        self.x = x
        self.z = z

    def __repr__(self):
        return f'{self.__class__.__name__}(id={self.id}, x={self.x}, z={self.z}' \
               + f', label="{self.label}")' if self.label is not None else ''

    def __str__(self):
        return f' {self.id:9n}'\
               + format_eng(self.x, ' {0:9.3f}E{1:+03n}') \
               + format_eng(self.z, ' {0:9.3f}E{1:+03n}') \
               + (' ' + self.label if self.label is not None else '')

    def coor(self):
        return [self.x, self.z]


class Nodes:
    """
    Class template for collection of Node objects
    """
    @classmethod
    def from_str(cls, string: str):
        lines = string.split('\n')
        nodes = cls()
        for line in lines:
            nodes.node.append(Node.from_str(line))
            nodes.count += 1
            nodes.iid.setdefault(nodes.node[-1].id, nodes.count - 1)
        return nodes

    def __init__(self):
        self.node = []   # Node objects
        self.iid = {}     # dictionary of Node IDs {external ID: internal ID}
        self.count = 0

    def __str__(self):
        message = '$NODE'
        for node in self.node:
            message += '\n' + str(node)
        return message

    def __repr__(self):
        return 'Nodes: %d, minID = %d, maxID = %d' % self.stat()

    def stat(self):
        return self.count, min(self.iid.keys()), max(self.iid.keys())

    def check_duplicates(self):
        logging.info(f'{self.__class__.__name__}.check()')
        setOfIDs = set()
        duplIDs = set()
        for node in self.node:
            if node.id in setOfIDs:
                duplIDs.add(node.id)
            else:
                setOfIDs.add(node.id)
        if len(duplIDs) > 0:
            duplIDs = list(duplIDs)
            tmp = '\n        '.join([''.join(['{0:10n}'.format(d) for d in duplIDs[i: i + 8]]) for i in range(0, len(duplIDs), 8)])
            logging.error('Duplicate Node IDs found:\n{0}'.format(tmp))
            raise IndexError('Duplicate Node IDs found.')
        logging.info('Node IDs checked: OK')
        return False

    def distance(self, ndID1: int, ndID2: int):
        pass


class Nodes2D(Nodes):
    """
    Collection of Node objects
    """
    @classmethod
    def from_str(cls, string: str):
        lines = string.split('\n')
        nodes = cls()
        for line in lines:
            nodes.node.append(Node2D.from_str(line))
            nodes.count += 1
            nodes.iid.setdefault(nodes.node[-1].id, nodes.count)
        return nodes

    def __init__(self):
        super().__init__()

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
