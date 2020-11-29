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
        vals = [s.strip(' ') for s in input_string.split(' ')]
        vals = [s.strip(' ') for s in string.split(' ')]
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
        vals = [s.strip(' ') for s in input_string.split(' ')]
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


if __name__ == '__main__':
    nd = Node2D(1, 1000.0, 2000.0, 'test')
    print(nd)
    nd2 = eval(repr(nd))
    print(nd2)
    nd4 = Node2D.from_str('    10   5000.0    -30.0E+03   test2')
    print(nd4)
