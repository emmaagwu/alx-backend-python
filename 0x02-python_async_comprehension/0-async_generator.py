#!/usr/bin/env python3
"""This module contains an async generator
 that generates a sequence of 10 random numbers.
"""
import asyncio
import random
from typing import Generator


async def async_generator() -> Generator[float, None, None]:
    """Async generator function.

    This function generates a sequence of 10 random numbers asynchronously.
    Each number is generated after a delay of 1 second.
    """
    for _ in range(10):
        await asyncio.sleep(1)
        yield random.random() * 10
