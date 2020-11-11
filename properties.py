
class Property:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class Properties:
    def __init__(self, file = None, array = None):
        self.number = 0
        self.ids = []
        self.properties = []
        if file:
            self.read_file(file)
        if array:
            self.read_array(array)

    def read_file(self, file):
        pass

    def read_array(self, array):
        pass

    @staticmethod
    def __parse_file(file):
        pass

    @staticmethod
    def __parse_array(array):
        pass
