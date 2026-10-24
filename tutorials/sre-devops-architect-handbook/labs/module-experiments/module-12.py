#!/usr/bin/env python3
"""Module 12 — Cloud availability zones and failover.

Standalone educational experiment for the Todo SRE/DevOps Architect handbook.
Run: python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-12.py

Learning flow:
  1. Read the comments and predict the output.
  2. Run the healthy case and inspect the output.
  3. Observe the explicitly labeled simulated failure.
  4. Explain the recovery and production limitations.

This script does not modify the Todo application's code or database.
"""

# An availability zone is a failure domain; this is a model, not cloud API usage.
zones = {"zone-a": True, "zone-b": True}

def available_zone():
    return next((name for name, healthy in zones.items() if healthy), None)

print("HEALTHY: route to", available_zone())
zones["zone-a"] = False
print("EXPECTED FAILURE: zone-a unavailable; fail over to", available_zone())
zones["zone-b"] = False
print("OUTAGE: no healthy zones:", available_zone())
zones["zone-b"] = True
print("RECOVERY: route to", available_zone())
print("TRADE-OFF: multi-zone architecture adds cost and data-consistency concerns.")
