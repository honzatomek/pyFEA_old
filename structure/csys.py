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
    _csys_types = {'cartesian': {'names': ['cartesian', 'cart'], 'form': ['xy', 'yx', 'xz', 'zx', 'yz', 'zy']},
                   'cylindrical': {'names': ['cylindrical', 'cyl'], 'form': ['rf', 'rz', 'zr']}}
    # TODO: implement cylindrical
    _input_types = ['vectors', 'coordinates', 'nodes']
    # TODO: implement nodes

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
    def __process_dict_coordinates(cls, id: int, coors: dict):
        for key in coors:
            try:
                coors[key][1] = cls.__process_coordinates(coors[key][0], key)
            except ValueError as e:
                message = f'{cls.__name__:s} {str(id):s} ' + str(e)
                logger.error(message)
                raise ValueError(message)
        return coors

    def __init__(self, id: int,
                 origin: [float, float, float],
                 coor1: [float, float, float],
                 coor2: [float, float, float],
                 csys_type='cartesian', form='xy', input_type='vectors'):
        super(CSys, self).__init__(id=id)
        self.type = csys_type
        self.form = form
        self.input = input_type
        self.origin = origin
        self.coor1 = coor1
        self.coor2 = coor2
        self.__consolidated = False
        self.__axes = []

    def __error(self, message: str, exception: Exception = None):
        try:
            assert isinstance(exception, Exception) or issubclass(type(exception), Exception)
        except Exception as e:
            exception = Exception
        message = f'{type(self).__name__:s} {str(self.id):s} ' + message
        logger.error(message)
        raise exception(message)

    def consolidate(self):
        # TODO: implement Nodes and Cylindrical CSys
        u = None
        v = None
        if self.type == 'cartesian':
            if self.input == 'vectors':
                u = self.coor1
                v = self.coor2
            elif self.input == 'coordinates':
                u = self.coor1 - self.origin
                v = self.coor2 - self.origin
            else:
                self.__error(f'{self.input:s} input_type is not yet implemented.')

            u = u / np.linalg.norm(u)
            v = v / np.linalg.norm(v)

            x = None
            y = None
            z = None

            if self.form == 'xy':
                x = u
                z = np.cross(x, v)
                y = np.cross(z, x)
            elif self.form == 'yx':
                y = u
                z = np.cross(v, y)
                x = np.cross(y, z)
            elif self.form == 'xz':
                x = u
                y = np.cross(v, x)
                z = np.cross(x, y)
            elif self.form == 'zx':
                z = u
                y = np.cross(z, v)
                x = np.cross(y, z)
            elif self.form == 'yz':
                y = u
                x = np.cross(y, v)
                z = np.cross(x, y)
            elif self.form == 'zy':
                z = u
                x = np.cross(v, z)
                y = np.cross(z, x)
            else:
                self.__error(f'{self.form:s} formulation is not yet implemented.')

            self.__axes = [x / np.linalg.norm(x), y / np.linalg.norm(y), z / np.linalg.norm(z)]

        else:
            self.__error(f'{self.type:s} type is not yet implemented.')

        self.__consolidated = True

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, csys_type: str):
        if csys_type is None:
            for key in type(self)._csys_types:
                self.__type = key
                return

        try:
            assert isinstance(csys_type, str)
        except AssertionError:
            message = f'csys_type attribute must be an instance of "str", ' \
                      f'not "{type(csys_type).__name__:s}" (value: {str(csys_type):s}).'
            self.__error(message, ValueError)

        try:
            assert True in [csys_type in s['names'] for ct, s in type(self)._csys_types.items()]
        except AssertionError:
            message = f'csys_type must be one of {str([s["names"] for ct, s in type(self)._csys_types.items()]):s}, ' \
                      f'not {str(csys_type):s}.'
            self.__error(message)
        self.__type = [ct for ct, s in type(self)._csys_types.items() if csys_type in s['names']][0]

    @property
    def form(self):
        return self.__form

    @form.setter
    def form(self, form: str):
        if form is None:
            self.__form = type(self)._csys_types[self.type]['form'][0]
            return

        try:
            assert isinstance(form, str)
        except AssertionError:
            message = f'form attribute must be an instance of "str", ' \
                      f'not "{type(form).__name__:s}" (value: {str(form):s}).'
            self.__error(message, ValueError)

        try:
            assert form in type(self)._csys_types[self.type]['form']
        except AssertionError:
            message = f'form must be one of {str(type(self)._csys_types[self.type]["form"]):s}, ' \
                      f'not {str(form):s}.'
            self.__error(message)

        self.__form = form

    @property
    def input(self):
        return self.__input

    @input.setter
    def input(self, input_type: str):
        try:
            assert isinstance(input_type, str)
        except AssertionError:
            message = f'input_type attribute must be an instance of "str", ' \
                      f'not "{type(input_type).__name__:s}" (value: {str(input_type):s}).'
            self.__error(message, ValueError)

        try:
            assert input_type in type(self)._input_types
        except AssertionError:
            message = f'input_type must be one of {str(type(self)._input_types):s}, ' \
                      f'not {str(input_type):s}.'
            self.__error(message)

        self.__input = input_type

    @property
    def origin(self):
        return self.__o

    @origin.setter
    def origin(self, origin: [float, float, float]):
        try:
            self.__o = self.__process_coordinates(origin, 'origin')
        except ValueError as e:
            self.__error(str(e))

    @property
    def coor1(self):
        return self.__c1

    @coor1.setter
    def coor1(self, coor1: [float, float, float]):
        try:
            self.__c1 = self.__process_coordinates(coor1, 'coor1')
        except ValueError as e:
            self.__error(str(e))

    @property
    def coor2(self):
        return self.__c2

    @coor2.setter
    def coor2(self, coor2: [float, float, float]):
        try:
            self.__c2 = self.__process_coordinates(coor2, 'coor2')
        except ValueError as e:
            self.__error(str(e))

    @property
    def x_axis(self):
        if not self.__consolidated:
            try:
                self.consolidate()
            except Exception as e:
                self.__error(f'consolidation failed.')

        if self.type != 'cartesian':
            self.__error(f'{self.type:s} has no x_axis property.')
        else:
            return self.__axes[0]

    @property
    def y_axis(self):
        if not self.__consolidated:
            try:
                self.consolidate()
            except Exception as e:
                self.__error(f'consolidation failed.')

        if self.type != 'cartesian':
            self.__error(f'{self.type:s} has no y_axis property.')
        else:
            return self.__axes[1]

    @property
    def z_axis(self):
        if not self.__consolidated:
            try:
                self.consolidate()
            except Exception as e:
                self.__error(f'consolidation failed.')

        if self.type != 'cartesian':
            self.__error(f'{self.type:s} has no z_axis property.')
        else:
            return self.__axes[2]

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

    c = CSys(2, [1, 1, 1], [0, 1, 0], [0, 0, 1])
    pass

