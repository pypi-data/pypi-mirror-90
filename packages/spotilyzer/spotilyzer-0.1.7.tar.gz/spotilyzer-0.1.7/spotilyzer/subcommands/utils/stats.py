"""
spotilyzer stats utilities
"""

# system imports
import math


def quality(count, total, square_total, cov_level):
    """
    Determine if variance is within an acceptable level.
    :param count: population count
    :param total: value total
    :param square_total: total of value squares
    :param cov_level: acceptable coefficient of variation
    :return: True if coefficient of variation is within acceptable limit
    """
    avg = total / count
    variance = square_total / count - avg * avg
    if variance < 0.0:
        return True
    return math.sqrt(variance) / avg < cov_level
