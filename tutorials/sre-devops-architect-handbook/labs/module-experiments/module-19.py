#!/usr/bin/env python3
"""Safe standalone baseline/failure/recovery experiment."""
alerts=[{'service':'todo-api','error_rate':.12,'latency_ms':800}]
for a in alerts:
 print('read-only diagnosis:',a)
 if a['error_rate']>.05:print('PROPOSE: inspect logs, metrics and recent deployments')
print('Failure scenario: model proposes unsafe automatic restart')
print('Recovery: require human approval, audit logs and bounded permissions')
