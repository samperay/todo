from dataclasses import dataclass

from prometheus_client import CollectorRegistry, Counter, Gauge, Histogram


@dataclass(frozen=True, slots=True)
class HttpMetrics:
    requests: Counter
    duration: Histogram
    in_progress: Gauge


def create_http_metrics(registry: CollectorRegistry) -> HttpMetrics:
    """Declare the three HTTP series on the given registry."""
    return HttpMetrics(
        requests=Counter(
            "http_requests_total",
            "Completed HTTP requests.",
            labelnames=("method", "handler", "status"),
            registry=registry,
        ),
        duration=Histogram(
            "http_request_duration_seconds",
            "HTTP request latency in seconds.",
            labelnames=("method", "handler", "status"),
            registry=registry,
        ),
        in_progress=Gauge(
            "http_requests_in_progress",
            "HTTP requests currently in progress.",
            labelnames=("method",),
            registry=registry,
        ),
    )
