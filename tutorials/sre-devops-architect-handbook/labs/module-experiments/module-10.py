#!/usr/bin/env python3
"""Module 10 — Kubernetes desired-state reconciliation.

Standalone educational experiment for the Todo SRE/DevOps Architect handbook.
Run: python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-10.py

Learning flow:
  1. Read the comments and predict the output.
  2. Run the healthy case and inspect the output.
  3. Observe the explicitly labeled simulated failure.
  4. Explain the recovery and production limitations.

This script does not modify the Todo application's code or database.
"""

# Kubernetes controllers compare desired replicas with observed replicas.
desired_replicas = 3
running_pods = ["pod-a", "pod-b", "pod-c"]
print("HEALTHY: running =", len(running_pods))
running_pods.pop()  # Simulate one pod failing.
print("EXPECTED FAILURE: running =", len(running_pods))
while len(running_pods) < desired_replicas:
    running_pods.append(f"replacement-{len(running_pods) + 1}")
print("RECOVERY: reconciled pods =", running_pods)
print("NOTE: this is a controller simulation, not a Kubernetes cluster test.")
