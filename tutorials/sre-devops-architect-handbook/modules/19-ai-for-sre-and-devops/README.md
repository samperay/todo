# Module 19 — Ai For Sre And Devops

**Scope:** AI-assisted operations safety gate.  
**Status:** Guided learning; verify evidence before marking complete.

## Why it matters

This module connects the running Todo application with **Ai For Sre And Devops**. Begin with a dependency-free simulation, then investigate the actual application or local infrastructure. A simulated result is not evidence of a deployed production capability.

## Prerequisites

- Python 3, Git, Todo repository checked out on the intended branch.
- Read [environment setup](../../labs/ENVIRONMENT_SETUP.md) and [architecture baseline](../../architecture/CURRENT_AND_TARGET.md).
- Optional infrastructure tools are introduced only when their lessons require them.

## Baseline lab — executable

From the Todo repository root:

```bash
pwd
git status --short
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-19.py
```

**Expected:** A successful baseline observation plus a bounded failure/recovery demonstration for **AI-assisted operations safety gate**. The experiment does not modify Todo application code. A `SKIP` line means a prerequisite is absent; do not report the corresponding infrastructure as tested.

**Failure:** The experiment includes a labeled failure case. Explain the symptom, scope, and recovery; for real infrastructure, do not induce outages without an approved disposable environment.

## Lessons and exercises

| Lesson | Focus | Executable foundation |
|---|---|---|
| [19.01-llm-capabilities-and-limitations](lessons/19.01-llm-capabilities-and-limitations.md) | LLM capabilities and limitations | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-19.py` and answer topic questions |
| [19.02-rag-for-runbooks-and-incidents](lessons/19.02-rag-for-runbooks-and-incidents.md) | RAG for runbooks and incidents | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-19.py` and answer topic questions |
| [19.03-tool-calling-agents-and-permissions](lessons/19.03-tool-calling-agents-and-permissions.md) | Tool-calling agents and permissions | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-19.py` and answer topic questions |
| [19.04-prompt-and-context-design](lessons/19.04-prompt-and-context-design.md) | Prompt and context design | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-19.py` and answer topic questions |
| [19.05-human-in-the-loop-operations](lessons/19.05-human-in-the-loop-operations.md) | Human-in-the-loop operations | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-19.py` and answer topic questions |
| [19.06-read-only-diagnosis-before-write-actions](lessons/19.06-read-only-diagnosis-before-write-actions.md) | Read-only diagnosis before write actions | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-19.py` and answer topic questions |
| [19.07-evaluation-datasets-and-grounded-answers](lessons/19.07-evaluation-datasets-and-grounded-answers.md) | Evaluation datasets and grounded answers | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-19.py` and answer topic questions |
| [19.08-prompt-injection-and-tool-output-trust](lessons/19.08-prompt-injection-and-tool-output-trust.md) | Prompt injection and tool-output trust | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-19.py` and answer topic questions |
| [19.09-auditability-and-rollback](lessons/19.09-auditability-and-rollback.md) | Auditability and rollback | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-19.py` and answer topic questions |
| [19.10-ai-assisted-incident-summarization](lessons/19.10-ai-assisted-incident-summarization.md) | AI-assisted incident summarization | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-19.py` and answer topic questions |
| [19.11-cost-and-latency-controls](lessons/19.11-cost-and-latency-controls.md) | Cost and latency controls | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-19.py` and answer topic questions |

## Production application exercise

1. Inspect relevant current Todo files and record exact paths; use the real source as the authority.
2. Draw a component diagram showing request path, state boundary, and failure domain.
3. State which features exist now and which are only proposed.
4. Create a small spec and ADR before changing Todo; validate with CI and a rollback plan.
5. Add evidence to [learning log](../../progress/LEARNING_LOG.md).

## Completion gate

A module is complete only after its individual topic questions are answered and at least one actual Todo-related lab has independently verified evidence. Running the common module experiment alone does **not** complete all lessons.
