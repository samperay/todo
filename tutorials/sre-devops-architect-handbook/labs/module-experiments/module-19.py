#!/usr/bin/env python3
"""Module 19 — AI-assisted incident triage with guardrails.

Standalone educational experiment for the Todo SRE/DevOps Architect handbook.
Run: python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-19.py

Learning flow:
  1. Read the comments and predict the output.
  2. Run the healthy case and inspect the output.
  3. Observe the explicitly labeled simulated failure.
  4. Explain the recovery and production limitations.

This script does not modify the Todo application's code or database.
"""

# Rule-based stand-in for an AI assistant: read-only recommendations, no changes.
incidents = ["HTTP 503 on Todo API", "Queue backlog increasing", "All healthy"]

def suggest(message):
    text = message.lower()
    if "503" in text:
        return "Check upstream readiness, dependencies, and recent deploys"
    if "backlog" in text:
        return "Inspect consumer health, message age, and worker throughput"
    return "No immediate action; continue monitoring"

for incident in incidents:
    print("SIGNAL:", incident, "| SUGGESTION:", suggest(incident))
print("FAILURE MODE: recommendations can be wrong or incomplete.")
print("RECOVERY: human verifies evidence before approving any remediation.")
