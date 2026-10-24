# Module 10 — Kubernetes Fundamentals

**Status:** Not started  
**Scope:** Pods, Deployments, Services, ConfigMaps, Secrets and probes  
**Outcome:** Deploy stateless Todo API experiments to a local Kubernetes cluster.

> This handbook is a **guided curriculum**. Example commands and future architecture are not proof that features exist in the current branch. Inspect repository code and dependencies before execution.

## Why this matters to an SRE/DevOps Architect

An architect must be able to explain the user-facing behavior, identify the operational boundary where it can fail, and justify design decisions under reliability, security, cost, and complexity constraints. This module practices those skills using the Todo application rather than disconnected toy systems.

## Prerequisites and environment

- Clone and check out the **active Todo learning branch**; use `git status --short` before modifying anything.
- Read [environment setup](../../labs/ENVIRONMENT_SETUP.md) and the [architecture baseline](../../architecture/CURRENT_AND_TARGET.md).
- Confirm the actual source files and API routes; do not assume a future service is already implemented.
- Keep experimental code in `tutorials/` or a disposable working directory until a spec-driven implementation PR is approved.

## Lessons

| Lesson | Topic | Evidence to collect |
|---|---|---|
| 10.01 | Control plane and worker nodes | Explanation, observed output, and one failure mode |
| 10.02 | Pods and container lifecycle | Explanation, observed output, and one failure mode |
| 10.03 | Deployments and ReplicaSets | Explanation, observed output, and one failure mode |
| 10.04 | Services and DNS | Explanation, observed output, and one failure mode |
| 10.05 | Namespaces and labels | Explanation, observed output, and one failure mode |
| 10.06 | ConfigMaps and Secrets | Explanation, observed output, and one failure mode |
| 10.07 | Resource requests and limits | Explanation, observed output, and one failure mode |
| 10.08 | Liveness, readiness, startup probes | Explanation, observed output, and one failure mode |
| 10.09 | kubectl describe and logs | Explanation, observed output, and one failure mode |
| 10.10 | Rolling updates and rollback | Explanation, observed output, and one failure mode |
| 10.11 | Persistent storage introduction | Explanation, observed output, and one failure mode |

## Lesson method — use for every row above

**1. Explain.** Define the topic and what problem it solves. State which guarantees it does *not* provide.  
**2. Trace.** Find the actual relevant Todo source/configuration and sketch the path from user action to dependency.  
**3. Inspect.** Record the command or browser observation proving the current behavior.  
**4. Experiment.** Make one small reversible change or run a disposable simulation.  
**5. Break safely.** Introduce one bounded failure and collect symptoms, logs, and status codes.  
**6. Decide.** Compare at least two designs using reliability, operational burden, security, and cost.  
**7. Record.** Use the lab template, update the learning log, and capture an ADR for a consequential decision.

## Architecture reasoning exercise

**Scenario:** {outcome}

Draw a diagram showing the **client**, **component under study**, **external dependencies**, **stateful data**, and **failure boundary**. Mark which components can be restarted independently and which data must survive restarts.

Questions to answer before implementation:

1. What is the user-visible success criterion?
2. Which dependency failure can break it?
3. What evidence distinguishes application failure from network or configuration failure?
4. Which behavior should be synchronous, asynchronous, retried, or rejected?
5. What would you measure in production, and what is the rollback strategy?

## Guided hands-on lab — baseline

**Goal:** {outcome}

**Run from the Todo repository root unless a command changes directories.** Check your working tree and ensure disposable resources are used.

```bash
{commands}
```

### Observe

- Capture process/HTTP/test output or the diagram produced by the lab.
- Note the difference between **expected behavior** and **observed behavior**.
- Record the current git branch and relevant file paths.
- Redact tokens, personal data, cloud IDs, and secret values.

### Failure-injection lab

{failure}

**Recovery:** Undo only your own disposable changes, restore the service, rerun the healthy-path check, and record whether the outcome returned to baseline.

### Expected learning outcome

{outcome}

## Development → DevOps → Architecture connection

| Lens | Questions to answer |
|---|---|
| Development | Which functions, contracts, and tests implement this behavior? |
| DevOps | Which process, configuration, network path, artifact, or automation operates it? |
| SRE | What breaks, how is it detected, and how quickly can it recover? |
| Architecture | What alternatives exist, what trade-offs matter, and why is this design justified? |

## Design caution

**{caveat}**

## Verification and exit criteria

- [ ] Explain all lesson topics in your own words.
- [ ] Show the relevant actual code/configuration or clearly label a hypothetical design.
- [ ] Complete the healthy-path lab with output.
- [ ] Simulate and diagnose one reversible failure.
- [ ] Restore service and verify recovery.
- [ ] Document one trade-off and one security consideration.
- [ ] Update `progress/LEARNING_LOG.md` with evidence and next lesson.

## Suggested SDD deliverable

If this module results in a Todo feature change, prepare a **small** feature specification, implementation plan, tasks, contract changes, automated tests, and rollback notes. Use existing `.specify/` conventions. Do not automatically install or deploy the technologies described in this handbook.

## Tutor handoff prompt

```text
Read tutorials/sre-devops-architect-handbook/modules/{i:02}-{slug}/README.md
and inspect the actual Todo repository on my current branch.
Resume at Lesson {i:02}.01 (or the next incomplete lesson in progress/LEARNING_LOG.md).
Teach one lesson only: concept, real code, architecture, commands, safe failure lab,
expected observations, and a brief check for understanding. Wait for my results.
Do not assume unimplemented infrastructure exists.
```
