#!/usr/bin/env python3
"""Safe standalone baseline/failure/recovery experiment."""
import queue,threading,time
q=queue.Queue()
def worker():
    while True:
        item=q.get()
        if item is None:q.task_done();break
        print('consumed:',item);q.task_done()
t=threading.Thread(target=worker);t.start()
for n in range(3):q.put(f'TodoCompleted-{n}')
q.put(None);q.join();t.join();print('healthy: all tasks acknowledged')
print('Failure simulation: new in-memory queue contains pending message')
volatile=queue.Queue();volatile.put('unprocessed-event');print('before simulated restart:',volatile.qsize())
volatile=queue.Queue();print('after simulated restart:',volatile.qsize())
print('Recovery design: use durable outbox/broker, acknowledgments and idempotent consumers')
