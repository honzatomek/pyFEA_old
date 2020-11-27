import unittest
import os
from configparser import ConfigParser
import logging
import numpy as np

from basic import beam2d


class Verification01(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(Verification01, self).__init__(*args, **kwargs)
        self.path = os.path.join(os.path.dirname(__file__), 'verification/01-linear_statics-simple_cantilever')
        self.cfg = ConfigParser()
        self.cfg.read(os.path.join(self.path, 'g.ini'))
        self.ndu, self.r, self.ue, self.se = beam2d.beam2d(self.path)

    def template(self):
        sections = [s.strip() for s in self.cfg['DEFAULT']['verification'].split(',')]
        for section in sections:
            t = self.cfg[section]['type']
            n = int(self.cfg[section]['node'])
            d = int(self.cfg[section]['direction'])
            verification = float(self.cfg[section]['value'])
            if t == 'displacement':
                value = self.ndu[n - 1][d - 1]
            elif t == 'reaction':
                idx = np.where(self.r[:, 0] == n)[0][0]
                tmp = self.r[idx]
                value = self.r[idx][d]
            else:
                raise NotImplemented(f'Result type test {t} is not yet implmented')
            self.assertAlmostEqual(verification, value, delta=abs(verification * 0.05))

    def test_displacement(self):
        section = 'DISPLACEMENT'
        t = self.cfg[section]['type']
        n = int(self.cfg[section]['node'])
        d = int(self.cfg[section]['direction'])
        verification = float(self.cfg[section]['value'])
        if t == 'displacement':
            value = self.ndu[n - 1][d - 1]
        elif t == 'reaction':
            idx = np.where(self.r[:, 0] == n)[0][0]
            tmp = self.r[idx]
            value = self.r[idx][d]
        else:
            raise NotImplemented(f'Result type test {t} is not yet implmented')
        self.assertAlmostEqual(verification, value, msg=f'precison = {abs(1 - verification / value)}',
                               delta=abs(verification * 0.05))

    def test_reaction(self):
        section = 'REACTION'
        t = self.cfg[section]['type']
        n = int(self.cfg[section]['node'])
        d = int(self.cfg[section]['direction'])
        verification = float(self.cfg[section]['value'])
        if t == 'displacement':
            value = self.ndu[n - 1][d - 1]
        elif t == 'reaction':
            idx = np.where(self.r[:, 0] == n)[0][0]
            tmp = self.r[idx]
            value = self.r[idx][d]
        else:
            raise NotImplemented(f'Result type test {t} is not yet implmented')
        self.assertAlmostEqual(verification, value, delta=abs(verification * 0.05))

    def test_moment(self):
        section = 'MOMENT'
        t = self.cfg[section]['type']
        n = int(self.cfg[section]['node'])
        d = int(self.cfg[section]['direction'])
        verification = float(self.cfg[section]['value'])
        if t == 'displacement':
            value = self.ndu[n - 1][d - 1]
        elif t == 'reaction':
            idx = np.where(self.r[:, 0] == n)[0][0]
            tmp = self.r[idx]
            value = self.r[idx][d]
        else:
            raise NotImplemented(f'Result type test {t} is not yet implmented')
        self.assertAlmostEqual(verification, value, delta=abs(verification * 0.05))


if __name__ == '__main__':
    logger = logging.getLogger()
    logger.disabled = True
    # logger_handler = logger.handlers[0]
    # logger_handler.setLevel(logging.FATAL)
    unittest.main(verbosity=2)
