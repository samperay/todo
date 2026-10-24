#!/usr/bin/env python3
"""Module 04: Backend Architecture And Database Engineering. Safe Python 3 standard-library learning lab.

Usage:
  python3 module-04.py
  python3 module-04.py --list
  python3 module-04.py --lesson 04.01

The lab is a teaching model; it does NOT deploy infrastructure or modify Todo.
"""
import argparse

LESSONS = {'04.01': 'fastapi request lifecycle', '04.02': 'route versus service versus repository', '04.03': 'pydantic v2 typed contracts', '04.04': 'authentication and authorization boundaries', '04.05': 'sqlalchemy sessions and transactions', '04.06': 'sqlite locking and concurrency', '04.07': 'schema evolution without alembic', '04.08': 'indexes and query plans', '04.09': 'data integrity and uniqueness', '04.10': 'api error contracts', '04.11': 'dependency injection and testability', '04.12': 'architecture review for database migration'}


def demonstrate():
    """Show a small working example, an observed failure, and a design lesson."""
    import sqlite3
    connection = sqlite3.connect(':memory:')
    connection.execute('CREATE TABLE todo (id INTEGER PRIMARY KEY, title TEXT NOT NULL)')
    connection.execute("INSERT INTO todo VALUES (1, 'read')")
    connection.commit()
    try:
        with connection:
            connection.execute("INSERT INTO todo VALUES (2, 'write')")
            raise RuntimeError('simulated transaction failure')
    except RuntimeError as error:
        print('EXPECTED FAILURE:', error)
    print('ROWS AFTER ROLLBACK:', connection.execute('SELECT * FROM todo').fetchall())


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
        print('MODULE 04: Backend Architecture And Database Engineering')
    print('LAB: SQLite transaction')
    demonstrate()
    print('ARCHITECTURE LESSON: Transaction rollback preserves committed data and discards uncommitted changes.')
    print('EVIDENCE: this was a standalone local exercise, not a production deployment')


if __name__ == '__main__':
    main()
