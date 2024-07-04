#!/usr/bin/env python3
"""
This module provides a function for summing a
    mixed list of integers and floats.
"""
from typing import Union


def sum_mixed_list(mxd_lst: Union[int, float]) -> float:
    """
    Calculate the sum of a mixed list of integers and floats.

    Args:
        mxd_lst: A list containing integers and/or floats.

    Returns:
        The sum of the elements in the list.

    """
    return sum(mxd_lst)
