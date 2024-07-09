#!/usr/bin/env python3
"""Executes async_comprehension 4 times
"""
import asyncio
import time
from importlib import import_module as bring


async_comprehension = bring('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """Executes async_comprehension 4 times and measures the
    total execution time.
    """
    start_time = time.time()
    await asyncio.gather(*(async_comprehension() for _ in range(4)))
    return time.time() - start_time
