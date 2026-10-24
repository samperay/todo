#!/usr/bin/env python3
"""Module 09 — Infrastructure as Code drift.

Standalone educational experiment for the Todo SRE/DevOps Architect handbook.
Run: python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-09.py

Learning flow:
  1. Read the comments and predict the output.
  2. Run the healthy case and inspect the output.
  3. Observe the explicitly labeled simulated failure.
  4. Explain the recovery and production limitations.

This script does not modify the Todo application's code or database.
"""

# Desired configuration is declarative; actual configuration can drift.
desired = {"replicas": 2, "port": 8000, "tls": True}
actual = {"replicas": 1, "port": 8000, "tls": False}

def diff(wanted, observed):
    return {key: (wanted[key], observed.get(key)) for key in wanted if wanted[key] != observed.get(key)}

print("EXPECTED FAILURE: configuration drift =", diff(desired, actual))
actual.update(desired)  # Simulated reconciliation; no cloud resources changed.
print("RECOVERY: drift after reconciliation =", diff(desired, actual))
print("TRADE-OFF: IaC plans require review before applying destructive changes.")
