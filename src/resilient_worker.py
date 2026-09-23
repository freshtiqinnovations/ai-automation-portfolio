import time
from collections.abc import Callable
from dataclasses import dataclass

@dataclass(frozen=True)
class RetryPolicy:
    attempts: int = 4
    base_delay_seconds: float = 0.25
    max_delay_seconds: float = 2.0

class DeliveryError(RuntimeError):
    pass

def run_with_retry(
    operation: Callable[[], object],
    *,
    policy: RetryPolicy = RetryPolicy(),
    sleep: Callable[[float], None] = time.sleep,
) -> object:
    """Run an operation with bounded exponential backoff."""
    last_error: Exception | None = None

    for attempt in range(1, policy.attempts + 1):
        try:
            return operation()
        except Exception as exc:  # boundary wrapper for external providers
            last_error = exc
            if attempt == policy.attempts:
                break
            delay = min(
                policy.base_delay_seconds * (2 ** (attempt - 1)),
                policy.max_delay_seconds,
            )
            sleep(delay)

    raise DeliveryError(
        f"operation failed after {policy.attempts} attempts"
    ) from last_error
