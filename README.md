# 🚀 DevOps Employee Leave API

A robust, containerized FastAPI application demonstrating a complete DevOps lifecycle. This project features a fully automated CI/CD pipeline, Kubernetes deployment, and a full observability stack (Logs, Metrics, Traces).

## 📋 Table of Contents
- [Architecture](#-architecture)
- [Prerequisites](#-prerequisites)
- [Local Setup (Python)](#-local-setup-python)
- [Docker Usage](#-docker-usage)
- [Kubernetes Deployment](#-kubernetes-deployment)
- [Observability (The 3 Pillars)](#-observability-logs-metrics-traces)
    - [1. Logs](#1-logs-json-structure)
    - [2. Metrics (Prometheus)](#2-metrics-prometheus)
    - [3. Traces (Jaeger)](#3-traces-jaeger)
- [Security & CI/CD](#-security--cicd)

---

## 🏗 Architecture
* **API Framework:** FastAPI (Python 3.10)
* **Containerization:** Docker (Multi-stage build)
* **Orchestration:** Kubernetes (Minikube)
* **Observability:** Prometheus (Metrics), Jaeger (Tracing), Structlog (JSON Logs)
* **CI/CD:** GitHub Actions (Automated Testing, Security Scanning, Docker Push)

---

## 🛠 Prerequisites
Ensure you have the following installed:
* Python 3.9+
* Docker & Docker Compose
* Minikube & kubectl
* Git

---

## 🐍 Local Setup (Python)
To run the application without Docker (for development):

\`\`\`bash
# 1. Create virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
# source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
uvicorn app.main:app --reload
\`\`\`
Access Swagger UI at: http://localhost:8000/docs

---

## 🐳 Docker Usage

### Build and Run with Docker
\`\`\`bash
# Build the image
docker build -t employee-leave-api:latest .

# Run the container
docker run -d -p 8000:8000 --name leave-api employee-leave-api:latest
\`\`\`

### Run with Docker Compose (Includes Jaeger & Prometheus)
\`\`\`bash
docker-compose up -d
\`\`\`
* **API:** http://localhost:8000/docs
* **Jaeger UI:** http://localhost:16686
* **Prometheus:** http://localhost:9090

---

## ☸ Kubernetes Deployment

This project uses **Minikube** to simulate a production cluster.

### 1. Start Minikube
\`\`\`bash
minikube start
\`\`\`

### 2. Apply Manifests
Deploy the App, Jaeger, and Prometheus:
\`\`\`bash
# Deploy the Application
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Deploy Observability Stack
kubectl apply -f k8s/jaeger.yaml
kubectl apply -f k8s/prometheus.yaml
\`\`\`

### 3. Verify Deployment
Wait until all pods are Running:
\`\`\`bash
kubectl get pods
\`\`\`

---

## 🔍 Observability (Logs, Metrics, Traces)

### 1. Logs (JSON Structure & File)
The application writes structured JSON logs to both the terminal and a file inside the container.

**Method A: Stream logs in terminal**
\`\`\`bash
# Get pod name
kubectl get pods
# Stream logs
kubectl logs -f <POD_NAME>
\`\`\`

**Method B: Download log file (Persistent Log)**
\`\`\`bash
# Copy the log file from the container to your local machine
kubectl cp <POD_NAME>:/app/app.log ./app.log
\`\`\`

**Method C: Read file directly inside Pod**
\`\`\`bash
kubectl exec <POD_NAME> -- cat app.log
\`\`\`

### 2. Metrics (Prometheus)
Visualizes HTTP request rates and performance.

1.  **Port-forward Prometheus:**
    \`\`\`bash
    kubectl port-forward svc/prometheus-service 9090:9090
    \`\`\`
2.  **Access Dashboard:** Open http://localhost:9090
3.  **Query:** Type \`http_requests_total\` and click "Graph".

### 3. Traces (Jaeger)
Visualizes the request lifecycle across microservices.

1.  **Port-forward Jaeger:**
    \`\`\`bash
    kubectl port-forward svc/jaeger-service 16686:16686
    \`\`\`
2.  **Access UI:** Open http://localhost:16686
3.  **Find Traces:** Select \`EmployeeLeaveAPI\` and search.

---

## 🛡 Security & CI/CD
The GitHub Actions Pipeline (\`.github/workflows/ci-cd.yml\`) automates:
1.  **Unit Tests:** Pytest with Coverage (>80%)
2.  **SAST Scan:** Bandit (Static Application Security Testing)
3.  **DAST Scan:** OWASP ZAP (Dynamic Analysis on running container)
4.  **Build & Push:** Docker Hub Registry
5.  **Simulation:** Kubernetes Deployment Dry-Run