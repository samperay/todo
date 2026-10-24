#!/usr/bin/env python3
"""Safe standalone baseline/failure/recovery experiment."""
import time
attempts=0
for n in range(1,5):
    attempts+=1
    ok=n>=3
    print('attempt',n,'success' if ok else 'simulated HTTP 503')
    if ok:break
    delay=min(0.05*2**(n-1),0.2)
    print('backoff seconds',round(delay,3));time.sleep(delay)
print('Failure: persistent 503; circuit opens after 3 failures')
failures=3;state='OPEN' if failures>=3 else 'CLOSED'
print('breaker state:',state)
print('Recovery: after cooldown, test ONE request in HALF_OPEN before closing')
