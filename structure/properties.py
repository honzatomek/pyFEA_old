from misc.misc import Data, format_eng


class Property(Data):
    _ids = set()
    _instances = set()
    _counter = 0

    def __init__(self, id: int, label: str):
        super(Property, self).__init__(id, label)

    def __del__(self):
        super(Property, self).__del__()

    def __str__(self):
        message = [f'$PROPERTY ID = {self.id:n} TYPE = {type(self).__name__:s}']
        if self.label is not None:
            if ' ' in self.label:
                message.extend(['  $LABEL', f"    '{self.label}'"])
            else:
                message.extend(['  $LABEL', f'    {self.label}'])

        message.append('$END PROPERY')
        return '\n'.join(message)


class CrossSectionBeam2D(Property):
    _counter = 0

    def __init__(self, id: int, label: str, A: float, Iyy: float,
                 Wyy: float, Ash: float, nsm: float):
        self.A = A
        self.Iyy = Iyy
        self.Wyy = Wyy
        self.Ash = Ash
        self.nsm = nsm
        super(CrossSectionBeam2D, self).__init__(id, label)

    def __del__(self):
        # del self.A
        # del self.Iyy
        # del self.Wyy
        # del self.Ash
        # del self.nsm
        super(CrossSectionBeam2D, self).__del__()

    def __str__(self):
        message = super(CrossSectionBeam2D, self).__str__().split('\n')
        end = message[-1]
        message = message[:-1]
        message.extend(['  $GEOMETRY', f'    {format_eng(self.A):s} {format_eng(self.Iyy):s}'
                                       f' {format_eng(self.Wyy):s} {format_eng(self.Ash):s}'])
        message.extend(['  $MASS', f'    {format_eng(self.nsm):s}'])
        message.append(end)
        return '\n' + '\n'.join(message)

    def __repr__(self):
        message = f"{type(self).__name__:s}(id={self.id:n}, label='{self.label:s}'" \
                  f", A={format_eng(self.A):s}" \
                  f", Iyy={format_eng(self.Iyy):s}" \
                  f", Wyy={format_eng(self.Wyy):s}" \
                  f", Ash={format_eng(self.Ash):s}" \
                  f", nsm={format_eng(self.nsm):s})"
        return message