#!/usr/bin/env python3
"""Safe standalone baseline/failure/recovery experiment."""
import socket
for host in ('localhost','example.invalid'):
 try:print('DNS',host,socket.getaddrinfo(host,None)[0][4][0])
 except socket.gaierror:print('EXPECTED DNS failure:',host)
s=socket.socket();s.settimeout(1)
try:s.connect(('127.0.0.1',65534));print('unexpected listener')
except OSError as e:print('EXPECTED TCP failure:',type(e).__name__)
finally:s.close()
print('Recovery: confirm DNS and target service listener before changing firewall rules')
