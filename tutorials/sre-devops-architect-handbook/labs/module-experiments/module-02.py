#!/usr/bin/env python3
"""Module 02: Application Lifecycle And Resilience. Safe Python 3 standard-library learning lab.

Usage:
  python3 module-02.py
  python3 module-02.py --list
  python3 module-02.py --lesson 02.01

The lab is a teaching model; it does NOT deploy infrastructure or modify Todo.
"""
import argparse

LESSONS = {'02.01': 'react state and re rendering', '02.02': 'browser localstorage versus server persistence', '02.03': 'useeffect and cleanup', '02.04': 'useref and mutable coordination', '02.05': 'abortcontroller and stale requests', '02.06': 'session generations and race prevention', '02.07': 'timeout budgets and http failure taxonomy', '02.08': 'idempotency and safe retry decisions', '02.09': 'exponential backoff and jitter', '02.10': 'circuit breaker states', '02.11': 'graceful degradation and incident diagnosis'}


def demonstrate():
    """Show a small working example, an observed failure, and a design lesson."""
    import random
    random.seed(7)
    for attempt in range(1, 5):
        delay = min(0.1 * 2 ** (attempt - 1), 1.0)
        jitter = random.uniform(0, delay / 2)
        print(f'attempt={attempt} planned_backoff={delay + jitter:.3f}s')
    print('FAILURE: blind retries can amplify overload; bound attempts and use idempotency')


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
        print('MODULE 02: Application Lifecycle And Resilience')
    print('LAB: Retries and timeouts')
    demonstrate()
    print('ARCHITECTURE LESSON: Retries are only safe when the operation is idempotent or deduplicated.')
    print('EVIDENCE: this was a standalone local exercise, not a production deployment')


if __name__ == '__main__':
    main()
