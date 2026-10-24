#!/usr/bin/env python3
"""Module 20 — Architecture decision records and trade-offs.

Standalone educational experiment for the Todo SRE/DevOps Architect handbook.
Run: python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-20.py

Learning flow:
  1. Read the comments and predict the output.
  2. Run the healthy case and inspect the output.
  3. Observe the explicitly labeled simulated failure.
  4. Explain the recovery and production limitations.

This script does not modify the Todo application's code or database.
"""

import json

# An ADR captures context, decision, alternatives, consequences and verification.
adr = {
    "context": "Todo currently uses SQLite in the local learning baseline",
    "decision": "Keep SQLite for the single-instance prototype",
    "alternatives": ["SQLite", "PostgreSQL"],
    "benefit": "Simple local setup and low operational cost",
    "risk": "Multi-instance concurrent writes require architectural review",
    "verification": "Measure write concurrency and test backup/restore",
}
print("ARCHITECTURE DECISION RECORD:")
print(json.dumps(adr, indent=2))
print("EXPECTED FAILURE: assuming this design scales without measurements")
print("RECOVERY: revisit the ADR with load tests, requirements and evidence.")
