# Module 07 — Containerization (Handbook v3)

**Purpose:** Learn containerization through small Python experiments and Todo code inspection.  
**Baseline lab:** [`module-07.py`](../../labs/module-experiments/module-07.py)  
**Status:** Planned/guided; no module is complete until individual exercises are verified.

## V4 learning companion: analogy, concept and observations

Each linked lesson now includes **1. Real-world analogy**, **2. Understanding the core concept** (for `03.02`, **Understanding `queue.Queue`**), and **4. What to Observe**. These sections supplement the existing explanations, commands, expected outputs, failure labs and knowledge checks; they do not replace them.

**Start here:** Open the first lesson in the table below, read the new sections, run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-07.py --lesson NN.MM` (substitute that lesson's actual ID), and record the observed results. The shared module experiment is not proof of every lesson's real-world technology.

## Start here

From the repository root:

```bash
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-07.py --list
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-07.py
```

Run only one lesson at a time. `--lesson NN.MM` prints the lesson focus and executes the shared module demonstration. **The shared demonstration is a foundation, not a separate full implementation for every topic.** The Markdown lesson adds the topic-specific inspection, discussion and architecture review.

## Lessons

| Lesson | Command |
|---|---|
| [07.01 — containers versus virtual machines](lessons/07.01-containers-versus-virtual-machines.md) | `python3 .../module-07.py --lesson 07.01` |
| [07.02 — dockerfile layers and build cache](lessons/07.02-dockerfile-layers-and-build-cache.md) | `python3 .../module-07.py --lesson 07.02` |
| [07.03 — multi stage react build](lessons/07.03-multi-stage-react-build.md) | `python3 .../module-07.py --lesson 07.03` |
| [07.04 — fastAPI container image](lessons/07.04-fastapi-container-image.md) | `python3 .../module-07.py --lesson 07.04` |
| [07.05 — port publishing and container dns](lessons/07.05-port-publishing-and-container-dns.md) | `python3 .../module-07.py --lesson 07.05` |
| [07.06 — compose services and networks](lessons/07.06-compose-services-and-networks.md) | `python3 .../module-07.py --lesson 07.06` |
| [07.07 — volumes and SQLite persistence](lessons/07.07-volumes-and-sqlite-persistence.md) | `python3 .../module-07.py --lesson 07.07` |
| [07.08 — environment variables and secrets](lessons/07.08-environment-variables-and-secrets.md) | `python3 .../module-07.py --lesson 07.08` |
| [07.09 — health checks and startup dependenCIes](lessons/07.09-health-checks-and-startup-dependencies.md) | `python3 .../module-07.py --lesson 07.09` |
| [07.10 — image scanning and non root users](lessons/07.10-image-scanning-and-non-root-users.md) | `python3 .../module-07.py --lesson 07.10` |
| [07.11 — container debugging and logs](lessons/07.11-container-debugging-and-logs.md) | `python3 .../module-07.py --lesson 07.11` |

## Completion gate

For each lesson: understand the concept, inspect actual Todo code, run the lab, discuss a failure/recovery, and record the output. Infrastructure experiments are offline models unless explicitly labeled otherwise.
