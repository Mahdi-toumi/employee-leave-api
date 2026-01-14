# 🚀 DevOps Employee Leave API

A robust, containerized FastAPI application demonstrating a complete DevOps lifecycle. This project features a fully automated CI/CD pipeline, Kubernetes deployment, and a full observability stack.

## 📋 Table of Contents
- [Architecture](#-architecture)
- [Development Workflow](#-development-workflow)
- [CI/CD Pipeline Details](#-cicd-pipeline-details)
- [Local Setup](#-local-setup-python)
- [Docker Usage](#-docker-usage)
- [Kubernetes Deployment](#-kubernetes-deployment)
- [Observability](#-observability-logs-metrics-traces)

---

## 🏗 Architecture
* **API Framework:** FastAPI (Python 3.10)
* **Containerization:** Docker (Multi-stage build)
* **Orchestration:** Kubernetes (Minikube)
* **Observability:** Prometheus (Metrics), Jaeger (Tracing), Structlog (JSON Logs)
* **CI/CD:** GitHub Actions

---

## 🤝 Development Workflow
This project follows strict DevOps best practices for version control:

1.  **Branching Strategy:** No direct commits to `main`. All changes are made on feature branches (e.g., `feat/backend`, `ops/docker`, `fix/security`).
2.  **Conventional Commits:** Commit messages follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:
    * `feat:` New features
    * `fix:` Bug fixes
    * `ops:` CI/CD, Docker, or K8s changes
    * `docs:` Documentation updates
3.  **Pull Requests & Reviews:** Every branch is merged via a Pull Request (PR) linked to a GitHub Issue. Code reviews are performed to ensure quality before merging.

---

## ⚙️ CI/CD Pipeline Details
The pipeline (`.github/workflows/ci-cd.yml`) triggers on every push to `main`.

### 🔹 Stage 1: Build & Test
* **Unit Testing:** Runs `pytest` with `pytest-cov`.
* **Coverage Check:** Generates an HTML coverage report (Target > 80%).
* **Artifacts:** Uploads `coverage-report` for review.

### 🔹 Stage 2: Security Scans (DevSecOps)
* **SAST (Static Analysis):** Uses **Bandit** to scan Python source code for security flaws (e.g., hardcoded secrets).
* **Artifacts:** Uploads `sast-report.json`.

### 🔹 Stage 3: Containerization
* **Build:** Builds the Docker image using the `Dockerfile`.
* **Push:** Pushes the image to **Docker Hub** with the tag `latest`.

### 🔹 Stage 4: DAST (Dynamic Security)
* **Runtime Scan:** Spins up the container and runs **OWASP ZAP**.
* **Configuration:** Runs as root to bypass permission issues and generates an HTML report.
* **Artifacts:** Uploads `zap-scan-report.html`.

### 🔹 Stage 5: Deployment Simulation
* **Dry Run:** Simulates the application of Kubernetes manifests (`kubectl apply`) to verify configuration integrity before production.

---

## 🐍 Local Setup (Python)
To run without Docker:
```bash
python -m venv venv
# Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Swagger UI: http://localhost:8000/docs

---

## 🐳 Docker Usage
```bash
# Build & Run
docker build -t employee-leave-api:latest .
docker run -d -p 8000:8000 employee-leave-api:latest

# Full Stack (App + Jaeger + Prometheus)
docker-compose up -d
```

---

## ☸ Kubernetes Deployment
```bash
# 1. Start Minikube
minikube start

# 2. Deploy Stack
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/jaeger.yaml
kubectl apply -f k8s/prometheus.yaml

# 3. Verify
kubectl get pods
```

---

## 🔍 Observability (The 3 Pillars)

### 1. Logs (JSON)
Logs are structured and persisted to a file.
```bash
# Download log file from Pod
kubectl exec <POD_NAME> -- cat app.log
```

### 2. Metrics (Prometheus)
```bash
kubectl port-forward svc/prometheus-service 9090:9090
# Go to http://localhost:9090 -> Query: http_requests_total
```

### 3. Traces (Jaeger)
```bash
kubectl port-forward svc/jaeger-service 16686:16686
# Go to http://localhost:16686 -> Find Traces
```
