# Module 05 — Linux And Operating Systems

**Scope:** Linux processes and signals.  
**Status:** Guided learning; verify evidence before marking complete.

## Why it matters

This module connects the running Todo application with **Linux And Operating Systems**. Begin with a dependency-free simulation, then investigate the actual application or local infrastructure. A simulated result is not evidence of a deployed production capability.

## Prerequisites

- Python 3, Git, Todo repository checked out on the intended branch.
- Read [environment setup](../../labs/ENVIRONMENT_SETUP.md) and [architecture baseline](../../architecture/CURRENT_AND_TARGET.md).
- Optional infrastructure tools are introduced only when their lessons require them.

## Baseline lab — executable

From the Todo repository root:

```bash
pwd
git status --short
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-05.py
```

**Expected:** A successful baseline observation plus a bounded failure/recovery demonstration for **Linux processes and signals**. The experiment does not modify Todo application code. A `SKIP` line means a prerequisite is absent; do not report the corresponding infrastructure as tested.

**Failure:** The experiment includes a labeled failure case. Explain the symptom, scope, and recovery; for real infrastructure, do not induce outages without an approved disposable environment.

## Lessons and exercises

| Lesson | Focus | Executable foundation |
|---|---|---|
| [05.01-process-lifecycle-pid-and-ppid](lessons/05.01-process-lifecycle-pid-and-ppid.md) | Process lifecycle, PID and PPID | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-05.py` and answer topic questions |
| [05.02-signals-graceful-termination](lessons/05.02-signals-graceful-termination.md) | Signals, graceful termination | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-05.py` and answer topic questions |
| [05.03-file-descriptors-and-sockets](lessons/05.03-file-descriptors-and-sockets.md) | File descriptors and sockets | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-05.py` and answer topic questions |
| [05.04-cpu-memory-and-i-o-fundamentals](lessons/05.04-cpu-memory-and-i-o-fundamentals.md) | CPU, memory, and I/O fundamentals | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-05.py` and answer topic questions |
| [05.05-users-groups-permissions-umask](lessons/05.05-users-groups-permissions-umask.md) | Users, groups, permissions, umask | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-05.py` and answer topic questions |
| [05.06-systemd-unit-files-and-journald](lessons/05.06-systemd-unit-files-and-journald.md) | systemd unit files and journald | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-05.py` and answer topic questions |
| [05.07-environment-and-startup-configuration](lessons/05.07-environment-and-startup-configuration.md) | Environment and startup configuration | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-05.py` and answer topic questions |
| [05.08-resource-limits-and-oom-behavior](lessons/05.08-resource-limits-and-oom-behavior.md) | Resource limits and OOM behavior | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-05.py` and answer topic questions |
| [05.09-disk-and-filesystem-troubleshooting](lessons/05.09-disk-and-filesystem-troubleshooting.md) | Disk and filesystem troubleshooting | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-05.py` and answer topic questions |
| [05.10-shell-automation-and-runbooks](lessons/05.10-shell-automation-and-runbooks.md) | Shell automation and runbooks | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-05.py` and answer topic questions |

## Production application exercise

1. Inspect relevant current Todo files and record exact paths; use the real source as the authority.
2. Draw a component diagram showing request path, state boundary, and failure domain.
3. State which features exist now and which are only proposed.
4. Create a small spec and ADR before changing Todo; validate with CI and a rollback plan.
5. Add evidence to [learning log](../../progress/LEARNING_LOG.md).

## Completion gate

A module is complete only after its individual topic questions are answered and at least one actual Todo-related lab has independently verified evidence. Running the common module experiment alone does **not** complete all lessons.
