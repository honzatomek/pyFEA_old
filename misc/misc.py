import math
import logging
import weakref
import numpy as np

from misc.errors import *


logger = logging.getLogger(__name__)
# logger = logging.getLogger()


def format_eng(value: float, format_spec: str = ' {0:10.4f}E{1:+03n}'):
    """
    Formats float value into engineering format with exponent a multiple of 3
    :param value:        float or numpy float value
    :param format_spec:  string with format for mantisa and exponent e.g.: ' {0:9.3f}E{1:+03n}'
    :return:             formated value as string
    """
    try:
        if value == 0.0:
            return format_spec.format(0.0, 0)
        exponent = int(math.log10(abs(value)))
        exponent = exponent - exponent % 3
        mantissa = value / (10 ** exponent)
        return format_spec.format(mantissa, exponent)
    except OverflowError as e:
        logger.exception(e)
        return str('{0:' + str(len(format_eng(1.1, format_spec))) + 'n}').format(np.infty)
    except ValueError as e:
        logger.exception(e)
        return str('{0:' + str(len(format_eng(1.1, format_spec))) + 'n}').format(np.nan)
    except TypeError as e:
        logger.exception(e)
        return str('{0:' + str(len(format_eng(1.1, format_spec))) + 'n}').format(np.nan)


class Data:
    _ids = set()
    _instances = set()
    _counter = 0
    _command = 'DATA'
    _last_label_id = 0

    @classmethod
    def __add(cls, obj: object):
        try:
            cls._ids.add(obj.id)
            cls._instances.add(weakref.ref(obj))
            cls._counter += 1
        except AttributeError as e:
            logger.exception(e)
            raise e

    @classmethod
    def __del(cls, obj: object):
        try:
            cls._ids.remove(obj.id)
            cls._counter -= 1
        except (AttributeError, KeyError):
            pass

        remove = set()
        for ref in cls._instances:
            if obj == ref():
                remove.add(ref)
        cls._instances -= remove

    @classmethod
    def __remove_dead_refs(cls):
        dead = set()
        for ref in cls._instances:
            obj = ref()
            if obj is None:
                dead.add(ref)
        cls._instances -= dead

    @classmethod
    def __get_instances(cls):
        dead = set()
        for ref in cls._instances:
            obj = ref()
            if obj is not None:
                yield obj
            else:
                dead.add(ref)
        cls._instances -= dead

    @classmethod
    def instances(cls):
        return cls._counter

    @classmethod
    def next_free_id(cls):
        if len(cls._ids) == 0:
            return 1
        else:
            return max(cls._ids) + 1

    @classmethod
    def getID(cls, id):
        for instance in cls.__get_instances():
            if instance.id == id:
                return instance
        return None

    @classmethod
    def next_free_label(cls):
        cls._last_label_id += 1
        label = f'{cls._command:10s}'.strip(' ') + '_' f'{cls._last_label_id:05n}'
        while cls.label_exists(label):
            cls._last_label_id += 1
            label = f'{cls._command:10s}'.strip(' ') + '_' f'{cls._last_label_id:05n}'
        return label

    @classmethod
    def getLabel(cls, label: str):
        for instance in cls.__get_instances():
            if instance.label == label:
                return instance
        return None

    @classmethod
    def getType(cls, obj_type: type):
        for instance in cls.__get_instances():
            if isinstance(instance, obj_type):
                yield instance

    @classmethod
    def id_exists(cls, id):
        if id in cls._ids:
            return True
        else:
            return False

    @classmethod
    def label_exists(cls, label: str):
        for instance in cls.__get_instances():
            if instance.label == label:
                return True
        return False

    def __init__(self, id: int = None, label: str = None):
        self.id = None
        self.label = None
        if id is None:
            id = type(self).next_free_id()
        elif not isinstance(id, int):
            raise AttributeError(f'{type(self).__name__:s} id must be of _type int (value: {str(id):s})')
        if type(self).id_exists(id):
            message = f'Duplicate {type(self).__name__} ID: {id}'
            logger.error(message)
            raise DuplicateIDError(message)
        self.id = id
        self.label = label
        type(self).__add(self)

    def __del__(self):
        type(self).__del(self)

    def __repr__(self):
        message = f'{type(self).__name__:s}(id={self.id:n}'
        if self.label is not None:
            message += f", label='{self.label:s}'"
        message += ')'
        return message

    def __str__(self):
        message = f'    {self.id:9n}'
        if self.label is not None:
            if ' ' in self.label:
                message += ' ' + '{0:16s}'.format("'{0:s}'".format(self.label))
            else:
                message += f' {self.label:32s}'
        return message


class DataSet(Data):
    _type = Data
    _ids = set()
    _instances = set()
    _counter = 0
    _command = 'GENERIC'
    _last_label_id = 0

    @classmethod
    def collect(cls):
        """
        Class method to collect objects of all DataSet classes of the same _type, concatenate them
        and return only one DataSet class containing all of the objects.
        :return: DataSet instance containing objects of all existing DataSet instances
        """
        # master DataSet
        mds = cls()
        for ref in cls._instances:
            ds = ref()
            if ds is not mds:
                for obj in ds:
                    mds._add_object(obj)
        return mds

    def _add_object(self, obj):
        if isinstance(obj, self._type) or issubclass(type(obj), self._type):
            self.objects.append(obj)
            self._im.setdefault(obj.id, self.count() - 1)
        else:
            raise TypeError(f'{str(obj):s} is neither an instance of class nor subclass of {self._type.__name__}')

    def _create_object(self, obj_type: type, *args, **kwargs):
        if obj_type is self._type or issubclass(obj_type, self._type):
            obj = obj_type(*args, **kwargs)
            self.objects.append(obj)
            self._im.setdefault(obj.id, self.count() - 1)
        else:
            raise TypeError(f'{obj_type.__name__:s} is neither {self._type.__name__} nor its sublcass')

    def _get_objects_by_type(self):
        objects_by_type = {}
        for obj in self.objects:
            if type(obj).__name__ not in objects_by_type.keys():
                objects_by_type.setdefault(type(obj).__name__, [obj])
            else:
                objects_by_type[type(obj).__name__].append(obj)
        return objects_by_type

    def __init__(self, obj_type: type = None, id: int = None, label: str = None):
        if id is None:
            id = type(self).next_free_id()
        if label is None:
            label = type(self).next_free_label()
        if type(self).label_exists(label):
            message = f'Duplicate {type(self).__name__} label: {label}'
            logger.error(message)
            raise DuplicateLabelError(message)
        super(DataSet, self).__init__(id=id, label=label)
        if obj_type is not None:
            self._type = obj_type
        self.objects = []
        self._im = {}  # mapping of ids

    def __repr__(self):
        message = f"{type(self).__name__:s}(id={self.id:n}, label='{self.label:s}')\n"
        for obj in self.objects:
            message += f'{type(self).__name__:s}.getID({self.id:n})._add_obj({repr(obj):s})\n'
        return message

    def __str__(self):
        message = ''
        objs_by_type = self._get_objects_by_type()
        for obj_type in objs_by_type.keys():
            message += f'${type(self)._command:s} TYPE = {obj_type:s}\n'
            for obj in objs_by_type[obj_type]:
                message += str(obj) + '\n'
            message += '\n'
        return message

    def __iter__(self):
        self.__n = 0
        return self

    def __next__(self):
        if self.__n < len(self.objects):
            n = self.__n
            self.__n += 1
            return self.objects[n]
        else:
            raise StopIteration

    def count(self):
        return len(self.objects)

    def get(self, identifier: (int, str)):
        if isinstance(identifier, int):
            return self.objects[self._im[identifier]]
            # for obj in self.objects:
            #     if obj.id == identifier:
            #         return obj
        elif isinstance(identifier, str):
            for obj in self.objects:
                if obj.label == identifier:
                    return obj
        return None


if __name__ == '__main__':
    logger.disabled = True
