

# 1. Bootstrap the Master


```bash
# Install master and minion services
./bootstrap-salt.sh -M

# Install master and minion services, plus specify that saltmaster is 'localhost'
# Otherwise, it looks for 'salt' in dns entries.
./bootstrap-salt.sh -M -A localhost

# Install just the Master service.
./bootstrap-salt.sh -M -N
```

# 2. Bootstrap the Minion

```bash
# Create minion(Will look for 'salt' in dns entries)
./bootstrap-salt.sh

# Specify a custom Master host
./bootstrap-salt.sh -A mysaltmaster
```

# 3. Accept minion keys
After you have created your minions and the key is cached, don't forget to 
accept the keys on the master.

```bash
# Look at keys.
sudo salt-key -L

# Accept all the keys.
sudo salt-key -A
```

# 4. Test your install

```bash
sudo salt '*' test.ping
```

