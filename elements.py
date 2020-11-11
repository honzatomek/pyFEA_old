# Nodes

class Element:
    def __init__(self, id, pID):
        self.id = id
        self. pID = pID


class Element1D(Element):
    def __init__(self, id, ndA, ndB, pID):
        super().__init__(id, pID)
        self.ndA = ndA
        self.ndB = ndB


class Element2D(Element):
    def __init__(self, id, ndA, ndB, ndC, pID):
        super().__init__(id, pID)
        self.ndA = ndA
        self.ndB = ndB


class Elements:
    def __init__(self, file = None, array = None):
        self.number = 0
        self.ids = []
        self.local_ids = []
        self.elements = []
        if file:
            self.__parse_file(file)
        if array:
            self.__parse_array(array)

    def add(sellf, id, ndA = 0, ndB = 0, pID)
        pass

    @staticmethod
    def __parse_file(file):
        pass

    @staticmethod
    def __parse_array(array):
        pass
