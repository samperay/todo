#!/usr/bin/env python3
"""Module 04 — Database transactions and rollback.

Standalone educational experiment for the Todo SRE/DevOps Architect handbook.
Run: python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-04.py

Learning flow:
  1. Read the comments and predict the output.
  2. Run the healthy case and inspect the output.
  3. Observe the explicitly labeled simulated failure.
  4. Explain the recovery and production limitations.

This script does not modify the Todo application's code or database.
"""

import sqlite3

# :memory: creates a disposable SQLite database, not the real Todo database.
db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE todos (id INTEGER PRIMARY KEY, title TEXT NOT NULL)")
with db:
    db.execute("INSERT INTO todos VALUES (1, 'Read architecture')")
print("SUCCESS: rows =", db.execute("SELECT COUNT(*) FROM todos").fetchone()[0])

# Failure: duplicate primary key forces a rollback of the transaction.
try:
    with db:
        db.execute("INSERT INTO todos VALUES (2, 'Temporary')")
        db.execute("INSERT INTO todos VALUES (1, 'Duplicate')")
except sqlite3.IntegrityError as error:
    print("EXPECTED FAILURE:", type(error).__name__)
print("RECOVERY: rows after rollback =", db.execute("SELECT COUNT(*) FROM todos").fetchone()[0])
db.close()
