#!/usr/bin/env python3
"""Module 02 — Timeouts, retries and idempotency.

Standalone educational experiment for the Todo SRE/DevOps Architect handbook.
Run: python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-02.py

Learning flow:
  1. Read the comments and predict the output.
  2. Run the healthy case and inspect the output.
  3. Observe the explicitly labeled simulated failure.
  4. Explain the recovery and production limitations.

This script does not modify the Todo application's code or database.
"""

import time

# A transient failure can be retried. A permanent failure should not be retried forever.
attempts = 0

def flaky_service():
    global attempts
    attempts += 1
    if attempts < 3:
        raise ConnectionError("temporary dependency outage")
    return "Todo notification accepted"

for attempt in range(1, 5):
    try:
        print("SUCCESS:", flaky_service(), "on attempt", attempt)
        break
    except ConnectionError as error:
        print("EXPECTED FAILURE:", error)
        if attempt == 4:
            raise
        delay = 0.05 * (2 ** (attempt - 1))  # Small exponential backoff for demo.
        print("RETRY after", round(delay, 3), "seconds")
        time.sleep(delay)
print("TRADE-OFF: retrying non-idempotent writes may create duplicates.")
