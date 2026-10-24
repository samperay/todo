#!/usr/bin/env python3
"""Safe standalone baseline/failure/recovery experiment."""
import shutil,subprocess
for tool in ('kubectl','helm'):
 print(tool,'available' if shutil.which(tool) else 'SKIP: not installed')
print('Failure drill: avoid changing real cluster contexts; use a disposable local cluster')
print('Recovery: verify context, namespace, rollout status, then rollback a test deployment')
