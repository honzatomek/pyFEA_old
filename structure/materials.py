from misc.misc import eng, Data, DataSet
from misc.errors import DuplicateIDError, DuplicateLabelError
import numpy as np


class Material(Data):
    _ids = set()
    _instances = set()
    _counter = 0
    _command = 'MATERIAL'
    _last_label_id = 0

    def __init__(self, label: str):
        if self.label_exists(label):
            raise DuplicateLabelError(f'Duplicate {type(self).__name__:s} label: {label:s}.')
        super(Material, self).__init__(label=label)

    def __del__(self):
        super(Material, self).__del__()


class LinearElastic(Material):
    _counter = 0

    @staticmethod
    def temperature_dependent(array: np.ndarray, temperature: float = 0.0):
        if array.shape[0] < 2:
            return array[0, 0]
        else:
            return np.interp(temperature, array[:, 0], array[:, 1])

    @staticmethod
    def convert_to_ndarray(value):
        # if already numpy array, do nothing
        if isinstance(value, np.ndarray):
            return value
        # process float
        elif isinstance(value, float):
            return np.array([[0.0, value]], dtype=float)
        # process array
        elif isinstance(value, list):
            return np.array(value, dtype=float)
        # process rest
        else:
            return np.array([[0.0, float(value)]], dtype=float)

    def __init__(self, label: str, density: np.array, youngs_modulus: np.array,
                 poissons_ratio: np.array, thermal_expansion_coefficient: np.array):
        """
        init method for LinearElasticMaterial, could be temperature dependent
        :param id:                             material ID
        :param label:                          material label
        :param density:                        material density, [temperature, density] if temperature dependent
        :param youngs_modulus:                 material youngs_modulus, [temperature, youngs_modulus] if temperature
                                               dependent
        :param poissons_ratio:                 material poissons_ratio, [temperature, poissons_ratio] if temperature
                                               dependent
        :param thermal_expansion_coefficient:  material thermal_expansion_coefficient,
                                               [temperature, thermal_expansion_coefficient] if temperature dependent
        """
        self._ro = self.convert_to_ndarray(density)
        self._E = self.convert_to_ndarray(youngs_modulus)
        self._nu = self.convert_to_ndarray(poissons_ratio)
        self._alpha = self.convert_to_ndarray(thermal_expansion_coefficient)
        super(LinearElastic, self).__init__(label=label)

    def ro(self, temperature: float = 0.0):
        return self.temperature_dependent(self._ro, temperature)

    def E(self, temperature: float = 0.0):
        return self.temperature_dependent(self._E, temperature)

    def nu(self, temperature: float = 0.0):
        return self.temperature_dependent(self._nu, temperature)

    def G(self, temperature: float = 0.0):
        return self.E(temperature) / (2. * (1. + self.nu(temperature)))

    def alpha(self, temperature: float = 0.0):
        return self.temperature_dependent(self._alpha, temperature)

    def __del__(self):
        super(LinearElastic, self).__del__()

    def __repr__(self):
        return f"{type(self).__name__:s}(label='{self.label:s}', " \
               f"density={eng(self._ro):s}, youngs_modulus={eng(self._E):s}, " \
               f"poissons_ratio={eng(self._nu):s}, " \
               f"thermal_expansion_coefficient={eng(self._alpha):s})"

    def __str__(self):
        retval = super(LinearElastic, self).__str__().split('\n')
        end = retval[-1]
        retval = retval[:-1]
        retval.append('  $DENSITY')
        retval.append(f'    {eng(self.ro):s}')
        retval.append('  $YOUNG')
        retval.append(f'    {eng(self.E):s}')
        retval.append('  $POISSON')
        retval.append(f'    {eng(self.nu):s}')
        retval.append('  $THERMEXP')
        retval.append(f'    {eng(self.alpha):s}')
        retval.append(end)
        return '\n'.join(retval)


class Materials(DataSet):
    """
    Class for collection of Material objects
    """
    _type = Material
    _ids = set()
    _instances = set()
    _counter = 0
    _command = 'MATERIAL'
    _last_label_id = 0

    def __init__(self, id: int = None, label: str = None):
        super(Materials, self).__init__(Material, id, label)

    # TODO:
    def __repr__(self):
        message = f"{type(self).__name__:s}(id={self.id:n}, label='{self.label:s}')"
        for obj in self.objects:
            message += f'\n{type(self).__name__:s}.getID({self.id:n})._add_obj({repr(obj):s})'
        return message

    def __str__(self):
        return '\n'.join([str(mat) for mat in self]) + '\n'
