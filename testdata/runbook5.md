## High Memory Usage

### PagerDuty Alert

```
[WARNING] High Memory Usage on cache-server-05
Host: cache-server-05.example.com
Memory Usage: 92%
Threshold: 85%
```

### Runbook

1. SSH into the affected server:
   ```
   ssh user@cache-server-05.example.com
   ```

2. Check memory usage:
   ```
   free -m
   ```

3. Identify top memory-consuming processes:
   ```
   ps aux --sort=-%mem | head -n 10
   ```

4. If it's a cache server, consider clearing some cache:
   ```
   redis-cli flushall
   ```
