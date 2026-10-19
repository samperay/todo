# Lab 02 — Prometheus alerting and Alertmanager

## Step 1: Add a rule file

Create `observability/alerts.yml` **in your local Todo repository**:

```yaml
groups:
  - name: todo-api
    interval: 15s
    rules:
      - alert: TodoAPIScrapeFailed
        expr: up{job="todo-api"} == 0
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Todo API metrics target is not scrapeable"
          description: "Verify container, /metrics endpoint, and Docker network"
```

Mount this file into the Prometheus container and add its container path to `rule_files` in `prometheus.yml`; exact paths depend on your current Compose layout. Validate before restart:

```bash
# If promtool is installed locally:
promtool check rules observability/alerts.yml
# Then restart/reload Prometheus according to your actual configuration.
```

Check the Prometheus **Rules** and **Alerts** pages. `for: 2m` means two minutes elapsed since the alert became pending, not two successful evaluations.

## Step 2: Trigger safely

```bash
docker compose stop todo-api
```

Wait for a failed scrape, then watch `up{job="todo-api"}` and alert states. After testing:

```bash
docker compose start todo-api
```

Verify recovery and the alert returning to inactive. If the target disappears from discovery altogether, `up==0` may not fire; consider `absent(up{job="todo-api"})` where appropriate.

## Step 3: Add Alertmanager (extension)

Add an Alertmanager service, mount a minimal config, and configure Prometheus `alerting.alertmanagers`. Begin with a **non-delivering test receiver**; only later add a dedicated Slack test channel using an injected secret. Never commit a Slack webhook or send simulated incidents to operational channels.

## Independent exercise

Add a sustained high-5xx-rate rule with a traffic minimum. Explain why low-volume ratios can be noisy.

## Incident challenge

An alert is pending for two evaluations then recovers before `for` elapses. Should a notification fire? Prove your answer from timestamps and rule evaluation interval.
