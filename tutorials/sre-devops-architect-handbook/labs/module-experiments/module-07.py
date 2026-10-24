#!/usr/bin/env python3
"""Module 07 — Container lifecycle preflight.

Standalone educational experiment for the Todo SRE/DevOps Architect handbook.
Run: python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-07.py

Learning flow:
  1. Read the comments and predict the output.
  2. Run the healthy case and inspect the output.
  3. Observe the explicitly labeled simulated failure.
  4. Explain the recovery and production limitations.

This script does not modify the Todo application's code or database.
"""

import shutil
import subprocess

# Read-only checks: never stop or remove real containers during this lab.
if not shutil.which("docker"):
    print("SKIP: Docker CLI is not installed; no infrastructure test performed")
else:
    for command in (["docker", "--version"], ["docker", "info", "--format", "{{.ServerVersion}}"]):
        try:
            result = subprocess.run(command, text=True, capture_output=True, timeout=5)
            print("COMMAND:", " ".join(command), "EXIT:", result.returncode)
            print("OUTPUT:", (result.stdout or result.stderr).strip()[:250])
        except (OSError, subprocess.TimeoutExpired) as error:
            print("EXPECTED FAILURE/UNAVAILABLE:", type(error).__name__)
print("RECOVERY: start Docker Desktop if the daemon is unavailable; rerun checks.")
