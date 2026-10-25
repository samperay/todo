#!/usr/bin/env python3
"""Module 20: Sre Devops Architect Capstone. Safe Python 3 standard-library learning lab.

Usage:
  python3 module-20.py
  python3 module-20.py --list
  python3 module-20.py --lesson 20.01

The lab is a teaching model; it does NOT deploy infrastructure or modify Todo.
"""
import argparse

LESSONS = {'20.01': 'business and nonfunctional requirements', '20.02': 'current state and target state architecture', '20.03': 'capacity and failure assumptions', '20.04': 'security and threat modeling', '20.05': 'cost and operational complexity', '20.06': 'technology selection trade offs', '20.07': 'architecture decision records', '20.08': 'ci cd and change safety', '20.09': 'slos monitoring and incident response', '20.10': 'disaster recovery and game days', '20.11': 'operational readiness review', '20.12': 'executive communication and portfolio presentation'}


def demonstrate():
    """Show a small working example, an observed failure, and a design lesson."""
    import json
    adr = {'context': 'single-instance Todo with SQLite', 'decision': 'retain SQLite for local baseline', 'alternatives': ['managed database'], 'risk': 'multi-writer scale needs review', 'validation': 'backup/restore and load labs'}
    print(json.dumps(adr, indent=2))
    print('FAILURE: assumptions are invalid without measured evidence')


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
        print('MODULE 20: Sre Devops Architect Capstone')
    print('LAB: Architecture decision record')
    demonstrate()
    print('ARCHITECTURE LESSON: Architecture decisions should capture constraints, alternatives, validation and reversal conditions.')
    print('EVIDENCE: this was a standalone local exercise, not a production deployment')


if __name__ == '__main__':
    main()
