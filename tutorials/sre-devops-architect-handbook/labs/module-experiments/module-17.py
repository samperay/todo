#!/usr/bin/env python3
"""Safe standalone baseline/failure/recovery experiment."""
events=['evt-1','evt-1','evt-2'];seen=set();applied=[]
for event in events:
 if event in seen:print('duplicate suppressed:',event);continue
 seen.add(event);applied.append(event)
print('applied events:',applied)
print('failure: at-least-once transport can redeliver')
print('recovery: durable deduplication key and transactional side effects')
