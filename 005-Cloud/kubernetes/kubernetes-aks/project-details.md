# Azure Kubernetes Service (AKS) & GitOps Lab — Project Details

## 1. Executive Summary

This project establishes a production-grade, cost-optimized cloud delivery pipeline on **Azure Kubernetes Service (AKS)** leveraging **GitOps (ArgoCD)** and **Azure Container Registry (ACR)** for containerized .NET minimal APIs (.NET 8 and .NET 10).

The lab is designed specifically for enterprise-grade DevOps practice with an optimized **single-node, single-pool architecture** to minimize cloud compute expenses while enforcing zero-downtime rolling updates, security guardrails, and automated daily build-up/teardown lifecycles.

---

## 2. Workload Specifications

### Application Overview
The application consists of lightweight, high-performance .NET Minimal APIs:
- **`HelloWorldApi-v8`**: Built on .NET 8 LTS (`mcr.microsoft.com/dotnet/aspnet:8.0` / Red Hat UBI 8).
- **`HelloWorldApi-v10`**: Built on .NET 10 Preview (`mcr.microsoft.com/dotnet/aspnet:10.0` / Red Hat UBI 9).

### Endpoints
- `GET /`: Returns JSON payload with application welcome message and version tag:
  ```json
  {"message":"Hello from the .NET 10 API","version":"v10"}
  ```
- `GET /health`: Health probe endpoint returning HTTP 200:
  ```json
  {"status":"healthy"}
  ```

### Non-Root Security Hardening (Red Hat UBI)
- Both container images utilize Red Hat Universal Base Image (UBI) containers running under unprivileged user `UID 1001` (`USER 1001`).
- Source builds and binaries reside in `/opt/app-root/src` with `--chown=1001:0` to eliminate root privilege escalation vulnerabilities and permission denial errors during build/runtime.
- Standardized internal container port binding: `ENV ASPNETCORE_URLS=http://+:8080`.

---

## 3. Infrastructure Architecture

### Cloud Footprint (Cost-Optimized Design)
- **Resource Group:** `rg-ram-aks` (`eastus2`)
- **Container Registry:** `ramacrdotnet.azurecr.io` (Basic SKU, attached directly to AKS via Managed Identity)
- **AKS Cluster:** `aks-cluster-ram`
  - **Tier:** Free Control Plane tier (`--tier free`, $0/hr base fee)
  - **Nodepool:** Single system nodepool `ramnodepool` (1 VM, `Standard_B2s` — 2 vCPUs, 4 GiB RAM)
  - **Single-VM Efficiency:** System pods (CoreDNS, Metrics, CSI drivers) and user application workloads co-exist on the single node, avoiding multi-VM compute bills.

### Compute Lifecycle & Teardown
- **Spin-Up (`./provision-ram-aks-resources.sh`):** Provisions resource group, ACR, builds container images using cloud ACR Tasks (skipping existing tags), provisions AKS, installs ArgoCD, and initializes workloads.
- **Teardown (`CONFIRM_DESTROY=YES KEEP_ACR=true ./destroy-ram-aks-resources.sh`):** Destroys AKS cluster, VM scale sets, disks, and load balancers to achieve **$0/hr compute** when idle, while preserving ACR images for fast spin-up next day.

---

## 4. GitOps Delivery Pipeline (ArgoCD)

### Repository & Structure
- **Public Git Source:** `https://github.com/naren93/dev-ops-project-learning.git`
- **GitOps Root Path:** `005-Cloud/kubernetes/kubernetes-aks/k8s-gitops/`
  - `base/`: Base Kubernetes manifests ([`deployment.yaml`](file:///Users/rsubramanian/Documents/My_Folder/ProgsFolio/github-saves/dev-ops-project-learning/005-Cloud/kubernetes/kubernetes-aks/k8s-gitops/base/deployment.yaml), [`service.yaml`](file:///Users/rsubramanian/Documents/My_Folder/ProgsFolio/github-saves/dev-ops-project-learning/005-Cloud/kubernetes/kubernetes-aks/k8s-gitops/base/service.yaml), [`kustomization.yaml`](file:///Users/rsubramanian/Documents/My_Folder/ProgsFolio/github-saves/dev-ops-project-learning/005-Cloud/kubernetes/kubernetes-aks/k8s-gitops/base/kustomization.yaml))
  - `overlays/dev/`: Development environment overlay configuring namespace `dev` and image tags.
  - `overlays/qa/`: QA environment overlay for multi-stage promotions.

### Deployment & Sync Strategy
- **Manual Approval Gate:** Auto-sync (`syncPolicy.automated`) is intentionally disabled. Commits pushed to GitHub transition ArgoCD into `OutOfSync` (yellow badge), allowing operators to review the line-by-line diff (`App Diff`) and click **`SYNC`** to approve.
- **Zero-Downtime Rolling Update:**
  ```yaml
  replicas: 2
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 50%
  ```
  - Guarantees at least **50% availability (1 healthy replica minimum)** at all times during updates.
  - New pods must pass HTTP readiness probes on `/health` before traffic routes to them or old pods terminate.

---

## 5. Security & Pre-Commit Guardrails

- **Pre-Commit Secret Scanning:**
  - Automated scanner ([`scan-secrets.sh`](file:///Users/rsubramanian/Documents/My_Folder/ProgsFolio/github-saves/dev-ops-project-learning/005-Cloud/kubernetes/kubernetes-aks/scan-secrets.sh) / [`scan-secrets.py`](file:///Users/rsubramanian/Documents/My_Folder/ProgsFolio/github-saves/dev-ops-project-learning/005-Cloud/kubernetes/kubernetes-aks/scan-secrets.py)) checks for Azure Subscription IDs, Tenant IDs, API tokens, passwords, and private keys.
  - Enforced before every git commit via agent rules ([`AGENTS.md`](file:///Users/rsubramanian/Documents/My_Folder/ProgsFolio/github-saves/dev-ops-project-learning/005-Cloud/kubernetes/kubernetes-aks/AGENTS.md) and [`.agents/rules/pre-commit-security.md`](file:///Users/rsubramanian/Documents/My_Folder/ProgsFolio/github-saves/dev-ops-project-learning/005-Cloud/kubernetes/kubernetes-aks/.agents/rules/pre-commit-security.md)).
- **Role-Based Access Control:** ACR attached directly to AKS via Azure Managed Identity, completely eliminating static registry credentials and secrets in Kubernetes manifests.
