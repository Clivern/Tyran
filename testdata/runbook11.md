## Application Deployment Failure

### PagerDuty Alert

```
[CRITICAL] Application Deployment Failure on app-server-07
Host: app-server-07.example.com
Deployment ID: 12345
Error: Build failed
```

### Runbook

1. SSH into the application server:
   ```
   ssh user@app-server-07.example.com
   ```

2. Check deployment logs for errors:
   ```
   tail -n 100 /var/log/deployments/deployment-12345.log
   ```

3. Verify build dependencies and environment:
   ```
   env | grep BUILD
   ```

4. Re-run the deployment script:
   ```
   /usr/local/bin/deploy_script.sh 12345
   ```
