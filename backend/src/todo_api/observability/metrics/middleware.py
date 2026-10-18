import time

from prometheus_client import CollectorRegistry
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from todo_api.observability.metrics.definitions import HttpMetrics, create_http_metrics

_SCRAPE_PATHS = {"/metrics", "/metrics/"}


def _handler(scope: Scope) -> str:
    route = scope.get("route")
    path = getattr(route, "path", None)
    if isinstance(path, str) and path:
        return path
    return "unmatched"


class PrometheusMiddleware:
    """Record HTTP traffic, latency, and in-progress requests."""

    def __init__(self, app: ASGIApp, registry: CollectorRegistry) -> None:
        self.app = app
        self.metrics: HttpMetrics = create_http_metrics(registry)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        path = scope.get("path")
        if isinstance(path, str) and path in _SCRAPE_PATHS:
            await self.app(scope, receive, send)
            return

        method = scope.get("method")
        method_label = method if isinstance(method, str) else "UNKNOWN"
        started = time.perf_counter()
        status_code = "500"
        response_started = False
        failed_before_response = False
        response_finished: float | None = None
        try:
            gauge = self.metrics.in_progress.labels(method=method_label)
            gauge.inc()
        except Exception:
            await self.app(scope, receive, send)
            return

        async def send_wrapper(message: Message) -> None:
            nonlocal response_started, status_code, response_finished
            if message["type"] == "http.response.start":
                response_started = True
                status_code = str(message["status"])
            await send(message)
            if message["type"] == "http.response.body" and not message.get("more_body", False):
                response_finished = time.perf_counter()

        try:
            await self.app(scope, receive, send_wrapper)
        except Exception:
            if not response_started:
                failed_before_response = True
            raise
        finally:
            if response_finished is not None or failed_before_response:
                self._observe(
                    scope,
                    method_label,
                    status_code,
                    (response_finished if response_finished is not None else time.perf_counter())
                    - started,
                )
            try:
                gauge.dec()
            except Exception:
                pass

    def _observe(self, scope: Scope, method: str, status: str, elapsed: float) -> None:
        labels = {"method": method, "handler": _handler(scope), "status": status}
        try:
            self.metrics.requests.labels(**labels).inc()
        except Exception:
            pass
        try:
            self.metrics.duration.labels(**labels).observe(elapsed)
        except Exception:
            pass
