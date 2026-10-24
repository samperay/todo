#!/usr/bin/env python3
"""Module 06 — TCP connectivity and timeouts.

Standalone educational experiment for the Todo SRE/DevOps Architect handbook.
Run: python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-06.py

Learning flow:
  1. Read the comments and predict the output.
  2. Run the healthy case and inspect the output.
  3. Observe the explicitly labeled simulated failure.
  4. Explain the recovery and production limitations.

This script does not modify the Todo application's code or database.
"""

import socket
from threading import Thread

# Bind an ephemeral loopback port; no real Todo service is changed.
server = socket.socket()
server.bind(("127.0.0.1", 0))
server.listen(1)
port = server.getsockname()[1]

def serve_once():
    connection, _ = server.accept()
    with connection:
        connection.sendall(b"hello from server")
    server.close()

thread = Thread(target=serve_once)
thread.start()
with socket.create_connection(("127.0.0.1", port), timeout=2) as client:
    print("SUCCESS:", client.recv(1024).decode())
thread.join()
try:
    socket.create_connection(("127.0.0.1", port), timeout=1)
except OSError as error:
    print("EXPECTED FAILURE: listener closed:", type(error).__name__)
print("RECOVERY: restore the listener and verify TCP connectivity.")
