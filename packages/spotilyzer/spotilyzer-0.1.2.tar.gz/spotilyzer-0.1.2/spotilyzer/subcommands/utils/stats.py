"""
spotilyzer stats utilities
"""

# system imports
import math


def quality(count, total, square_total, cov_level):
    avg = total / count
    variance = square_total / count - avg * avg
    if variance < 0.0:
        return True
    return math.sqrt(variance) / avg < cov_level
