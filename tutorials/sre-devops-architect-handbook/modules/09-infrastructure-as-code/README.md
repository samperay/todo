# Module 09 — Infrastructure As Code (Handbook v5)

**Purpose:** Learn infrastructure as code through small Python experiments and Todo code inspection.  
**Baseline lab:** [`module-09.py`](../../labs/module-experiments/module-09.py)  
**Status:** Planned/guided; no module is complete until individual exercises are verified.

## V4 learning companion: analogy, concept and observations

Each linked lesson now includes **1. Real-world analogy**, **2. Understanding the core concept** (for `03.02`, **Understanding `queue.Queue`**), and **4. What to Observe**. These sections supplement the existing explanations, commands, expected outputs, failure labs and knowledge checks; they do not replace them.

**Start here:** Open the first lesson in the table below, read the new sections, run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-09.py --lesson NN.MM` (substitute that lesson's actual ID), and record the observed results. The shared module experiment is not proof of every lesson's real-world technology.

## Start here

From the repository root:

```bash
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-09.py --list
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-09.py
```

Run only one lesson at a time. `--lesson NN.MM` prints the lesson focus and executes the shared module demonstration. **The shared demonstration is a foundation, not a separate full implementation for every topic.** The Markdown lesson adds the topic-specific inspection, discussion and architecture review.

## Lessons

| Lesson | Command |
|---|---|
| [09.01 — declarative infrastructure](lessons/09.01-declarative-infrastructure.md) | `python3 .../module-09.py --lesson 09.01` |
| [09.02 — terraform providers and resources](lessons/09.02-terraform-providers-and-resources.md) | `python3 .../module-09.py --lesson 09.02` |
| [09.03 — variables outputs locals](lessons/09.03-variables-outputs-locals.md) | `python3 .../module-09.py --lesson 09.03` |
| [09.04 — state and state locking](lessons/09.04-state-and-state-locking.md) | `python3 .../module-09.py --lesson 09.04` |
| [09.05 — plan apply destroy lifecycle](lessons/09.05-plan-apply-destroy-lifecycle.md) | `python3 .../module-09.py --lesson 09.05` |
| [09.06 — remote state and encryption](lessons/09.06-remote-state-and-encryption.md) | `python3 .../module-09.py --lesson 09.06` |
| [09.07 — modules and composition](lessons/09.07-modules-and-composition.md) | `python3 .../module-09.py --lesson 09.07` |
| [09.08 — environment separation](lessons/09.08-environment-separation.md) | `python3 .../module-09.py --lesson 09.08` |
| [09.09 — drift detection](lessons/09.09-drift-detection.md) | `python3 .../module-09.py --lesson 09.09` |
| [09.10 — least privilege for automation](lessons/09.10-least-privilege-for-automation.md) | `python3 .../module-09.py --lesson 09.10` |
| [09.11 — policy checks and cost awareness](lessons/09.11-policy-checks-and-cost-awareness.md) | `python3 .../module-09.py --lesson 09.11` |

## Completion gate

For each lesson: understand the concept, inspect actual Todo code, run the lab, discuss a failure/recovery, and record the output. Infrastructure experiments are offline models unless explicitly labeled otherwise.

## V5 study protocol

Open each linked lesson and complete **Beginner → Intermediate → Architect**. Each lesson contains the complete code and expected observations; the shared `module-NN.py` is only an optional baseline. Tutor: reference the lesson path and ask for actual output; do not paste the lesson into chat.

## Canonical roadmap technology tracks

- [Terraform and cloud architecture — Learn → Integrate → Operate](technologies/terraform-cloud/README.md)

## Technology track: Terraform and cloud

Start with [Terraform and cloud — Learn → Integrate → Operate](technologies/terraform-cloud/README.md).
