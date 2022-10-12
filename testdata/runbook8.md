## High Load Average

### PagerDuty Alert

```
[WARNING] High Load Average on compute-node-06
Host: compute-node-06.example.com
Load Average: 15.0
Threshold: 10.0
```

### Runbook

1. SSH into the affected server:
   ```
   ssh user@compute-node-06.example.com
   ```

2. Check the current load average:
   ```
   uptime
   ```

3. Identify processes causing high load:
   ```
   top -o %CPU
   ```

4. Consider redistributing workloads or adding more resources to the server.
