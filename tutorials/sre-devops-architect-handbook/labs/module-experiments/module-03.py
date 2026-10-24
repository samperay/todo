#!/usr/bin/env python3
"""Module 03: Asynchronous Processing And Event Driven Architecture. Safe Python 3 standard-library learning lab.

Usage:
  python3 module-03.py
  python3 module-03.py --list
  python3 module-03.py --lesson 03.01

The lab is a teaching model; it does NOT deploy infrastructure or modify Todo.
"""
import argparse

LESSONS = {'03.01': 'synchronous versus asynchronous requests', '03.02': 'python queue queue producer consumer', '03.03': 'threads and worker lifecycle', '03.04': 'messages commands and events', '03.05': 'todocompleted event contract', '03.06': 'durability and acknowledgment semantics', '03.07': 'sqlite transactional outbox', '03.08': 'retry policies and poison messages', '03.09': 'dead letter queues and replay', '03.10': 'idempotent consumer and deduplication', '03.11': 'rabbitmq exchange queue routing key', '03.12': 'python publisher and consumer integration', '03.13': 'docker compose multi service topology', '03.14': 'competing consumers and scaling', '03.15': 'queue depth and age observability', '03.16': 'failure injection and recovery', '03.17': 'broker security tls and secrets', '03.18': 'architecture review and delivery guarantees'}


def demonstrate():
    """Show a small working example, an observed failure, and a design lesson."""
    from queue import Queue, Empty
    q = Queue()
    for n in range(1, 4):
        q.put(f'TodoCompleted-{n}')
        print('PRODUCER queued:', f'TodoCompleted-{n}')
    print('pending:', q.qsize())
    while True:
        try:
            item = q.get_nowait()
        except Empty:
            break
        print('CONSUMER processed:', item)
        q.task_done()
    q.join()
    print('SUCCESS: queue accounting complete')
    volatile = Queue()
    volatile.put('unprocessed-event')
    print('BEFORE RESTART:', volatile.qsize())
    volatile = Queue()  # Simulated process restart; memory is replaced.
    print('AFTER RESTART:', volatile.qsize())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--list', action='store_true', help='List lesson identifiers')
    parser.add_argument('--lesson', choices=list(LESSONS), help='Focus the experiment on one lesson')
    args = parser.parse_args()
    if args.list:
        for key, topic in LESSONS.items():
            print(key, topic)
        return
    if args.lesson:
        print('LESSON:', args.lesson, LESSONS[args.lesson])
    else:
        print('MODULE 03: Asynchronous Processing And Event Driven Architecture')
    print('LAB: Queue lifecycle')
    demonstrate()
    print('ARCHITECTURE LESSON: get() retrieves/removes work; task_done() updates unfinished-work accounting, not durability.')
    print('EVIDENCE: this was a standalone local exercise, not a production deployment')


if __name__ == '__main__':
    main()
