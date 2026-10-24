#!/usr/bin/env python3
"""Module 14 — SLIs, SLOs and error budgets.

Standalone educational experiment for the Todo SRE/DevOps Architect handbook.
Run: python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-14.py

Learning flow:
  1. Read the comments and predict the output.
  2. Run the healthy case and inspect the output.
  3. Observe the explicitly labeled simulated failure.
  4. Explain the recovery and production limitations.

This script does not modify the Todo application's code or database.
"""

# SLI = successful requests / eligible requests.
total = 1000
failures = 8
slo = 0.995
success_rate = (total - failures) / total
allowed_failures = int(total * (1 - slo) + 1e-9)
print(f"AVAILABILITY SLI: {success_rate:.2%}")
print(f"SLO TARGET: {slo:.2%}")
print("ERROR BUDGET (requests):", allowed_failures)
print("EXPECTED FAILURE: SLO breached?", success_rate < slo)
failures = 2  # Simulate recovery in a new evaluation window.
print("RECOVERY: new-window SLI =", f"{(total - failures) / total:.2%}")
print("NOTE: do not rewrite historical failure data to claim recovery.")
