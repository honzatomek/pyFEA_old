import logging
import numpy as np

from misc.data_template import Data, DataSet
# from structure.nodes import Node


logger = logging.getLogger(__name__)


class CSys(Data):
    _instances = dict()
    _command = 'CSYS'
    _id = {'type': int, 'len': 12, 'prefix': ''}
    _base_id = 100000001

    @staticmethod
    def __process_coordinates(coors, name='__process_coordinates'):
        try:
            assert isinstance(coors, list) or isinstance(coors, tuple) or isinstance(coors, np.ndarray)
        except AssertionError:
            message = f'{name:s} input coordinates must be an iterable, ' \
                      f'not {type(coors).__name__:s} ({str(coors):s}).'
            raise ValueError(message)
        c = np.array(coors, dtype=float)
        try:
            assert c.shape == (3,) or c.shape == (1, 3) or c.shape == (3, 1)
        except AssertionError:
            message = f'{name:s} input coordinates must be of length 3 not {len(c):n} ({str(coors):s}).'
            raise ValueError(message)
        return c.reshape((3,))

    @classmethod
    def from_xz(cls, id: int,
                origin: [float, float, float] or [float, float, float],
                x_axis: [float, float, float] or [float, float, float],
                z_axis: [float, float, float] or [float, float, float]):

        coors = {'origin': [origin, None], 'x_axis': [x_axis, None], 'z_axis': [z_axis, None]}
        for key, value in coors.items():
            try:
                value[1] = cls.__process_coordinates(value[0], key)
            except ValueError as e:
                message = f'{cls.__name__:s} {str(id):s} ' + str(e)
                logger.error(message)
                raise ValueError(message)

        coors.setdefault('y_axis', [None, np.cross(coors['z_axis'][1], coors['x_axis'][1])])
        return cls(id, coors['origin'][1], coors['x_axis'][1], coors['y_axis'][1])

    @classmethod
    def from_zx(cls, id: int,
                origin: [float, float, float] or [float, float, float],
                z_axis: [float, float, float] or [float, float, float],
                x_axis: [float, float, float] or [float, float, float]):

        coors = {'origin': [origin, None], 'x_axis': [x_axis, None], 'z_axis': [z_axis, None]}
        for key, value in coors.items():
            try:
                value[1] = cls.__process_coordinates(value[0], key)
            except ValueError as e:
                message = f'{cls.__name__:s} {str(id):s} ' + str(e)
                logger.error(message)
                raise ValueError(message)

        coors.setdefault('y_axis', [None, np.cross(coors['z_axis'][1], coors['x_axis'][1])])
        coors['x_axis'][1] = np.cross(coors['y_axis'][1], coors['z_axis'][1])
        return cls(id, coors['origin'][1], coors['x_axis'][1], coors['y_axis'][1])

    @classmethod
    def from_yz(cls, id: int,
                origin: [float, float, float] or [float, float, float],
                y_axis: [float, float, float] or [float, float, float],
                z_axis: [float, float, float] or [float, float, float]):

        coors = {'origin': [origin, None], 'y_axis': [y_axis, None], 'z_axis': [z_axis, None]}
        for key, value in coors.items():
            try:
                value[1] = cls.__process_coordinates(value[0], key)
            except ValueError as e:
                message = f'{cls.__name__:s} {str(id):s} ' + str(e)
                logger.error(message)
                raise ValueError(message)

        coors.setdefault('x_axis', [None, np.cross(coors['y_axis'][1], coors['z_axis'][1])])
        return cls(id, coors['origin'][1], coors['x_axis'][1], coors['y_axis'][1])

    @classmethod
    def from_zy(cls, id: int,
                origin: [float, float, float] or [float, float, float],
                z_axis: [float, float, float] or [float, float, float],
                y_axis: [float, float, float] or [float, float, float]):

        coors = {'origin': [origin, None], 'y_axis': [y_axis, None], 'z_axis': [z_axis, None]}
        for key, value in coors.items():
            try:
                value[1] = cls.__process_coordinates(value[0], key)
            except ValueError as e:
                message = f'{cls.__name__:s} {str(id):s} ' + str(e)
                logger.error(message)
                raise ValueError(message)

        coors.setdefault('x_axis', [None, np.cross(coors['y_axis'][1], coors['z_axis'][1])])
        coors['y_axis'][1] = np.cross(coors['z_axis'][1], coors['x_axis'][1])
        return cls(id, coors['origin'][1], coors['x_axis'][1], coors['y_axis'][1])

    @classmethod
    def from_yx(cls, id: int,
                origin: [float, float, float] or [float, float, float],
                y_axis: [float, float, float] or [float, float, float],
                x_axis: [float, float, float] or [float, float, float]):

        coors = {'origin': [origin, None], 'x_axis': [x_axis, None], 'y_axis': [y_axis, None]}
        for key, value in coors.items():
            try:
                value[1] = cls.__process_coordinates(value[0], key)
            except ValueError as e:
                message = f'{cls.__name__:s} {str(id):s} ' + str(e)
                logger.error(message)
                raise ValueError(message)

        coors.setdefault('z_axis', [None, np.cross(coors['x_axis'][1], coors['y_axis'][1])])
        coors['x_axis'][1] = np.cross(coors['y_axis'][1], coors['z_axis'][1])
        return cls(id, coors['origin'][1], coors['x_axis'][1], coors['y_axis'][1])

    def __init__(self, id: int,
                 origin: [float, float, float] or [float, float, float],
                 x_axis: [float, float, float] or [float, float, float],
                 y_axis: [float, float, float] or [float, float, float]):
        super(CSys, self).__init__(id=id)
        self.origin = origin
        self.x_axis = x_axis
        self.y_axis = y_axis

    @property
    def origin(self):
        return self.__o

    @origin.setter
    def origin(self, origin: [float, float, float]):
        try:
            self.__o = self.__process_coordinates(origin, 'origin')
        except ValueError as e:
            message = f'{type(self).__name__:s} {str(self.id):s} ' + str(e)
            logger.error(message)
            raise ValueError(message)

    @property
    def x_axis(self):
        return self.__x

    @x_axis.setter
    def x_axis(self, x_axis: [float, float, float]):
        try:
            v = self.__process_coordinates(x_axis, 'x_axis')
            v = v / np.linalg.norm(v)
            self.__x = v
        except ValueError as e:
            message = f'{type(self).__name__:s} {str(self.id):s} ' + str(e)
            logger.error(message)
            raise ValueError(message)

    @property
    def y_axis(self):
        return self.__y

    @y_axis.setter
    def y_axis(self, y_axis: [float, float, float]):
        try:
            v = self.__process_coordinates(y_axis, 'y_axis')
            v = v / np.linalg.norm(v)
            z = np.cross(self.x_axis, v)
            self.__y = np.cross(z, self.x_axis)
        except ValueError as e:
            message = f'{type(self).__name__:s} {str(self.id):s} ' + str(e)
            logger.error(message)
            raise ValueError(message)

    @property
    def z_axis(self):
        return np.cross(self.x_axis, self.y_axis)

    @property
    def rotation_matrix_gcs_lcs(self):
        return np.array([self.x_axis, self.y_axis, self.z_axis]).reshape((3, 3))

    @property
    def rotation_matrix_lcs_gcs(self):
        return self.rotation_matrix_gcs_lcs.T

    def transform_to_global(self, coors: [float, float, float]):
        try:
            c = self.__process_coordinates(coors, 'transform_to_global')
            c = self.rotation_matrix_lcs_gcs @ c.T
            c += self.origin.T
            return c.reshape((3,))
        except ValueError as e:
            message = f'{type(self).__name__:s} {str(self.id):s} '
            logger.error(message)
            raise ValueError(message)

    def transform_to_local(self, coors: [float, float, float]):
        try:
            c = self.__process_coordinates(coors, 'transform_to_local')
            c -= self.origin
            c = self.rotation_matrix_gcs_lcs @ c.T
            return c.reshape((3,))
        except ValueError as e:
            message = f'{type(self).__name__:s} {str(self.id):s} '
            logger.error(message)
            raise ValueError(message)


if __name__ == '__main__':
    a = CSys(1, np.array([1, 1, 1]), np.array([0, 1, 0]), np.array([-1, 0, 0]))
    b = np.array([1, 2, 0], dtype=float)
    print(b)
    b = a.transform_to_local(b)
    print(b)
    b = a.transform_to_global(b)
    print(b)

    c = CSys.from_xz(2, [1, 1, 1], [0, 1, 0], [0, 0, 1])
    pass

