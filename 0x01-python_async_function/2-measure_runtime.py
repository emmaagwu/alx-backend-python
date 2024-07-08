#!/usr/bash/env python3
"""
Returns the runtime of the function
"""
import time
import importlib
import asyncio


wait_n = importlib.import_module("1-concurrent_coroutines").wait_n


def measure_time(n: int = 0, max_delay: int = 10) -> float:
  """
  Measure the runtime of the wait_n function.

  Args:
    n (int): The number of times to call the wait_n function.
    max_delay (int): The maximum delay value for each call to the wait_n function.

  Returns:
    float: The average runtime of the wait_n function in seconds.
  """
  start_time = time.time()
  asyncio.run(wait_n(n, max_delay))
  return (time.time() - start_time) / n
