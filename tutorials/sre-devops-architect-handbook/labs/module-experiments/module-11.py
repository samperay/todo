#!/usr/bin/env python3
"""Module 11: Advanced Kubernetes Architecture. Safe Python 3 standard-library learning lab.

Usage:
  python3 module-11.py
  python3 module-11.py --list
  python3 module-11.py --lesson 11.01

The lab is a teaching model; it does NOT deploy infrastructure or modify Todo.
"""
import argparse

LESSONS = {'11.01': 'ingress and gateway api', '11.02': 'service discovery and traffic flow', '11.03': 'horizontal pod autoscaler', '11.04': 'cluster autoscaling concepts', '11.05': 'persistentvolumes and claims', '11.06': 'storage classes and failure domains', '11.07': 'helm charts and values', '11.08': 'networkpolicies', '11.09': 'poddisruptionbudgets', '11.10': 'affinity and topology spread', '11.11': 'rbac and service accounts', '11.12': 'multi tenant operational boundaries'}


def demonstrate():
    """Show a small working example, an observed failure, and a design lesson."""
    old, new, desired = 3, 0, 3
    while new < desired:
        new += 1
        print('START new replica:', new, 'old:', old)
        if old:
            old -= 1
            print('RETIRE old replica:', old)
    print('ROLLOUT COMPLETE; probe checks are still required in real systems')


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
        print('MODULE 11: Advanced Kubernetes Architecture')
    print('LAB: Rolling update safety')
    demonstrate()
    print('ARCHITECTURE LESSON: A real rollout must consider readiness, PDBs, capacity and rollback, not just replica counts.')
    print('EVIDENCE: this was a standalone local exercise, not a production deployment')


if __name__ == '__main__':
    main()
