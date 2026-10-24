#!/usr/bin/env python3
"""Module 16 — Least privilege and secret handling.

Standalone educational experiment for the Todo SRE/DevOps Architect handbook.
Run: python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-16.py

Learning flow:
  1. Read the comments and predict the output.
  2. Run the healthy case and inspect the output.
  3. Observe the explicitly labeled simulated failure.
  4. Explain the recovery and production limitations.

This script does not modify the Todo application's code or database.
"""

# Model permissions; never print or embed real tokens in labs.
permissions = {"reader": {"todos:read"}, "editor": {"todos:read", "todos:write"}}

def authorize(role, action):
    return action in permissions.get(role, set())

print("SUCCESS: reader can read:", authorize("reader", "todos:read"))
print("EXPECTED DENIAL: reader can write:", authorize("reader", "todos:write"))
print("RECOVERY: use an explicitly authorized role:", authorize("editor", "todos:write"))
print("SECURITY: do not elevate reader privileges to hide authorization errors.")
