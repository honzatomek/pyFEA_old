import math
import logging
from misc.misc import eng, Data, DataSet
from misc.errors import *


logger = logging.getLogger(__name__)


class Node(Data):
    """
    Parent class for all Nodes
    """
    _ids = set()
    _instances = set()
    _counter = 0
    _command = 'NODE'
    _last_label_id = 0

    def __init__(self, id: int, coors: list, label: str = None):
        """
        Node initialization
        :param id:    Unique Node ID
        :param label: Optional Node Label, max 16 chars, rest will be cropped
        """
        if (not isinstance(coors, list)) and (not isinstance(coors, tuple)):
            raise AttributeError(f'{type(self).__name__:s} "coors" attribute must be a list or a tuple, '
                                 f'not {type(coors).__name__:s} ({str(coors):s}).')
        if len(coors) < 2:
            raise AttributeError(f'{type(self).__name__:s} "coors" attribute must be of len >= 2.')
        self._coor = coors
        super(Node, self).__init__(id, label)

    def __del__(self):
        super(Node, self).__del__()

    def __repr__(self):
        if self.label is not None:
            return f"{type(self).__name__}(id={self.id:n}, coors={eng(self._coor).strip():s}, " \
                   f"label='{self.label:s}')"
        else:
            return f'{type(self).__name__}(id={self.id:n}, coors={eng(self._coor).strip():s})'

    def __str__(self):
        message = f' {self.id:9n}' + ''.join([f' {eng(coor):s}' for coor in self._coor])
        if self.label is not None:
            if ' ' in self.label:
                message += f"  : '{self.label:s}'"
            else:
                message += f'  : {self.label:s}'
        return message

    @property
    def coor(self):
        return self._coor


class Nodes(DataSet):
    """
    Class for collection of Node objects
    """
    _type = Node
    _ids = set()
    _instances = set()
    _counter = 0
    _command = 'NODE'
    _last_label_id = 0

    def __init__(self, id: int = None, label: str = None):
        super(Nodes, self).__init__(Node, id, label)

    def node_ids(self):
        return self._object_ids()

    def add(self, id: int, coors: list, label: str = None):
        self._create_object(self._type, id, coors, label)

    def distance(self, node_id1: int, node_id2: int):
        nd1 = self._type.getID(node_id1).coor
        nd2 = self._type.getID(node_id2).coor
        distance = 0
        for i in range(len(nd1)):
            distance += (nd2[i] - nd1[i]) ** 2
        return math.sqrt(distance)


if __name__ == '__main__':
    pass
