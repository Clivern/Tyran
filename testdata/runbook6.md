## Network Interface Down

### PagerDuty Alert

```
[CRITICAL] Network Interface Down on router-01
Host: router-01.example.com
Interface: eth0
Status: DOWN
```

### Runbook

1. SSH into the affected router:
   ```
   ssh user@router-01.example.com
   ```

2. Check network interface status:
   ```
   ip link show
   ```

3. Attempt to bring the interface up:
   ```
   sudo ip link set eth0 up
   ```

4. Check system logs for network-related errors:
   ```
   journalctl -u networking.service
   ```
