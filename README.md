# LNT_ALL_PROJECTS

[![GitHub](https://img.shields.io/badge/GitHub-darshankerkar-181717?style=flat&logo=github)](https://github.com/darshankerkar)
[![Projects](https://img.shields.io/badge/Projects-5-blue?style=flat)](https://github.com/darshankerkar/LNT_ALL_PROJECTS)
[![Training](https://img.shields.io/badge/Program-LnT%20DevOps%20Training-orange?style=flat)](https://github.com/darshankerkar/LNT_ALL_PROJECTS)
[![License](https://img.shields.io/badge/license-MIT-green?style=flat)](LICENSE)

---

A consolidated repository containing all hands-on projects built during the **LnT DevOps Training Program**. Each project is a self-contained, production-oriented implementation covering a core area of modern DevOps — from CI/CD pipelines and containerization to infrastructure automation and Kubernetes orchestration.

---

## Table of Contents

- [Repository Structure](#repository-structure)
- [Projects Overview](#projects-overview)
  - [1. CI/CD Pipeline — Day 3](#1-cicd-pipeline--day-3)
  - [2. Dockerised To-Do API](#2-dockerised-to-do-api)
  - [3. Git Workflow Simulator](#3-git-workflow-simulator)
  - [4. Infrastructure as Code Pipeline](#4-infrastructure-as-code-pipeline)
  - [5. Kubernetes Autoscaling — Day 4](#5-kubernetes-autoscaling--day-4)
- [Technology Stack](#technology-stack)
- [Training Curriculum](#training-curriculum)
- [Getting Started](#getting-started)

---

## Repository Structure

```
LNT_ALL_PROJECTS/
│
├── CICD_PIPELINE_DAY3/          # GitHub Actions CI/CD with Python Calculator
│   ├── .github/workflows/
│   │   └── CI.yml
│   └── Day_3/Project/Calculator/
│       ├── calculator.py
│       └── test_calculator.py
│
├── Dockerised-TO-DO/            # Production-grade Dockerized REST API
│   ├── app.py
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── Makefile
│   └── requirements.txt
│
├── Git_Worflow_Simulator/       # Professional Git collaboration model
│   ├── .github/
│   │   ├── CODEOWNERS
│   │   └── PULL_REQUEST_TEMPLATE.md
│   └── workflow-simulator.py
│
├── IAC_Pipeline/                # Terraform + GitHub Actions IaC pipeline
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── modules/staging/
│   └── .github/workflows/
│       ├── lint.yml
│       ├── plan.yml
│       └── apply.yml
│
├── LnT_Day_4/                   # Kubernetes Deployment with HPA
│   ├── deployment.yaml
│   ├── hpa.yaml
│   ├── components.yaml
│   └── dockerfile
│
└── README.md
```

---

## Projects Overview

---

### 1. CI/CD Pipeline — Day 3

**Directory:** [`CICD_PIPELINE_DAY3`](./CICD_PIPELINE_DAY3)

A complete CI/CD pipeline implementation using **GitHub Actions** built around a Python Calculator application. This project demonstrates how automated pipelines enforce code quality and testing on every commit.

#### What it does

- Runs **pytest** unit tests automatically on every push and pull request
- Performs **pylint** static code analysis to enforce code quality standards
- Validates that all calculator functions (add, subtract) behave correctly before merging

#### Pipeline Flow

```
Developer pushes code
        |
        v
  GitHub Actions triggered
        |
        +---> Checkout code
        |
        +---> Install dependencies (pytest, pylint)
        |
        +---> Run pylint (code quality check)
        |
        +---> Run pytest (unit tests)
        |
        v
  Pass / Fail reported on commit
```

#### Key Files

| File | Purpose |
|------|---------|
| `.github/workflows/CI.yml` | GitHub Actions pipeline definition |
| `Calculator/calculator.py` | Calculator module with add and subtract functions |
| `Calculator/test_calculator.py` | Pytest test cases for both functions |

#### Concepts Covered

- GitHub Actions workflow syntax (`on`, `jobs`, `steps`)
- Automated testing with pytest
- Static analysis with pylint
- Branch-level CI enforcement

---

### 2. Dockerised To-Do API

**Directory:** [`Dockerised-TO-DO`](./Dockerised-TO-DO)

A **production-ready, containerized REST API** for to-do management built with Python Flask, multi-stage Docker builds, and Gunicorn as the WSGI server. Designed to be deployed on Docker Hub, Kubernetes, or any container orchestration platform.

#### Architecture

```
Multi-Stage Docker Build
--------------------------

Stage 1 — Builder
  Python 3.13-slim base
  Install build tools (gcc)
  Compile and cache dependencies

Stage 2 — Runtime
  Lightweight Python 3.13-slim
  Copy pre-built wheels from Stage 1
  Non-root user execution (appuser)
  Health check configuration
  Gunicorn production server (4 workers)

Result: ~150MB image (down from ~1GB)
```

#### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Service health check |
| GET | `/todos` | List all todos (paginated) |
| GET | `/todos/{id}` | Retrieve a single todo |
| POST | `/todos` | Create a new todo |
| PUT | `/todos/{id}` | Update an existing todo |
| DELETE | `/todos/{id}` | Delete a single todo |
| DELETE | `/todos` | Delete all todos |

#### Performance Benchmarks

```
Benchmark: ab -n 1000 -c 10 http://localhost:5000/health

Requests per second : 1,250 req/sec
Mean response time  : 8ms
p95 response time   : < 100ms
Container startup   : < 2s
Image size          : ~150MB
```

#### Security Measures

- Non-root container execution (`appuser`)
- Minimal base image (Python slim) — reduced attack surface
- Build tools excluded from production image
- Secrets isolated via `.env` (excluded from git and Docker context)
- Automatic health-check restart on failure

#### Concepts Covered

- Multi-stage Docker builds for optimized image size
- Gunicorn WSGI production server configuration
- Docker Compose for local orchestration
- Makefile-based build automation
- Semantic versioning (`MAJOR.MINOR.PATCH`)
- Docker Hub image publishing

---

### 3. Git Workflow Simulator

**Directory:** [`Git_Worflow_Simulator`](./Git_Worflow_Simulator)

A documentation-first project that models a **professional GitHub collaboration workflow** for a 3-person engineering team. It codifies branching strategies, pull request standards, code ownership, and release tagging.

#### Team Workflow Model

```
main (protected)
  |
  +--- feature/123-add-user-guide    (Developer A)
  |         |
  |         +--> Pull Request --> Code Review (Developer B)
  |                                   |
  |                              Approved --> Merge --> main
  |
  +--- bugfix/234-fix-typo           (Developer A)
  |
  +--- hotfix/345-patch-build-error  (Release Manager)
```

#### Branch Protection Rules Demonstrated

| Rule | Purpose |
|------|---------|
| Require pull request before merge | No direct pushes to `main` |
| Require 1-2 approving reviews | Enforces peer code review |
| Require passing status checks | CI must pass before merge |
| Dismiss stale approvals | Forces re-review after new commits |
| Require branches to be up to date | Prevents out-of-date merges |

#### Release Tagging Strategy

```
v1.0.0   Initial release
v1.1.0   New functionality (backward compatible)
v1.1.1   Bug fix
v2.0.0   Breaking changes
```

#### Repository Components

| File | Purpose |
|------|---------|
| `.github/PULL_REQUEST_TEMPLATE.md` | Standardized PR checklist for all contributors |
| `.github/CODEOWNERS` | Automatic reviewer assignment by file path |
| `workflow-simulator.py` | Script that prints the complete team workflow steps |

#### Concepts Covered

- Feature branch naming conventions
- Pull request lifecycle and code review process
- Conflict resolution via rebase and merge
- CODEOWNERS for automatic reviewer routing
- Semantic versioning and release tagging

---

### 4. Infrastructure as Code Pipeline

**Directory:** [`IAC_Pipeline`](./IAC_Pipeline)

A **production-ready Terraform + GitHub Actions CI/CD pipeline** for deploying AWS infrastructure with fully automated linting, planning, and applying stages. Follows IaC best practices with reusable modules and GitOps-style state management.

#### Pipeline Architecture

```
Pull Request opened / updated
        |
        v
   LINT stage
   terraform fmt     (format check)
   terraform validate (syntax check)
   tflint            (best practices)
        |
        v
   PLAN stage
   terraform plan    (generates execution plan)
   Posts plan output as PR comment for human review
        |
        v
   PR approved and merged to main
        |
        v
   APPLY stage
   terraform apply   (provisions AWS resources)
   State file committed back to repo
```

#### Infrastructure Deployed

| Resource | Configuration |
|----------|--------------|
| AWS EC2 Instances | Configurable count, default `t2.micro` |
| Security Group | HTTP (80), HTTPS (443), SSH (22) |
| Tags | Auto-tagged with environment and project metadata |

#### Terraform Module Structure

| Module | Location | Responsibility |
|--------|----------|---------------|
| Root | `main.tf` | Entry point, calls staging module |
| Staging | `modules/staging/` | EC2 + Security Group resources |

#### GitHub Actions Workflows

| Workflow | Trigger | Actions |
|----------|---------|---------|
| `lint.yml` | PR opened | `fmt`, `validate`, `tflint` |
| `plan.yml` | PR updated | Posts `terraform plan` to PR comment |
| `apply.yml` | Merge to `main` | `terraform apply`, commits state |

#### Concepts Covered

- Terraform modules and reusable infrastructure
- GitOps: infrastructure changes reviewed via pull requests
- Automated `terraform plan` output in PR comments
- AWS credential management via GitHub Secrets
- State management and remote backend considerations

---

### 5. Kubernetes Autoscaling — Day 4

**Directory:** [`LnT_Day_4`](./LnT_Day_4)

A complete **Kubernetes autoscaling setup** demonstrating Horizontal Pod Autoscaler (HPA) with Metrics Server integration. The application is containerized with Nginx and deployed via a Kubernetes Deployment manifest.

#### Scaling Architecture

```
                         CPU load increases
                                |
                                v
                    HPA monitors CPU utilization
                    (target: 80% average)
                                |
                +---------------+---------------+
                |                               |
         Below threshold                 Above threshold
                |                               |
         Scale down to min                Scale up pods
         (minReplicas: 2)           (up to maxReplicas: 8)

Metrics Server  <---  kubelet  <---  Node resource usage
(kube-system namespace)
```

#### Kubernetes Resources

| Resource | Name | Namespace | Purpose |
|----------|------|-----------|---------|
| Deployment | `my-app` | default | Runs the Nginx application with 3 replicas |
| HPA | `my-app` | default | Auto-scales pods between 2-8 based on CPU |
| Metrics Server | `metrics-server` | kube-system | Collects node and pod resource metrics |
| APIService | `v1beta1.metrics.k8s.io` | cluster-wide | Registers metrics API with the API server |

#### HPA Configuration

```
Scale Target : my-app Deployment
Min Replicas : 2
Max Replicas : 8
Scale Metric : CPU Utilization
Threshold    : 80% average across all pods
```

#### Deployment Commands

```bash
# Step 1 — Build Docker image
docker build -t my-app:latest -f dockerfile .

# Step 2 — Install Metrics Server (required for HPA)
kubectl apply -f components.yaml

# Step 3 — Deploy the application
kubectl apply -f deployment.yaml

# Step 4 — Enable autoscaling
kubectl apply -f hpa.yaml

# Step 5 — Watch HPA in action
kubectl get hpa my-app --watch
```

#### Concepts Covered

- Kubernetes Deployments and replica management
- Horizontal Pod Autoscaler (HPA) with CPU-based scaling
- Metrics Server installation and APIService registration
- RBAC — ServiceAccount, ClusterRole, ClusterRoleBinding
- Docker image creation and Kubernetes integration

---

## Technology Stack

| Category | Technologies |
|----------|-------------|
| Containerization | Docker, Docker Compose, Multi-stage builds, Gunicorn |
| Orchestration | Kubernetes, HPA, Metrics Server |
| CI/CD | GitHub Actions, Automated testing, Pipeline stages |
| Infrastructure as Code | Terraform, AWS EC2, Security Groups |
| Version Control | Git, Branch strategies, CODEOWNERS, PR templates |
| Application | Python 3.13, Flask 3.0, pytest, pylint |
| Cloud | AWS (EC2, IAM, Security Groups) |

---

## Training Curriculum

```
LnT DevOps Training Program
==============================

  Day 3
  ------
  Topic  : CI/CD Pipelines
  Project: CICD_PIPELINE_DAY3
  Tools  : GitHub Actions, pytest, pylint
  Output : Automated pipeline on every commit

  Day 4
  ------
  Topic  : Kubernetes Orchestration and Autoscaling
  Project: LnT_Day_4
  Tools  : Kubernetes, Docker, HPA, Metrics Server
  Output : Self-scaling containerized application

  Supplementary Projects
  -----------------------
  Dockerised-TO-DO   : Production Docker patterns and REST API design
  Git_Worflow_Simulator : Team collaboration and branching workflows
  IAC_Pipeline       : Terraform-based infrastructure automation
```

---

## Getting Started

Clone the repository:

```bash
git clone https://github.com/darshankerkar/LNT_ALL_PROJECTS.git
cd LNT_ALL_PROJECTS
```

Navigate to any project and follow its individual README:

```bash
# CI/CD Pipeline
cd CICD_PIPELINE_DAY3

# Dockerised REST API
cd Dockerised-TO-DO

# Git Workflow Model
cd Git_Worflow_Simulator

# Terraform IaC Pipeline
cd IAC_Pipeline

# Kubernetes HPA
cd LnT_Day_4
```

Each project directory contains a `README.md` with full setup instructions, command references, and architecture details.

---

## Author

**Darshan Kerkar**
LnT DevOps Training Program

---

*Last Updated: June 2026*
