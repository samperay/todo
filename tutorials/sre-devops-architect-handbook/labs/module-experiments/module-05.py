#!/usr/bin/env python3
"""Safe standalone baseline/failure/recovery experiment."""
import os,signal,subprocess,sys,time
p=subprocess.Popen([sys.executable,'-c','import time;time.sleep(30)'])
print('child PID:',p.pid,'alive:',p.poll() is None)
p.terminate()
try:p.wait(timeout=3)
except subprocess.TimeoutExpired:p.kill();p.wait()
print('failure injected: SIGTERM; exit status:',p.returncode)
print('recovery: restart service using its supervisor; no orphaned child')
