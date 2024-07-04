#!/usr/bin/env python3
"""
This module provides a function to calculate the sum of all elements in a list.
"""
from typing import List


def sum_list(input_list: List[float]) -> float:
    """
    Calculate the sum of all elements in a list.

    Args:
        input_list (List[float]): A list of floating-point numbers.

    Returns:
        float: The sum of all elements in the list.
    """
    return sum(input_list)
