from math import floor, log10
from copy import copy,deepcopy


def eng(x, format_spec):
    """
    Return a string representing x in an engineer friendly notation
    """
    def powerise10(x):
        """
        Returns x as a*10**b with 0 <= a < 10
        """
        if x == 0: return 0, 0
        neg = x < 0
        if neg: x = -x
        a = 1.0 * x / 10 ** (floor(log10(x)))
        b = int(floor(log10(x)))
        if neg: a = -a
        return a, b

    def get_format(fmt_spec):
        """
        Convert a format specifier of type 12.3E+2 to %9.3fE%+03d
        """
        # get flags
        flag_val = ''
        i = 0
        while fmt_spec[i] in ['0', '#', '-', ' ', '+']:
            flag_val += fmt_spec[0]
            i += 1
        fmt_spec = fmt_spec[i:]

        if 'e' in fmt_spec:
            exp = 'e'
        else:
            exp = 'E'
        val_fmt = fmt_spec.split(exp)[0]
        exp_fmt = fmt_spec.split(exp)[1]

        i = 0
        flag_exp = ''
        while exp_fmt[i] in ['0', '+']:
            flag_exp += exp_fmt[0]
            i += 1
        exp_fmt = int(exp_fmt[i:]) + 1
        if exp_fmt > 1 and '0' not in flag_exp:
            flag_exp += '0'
        if '+' not in flag_exp:
            flag_exp = '+' + flag_exp

        tmp = '{0:' + flag_exp + str(exp_fmt) + 'n}'
        exp_len = len(str('%' + flag_exp + str(exp_fmt) + 'd') % -1)
        val_fmt = '{0:.1f}'.format(float(val_fmt) - exp_len - 1)
        return '%' + flag_val + val_fmt + 'f' + exp + '%' + flag_exp + str(exp_fmt) + 'd'

    new_format = get_format(format_spec)
    a, b = powerise10(x)
    # if -3 < b < 3:
    #     return "%.4g" % x
    # else:
    #     a = a * 10**(b % 3)
    #     b = b - b % 3
    #     return "%.4gE%s" % (a, b)

    a = a * 10 ** (b % 3)
    b = b - b % 3
    return new_format % (a, b)


def eng_str(value, format_spec):
    y = abs(value)
    exponent = int(log10(y))
    eng_exponent = exponent - exponent % 3
    z = y/10 ** eng_exponent
    sign = '-' if value < 0 else ''
    return sign + str(z) + 'e' + str(eng_exponent)


def format_eng(value, format_spec):
    """
    Return a string representing x in an engineer friendly notation
    """
    def powerise10(x):
        """
        Returns x as a*10**b with 0 <= a < 10
        """
        if x == 0:
            return 0, 0
        neg = x < 0
        if neg:
            x = -x
        mantisa = 1.0 * x / 10 ** (floor(log10(x)))
        exponent = int(floor(log10(x)))
        if neg:
            mantisa = -mantisa
        return mantisa, exponent

    a, b = powerise10(value)
    a = a * 10 ** (b % 3)
    b = b - b % 3
    return format_spec % (a, b)


def format_eng2(value, format_spec):
    exponent = int(log10(abs(value)))
    exponent = exponent - exponent % 3
    mantissa = value / (10 ** exponent)
    return format_spec % (mantissa, exponent)


if __name__ == '__main__':
    print(eng_str(123456789.123456789, '10.3E+2'))
    print(eng_str(-123456789.123456789, '10.3E+2'))
    print(eng_str(-0.00000000123456789, '10.3E+2'))
    print(eng_str(0.00000000123456789, '10.3E+2'))

    print()

    print(eng(123456789.123456789, '12.3E+2'))
    print(eng(-123456789.123456789, '12.3E+2'))
    print(eng(-0.00000000123456789, '12.3E+2'))
    print(eng(0.00000000123456789, '12.3E+2'))

    print()

    print(format_eng(123456789.123456789, '%9.3fE%+03d'))
    print(format_eng(-123456789.123456789, '%9.3fE%+03d'))
    print(format_eng(-0.00000000123456789, '%9.3fE%+03d'))
    print(format_eng(0.00000000123456789, '%9.3fE%+03d'))

    print()

    print(format_eng2(123456789.123456789, '%9.3fE%+03d'))
    print(format_eng2(-123456789.123456789, '%9.3fE%+03d'))
    print(format_eng2(-0.00000000123456789, '%9.3fE%+03d'))
    print(format_eng2(0.00000000123456789, '%9.3fE%+03d'))
