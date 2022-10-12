## Email Delivery Failure

### PagerDuty Alert

```
[WARNING] Email Delivery Failure on mail-server-01
Host: mail-server-01.example.com
Error: Connection timed out
```

### Runbook

1. SSH into the mail server:
   ```
   ssh user@mail-server-01.example.com
   ```

2. Check the mail service status:
   ```
   systemctl status postfix
   ```

3. Restart the mail service if necessary:
   ```
   sudo systemctl restart postfix
   ```

4. Check mail logs for errors:
   ```
   tail -n 100 /var/log/mail.log
   ```
