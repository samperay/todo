# Module 01 — Application Architecture Fundamentals (Handbook v5)

**Purpose:** Learn application architecture fundamentals through small Python experiments and Todo code inspection.  
**Baseline lab:** [`module-01.py`](../../labs/module-experiments/module-01.py)  
**Status:** Planned/guided; no module is complete until individual exercises are verified.

## V4 learning companion: analogy, concept and observations

Each linked lesson now includes **1. Real-world analogy**, **2. Understanding the core concept** (for `03.02`, **Understanding `queue.Queue`**), and **4. What to Observe**. These sections supplement the existing explanations, commands, expected outputs, failure labs and knowledge checks; they do not replace them.

**Start here:** Open the first lesson in the table below, read the new sections, run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-01.py --lesson NN.MM` (substitute that lesson's actual ID), and record the observed results. The shared module experiment is not proof of every lesson's real-world technology.

## Start here

From the repository root:

```bash
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-01.py --list
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-01.py
```

Run only one lesson at a time. `--lesson NN.MM` prints the lesson focus and executes the shared module demonstration. **The shared demonstration is a foundation, not a separate full implementation for every topic.** The Markdown lesson adds the topic-specific inspection, discussion and architecture review.

## Lessons

| Lesson | Command |
|---|---|
| [01.01 — application boundaries and responsibilities](lessons/01.01-application-boundaries-and-responsibilities.md) | `python3 .../module-01.py --lesson 01.01` |
| [01.02 — react bootstrap main tsx](lessons/01.02-react-bootstrap-main-tsx.md) | `python3 .../module-01.py --lesson 01.02` |
| [01.03 — component composition app tsx](lessons/01.03-component-composition-app-tsx.md) | `python3 .../module-01.py --lesson 01.03` |
| [01.04 — development servers and ports](lessons/01.04-development-servers-and-ports.md) | `python3 .../module-01.py --lesson 01.04` |
| [01.05 — TCP listeners and process trees](lessons/01.05-tcp-listeners-and-process-trees.md) | `python3 .../module-01.py --lesson 01.05` |
| [01.06 — HTTP status codes and headers](lessons/01.06-http-status-codes-and-headers.md) | `python3 .../module-01.py --lesson 01.06` |
| [01.07 — vite proxy and same origin routing](lessons/01.07-vite-proxy-and-same-origin-routing.md) | `python3 .../module-01.py --lesson 01.07` |
| [01.08 — bearer authentication request path](lessons/01.08-bearer-authentication-request-path.md) | `python3 .../module-01.py --lesson 01.08` |
| [01.09 — dependency failure and 502 diagnosis](lessons/01.09-dependency-failure-and-502-diagnosis.md) | `python3 .../module-01.py --lesson 01.09` |
| [01.10 — architecture diagrams and adrs](lessons/01.10-architecture-diagrams-and-adrs.md) | `python3 .../module-01.py --lesson 01.10` |

## Completion gate

For each lesson: understand the concept, inspect actual Todo code, run the lab, discuss a failure/recovery, and record the output. Infrastructure experiments are offline models unless explicitly labeled otherwise.

## V5 study protocol

Open each linked lesson and complete **Beginner → Intermediate → Architect**. Each lesson contains the complete code and expected observations; the shared `module-NN.py` is only an optional baseline. Tutor: reference the lesson path and ask for actual output; do not paste the lesson into chat.
