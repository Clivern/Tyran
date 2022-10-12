## Disk Space Critical

### PagerDuty Alert

```
[CRITICAL] Low Disk Space on db-server-03
Host: db-server-03.example.com
Available Space: 2%
Threshold: 10%
```

### Runbook

1. SSH into the affected server:
   ```
   ssh user@db-server-03.example.com
   ```

2. Check disk usage:
   ```
   df -h
   ```

3. Identify large files and directories:
   ```
   du -sh /* | sort -rh | head -n 10
   ```

4. Remove unnecessary files or compress logs:
   ```
   find /var/log -name "*.log" -mtime +30 -delete
   ```
