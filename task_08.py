"""Task 08: TTL cache decorator with hit/miss counters."""

import functools
import time

def ttl_cache(seconds):
    if seconds < 0:
        raise ValueError("Cache duration cannot be negative")

    def decorate(function):
        cache = {}
        stats = {"hits": 0, "misses": 0}

        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            try:
                # Sorting keyword pairs makes their order irrelevant.
                key = (args, tuple(sorted(kwargs.items())))
                hash(key)  # Raises TypeError for unhashable arguments.
            except TypeError as exc:
                raise TypeError("ttl_cache arguments must be hashable") from exc

            now = time.monotonic()
            entry = cache.get(key)
            if entry is not None:
                expiry, result = entry
                if now < expiry:
                    stats["hits"] += 1
                    return result

            stats["misses"] += 1
            result = function(*args, **kwargs)
            cache[key] = (now + seconds, result)
            return result

        wrapper.cache_info = lambda: {
            "hits": stats["hits"],
            "misses": stats["misses"],
            "size": len(cache)
        }
        wrapper.cache_clear = cache.clear
        return wrapper
    return decorate


if __name__ == "__main__":
    @ttl_cache(5)
    def add(x, y):
        print("Computing...")
        return x + y

    print(add(x=2, y=3))
    print(add(y=3, x=2))
    print(add.cache_info())
