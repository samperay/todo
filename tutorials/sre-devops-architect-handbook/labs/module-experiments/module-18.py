#!/usr/bin/env python3
"""Module 18: Disaster Recovery And Chaos Engineering. Safe Python 3 standard-library learning lab.

Usage:
  python3 module-18.py
  python3 module-18.py --list
  python3 module-18.py --lesson 18.01

The lab is a teaching model; it does NOT deploy infrastructure or modify Todo.
"""
import argparse

LESSONS = {'18.01': 'backup versus replication', '18.02': 'rpo and rto definitions', '18.03': 'sqlite consistent backup practices', '18.04': 'restore verification', '18.05': 'failure modes and blast radius', '18.06': 'dependency mapping', '18.07': 'fault injection hypotheses', '18.08': 'graceful shutdown and recovery', '18.09': 'disaster runbooks', '18.10': 'game days and incident learning'}


def demonstrate():
    """Show a small working example, an observed failure, and a design lesson."""
    import sqlite3
    source = sqlite3.connect(':memory:')
    source.execute('CREATE TABLE todos (id INTEGER PRIMARY KEY, title TEXT)')
    source.execute("INSERT INTO todos VALUES (1, 'important')")
    source.commit()
    backup = sqlite3.connect(':memory:')
    source.backup(backup)
    source.execute('DELETE FROM todos')
    source.commit()
    print('AFTER LOSS:', source.execute('SELECT * FROM todos').fetchall())
    print('RESTORED COPY:', backup.execute('SELECT * FROM todos').fetchall())


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
        print('MODULE 18: Disaster Recovery And Chaos Engineering')
    print('LAB: Backup and restore')
    demonstrate()
    print('ARCHITECTURE LESSON: A verified restore is stronger evidence than a successful backup command.')
    print('EVIDENCE: this was a standalone local exercise, not a production deployment')


if __name__ == '__main__':
    main()
