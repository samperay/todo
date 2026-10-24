# Module 16 — Security And Devsecops

**Scope:** Secrets and least privilege.  
**Status:** Guided learning; verify evidence before marking complete.

## Why it matters

This module connects the running Todo application with **Security And Devsecops**. Begin with a dependency-free simulation, then investigate the actual application or local infrastructure. A simulated result is not evidence of a deployed production capability.

## Prerequisites

- Python 3, Git, Todo repository checked out on the intended branch.
- Read [environment setup](../../labs/ENVIRONMENT_SETUP.md) and [architecture baseline](../../architecture/CURRENT_AND_TARGET.md).
- Optional infrastructure tools are introduced only when their lessons require them.

## Baseline lab — executable

From the Todo repository root:

```bash
pwd
git status --short
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-16.py
```

**Expected:** A successful baseline observation plus a bounded failure/recovery demonstration for **Secrets and least privilege**. The experiment does not modify Todo application code. A `SKIP` line means a prerequisite is absent; do not report the corresponding infrastructure as tested.

**Failure:** The experiment includes a labeled failure case. Explain the symptom, scope, and recovery; for real infrastructure, do not induce outages without an approved disposable environment.

## Lessons and exercises

| Lesson | Focus | Executable foundation |
|---|---|---|
| [16.01-threat-modeling-and-trust-boundaries](lessons/16.01-threat-modeling-and-trust-boundaries.md) | Threat modeling and trust boundaries | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-16.py` and answer topic questions |
| [16.02-authentication-versus-authorization](lessons/16.02-authentication-versus-authorization.md) | Authentication versus authorization | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-16.py` and answer topic questions |
| [16.03-bearer-token-risks-and-localstorage](lessons/16.03-bearer-token-risks-and-localstorage.md) | Bearer-token risks and localStorage | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-16.py` and answer topic questions |
| [16.04-tls-and-certificate-validation](lessons/16.04-tls-and-certificate-validation.md) | TLS and certificate validation | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-16.py` and answer topic questions |
| [16.05-root-and-intermediate-cas](lessons/16.05-root-and-intermediate-cas.md) | Root and intermediate CAs | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-16.py` and answer topic questions |
| [16.06-secrets-lifecycle-and-rotation](lessons/16.06-secrets-lifecycle-and-rotation.md) | Secrets lifecycle and rotation | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-16.py` and answer topic questions |
| [16.07-dependency-vulnerability-scanning](lessons/16.07-dependency-vulnerability-scanning.md) | Dependency vulnerability scanning | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-16.py` and answer topic questions |
| [16.08-sbom-and-image-provenance](lessons/16.08-sbom-and-image-provenance.md) | SBOM and image provenance | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-16.py` and answer topic questions |
| [16.09-least-privilege-and-rbac](lessons/16.09-least-privilege-and-rbac.md) | Least privilege and RBAC | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-16.py` and answer topic questions |
| [16.10-input-validation-and-abuse-prevention](lessons/16.10-input-validation-and-abuse-prevention.md) | Input validation and abuse prevention | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-16.py` and answer topic questions |
| [16.11-audit-logging-and-incident-response](lessons/16.11-audit-logging-and-incident-response.md) | Audit logging and incident response | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-16.py` and answer topic questions |

## Production application exercise

1. Inspect relevant current Todo files and record exact paths; use the real source as the authority.
2. Draw a component diagram showing request path, state boundary, and failure domain.
3. State which features exist now and which are only proposed.
4. Create a small spec and ADR before changing Todo; validate with CI and a rollback plan.
5. Add evidence to [learning log](../../progress/LEARNING_LOG.md).

## Completion gate

A module is complete only after its individual topic questions are answered and at least one actual Todo-related lab has independently verified evidence. Running the common module experiment alone does **not** complete all lessons.
