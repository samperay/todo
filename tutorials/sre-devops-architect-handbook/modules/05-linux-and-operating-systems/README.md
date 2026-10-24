# Module 05 — Linux And Operating Systems (Handbook v3)

**Purpose:** Learn linux and operating systems through small Python experiments and Todo code inspection.  
**Baseline lab:** [`module-05.py`](../../labs/module-experiments/module-05.py)  
**Status:** Planned/guided; no module is complete until individual exercises are verified.

## V4 learning companion: analogy, concept and observations

Each linked lesson now includes **1. Real-world analogy**, **2. Understanding the core concept** (for `03.02`, **Understanding `queue.Queue`**), and **4. What to Observe**. These sections supplement the existing explanations, commands, expected outputs, failure labs and knowledge checks; they do not replace them.

**Start here:** Open the first lesson in the table below, read the new sections, run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-05.py --lesson NN.MM` (substitute that lesson's actual ID), and record the observed results. The shared module experiment is not proof of every lesson's real-world technology.

## Start here

From the repository root:

```bash
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-05.py --list
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-05.py
```

Run only one lesson at a time. `--lesson NN.MM` prints the lesson focus and executes the shared module demonstration. **The shared demonstration is a foundation, not a separate full implementation for every topic.** The Markdown lesson adds the topic-specific inspection, discussion and architecture review.

## Lessons

| Lesson | Command |
|---|---|
| [05.01 — process lifecycle pid and ppid](lessons/05.01-process-lifecycle-pid-and-ppid.md) | `python3 .../module-05.py --lesson 05.01` |
| [05.02 — signals graceful termination](lessons/05.02-signals-graceful-termination.md) | `python3 .../module-05.py --lesson 05.02` |
| [05.03 — file descriptors and sockets](lessons/05.03-file-descriptors-and-sockets.md) | `python3 .../module-05.py --lesson 05.03` |
| [05.04 — cpu memory and i o fundamentals](lessons/05.04-cpu-memory-and-i-o-fundamentals.md) | `python3 .../module-05.py --lesson 05.04` |
| [05.05 — users groups permissions umask](lessons/05.05-users-groups-permissions-umask.md) | `python3 .../module-05.py --lesson 05.05` |
| [05.06 — systemd unit files and journald](lessons/05.06-systemd-unit-files-and-journald.md) | `python3 .../module-05.py --lesson 05.06` |
| [05.07 — environment and startup configuration](lessons/05.07-environment-and-startup-configuration.md) | `python3 .../module-05.py --lesson 05.07` |
| [05.08 — resource limits and oom behavior](lessons/05.08-resource-limits-and-oom-behavior.md) | `python3 .../module-05.py --lesson 05.08` |
| [05.09 — disk and filesystem troubleshooting](lessons/05.09-disk-and-filesystem-troubleshooting.md) | `python3 .../module-05.py --lesson 05.09` |
| [05.10 — shell automation and runbooks](lessons/05.10-shell-automation-and-runbooks.md) | `python3 .../module-05.py --lesson 05.10` |

## Completion gate

For each lesson: understand the concept, inspect actual Todo code, run the lab, discuss a failure/recovery, and record the output. Infrastructure experiments are offline models unless explicitly labeled otherwise.
