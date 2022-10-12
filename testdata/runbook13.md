## Temperature Threshold Exceeded

### PagerDuty Alert

```
[CRITICAL] Temperature Threshold Exceeded on server-room-01
Host: server-room-01.example.com
Temperature: 85°F
Threshold: 75°F
```

### Runbook

1. SSH into the affected server:
   ```
   ssh user@server-room-01.example.com
   ```

2. Check temperature sensors:
   ```
   sensors
   ```

3. Ensure cooling systems are operational:
   - Verify air conditioning units are running.
   - Check for obstructions in airflow.

4. If necessary, power down non-critical systems to reduce heat.
