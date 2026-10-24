#!/usr/bin/env python3
"""Module 14: Sre Reliability Engineering. Safe Python 3 standard-library learning lab.

Usage:
  python3 module-14.py
  python3 module-14.py --list
  python3 module-14.py --lesson 14.01

The lab is a teaching model; it does NOT deploy infrastructure or modify Todo.
"""
import argparse

LESSONS = {'14.01': 'service level indicators', '14.02': 'service level objectives', '14.03': 'error budgets and burn rates', '14.04': 'availability versus correctness', '14.05': 'latency percentiles', '14.06': 'alerting on symptoms', '14.07': 'incident severity and response', '14.08': 'runbooks and escalation', '14.09': 'postmortems and action items', '14.10': 'toil reduction and automation', '14.11': 'capacity planning and reliability reviews'}


def demonstrate():
    """Show a small working example, an observed failure, and a design lesson."""
    total = 10000
    success = 9980
    target = 0.999
    allowed_failures = round(total * (1 - target))
    actual_failures = total - success
    print('SLO:', target, 'allowed failures:', allowed_failures)
    print('actual failures:', actual_failures, 'remaining budget:', allowed_failures - actual_failures)


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
        print('MODULE 14: Sre Reliability Engineering')
    print('LAB: SLO error budget')
    demonstrate()
    print('ARCHITECTURE LESSON: Error budgets quantify how much unreliability is permitted in an SLO window.')
    print('EVIDENCE: this was a standalone local exercise, not a production deployment')


if __name__ == '__main__':
    main()
