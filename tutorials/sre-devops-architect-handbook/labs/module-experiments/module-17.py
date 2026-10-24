#!/usr/bin/env python3
"""Module 17: Distributed Systems Architecture. Safe Python 3 standard-library learning lab.

Usage:
  python3 module-17.py
  python3 module-17.py --list
  python3 module-17.py --lesson 17.01

The lab is a teaching model; it does NOT deploy infrastructure or modify Todo.
"""
import argparse

LESSONS = {'17.01': 'partial failure and unreliable networks', '17.02': 'latency and timeout uncertainty', '17.03': 'cap trade offs with assumptions', '17.04': 'strong versus eventual consistency', '17.05': 'replication and failover', '17.06': 'leader election concepts', '17.07': 'distributed locks and fencing', '17.08': 'idempotency and deduplication', '17.09': 'at least once versus at most once delivery', '17.10': 'transactional outbox and sagas', '17.11': 'clock skew and ordering', '17.12': 'architecture decision trade offs'}


def demonstrate():
    """Show a small working example, an observed failure, and a design lesson."""
    seen = set()
    for event_id in ('evt-1', 'evt-2', 'evt-1'):
        if event_id in seen:
            print('DUPLICATE SKIPPED:', event_id)
            continue
        seen.add(event_id)
        print('APPLIED ONCE:', event_id)


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
        print('MODULE 17: Distributed Systems Architecture')
    print('LAB: Duplicate delivery')
    demonstrate()
    print('ARCHITECTURE LESSON: At-least-once delivery may produce duplicates; durable deduplication needs persistent state.')
    print('EVIDENCE: this was a standalone local exercise, not a production deployment')


if __name__ == '__main__':
    main()
