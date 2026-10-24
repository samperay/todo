#!/usr/bin/env python3
"""Module 13: Observability Engineering. Safe Python 3 standard-library learning lab.

Usage:
  python3 module-13.py
  python3 module-13.py --list
  python3 module-13.py --lesson 13.01

The lab is a teaching model; it does NOT deploy infrastructure or modify Todo.
"""
import argparse

LESSONS = {'13.01': 'three pillars and their limitations', '13.02': 'existing metrics endpoint and exposition format', '13.03': 'counters gauges histograms', '13.04': 'red and use methods', '13.05': 'label cardinality', '13.06': 'promql rates and quantiles', '13.07': 'grafana dashboards', '13.08': 'structured application logging', '13.09': 'trace and span fundamentals', '13.10': 'opentelemetry instrumentation', '13.11': 'alerting and noise reduction', '13.12': 'operational runbooks'}


def demonstrate():
    """Show a small working example, an observed failure, and a design lesson."""
    requests = [('GET', 200, .05), ('GET', 200, .07), ('POST', 500, .20)]
    print('COUNTER:', len(requests))
    print('5XX:', sum(500 <= status < 600 for _, status, _ in requests))
    print('HISTOGRAM_COUNT:', len(requests))
    print('HISTOGRAM_SUM:', round(sum(duration for _, _, duration in requests), 3))
    print('FAILURE: missing scrape is unknown, not zero traffic')


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
        print('MODULE 13: Observability Engineering')
    print('LAB: RED metrics')
    demonstrate()
    print('ARCHITECTURE LESSON: Counter, gauge and histogram answer different questions; labels must remain bounded.')
    print('EVIDENCE: this was a standalone local exercise, not a production deployment')


if __name__ == '__main__':
    main()
