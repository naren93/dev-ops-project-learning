# Azure Kubernetes Service (AKS) Lean Lab — Project Summary & Milestone Log

**Project Workspace:** `dev-ops-project-learning/005-Cloud/kubernetes/kubernetes-aks`  
**Git Repository:** `https://github.com/naren93/dev-ops-project-learning.git`  
**Azure Subscription:** `<AZURE_SUBSCRIPTION>` (`<AZURE_SUBSCRIPTION_ID>`)  
**Resource Group:** `rg-ram-aks` (`eastus2`)  
**Container Registry:** `ramacrdotnet.azurecr.io`  
**AKS Cluster:** `aks-cluster-ram`  
**GitOps Namespace:** `argocd` (ArgoCD Server on `https://localhost:8443`)  
**Workload Namespace:** `dev` (`http://localhost:8080/`)  

---

## 1. Registry & Container Images

* **Azure Container Registry (ACR):** Established `ramacrdotnet` in `rg-ram-aks`.
* **Red Hat UBI Non-Root Hardening:**
  * **Problem:** Red Hat UBI images (`ubi8/dotnet-80`, `ubi9/dotnet-100`) run as unprivileged user `UID 1001`. The initial build failed with `Access to the path '/src/obj' is denied` because `/src` had root-only ownership.
  * **Resolution:** Standardized both Dockerfiles on `/opt/app-root/src` with `--chown=1001:0`.
* **Cloud Builds via ACR Tasks:**
  * Built and pushed both container images directly in Azure using `az acr build` (no local Docker daemon required on the host):
    * `ramacrdotnet.azurecr.io/hello-world-api:v8` (.NET 8 minimal API on Port 8080)
    * `ramacrdotnet.azurecr.io/hello-world-api:v10` (.NET 10 minimal API on Port 8080)
* **Idempotency Safeguard:** Provisioning scripts query `az acr repository show` before triggering cloud builds, guaranteeing existing tags are **never redundantly re-compiled**.

---

## 2. Architecture & AKS Cost Optimization

* **Single-Node, Single-Pool Design:**
  * By default, adding a separate user nodepool creates at least 2 VMs (1 system pool + 1 user pool), doubling compute charges.
  * We configured the primary system nodepool (`ramnodepool`) with **1 node** on `Standard_B2s` (2 vCPUs, 4 GiB RAM) on the **Free tier** (`--tier free`).
  * The single node hosts both system components (CoreDNS, metrics, CSI) and application workloads, capping compute costs at ~**$0.04/hour** when running.
* **Direct ACR Attachment:** Configured `--attach-acr ramacrdotnet` during cluster provisioning for managed-identity image pull permissions without image-pull secrets.

---

## 3. GitOps Adoption with ArgoCD (`k8s-gitops/`)

* **ArgoCD Control Plane:** Deployed standard ArgoCD inside the AKS cluster under namespace `argocd`.
* **Kustomize Base & Overlay Hierarchy:**
  * `base/`: Base deployment, cluster service, and kustomization file.
  * `overlays/dev/`: Targets namespace `dev`, overrides image tag (e.g. `v8` or `v10`).
  * `overlays/qa/`: Staged overlay for multi-environment promotion testing.
* **Git Repository Integration:**
  * Connected ArgoCD Application (`hello-world-dev`) directly to the public GitHub repository:
    * Repo: `https://github.com/naren93/dev-ops-project-learning.git`
    * Revision: `main`
    * Path: `005-Cloud/kubernetes/kubernetes-aks/k8s-gitops/overlays/dev`

---

## 4. Zero-Downtime Rolling Updates & High Availability

* **2-Replica Architecture:** Scaled deployment to 2 pods for high availability.
* **RollingUpdate Strategy:**
  ```yaml
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 50%
  ```
  * **50% Guaranteed Availability:** At least 1 pod is actively serving traffic during rollouts.
  * **Readiness Probes:** Configured HTTP probe on `/health`. Kubernetes will not terminate an old pod or route user requests to a new pod until the new pod returns HTTP 200.

---

## 5. Manual Approval Gates & Rollback Support

* **Controlled Deployment Approval:**
  * Removed `syncPolicy.automated` from [`argocd-dev-app.yaml`](file:///Users/rsubramanian/Documents/My_Folder/ProgsFolio/github-saves/dev-ops-project-learning/005-Cloud/kubernetes/kubernetes-aks/argocd-dev-app.yaml).
  * Commits pushed to GitHub transition ArgoCD into **`OutOfSync` (yellow status)**.
  * Operators inspect the exact line-by-line diff (`App Diff`) and click **`SYNC`** to give manual approval.
* **Rollback Capabilities:**
  * **GitOps Revert (Recommended):** Revert commit in Git (`git revert HEAD`), push to GitHub, and click Sync.
  * **ArgoCD UI Rollback:** Instant rollback via the "History and Rollback" menu in ArgoCD dashboard.
  * **Kubernetes Native Rollback:** `kubectl rollout undo deployment/hello-world-api -n dev`.

---

## 6. Automated Daily Lifecycle (Build Up & Tear Down)

We designed a two-tiered lifecycle allowing daily practice while keeping idle cloud compute charges at **$0/hour**:

| Purpose | Command | Highlights |
| :--- | :--- | :--- |
| **Spin Up (Build Up)** | `./provision-ram-aks-resources.sh` | Checks ACR, skips re-builds, creates 1-node cluster, fetches credentials, installs ArgoCD, and applies GitOps app (~3–4 mins). |
| **Inspect Resources** | `./list-ram-aks-resources.sh` | Queries `rg-ram-aks` and managed node groups (`MC_*`), reporting compute vs storage billing state. |
| **Daily Teardown (Build Down)** | `CONFIRM_DESTROY=YES KEEP_ACR=true ./destroy-ram-aks-resources.sh` | Destroys AKS cluster, VMSS, OS disks, and load balancers (**$0/hr compute**). Keeps ACR images intact for fast next spin up. |
| **Full Wipeout** | `CONFIRM_DESTROY=YES ./destroy-ram-aks-resources.sh` | Permanently deletes the resource group `rg-ram-aks` including the registry. |

---

## 7. Security Guardrails & Pre-Commit Scanning

* **Automated Secret Scanner:** Created [`scan-secrets.sh`](file:///Users/rsubramanian/Documents/My_Folder/ProgsFolio/github-saves/dev-ops-project-learning/005-Cloud/kubernetes/kubernetes-aks/scan-secrets.sh) and [`scan-secrets.py`](file:///Users/rsubramanian/Documents/My_Folder/ProgsFolio/github-saves/dev-ops-project-learning/005-Cloud/kubernetes/kubernetes-aks/scan-secrets.py).
* **Policy Enforcement:** Scans all files across the repository before any `git commit` to detect Azure Subscription IDs, Tenant IDs, API tokens, passwords, and private keys.
* **Status:** Scanned 29 repository files with **0 secrets detected**.

---

## 8. Milestone Timeline

- **Milestone 1:** Identified active Azure subscription, created `rg-ram-aks`, and established ACR `ramacrdotnet`.
- **Milestone 2:** Fixed Red Hat UBI non-root permission errors; compiled and pushed both `v8` and `v10` images using ACR Tasks.
- **Milestone 3:** Built automated daily spin-up and tear-down scripts with cost-saving `KEEP_ACR=true` mode.
- **Milestone 4:** Resolved incomplete `~/.kube/config` and ArgoCD CRD annotation size limits via server-side apply.
- **Milestone 5:** Implemented repository-wide secret scanner and pre-commit guardrail rules.
- **Milestone 6:** Migrated workloads to GitOps using Kustomize overlays and deployed ArgoCD inside the AKS cluster.
- **Milestone 7:** Configured zero-downtime rolling update strategy with 50% guaranteed uptime and `/health` readiness probes.
- **Milestone 8:** Configured manual approval gates (disabling auto-sync) to allow visual diff reviews before deployments.
- **Milestone 9:** Connected ArgoCD directly to public GitHub repository; verified end-to-end Git commit ➔ push ➔ OutOfSync ➔ Manual Sync ➔ Zero-Downtime rollout.
- **Milestone 10:** Documented auto-reconnecting port forwarding and multi-environment rollback procedures.

---

## 9. Current System State

* **AKS Cluster:** Active and healthy (`aks-cluster-ram`, 1 VMSS node `Standard_B2s`).
* **Workload Namespace (`dev`):** 2 replicas of `hello-world-api` running `v10` (`ramacrdotnet.azurecr.io/hello-world-api:v10`).
* **GitOps State:** ArgoCD application `hello-world-dev` is **`Synced`** and **`Healthy`** with `https://github.com/naren93/dev-ops-project-learning.git`.
* **Live App Endpoint:** Responding on `http://localhost:8080/` with:
  ```json
  {"message":"Hello from the .NET 10 API","version":"v10"}
  ```
