#!/usr/bin/env python3
"""Module 09: Infrastructure As Code. Safe Python 3 standard-library learning lab.

Usage:
  python3 module-09.py
  python3 module-09.py --list
  python3 module-09.py --lesson 09.01

The lab is a teaching model; it does NOT deploy infrastructure or modify Todo.
"""
import argparse

LESSONS = {'09.01': 'declarative infrastructure', '09.02': 'terraform providers and resources', '09.03': 'variables outputs locals', '09.04': 'state and state locking', '09.05': 'plan apply destroy lifecycle', '09.06': 'remote state and encryption', '09.07': 'modules and composition', '09.08': 'environment separation', '09.09': 'drift detection', '09.10': 'least privilege for automation', '09.11': 'policy checks and cost awareness'}


def demonstrate():
    """Show a small working example, an observed failure, and a design lesson."""
    desired = {'replicas': 2, 'region': 'local', 'encrypted': True}
    actual = {'replicas': 1, 'region': 'local', 'encrypted': True}
    for key, expected in desired.items():
        if actual.get(key) != expected:
            print('DRIFT:', key, 'actual=', actual.get(key), 'desired=', expected)
    print('PLAN: review changes before applying')


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
        print('MODULE 09: Infrastructure As Code')
    print('LAB: Configuration drift')
    demonstrate()
    print('ARCHITECTURE LESSON: Declarative IaC compares desired and observed state; this is an offline model, not Terraform.')
    print('EVIDENCE: this was a standalone local exercise, not a production deployment')


if __name__ == '__main__':
    main()
