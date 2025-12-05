"""Server-side caching for API queries."""

from cachetools import TTLCache
from functools import wraps
import hashlib
import json

from config import FIRM_CACHE_HOURS, FILING_CACHE_HOURS

# Cache instances with TTL in seconds
_firm_cache = TTLCache(maxsize=500, ttl=FIRM_CACHE_HOURS * 3600)
_filing_cache = TTLCache(maxsize=200, ttl=FILING_CACHE_HOURS * 3600)
_adv_cache = TTLCache(maxsize=200, ttl=FIRM_CACHE_HOURS * 3600)
_rss_cache = TTLCache(maxsize=50, ttl=1800)  # 30 min for RSS
_s1_cache = TTLCache(maxsize=200, ttl=FIRM_CACHE_HOURS * 3600)
_company_info_cache = TTLCache(maxsize=1000, ttl=FIRM_CACHE_HOURS * 3600)


def _make_key(*args, **kwargs) -> str:
    """Create a hashable cache key from arguments."""
    key_data = json.dumps({"args": args, "kwargs": kwargs}, sort_keys=True, default=str)
    return hashlib.md5(key_data.encode()).hexdigest()


def cached(cache: TTLCache):
    """Decorator to cache function results."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = f"{func.__name__}:{_make_key(*args, **kwargs)}"
            if key in cache:
                return cache[key]
            result = func(*args, **kwargs)
            cache[key] = result
            return result
        return wrapper
    return decorator


# Export caches for use in services
firm_cache = cached(_firm_cache)
filing_cache = cached(_filing_cache)
adv_cache = cached(_adv_cache)
rss_cache = cached(_rss_cache)
s1_cache = cached(_s1_cache)
company_info_cache = cached(_company_info_cache)


def clear_all_caches():
    """Clear all caches (useful for debugging/testing)."""
    _firm_cache.clear()
    _filing_cache.clear()
    _adv_cache.clear()
    _rss_cache.clear()
    _s1_cache.clear()
    _company_info_cache.clear()


def get_cache_stats() -> dict:
    """Get current cache statistics."""
    return {
        "firm_cache": {"size": len(_firm_cache), "maxsize": _firm_cache.maxsize},
        "filing_cache": {"size": len(_filing_cache), "maxsize": _filing_cache.maxsize},
        "adv_cache": {"size": len(_adv_cache), "maxsize": _adv_cache.maxsize},
        "rss_cache": {"size": len(_rss_cache), "maxsize": _rss_cache.maxsize},
        "s1_cache": {"size": len(_s1_cache), "maxsize": _s1_cache.maxsize},
        "company_info_cache": {"size": len(_company_info_cache), "maxsize": _company_info_cache.maxsize},
    }

