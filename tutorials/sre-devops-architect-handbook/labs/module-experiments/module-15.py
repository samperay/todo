#!/usr/bin/env python3
"""Module 15 — Capacity, throughput and queue backlog.

Standalone educational experiment for the Todo SRE/DevOps Architect handbook.
Run: python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-15.py

Learning flow:
  1. Read the comments and predict the output.
  2. Run the healthy case and inspect the output.
  3. Observe the explicitly labeled simulated failure.
  4. Explain the recovery and production limitations.

This script does not modify the Todo application's code or database.
"""

# If arrivals exceed processing capacity, backlog grows.
arrival_rate = 12  # jobs/second
worker_rate = 4   # jobs/second per worker
workers = 2
backlog = 0
for second in range(1, 6):
    backlog = max(0, backlog + arrival_rate - worker_rate * workers)
    print(f"SECOND {second}: backlog={backlog}")
print("EXPECTED FAILURE: capacity below demand causes growing backlog")
workers = 4  # Simulate adding capacity.
for second in range(6, 11):
    backlog = max(0, backlog + arrival_rate - worker_rate * workers)
    print(f"RECOVERY SECOND {second}: backlog={backlog}")
print("TRADE-OFF: scaling costs money and may stress downstream dependencies.")
