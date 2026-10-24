#!/usr/bin/env python3
"""Module 13 — Metrics, errors and latency.

Standalone educational experiment for the Todo SRE/DevOps Architect handbook.
Run: python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-13.py

Learning flow:
  1. Read the comments and predict the output.
  2. Run the healthy case and inspect the output.
  3. Observe the explicitly labeled simulated failure.
  4. Explain the recovery and production limitations.

This script does not modify the Todo application's code or database.
"""

# Synthetic HTTP observations; no Prometheus server is required.
requests = [("GET", 200, 0.05), ("GET", 200, 0.07), ("POST", 500, 0.20)]
count = len(requests)
errors = sum(500 <= status < 600 for _, status, _ in requests)
latency_sum = sum(seconds for _, _, seconds in requests)
print("REQUEST COUNTER:", count)
print("SERVER ERROR COUNTER:", errors)
print("LATENCY HISTOGRAM COUNT:", count)
print("LATENCY HISTOGRAM SUM:", round(latency_sum, 3))
print("EXPECTED FAILURE: one POST returned HTTP 500")
print("RECOVERY: inspect traces/logs and verify metrics return to baseline.")
print("CAUTION: a missing scrape is unknown data, not zero traffic.")
