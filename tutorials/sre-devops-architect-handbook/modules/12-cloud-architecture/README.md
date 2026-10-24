# Module 12 — Cloud Architecture (Handbook v5)

**Purpose:** Learn cloud architecture through small Python experiments and Todo code inspection.  
**Baseline lab:** [`module-12.py`](../../labs/module-experiments/module-12.py)  
**Status:** Planned/guided; no module is complete until individual exercises are verified.

## V4 learning companion: analogy, concept and observations

Each linked lesson now includes **1. Real-world analogy**, **2. Understanding the core concept** (for `03.02`, **Understanding `queue.Queue`**), and **4. What to Observe**. These sections supplement the existing explanations, commands, expected outputs, failure labs and knowledge checks; they do not replace them.

**Start here:** Open the first lesson in the table below, read the new sections, run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-12.py --lesson NN.MM` (substitute that lesson's actual ID), and record the observed results. The shared module experiment is not proof of every lesson's real-world technology.

## Start here

From the repository root:

```bash
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-12.py --list
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-12.py
```

Run only one lesson at a time. `--lesson NN.MM` prints the lesson focus and executes the shared module demonstration. **The shared demonstration is a foundation, not a separate full implementation for every topic.** The Markdown lesson adds the topic-specific inspection, discussion and architecture review.

## Lessons

| Lesson | Command |
|---|---|
| [12.01 — regions availability zones and failure domains](lessons/12.01-regions-availability-zones-and-failure-domains.md) | `python3 .../module-12.py --lesson 12.01` |
| [12.02 — vpc and subnet design](lessons/12.02-vpc-and-subnet-design.md) | `python3 .../module-12.py --lesson 12.02` |
| [12.03 — routing nat and firewalls](lessons/12.03-routing-nat-and-firewalls.md) | `python3 .../module-12.py --lesson 12.03` |
| [12.04 — iam identities and least privilege](lessons/12.04-iam-identities-and-least-privilege.md) | `python3 .../module-12.py --lesson 12.04` |
| [12.05 — compute selection vms containers serverless](lessons/12.05-compute-selection-vms-containers-serverless.md) | `python3 .../module-12.py --lesson 12.05` |
| [12.06 — managed database trade offs](lessons/12.06-managed-database-trade-offs.md) | `python3 .../module-12.py --lesson 12.06` |
| [12.07 — object storage and backup](lessons/12.07-object-storage-and-backup.md) | `python3 .../module-12.py --lesson 12.07` |
| [12.08 — load balancers and dns](lessons/12.08-load-balancers-and-dns.md) | `python3 .../module-12.py --lesson 12.08` |
| [12.09 — secrets and key management](lessons/12.09-secrets-and-key-management.md) | `python3 .../module-12.py --lesson 12.09` |
| [12.10 — cost and tagging](lessons/12.10-cost-and-tagging.md) | `python3 .../module-12.py --lesson 12.10` |
| [12.11 — well architected review](lessons/12.11-well-architected-review.md) | `python3 .../module-12.py --lesson 12.11` |

## Completion gate

For each lesson: understand the concept, inspect actual Todo code, run the lab, discuss a failure/recovery, and record the output. Infrastructure experiments are offline models unless explicitly labeled otherwise.

## V5 study protocol

Open each linked lesson and complete **Beginner → Intermediate → Architect**. Each lesson contains the complete code and expected observations; the shared `module-NN.py` is only an optional baseline. Tutor: reference the lesson path and ask for actual output; do not paste the lesson into chat.
