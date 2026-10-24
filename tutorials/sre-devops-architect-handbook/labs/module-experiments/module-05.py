#!/usr/bin/env python3
"""Module 05 — Processes and exit codes.

Standalone educational experiment for the Todo SRE/DevOps Architect handbook.
Run: python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-05.py

Learning flow:
  1. Read the comments and predict the output.
  2. Run the healthy case and inspect the output.
  3. Observe the explicitly labeled simulated failure.
  4. Explain the recovery and production limitations.

This script does not modify the Todo application's code or database.
"""

import subprocess
import sys

# A process has a lifecycle and an exit status; 0 conventionally means success.
for exit_code in (0, 2):
    child = subprocess.run([sys.executable, "-c", f"import sys; sys.exit({exit_code})"], check=False)
    print("CHILD EXIT CODE:", child.returncode)
    if child.returncode:
        print("EXPECTED FAILURE: supervisor would flag a failed process")
print("RECOVERY: restart a failed disposable process after fixing its cause.")
