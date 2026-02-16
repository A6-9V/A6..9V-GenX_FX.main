"""
EA API Key Authentication Utilities

Provides API key-based authentication for Expert Advisor (EA) HTTP endpoints.
This adds security to EA communication without requiring full JWT implementation.
"""

import functools
import logging
import os
from typing import Optional

from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

from ..config import settings

logger = logging.getLogger(__name__)

# Define API key header schema
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


@functools.lru_cache(maxsize=32)
def _get_keys_cached(key_str: Optional[str], keys_str: Optional[str]) -> frozenset:
    """
    Helper function to parse and cache API keys.
    Returns a frozenset for immutability and O(1) lookup.
    """
    valid_keys = set()

    # Add single EA_API_KEY if configured
    if key_str:
        valid_keys.add(key_str)

    # Add multiple keys from EA_API_KEYS (comma-separated)
    if keys_str:
        keys = [k.strip() for k in keys_str.split(",") if k.strip()]
        valid_keys.update(keys)

    return frozenset(valid_keys)


def get_valid_ea_api_keys() -> set:
    """
    Get the set of valid EA API keys from configuration.
    Uses LRU cache to avoid redundant parsing and set creation.
    In testing mode, also checks os.environ for reactivity.

    Returns:
        set: Set of valid API keys
    """
    # ⚡ Bolt Optimization: Use LRU cache for speed and dynamic environ check.
    # We check os.environ dynamically instead of at module-level to ensure
    # that test fixtures can inject keys even if the module was already imported.
    # Benchmarking shows os.environ.get() is extremely fast (~1.5µs).
    if os.environ.get("TESTING") == "1":
        key_str = os.environ.get("EA_API_KEY") or settings.EA_API_KEY
        keys_str = os.environ.get("EA_API_KEYS") or settings.EA_API_KEYS
    else:
        key_str = settings.EA_API_KEY
        keys_str = settings.EA_API_KEYS

    # We return a set() to the caller to maintain the original return type.
    # Membership check on a set is O(1).
    return set(_get_keys_cached(key_str, keys_str))


async def validate_ea_api_key(api_key: Optional[str] = Security(api_key_header)) -> str:
    """
    Validates the EA API key from the request header.

    Args:
        api_key: The API key from X-API-Key header

    Returns:
        str: The validated API key

    Raises:
        HTTPException: If the API key is missing or invalid
    """
    if not api_key:
        logger.warning("EA API request without API key")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key. Please provide X-API-Key header.",
            headers={"WWW-Authenticate": "ApiKey"},
        )

    valid_keys = get_valid_ea_api_keys()

    # Check if any valid keys are configured
    if not valid_keys:
        logger.error(
            "No EA API keys configured. Set EA_API_KEY or EA_API_KEYS in environment."
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server configuration error. Contact administrator.",
        )

    # Validate the provided key
    if api_key not in valid_keys:
        logger.warning(f"Invalid EA API key attempt (length: {len(api_key)})")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "ApiKey"},
        )

    logger.debug("EA API key validated successfully")
    return api_key


async def validate_ea_api_key_optional(
    api_key: Optional[str] = Security(api_key_header),
) -> Optional[str]:
    """
    Optionally validates the EA API key (doesn't raise if missing).
    Useful for endpoints that support both authenticated and unauthenticated access.

    Args:
        api_key: The API key from X-API-Key header

    Returns:
        Optional[str]: The validated API key or None if not provided

    Raises:
        HTTPException: If the API key is provided but invalid
    """
    if not api_key:
        return None

    valid_keys = get_valid_ea_api_keys()

    if not valid_keys:
        # If no keys configured, allow unauthenticated access
        return None

    if api_key not in valid_keys:
        logger.warning(f"Invalid EA API key attempt (length: {len(api_key)})")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "ApiKey"},
        )

    logger.debug("EA API key validated successfully")
    return api_key
