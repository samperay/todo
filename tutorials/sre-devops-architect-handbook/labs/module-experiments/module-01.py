#!/usr/bin/env python3
"""Safe standalone baseline/failure/recovery experiment."""
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
for port in (5173,8000):
    url=f'http://127.0.0.1:{port}/api/v1/todos'
    try:
        with urlopen(url,timeout=2) as r: print(url,'HTTP',r.status)
    except HTTPError as e: print(url,'HTTP',e.code,'(401 means service reachable)')
    except URLError as e: print(url,'UNREACHABLE',type(e.reason).__name__)
print('Failure simulation: unreachable port 65534')
try: urlopen('http://127.0.0.1:65534/',timeout=1)
except URLError as e: print('EXPECTED failure:',type(e.reason).__name__)
print('Recovery: repeat the healthy endpoint check after starting the local services.')
