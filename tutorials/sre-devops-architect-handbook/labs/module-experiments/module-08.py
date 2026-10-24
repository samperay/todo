#!/usr/bin/env python3
"""Safe standalone baseline/failure/recovery experiment."""
import shutil,subprocess
for cmd in (['git','status','--short'],['git','branch','--show-current']):
 if shutil.which(cmd[0]):
  p=subprocess.run(cmd,capture_output=True,text=True);print(' '.join(cmd),':',p.stdout.strip() or '(clean/no output)')
print('Failure simulation: an intentionally failing test should block a merge')
print('Recovery: fix the test, rerun all gates, and verify branch protection')
