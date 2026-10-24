#!/usr/bin/env python3
"""Module 05: Linux And Operating Systems. Safe Python 3 standard-library learning lab.

Usage:
  python3 module-05.py
  python3 module-05.py --list
  python3 module-05.py --lesson 05.01

The lab is a teaching model; it does NOT deploy infrastructure or modify Todo.
"""
import argparse

LESSONS = {'05.01': 'process lifecycle pid and ppid', '05.02': 'signals graceful termination', '05.03': 'file descriptors and sockets', '05.04': 'cpu memory and i o fundamentals', '05.05': 'users groups permissions umask', '05.06': 'systemd unit files and journald', '05.07': 'environment and startup configuration', '05.08': 'resource limits and oom behavior', '05.09': 'disk and filesystem troubleshooting', '05.10': 'shell automation and runbooks'}


def demonstrate():
    """Show a small working example, an observed failure, and a design lesson."""
    import os, subprocess, sys
    print('CURRENT PID:', os.getpid())
    for code in (0, 2):
        result = subprocess.run([sys.executable, '-c', f'import sys;sys.exit({code})'])
        print('CHILD EXIT CODE:', result.returncode)


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
        print('MODULE 05: Linux And Operating Systems')
    print('LAB: Process and exit code')
    demonstrate()
    print('ARCHITECTURE LESSON: Exit codes are process-level signals; a nonzero exit is a failure indicator, not the root cause.')
    print('EVIDENCE: this was a standalone local exercise, not a production deployment')


if __name__ == '__main__':
    main()
