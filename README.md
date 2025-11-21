# L00188491-ATU-DevOps-Full-Pipeline
DevOps Engineering (SWEN_IT902) Full Pipeline Project
Arno Moelich - L00188491

[![CI/CD Pipeline](https://github.com/Arno-ATU/L00188491-ATU-DevOps-Full-Pipeline/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/Arno-ATU/L00188491-ATU-DevOps-Full-Pipeline/actions/workflows/ci-cd.yml)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=Arno-ATU_L00188491-ATU-DevOps-Full-Pipeline&metric=coverage)](https://sonarcloud.io/summary/new_code?id=Arno-ATU_L00188491-ATU-DevOps-Full-Pipeline)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=Arno-ATU_L00188491-ATU-DevOps-Full-Pipeline&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=Arno-ATU_L00188491-ATU-DevOps-Full-Pipeline)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=Arno-ATU_L00188491-ATU-DevOps-Full-Pipeline&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=Arno-ATU_L00188491-ATU-DevOps-Full-Pipeline)

---

## Project Overview

This project demonstrates a complete CI/CD pipeline for a Python Flask web application. The application itself is a simple quote generator with REST API endpoints, designed to generate user activity for monitoring and observability demonstrations.

**Live Application:** <a href="https://l00188491-web-app-pipeline-h0breuchbbf3hvfm.swedencentral-01.azurewebsites.net/" target="_blank">Query Generator App - Azure Deployment</a>

> **Note:** Chrome may show a security warning. The site is safe - click "Details" → "visit this unsafe site" to proceed. This is due to Azure's default domain not having an SSL certificate.

---

## Key Technologies Used

| Component | Technologies | Status |
|-----------|-------------|--------|
| **Application** | Python 3.11, Flask 2.3.3, pytest | ✅ |
| **Source Code Management** | Git, GitHub | ✅ |
| **Automated Builds & Testing** | GitHub Actions, pytest, 92% coverage | ✅ |
| **Static Analysis & Security** | SonarCloud, Trivy, Flake8, Pylint | ✅ |
| **Containerization** | Docker, Docker Compose | ✅ |
| **Container Registry** | Docker Hub | ✅ |
| **Cloud Deployment** | Azure App Service, Linux Containers | ✅ |
| **Monitoring & Logging** | Azure Application Insights, custom events, alerts | ✅ |

---

## CI/CD Pipeline Architecture

### Pipeline Stages

The automated pipeline consists of five sequential stages:

```
Source Code (GitHub) 
    ↓
[1] Test & Build
    ├─ Unit tests (pytest)
    ├─ Code coverage analysis
    └─ Linting (flake8, pylint)
    ↓
[2] Static Analysis & Security
    ├─ SonarCloud code quality scan
    └─ Trivy vulnerability scanning
    ↓
[3] Containerization
    ├─ Docker image build
    └─ Push to Docker Hub
    ↓
[4] Cloud Deployment
    └─ Deploy to Azure App Service
    ↓
[5] Monitoring & Alerting
    └─ Application Insights telemetry
```

---

## Implementation Details

### 1. Source Code Management

**Tool:** Git & GitHub  
**Workflow:** Feature branches, pull requests, and trunk-based development

- Professional commit history with meaningful messages
- `.gitignore` configured for Python projects
- Branch protection and code review processes

### 2. Automated Testing

**Framework:** pytest with coverage reporting  
**Coverage:** 92% overall code coverage

- 25 unit and integration tests
- Automated execution on every push
- Coverage reports uploaded to SonarCloud

**Run tests locally:**
```bash
pytest tests/ --cov=app --cov-report=term
```

### 3. Static Analysis & Security Scanning

**Tools Implemented:**

- **SonarCloud:** Code quality, code smells, maintainability analysis
- **Trivy:** Vulnerability scanning for dependencies and container images
- **Flake8:** Python code style checking
- **Pylint:** Static code analysis

**Quality Gates:** 
- Code coverage > 80%
- Security hotspots reviewed
- No critical vulnerabilities

### 4. Containerization

**Technology:** Docker  
**Container Registry:** Docker Hub  
**Image:** `arnoatu/cicd-pipeline-demo:latest`

**Dockerfile optimizations:**
- Python 3.11 slim base image
- Layer caching for faster builds
- `.dockerignore` to minimize image size

**Local development:**
```bash
# Run with Docker Compose
docker-compose up

# Access application
http://localhost:8000
```

### 5. Cloud Deployment

**Platform:** Microsoft Azure  
**Service:** App Service (Linux container)  
**Region:** Sweden Central

**Deployment Process:**
1. GitHub Actions builds Docker image
2. Image pushed to Docker Hub with tags (latest, branch, SHA)
3. Azure App Service pulls latest image
4. Container deployed with zero-downtime

**Infrastructure:**
- Resource Group: `SWEN_IT902_DevOps_Engineering`
- App Service Plan: Basic B1 (Linux)
- Automated deployment via GitHub Actions

### 6. Monitoring & Logging

**Tool:** Azure Application Insights

**Telemetry Collected:**
- HTTP request/response metrics
- Application performance (response times)
- Custom events (user actions, API calls)
- Error tracking and exception logging
- Resource utilization (CPU, memory)

**Configured Alerts:**
- High error rate (> 5 errors in 5 minutes)
- Slow response time (> 2 seconds average)
- Application availability < 80%

**Notifications:** Email alerts to L00188491@atu.ie

---

## Local Development Setup

### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- Git

### Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/Arno-ATU/L00188491-ATU-DevOps-Full-Pipeline.git
cd L00188491-ATU-DevOps-Full-Pipeline
```

2. **Run with Docker Compose**
```bash
docker-compose up
```

3. **Access the application**
- Application: http://localhost:8000
- Health check: http://localhost:8000/health

### Running Tests

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/

# Run with coverage
pytest tests/ --cov=app --cov-report=html
```

---

## Security & Secret Management

All sensitive credentials are managed via GitHub Actions secrets:

- `AZURE_WEBAPP_PUBLISH_PROFILE` - Azure deployment credentials
- `DOCKER_USERNAME` / `DOCKER_TOKEN` - Docker Hub authentication
- `SONAR_TOKEN` - SonarCloud integration
- `APPLICATIONINSIGHTS_CONNECTION_STRING` - Monitoring telemetry

Secrets are encrypted by GitHub and injected at runtime. Never committed to source control.

---

## Project Structure

```
.
├── .github/
│   └── workflows/
│       └── ci-cd.yml          # GitHub Actions pipeline
├── app/
│   ├── __init__.py
│   ├── main.py                # Flask application with monitoring
│   ├── models.py              # Quote data models
│   └── stats.py               # Statistics tracking
├── static/
│   ├── index.html             # Frontend UI
│   └── style.css              # Styling
├── tests/
│   ├── test_api.py            # API endpoint tests
│   ├── test_models.py         # Model tests
│   └── test_stats.py          # Statistics tests
├── .dockerignore              # Docker build exclusions
├── .gitignore                 # Git exclusions
├── docker-compose.yml         # Local development orchestration
├── Dockerfile                 # Container image definition
├── pytest.ini                 # Test configuration
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

---

## CI/CD Pipeline Configuration

### GitHub Actions Workflow

**Triggers:**
- Push to `main` branch
- Pull requests to `main`

**Jobs:**
1. **test** - Run pytest suite with coverage
2. **lint** - Code quality checks (flake8, pylint)
3. **security-scan** - Trivy vulnerability scanning
4. **docker** - Build and push container image
5. **deploy** - Deploy to Azure App Service

**Workflow file:** `.github/workflows/ci-cd.yml`

---

## Monitoring Dashboard

Access real-time monitoring:
1. Azure Portal → Application Insights → `l00188491-app-insights`
2. View dashboards for:
   - Request rates and response times
   - Error rates and exceptions
   - Resource utilization
   - Custom application events

**Query logs:**
```kusto
customEvents
| where timestamp > ago(24h)
| summarize count() by name
```

---

## Potential Future Enhancements

Potential improvements for production deployment:
- Infrastructure as Code (Terraform/ARM templates)
- Multi-environment strategy (dev/staging/prod)
- Kubernetes orchestration for scalability
- More advanced monitoring with Prometheus/Grafana, but for now Azure Insights provides enough for this app's requirements
- Automated rollback mechanisms

---

## For Educational Purposes Only

This project is submitted as coursework for Postgraduate Diploma in Computing in DevOps at Atlantic Technological University.

---

## Contact

**Student:** Arno Moelich  
**Email:** L00188491@atu.ie  
**GitHub:** [@Arno-ATU](https://github.com/Arno-ATU)
