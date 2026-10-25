# Module 16 — Security And Devsecops (Handbook v5)

**Purpose:** Learn security and devsecops through small Python experiments and Todo code inspection.  
**Baseline lab:** [`module-16.py`](../../labs/module-experiments/module-16.py)  
**Status:** Planned/guided; no module is complete until individual exercises are verified.

## V4 learning companion: analogy, concept and observations

Each linked lesson now includes **1. Real-world analogy**, **2. Understanding the core concept** (for `03.02`, **Understanding `queue.Queue`**), and **4. What to Observe**. These sections supplement the existing explanations, commands, expected outputs, failure labs and knowledge checks; they do not replace them.

**Start here:** Open the first lesson in the table below, read the new sections, run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-16.py --lesson NN.MM` (substitute that lesson's actual ID), and record the observed results. The shared module experiment is not proof of every lesson's real-world technology.

## Start here

From the repository root:

```bash
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-16.py --list
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-16.py
```

Run only one lesson at a time. `--lesson NN.MM` prints the lesson focus and executes the shared module demonstration. **The shared demonstration is a foundation, not a separate full implementation for every topic.** The Markdown lesson adds the topic-specific inspection, discussion and architecture review.

## Lessons

| Lesson | Command |
|---|---|
| [16.01 — threat modeling and trust boundaries](lessons/16.01-threat-modeling-and-trust-boundaries.md) | `python3 .../module-16.py --lesson 16.01` |
| [16.02 — authentication versus authorization](lessons/16.02-authentication-versus-authorization.md) | `python3 .../module-16.py --lesson 16.02` |
| [16.03 — bearer token risks and localstorage](lessons/16.03-bearer-token-risks-and-localstorage.md) | `python3 .../module-16.py --lesson 16.03` |
| [16.04 — TLS and certificate validation](lessons/16.04-tls-and-certificate-validation.md) | `python3 .../module-16.py --lesson 16.04` |
| [16.05 — root and intermediate cas](lessons/16.05-root-and-intermediate-cas.md) | `python3 .../module-16.py --lesson 16.05` |
| [16.06 — secrets lifecycle and rotation](lessons/16.06-secrets-lifecycle-and-rotation.md) | `python3 .../module-16.py --lesson 16.06` |
| [16.07 — dependency vulnerability scanning](lessons/16.07-dependency-vulnerability-scanning.md) | `python3 .../module-16.py --lesson 16.07` |
| [16.08 — sbom and image provenance](lessons/16.08-sbom-and-image-provenance.md) | `python3 .../module-16.py --lesson 16.08` |
| [16.09 — least privilege and rbac](lessons/16.09-least-privilege-and-rbac.md) | `python3 .../module-16.py --lesson 16.09` |
| [16.10 — input validation and abuse prevention](lessons/16.10-input-validation-and-abuse-prevention.md) | `python3 .../module-16.py --lesson 16.10` |
| [16.11 — audit logging and inCIdent response](lessons/16.11-audit-logging-and-incident-response.md) | `python3 .../module-16.py --lesson 16.11` |

## Completion gate

For each lesson: understand the concept, inspect actual Todo code, run the lab, discuss a failure/recovery, and record the output. Infrastructure experiments are offline models unless explicitly labeled otherwise.

## V5 study protocol

Open each linked lesson and complete **Beginner → Intermediate → Architect**. Each lesson contains the complete code and expected observations; the shared `module-NN.py` is only an optional baseline. Tutor: reference the lesson path and ask for actual output; do not paste the lesson into chat.

## Canonical roadmap technology tracks

- [Keycloak and OIDC — Learn → Integrate → Operate](technologies/keycloak-oidc/README.md)

## Technology track: Keycloak and OIDC

Start with [Keycloak and OIDC — Learn → Integrate → Operate](technologies/keycloak-oidc/README.md).
