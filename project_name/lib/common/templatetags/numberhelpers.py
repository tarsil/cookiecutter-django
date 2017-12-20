from math import floor
from django import template
from django.template.defaultfilters import floatformat

import numbers

register = template.Library()


@register.filter_function
def humanise_number(number, decimals=1):
    digits = number
    suffix = None

    if not isinstance(number, numbers.Number):
        return str(number)

    if number < 1000:
        return str(number)

    number = float(number)

    if number >= 1000:
        digits = floored_division(number, 1000.0, decimals)
        suffix = 'K'
    if number >= 1000000:
        digits = floored_division(number, 1000000.0, decimals)
        suffix = 'M'

    return "{:.{precision}f}{suffix}+".format(digits, precision=decimals, suffix=suffix)


def floored_division(numerator, divisor, digits):
    val = (numerator / divisor) * 10 ** digits
    return floor(val) / 10 ** digits


@register.filter
def percent(value, decimal_places=0):
    if value is None:
        return None
    try:
        value = float(value)
    except ValueError:
        return None
    return floatformat(value * 100.0, decimal_places) + '%'
