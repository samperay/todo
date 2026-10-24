#!/usr/bin/env python3
"""Module 15: Performance And Scalability. Safe Python 3 standard-library learning lab.

Usage:
  python3 module-15.py
  python3 module-15.py --list
  python3 module-15.py --lesson 15.01

The lab is a teaching model; it does NOT deploy infrastructure or modify Todo.
"""
import argparse

LESSONS = {'15.01': 'latency versus throughput', '15.02': 'concurrency and queueing', '15.03': 'baseline and reproducibility', '15.04': 'load generators and safe limits', '15.05': 'p50 p95 p99 latency', '15.06': 'python profiling', '15.07': 'database query analysis', '15.08': 'caching and invalidation', '15.09': 'rate limiting and overload', '15.10': 'capacity estimates', '15.11': 'autoscaling trade offs'}


def demonstrate():
    """Show a small working example, an observed failure, and a design lesson."""
    arrival_rate = 100
    service_rate = 60
    for seconds in (1, 10, 60):
        backlog = max(0, arrival_rate - service_rate) * seconds
        print(f'AFTER {seconds}s: backlog={backlog}')
    print('FAILURE: sustained overload grows queue and delay')


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
        print('MODULE 15: Performance And Scalability')
    print('LAB: Queue capacity')
    demonstrate()
    print('ARCHITECTURE LESSON: Adding a queue does not solve sustained throughput deficits.')
    print('EVIDENCE: this was a standalone local exercise, not a production deployment')


if __name__ == '__main__':
    main()
