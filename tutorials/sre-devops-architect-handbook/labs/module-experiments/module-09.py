#!/usr/bin/env python3
"""Safe standalone baseline/failure/recovery experiment."""
import shutil,subprocess
if not shutil.which('terraform'):print('SKIP: Terraform not installed; no cloud resources created')
else:
 p=subprocess.run(['terraform','version'],capture_output=True,text=True,timeout=10)
 print(p.stdout.splitlines()[0] if p.stdout else p.stderr[:180])
print('Failure drill: invalid configuration should fail terraform validate, NOT apply')
print('Recovery: correct configuration; run fmt, validate and plan; inspect cost before apply')
