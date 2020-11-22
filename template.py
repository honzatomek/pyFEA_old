#!/usr/bin/python3.6

from config import *

import weakref

class Error(Exception):
    pass


class DuplicateIDError(Error):
    pass


class InstanceSetMeta(type):
    '''
    Meta class with set of weak refs to all instances
    '''
    def __new__(cls, name, bases, attrs):
        new_cls = super(InstanceSetMeta, cls).__new__(cls, name, bases, attrs)
        new_cls._instances = set()
        return new_cls


class Data(metaclass=InstanceSetMeta):
    '''
    Basic Data class - id, name, set with all instances of the same subclass
    '''
    def __init__(self, id=-1, name=None):
        type(self)._instances.add(weakref.ref(self))
        self._id = None
        if id == -1 or id is None:
            self._id = type(self).next_free_id()
        else:
            try:
                exists = type(self).id_exists(id)
                self._id = id
            except DuplicateIDError as e:
                logging.exception(f'Creation of instance of {type(self).__name__}'
                                  f'failed, ID {id} already exists')

        if name is None:
            self._name = f'{self._id} - {type(self).__name__}'
        else:
            self._name = name

    def __str__(self):
        return '{0:8n} - {1:16s}'.format(self._id, self._name)

    def __repr__(self):
        return str(self)

    def __del__(self):
        type(self)._instances.remove(weakref.ref(self))

    def id(self):
        return self._id

    def name(self):
        return self._name

    @classmethod
    def get_id(cls, id):
        for instance in cls.get_instances():
            if instance.id() == id:
                return instance
        return None

    @classmethod
    def remove(cls, id):
        instance = cls.get_id(id)
        if instance is not None:
            cls._instances.remove(weakref.ref(instance))

    @classmethod
    def count(cls):
        return len(cls._instances)

    @classmethod
    def id_exists(cls, id):
        exists = False
        for instance in cls.get_instances():
            if instance.id() == id:
                exists = True
                # raise DuplicateIDError(f'Creation of instance of {cls.__name__}'
                #                        f'failed, ID {id} already exists')
                raise DuplicateIDError()
        return exists


    @classmethod
    def next_free_id(cls):
        id = 0
        for instance in cls.get_instances():
            if instance.id() > id:
                id = instance.id() + 1
        return id

    @classmethod
    def get_instances(cls):
        dead = set()
        for ref in cls._instances:
            obj = ref()
            if obj is not None:
                yield obj
            else:
                dead.add(ref)
        cls._instances -= dead


class DataSet(Data):
    '''
    Basic class for data sets
    '''
    def __init__(self, id, name):
        super().__init__(id, name)
        self._total = 0
        self._data = {}

    def __iter__(self):
        self._iter = 0
        return self

    def __next__(self):
        if self._iter >= self._total:
            raise StopIteration
        self._iter += 1
        return self._data[list(self._data.keys())[self._iter - 1]]

    def __len__(self):
        return self._total

    def print(self):
        print('${0:s} ID = {1:n} NAME = \'{2:s}\''.format(self._title, self._id, self._name))
        for i, id in enumerate(sorted([int(id) for id in self._data.keys()])):
            print('{0:8n}'.format(self._data[str(id)].id()), end='')
            if (i + 1) % 8 == 0:
                print()

    def add(self, id, name):
        if str(id) in self._data.keys():
            raise DuplicateIDError('Duplicate ID: {0}'.format(id))
        self._data.setdefault(str(id), type(self)(id, name))
        self._total += 1

    def get(self, id):
        return self._data[id]

    def get_free_id(self):
        free_id = 1
        for i in range(len(self._data.keys())):
            if str(free_id) in self._data.keys():
                free_id += 1
        return free_id

    def get_min_id(self):
        return min([int(i) for i in self._data.keys()])

    def get_max_id(self):
        return max([int(i) for i in self._data.keys()])

    @classmethod
    def count(cls):
        return len(cls._instances)

    @classmethod
    def get_instances(cls):
        dead = set()
        for ref in cls._instances:
            obj = ref()
            if obj is not None:
                yield obj
            else:
                dead.add(ref)
        cls._instances -= dead

    @classmethod
    def merge_all(cls):
        result = DataSet(0, None)
        for ds in cls.get_instances():
            if ds.id() != result.id():
                result._data.update(ds._data)
                result._total += ds._total
        return result


def merge(objects):
    result = type(objects[0])(0, str(type(objects[0])))
    for i in range(len(objects)):
        result._data.update(objects[i]._data)
    result._total = len(result._data.keys())
    return result


if __name__ == '__main__':
    a = DataSet(1, 'test 1')
    b = DataSet(2, 'test 2')
    for i in range(10):
        a.add(i + 1, 'test ' + str(i + 1))
        b.add(i + 101, 'test ' + str(i + 101))
    c = DataSet.merge_all()

    for z in c:
        print(str(z))

    c.print()
