## Unauthorized Access Attempt

### PagerDuty Alert

```
[WARNING] Unauthorized Access Attempt on auth-server-02
Host: auth-server-02.example.com
IP Address: 192.168.1.100
Attempts: 5
```

### Runbook

1. SSH into the affected server:
   ```
   ssh user@auth-server-02.example.com
   ```

2. Check authentication logs for unauthorized access attempts:
   ```
   grep "192.168.1.100" /var/log/auth.log
   ```

3. Block the offending IP address:
   ```
   sudo iptables -A INPUT -s 192.168.1.100 -j DROP
   ```

4. Consider updating firewall rules or enabling fail2ban for automated protection.
