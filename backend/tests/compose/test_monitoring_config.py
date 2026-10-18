"""Read the committed Compose, Prometheus, and README files. These tests do not start Docker."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
COMPOSE_PATH = REPO_ROOT / "compose.yaml"
PROMETHEUS_PATH = REPO_ROOT / "deploy" / "prometheus" / "prometheus.yml"
README_PATH = REPO_ROOT / "README.md"

THROUGHPUT_BY_LABELS = "sum by (method, handler, status) (rate(http_requests_total[1m]))"
THROUGHPUT_TOTAL = "sum(rate(http_requests_total[1m]))"
CLIENT_ERROR_RATE = 'sum(rate(http_requests_total{status=~"4.."}[1m]))'
SERVER_ERROR_RATE = 'sum(rate(http_requests_total{status=~"5.."}[1m])) or vector(0)'
LATENCY_BUCKET_RATE = "rate(http_request_duration_seconds_bucket[1m])"

Node = dict[str, Any] | list[Any] | str | int | float | bool | None
Mapping = dict[str, Any]


def test_compose_services_are_only_the_api_and_prometheus() -> None:
    services = _compose()["services"]
    assert set(services) == {"todo-api", "prometheus"}


def test_prometheus_image_is_pinned() -> None:
    prometheus = _compose()["services"]["prometheus"]
    assert prometheus["image"] == "prom/prometheus:v3.13.4"


def test_published_ports_bind_loopback_only() -> None:
    services = _compose()["services"]
    assert _published_ports(services["todo-api"]) == [("127.0.0.1", "8000", "8000")]
    assert _published_ports(services["prometheus"]) == [("127.0.0.1", "9090", "9090")]
    published = _published_ports(services["todo-api"]) + _published_ports(services["prometheus"])
    assert all(host_ip != "0.0.0.0" for host_ip, _, _ in published)


def test_prometheus_scrapes_the_compose_service_every_15_seconds() -> None:
    document = _prometheus()
    assert document["global"]["scrape_interval"] == "15s"
    jobs = document["scrape_configs"]
    assert [job["job_name"] for job in jobs] == ["todo-api"]
    job = jobs[0]
    assert job["metrics_path"] == "/metrics"
    assert job.get("scheme", "http") == "http"
    assert job["scrape_interval"] == "15s"
    targets = [target for group in job["static_configs"] for target in group["targets"]]
    assert targets == ["todo-api:8000"]
    assert all(not target.startswith(("localhost", "127.0.0.1")) for target in targets)


def test_prometheus_config_has_no_rules_or_alerting() -> None:
    document = _prometheus()
    assert "rule_files" not in document
    assert "alerting" not in document


def test_committed_monitoring_files_have_no_secrets_or_todo_contents() -> None:
    for path in (COMPOSE_PATH, PROMETHEUS_PATH):
        text = _read(path).lower()
        for forbidden in ("password", "token", "bearer"):
            assert forbidden not in text
        assert "todo" not in text.replace("todo-api", "")


def test_prometheus_data_is_a_named_volume() -> None:
    compose = _compose()
    mounts = _volume_mounts(compose["services"]["prometheus"])
    data_mounts = [mount for mount in mounts if mount["target"] == "/prometheus"]
    assert data_mounts == [{"source": "prometheus-data", "target": "/prometheus", "type": "volume"}]
    assert "prometheus-data" in compose["volumes"]
    assert all(mount["type"] == "volume" for mount in data_mounts)


def test_readme_documents_throughput_error_and_latency_queries() -> None:
    text = _read(README_PATH)
    assert THROUGHPUT_BY_LABELS in text
    assert THROUGHPUT_TOTAL in text
    assert CLIENT_ERROR_RATE in text
    assert SERVER_ERROR_RATE in text
    compact = _compact(text)
    for quantile in ("0.50", "0.95"):
        expected = _compact(f"histogram_quantile({quantile}, sum by (le) ({LATENCY_BUCKET_RATE}))")
        assert expected in compact


def test_client_error_query_has_no_zero_substitution() -> None:
    """An empty 4xx selector stays empty. Only the 5xx query substitutes the number 0."""
    text = _read(README_PATH)
    assert CLIENT_ERROR_RATE in text
    assert _compact(f"{CLIENT_ERROR_RATE} or vector(0)") not in _compact(text)
    for line in text.splitlines():
        if 'status=~"4.."' in line:
            assert "or vector(0)" not in line


def test_readme_documents_prometheus_volume_persistence() -> None:
    text = _read(README_PATH)
    lowered = text.lower()
    down_without_reset = text.replace("docker compose down -v", "")
    missing = [
        name
        for name, present in (
            ("named volume prometheus-data", "prometheus-data" in text),
            ("volume mounted at /prometheus", "/prometheus" in text),
            (
                "samples survive docker compose restart",
                "docker compose restart" in text and "surviv" in lowered,
            ),
            (
                "samples survive recreation while prometheus-data is retained",
                "recreat" in lowered and "prometheus-data" in text,
            ),
            (
                "docker compose down preserves the named volume",
                "docker compose down" in down_without_reset and "surviv" in lowered,
            ),
            (
                "docker compose down -v removes the named volume",
                "docker compose down -v" in text and ("remov" in lowered or "delet" in lowered),
            ),
        )
        if not present
    ]
    assert missing == [], "README persistence section is missing: " + "; ".join(missing)


def test_readme_documents_that_the_api_database_has_no_volume() -> None:
    lowered = _read(README_PATH).lower()
    missing = [
        name
        for name, present in (
            (
                "todo-api has no persistent SQLite database volume",
                "todo-api" in lowered and "no database volume" in lowered and "sqlite" in lowered,
            ),
        )
        if not present
    ]
    assert missing == [], "README API storage section is missing: " + "; ".join(missing)


PROMTOOL_CHECK = (
    "docker compose run --rm --no-deps --entrypoint promtool prometheus "
    "check config /etc/prometheus/prometheus.yml"
)


def test_readme_documents_promtool_validation() -> None:
    text = _read(README_PATH)
    assert PROMTOOL_CHECK in text


def test_readme_documents_the_verification_procedure() -> None:
    text = _read(README_PATH)
    missing = [
        name
        for name, present in (
            ("baseline POST /api/v1/users", "POST /api/v1/users" in text),
            ("authorized GET /api/v1/todos", "GET /api/v1/todos" in text),
            ("unauthenticated POST /api/v1/todos", "POST /api/v1/todos" in text),
            (
                "wait for both a 2xx and a 4xx http_requests_total series",
                "2xx" in text and "4xx" in text and "http_requests_total" in text,
            ),
            (
                "at least 10 additional requests before the next scrape",
                "at least 10" in text and "next scrape" in text,
            ),
            (
                "a one-sample counter is not a rate",
                "one-sample counter is not a rate" in text,
            ),
        )
        if not present
    ]
    assert missing == [], "README verification procedure is missing: " + "; ".join(missing)


def _compose() -> Mapping:
    loaded = _load(COMPOSE_PATH)
    assert isinstance(loaded, dict)
    return loaded


def _prometheus() -> Mapping:
    loaded = _load(PROMETHEUS_PATH)
    assert isinstance(loaded, dict)
    return loaded


def _load(path: Path) -> Node:
    return parse_yaml(_read(path))


def _compact(text: str) -> str:
    return "".join(text.split())


def _read(path: Path) -> str:
    if not path.is_file():
        pytest.fail(f"{path.relative_to(REPO_ROOT)} is missing")
    return path.read_text(encoding="utf-8")


def _published_ports(service: Mapping) -> list[tuple[str, str, str]]:
    ports: list[tuple[str, str, str]] = []
    for item in service.get("ports") or []:
        if isinstance(item, str):
            host_ip, published, target = item.split(":")
            ports.append((host_ip, published, target))
        else:
            ports.append(
                (
                    str(item.get("host_ip", "0.0.0.0")),
                    str(item["published"]),
                    str(item["target"]),
                )
            )
    return ports


def _volume_mounts(service: Mapping) -> list[dict[str, str]]:
    mounts: list[dict[str, str]] = []
    for item in service.get("volumes") or []:
        if isinstance(item, str):
            source, target = _split_short_volume(item)
            mount_type = "bind" if _is_bind_source(source) else "volume"
        else:
            source = str(item.get("source", ""))
            target = str(item.get("target", ""))
            explicit = item.get("type")
            if explicit:
                mount_type = str(explicit)
            else:
                mount_type = "bind" if _is_bind_source(source) else "volume"
        mounts.append({"source": source, "target": target, "type": mount_type})
    return mounts


def _split_short_volume(spec: str) -> tuple[str, str]:
    source, rest = spec.split(":", 1)
    target = rest.rsplit(":", 1)[0] if rest.endswith((":ro", ":rw")) else rest
    return source, target


def _is_bind_source(source: str) -> bool:
    return source.startswith((".", "/")) or "/" in source


def parse_yaml(text: str) -> Node:
    """Parse the mappings and lists used by the Compose and Prometheus files."""
    lines = _content_lines(text)
    if not lines:
        return None
    value, index = _parse_block(lines, 0)
    if index != len(lines):
        raise ValueError("unexpected trailing YAML content")
    return value


def _content_lines(text: str) -> list[tuple[int, str]]:
    parsed: list[tuple[int, str]] = []
    for raw in text.splitlines():
        stripped = _strip_comment(raw).rstrip()
        if not stripped.strip() or stripped.strip() in {"---", "..."}:
            continue
        indent = len(stripped) - len(stripped.lstrip(" "))
        parsed.append((indent, stripped.strip()))
    return parsed


def _strip_comment(line: str) -> str:
    in_single = False
    in_double = False
    escaped = False
    for index, char in enumerate(line):
        if in_double and escaped:
            escaped = False
            continue
        if char == "\\" and in_double:
            escaped = True
            continue
        if char == "'" and not in_double:
            in_single = not in_single
        elif char == '"' and not in_single:
            in_double = not in_double
        elif char == "#" and not in_single and not in_double:
            return line[:index]
    return line


def _parse_scalar(value: str) -> Node:
    if value in {"", "null", "~", "Null", "NULL"}:
        return None
    if value in {"true", "True", "TRUE"}:
        return True
    if value in {"false", "False", "FALSE"}:
        return False
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    if value.isdigit():
        return int(value)
    return value


def _split_mapping_entry(content: str) -> tuple[str, str] | None:
    if content.startswith(("'", '"', "-")):
        return None
    if content.endswith(":") and ": " not in content:
        key = content[:-1].strip()
        if key and " " not in key:
            return key, ""
        return None
    if ": " not in content:
        return None
    key, value = content.split(": ", 1)
    if not key or " " in key:
        return None
    return key, value.strip()


def _parse_block(lines: list[tuple[int, str]], index: int) -> tuple[Node, int]:
    if lines[index][1].startswith("- "):
        return _parse_list(lines, index, lines[index][0])
    return _parse_map(lines, index, lines[index][0])


def _parse_map(
    lines: list[tuple[int, str]], index: int, indent: int
) -> tuple[dict[str, Node], int]:
    mapping: dict[str, Node] = {}
    while index < len(lines) and lines[index][0] == indent and not lines[index][1].startswith("- "):
        entry = _split_mapping_entry(lines[index][1])
        if entry is None:
            raise ValueError(f"expected a mapping entry: {lines[index][1]}")
        key, raw_value = entry
        index += 1
        if raw_value == "" and index < len(lines) and lines[index][0] > indent:
            value, index = _parse_block(lines, index)
        elif raw_value == "":
            value = None
        else:
            value = _parse_scalar(raw_value)
        mapping[key] = value
    return mapping, index


def _parse_list(lines: list[tuple[int, str]], index: int, indent: int) -> tuple[list[Node], int]:
    items: list[Node] = []
    while index < len(lines) and lines[index][0] == indent and lines[index][1].startswith("- "):
        content = lines[index][1][2:].strip()
        index += 1
        if content == "":
            value, index = _parse_block(lines, index)
            items.append(value)
            continue
        entry = _split_mapping_entry(content)
        if entry is None:
            items.append(_parse_scalar(content))
            continue
        key, raw_value = entry
        item: dict[str, Node] = {}
        if raw_value == "" and index < len(lines) and lines[index][0] > indent:
            item[key], index = _parse_block(lines, index)
        elif raw_value == "":
            item[key] = None
        else:
            item[key] = _parse_scalar(raw_value)
        if index < len(lines) and lines[index][0] > indent and not lines[index][1].startswith("- "):
            extra, index = _parse_map(lines, index, lines[index][0])
            item.update(extra)
        items.append(item)
    return items, index
