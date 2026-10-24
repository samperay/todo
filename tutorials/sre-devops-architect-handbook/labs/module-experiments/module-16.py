#!/usr/bin/env python3
"""Module 16: Security And Devsecops. Safe Python 3 standard-library learning lab.

Usage:
  python3 module-16.py
  python3 module-16.py --list
  python3 module-16.py --lesson 16.01

The lab is a teaching model; it does NOT deploy infrastructure or modify Todo.
"""
import argparse

LESSONS = {'16.01': 'threat modeling and trust boundaries', '16.02': 'authentication versus authorization', '16.03': 'bearer token risks and localstorage', '16.04': 'tls and certificate validation', '16.05': 'root and intermediate cas', '16.06': 'secrets lifecycle and rotation', '16.07': 'dependency vulnerability scanning', '16.08': 'sbom and image provenance', '16.09': 'least privilege and rbac', '16.10': 'input validation and abuse prevention', '16.11': 'audit logging and incident response'}


def demonstrate():
    """Show a small working example, an observed failure, and a design lesson."""
    permissions = {'reader': {'todo:read'}, 'editor': {'todo:read', 'todo:write'}}
    for role, action in (('reader', 'todo:read'), ('reader', 'todo:write'), ('editor', 'todo:write')):
        allowed = action in permissions[role]
        print(role, action, 'ALLOW' if allowed else 'DENY')
    print('SECURITY: deny by default; never print real tokens')


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
        print('MODULE 16: Security And Devsecops')
    print('LAB: Authorization check')
    demonstrate()
    print('ARCHITECTURE LESSON: Authentication identifies the caller; authorization limits permitted actions.')
    print('EVIDENCE: this was a standalone local exercise, not a production deployment')


if __name__ == '__main__':
    main()
