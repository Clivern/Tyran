## DNS Resolution Failure

### PagerDuty Alert

```
[CRITICAL] DNS Resolution Failure on dns-server-01
Host: dns-server-01.example.com
Domain: example.com
Error: NXDOMAIN
```

### Runbook

1. SSH into the DNS server:
   ```
   ssh user@dns-server-01.example.com
   ```

2. Check DNS service status:
   ```
   systemctl status named
   ```

3. Restart the DNS service if necessary:
   ```
   sudo systemctl restart named
   ```

4. Check DNS configuration files for errors:
   ```
   named-checkconf
   named-checkzone example.com /var/named/example.com.zone
   ```
