#!/usr/bin/env python3
"""Safe standalone baseline/failure/recovery experiment."""
availability=[0.99,0.995,0.999]
print('Series dependency availability:',round(__import__('math').prod(availability)*100,4),'%')
print('Failure: if any mandatory dependency fails, end-to-end request fails')
print('Recovery: remove noncritical synchronous dependency or add safe fallback')
print('No cloud calls or charges performed')
