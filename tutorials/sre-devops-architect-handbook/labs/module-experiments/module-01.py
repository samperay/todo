#!/usr/bin/env python3
"""Module 01: Application Architecture Fundamentals. Safe Python 3 standard-library learning lab.

Usage:
  python3 module-01.py
  python3 module-01.py --list
  python3 module-01.py --lesson 01.01

The lab is a teaching model; it does NOT deploy infrastructure or modify Todo.
"""
import argparse

LESSONS = {'01.01': 'application boundaries and responsibilities', '01.02': 'react bootstrap main tsx', '01.03': 'component composition app tsx', '01.04': 'development servers and ports', '01.05': 'tcp listeners and process trees', '01.06': 'http status codes and headers', '01.07': 'vite proxy and same origin routing', '01.08': 'bearer authentication request path', '01.09': 'dependency failure and 502 diagnosis', '01.10': 'architecture diagrams and adrs'}


def demonstrate():
    """Show a small working example, an observed failure, and a design lesson."""
    from urllib.request import urlopen
    from urllib.error import URLError, HTTPError
    for port in (5173, 8000, 65534):
        url = f"http://127.0.0.1:{port}/api/v1/todos"
        try:
            with urlopen(url, timeout=1) as response:
                print(url, 'HTTP', response.status)
        except HTTPError as error:
            print(url, 'HTTP', error.code, '(reachable, response error)')
        except URLError as error:
            print(url, 'UNREACHABLE:', type(error.reason).__name__)


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
        print('MODULE 01: Application Architecture Fundamentals')
    print('LAB: HTTP dependency boundary')
    demonstrate()
    print('ARCHITECTURE LESSON: An HTTP 401 can mean a reachable service requiring authentication; a refused connection is different.')
    print('EVIDENCE: this was a standalone local exercise, not a production deployment')


if __name__ == '__main__':
    main()
