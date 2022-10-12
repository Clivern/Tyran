## SSL Certificate Expiration

### PagerDuty Alert

```
[WARNING] SSL Certificate Expiring Soon on loadbalancer-02
Host: loadbalancer-02.example.com
Domain: www.example.com
Days until expiration: 7
```

### Runbook

1. SSH into the load balancer:
   ```
   ssh user@loadbalancer-02.example.com
   ```

2. Check the SSL certificate expiration date:
   ```
   openssl x509 -in /etc/ssl/certs/example.com.crt -noout -dates
   ```

3. Generate a new Certificate Signing Request (CSR):
   ```
   openssl req -new -key /etc/ssl/private/example.com.key -out example.com.csr
   ```

4. Submit the CSR to your Certificate Authority and follow their process to obtain a new certificate.
