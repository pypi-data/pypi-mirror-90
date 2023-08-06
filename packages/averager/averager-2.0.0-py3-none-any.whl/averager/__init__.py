"""Simple utilities for calculating averages"""

from __future__ import division

__version__ = "2.0.0"


def average(values):
    """Calculates an unweighted average

    Args:
        values (Iterable): The values to find the average of

    Returns:
        The average of the inputs

    Example:
        >>> average([1, 2, 3])
        2
    """

    res = sum(values) / len(values)

    if res == int(res):
        return int(res)

    return res


def weighted_average(values):
    """Calculates an weighted average

    Args:
        values (Iterable): The values to find the average as an iterable of
            ``(value, weight)`` pairs

    Returns:
        The weighted average of the inputs

    Example:
        >>> weighted_average([(1, 2), (2, 3)])
        1.6
    """

    if any(weight < 0 for _, weight in values):
        raise ValueError("Weights cannot be less than zero")

    dividend, divisor = 0, 0

    for value, weight in values:
        dividend += value * weight
        divisor += weight

    res = dividend / divisor

    if res == int(res):
        return int(res)

    return res
