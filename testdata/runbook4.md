## Database Connection Failure

### PagerDuty Alert

```
[CRITICAL] Database Connection Failure on app-server-02
Host: app-server-02.example.com
Database: main_production
Error: Connection refused
```

### Runbook

1. SSH into the database server:
   ```
   ssh user@db-server.example.com
   ```

2. Check if the database service is running:
   ```
   systemctl status postgresql
   ```

3. If not running, start the service:
   ```
   sudo systemctl start postgresql
   ```

4. Check database logs for errors:
   ```
   tail -n 100 /var/log/postgresql/postgresql-main.log
   ```