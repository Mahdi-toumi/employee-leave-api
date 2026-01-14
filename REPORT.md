# DevOps Project Final Report
**Project:** Employee Leave API with Kubernetes & Observability
**Author:** Mahdi Toumi
**Date:** January 2026

## 1. Introduction
This project implements a complete DevOps lifecycle for a backend service. I designed a lightweight REST API for Employee Leave Management using **FastAPI** (Python). The goal was to practice end-to-end automation, from coding to containerization, security, and Kubernetes deployment.

## 2. Architecture & Tools
* **Backend:** FastAPI (Python 3.10) chosen for performance and automatic Swagger documentation.
* **Database:** In-memory dictionary to keep the service lightweight (<150 lines of code).
* **Containerization:** **Docker** (multi-stage build) to create immutable artifacts.
* **Orchestration:** **Kubernetes (Minikube)** for managing deployments, services, and scaling.
* **CI/CD:** **GitHub Actions** for automated testing and deployment.

## 3. Observability Strategy (The 3 Pillars)
I implemented full-stack observability to monitor the application health in production:
1.  **Logs:** Used \`structlog\` to generate structured **JSON logs**. Logs are written to \`stdout\` (for kubectl logs) and persisted to \`app.log\` inside the container for file-based retrieval.
2.  **Metrics:** Deployed a **Prometheus** server in the cluster. It scrapes the \`/metrics\` endpoint exposed by \`prometheus-fastapi-instrumentator\` to track request rates and latency.
3.  **Traces:** Deployed **Jaeger** in the cluster. The application is instrumented with OpenTelemetry to send traces to Jaeger, allowing visualization of request flows.

## 4. Security Implementation (DevSecOps)
Security was integrated into the pipeline ("Shift Left"):
* **SAST (Static Analysis):** Used **Bandit** to scan source code for common Python vulnerabilities (e.g., hardcoded secrets).
* **DAST (Dynamic Analysis):** Used **OWASP ZAP** to scan the running container for runtime issues (e.g., missing security headers like CSP).
* **Results:** The pipeline generates and uploads security reports as artifacts on every build.

## 5. Kubernetes Setup
The application is deployed using declarative manifests:
* **Deployment:** Defines the Pods, replicas, and resource limits (CPU/Memory).
* **Service:** Exposes the API via a LoadBalancer (or NodePort in Minikube).
* **Sidecars/Addons:** Prometheus and Jaeger are deployed as separate services within the same namespace to support monitoring.

## 6. Lessons Learned
* **Persistence:** Learned how to extract files from pods using \`kubectl cp\` and \`kubectl exec\`.
* **Networking:** Understanding Service DNS (\`http://jaeger-service:4317\`) was critical to connect the App to the Tracing backend.
* **Automation:** The CI/CD pipeline significantly reduces manual errors by automatically testing and scanning code before pushing to Docker Hub.