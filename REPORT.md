# DevOps Project Final Report
**Project:** Employee Leave API with Kubernetes & Observability
**Author:** Mahdi Toumi
**Date:** January 2026

## 1. Introduction
This project implements a complete DevOps lifecycle for a backend service. I designed a lightweight REST API for Employee Leave Management using **FastAPI**. The goal was to practice end-to-end automation, from coding to containerization, security, and Kubernetes deployment.

## 2. Git Workflow & Collaboration
To simulate a professional environment, I strictly adhered to DevOps best practices:
* **Task Tracking:** Used GitHub Issues to track deliverables (e.g., #1 Backend, #6 K8s).
* **Branching:** Utilized feature branches (e.g., `feat/backend`, `ops/docker`) instead of committing to main.
* **Conventional Commits:** Used standardized commit messages (e.g., `feat: ...`, `fix: ...`) for a clean history.
* **Code Reviews:** All features were merged via Pull Requests (PRs). I simulated peer reviews by commenting on code quality, security implications, and best practices before merging.

## 3. Architecture & Tools
* **Backend:** FastAPI (Python 3.10) - Chosen for high performance and automatic Swagger UI.
* **Containerization:** Docker - Used multi-stage builds (`python:3.10-slim`) to keep image size low.
* **Orchestration:** Kubernetes (Minikube) - Managed Deployment, Service, and ConfigMaps.

## 4. CI/CD Pipeline (GitHub Actions)
I built a robust pipeline that ensures only high-quality code reaches production:
1.  **Automated Testing:** Runs `pytest` with `pytest-cov`. I achieved **>95% code coverage**, ensuring reliability.
2.  **Security Gates:**
    * **SAST (Bandit):** Scans code for vulnerabilities before the build.
    * **DAST (OWASP ZAP):** Scans the running container for HTTP vulnerabilities (e.g., missing headers).
3.  **Artifact Management:** Security reports and coverage results are uploaded as GitHub Artifacts for audit trails.
4.  **Deployment Simulation:** A final stage verifies that Kubernetes manifests can be applied without errors.

## 5. Observability Strategy
I implemented the "Three Pillars of Observability" to monitor the system:
1.  **Logs:** Used `structlog` for JSON logging. Logs are written to `stdout` (for K8s) and persisted to `app.log` inside the container, retrievable via `kubectl cp`.
2.  **Metrics:** Deployed **Prometheus** to scrape the `/metrics` endpoint, tracking request rates and error counts.
3.  **Traces:** Deployed **Jaeger** and instrumented the app with OpenTelemetry. This visualizes the request path and latency across the system.

## 6. Kubernetes Setup
The deployment is fully declarative:
* **Deployment:** Defines 1 replica with CPU/Memory limits to prevent resource exhaustion.
* **Service:** Uses a LoadBalancer strategy to expose the API.
* **Integration:** The App Pod connects to Jaeger and Prometheus services using internal ClusterDNS names (e.g., `http://jaeger-service:4317`).

## 7. Lessons Learned
* **Permissions in CI:** Running DAST scans in Docker requires root permissions (`-u 0`) to write reports to the GitHub runner volume.
* **Service Discovery:** In Kubernetes, services must communicate via DNS names, not `localhost`.
* **Process Matters:** Using Conventional Commits and PRs makes the project history readable and professional.
