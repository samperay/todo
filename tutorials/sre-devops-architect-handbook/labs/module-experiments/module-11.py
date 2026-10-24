#!/usr/bin/env python3
"""Module 11 — Readiness and rolling deployment.

Standalone educational experiment for the Todo SRE/DevOps Architect handbook.
Run: python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-11.py

Learning flow:
  1. Read the comments and predict the output.
  2. Run the healthy case and inspect the output.
  3. Observe the explicitly labeled simulated failure.
  4. Explain the recovery and production limitations.

This script does not modify the Todo application's code or database.
"""

# Readiness gates traffic; a running process may still be unready.
pods = [{"name": "old-1", "ready": True}, {"name": "new-1", "ready": False}]

def routable(items):
    return [pod["name"] for pod in items if pod["ready"]]

print("HEALTHY TARGETS:", routable(pods))
print("EXPECTED FAILURE: new pod is running but not ready")
pods[1]["ready"] = True  # Simulate successful startup probe/dependency recovery.
print("RECOVERY: routable targets =", routable(pods))
print("RULE: do not terminate all old ready pods before new pods become ready.")
