#!/usr/bin/env python3
"""Module 01 — HTTP requests and dependency failures.

Standalone educational experiment for the Todo SRE/DevOps Architect handbook.
Run: python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-01.py

Learning flow:
  1. Read the comments and predict the output.
  2. Run the healthy case and inspect the output.
  3. Observe the explicitly labeled simulated failure.
  4. Explain the recovery and production limitations.

This script does not modify the Todo application's code or database.
"""

from urllib.request import urlopen
from urllib.error import HTTPError, URLError

# A reachable API can return 401: that is an authentication response, not an outage.
for port in (5173, 8000):
    url = f"http://127.0.0.1:{port}/api/v1/todos"
    try:
        with urlopen(url, timeout=2) as response:
            print(f"HEALTHY: {url} returned HTTP {response.status}")
    except HTTPError as error:
        print(f"REACHABLE: {url} returned HTTP {error.code}")
    except (URLError, TimeoutError) as error:
        print(f"UNREACHABLE: {url}: {type(error).__name__}")

# Failure: a deliberately unused local port, without touching Todo.
try:
    urlopen("http://127.0.0.1:65534/", timeout=1)
except (URLError, TimeoutError) as error:
    print("EXPECTED FAILURE: dependency unavailable:", type(error).__name__)
print("RECOVERY: start the missing local service, then rerun this script.")
