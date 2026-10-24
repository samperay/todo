# Module 07 — Containerization

**Scope:** Container runtime inspection.  
**Status:** Guided learning; verify evidence before marking complete.

## Why it matters

This module connects the running Todo application with **Containerization**. Begin with a dependency-free simulation, then investigate the actual application or local infrastructure. A simulated result is not evidence of a deployed production capability.

## Prerequisites

- Python 3, Git, Todo repository checked out on the intended branch.
- Read [environment setup](../../labs/ENVIRONMENT_SETUP.md) and [architecture baseline](../../architecture/CURRENT_AND_TARGET.md).
- Optional infrastructure tools are introduced only when their lessons require them.

## Baseline lab — executable

From the Todo repository root:

```bash
pwd
git status --short
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-07.py
```

**Expected:** A successful baseline observation plus a bounded failure/recovery demonstration for **Container runtime inspection**. The experiment does not modify Todo application code. A `SKIP` line means a prerequisite is absent; do not report the corresponding infrastructure as tested.

**Failure:** The experiment includes a labeled failure case. Explain the symptom, scope, and recovery; for real infrastructure, do not induce outages without an approved disposable environment.

## Lessons and exercises

| Lesson | Focus | Executable foundation |
|---|---|---|
| [07.01-containers-versus-virtual-machines](lessons/07.01-containers-versus-virtual-machines.md) | Containers versus virtual machines | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-07.py` and answer topic questions |
| [07.02-dockerfile-layers-and-build-cache](lessons/07.02-dockerfile-layers-and-build-cache.md) | Dockerfile layers and build cache | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-07.py` and answer topic questions |
| [07.03-multi-stage-react-build](lessons/07.03-multi-stage-react-build.md) | Multi-stage React build | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-07.py` and answer topic questions |
| [07.04-fastapi-container-image](lessons/07.04-fastapi-container-image.md) | FastAPI container image | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-07.py` and answer topic questions |
| [07.05-port-publishing-and-container-dns](lessons/07.05-port-publishing-and-container-dns.md) | Port publishing and container DNS | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-07.py` and answer topic questions |
| [07.06-compose-services-and-networks](lessons/07.06-compose-services-and-networks.md) | Compose services and networks | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-07.py` and answer topic questions |
| [07.07-volumes-and-sqlite-persistence](lessons/07.07-volumes-and-sqlite-persistence.md) | Volumes and SQLite persistence | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-07.py` and answer topic questions |
| [07.08-environment-variables-and-secrets](lessons/07.08-environment-variables-and-secrets.md) | Environment variables and secrets | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-07.py` and answer topic questions |
| [07.09-health-checks-and-startup-dependencies](lessons/07.09-health-checks-and-startup-dependencies.md) | Health checks and startup dependencies | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-07.py` and answer topic questions |
| [07.10-image-scanning-and-non-root-users](lessons/07.10-image-scanning-and-non-root-users.md) | Image scanning and non-root users | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-07.py` and answer topic questions |
| [07.11-container-debugging-and-logs](lessons/07.11-container-debugging-and-logs.md) | Container debugging and logs | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-07.py` and answer topic questions |

## Production application exercise

1. Inspect relevant current Todo files and record exact paths; use the real source as the authority.
2. Draw a component diagram showing request path, state boundary, and failure domain.
3. State which features exist now and which are only proposed.
4. Create a small spec and ADR before changing Todo; validate with CI and a rollback plan.
5. Add evidence to [learning log](../../progress/LEARNING_LOG.md).

## Completion gate

A module is complete only after its individual topic questions are answered and at least one actual Todo-related lab has independently verified evidence. Running the common module experiment alone does **not** complete all lessons.
