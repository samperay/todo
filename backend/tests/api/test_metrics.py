import asyncio
import socket
import threading
from collections import Counter
from collections.abc import Iterator
from unittest.mock import Mock
from uuid import uuid4

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient, AsyncHTTPTransport, HTTPTransport
from prometheus_client import Histogram
from prometheus_client.parser import text_string_to_metric_families
from prometheus_client.samples import Sample
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from tests.api_helpers import auth, create_person
from todo_api.core.config import Settings
from todo_api.main import create_app
from todo_api.observability.metrics.middleware import PrometheusMiddleware
from todo_api.repositories.todo_repository import SqlAlchemyTodoRepository
from todo_api.repositories.user_repository import SqlAlchemyUserRepository

EXPOSITION_TYPE = "text/plain; version=0.0.4; charset=utf-8"


def samples(body: str, name: str) -> list[Sample]:
    return [
        sample
        for family in text_string_to_metric_families(body)
        for sample in family.samples
        if sample.name == name
    ]


def values(body: str, name: str) -> dict[tuple[tuple[str, str], ...], float]:
    return {tuple(sorted(sample.labels.items())): sample.value for sample in samples(body, name)}


def sample_value(body: str, name: str, labels: dict[str, str]) -> float:
    return values(body, name).get(tuple(sorted(labels.items())), 0.0)


def middleware(app: FastAPI) -> PrometheusMiddleware:
    current = app.middleware_stack
    while not isinstance(current, PrometheusMiddleware):
        current = current.app
    return current


@pytest.fixture
def forbid_metrics_dependencies(
    monkeypatch: pytest.MonkeyPatch, client: AsyncClient
) -> Iterator[list[str]]:
    calls: list[str] = []

    def reject_session(*_args: object, **_kwargs: object) -> None:
        calls.append("session")
        raise AssertionError("GET /metrics opened a database session")

    def reject_user(self: object, *_args: object, **_kwargs: object) -> None:
        calls.append("user-repository")
        raise AssertionError("GET /metrics constructed a user repository")

    def reject_todo(self: object, *_args: object, **_kwargs: object) -> None:
        calls.append("todo-repository")
        raise AssertionError("GET /metrics constructed a todo repository")

    def reject_network(*_args: object, **_kwargs: object) -> None:
        calls.append("network")
        raise AssertionError("GET /metrics opened a network connection")

    monkeypatch.setattr(client.app_under_test.state, "session_factory", reject_session)
    monkeypatch.setattr(SqlAlchemyUserRepository, "__init__", reject_user)
    monkeypatch.setattr(SqlAlchemyTodoRepository, "__init__", reject_todo)
    monkeypatch.setattr(AsyncEngine, "connect", reject_session)
    monkeypatch.setattr(AsyncSession, "execute", reject_session)
    monkeypatch.setattr(AsyncHTTPTransport, "handle_async_request", reject_network)
    monkeypatch.setattr(HTTPTransport, "handle_request", reject_network)
    monkeypatch.setattr(socket, "create_connection", reject_network)
    monkeypatch.setattr(socket.socket, "connect", reject_network)
    monkeypatch.setattr(socket.socket, "connect_ex", reject_network)
    yield calls


async def test_metrics_snapshot_is_prometheus_text_without_dependencies(
    client: AsyncClient,
    forbid_metrics_dependencies: list[str],
) -> None:
    response = await client.get("/metrics")

    assert response.status_code == 200
    assert response.headers["content-type"] == EXPOSITION_TYPE
    body = response.text
    assert "# TYPE http_requests_total counter" in body
    assert "# TYPE http_request_duration_seconds histogram" in body
    assert "# TYPE http_requests_in_progress gauge" in body
    assert "http_requests_total{" not in body
    assert forbid_metrics_dependencies == []


async def test_existing_user_call_is_unchanged_and_scrapes_are_excluded(
    client: AsyncClient,
) -> None:
    created = await client.post("/api/v1/users")
    assert created.status_code == 201
    body = created.json()
    assert set(body) == {"id", "token"}

    first = await client.get("/metrics")
    second = await client.get("/metrics")
    assert first.status_code == 200
    assert second.content == first.content
    assert all(
        sample.labels["handler"] not in {"/metrics", "/metrics/"}
        for sample in samples(second.text, "http_requests_total")
    )
    assert body["token"] not in second.text
    assert body["id"] not in second.text


async def test_scrape_rendering_runs_off_event_loop(monkeypatch: pytest.MonkeyPatch) -> None:
    from todo_api.observability.metrics import endpoint

    original = endpoint.generate_latest
    event_loop_thread = threading.get_ident()
    rendering_threads: list[int] = []

    def render(registry):
        rendering_threads.append(threading.get_ident())
        return original(registry)

    monkeypatch.setattr(endpoint, "generate_latest", render)
    # No lifespan or session factory: a scrape must work without database initialization.
    app = create_app(Settings())
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as api:
        first = await api.get("/metrics")
        second = await api.get("/metrics")
    assert first.status_code == second.status_code == 200
    assert first.content == second.content
    assert rendering_threads and all(t != event_loop_thread for t in rendering_threads)
    other = create_app(Settings())
    assert app.state.metrics_registry is not other.state.metrics_registry
    assert not samples(first.text, "http_requests_total")


async def test_exact_hundred_request_mix_and_private_labels(client: AsyncClient) -> None:
    app = client.app_under_test

    @app.get("/test-failure")
    async def fail() -> None:
        raise RuntimeError("test-only failure")

    user_id, token = await create_person(client)
    title, description = "private-title-metrics", "private-description-metrics"
    todo_ids = []
    for _ in range(2):
        response = await client.post(
            "/api/v1/todos",
            headers=auth(token),
            json={"title": title, "description": description},
        )
        assert response.status_code == 201
        todo_ids.append(response.json()["id"])
    before = await client.get("/metrics")
    requests = (
        [
            (f"/api/v1/todos/{todo_ids[i % 2]}", auth(token), 200, "/api/v1/todos/{todo_id}")
            for i in range(80)
        ]
        + [("/api/v1/todos", {}, 401, "/api/v1/todos") for _ in range(5)]
        + [(f"/missing-{uuid4()}", {}, 404, "unmatched") for _ in range(5)]
        + [
            ("/api/v1/todos/not-a-uuid", auth(token), 422, "/api/v1/todos/{todo_id}")
            for _ in range(5)
        ]
        + [("/test-failure", {}, 500, "/test-failure") for _ in range(5)]
    )
    expected = Counter(("GET", handler, str(status)) for _, _, status, handler in requests)
    async with AsyncClient(
        transport=ASGITransport(app=app, raise_app_exceptions=False), base_url="http://test"
    ) as api:
        responses = await asyncio.gather(*(api.get(path, headers=h) for path, h, _, _ in requests))
    assert [r.status_code for r in responses] == [r[2] for r in requests]
    after = await client.get("/metrics")
    initial = values(before.text, "http_requests_total")
    final = values(after.text, "http_requests_total")
    delta = {labels: value - initial.get(labels, 0) for labels, value in final.items()}
    assert {labels: value for labels, value in delta.items() if value} == {
        tuple(sorted(zip(("method", "handler", "status"), labels, strict=True))): count
        for labels, count in expected.items()
    }
    assert sum(expected.values()) == 100
    assert sum(n for (_, _, status), n in expected.items() if 400 <= int(status) < 500) == 15
    assert sum(n for (_, _, status), n in expected.items() if 500 <= int(status) < 600) == 5
    for private in [title, description, token, user_id, *todo_ids, "not-a-uuid"]:
        assert private not in after.text


@pytest.mark.parametrize("failure", ["counter", "gauge_labels", "gauge_increment"])
async def test_recording_failure_preserves_todo_response(
    client: AsyncClient,
    monkeypatch: pytest.MonkeyPatch,
    failure: str,
) -> None:
    _, token = await create_person(client)
    response = await client.post("/api/v1/todos", headers=auth(token), json={"title": "test"})
    todo = response.json()
    instrument = middleware(client.app_under_test)
    broken = Mock(side_effect=RuntimeError("recording unavailable"))
    if failure == "counter":
        monkeypatch.setattr(
            instrument.metrics.requests.labels(
                method="GET", handler="/api/v1/todos/{todo_id}", status="200"
            ),
            "inc",
            broken,
        )
    elif failure == "gauge_labels":
        monkeypatch.setattr(instrument.metrics.in_progress, "labels", broken)
    else:
        monkeypatch.setattr(instrument.metrics.in_progress.labels(method="GET"), "inc", broken)
    result = await client.get(f"/api/v1/todos/{todo['id']}", headers=auth(token))
    assert result.status_code == 200
    assert result.json() == todo
    broken.assert_called_once()


async def test_histogram_matches_completions_and_default_buckets(client: AsyncClient) -> None:
    app = client.app_under_test

    @app.get("/latency-failure")
    async def fail() -> None:
        raise RuntimeError("test-only failure")

    _, token = await create_person(client)
    await client.get("/api/v1/todos", headers=auth(token))
    await client.get("/api/v1/todos")
    async with AsyncClient(
        transport=ASGITransport(app=app, raise_app_exceptions=False), base_url="http://test"
    ) as api:
        response = await api.get("/latency-failure")
        assert response.status_code == 500
    snapshot = await client.get("/metrics")
    assert values(snapshot.text, "http_request_duration_seconds_count") == values(
        snapshot.text, "http_requests_total"
    )
    for count in samples(snapshot.text, "http_request_duration_seconds_count"):
        buckets = [
            s
            for s in samples(snapshot.text, "http_request_duration_seconds_bucket")
            if {k: v for k, v in s.labels.items() if k != "le"} == count.labels
        ]
        assert {float(s.labels["le"]) for s in buckets} == set(Histogram.DEFAULT_BUCKETS)
        assert next(s.value for s in buckets if s.labels["le"] == "+Inf") == count.value
        assert sample_value(snapshot.text, "http_request_duration_seconds_sum", count.labels) >= 0
    slash = await client.get("/metrics/", follow_redirects=True)
    repeated = await client.get("/metrics")
    assert slash.content == repeated.content == snapshot.content


async def test_counter_failure_does_not_skip_latency_or_leave_active_request(
    client: AsyncClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _, token = await create_person(client)
    instrument = middleware(client.app_under_test)
    labels = {"method": "GET", "handler": "/api/v1/todos", "status": "200"}
    monkeypatch.setattr(
        instrument.metrics.requests.labels(**labels),
        "inc",
        Mock(side_effect=RuntimeError("counter unavailable")),
    )
    response = await client.get("/api/v1/todos", headers=auth(token))
    assert response.status_code == 200
    assert response.json() == []
    snapshot = await client.get("/metrics")
    assert sample_value(snapshot.text, "http_request_duration_seconds_count", labels) == 1
    assert sample_value(snapshot.text, "http_requests_in_progress", {"method": "GET"}) == 0


async def test_latency_stops_when_response_finishes(
    client: AsyncClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from types import SimpleNamespace

    from starlette.background import BackgroundTask
    from starlette.responses import Response

    import todo_api.observability.metrics.middleware as instrumentation

    clock = [10.0]
    monkeypatch.setattr(instrumentation, "time", SimpleNamespace(perf_counter=lambda: clock[0]))

    async def background() -> None:
        clock[0] = 100.0

    @client.app_under_test.get("/response-time")
    async def timed() -> Response:
        clock[0] = 12.0
        return Response(content=b"done", background=BackgroundTask(background))

    response = await client.get("/response-time")
    assert response.content == b"done"
    snapshot = await client.get("/metrics")
    assert (
        sample_value(
            snapshot.text,
            "http_request_duration_seconds_sum",
            {
                "method": "GET",
                "handler": "/response-time",
                "status": "200",
            },
        )
        == 2.0
    )


@pytest.mark.parametrize("outcome", ["success", "failure", "cancelled"])
async def test_twenty_active_requests_are_released(client: AsyncClient, outcome: str) -> None:
    app = client.app_under_test
    entered = 0
    ready, release = asyncio.Event(), asyncio.Event()

    @app.get("/held-open")
    async def held() -> None:
        nonlocal entered
        entered += 1
        if entered == 20:
            ready.set()
        await release.wait()
        if outcome == "failure":
            raise RuntimeError("test-only failure")

    before = await client.get("/metrics")
    baseline = sample_value(before.text, "http_requests_in_progress", {"method": "GET"})
    async with AsyncClient(
        transport=ASGITransport(app=app, raise_app_exceptions=False), base_url="http://test"
    ) as api:
        tasks = [asyncio.create_task(api.get("/held-open")) for _ in range(20)]
        try:
            await asyncio.wait_for(ready.wait(), timeout=5)
            active = await client.get("/metrics")
            gauges = samples(active.text, "http_requests_in_progress")
            assert gauges and all(set(s.labels) == {"method"} for s in gauges)
            assert sample_value(active.text, "http_requests_in_progress", {"method": "GET"}) == 20
            assert not samples(active.text, "http_requests_total")
            if outcome == "cancelled":
                for task in tasks:
                    task.cancel()
            else:
                release.set()
            results = await asyncio.gather(*tasks, return_exceptions=True)
        finally:
            release.set()
            for task in tasks:
                if not task.done():
                    task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)
    if outcome == "cancelled":
        assert all(isinstance(r, asyncio.CancelledError) for r in results)
    else:
        assert all(r.status_code == (200 if outcome == "success" else 500) for r in results)
        if outcome == "success":
            assert all(r.json() is None for r in results)
    after = await client.get("/metrics")
    assert sample_value(after.text, "http_requests_in_progress", {"method": "GET"}) == baseline
    if outcome == "cancelled":
        # An abandoned request with no response is no longer active, but has not completed.
        assert not samples(after.text, "http_requests_total")
        assert not samples(after.text, "http_request_duration_seconds_count")
    else:
        labels = {
            "method": "GET",
            "handler": "/held-open",
            "status": "200" if outcome == "success" else "500",
        }
        assert sample_value(after.text, "http_requests_total", labels) == 20
        assert sample_value(after.text, "http_request_duration_seconds_count", labels) == 20


async def test_histogram_failure_preserves_response_and_releases_gauge(
    client: AsyncClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _, token = await create_person(client)
    instrument = middleware(client.app_under_test)
    labels = {"method": "GET", "handler": "/api/v1/todos", "status": "200"}
    broken = Mock(side_effect=RuntimeError("histogram unavailable"))
    monkeypatch.setattr(instrument.metrics.duration.labels(**labels), "observe", broken)
    response = await client.get("/api/v1/todos", headers=auth(token))
    assert response.status_code == 200
    assert response.json() == []
    broken.assert_called_once()
    snapshot = await client.get("/metrics")
    assert sample_value(snapshot.text, "http_requests_in_progress", {"method": "GET"}) == 0
    assert sample_value(snapshot.text, "http_requests_total", labels) == 1


async def test_operational_metric_catalog(client: AsyncClient) -> None:
    _, token = await create_person(client)
    assert (await client.get("/api/v1/todos", headers=auth(token))).status_code == 200
    assert (await client.get("/api/v1/todos")).status_code == 401
    snapshot = await client.get("/metrics")
    for name, kind, help_text in (
        ("http_requests_total", "counter", "Completed HTTP requests."),
        ("http_request_duration_seconds", "histogram", "HTTP request latency in seconds."),
        ("http_requests_in_progress", "gauge", "HTTP requests currently in progress."),
    ):
        assert f"# HELP {name} {help_text}\n" in snapshot.text
        assert f"# TYPE {name} {kind}\n" in snapshot.text
    for name, labels in (
        ("http_requests_total", {"method", "handler", "status"}),
        ("http_request_duration_seconds_bucket", {"method", "handler", "status", "le"}),
        ("http_requests_in_progress", {"method"}),
    ):
        observed = samples(snapshot.text, name)
        assert observed
        assert all(set(s.labels) == labels for s in observed)
