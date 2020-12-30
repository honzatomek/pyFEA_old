import logging
import weakref

from misc.errors import *


logger = logging.getLogger(__name__)


class Data:
    _instances = dict()
    _command = 'DATA'
    _id = {'type': int, 'len': 12, 'prefix': ''}  # either 'int', 12, '' or 'str', 16, 'SOL_'
    _base_id = 100000001

    @classmethod
    def set_base(cls, base: int):
        """
        Set base for automatic numbering
        :param base: base number for automatic numbering
        :return:
        """
        try:
            # test if number
            assert base - 0 == base
            # test if > 0
            assert base > 0
        except AssertionError:
            message = f'{cls.__name__:s} base for automatic numbering must be number > 0'
            logger.error(message)
            raise ValueError(message)
        cls._base_id = int(base)

    @classmethod
    def __add(cls, obj: object):
        try:
            assert type(obj) == cls
        except AssertionError:
            message = f'{cls.__name__:s} add() attribute "obj" must be of type "{cls.__name__:s}", ' \
                      f'not "{type(obj).__name__:s}".'
            logger.error(message)
            raise ValueError(message)
        if obj.id in cls._instances:
            message = f'Duplicate {type(object).__name__} ID: {str(obj.id):s}'
            logger.error(message)
            raise DuplicateIDError(message)
        cls._instances[obj.id] = weakref.ref(obj)

    @classmethod
    def __del(cls, obj: object):
        try:
            assert type(obj) == cls
        except AssertionError:
            message = f'{cls.__name__:s} add() attribute "obj" must be of type "{cls.__name__:s}", ' \
                      f'not "{type(obj).__name__:s}".'
            logger.error(message)
            raise ValueError(message)
        cls._instances.pop(obj.id, None)

    @classmethod
    def __remove_dead_instances(cls):
        for key, ref in cls._instances:
            obj = ref()
            if obj is None:
                cls._instances.pop(key, None)

    @classmethod
    def get_instances(cls):
        for key, ref in cls._instances:
            obj = ref()
            if obj is not None:
                yield obj
            else:
                cls._instances.pop(key, None)

    @classmethod
    def count_instances(cls):
        return len(cls._instances)

    @classmethod
    def exists(cls, id: int or str):
        return id in cls._instances

    @classmethod
    def next_free_id(cls):
        id = cls._base_id
        while True:
            if cls._id['type'] == int:
                id = max(max(cls._instances.keys()) + 1, cls._base_id)
            while cls.exists(cls._id['type'](cls._id['prefix'] + str(id))):
                id += 1
            try:
                assert id <= 999999999999
            except AssertionError:
                message = f'{cls.__name__:s}.next_free_id(() results in number overflow, ' \
                          f'id > 999 999 999 999 ({cls._id["type"](cls._id["prefix"] + str(id)):s}).'
                logger.error(message)
                raise OverflowError(message)
            yield cls._id['type'](cls._id['prefix'] + str(id))

    @classmethod
    def _get_instance(cls, id):
        try:
            assert type(id) is cls._id['type']
        except AssertionError:
            message = f'{cls.__name__:s} is of type "{cls._id["type"].__name__:s}", not "{type(id).__name__}".'
            logger.error(message)
            raise ValueError(message)
        if id not in cls._instances:
            cls(id)
        ref = cls._instances[id]
        return ref()

    def __init__(self, id=None):
        self.id = id
        type(self).__add(self)

    def __del__(self):
        type(self).__del(self)

    def __repr__(self):
        if type(self)._id['type'] is int:
            message = f'{type(self).__name__:s}(id={self.id:n})'
        else:
            message = f'{type(self).__name__:s}(id="{str(self.id):s}")'
        return message

    def __str__(self):
        if type(self)._id['type'] is int:
            message = str('{0:' + str(type(self)._id['len']) + 'n}').format(self.id)
        else:
            message = str('{0:' + str(type(self)._id['len']) + 's}').format(self.id)
        if ' ' in message:
            message = "'" + message + "'"
        return message

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id):
        if id is None:
            id = type(self).next_free_id()
            message = f'{type(self).__name__:s} id {str(self.__id):s} was automatically generated.'
            logger.info(message)

        try:
            assert type(id) is type(self)._id['type']
        except AssertionError:
            message = f'{type(self).__name__:s} attribute "id" must be "{type(self)._id["type"]:s}", ' \
                      f'not {type(id).__name__:s} (value = {str(id):s}).'
            logger.error(message)
            raise ValueError(message)

        try:
            assert not type(self).exists(id)
        except AssertionError:
            message = f'{type(self).__name__:s} attribute "id" ({str(id):s}) must be unique.'
            logger.error(message)
            raise DuplicateIDError(message)

        self.__id = id


class DataSet(Data):
    _type = Data
    _instances = dict()
    _command = 'DATASET'
    _id = {'type': str, 'len': 16, 'prefix': 'SOL_'}  # either 'int', 12, '' or 'str', 16, 'SOL_'
    _base_id = 100000001

    @classmethod
    def collect(cls):
        mds = cls()
        for id in cls._instances:
            ds = cls._instances[id]()
            if ds is not mds:
                for obj in ds:
                    mds._add_object(obj)

    def __init__(self, id = None):
        super(DataSet, self).__init__(id=id)
        self.objects = dict()

    def __repr__(self):
        message = f"{type(self).__name__:s}(id={str(self.id):s})"
        for obj in self.objects:
            message += f'\n{type(self).__name__:s}._get_instance({str(self.id):s})._add_object({repr(obj):s})'
        return message

    def __str__(self):
        message = f'{type(self).__name__:s} {str(self.id):s}: ' \
                  f'{str(self.count()):s} objects of type {type(self)._type.__name__:s}.'
        return message

    def __iadd__(self, other):
        self._add_object(other)
        return self

    def __isub__(self, other):
        self._remove_object(other)
        return self

    def __iter__(self):
        self.__n = 0
        return self

    def __next__(self):
        objects = self.objects.items()
        if self.__n < len(objects):
            n = self.__n
            self.__n += 1
            return objects[n]
        else:
            raise StopIteration

    def _add_object(self, obj: object):
        try:
            assert isinstance(obj, type(self)._type) or issubclass(type(obj), type(self)._type)
        except AssertionError:
            message = f'{type(self).__name__:s} {str(self.id):s} cannot add ' \
                      f'object of type {type(obj).__name__:s} ({str(obj):s}).'
            logger.error(message)
            raise ValueError(message)
        self.objects.setdefault(obj.id, obj)

    def _create_object(self, obj_type: type, *args, **kwargs):
        try:
            assert obj_type is type(self)._type or issubclass(obj_type, type(self)._type)
        except AssertionError:
            message = f'{type(self).__name__:s} {str(self.id):s} cannot add ' \
                      f'object of type "{obj_type.__name__:s}" ' \
                      f'(wrong call: {obj_type.__name__:s}({", ".join([str(a) for a in args]):s}, ' \
                      f'{", ".join({str(key) + "=" + str(value) for (key, value) in kwargs}):s}).'
            logger.error(message)
            raise TypeError(message)
        obj = obj_type(args, kwargs)
        self.objects.setdefault(obj.id, obj)

    def _remove_object(self, obj: object):
        try:
            assert isinstance(obj, type(self)._type) or issubclass(type(obj), type(self)._type)
        except AssertionError:
            message = f'{type(self).__name__:s} {str(self.id)} cannot remove ' \
                      f'object of type {type(obj).__name__:s} ({str(obj)}).'
            logger.error(message)
            raise ValueError(message)
        try:
            assert obj.id in self.objects
        except AssertionError:
            message = f'{type(self).__name__:s} {str(self.id):s} does not contain ' \
                      f'{type(obj).__name__:s} {str(obj.id):s} and therefore it cannot be removed.'
            logger.warning(message)
        self.objects.pop(obj.id, None)

    def _get_objects_by_type(self):
        objects_by_type = {}
        for id, obj in self.objects:
            if type(obj).__name__ not in objects_by_type:
                objects_by_type.setdefault(type(obj).__name__, [obj])
            else:
                objects_by_type[type(obj).__name__].append(obj)
        return objects_by_type

    def count(self):
        return len(self.objects)

    def _object_ids(self):
        return sorted(self.objects.keys())

    def stat(self):
        ids = sorted(self.objects.keys())
        return len(ids), ids[0], ids[-1]

    def stat_str(self):
        count, max, min,_ = [str(s) for s in self.stat()]
        return 'number: %9s    minID: %9s    maxID: %9s' % (count, max, min)

    def get(self, id):
        try:
            assert id in self.objects
        except AssertionError:
            message = f'{type(self).__name__:s} {str(self.id):s} does not contain ' \
                      f'{type(self)._type.__name__:s} {str(id):s}.'
            logger.warning(message)
            return None
        return self.objects[id]
