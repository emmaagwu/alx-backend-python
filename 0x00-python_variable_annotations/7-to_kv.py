#!/usr/bin/env python3
""" This module Converts a key-value pair to a tuple where
    the value is squared.
"""
from typing import Union, Tuple


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """
    Converts a key-value pair to a tuple where the value is squared.

    Args:
        k (str): The key of the pair.
        v (Union[int, float]): The value of the pair.

    Returns:
        Tuple[str, float]: A tuple containing the key and the squared value.
    """
    return (k, (v ** 2))
