#!/usr/bin/env python3
"""Module 08: Ci Cd And Software Delivery. Safe Python 3 standard-library learning lab.

Usage:
  python3 module-08.py
  python3 module-08.py --list
  python3 module-08.py --lesson 08.01

The lab is a teaching model; it does NOT deploy infrastructure or modify Todo.
"""
import argparse

LESSONS = {'08.01': 'ci versus cd', '08.02': 'git branching and protected main', '08.03': 'ruff mypy and pytest jobs', '08.04': 'frontend lint build test gates', '08.05': 'dependency pinning and caching', '08.06': 'build artifacts and provenance', '08.07': 'container registry workflows', '08.08': 'release tags and semantic versioning', '08.09': 'deployment environments and approvals', '08.10': 'rolling blue green and canary strategies', '08.11': 'rollback and verification', '08.12': 'pipeline threat modeling'}


def demonstrate():
    """Show a small working example, an observed failure, and a design lesson."""
    import subprocess, sys
    for script in ('print("PASS")', 'raise SystemExit(1)'):
        r = subprocess.run([sys.executable, '-c', script], capture_output=True, text=True)
        print('CI STEP:', 'PASS' if r.returncode == 0 else 'FAIL', 'exit=', r.returncode)


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
        print('MODULE 08: Ci Cd And Software Delivery')
    print('LAB: Quality gate')
    demonstrate()
    print('ARCHITECTURE LESSON: CI should block merging when required checks fail.')
    print('EVIDENCE: this was a standalone local exercise, not a production deployment')


if __name__ == '__main__':
    main()
