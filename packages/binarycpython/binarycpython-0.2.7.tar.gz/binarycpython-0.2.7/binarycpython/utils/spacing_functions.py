"""
Module containing the spacing functions for the binarycpython package. Very under-populated at the moment, but more are likely to come soon

Tasks:
    TODO: add more spacing functions to this module.
"""

from typing import Union
import numpy as np


def const(
    min_bound: Union[int, float], max_bound: Union[int, float], steps: int
) -> list:
    """
    Samples a range linearly. Uses numpy linspace.

    Args:
        min_bound: lower bound of range
        max_bound: upper bound of range
        steps: amount of segments between min_bound and max_bound

    Returns:
        np.linspace(min_bound, max_bound, steps)
    """

    return np.linspace(min_bound, max_bound, steps)
