#!/usr/bin/env python3
"""Safe standalone baseline/failure/recovery experiment."""
import shutil,subprocess
if not shutil.which('docker'):print('SKIP: install Docker when ready for Module 07')
else:
 for cmd in (['docker','--version'],['docker','info','--format','{{.ServerVersion}}']):
  p=subprocess.run(cmd,capture_output=True,text=True,timeout=8);print(' '.join(cmd),'exit',p.returncode,(p.stdout or p.stderr).strip()[:250])
 print('Failure drill: stop a disposable test container ONLY, then start it again; do not touch production containers')
