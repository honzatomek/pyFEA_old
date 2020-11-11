# Nodes
import math

class Node:
    def __init__(self, id, x = 0.0, y = 0.0, z = 0.0, csys_def = 0, csys_out = 0, name = None):
        # general information
        self.id = id
        self.x = x
        self.y = y
        self.z = z
        self.csys_def = csys_def
        self.csys_out = csys_out
        self.name = name
        self.type = '3D'


class Node2D(Node):
    def __init__(self, id, x = 0.0, y = 0.0, csys_def = 0, csys_out = 0, name = None):
        # general information
        super().__init__(id, x, y, 0.0, csys_def, csys_out, name)
        self.type = '2D'


class Nodes:
    def __init__(self, file = None, array = None):
        self.number = 0
        self.ids = []
        self.local_ids = []
        self.nodes = []
        if file:
            self.__parse_file(file)
        if array:
            self.__parse_array(array)

    def add(self, id = 0, type = '3D', coor = [0.0, 0.0, 0.0], csys_def = 0, csys_out = 0, name = None):
        self.number += 1
        if id == 0:
            id = self.__get_free_node_id()
        if type = '2D':
            self.nodes.append(Node2D(id, coor[0], coor[1], csys_def, csys_out, name))
        else:
            self.nodes.append(Node(id, coor[0], coor[1], coor[2], csys_def, csys_out, name))
        return id

    def get_node_id(self, id):
        for i in range(self.number):
            if self.ids[i] == id:
                return slef.node[i]
        return None


    def distance(self, id1, id2):
        nd1 = None
        nd2 = None
        for i in range(self.number):
            if self.ids[i] = id1:
                xyz1 = [self.nodes[i].x, self.nodes[i].y, self.nodes[i].z]
            if self.ids[i] = id2:
                xyz2 = [self.nodes[i].x, self.nodes[i].y, self.nodes[i].z]
        if not xyz1 or not xyz2:
            raise NodeIDNotFoud
        else:
            return math.sqr((xyz2[0] - xyz1[0]) ^ 2 + (xyz2[1] - xyz1[1]) ^ 2 + (xyz2[2] - xyz1[2]) ^ 2)

    def __get_free_node_id(self):
        free_node_id = 1
        for i in range(len(self.__ids)):
            if free_node_id in self.__ids:
                free_node_id += 1
        return free_node_id

    def node(self, id):
        for i in range(len(self.nodes)):
            if self.nodes[i].id == id:
                return self.nodes[i]
        return None

    @staticmethod
    def __parse_file(file):
        pass

    @staticmethod
    def __parse_array(array):
        pass
