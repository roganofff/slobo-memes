import time
from functools import wraps
from typing import Any, Callable, Coroutine

from prometheus_client import Counter, Histogram
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

BUCKETS = [
    0.2,
    0.4,
    0.6,
    0.8,
    1.0,
    1.2,
    1.4,
    1.6,
    1.8,
    2.0,
    float('+inf'),
]

LATENCY = Histogram('latency_seconds_handler', 'считает задержку', labelnames=['handler'], buckets=BUCKETS)


def track_latency(
    method_name: str,
) -> Callable[[Callable[..., Coroutine[Any, Any, Any]]], Callable[..., Coroutine[Any, Any, Any]]]:
    def decorator(func: Callable[..., Coroutine[Any, Any, Any]]) -> Callable[..., Coroutine[Any, Any, Any]]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = time.monotonic()
            try:
                return await func(*args, **kwargs)
            finally:
                elapsed_time = time.monotonic() - start_time
                LATENCY.labels(handler=method_name).observe(elapsed_time)

        return wrapper

    return decorator


REQUESTS_TOTAL = Counter('http_request_total', 'Количество запросов на сервер', labelnames=['handler', 'status_code'])


class RPSTrackerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        try:
            response: Response = await call_next(request)
            status_code = response.status_code
        except Exception:
            status_code = 500
            raise
        finally:
            REQUESTS_TOTAL.labels(handler=request.url.path, status_code=str(status_code)).inc()

        return response


SEND_MESSAGE = Counter(
    'bot_messages_sent',
    'Отправленные сообщения в очередь',
)