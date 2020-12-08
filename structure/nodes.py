import math
import logging
from misc.misc import format_eng, Data, DataSet
from misc.errors import *


logger = logging.getLogger(__name__)


class Node2D(Data):
    """
    Parent class for all Nodes
    """
    _ids = set()
    _instances = set()
    _counter = 0
    _command = 'NODE'
    _last_label_id = 0

    @classmethod
    def from_str(cls, string: str):
        """
        Constructor for parsing string into a new instance of Node
        :param string:  String with data separated by ' ': 'NodeID  X  Z [: Label]'
        :return:        Node object
        """
        input_string = string.strip()
        if ':' in input_string:
            label = input_string.split(':')[1].strip().strip("'").strip('"')
            input_string = input_string.split(':')[0].strip()
        else:
            label = None

        while '  ' in input_string:
            input_string = input_string.replace('  ', ' ')
        vals = [s.strip(' ') for s in input_string.split()]

        if len(vals) < 3:
            raise AttributeError(f'String {string} must contain at least NodeID, X-Coor, Z-Coor')
        else:
            id = int(vals[0])
            x = float(vals[1])
            z = float(vals[2])

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
        super(Node2D, self).__del__()

    def __repr__(self):
        if self.label is not None:
            return f"{type(self).__name__}(id={self.id:n}, x={format_eng(self.x).strip():s}," \
                   f" z={format_eng(self.z).strip():s}, label='{self.label:s}')"
        else:
            return f'{type(self).__name__}(id={self.id:n}, x={format_eng(self.x):s},' \
                   f' z={format_eng(self.z):s})'

    def __str__(self):
        message = f' {self.id:9n} {format_eng(self.x):s} {format_eng(self.z):s}'
        if self.label is not None:
            if ' ' in self.label:
                message += f"  : '{self.label:s}'"
            else:
                message += f'  : {self.label:s}'
        return message

    def coor(self):
        return [self.x, self.z]


class Nodes2D(DataSet):
    """
    Class for collection of Node objects
    """
    _type = Node2D
    _ids = set()
    _instances = set()
    _counter = 0
    _command = 'NODE'
    _last_label_id = 0

    @classmethod
    def from_str(cls, string: str):
        lines = string.split('\n')
        nodes = cls()
        for line in lines:
            if line.strip() != '':
                nodes._add_object(Node2D.from_str(line))
        return nodes

    def __init__(self, id: int = None, label: str = None):
        super(Nodes2D, self).__init__(Node2D, id, label)

    def node_ids(self):
        return self._object_ids()

    def add(self, id: int, x: float, z: float, label: str = None):
        self._create_object(self._type, id, x, z, label)

    def distance(self, node_id1: int, node_id2: int):
        nd1 = self.objects[self._im[node_id1]]
        nd2 = self.objects[self._im[node_id2]]
        distance = math.sqrt((nd2.x - nd1.x) ** 2. + (nd2.z - nd1.z) ** 2.)
        return distance


if __name__ == '__main__':
    nds = eval('Nodes2D()')
    pass
