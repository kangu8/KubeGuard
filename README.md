# KubeGuard — Kubernetes DevSecOps Platform

> KubeGuard is a hands-on Kubernetes DevSecOps security laboratory featuring a containerized FastAPI application, persistent event storage, automated security scanning, hardened containers and practical network isolation exercises.

## Overview

KubeGuard is a portfolio project focused on learning and demonstrating the operational practices required to deploy, manage, monitor and secure containerized applications in Kubernetes.

The project begins with a reproducible local K3s cluster managed through k3d and will evolve through infrastructure-as-code, automated delivery, GitOps, observability and runtime security.

## Phase 1 — Initial Architecture

```mermaid
flowchart TB
    W[Windows 11 host] --> D[Docker Desktop / WSL 2]
    D --> C[k3d cluster: kubeguard]
    C --> S[K3s server node / control plane]
    C --> A[K3s agent node]
    S --> P1[NGINX Pod]
    A --> P2[NGINX Pod]
    CL[ClusterIP Service: kubeguard-web] --> P1
    CL --> P2
    L[Local browser / localhost:8080] --> F[kubectl port-forward]
    F --> CL
```

> This is a local learning environment, **not** a highly available production cluster. A single control-plane server remains a single point of failure. Kubernetes scheduling placed the two initial Pods on different nodes, but the current manifests do not enforce anti-affinity.

## Technology stack

| Area | Technology | Status |
| --- | --- | --- |
| Container runtime | Docker Desktop / WSL 2 | Implemented |
| Kubernetes distribution | K3s v1.35.5 via k3d v5.9.0 | Implemented |
| Cluster operations | kubectl | Implemented |
| Sample workload | NGINX (2 replicas) | Implemented |
| Kubernetes resources | Namespace, Deployment, ClusterIP Service, readiness probe, resource requests/limits | Implemented |
| CI/CD and image scanning | GitHub Actions, Trivy | Implemented |
| GitOps and packaging | Argo CD, Helm | Planned |
| Network security | Kubernetes NetworkPolicies | Implemented |
| Advanced security | RBAC, Kyverno | Planned |
| Observability | Prometheus, Grafana | Planned |
| Runtime threat detection | Falco | Planned |

## Prerequisites

- Windows with Docker Desktop configured to run Linux containers (WSL 2 backend)
- `k3d` and `kubectl` installed and available in `PATH`
- A terminal with access to Docker Desktop

## Reproduce Phase 1

Clone this repository and run the following commands from its root directory. The cluster name `kubeguard` must be available; if it already exists, reuse it rather than creating a duplicate.

```powershell
k3d cluster create kubeguard --servers 1 --agents 1 --wait --timeout 180s
kubectl config use-context k3d-kubeguard
kubectl get nodes -o wide
kubectl create namespace kubeguard
kubectl apply -f k8s/base/web.yaml
kubectl rollout status deployment/kubeguard-web -n kubeguard --timeout=120s
kubectl get pods,deployments,services -n kubeguard -o wide
```

In a terminal, expose the internal Service to your local machine:

```powershell
kubectl port-forward -n kubeguard svc/kubeguard-web 8080:80
```

Open **http://localhost:8080** and confirm that the NGINX welcome page appears. The port-forward runs until you stop the command (Ctrl+C).

> If the namespace already exists, skip `kubectl create namespace kubeguard`.

## Phase 1 validation

- [x] Docker Desktop and WSL 2 verified
- [x] k3d and kubectl installed
- [x] Two-node K3s cluster created (one server, one agent)
- [x] Kubernetes system Pods verified healthy
- [x] `kubeguard` namespace created
- [x] Two NGINX replicas running and Deployment available
- [x] ClusterIP Service configured
- [x] Application accessed through `kubectl port-forward`
- [x] CLI evidence and browser screenshot captured

### Evidence

| Evidence | File |
| --- | --- |
| Cluster nodes | [`nodes.txt`](evidence/phase-01/nodes.txt) |
| System Pods | [`system-pods.txt`](evidence/phase-01/system-pods.txt) |
| Application resources | [`application.txt`](evidence/phase-01/application.txt) |

![NGINX sample workload accessed locally](evidence/phase-01/nginx-localhost.png)

> Evidence captures represent a point-in-time validation of the lab, not ongoing production monitoring.

## Roadmap

- [x] **Phase 1 — Cluster foundation:** provision Kubernetes, deploy NGINX, capture evidence
- [x] **Phase 2 — Custom application:** develop and containerize a small Python API; Kubernetes manifests and health endpoints
- [x] **Phase 3 — CI pipeline:** automated tests, image builds, Trivy vulnerability scanning
- [x] **Phase 4 — Controlled Kubernetes upgrade:** deploy the hardened Alpine image while preserving SQLite data and the PVC
- [ ] **Planned — GitOps:** Helm charts and Argo CD deployment workflow
- [ ] **Phase 5 — Security controls:** least-privilege RBAC, NetworkPolicies, Kyverno policies
- [ ] **Phase 6 — Observability:** Prometheus metrics and Grafana dashboards
- [ ] **Phase 7 — Threat detection:** controlled Falco detections and documented investigation scenarios
- [ ] **Phase 8 — Portfolio release:** architecture documentation, threat model, demonstrations and lessons learned

## Repository structure

| Directory or file | Description |
|---|---|
| .github/workflows/ | GitHub Actions CI pipeline |
| app/ | FastAPI application and SQLite persistence |
| app/static/ | Security events dashboard |
| k8s/base/ | Kubernetes manifests and Kustomize |
| k8s/scenarios/ | Red Team vs Blue Team laboratory and NetworkPolicies |
| tests/ | Automated API tests |
| evidence/phase-01/ | Cluster foundation evidence |
| evidence/phase-02/ | API deployment evidence |
| evidence/phase-03/ | Container security scan evidence |
| evidence/phase-04/ | Kubernetes upgrade and SQLite persistence evidence |
| evidence/scenario-01-network-isolation/ | Attack and defense validation screenshots |
| Dockerfile | Hardened multistage container build |
| Dockerfile.debian, Dockerfile.alpine, Dockerfile.multistage | Historical build variants |
| requirements.txt, requirements-dev.txt | Python dependencies |

Local SQLite databases, backups and virtual environments are excluded from Git.

## Security and scope notes

KubeGuard is a local DevSecOps security laboratory, **not** a production-ready security monitoring platform. The NGINX deployment remains a baseline lab workload.

Implemented security controls include FastAPI container hardening (non-root execution, read-only root filesystem, seccomp and dropped Linux capabilities), Trivy image vulnerability scanning and Kubernetes NetworkPolicies validated through a Red Team vs Blue Team scenario.

Application-level authentication, comprehensive Kubernetes RBAC, admission policies, GitOps and runtime threat detection remain outside the current implementation.

Before publishing evidence, check the contents of screenshots and terminal captures to avoid exposing tokens, kubeconfig credentials or other sensitive information.

## Learning outcomes

- Kubernetes resource lifecycle, service discovery and scheduling
- Declarative deployments and repeatable validation
- DevSecOps tooling integration across build, deploy and runtime stages (upcoming)
- Clear technical evidence and architecture documentation

## Phase 2 — Security Events API

**Status: Implemented and locally validated**

KubeGuard now includes a Python FastAPI application for collecting and visualizing simulated security events.

### Implemented features

- REST API for security event ingestion and retrieval
- Pydantic request validation
- SQLite event persistence
- Security operations dashboard
- Automated API tests with pytest
- Docker image running as a non-root user
- Kubernetes deployment with readiness and liveness probes
- PersistentVolumeClaim for SQLite storage
- Resource limits and container security contexts

### API endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | / | Application information |
| GET | /health | Health check |
| GET | /ready | Readiness check |
| POST | /events | Create a security event |
| GET | /events | Retrieve security events |
| GET | /dashboard | Security dashboard |

### Run locally with Docker

```bash
docker build -t kubeguard-api:0.3.0 .
docker volume create kubeguard-data
docker run -d --name kubeguard-api -p 127.0.0.1:8001:8000 --mount type=volume,source=kubeguard-data,target=/app/data kubeguard-api:0.3.0
```

Dashboard: http://127.0.0.1:8001/dashboard

### Deploy on Kubernetes

The local development cluster uses k3d.

```bash
k3d image import kubeguard-api:0.3.0 -c kubeguard
kubectl apply -k k8s/base
kubectl rollout status deployment/kubeguard-api -n kubeguard
kubectl port-forward -n kubeguard svc/kubeguard-api 8002:8000
```

Dashboard: http://127.0.0.1:8002/dashboard

### Automated tests

```bash
python -m pytest -v
```

Seven automated tests passed during local validation.


### Security Events Dashboard

Interactive dashboard for reviewing simulated
security events, severity levels and event sources.

<img width="1893" height="888" alt="Captura de pantalla 2026-11-20 135609" src="https://github.com/user-attachments/assets/4b86aff6-0ef6-49aa-af40-6fa4832a82a9" />

### Current limitations

This is a local security laboratory, not a production SOC platform. Events are simulated and the API does not yet implement authentication or authorization.

SQLite currently supports a single API replica. The Kubernetes local-path volume provides persistence within the local cluster, not highly available storage.

Future phases will focus on deploying the hardened image to Kubernetes, GitOps, observability and additional security controls.

## Phase 3 — DevSecOps CI and Container Hardening

**Status: Completed and validated — November 19, 2026**

This phase introduces automated testing, container vulnerability scanning, and security-focused Docker image optimization.

### Continuous Integration — GitHub Actions

The CI pipeline runs automatically on pushes and pull requests targeting the `main` branch.

It consists of two sequential jobs:

1. **Python API Tests**
   - Sets up Python 3.14.
   - Installs development dependencies.
   - Executes seven automated pytest tests.

2. **Docker Build & Security Scan**
   - Builds the application using a multi-stage Dockerfile.
   - Scans the resulting image with Trivy.
   - Checks operating-system and Python dependencies.
   - Fails the CI job when HIGH or CRITICAL vulnerabilities are detected (`exit-code: 1`).

Workflow: [KubeGuard CI](.github/workflows/ci.yml)

### Docker Image Hardening

The original Debian-based image was compared against Alpine-based alternatives.

Security improvements include:

- Alpine Linux as the container base.
- Multi-stage Docker build.
- Isolated Python virtual environment.
- Removal of pip from the final runtime filesystem.
- Non-root execution using UID/GID 10001.
- Reduced runtime dependencies.
- Persistent SQLite storage through a mounted volume.

### Vulnerability Assessment Results

The following results were obtained using Trivy during local validation on November 19, 2026.

| Docker Image | Disk Usage | HIGH | CRITICAL |
|---|---:|---:|---:|
| Debian Slim (original) | 204 MB | 53 | 0 |
| Alpine | 100 MB | 5 | 0 |
| Alpine Hardened | 100 MB | 0 | 0 |
| Alpine Multistage (final) | 100 MB | 0 | 0 |

**Results:**
- Approximately 51% reduction in Docker image disk usage.
- From 53 HIGH findings to 0 detected HIGH findings.
- No HIGH or CRITICAL findings in the final image scan.
- Successful validation of FastAPI, SQLite, and the application dashboard.
- Successful GitHub Actions CI execution with vulnerability blocking enabled.

### Security Considerations

These results reflect known vulnerabilities identified by Trivy at the time of scanning. They do not guarantee that the image is free from all security risks.

The removal of pip from the runtime filesystem does not necessarily remove its contents from underlying Docker image layers.

The project remains a local security laboratory and is not intended as a production-ready security monitoring platform.

### Evidence

- [Original Debian vulnerability report](evidence/phase-03/debian-trivy.json)
- [Hardened Alpine vulnerability report](evidence/phase-03/alpine-hardened-trivy.json)
- [GitHub Actions executions](https://github.com/kangu8/KubeGuard/actions)

### Phase 3 Validation

- [x] Automated Python tests
- [x] GitHub Actions CI
- [x] Docker multi-stage build
- [x] Non-root container execution
- [x] Trivy image vulnerability scanning
- [x] HIGH/CRITICAL vulnerability gate
- [x] Functional validation of the hardened image


### CI Pipeline — Successful Execution

The GitHub Actions pipeline validates the FastAPI
application through automated pytest tests, builds
the hardened Docker image and performs vulnerability
scanning with Trivy.

<img width="1090" height="339" alt="workflows" src="https://github.com/user-attachments/assets/6bc15424-b087-4c6f-96ea-6d1323648318" />


## Phase 4 — Controlled Kubernetes Image Upgrade and SQLite Persistence

### Objective

Deploy the hardened Alpine Multistage container image to the existing Kubernetes cluster while preserving the SQLite database, security controls and persistent storage.

### Deployment upgrade

| Component | Before | After |
|---|---|---|
| Container image | kubeguard-api:0.3.0 | kubeguard-api:0.3.0-final |
| Base image | Debian Slim | Alpine Multistage |
| Deployment replicas | 1 | 1 |
| Update strategy | Recreate | Recreate |
| Persistent storage | 1Gi PVC | Same PVC |
| SQLite events | 3 | 4 |

The new image was imported into both k3d nodes before updating the Kubernetes Deployment.

The image reference was updated in `k8s/base/api.yaml`, preserving the existing Service, PVC, resource limits, security contexts and health probes.

The manifests were validated using Kubernetes server-side dry-run before deployment.

### SQLite backup and recovery preparation

Before performing the upgrade:

1. Created a consistent SQLite backup using Python's `sqlite3.Connection.backup()` API.
2. Copied the backup outside the Kubernetes cluster to the Windows host.
3. Verified database integrity with `PRAGMA integrity_check`.
4. Confirmed that all three original security events were present.

The local backup is stored in `data/backups/kubeguard-pre-upgrade.db` and excluded from Git.

### Persistence validation

After deploying the hardened image:

- The API successfully started with the existing persistent volume.
- SQLite integrity verification returned `ok`.
- All three original event UUIDs were preserved.
- A new synthetic event was successfully written to SQLite.
- The final database contained four events.
- The `/health`, `/ready` and `/events` endpoints responded successfully.
- The security dashboard displayed the new event.

The post-upgrade validation event has the UUID:

`d05292a1-dc02-445c-8bf6-2ac3c4c63d11`

This demonstrates successful application replacement without losing the original SQLite records.

### Kubernetes security controls

The upgraded Deployment retains:

- Non-root execution using UID/GID 10001.
- Read-only container root filesystem.
- Disabled privilege escalation.
- Dropped Linux capabilities.
- RuntimeDefault seccomp profile.
- CPU and memory requests and limits.
- Readiness and liveness probes.
- Persistent volume mounted at `/app/data`.

### Evidence

- [Kubernetes resources after upgrade](evidence/phase-04/kubernetes-after-upgrade.txt)
- [Deployed container image](evidence/phase-04/deployed-image.txt)
- [SQLite persistence verification](evidence/phase-04/sqlite-persistence.txt)

## Final architecture — KubeGuard

The diagram below represents the completed local Kubernetes and DevSecOps laboratory. GitHub Actions validates the code and container image; deployment to k3d is performed manually.

```mermaid
flowchart TB
    subgraph HOST["LOCAL ENVIRONMENT"]
        direction LR
        WIN["Windows 11"] --> DOCKER["Docker Desktop / WSL2"]
        DOCKER --> K3D["k3d cluster: kubeguard"]
        BROWSER["Browser: localhost:8010/dashboard"]
    end

    subgraph K8S["KUBERNETES / K3s - 2 nodes"]
        direction TB
        NODES["K3s server: control plane<br/>K3s agent: worker"]

        subgraph APP["Namespace: kubeguard"]
            direction TB
            WEB_SVC["ClusterIP: kubeguard-web"] --> WEB["NGINX Deployment<br/>2 Pods"]
            API_SVC["ClusterIP: kubeguard-api<br/>TCP 8000"] --> API["FastAPI + security dashboard<br/>kubeguard-api:0.3.0-final"]
            API --> PVC[("PVC 1 GiB<br/>SQLite: kubeguard.db")]

            POLICY["NetworkPolicy<br/>kubeguard-api-ingress"] -.->|"Enforces API Pod ingress"| API
            HARDEN["Container hardening<br/>non-root / read-only root FS<br/>seccomp / drop ALL"] -.-> API
            CLIENT["authorized-client<br/>access=kubeguard-api"] -->|"ALLOWED"| API_SVC
            WEB -.->|"DENIED in test"| API_SVC
        end

        subgraph ATTACK["Namespace: kubeguard-attack"]
            ATTACKER["attacker Pod / curl"]
        end

        ATTACKER -.->|"DENIED"| API_SVC
    end

    K3D --> NODES
    BROWSER -->|"kubectl port-forward 8010:8000"| API_SVC

    subgraph CI["GITHUB ACTIONS - SECURITY CI"]
        direction LR
        REPO["GitHub repository"] --> TESTS["pytest"]
        TESTS --> BUILD["Docker multistage build"]
        BUILD --> TRIVY["Trivy HIGH / CRITICAL gate"]
    end

    MANUAL["Local image build + k3d image import<br/>Manual kubectl apply"] -.->|"Deployment (not CI/CD)"| API

    classDef infrastructure fill:#e0f2fe,stroke:#0284c7,color:#0c4a6e,stroke-width:1.5px
    classDef application fill:#dbeafe,stroke:#2563eb,color:#1e3a8a,stroke-width:1.5px
    classDef storage fill:#f1f5f9,stroke:#64748b,color:#0f172a,stroke-width:1.5px
    classDef security fill:#fef3c7,stroke:#d97706,color:#78350f,stroke-width:1.5px
    classDef allow fill:#dcfce7,stroke:#16a34a,color:#14532d,stroke-width:1.5px
    classDef deny fill:#fee2e2,stroke:#dc2626,color:#7f1d1d,stroke-width:1.5px
    classDef pipeline fill:#f3e8ff,stroke:#9333ea,color:#581c87,stroke-width:1.5px

    class WIN,DOCKER,K3D,BROWSER,NODES infrastructure
    class WEB_SVC,WEB,API_SVC,API application
    class PVC storage
    class POLICY,HARDEN,MANUAL security
    class CLIENT allow
    class ATTACKER deny
    class REPO,TESTS,BUILD,TRIVY pipeline
```

**Traffic legend:** solid arrow = communication/dependency; dashed arrow marked *DENIED* = attempted, blocked connection. The network policy selects the FastAPI Pods, not the ClusterIP Service. The NGINX denial is an intentional security test, not an application dependency.


---

## Red Team vs Blue Team — Kubernetes Security Lab

This practical security scenario demonstrates how
Kubernetes NetworkPolicies can prevent unauthorized
access to internal services through network isolation
and least-privilege controls.

### Attack Scenario

An attacker-controlled Pod was deployed in a
separate namespace (`kubeguard-attack`).

Initially, the attacker successfully accessed the
FastAPI security events endpoint, retrieving four
simulated events without authentication.

### Defense Implementation

Two security configurations were tested:

1. Namespace-based network isolation.
2. Least-privilege NetworkPolicy using trusted Pod labels.

The final policy restricts access to the FastAPI
service while allowing explicitly selected clients.

### Security Validation

| Test | Result |
|---|---|
| Initial unauthorized API access | HTTP 200 OK |
| External attacker after mitigation | Blocked |
| Unauthorized NGINX Pod | Blocked |
| Authorized client | HTTP 200 OK |
| FastAPI health check | Healthy |

### Unauthorized Access Blocked

![NetworkPolicy Attack Blocked](evidence/scenario-01-network-isolation/attacker-blocked.png)

### Authorized Access

![Authorized Client](evidence/scenario-01-network-isolation/authorized-access.png)

### Full Laboratory Documentation

[View the complete Red Team vs Blue Team laboratory](k8s/scenarios/README.md)

**Technologies:** Kubernetes, K3s, k3d, Docker,
NetworkPolicies, FastAPI, Linux and YAML.

**Security note:** NetworkPolicies enforce network
segmentation but do not replace application authentication
or Kubernetes RBAC.
