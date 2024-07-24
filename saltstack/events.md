# Configuring Events

Example, monitor the 'kubelet' Systemd service.

## 1. Create a beacon on the minion

```bash
sudo vim /etc/salt/minion.d/beacons.conf
```

```yaml 
beacons:
  service:
    - kubelet:
        running: False
        interval: 10  # Check every 10 seconds
```

This configuration tells the beacon to check the status of the kubelet service  
every 10 seconds. If the service is not running, it will trigger an event.

```bash
sudo systemctl restart salt-minion
```

To see events as they occur(Equivalent to tail -F a log file):
```bash
salt-run state.event pretty=true
```

## 2. Reacting to events

Create a new reactor file on the Salt master, for example,  
/srv/reactor/kubelet_monitor.sls:

```bash
sudo mkdir -p /srv/reactor
sudo vim /srv/reactor/kubelet_monitor.sls
```

Add Reactor Configuration:
```yaml
kubelet_down:
  salt.state:
    - tgt: {{ data['id'] }}
    - sls: kubelet.restart # The state file to be executed.
```

This configuration will trigger the state kubelet.restart when the kubelet  
service goes down.

Create the State File:
Create the state file that will be executed when the kubelet goes down. 
For example, /srv/salt/kubelet.restart.sls:
```bash
sudo vim /srv/salt/kubelet.restart.sls
```

Add the following content to restart the kubelet service:
```yaml
restart_kubelet:
  service.running:
    - name: kubelet
    - enable: True
    - watch:
      - service: kubelet
```

Configure the Reactor in the Master Configuration:
Edit the Salt master configuration file (/etc/salt/master) to include the reactor:
```yaml
reactor:
  - 'salt/beacon/*/service/kubelet':
    - salt://reactor/kubelet_monitor.sls
```

Restart the Salt Master:
```bash
sudo systemctl restart salt-master
```
