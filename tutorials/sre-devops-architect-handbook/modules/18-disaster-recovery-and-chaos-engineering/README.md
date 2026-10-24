# Module 18 — Disaster Recovery And Chaos Engineering

**Scope:** Recovery point and time objectives.  
**Status:** Guided learning; verify evidence before marking complete.

## Why it matters

This module connects the running Todo application with **Disaster Recovery And Chaos Engineering**. Begin with a dependency-free simulation, then investigate the actual application or local infrastructure. A simulated result is not evidence of a deployed production capability.

## Prerequisites

- Python 3, Git, Todo repository checked out on the intended branch.
- Read [environment setup](../../labs/ENVIRONMENT_SETUP.md) and [architecture baseline](../../architecture/CURRENT_AND_TARGET.md).
- Optional infrastructure tools are introduced only when their lessons require them.

## Baseline lab — executable

From the Todo repository root:

```bash
pwd
git status --short
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-18.py
```

**Expected:** A successful baseline observation plus a bounded failure/recovery demonstration for **Recovery point and time objectives**. The experiment does not modify Todo application code. A `SKIP` line means a prerequisite is absent; do not report the corresponding infrastructure as tested.

**Failure:** The experiment includes a labeled failure case. Explain the symptom, scope, and recovery; for real infrastructure, do not induce outages without an approved disposable environment.

## Lessons and exercises

| Lesson | Focus | Executable foundation |
|---|---|---|
| [18.01-backup-versus-replication](lessons/18.01-backup-versus-replication.md) | Backup versus replication | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-18.py` and answer topic questions |
| [18.02-rpo-and-rto-definitions](lessons/18.02-rpo-and-rto-definitions.md) | RPO and RTO definitions | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-18.py` and answer topic questions |
| [18.03-sqlite-consistent-backup-practices](lessons/18.03-sqlite-consistent-backup-practices.md) | SQLite consistent backup practices | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-18.py` and answer topic questions |
| [18.04-restore-verification](lessons/18.04-restore-verification.md) | Restore verification | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-18.py` and answer topic questions |
| [18.05-failure-modes-and-blast-radius](lessons/18.05-failure-modes-and-blast-radius.md) | Failure modes and blast radius | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-18.py` and answer topic questions |
| [18.06-dependency-mapping](lessons/18.06-dependency-mapping.md) | Dependency mapping | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-18.py` and answer topic questions |
| [18.07-fault-injection-hypotheses](lessons/18.07-fault-injection-hypotheses.md) | Fault-injection hypotheses | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-18.py` and answer topic questions |
| [18.08-graceful-shutdown-and-recovery](lessons/18.08-graceful-shutdown-and-recovery.md) | Graceful shutdown and recovery | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-18.py` and answer topic questions |
| [18.09-disaster-runbooks](lessons/18.09-disaster-runbooks.md) | Disaster runbooks | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-18.py` and answer topic questions |
| [18.10-game-days-and-incident-learning](lessons/18.10-game-days-and-incident-learning.md) | Game days and incident learning | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-18.py` and answer topic questions |

## Production application exercise

1. Inspect relevant current Todo files and record exact paths; use the real source as the authority.
2. Draw a component diagram showing request path, state boundary, and failure domain.
3. State which features exist now and which are only proposed.
4. Create a small spec and ADR before changing Todo; validate with CI and a rollback plan.
5. Add evidence to [learning log](../../progress/LEARNING_LOG.md).

## Completion gate

A module is complete only after its individual topic questions are answered and at least one actual Todo-related lab has independently verified evidence. Running the common module experiment alone does **not** complete all lessons.
