#!/usr/bin/env python3
"""Module 17 — Distributed delivery and idempotency.

Standalone educational experiment for the Todo SRE/DevOps Architect handbook.
Run: python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-17.py

Learning flow:
  1. Read the comments and predict the output.
  2. Run the healthy case and inspect the output.
  3. Observe the explicitly labeled simulated failure.
  4. Explain the recovery and production limitations.

This script does not modify the Todo application's code or database.
"""

# Networks can duplicate deliveries; consumers must prevent duplicate effects.
events = ["event-101", "event-102", "event-101"]
processed = set()
notifications = []
for event in events:
    if event in processed:
        print("EXPECTED DUPLICATE: skipping", event)
        continue
    notifications.append(event)
    processed.add(event)
    print("PROCESSED:", event)
print("RECOVERY: unique side effects =", notifications)
print("CAUTION: a process-local set is NOT durable deduplication.")
