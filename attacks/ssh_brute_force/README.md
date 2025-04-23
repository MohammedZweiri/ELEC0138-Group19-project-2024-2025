# SSH brute force Attack

## Mitigation

1. Using the `fail2ban` software

2. To install and run `fail2ban`:
```
sudo apt update && sudo apt upgrade
sudo apt-get install fail2ban
sudo systemctl enable fail2ban.service

```

3. Check status
```
sudo fail2ban-client status
sudo fail2ban-client status sshd
```