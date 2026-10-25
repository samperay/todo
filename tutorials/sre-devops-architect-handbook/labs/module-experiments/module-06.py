#!/usr/bin/env python3
"""Module 06: Networking And Api Architecture. Safe Python 3 standard-library learning lab.

Usage:
  python3 module-06.py
  python3 module-06.py --list
  python3 module-06.py --lesson 06.01

The lab is a teaching model; it does NOT deploy infrastructure or modify Todo.
"""
import argparse

LESSONS = {'06.01': 'tcp handshake and ports', '06.02': 'loopback versus bind all addresses', '06.03': 'dns resolution and caching', '06.04': 'http methods headers and status', '06.05': 'tls certificates and trust chains', '06.06': 'reverse proxies and upstreams', '06.07': 'cors and same origin policy', '06.08': 'api gateways and rate limiting', '06.09': 'load balancing and health checks', '06.10': 'network failure diagnostics', '06.11': 'request tracing across hops'}


def demonstrate():
    """Show a small working example, an observed failure, and a design lesson."""
    import socket
    for port in (8000, 65534):
        try:
            with socket.create_connection(('127.0.0.1', port), timeout=1):
                print('CONNECTED:', port)
        except OSError as error:
            print('CONNECTION FAILURE:', port, type(error).__name__)


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
        print('MODULE 06: Networking And Api Architecture')
    print('LAB: TCP connection')
    demonstrate()
    print('ARCHITECTURE LESSON: A failed TCP connection is not the same as an HTTP 401/500 response.')
    print('EVIDENCE: this was a standalone local exercise, not a production deployment')


if __name__ == '__main__':
    main()
