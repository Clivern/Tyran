## High CPU Usage Alert

### PagerDuty Alert

```
[CRITICAL] High CPU Usage on web-server-01
Host: web-server-01.example.com
CPU Usage: 95%
Threshold: 80%
```

### Runbook

1. SSH into the affected server:
   ```
   ssh user@web-server-01.example.com
   ```

2. Check top processes consuming CPU:
   ```
   top -o %CPU
   ```

3. Identify and kill any runaway processes if necessary:
   ```
   kill -15 <PID>
   ```

4. If it's a web server, check for high traffic and consider scaling:
   ```
   tail -f /var/log/nginx/access.log | awk '{print $1}' | sort | uniq -c | sort -nr | head -n 10
   ```
