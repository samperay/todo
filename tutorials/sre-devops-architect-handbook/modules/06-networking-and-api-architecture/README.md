# Module 06 — Networking And Api Architecture

**Scope:** DNS, sockets and TCP failures.  
**Status:** Guided learning; verify evidence before marking complete.

## Why it matters

This module connects the running Todo application with **Networking And Api Architecture**. Begin with a dependency-free simulation, then investigate the actual application or local infrastructure. A simulated result is not evidence of a deployed production capability.

## Prerequisites

- Python 3, Git, Todo repository checked out on the intended branch.
- Read [environment setup](../../labs/ENVIRONMENT_SETUP.md) and [architecture baseline](../../architecture/CURRENT_AND_TARGET.md).
- Optional infrastructure tools are introduced only when their lessons require them.

## Baseline lab — executable

From the Todo repository root:

```bash
pwd
git status --short
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-06.py
```

**Expected:** A successful baseline observation plus a bounded failure/recovery demonstration for **DNS, sockets and TCP failures**. The experiment does not modify Todo application code. A `SKIP` line means a prerequisite is absent; do not report the corresponding infrastructure as tested.

**Failure:** The experiment includes a labeled failure case. Explain the symptom, scope, and recovery; for real infrastructure, do not induce outages without an approved disposable environment.

## Lessons and exercises

| Lesson | Focus | Executable foundation |
|---|---|---|
| [06.01-tcp-handshake-and-ports](lessons/06.01-tcp-handshake-and-ports.md) | TCP handshake and ports | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-06.py` and answer topic questions |
| [06.02-loopback-versus-bind-all-addresses](lessons/06.02-loopback-versus-bind-all-addresses.md) | Loopback versus bind-all addresses | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-06.py` and answer topic questions |
| [06.03-dns-resolution-and-caching](lessons/06.03-dns-resolution-and-caching.md) | DNS resolution and caching | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-06.py` and answer topic questions |
| [06.04-http-methods-headers-and-status](lessons/06.04-http-methods-headers-and-status.md) | HTTP methods, headers and status | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-06.py` and answer topic questions |
| [06.05-tls-certificates-and-trust-chains](lessons/06.05-tls-certificates-and-trust-chains.md) | TLS certificates and trust chains | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-06.py` and answer topic questions |
| [06.06-reverse-proxies-and-upstreams](lessons/06.06-reverse-proxies-and-upstreams.md) | Reverse proxies and upstreams | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-06.py` and answer topic questions |
| [06.07-cors-and-same-origin-policy](lessons/06.07-cors-and-same-origin-policy.md) | CORS and same-origin policy | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-06.py` and answer topic questions |
| [06.08-api-gateways-and-rate-limiting](lessons/06.08-api-gateways-and-rate-limiting.md) | API gateways and rate limiting | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-06.py` and answer topic questions |
| [06.09-load-balancing-and-health-checks](lessons/06.09-load-balancing-and-health-checks.md) | Load balancing and health checks | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-06.py` and answer topic questions |
| [06.10-network-failure-diagnostics](lessons/06.10-network-failure-diagnostics.md) | Network failure diagnostics | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-06.py` and answer topic questions |
| [06.11-request-tracing-across-hops](lessons/06.11-request-tracing-across-hops.md) | Request tracing across hops | Run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-06.py` and answer topic questions |

## Production application exercise

1. Inspect relevant current Todo files and record exact paths; use the real source as the authority.
2. Draw a component diagram showing request path, state boundary, and failure domain.
3. State which features exist now and which are only proposed.
4. Create a small spec and ADR before changing Todo; validate with CI and a rollback plan.
5. Add evidence to [learning log](../../progress/LEARNING_LOG.md).

## Completion gate

A module is complete only after its individual topic questions are answered and at least one actual Todo-related lab has independently verified evidence. Running the common module experiment alone does **not** complete all lessons.
