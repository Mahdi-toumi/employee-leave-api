# 🚀 DevOps Employee Leave API

A robust, containerized FastAPI application demonstrating a complete DevOps lifecycle. This project features a fully automated CI/CD pipeline, Kubernetes deployment, and a full observability stack.

## 📋 Table of Contents
- [Architecture](#-architecture)
- [Development Workflow](#-development-workflow)
- [CI/CD Pipeline Details](#-cicd-pipeline-details)
- [Local Setup](#-local-setup-python)
- [Docker Usage](#-docker-usage)
- [Kubernetes Deployment](#-kubernetes-deployment)
- [Observability](#-observability-logs-metrics-traces-visualization)
- [🔥 Defense Cheat Sheet](#-defense-cheat-sheet-commandes-pour-la-soutenance)

---

## 🏗 Architecture
* **API Framework:** FastAPI (Python 3.10)
* **Containerization:** Docker (Multi-stage build)
* **Orchestration:** Kubernetes (Minikube)
* **Observability:**
    * **Prometheus:** Metrics Collection (The Database)
    * **Grafana:** Metrics Visualization (The Dashboard)
    * **Jaeger:** Distributed Tracing
    * **Structlog:** JSON Logs
* **CI/CD:** GitHub Actions

---

## 🤝 Development Workflow
This project follows strict DevOps best practices for version control:

1. **Branching Strategy:** No direct commits to `main`. All changes are made on feature branches (e.g., `feat/backend`, `ops/docker`, `fix/security`).
2. **Conventional Commits:** Commit messages follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:
    * `feat:` New features
    * `fix:` Bug fixes
    * `ops:` CI/CD, Docker, or K8s changes
    * `docs:` Documentation updates
3. **Pull Requests & Reviews:** Every branch is merged via a Pull Request (PR) linked to a GitHub Issue. Code reviews are performed to ensure quality before merging.

---

## ⚙️ CI/CD Pipeline Details
The pipeline (`.github/workflows/ci-cd.yml`) triggers on every push to `main`.

### 🔹 Stage 1: CI (Continuous Integration)
* **Unit Testing:** Runs `pytest` with `pytest-cov`.
* **Coverage Check:** Generates a coverage report (Target > 95%).
* **Security (SAST):** Uses **Bandit** to scan Python source code for security flaws (e.g., hardcoded secrets).

### 🔹 Stage 2: CD (Continuous Delivery)
* **Containerization:** Builds the Docker image and pushes it to **Docker Hub**.
* **Security (DAST):** Runs **OWASP ZAP** against the running container to find runtime vulnerabilities.
* **Deployment Simulation:** Simulates `kubectl apply` to ensure manifests are valid for production.

---

## 🐍 Local Setup (Python)
To run without Docker:
```bash
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Swagger UI: http://localhost:8000/docs

---

## 🐳 Docker Usage
This project uses Docker Compose to orchestrate the entire stack locally (App + Jaeger + Prometheus + Grafana).

```bash
# Start the full stack
docker-compose up -d
```

| Service | URL | Credentials |
| :--- | :--- | :--- |
| **API Docs** | http://localhost:8000/docs | - |
| **Grafana** | http://localhost:3000 | (No login required) |
| **Prometheus** | http://localhost:9090 | - |
| **Jaeger** | http://localhost:16686 | - |

---

## ☸ Kubernetes Deployment
Deployed on **Minikube** using declarative manifests.

```bash
# 1. Start Minikube
minikube start

# 2. Deploy the Stack (App + Observability)
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/jaeger.yaml
kubectl apply -f k8s/prometheus.yaml
kubectl apply -f k8s/grafana.yaml

# 3. Verify
kubectl get pods
```

---

## 🔍 Observability (Logs, Metrics, Traces, Visualization)

### 1. Visualization (Grafana)
Grafana is pre-configured to connect to Prometheus.
```bash
kubectl port-forward svc/grafana-service 3000:3000
# Access: http://localhost:3000
# Data Source: Configured automatically via ConfigMap
```

### 2. Metrics (Prometheus)
Scrapes raw data from the API.
```bash
kubectl port-forward svc/prometheus-service 9090:9090
# Access: http://localhost:9090
```

### 3. Traces (Jaeger)
Visualizes the request lifecycle.
```bash
kubectl port-forward svc/jaeger-service 16686:16686
# Access: http://localhost:16686
```

### 4. Logs (JSON)
Structured logs are persisted inside the container.
```bash
kubectl exec <POD_NAME> -- cat app.log
```

---

## 🔥 Defense Cheat Sheet (Commandes pour la Soutenance)

Use these commands during your technical demonstration.

### 🛠️ 1. Docker Compose (Local Dev Demo)
If you demo with Docker Compose:
```bash
# Start everything
docker-compose up -d --build

# Show running containers
docker-compose ps

# Show Logs (Real-time)
docker-compose logs -f api

# Stop everything
docker-compose down
```

### ☸️ 2. Kubernetes (Prod Simulation Demo)
If you demo with Minikube:

**Setup:**
```bash
minikube start
kubectl apply -f k8s/
kubectl get pods -w  # Watch them start
```

**Accessing Dashboards (Open 4 terminals):**
```bash
# Terminal 1: API Access (if needed)
kubectl port-forward svc/leave-api-service 8000:8000

# Terminal 2: Grafana (The Dashboard)
kubectl port-forward svc/grafana-service 3000:3000

# Terminal 3: Prometheus (Raw Metrics)
kubectl port-forward svc/prometheus-service 9090:9090

# Terminal 4: Jaeger (Tracing)
kubectl port-forward svc/jaeger-service 16686:16686
```

**Checking Logs:**
```bash
# Get Pod Name
export POD_NAME=$(kubectl get pods -l app=employee-leave-api -o jsonpath="{.items[0].metadata.name}")

# Method A: Standard K8s Logs
kubectl logs $POD_NAME

# Method B: Read the JSON file inside the container
kubectl exec $POD_NAME -- cat app.log
```

**Debugging (If something breaks):**
```bash
# Check why a pod is crashing
kubectl describe pod $POD_NAME

# Restart the application
kubectl rollout restart deployment/employee-leave-api
```