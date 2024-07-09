#!/usr/bin/env python3
"""
    Generate a list of 10 numbers using async comprehension.
"""
from typing import List
from importlib import import_module as using


async_generator = using("0-async_generator").async_generator


async def async_comprehension() -> List[float]:
    """
    Generate a list of 10 numbers using async comprehension.

    Returns:
        A list of 10 floating-point numbers.
    """
    return [num async for num in async_generator()]
