#!/usr/bin/env python3
"""Module 03 — Producer–consumer queues.

Standalone educational experiment for the Todo SRE/DevOps Architect handbook.
Run: python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-03.py

Learning flow:
  1. Read the comments and predict the output.
  2. Run the healthy case and inspect the output.
  3. Observe the explicitly labeled simulated failure.
  4. Explain the recovery and production limitations.

This script does not modify the Todo application's code or database.
"""

from queue import Queue
from threading import Thread

# The producer creates messages; a worker consumes them in another thread.
messages = Queue()

def worker():
    while True:
        item = messages.get()  # Wait until an item is available.
        try:
            if item is None:  # A sentinel asks the worker to stop.
                return
            print("CONSUMER processed:", item)
        finally:
            messages.task_done()  # Balance every successful get().

thread = Thread(target=worker)
thread.start()
for number in range(1, 4):
    message = f"TodoCompleted-{number}"
    messages.put(message)
    print("PRODUCER queued:", message)
messages.put(None)
messages.join()
thread.join()
print("SUCCESS: all queued items accounted for")

# Failure: model a process restart by replacing the in-memory queue.
pending = Queue()
pending.put("notification-not-yet-processed")
print("BEFORE RESTART: pending messages =", pending.qsize())
pending = Queue()  # Simulates loss of volatile state, not a real process crash.
print("AFTER RESTART: pending messages =", pending.qsize())
print("RECOVERY DESIGN: persistent outbox or durable broker + idempotent worker.")
