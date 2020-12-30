import logging
import weakref

from misc.errors import *


logger = logging.getLogger(__name__)


class Data:
    _instances = dict()
    _command = 'DATA'
    _last_label_id = 1
    _base_id = 100000001

    # 0 = not required, 1 = required, 2 = required and unique
    _locks = {'label': 0}
    # either id or label
    _store_as = 'id'

    @classmethod
    def set_base_id(cls, id: int):
        try:
            assert id > 0
            cls._base_id = id
        except AssertionError:
            message = f'{cls.__name__:s} base id must be > 0, not {str(id):s}.'

    @classmethod
    def set_locks(cls, label_lock: str = None):
        if label_lock is None:
            cls._locks['label'] = 0
        elif label_lock == 'required' or label_lock == 1:
            cls._locks['label'] = 1
        elif label_lock == 'unique' or label_lock == 2:
            cls._locks['label'] = 2

    @classmethod
    def __add(cls, obj: object):
        if cls._store_as == 'id':
            if obj.id in cls._instances:
                message = f'Duplicate {type(object).__name__} ID: {str(obj.id):s}'
                logger.error(message)
                raise DuplicateIDError(message)
            cls._instances[obj.id] = weakref.ref(obj)
        else:
            if obj.label in cls._instances:
                message = f'Duplicate {type(object).__name__} label: {obj.label:s}'
                logger.error(message)
                raise DuplicateLabelError(message)
            cls._instances[obj.label] = weakref.ref(obj)

    @classmethod
    def __del(cls, obj: object):
        if cls._store_as == 'id':
            cls._instances.pop(obj.id, None)
        else:
            cls._instances.pop(obj.label, None)

    @classmethod
    def __remove_dead_refs(cls):
        for key, ref in cls._instances:
            obj = ref()
            if obj is None:
                cls._instances.pop(key, None)

    @classmethod
    def __get_instances(cls):
        for key, ref in cls._instances:
            obj = ref()
            if obj is not None:
                yield obj
            else:
                cls._instances.pop(key, None)

    @classmethod
    def count(cls):
        return len(cls._instances)

    @classmethod
    def next_free_id(cls):
        while True:
            if len(cls._instances) == 0:
                last_id = 0
            else:
                last_id = max(cls._instances.keys())
            yield max(last_id + 1, cls._base_id)

    @classmethod
    def getID(cls, id):
        if cls._store_as == 'id':
            if id in cls._instances:
                ref = cls._instances[id]
                return ref()
        else:
            for instance in cls.__get_instances():
                if instance.id == id:
                    return instance
        return None

    @classmethod
    def next_free_label(cls):
        label_prefix = f'{cls._command:8s}'.strip(' ') + '_'
        while True:
            cls._last_label_id += 1
            if cls._last_label_id > 9999999:
                message = f'Automatically generated labels for {cls.__name__:s} have overflown max number = 9 999 999.'
                logger.error(message)
                raise OverflowError(message)
            label = label_prefix + f'{cls._last_label_id:07n}'
            if not cls.label_exists(label):
                yield label

    @classmethod
    def getLabel(cls, label: str):
        if cls._store_as == 'id':
            for instance in cls.__get_instances():
                if instance.label == label:
                    return instance
        else:
            if label in cls._instances:
                ref = cls._instances[label]
                return ref()
        return None

    @classmethod
    def getType(cls, obj_type: type):
        for instance in cls.__get_instances():
            if isinstance(instance, obj_type):
                yield instance

    @classmethod
    def id_exists(cls, id: int):
        if cls._store_as == 'id':
            return id in cls._instances
        else:
            for instance in cls.__get_instances():
                if instance.id == id:
                    return True
        return False

    @classmethod
    def label_exists(cls, label: str):
        if cls._store_as == 'id':
            for instance in cls.__get_instances():
                if instance.label == label:
                    return True
        else:
            return label in cls._instances
        return False

    def __init__(self, id: int = None, label: str = None):
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

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id: int = None):
        if id is None:
            if type(self)._store_as == 'id':
                self.__id = type(self).next_free_id()
                logger.warning(f'{type(self).__name__:s} ID {str(self.__id):s} was assigned automatically.')
            else:
                self.__id = None
        elif not isinstance(id, int):
            message = f'{type(self).__name__:s} attribute "id" must be of type int, ' \
                      f'not "{type(id).__name__:s}" (value: {str(id):s})'
            logger.error(message)
            raise AttributeError(message)
        elif type(self).id_exists(id):
            message = f'Duplicate {type(self).__name__} ID: {id}'
            logger.error(message)
            raise DuplicateIDError(message)
        else:
            self.__id = id

    @property
    def label(self):
        return self.__label

    @label.setter
    def label(self, label: str = None):
        if label is None:
            if type(self)._label_lock > 0:
                self.__label = type(self).next_free_label()
            else:
                self.__label = None
        elif not isinstance(label, str):
            message = f'{type(self).__name__:s} attribute "label" must be of type str, ' \
                      f'not "{type(label).__name__:s}" (value: {str(label):s})'
            logger.error(message)
            raise AttributeError(message)
        elif type(self)._label_lock > 1 and type(self).label_exists(label):
            message = f'Duplicate {type(self).__name__:s} label: {label:s}'
            logger.error(message)
            raise DuplicateLabelError(message)
        else:
            self.__label = label


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

    def _object_ids(self):
        return sorted(self._im.keys())

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
        message = f"{type(self).__name__:s}(id={self.id:n}, label='{self.label:s}')"
        for obj in self.objects:
            message += f'\n{type(self).__name__:s}.getID({self.id:n})._add_object({repr(obj):s})'
        return message

    def __str__(self):
        message = ''
        objs_by_type = self._get_objects_by_type()
        for obj_type in objs_by_type.keys():
            message += f'${type(self)._command:s} TYPE = {obj_type:s}\n'
            for obj in objs_by_type[obj_type]:
                message += str(obj) + '\n'
            message += '\n'
        return message[:-1]

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

    def stat(self):
        ids = self._im.keys()
        return self.count(), min(ids), max(ids)

    def stat_str(self):
        return 'number: %9d    minID: %9d    maxID: %9d' % self.stat()

    def count(self):
        return len(self.objects)

    def get(self, identifier: (int, str)):
        if isinstance(identifier, int):
            return self.objects[self._im[identifier]]

        elif isinstance(identifier, str):
            for obj in self.objects:
                if obj.label == identifier:
                    return obj
        return None


if __name__ == '__main__':
    logger.disabled = True
