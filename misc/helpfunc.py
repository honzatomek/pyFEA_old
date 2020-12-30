import math
import logging
import numpy as np
from functools import wraps
from time import time

from misc.errors import *


logger = logging.getLogger(__name__)
# logger = logging.getLogger()


def eng(value, format_spec: str = ' {0:10.4f}E{1:+03n}', oneline: bool = True):
    """
    Wrapper around format_eng function to process also lists and numpy arrays (max dim for non one line = 2)
    :param value:        float or numpy float value, also list of floats and numpy array of floats
    :param format_spec:  string with format for mantisa and exponent e.g.: ' {0:9.3f}E{1:+03n}'
    :param oneline:      for arrays only, whether feed newline between rows or not, if
                         False, max 2D matrix or array of floats can be used.
    :return:             formatted value as string
    """
    if isinstance(value, float) or isinstance(value, int):
        return format_eng(value, format_spec)
    elif isinstance(value, np.float) or isinstance(value, np.int):
        return format_eng(value, format_spec)
    elif isinstance(value, list) or isinstance(value, np.ndarray):
        # check if max dimension is 2 for oneline = False
        if not oneline:
            try:
                for r in value:
                    if isinstance(r, list) or isinstance(r, np.ndarray):
                        for c in r:
                            assert not isinstance(c, list) or not isinstance(c, np.ndarray)
            except AssertionError:
                message = '"value" attribute of "eng()" function with ' \
                          '"oneline=False" argument can be max 2D matrix' \
                          'or array.'
                logger.error(message)
                raise ValueError(message)
        # recurse through matrix
        retval = []
        for r in value:
            if isinstance(r, list) or isinstance(r, np.ndarray):
                if oneline:
                    retval.append('[' + ', '.join([eng(v, format_spec, oneline) for v in r]) + ']')
                else:
                    retval.append(''.join([eng(v, format_spec, oneline) for v in r]))
            else:
                retval.append(eng(r, format_spec, oneline))
        if oneline:
            retval = '[' + ', '.join(retval) + ']'
            while '  ' in retval:
                retval = retval.replace('  ', ' ')
        else:
            retval = '\n'.join(retval)
        return retval
    else:
        message = 'argument "value" of function eng() must be an instance of float,' \
                  'numpy.float or a list or numpy.ndarray of them.'
        logger.error(message)
        raise ValueError(message)


def format_eng(value: float, format_spec: str = ' {0:10.4f}E{1:+03n}'):
    """
    Formats float value into engineering format with exponent a multiple of 3
    :param value:        float or numpy float value
    :param format_spec:  string with format for mantisa and exponent e.g.: ' {0:9.3f}E{1:+03n}'
    :return:             formated value as string
    """
    try:
        if value == 0.0:
            return format_spec.format(0.0, 0)
        exponent = int(math.log10(abs(value)))
        exponent = exponent - exponent % 3
        mantissa = value / (10 ** exponent)
        return format_spec.format(mantissa, exponent)
    except OverflowError as e:
        logger.exception(e)
        return str('{0:' + str(len(format_eng(1.1, format_spec))) + 'n}').format(np.infty)
    except ValueError as e:
        logger.exception(e)
        return str('{0:' + str(len(format_eng(1.1, format_spec))) + 'n}').format(np.nan)
    except TypeError as e:
        logger.exception(e)
        return str('{0:' + str(len(format_eng(1.1, format_spec))) + 'n}').format(np.nan)


def timer(f):
    @wraps
    def wrap(*args, **kwargs):
        ts = time()
        result = f(*args, **kwargs)
        te = time()
        logging.info(f'{f.__name__} took {te - ts:2.4f} s')
        return result
    return wrap
