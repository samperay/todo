#!/usr/bin/env python3
"""Module 08 — CI pipeline quality gates.

Standalone educational experiment for the Todo SRE/DevOps Architect handbook.
Run: python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-08.py

Learning flow:
  1. Read the comments and predict the output.
  2. Run the healthy case and inspect the output.
  3. Observe the explicitly labeled simulated failure.
  4. Explain the recovery and production limitations.

This script does not modify the Todo application's code or database.
"""

import ast

# A miniature CI gate: syntax checks must pass before a release.
sources = {"valid.py": "def add(a, b):\n    return a + b\n", "broken.py": "def broken(:\n    pass\n"}
failed = 0
for filename, source in sources.items():
    try:
        ast.parse(source)
        print("PASS:", filename)
    except SyntaxError as error:
        failed += 1
        print("EXPECTED FAILURE:", filename, "line", error.lineno)
print("PIPELINE RESULT:", "BLOCK MERGE" if failed else "ALLOW MERGE")
print("RECOVERY: fix syntax, rerun gate, then request review.")
