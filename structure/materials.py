from misc.misc import Data, format_eng


class Material(Data):
    _ids = set()
    _instances = set()
    _counter = 0

    def __init__(self, id: int, label: str):
        super(Material, self).__init__(id, label)

    def __str__(self):
        retval = []
        retval.append(f'\n$MATERIAL ID = {self.id:n} TYPE = {type(self).__name__:s}')
        retval.append('  $LABEL')
        if ' ' in self.label:
            retval.append(f"    '{self.label:s}'")
        else:
            retval.append(f'    {self.label:s}')
        retval.append('$END MATERIAL')
        return '\n'.join(retval)

    def __del__(self):
        super(Material, self).__del__()


class LinearElastic(Material):
    _counter = 0

    def __init__(self, id: int, label: str, ro: float, E: float, nu: float, a: float):
        self.ro = ro
        self.E = E
        self.nu = nu
        self.G = self.E / (2. * (1. + self.nu))
        self.a = a
        super(LinearElastic, self).__init__(id, label)

    def __del__(self):
        # del self.ro
        # del self.E
        # del self.nu
        # del self.G
        # del self.a
        super(LinearElastic, self).__del__()

    def __repr__(self):
        return f"{type(self).__name__:s}(id={self.id:n}, label='{self.label:s}', " \
               f"ro={format_eng(self.ro):s}, E={format_eng(self.E):s}, " \
               f"nu={format_eng(self.nu):s} a={format_eng(self.a):s})"

    def __str__(self):
        retval = super(LinearElastic, self).__str__().split('\n')
        end = retval[-1]
        retval = retval[:-1]
        retval.append('  $DENSITY')
        retval.append(f'    {format_eng(self.ro):s}')
        retval.append('  $YOUNG')
        retval.append(f'    {format_eng(self.E):s}')
        retval.append('  $POISSON')
        retval.append(f'    {format_eng(self.nu):s}')
        retval.append('  $THERMEXP')
        retval.append(f'    {format_eng(self.a):s}')
        retval.append(end)
        return '\n'.join(retval)
