
# from: https://rednafi.github.io/digressions/python/2020/06/26/python-metaclasses.html#special-methods-used-by-metaclasses
# from: https://www.python-course.eu/python3_metaclasses.php
# from: https://stackoverflow.com/questions/8628123/counting-instances-of-a-class

import weakref
import logging

# logging.basicConfig(level=logging.INFO, format='%(asctime)-8s%(levelname)-8s%(message)s', datefmt='%H%M%S')
logging.basicConfig(level=logging.INFO, format='%(asctime)6s *%(levelname).1s* %(message)s', datefmt='%H%M%S')


class MetaCount(type):
    def __new__(cls, name, bases, attrs):
        # logging.info(f'classname: {name}')
        # logging.warning(f'baseclasses: {bases}')
        # logging.error(f'attributes: {attrs}')
        new_cls = super(MetaCount, cls).__new__(cls, name, bases, attrs)
        new_cls._instances = set()
        return new_cls


class Parent(metaclass=MetaCount):
    def __init__(self):
        type(self)._instances.add(weakref.ref(self))
        logging.info(f'classname: {type(self).__name__}')
        logging.warning(f'baseclasses: {type(self).__bases__}')
        logging.error(f'attributes: {type(self).__dict__}')
        logging.critical(f'instances: {len(type(self)._instances)}')

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


class Child(Parent):
    def __init__(self):
        super().__init__()


class SubChild(Child):
    def __init__(self):
        super().__init__()


p = Parent()
c1 = Child()
c2 = Child()
s = SubChild()

print(p.count())
print(c1.count())
print(c2.count())
print(s.count())
