"""
Retry Handler Utility for GenX FX Trading Platform
Provides decorators for automatic retries of network and trading operations.
"""

import asyncio
import functools
import logging
import random
from typing import Any, Callable, Optional, Tuple, Type

logger = logging.getLogger(__name__)

def retry_async(
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    max_retries: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
    jitter: bool = True,
):
    """
    A decorator for retrying asynchronous functions.

    Args:
        exceptions: A tuple of exceptions to catch and retry on.
        max_retries: The maximum number of retry attempts.
        initial_delay: The initial delay between retries in seconds.
        backoff_factor: The multiplier for the delay after each retry.
        jitter: Whether to add random jitter to the delay.
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            delay = initial_delay
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt == max_retries:
                        logger.error(
                            f"Max retries ({max_retries}) reached for {func.__name__}. "
                            f"Last error: {e}"
                        )
                        raise

                    wait_time = delay
                    if jitter:
                        wait_time *= (0.5 + random.random())

                    logger.warning(
                        f"Attempt {attempt + 1}/{max_retries + 1} failed for {func.__name__}: {e}. "
                        f"Retrying in {wait_time:.2f} seconds..."
                    )

                    await asyncio.sleep(wait_time)
                    delay *= backoff_factor

        return wrapper
    return decorator

def mt5_retry(max_retries: int = 5, initial_delay: float = 0.5):
    """
    Specific retry decorator for MT5 operations that might fail due to connection issues.
    """
    # Import here to avoid hard dependency if not used
    try:
        import MetaTrader5 as mt5
        mt5_exceptions = (Exception,) # MT5 doesn't have specific exception classes in the python lib
    except ImportError:
        mt5_exceptions = (Exception,)

    return retry_async(
        exceptions=mt5_exceptions,
        max_retries=max_retries,
        initial_delay=initial_delay,
        backoff_factor=1.5,
        jitter=True
    )
