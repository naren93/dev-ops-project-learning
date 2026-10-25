# Azure Kubernetes Service (AKS) Lean Lab

A lean, cost-optimized Kubernetes & GitOps lab for deploying containerized .NET APIs on Azure Kubernetes Service (AKS) with Azure Container Registry (ACR) and ArgoCD.

Designed for DevOps learning with a **single-node, single-pool architecture** to minimize cloud compute costs while maintaining production-grade patterns (GitOps, declarative Kustomize overlays, zero-downtime rolling updates, manual approval gates, and automated daily build-up/tear-down workflows).

---

## Architecture Overview

```
 ┌──────────────────────┐
 │   Developer Push     │
 └──────────┬───────────┘
            │ git push origin main
            ▼
 ┌────────────────────────────────────────────────────────┐
 │   GitHub: naren93/dev-ops-project-learning             │
 │   Path: 005-Cloud/.../k8s-gitops/overlays/dev          │
 └──────────────────────────┬─────────────────────────────┘
                            │ ArgoCD Git Poll
                            ▼
 ┌────────────────────────────────────────────────────────┐
 │              Resource Group: rg-ram-aks                │
 │                                                        │
 │   ┌────────────────────────────────────────────────┐   │
 │   │         Azure Container Registry (ACR)         │   │
 │   │                  ramacrdotnet                  │   │
 │   │   - hello-world-api:v8                         │   │
 │   │   - hello-world-api:v10                        │   │
 │   └────────────────────────┬───────────────────────┘   │
 │                            │ Managed Identity Pull     │
 │                            ▼                           │
 │   ┌────────────────────────────────────────────────┐   │
 │   │             AKS: aks-cluster-ram               │   │
 │   │         (Free Tier, Standard_B2s 1 VM)         │   │
 │   │                                                │   │
 │   │   Namespace: argocd                            │   │
 │   │     └─ ArgoCD Control Plane                    │   │
 │   │     └─ Manual Approval Gate (OutOfSync -> Sync)│   │
 │   │                                                │   │
 │   │   Namespace: dev                               │   │
 │   │     └─ Deployment: hello-world-api (2 pods)    │   │
 │   │     └─ Strategy: RollingUpdate (50% min uptime)│   │
 │   │     └─ Service: ClusterIP on Port 8080         │   │
 │   └────────────────────────────────────────────────┘   │
 └────────────────────────────────────────────────────────┘
```

* **Compute Footprint:** Exactly **1 VM** (`Standard_B2s` — 2 vCPUs, 4 GiB RAM) on the Free AKS control plane tier. The system nodepool handles both control plane agents and application workloads, capping compute costs at ~**$0.04/hour** when running.
* **Image Registry:** Azure Container Registry (Basic SKU) with images built directly in the cloud via ACR Tasks (`az acr build`).
* **GitOps Engine:** ArgoCD runs inside the AKS cluster, pulling declarative manifests directly from GitHub and requiring manual operator approval before applying updates.
* **High Availability & Zero Downtime:** 2 replicas with `RollingUpdate (maxSurge=1, maxUnavailable=50%)` and `/health` readiness probes.

---

## Directory Structure

### 1. Active Workspace Structure

```text
kubernetes-aks/
├── README.md                           # Master documentation and quickstart
├── AGENTS.md                           # Agent guidelines & mandatory pre-commit guardrail
├── architecture-overview.md            # High-level architecture and Mermaid workflow diagram
├── project-summary.md                  # Comprehensive milestone & accomplishment log
├── project-details.md                  # Workload, infrastructure, and GitOps specifications
├── az-k8s-commands-reference.md        # CLI & kubectl commands cheatsheet (quick lookup)
├── provision-ram-aks-resources.sh      # Automated daily spin-up script
├── destroy-ram-aks-resources.sh        # Automated tear-down script (with cost-saving mode)
├── list-ram-aks-resources.sh           # Cloud resource & billing state inspector
├── scan-secrets.sh                     # Pre-commit secret scanning wrapper
├── scan-secrets.py                     # Python engine for secret and identifier scanning
├── argocd-dev-app.yaml                 # ArgoCD Application manifest pointing to GitHub
├── .agents/
│   ├── rules/pre-commit-security.md    # Pre-commit secret scanning rule
│   └── skills/scan-secrets/SKILL.md    # On-demand secret scanner skill
├── HelloWorldApi-v8/                   # .NET 8 minimal API source & Dockerfile
│   ├── Dockerfile
│   ├── HelloWorldApi.csproj
│   ├── Program.cs
│   └── rebuild-and-run.sh
├── HelloWorldApi-v10/                  # .NET 10 minimal API source & Dockerfile
│   ├── Dockerfile
│   ├── HelloWorldApi.csproj
│   ├── Program.cs
│   └── rebuild-and-run.sh
├── k8s-gitops/                         # Declarative GitOps manifests
│   ├── base/                           # Base Kubernetes configuration
│   │   ├── deployment.yaml             # 2 replicas, RollingUpdate, probes, resources
│   │   ├── service.yaml                # ClusterIP service on port 8080
│   │   └── kustomization.yaml          # Base resource definitions
│   └── overlays/
│       ├── dev/                        # Dev environment overlay
│       │   └── kustomization.yaml      # Sets namespace to 'dev' and targets active image tag
│       └── qa/                         # QA environment overlay for promotions
│           └── kustomization.yaml      # Sets namespace to 'qa'
└── k8s/                                # Legacy standalone manifests (reference)
    ├── 00-namespace.yaml
    └── 01-hello-world-api-v8.yaml
```

### 2. Recommended Enterprise Structure (Ready Reckoner for Scale)

When expanding this repository beyond a single lab into multi-service enterprise infrastructure, adopt this modular layout:

```text
kubernetes-aks/
├── README.md                      # Entry point
├── AGENTS.md                      # Agent rules
├── argocd-dev-app.yaml            # ArgoCD application entry
├── k8s-gitops/                    # (KEEP AT ROOT so ArgoCD paths don't break)
│   ├── base/
│   └── overlays/
├── src/                           # Consolidated source code
│   ├── HelloWorldApi-v8/
│   └── HelloWorldApi-v10/
├── scripts/                       # Consolidated bash/python automation
│   ├── provision-resources.sh
│   ├── destroy-resources.sh
│   ├── list-resources.sh
│   └── scan-secrets.sh / .py
└── docs/                          # Consolidated secondary docs
    ├── architecture-overview.md
    ├── project-summary.md
    ├── project-details.md
    └── az-k8s-commands-reference.md
```

---

## Prerequisites

1. **Azure CLI (`az`)**: Installed and logged in (`az login`).
2. **Kubectl (`kubectl`)**: Installed (e.g. `brew install kubectl`).
3. An active Azure subscription (`az account show`).

---

## Daily Lifecycle Workflow

### 1. Spin Up the Environment (Build Up)

Run the provisioning script to set up the infrastructure and initialize ArgoCD:

```bash
./provision-ram-aks-resources.sh
```

**What this does automatically:**
1. Ensures Resource Group `rg-ram-aks` exists.
2. Ensures ACR `ramacrdotnet` exists.
3. Checks if `hello-world-api:v8` and `hello-world-api:v10` exist in ACR:
   - Builds & pushes missing images via Azure ACR Tasks.
   - Skips rebuilding if images are already present.
4. Creates a single-node AKS cluster (`aks-cluster-ram`) if it doesn't exist, and attaches it to `ramacrdotnet`.
5. Merges credentials into `~/.kube/config`.
6. Installs ArgoCD control plane in namespace `argocd`.
7. Applies the GitOps Application manifest ([`argocd-dev-app.yaml`](file:///Users/rsubramanian/Documents/My_Folder/ProgsFolio/github-saves/dev-ops-project-learning/005-Cloud/kubernetes/kubernetes-aks/argocd-dev-app.yaml)).

---

### 2. Access the ArgoCD Dashboard

1. **Port-forward the ArgoCD UI:**
   ```bash
   kubectl port-forward svc/argocd-server -n argocd 8443:443
   ```
2. **Retrieve the admin password:**
   ```bash
   kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo
   ```
3. Open [https://localhost:8443](https://localhost:8443) and log in with username `admin`.

---

### 3. Deploying & Promoting via GitOps

All deployments and promotions are managed through Git commits:

1. **Change the desired image tag:**
   In [`k8s-gitops/overlays/dev/kustomization.yaml`](file:///Users/rsubramanian/Documents/My_Folder/ProgsFolio/github-saves/dev-ops-project-learning/005-Cloud/kubernetes/kubernetes-aks/k8s-gitops/overlays/dev/kustomization.yaml), set `newTag: v10` (or `v8`).
2. **Scan secrets before committing:**
   ```bash
   ./scan-secrets.sh
   ```
3. **Commit and push to GitHub:**
   ```bash
   git commit -am "chore(gitops): promote dev to v10"
   git push origin main
   ```
4. **Manual Approval Gate in ArgoCD:**
   - In the ArgoCD UI, status changes to **`OutOfSync` (Yellow)**.
   - Click **`App Diff`** to inspect the exact lines of YAML changing.
   - Click the blue **`SYNC`** button to approve the zero-downtime rollout.

---

### 4. Testing the Application

#### Auto-Reconnecting Port Forward (Recommended for Local Dev)
Because rolling updates replace old pods with new pods, a single `kubectl port-forward` will disconnect when the old pod shuts down. Run this loop in a terminal tab to stay continuously connected:

```bash
while true; do
  kubectl port-forward -n dev service/hello-world-api 8080:8080
  sleep 1
done
```

Then test in another terminal:
```bash
curl http://localhost:8080/
curl http://localhost:8080/health
```

#### Production Public IP (`type: LoadBalancer`)
To obtain a permanent Azure Public IP instead of port-forwarding, change `type: ClusterIP` to `type: LoadBalancer` in [`k8s-gitops/base/service.yaml`](file:///Users/rsubramanian/Documents/My_Folder/ProgsFolio/github-saves/dev-ops-project-learning/005-Cloud/kubernetes/kubernetes-aks/k8s-gitops/base/service.yaml), commit, and sync in ArgoCD.

---

### 5. Rollback Procedures

- **Option A (GitOps Way — Recommended):**
  Revert the commit in Git and push:
  ```bash
  git revert HEAD
  git push origin main
  ```
  Then click **`SYNC`** in ArgoCD.
- **Option B (ArgoCD UI Emergency Rollback):**
  In the ArgoCD dashboard, click **History and Rollback**, select the previous revision, and click **Rollback**.
- **Option C (Kubernetes CLI Rollback):**
  ```bash
  kubectl rollout undo deployment/hello-world-api -n dev
  kubectl rollout status deployment/hello-world-api -n dev
  ```

---

### 6. Daily Cost-Saving Teardown (Build Down)

When you are done for the day and want to **stop all hourly compute charges ($0/hr)** while keeping your built container images intact:

```bash
CONFIRM_DESTROY=YES KEEP_ACR=true ./destroy-ram-aks-resources.sh
```

**What this deletes:**
* AKS cluster (`aks-cluster-ram`)
* Virtual Machine Scale Set & node VMs
* OS and data disks
* Load balancer & Public IP
* Managed node resource group (`MC_rg-ram-aks_aks-cluster-ram_eastus2`)
* Local `kubectl` cluster context

**What this preserves:**
* ACR `ramacrdotnet` with both `v8` and `v10` image tags.
* Next day spin-up takes only ~3–4 minutes because no images need to be rebuilt.

Confirm the teardown with:
```bash
./list-ram-aks-resources.sh
```

---

### 7. Full Teardown (Complete Wipeout)

To permanently delete everything including the container registry and resource group:

```bash
CONFIRM_DESTROY=YES ./destroy-ram-aks-resources.sh
```
