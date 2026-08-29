# Exercise-2: Deployment Automation & CI/CD Pipeline

## Overview

Production-grade CI/CD pipeline for a Python Flask application with automated testing, security scanning, containerization, and environment-based deployments with manual approval for production.

**Repository:** `jagadeesh0014/jagadeesh_octai_ex2`  
**Docker Hub:** `jyerramcdocker/exercise-2-app`

---

## Architecture Decisions

### 1. CI/CD Tool: GitHub Actions

**Why GitHub Actions?**

- Native integration with GitHub
- No external Jenkins server required
- Free GitHub Actions minutes available
- Easy environment protection and manual approval workflows
- Simple YAML-based configuration

**Workflow Location:**

```text
.github/workflows/ci-cd.yml
```

### 2. Pipeline Flow

```text
Pull Request
     |
     v
test-and-scan
(pytest + pip-audit + trivy)
     |
     v
Push to main
     |
     v
build-and-push
(docker buildx + Docker Hub)
     |
     +----------------+
     |                |
     v                v
deploy-staging   deploy-production
   (auto)       (manual approval)
```

### 3. Containerization

- Base image: `python:3.11-slim`
- Lighter footprint and fewer CVEs compared to full Python images
- Multi-stage builds are not necessary for this small Flask application
- `pip --no-cache-dir` used to reduce image size

### 4. Environments

#### Staging

- Automatic deployment
- Used for validation and testing

#### Production

- Protected environment
- Requires manual approval before deployment
- Uses GitHub Environment Required Reviewers

---

## How to Set Up and Run

### Prerequisites

- Python 3.11+
- Docker
- GitHub Account

### Run Locally

```bash
cd app

pip install -r requirements.txt
python app.py
```

Application URL:

```text
http://localhost:5000
```

### Run Tests

```bash
pytest ../tests -v
```

### Docker Run

Build the image:

```bash
docker build -t exercise-2-app ./app
```

Run the container:

```bash
docker run -p 5000:5000 exercise-2-app
```
Workflow Optimization
Path IgnoresTo optimize cost and avoid unnecessary builds, we have configured paths-ignore in the workflow. Any changes to documentation files will NOT trigger build and deployment pipelines.
```bash
on:
  push:
    branches: [ main ]
    paths-ignore:
      - '**.md'      # All markdown files (README.md, etc.)
      - 'docs/**'    # Documentation folder
  pull_request:
    branches: [ main ]
    paths-ignore:
      - '**.md'
      - 'docs/**'
```
Benefit: If you only update README.md or docs, the expensive build-and-push and deploy jobs are skipped, saving GitHub Actions minutes and Docker Hub pulls/pushes. 
Build triggers only when actual app code, Dockerfile, or requirements change.

---

## CI/CD Setup (For a New Fork)

### 1. Fork the Repository

Fork this repository into your GitHub account.

### 2. Configure GitHub Secrets

Navigate to:

```text
Settings → Secrets and variables → Actions
```

Add the following secrets:

| Secret Name | Value |
|------------|---------|
| DOCKER_USERNAME | jyerramcdocker |
| DOCKER_PASSWORD | Docker Hub Personal Access Token |

### 3. Configure Environments

Navigate to:

```text
Settings → Environments
```

Create:

- `staging`
- `production`

For the production environment:

1. Enable **Required Reviewers**
2. Add yourself as a reviewer

### 4. Trigger Pipeline

- Create a Pull Request → Runs testing and security scans
- Push to `main` → Runs full deployment pipeline

---

## Security Considerations

### Dependency Scanning

`pip-audit` runs during CI and fails the build if vulnerable Python packages are detected.

### Container Image Scanning

`aquasecurity/trivy-action` scans Docker images for:

- Operating system vulnerabilities
- Library/package vulnerabilities

Builds fail on High or Critical vulnerabilities.

### Secret Management

- Docker credentials stored in GitHub Secrets
- No hardcoded credentials
- Environment variables used for application secrets

### Least Privilege Principle

Using `python:3.11-slim` reduces the attack surface by including significantly fewer packages than full Python images.

### Branch Protection

Pull Requests must pass:

- Unit tests
- Security scans

before merging into `main`.

---

## Cost Optimization Measures

### GitHub Actions

- Uses `ubuntu-latest` runners
- Consumes free GitHub Actions minutes efficiently
- Jobs run only for:
  - Pull Requests
  - Pushes to `main`

### Docker Layer Caching

Dockerfile structured as:

```dockerfile
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
```

This allows dependency layers to remain cached unless requirements change.

### Slim Base Image

Benefits:

- Smaller image size
- Faster pull/push operations
- Lower storage usage
- Reduced bandwidth costs

### No Always-On Infrastructure

Deployment jobs are currently simulated.

In a production environment, serverless or on-demand platforms would be preferred, such as:

- AWS ECS Fargate
- Google Cloud Run
- Azure Container Apps

instead of always-running VMs.

### Image Retention

Only the following image tags are pushed:

- `latest`
- `${{ github.sha }}`

Older images can be cleaned automatically using Docker Hub retention policies.

---

## Best Practices Implemented

### 1. Secret Management

All sensitive information is stored in GitHub Encrypted Secrets.

Example:

```yaml
- name: Login to Docker Hub
  uses: docker/login-action@v3
  with:
    username: ${{ secrets.DOCKER_USERNAME }}
    password: ${{ secrets.DOCKER_PASSWORD }}
```

Additional measures:

- No `.env` files committed
- `.env.example` provided for developers
- Production secrets should come from:
  - AWS Secrets Manager
  - HashiCorp Vault
  - Azure Key Vault

### 2. Backup Strategy

#### Source Code Backup

- GitHub repository maintains complete history
- Branch protection prevents accidental force pushes

#### Container Image Backup

Each main branch build publishes:

```text
latest
<github-sha>
```

Rollback can be performed instantly using a previously tagged image.

#### Registry Backup

Images can be mirrored to:

- Amazon ECR
- GitHub Container Registry (GHCR)

for additional redundancy.

#### Workflow Artifacts

The pipeline retains:

- Test reports
- Security scan reports
- Build logs

for auditing and troubleshooting.

### Rollback Example

```bash
docker pull jyerramcdocker/exercise-2-app:<previous-sha>

docker tag \
  jyerramcdocker/exercise-2-app:<previous-sha> \
  jyerramcdocker/exercise-2-app:latest

docker push jyerramcdocker/exercise-2-app:latest
```

---

## Evidence

<img width="1882" height="823" alt="image" src="https://github.com/user-attachments/assets/fd546f59-38a7-4ec7-b498-8065a5209e8b" />


Pull Request execution showing:

- Tests passed
- Security scans passed

<img width="795" height="163" alt="image" src="https://github.com/user-attachments/assets/59964d73-90fa-4be7-bb8b-61166a5c2a5f" />


Push to `main` showing:

- Docker image build successful
- Docker Hub push successful

<img width="1911" height="927" alt="image" src="https://github.com/user-attachments/assets/4a80af6c-bd18-4b94-bc89-1c9ab1b37eb1" />


Production deployment workflow showing:

- Waiting for manual approval
- Approval granted
- Deployment successful

---

## Future Improvements

- Generate and publish Software Bill of Materials (SBOM)
- Deploy to Kubernetes (EKS/AKS/GKE) using Helm charts
- Integrate Dependabot for automated dependency updates
- Add Snyk security scanning
- Implement automated rollback strategies
- Add deployment notifications via Slack or Microsoft Teams

---
