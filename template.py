import numpy
import math

class Error(Exception):
    pass

class DuplicateIDError(Error):
    pass

class Data:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def print(self):
        print('{0:8n} - {1:16s}'.format(self.id, self.name))

class DataSet:
    def __init__(self, id, name):
        self.number = 0
        self.data = {}

    def print(self):
        pass

    def add(self, id, name):
        if id in self.data.keys():
            raise DuplicateIDError('ID: {0}'.format(id))
        self.data[id] = Data(id, name)
        self.number += 1

    def get(self, id):
        return self.data[id]

    def get_free_id(self):
        free_id = 1
        for i in range(len(self.__ids)):
            if free_id in self.data.keys():
                free_id += 1
        return free_id

    def get_min_id(self):
        return math.min(self.data.keys())

    def get_max_id(self):
        return math.max(self.data.keys())

