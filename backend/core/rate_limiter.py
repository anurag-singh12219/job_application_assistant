import time
from collections import defaultdict
from threading import Lock
from typing import Dict, List
from fastapi import HTTPException, Request, status


class InMemoryRateLimiter:
    """
    Sliding-window rate limiter by client IP address and endpoint bucket.
    Thread-safe and clears expired timestamps periodically.
    """
    def __init__(self):
        self._requests: Dict[str, List[float]] = defaultdict(list)
        self._lock = Lock()
        self._last_cleanup = time.time()

    def _cleanup_expired(self, current_time: float, window_seconds: float = 300):
        # Run cleanup every 60 seconds
        if current_time - self._last_cleanup > 60:
            keys_to_delete = []
            for key, timestamps in self._requests.items():
                self._requests[key] = [t for t in timestamps if current_time - t < window_seconds]
                if not self._requests[key]:
                    keys_to_delete.append(key)
            for key in keys_to_delete:
                del self._requests[key]
            self._last_cleanup = current_time

    def check_rate_limit(
        self,
        key: str,
        max_requests: int,
        window_seconds: int = 60
    ) -> None:
        current_time = time.time()
        with self._lock:
            self._cleanup_expired(current_time, float(window_seconds))
            timestamps = self._requests[key]
            # Filter timestamps within the current sliding window
            cutoff = current_time - window_seconds
            valid_timestamps = [t for t in timestamps if t > cutoff]
            
            if len(valid_timestamps) >= max_requests:
                oldest_timestamp = valid_timestamps[0]
                retry_after = int(window_seconds - (current_time - oldest_timestamp)) + 1
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Too many requests. Please slow down and try again later.",
                    headers={"Retry-After": str(max(1, retry_after))}
                )
            
            valid_timestamps.append(current_time)
            self._requests[key] = valid_timestamps

    def reset(self):
        """Reset all rate limiter state (useful for test isolation)."""
        with self._lock:
            self._requests.clear()


rate_limiter = InMemoryRateLimiter()


def get_client_ip(request: Request) -> str:
    """Extract client IP, taking into account trusted forward proxy headers if present."""
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        # First IP in the list is the original client
        return forwarded_for.split(",")[0].strip()
    return request.client.host if request.client else "127.0.0.1"


def rate_limit_endpoint(
    endpoint_name: str,
    max_requests: int,
    window_seconds: int = 60
):
    """Dependency helper to enforce rate limiting on specific endpoints."""
    def dependency(request: Request):
        client_ip = get_client_ip(request)
        rate_limit_key = f"{endpoint_name}:{client_ip}"
        rate_limiter.check_rate_limit(rate_limit_key, max_requests, window_seconds)
    return dependency
