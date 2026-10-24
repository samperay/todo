#!/usr/bin/env python3
"""Safe standalone baseline/failure/recovery experiment."""
import os,tempfile,stat
fd,path=tempfile.mkstemp();os.close(fd)
try:
 os.chmod(path,0o600)
 print('private file mode:',oct(stat.S_IMODE(os.stat(path).st_mode)))
 os.chmod(path,0o644)
 print('failure injected: overly broad mode:',oct(stat.S_IMODE(os.stat(path).st_mode)))
 os.chmod(path,0o600)
 print('recovery mode:',oct(stat.S_IMODE(os.stat(path).st_mode)))
finally:os.remove(path)
print('Never store actual credentials in lab output or git')
