#!/usr/bin/env python3
"""Module 12: Cloud Architecture. Safe Python 3 standard-library learning lab.

Usage:
  python3 module-12.py
  python3 module-12.py --list
  python3 module-12.py --lesson 12.01

The lab is a teaching model; it does NOT deploy infrastructure or modify Todo.
"""
import argparse

LESSONS = {'12.01': 'regions availability zones and failure domains', '12.02': 'vpc and subnet design', '12.03': 'routing nat and firewalls', '12.04': 'iam identities and least privilege', '12.05': 'compute selection vms containers serverless', '12.06': 'managed database trade offs', '12.07': 'object storage and backup', '12.08': 'load balancers and dns', '12.09': 'secrets and key management', '12.10': 'cost and tagging', '12.11': 'well architected review'}


def demonstrate():
    """Show a small working example, an observed failure, and a design lesson."""
    zones = {'zone-a': True, 'zone-b': True}
    print('HEALTHY ZONES:', sum(zones.values()))
    zones['zone-a'] = False
    print('FAILURE: zone-a down; available zones:', [k for k, ok in zones.items() if ok])
    print('RECOVERY: route to healthy zone and restore redundancy')


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
        print('MODULE 12: Cloud Architecture')
    print('LAB: Availability-zone failure')
    demonstrate()
    print('ARCHITECTURE LESSON: Availability zones reduce some correlated failures but do not replace backups.')
    print('EVIDENCE: this was a standalone local exercise, not a production deployment')


if __name__ == '__main__':
    main()
