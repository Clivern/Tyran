## Service Unavailable

### PagerDuty Alert

```
[CRITICAL] Service Unavailable on api-server-04
Host: api-server-04.example.com
Service: API Gateway
Error: 503 Service Unavailable
```

### Runbook

1. SSH into the affected server:
   ```
   ssh user@api-server-04.example.com
   ```

2. Check the status of the API service:
   ```
   systemctl status nginx
   ```

3. Restart the service if it's down:
   ```
   sudo systemctl restart nginx
   ```

4. Check application logs for errors:
   ```
   tail -n 100 /var/log/nginx/error.log
   ```
