#!/usr/bin/env python3
"""Module 07: Containerization. Safe Python 3 standard-library learning lab.

Usage:
  python3 module-07.py
  python3 module-07.py --list
  python3 module-07.py --lesson 07.01

The lab is a teaching model; it does NOT deploy infrastructure or modify Todo.
"""
import argparse

LESSONS = {'07.01': 'containers versus virtual machines', '07.02': 'dockerfile layers and build cache', '07.03': 'multi stage react build', '07.04': 'fastapi container image', '07.05': 'port publishing and container dns', '07.06': 'compose services and networks', '07.07': 'volumes and sqlite persistence', '07.08': 'environment variables and secrets', '07.09': 'health checks and startup dependencies', '07.10': 'image scanning and non root users', '07.11': 'container debugging and logs'}


def demonstrate():
    """Show a small working example, an observed failure, and a design lesson."""
    import shutil, subprocess
    if not shutil.which('docker'):
        print('SKIP: Docker not installed; read-only check only')
    else:
        for args in (['docker', '--version'], ['docker', 'info', '--format', '{{.ServerVersion}}']):
            try:
                r = subprocess.run(args, capture_output=True, text=True, timeout=5)
                print(' '.join(args), 'exit=', r.returncode, (r.stdout or r.stderr).strip()[:200])
            except (OSError, subprocess.TimeoutExpired) as error:
                print('CHECK FAILED:', type(error).__name__)


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
        print('MODULE 07: Containerization')
    print('LAB: Container prerequisites')
    demonstrate()
    print('ARCHITECTURE LESSON: The Docker CLI may be installed while its daemon is stopped.')
    print('EVIDENCE: this was a standalone local exercise, not a production deployment')


if __name__ == '__main__':
    main()
