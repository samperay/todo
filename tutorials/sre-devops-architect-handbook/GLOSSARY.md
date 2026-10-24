# Glossary

- **API gateway:** Policy and routing entry point for APIs; may provide authentication, rate limits, and routing.
- **Backoff:** Increasing wait between retries to reduce pressure during transient failure.
- **Circuit breaker:** Stops calls to an unhealthy dependency for a period and probes for recovery.
- **Dead-letter queue:** Destination for messages that cannot be processed under the defined retry policy.
- **Durability:** Whether acknowledged data survives defined failure conditions.
- **Idempotency:** Repeating an operation has the same intended effect as doing it once.
- **Liveness:** Whether a component should be considered alive and restarted if not.
- **Readiness:** Whether a component should receive traffic now.
- **Outbox:** Database table storing events atomically with business-state changes for later publication.
- **RPO:** Maximum tolerable data loss measured in time.
- **RTO:** Maximum tolerable time to restore a service.
- **SLI:** Measured indicator of service quality.
- **SLO:** Target value for an SLI over a defined window.
- **Stateless service:** Does not depend on per-client request history retained in the service process to handle a request.
- **Timeout:** A caller's maximum wait; does not guarantee the callee canceled its work.
- **Trust boundary:** Point where assumptions about identity, privileges, or input validation change.
