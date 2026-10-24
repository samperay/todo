#!/usr/bin/env python3
"""Safe standalone baseline/failure/recovery experiment."""
import json
adr={'decision':'Keep SQLite for single-writer local Todo baseline','alternatives':['PostgreSQL','SQLite'],'risk':'multi-instance writes need review','validation':'run transactional and backup labs'}
print(json.dumps(adr,indent=2))
print('Failure scenario: unsupported scale assumption')
print('Recovery: revise ADR using measured workload and constraints')
