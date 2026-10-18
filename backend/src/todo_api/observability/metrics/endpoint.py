import asyncio

from fastapi import FastAPI, Request
from prometheus_client import CONTENT_TYPE_PLAIN_0_0_4, CollectorRegistry, generate_latest
from starlette.responses import Response


async def metrics_response(registry: CollectorRegistry) -> Response:
    """Render the Prometheus 0.0.4 text snapshot for one application registry."""
    payload = await asyncio.to_thread(generate_latest, registry)
    return Response(content=payload, media_type=CONTENT_TYPE_PLAIN_0_0_4)


def register_metrics_endpoint(app: FastAPI) -> None:
    """Wire the unauthenticated protocol endpoint without domain dependencies."""

    @app.get("/metrics", response_model=None)
    async def scrape_metrics(request: Request) -> Response:
        return await metrics_response(request.app.state.metrics_registry)
