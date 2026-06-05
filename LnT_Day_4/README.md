# 🚀 LnT Day 4 — Kubernetes Deployment with HPA & Metrics Server

This project demonstrates **Kubernetes-based container orchestration** with **Horizontal Pod Autoscaling (HPA)** and **Metrics Server** setup — covered on Day 4 of the LnT DevOps training.

---

## 📁 Project Structure

```
LnT_Day_4/
├── dockerfile          # Docker image definition (Nginx-based)
├── deployment.yaml     # Kubernetes Deployment manifest for my-app
├── hpa.yaml            # Horizontal Pod Autoscaler configuration
└── components.yaml     # Metrics Server full component manifest
```

---

## 🛠️ Tech Stack

| Tool               | Purpose                              |
|--------------------|--------------------------------------|
| Docker             | Containerize the application         |
| Kubernetes (K8s)   | Container orchestration              |
| Metrics Server     | Resource usage metrics for HPA       |
| HPA                | Auto-scale pods based on CPU usage   |

---

## 📄 File Details

### `dockerfile`
Builds a lightweight **Nginx** container that serves static content.
- Base image: `nginx:latest`
- Exposes port `8080`

### `deployment.yaml`
Defines a Kubernetes **Deployment** for `my-app`:
- **3 replicas** by default
- Container image: `my-app:latest`
- Exposes port `8080`

### `hpa.yaml`
Configures **Horizontal Pod Autoscaler** for `my-app`:
- Min replicas: `2`
- Max replicas: `8`
- Scales based on **CPU utilization at 80%** threshold

### `components.yaml`
Full **Metrics Server** manifest including:
- ServiceAccount, ClusterRoles, RoleBindings
- Metrics Server Deployment in `kube-system` namespace
- APIService registration for `v1beta1.metrics.k8s.io`

---

## ▶️ How to Run

### 1. Build the Docker Image
```bash
docker build -t my-app:latest -f dockerfile .
```

### 2. Apply Metrics Server (required for HPA)
```bash
kubectl apply -f components.yaml
```

### 3. Deploy the Application
```bash
kubectl apply -f deployment.yaml
```

### 4. Apply the HPA
```bash
kubectl apply -f hpa.yaml
```

---

## 🔍 Verify Setup

```bash
# Check pods
kubectl get pods

# Check HPA status
kubectl get hpa

# Check Metrics Server
kubectl get pods -n kube-system | grep metrics-server

# Watch HPA scale in real-time
kubectl get hpa my-app --watch
```

---

## 📌 Key Concepts Learned

- **Kubernetes Deployments** — managing replicas and rolling updates
- **Horizontal Pod Autoscaler (HPA)** — dynamic scaling based on resource metrics
- **Metrics Server** — cluster-level resource metrics pipeline for HPA
- **Docker + Kubernetes integration** — containerizing and deploying apps

---

## 👨‍💻 Author

**LnT DevOps Training — Day 4**
