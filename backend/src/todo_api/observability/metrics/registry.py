from prometheus_client import CollectorRegistry


def create_registry() -> CollectorRegistry:
    """Return a registry owned by one application instance."""
    return CollectorRegistry()
