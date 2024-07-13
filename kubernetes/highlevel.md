
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
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $USER:$USER $HOME/.kube/config

```

Setup MASTER
```bash
sudo kubeadm init
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


# Install containerd
wget https://github.com/containerd/containerd/releases/download/v1.7.19/containerd-1.7.19-linux-amd64.tar.gz
tar Cxzvf /usr/local containerd-1.7.19-linux-amd64.tar.gz
## Install service
wget https://raw.githubusercontent.com/containerd/containerd/main/containerd.service # Save at /usr/local/lib/systemd/system/containerd.service
```

Move your bundle to the offline system.

```bash
cd ./k8s_offline_packages
sudo rpm -ivh *.rpm # OR, try yum install -y *.rpm

# Verify install
rpm -qa | grep -E 'kube'

# Firewall settings
# IF firewalld is active, please ensure ports [6443 10250] are open or your cluster may not function correctly
sudo firewall-cmd --permanent --add-port=6443/tcp
sudo firewall-cmd --permanent --add-port=10250/tcp
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

# Dont forget to set your admin.conf for your user after done.
```


On worker
```bash

# Configure Cgroups Ref: https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/configure-cgroup-driver/


kube join ...
```

## Issues I encountered
* Localhost:8080
  Issue is caused by not installing admin.config in your ~/.kube/

* Nameserver issue(Too many tries)
  Caused by having too many nameservers configured.  Google this. But,
  remove a few nameservers to fix <= 3 MAX nameservers.

* Containers in Not-Ready state
  You need to deploy container networking.
  ```bash
  kubectl apply -f https://docs.projectcalico.org/manifests/calico.yaml
  ```

* Cgroups issues
  * Cgroups setup issue
    Need to deploy with systemd init config.

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
