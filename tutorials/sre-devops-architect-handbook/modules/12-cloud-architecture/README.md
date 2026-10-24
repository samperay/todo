# Module 12 — Cloud Architecture

**Scope:** Cloud architecture offline reliability model.  
**Status:** Guided learning; verify evidence before marking complete.

## Why it matters

This module connects the running Todo application with **Cloud Architecture**. Begin with a dependency-free simulation, then investigate the actual application or local infrastructure. A simulated result is not evidence of a deployed production capability.

## Prerequisites

- Python 3, Git, Todo repository checked out on the intended branch.
- Read [environment setup](../../labs/ENVIRONMENT_SETUP.md) and [architecture baseline](../../architecture/CURRENT_AND_TARGET.md).
- Optional infrastructure tools are introduced only when their lessons require them.

## Baseline lab — executable

From the Todo repository root:

```bash
pwd
git status --short
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-12.py
```

**Expected:** A successful baseline observation plus a bounded failure/recovery demonstration for **Cloud architecture offline reliability model**. The experiment does not modify Todo application code. A `SKIP` line means a prerequisite is absent; do not report the corresponding infrastructure as tested.

**Failure:** The experiment includes a labeled failure case. Explain the symptom, scope, and recovery; for real infrastructure, do not induce outages without an approved disposable environment.

## Lessons and exercises

| Lesson | Focus | Executable foundation |
|---|---|---|
| [12.01-regions-availability-zones-and-failure-domains](lessons/12.01-regions-availability-zones-and-failure-domains.md) | Regions, availability zones and failure domains | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-12.py` and answer topic questions |
| [12.02-vpc-and-subnet-design](lessons/12.02-vpc-and-subnet-design.md) | VPC and subnet design | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-12.py` and answer topic questions |
| [12.03-routing-nat-and-firewalls](lessons/12.03-routing-nat-and-firewalls.md) | Routing, NAT and firewalls | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-12.py` and answer topic questions |
| [12.04-iam-identities-and-least-privilege](lessons/12.04-iam-identities-and-least-privilege.md) | IAM identities and least privilege | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-12.py` and answer topic questions |
| [12.05-compute-selection-vms-containers-serverless](lessons/12.05-compute-selection-vms-containers-serverless.md) | Compute selection: VMs, containers, serverless | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-12.py` and answer topic questions |
| [12.06-managed-database-trade-offs](lessons/12.06-managed-database-trade-offs.md) | Managed database trade-offs | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-12.py` and answer topic questions |
| [12.07-object-storage-and-backup](lessons/12.07-object-storage-and-backup.md) | Object storage and backup | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-12.py` and answer topic questions |
| [12.08-load-balancers-and-dns](lessons/12.08-load-balancers-and-dns.md) | Load balancers and DNS | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-12.py` and answer topic questions |
| [12.09-secrets-and-key-management](lessons/12.09-secrets-and-key-management.md) | Secrets and key management | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-12.py` and answer topic questions |
| [12.10-cost-and-tagging](lessons/12.10-cost-and-tagging.md) | Cost and tagging | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-12.py` and answer topic questions |
| [12.11-well-architected-review](lessons/12.11-well-architected-review.md) | Well-architected review | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-12.py` and answer topic questions |

## Production application exercise

1. Inspect relevant current Todo files and record exact paths; use the real source as the authority.
2. Draw a component diagram showing request path, state boundary, and failure domain.
3. State which features exist now and which are only proposed.
4. Create a small spec and ADR before changing Todo; validate with CI and a rollback plan.
5. Add evidence to [learning log](../../progress/LEARNING_LOG.md).

## Completion gate

A module is complete only after its individual topic questions are answered and at least one actual Todo-related lab has independently verified evidence. Running the common module experiment alone does **not** complete all lessons.
