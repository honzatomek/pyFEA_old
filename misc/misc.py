import math
import logging
import numpy as np


def format_eng(value: float, format_spec: str = ' {0:9.3f}E{1:+03n}'):
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
        logging.exception(e)
        return str('{0:' + str(len(format_eng(1.1, format_spec))) + 'n}').format(np.infty)
    except ValueError as e:
        logging.exception(e)
        return str('{0:' + str(len(format_eng(1.1, format_spec))) + 'n}').format(np.nan)
    except TypeError as e:
        logging.exception(e)
        return str('{0:' + str(len(format_eng(1.1, format_spec))) + 'n}').format(np.nan)
