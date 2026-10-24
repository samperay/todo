#!/usr/bin/env python3
"""Module 19: Ai For Sre And Devops. Safe Python 3 standard-library learning lab.

Usage:
  python3 module-19.py
  python3 module-19.py --list
  python3 module-19.py --lesson 19.01

The lab is a teaching model; it does NOT deploy infrastructure or modify Todo.
"""
import argparse

LESSONS = {'19.01': 'llm capabilities and limitations', '19.02': 'rag for runbooks and incidents', '19.03': 'tool calling agents and permissions', '19.04': 'prompt and context design', '19.05': 'human in the loop operations', '19.06': 'read only diagnosis before write actions', '19.07': 'evaluation datasets and grounded answers', '19.08': 'prompt injection and tool output trust', '19.09': 'auditability and rollback', '19.10': 'ai assisted incident summarization', '19.11': 'cost and latency controls'}


def demonstrate():
    """Show a small working example, an observed failure, and a design lesson."""
    incident = {'service': 'todo-api', 'status': 503, 'logs': ['upstream unavailable']}
    recommendation = 'inspect upstream health and timeout budget'
    print('EVIDENCE:', incident)
    print('PROPOSED READ-ONLY DIAGNOSIS:', recommendation)
    print('WRITE ACTION: BLOCKED pending human approval')


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
        print('MODULE 19: Ai For Sre And Devops')
    print('LAB: Read-only AI operations gate')
    demonstrate()
    print('ARCHITECTURE LESSON: LLM output is a hypothesis; verify against evidence before executing changes.')
    print('EVIDENCE: this was a standalone local exercise, not a production deployment')


if __name__ == '__main__':
    main()
