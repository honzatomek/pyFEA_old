from misc.misc import Data, eng, DataSet


class Property(Data):
    _ids = set()
    _instances = set()
    _counter = 0

    def __init__(self, label: str):
        super(Property, self).__init__(label=label)

    def __del__(self):
        super(Property, self).__del__()

    def __str__(self):
        message = list([f'$PROPERTY NAME = {self.label:s} TYPE = {type(self).__name__:s}'])
        message.append('$END PROPERY')
        return '\n'.join(message)


class CrossSectionBeam2D(Property):
    _counter = 0

    def __init__(self, label: str, A: float, I_11: float,
                 W_11: float, Ash1: float, nsm: float):
        self.A = A
        self.I_11 = I_11
        self.W_11 = W_11
        self.Ash1 = Ash1
        self.nsm = nsm
        super(CrossSectionBeam2D, self).__init__(label=label)

    def __del__(self):
        super(CrossSectionBeam2D, self).__del__()

    def __str__(self):
        message = super(CrossSectionBeam2D, self).__str__().split('\n')
        end = message[-1]
        message = message[:-1]
        message.extend(['  $GEOMETRY', f'    {eng(self.A):s} {eng(self.I_11):s}'
                                       f' {eng(self.W_11):s} {eng(self.Ash1):s}'])
        message.extend(['  $MASS', f'    {eng(self.nsm):s}'])
        message.append(end)
        return '\n' + '\n'.join(message)

    def __repr__(self):
        message = f"{type(self).__name__:s}(label='{self.label:s}'" \
                  f", A={eng(self.A):s}" \
                  f", I_11={eng(self.I_11):s}" \
                  f", W_11={eng(self.W_11):s}" \
                  f", Ash={eng(self.Ash1):s}" \
                  f", nsm={eng(self.nsm):s})"
        return message


class Properties(DataSet):
    """
    Class for collection of Property objects
    """
    _type = Property
    _ids = set()
    _instances = set()
    _counter = 0
    _command = 'PROPERTY'
    _last_label_id = 0

    def __init__(self, id: int = None, label: str = None):
        super(Properties, self).__init__(Property, id, label)
