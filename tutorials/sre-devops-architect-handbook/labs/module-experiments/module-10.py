#!/usr/bin/env python3
"""Module 10: Kubernetes Fundamentals. Safe Python 3 standard-library learning lab.

Usage:
  python3 module-10.py
  python3 module-10.py --list
  python3 module-10.py --lesson 10.01

The lab is a teaching model; it does NOT deploy infrastructure or modify Todo.
"""
import argparse

LESSONS = {'10.01': 'control plane and worker nodes', '10.02': 'pods and container lifecycle', '10.03': 'deployments and replicasets', '10.04': 'services and dns', '10.05': 'namespaces and labels', '10.06': 'configmaps and secrets', '10.07': 'resource requests and limits', '10.08': 'liveness readiness startup probes', '10.09': 'kubectl describe and logs', '10.10': 'rolling updates and rollback', '10.11': 'persistent storage introduction'}


def demonstrate():
    """Show a small working example, an observed failure, and a design lesson."""
    desired = 3
    running = 1
    print('DESIRED PODS:', desired, 'RUNNING:', running)
    while running < desired:
        running += 1
        print('RECONCILE: scheduled simulated pod', running)
    print('HEALTHY: replicas match desired state')


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
        print('MODULE 10: Kubernetes Fundamentals')
    print('LAB: Desired-state reconciliation')
    demonstrate()
    print('ARCHITECTURE LESSON: A Kubernetes controller continuously reconciles actual and desired state; no cluster was used.')
    print('EVIDENCE: this was a standalone local exercise, not a production deployment')


if __name__ == '__main__':
    main()
