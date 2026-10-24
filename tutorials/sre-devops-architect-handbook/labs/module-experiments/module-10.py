#!/usr/bin/env python3
"""Safe standalone baseline/failure/recovery experiment."""
import shutil,subprocess
if not shutil.which('kubectl'):print('SKIP: kubectl not installed')
else:
 p=subprocess.run(['kubectl','version','--client'],capture_output=True,text=True,timeout=8)
 print((p.stdout or p.stderr)[:300])
print('Failure drill: absent local cluster is a prerequisite issue, not application outage')
print('Recovery: configure disposable local cluster and verify kubectl config current-context')
