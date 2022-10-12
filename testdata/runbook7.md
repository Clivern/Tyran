## Failed Backup Job

### PagerDuty Alert

```
[CRITICAL] Backup Job Failed on backup-server-01
Host: backup-server-01.example.com
Job: daily_full_backup
Error: Insufficient disk space
```

### Runbook

1. SSH into the backup server:
   ```
   ssh user@backup-server-01.example.com
   ```

2. Check available disk space:
   ```
   df -h
   ```

3. If necessary, clean up old backups:
   ```
   find /backups -type f -mtime +30 -delete
   ```

4. Manually trigger the backup job:
   ```
   /usr/local/bin/backup_script.sh
   ```

5. Monitor the backup process and check logs:
   ```
   tail -f /var/log/backup.log
   ```
