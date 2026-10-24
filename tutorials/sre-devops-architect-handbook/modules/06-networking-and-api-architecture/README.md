# Module 06 — Networking And Api Architecture (Handbook v3)

**Purpose:** Learn networking and api architecture through small Python experiments and Todo code inspection.  
**Baseline lab:** [`module-06.py`](../../labs/module-experiments/module-06.py)  
**Status:** Planned/guided; no module is complete until individual exercises are verified.

## V4 learning companion: analogy, concept and observations

Each linked lesson now includes **1. Real-world analogy**, **2. Understanding the core concept** (for `03.02`, **Understanding `queue.Queue`**), and **4. What to Observe**. These sections supplement the existing explanations, commands, expected outputs, failure labs and knowledge checks; they do not replace them.

**Start here:** Open the first lesson in the table below, read the new sections, run `python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-06.py --lesson NN.MM` (substitute that lesson's actual ID), and record the observed results. The shared module experiment is not proof of every lesson's real-world technology.

## Start here

From the repository root:

```bash
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-06.py --list
python3 tutorials/sre-devops-architect-handbook/labs/module-experiments/module-06.py
```

Run only one lesson at a time. `--lesson NN.MM` prints the lesson focus and executes the shared module demonstration. **The shared demonstration is a foundation, not a separate full implementation for every topic.** The Markdown lesson adds the topic-specific inspection, discussion and architecture review.

## Lessons

| Lesson | Command |
|---|---|
| [06.01 — TCP handshake and ports](lessons/06.01-tcp-handshake-and-ports.md) | `python3 .../module-06.py --lesson 06.01` |
| [06.02 — loopback versus bind all addresses](lessons/06.02-loopback-versus-bind-all-addresses.md) | `python3 .../module-06.py --lesson 06.02` |
| [06.03 — dns resolution and caching](lessons/06.03-dns-resolution-and-caching.md) | `python3 .../module-06.py --lesson 06.03` |
| [06.04 — HTTP methods headers and status](lessons/06.04-http-methods-headers-and-status.md) | `python3 .../module-06.py --lesson 06.04` |
| [06.05 — TLS certificates and trust chains](lessons/06.05-tls-certificates-and-trust-chains.md) | `python3 .../module-06.py --lesson 06.05` |
| [06.06 — reverse proxies and upstreams](lessons/06.06-reverse-proxies-and-upstreams.md) | `python3 .../module-06.py --lesson 06.06` |
| [06.07 — cors and same origin policy](lessons/06.07-cors-and-same-origin-policy.md) | `python3 .../module-06.py --lesson 06.07` |
| [06.08 — API gateways and rate limiting](lessons/06.08-api-gateways-and-rate-limiting.md) | `python3 .../module-06.py --lesson 06.08` |
| [06.09 — load balanCIng and health checks](lessons/06.09-load-balancing-and-health-checks.md) | `python3 .../module-06.py --lesson 06.09` |
| [06.10 — network failure diagnostics](lessons/06.10-network-failure-diagnostics.md) | `python3 .../module-06.py --lesson 06.10` |
| [06.11 — request traCIng across hops](lessons/06.11-request-tracing-across-hops.md) | `python3 .../module-06.py --lesson 06.11` |

## Completion gate

For each lesson: understand the concept, inspect actual Todo code, run the lab, discuss a failure/recovery, and record the output. Infrastructure experiments are offline models unless explicitly labeled otherwise.
