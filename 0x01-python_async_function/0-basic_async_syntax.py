#!/usr/bin/env python3
""" This module provides an asynchronous
function to wait for a random delay.
"""
import asyncio
import random


async def wait_random(max_delay: int = 10) -> float:
    """
    Wait for a random delay between 0 and `max_delay` seconds.

    Args:
        max_delay (int): The maximum delay in seconds. Default is 10.

    Returns:
        float: The actual delay in seconds.
    """
    delay: float = random.uniform(0, max_delay)
    await asyncio.sleep(delay)
    return delay
