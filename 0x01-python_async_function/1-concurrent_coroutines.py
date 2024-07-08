#!/usr/bin/env python3
"""
This module contains a function for concurrently executing coroutines.
"""
from typing import List
import importlib
import asyncio


wait_random = importlib.import_module('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> List:
    """
    Waits for a random delay multiple times and
        returns a sorted list of the delays.

    Args:
        n (int): The number of times to wait.
        max_delay (int): The maximum delay in seconds.

    Returns:
        List: A sorted list of the delays.
    """
    delay_list = await asyncio.gather(
        *tuple(map(lambda _: wait_random(max_delay), range(n)))
    )
    return sorted(delay_list)
