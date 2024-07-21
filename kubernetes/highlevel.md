
# Keywords

* OCI(Open Container Initiative)  
  Implemented by both Podman and Docker.

* CE(Container Engine)  

* Load balancer  
  Used to route traffic to the correct location. 
  i.e. if you had a redundant container service up somewhere and the primary goes
  down, then traffic swaps to the secondary until the primary comes back up.

* Kubectl  
  Tool you can install anywhere to talk to the Master of the Kubernetes cluster.

* Kubelet  
  Runs ontop of Kube-proxy, used by the master to control the CE daemon.

* Pod  
  Runs somewhere in the K8s cluster, smallest deployable unit in K8s, can
  contain one or more containers. Containers in a pod communicate via localhost
  versus container name DNS in docker-compose, so they appear as one big 
  container.
  K8s provides persistent volumes(automatically provisioned) instead of regular
  volumes.

* Deployment/manifest file  
  Yaml similar to a docker-compose file.  It can describe one or more pods. 
  You use kubctl to 'apply' your manifest.  If you want to change the state of 
  your containers, i.e. increase replication, just update the manifest and
  reapply it.
          

# Architecture

* Master node Stack
  - Kubernetes API Server
  - Scheduler
  - Controller Manager
  - etcd

* Worker node Stack(In order of OSI model prevalence)
  - kubelet
  - kube-proxy
  - OCI CE
  - OS
  - Hardware

# Podman and Kubernetes

IF you don't have a Kubernetes cluster, you can still run Kubernetes manifest
files using Podman!

```bash
# Bring it up
podman kube play ./manifest.yml

# Bring it down
podman kube down ./manifest.yml
```

This is a great way to practice writing manifest files.


# Bootstrapping


## Tools

- kubeadm
- kubelet

Install kubeadm and kubelet on each system.


# Load balancing

We deploy a higher level object called a 'Service' which is load balanced across
all the replicated pods for that service.

Example: my-service.yaml
```yaml
apiVersion: v1
kind: Service
metadata:
  name: myservice
  annotations:
    service.beta.kubernetes.io/linode-loadbalancer-throttle: "4"
  labels:
    app: myservice
spec:
  type: LoadBalancer
  ports:
  - name: http
    port: 80
    protocol: TCP
    targetPort: 80
  selector:
    app: pod_name # This tells it to load balance across ANY pod with this app label.
  sessionAffinity: None
```
```bash
kubectl apply -f my-service.yaml
kubectl get services # It's similar to doing 'podman ps' but across all your nodes!
```

# Commands
```bash
kubectl get nodes
kubectl cluster-info

# Ad-HOC create a pod
kubectl run _podman_name --image=docker.io/_image_name --port=80
kubectl get pods
kubectl get pods -o wide # more details
kubectl describe pods

kubectl apply -f _your_manifest.yml # kind: deployment
kubectl apply -f my-service.yaml # kind: service. Apply service on the pod
kubectl edit deployment _your_manifest # From the 'name:' field of your deployment.
                                       # If you need to edit the manifest on-the-fly.
kubectl get services
kubectl describe services

kubectl delete pods _podman_name
```


# Cliffnotes

Setup basic node(Worker and Master)
```bash
sudo apt install docker.io
sudo swapoff -a
sudo vim /etc/fstab # comment /swap

# Ref: https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/
sudo apt-get update
# apt-transport-https may be a dummy package; if so, you can skip that package
sudo apt-get install -y apt-transport-https ca-certificates curl gpg
# If the directory `/etc/apt/keyrings` does not exist, it should be created before the curl command, read the note below.
# sudo mkdir -p -m 755 /etc/apt/keyrings
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.30/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
# This overwrites any existing configuration in /etc/apt/sources.list.d/kubernetes.list
echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.30/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list
sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl
sudo systemctl enable --now kubelet

# Install api key for your user
sudo mkdir -p ~/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $USER:$USER $HOME/.kube/config

```

Setup MASTER
```bash
sudo kubeadm init

# Setup cluster to use a DNS entry rather than IP.
sudo kubeadm init --control-plane-endpoint=cluster.example.com
# Add additional SubjectAlternativeNames(SAN's) to the server certificate.
sudo kubeadm init --apiserver-cert-extra-sans=cluster.example.com,alternate.example.com
```

Setup Worker
```bash
# Copy the kubeadm join command from the init command on master and run it on
# the worker
```



Querying the cluster:
If you don't add this config file to your user, then you will get localhost:8080
api failures.
```bash
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
```


# OFFLINE Installer builder

## Docs
https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/

## Oracle Linux 8.9
```bash
sudo setenforce 0

# This overwrites any existing configuration in /etc/yum.repos.d/kubernetes.repo
cat <<EOF | sudo tee /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://pkgs.k8s.io/core:/stable:/v1.30/rpm/
enabled=1
gpgcheck=1
gpgkey=https://pkgs.k8s.io/core:/stable:/v1.30/rpm/repodata/repomd.xml.key
exclude=kubelet kubeadm kubectl cri-tools kubernetes-cni
EOF

mkdir ./k8s_offline_packages
sudo yum install --downloadonly --downloaddir=./k8s_offline_packages -y kubelet kubeadm kubectl --disableexcludes=kubernetes


# Get containerd
wget https://github.com/containerd/containerd/releases/download/v1.7.19/containerd-1.7.19-linux-amd64.tar.gz
# Get service file
wget https://raw.githubusercontent.com/containerd/containerd/main/containerd.service # Will be saved to /usr/local/lib/systemd/system/containerd.service
```

Move your bundle to the offline system.

```bash

tar Cxzvf /usr/local containerd-1.7.19-linux-amd64.tar.gz
# Move the service file to: /usr/local/lib/systemd/system/containerd.service

cd ./k8s_offline_packages
sudo rpm -ivh *.rpm # OR, try yum install -y *.rpm

# Verify install
rpm -qa | grep -E 'kube'

# Firewall settings
# IF firewalld is active, please ensure ports [6443 10250] are open or your cluster may not function correctly
sudo firewall-cmd --permanent --add-port=6443/tcp # MASTER only
sudo firewall-cmd --permanent --add-port=10250/tcp # ALL
sudo firewall-cmd --add-masquerade --permanent # ALL
# Maybe? sudo firewall-cmd --permanent --add-port=8472/udp # ALL
sudo firewall-cmd --reload

# Enable IP forwarding if it's not on
cat /etc/sysctl.conf
echo "net.ipv4.ip_forward=1" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p


systemctl daemon-reload
systemctl enable --now containerd
sudo systemctl enable --now kubelet
sudo systemctl start kubelet

```

On master
``` bash
kubeadm init

# Deploy networking(Super Important)
kubectl apply -f https://docs.projectcalico.org/manifests/calico.yaml

# Monitor node health
kubectl get pods -n kube-system

# Dont forget to set your admin.conf for your user after done.
# or export KUBECONFIG=/etc/kubernetes/admin.conf
```


On worker
```bash

# Configure Cgroups Ref: https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/configure-cgroup-driver/


kube join ...
```

# Container runtime
Defined by environment variable in:
```
/var/lib/kubelet/kubeadm-flags.env
```

## Issues I encountered
* Localhost:8080
  Issue is caused by not installing admin.config in your ~/.kube/

* Nameserver issue(Too many tries)
  Caused by having too many nameservers configured.  Google this. But,
  remove a few nameservers to fix <= 3 MAX nameservers.

* Containers in Not-Ready state OR can't find CNI config on kubelet status
  You need to deploy container networking.
  ```bash
  kubectl apply -f https://docs.projectcalico.org/manifests/calico.yaml
  ```

* Cgroups issues
  * Cgroups setup issue
    Need to deploy with systemd init config.
    `sudo cat /var/lib/kubelet/config.yaml`

    ```yaml
    # kubeadm-config.yaml
    kind: ClusterConfiguration
    apiVersion: kubeadm.k8s.io/v1beta3
    kubernetesVersion: v1.30.2
    ---
    kind: KubeletConfiguration
    apiVersion: kubelet.config.k8s.io/v1beta1
    cgroupDriver: systemd
    ```

    ```bash
    kube init --config kubeadm-config.yaml
    ```

    And do the below

    * container-runtime-endpoint address
      Containerd issue, need to properly setup the Cgroups.
      https://kubernetes.io/docs/setup/production-environment/container-runtimes/#containerd-systemd

      Create containerd default config and edit it:
      ```bash
      containerd config default > /etc/containerd/config.toml
      vim /etc/containerd/config.toml
      # Set
      # [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc.options]
      #   SystemdCgroup = true
      ```
  * Containerd fails to find container hash or something
    ```bash
    # 1. Stop kubelet
    systemctl stop kubelet
    # 2. Stop containerd
    # Remove the containerd state
    rm -rf /var/lib/containerd
    systemctl start kubelet
    ```

  * Port not avail on Master
  https://docs.oracle.com/en/operating-systems/oracle-linux/kubernetes/kubernetes_install_upgrade.html#2.4-Setting-Up-a-Worker-Node

    * Verify DNS is working(Most likely issue)
      ```bash
      kubectl run -it --rm --restart=Never busybox --image=busybox:1.28 -- nslookup kubernetes.default
      ```

      Should see something like the following output:
      ```bash
      Server:    10.96.0.10
      Address 1: 10.96.0.10 kube-dns.kube-system.svc.cluster.local

      Name:      kubernetes.default
      Address 1: 10.96.0.1 kubernetes.default.svc.cluster.local
      ```

      Check port :53 DNS resolve
      ```bash
      $ sudo ss -tulpn | grep :53
      udp   UNCONN 0      0                             127.0.0.54:53         0.0.0.0:*    users:(("systemd-resolve",pid=645,fd=16))
      udp   UNCONN 0      0                          127.0.0.53%lo:53         0.0.0.0:*    users:(("systemd-resolve",pid=645,fd=14))
      tcp   LISTEN 0      4096                          127.0.0.54:53         0.0.0.0:*    users:(("systemd-resolve",pid=645,fd=17))
      tcp   LISTEN 0      4096                       127.0.0.53%lo:53         0.0.0.0:*    users:(("systemd-resolve",pid=645,fd=15))
      ```

      Should be running on ALL nodes:
      `systemctl status systemd-resolved`


    * Ensure Firewall is not blocking
      Even if your'e using localhost, firewall may still block.
      ```bash
      sudo firewall-cmd --permanent --add-port=30080/tcp
      sudo firewall-cmd --permanent --add-port=30080/udp
      ```

    * Check ip tables for the port:
      ```bash
      sudo iptables -t nat -L -n -v | grep 30080
      # 1    60 KUBE-EXT-URTTJQXLPCG6M7ZS  6    --  *      *       0.0.0.0/0            0.0.0.0/0            /* default/python-http-service */ tcp dpt:30080
      ```

    * Try disabling SELinux
      ```bash
      setenforce 0

      sudo vi /etc/selinux/config
      # Find the line that says "SELINUX=enforcing" and change it to:
      # text
      #SELINUX=Permissive
      ```
    * Connection refused on port 6443

      FIRST, verify that the kube-apiserver is running.
      It might be crashing.
      ```bash
      ps -ef | grep apiserver
      sudo crictl logs $(sudo crictl ps -q --name kube-apiserver)
      kubectl get pods -n kube-system
      ```

      Try replacing .kube/config
      ```bash
      rm -rf ~/.kube
      mkdir ~/.kube
      sudo cp /etc/kubernetes/admin.conf ~/.kube/config
      sudo chown -R $USER:$USER ~/.kube
        
      ```

      Renew certs on the master and nodes.
      ```bash
      sudo kubeadm certs renew all
      ```


# Example deployment

Manifest
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: python-http-server
spec:
  replicas: 1
  selector:
    matchLabels:
      app: python-http-server
  template:
    metadata:
      labels:
        app: python-http-server
    spec:
            #tolerations:
            #- key: specialized
            #operator: Equal
            #value: "true"
            #effect: NoSchedule
      containers:
      - name: python-http-server
        image: python:3.9-slim
        command: ["/bin/sh"]
        args: ["-c", "echo '<h1>Hello from Python HTTP Server</h1>' > index.html && python -m http.server 8080"]
        ports:
        - containerPort: 8080
---
apiVersion: v1
kind: Service
metadata:
  name: web-service
spec:
  selector:
    app: python-http-server
  ports:
  - name: http
    port: 80
    targetPort: 8080
    nodePort: 30080
  type: NodePort
```
