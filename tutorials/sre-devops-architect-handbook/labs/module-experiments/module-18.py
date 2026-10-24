#!/usr/bin/env python3
"""Module 18 — Backup, restore and recovery verification.

Standalone educational experiment for the Todo SRE/DevOps Architect handbook.
Run: python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-18.py

Learning flow:
  1. Read the comments and predict the output.
  2. Run the healthy case and inspect the output.
  3. Observe the explicitly labeled simulated failure.
  4. Explain the recovery and production limitations.

This script does not modify the Todo application's code or database.
"""

import sqlite3

# SQLite backup API copies data between two disposable in-memory databases.
source = sqlite3.connect(":memory:")
backup = sqlite3.connect(":memory:")
source.execute("CREATE TABLE todos (title TEXT)")
source.execute("INSERT INTO todos VALUES ('Recover me')")
source.commit()
source.backup(backup)
source.execute("DELETE FROM todos")  # Simulated data-loss incident.
source.commit()
print("EXPECTED FAILURE: live rows =", source.execute("SELECT COUNT(*) FROM todos").fetchone()[0])
backup.backup(source)
print("RECOVERY: restored rows =", source.execute("SELECT COUNT(*) FROM todos").fetchone()[0])
source.close()
backup.close()
print("NOTE: real recovery requires tested off-host backups and RPO/RTO targets.")
