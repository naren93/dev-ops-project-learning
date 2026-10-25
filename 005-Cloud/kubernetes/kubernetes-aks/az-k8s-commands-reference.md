# Azure CLI & Kubernetes Quick Reference Cheatsheet

A categorized reference of exact, pre-validated Azure CLI (`az`) and `kubectl` commands tailored for this AKS & GitOps lab. Use this reference to avoid syntax lookup, exploratory CLI calls, and token overhead.

---

## 1. Account & Subscription Management

```bash
# Check current logged-in account, tenant, and active subscription
az account show --query "{Subscription:name, SubId:id, TenantId:tenantId, User:user.name}" -o table

# List all available subscriptions
az account list --query "[].{Name:name, ID:id, IsDefault:isDefault, State:state}" -o table

# Switch active subscription
az account set --subscription "<AZURE_SUBSCRIPTION>"
```

---

## 2. Resource & Cost Auditing (Subscription-Wide)

```bash
# List all active resources across the entire subscription (names, groups, types)
az resource list --query "[].{Name:name, RG:resourceGroup, Type:type}" -o table

# List resources specifically in the lab group (rg-ram-aks)
az resource list --resource-group rg-ram-aks --query "[].{Name:name, Type:type, Location:location}" -o table

# Find AKS-managed Node Resource Groups (where VMSS, Disks, Load Balancer live)
az group list --query "[?starts_with(name, 'MC_rg-ram-aks_')].name" -o tsv

# Inspect VM Scale Set (Compute) in the node resource group
az vmss list --query "[].{Name:name, SKU:sku.name, Capacity:sku.capacity, RG:resourceGroup}" -o table
```

---

## 3. Azure Container Registry (ACR) (`ramacrdotnet`)

```bash
# Verify if ACR exists
az acr show --name ramacrdotnet --resource-group rg-ram-aks --query "{Name:name, LoginServer:loginServer, SKU:sku.name}" -o json

# Build and push an image in the cloud via ACR Tasks (no local Docker daemon required)
az acr build --registry ramacrdotnet --image hello-world-api:v8 ./HelloWorldApi-v8
az acr build --registry ramacrdotnet --image hello-world-api:v10 ./HelloWorldApi-v10

# List all repositories in the registry
az acr repository list --name ramacrdotnet -o table

# List tags for a repository
az acr repository show-tags --name ramacrdotnet --repository hello-world-api -o json

# Idempotency check: test if a specific tag exists (returns exit code 0 if exists)
az acr repository show --name ramacrdotnet --image hello-world-api:v8 >/dev/null 2>&1 && echo "Exists" || echo "Missing"

# Delete a specific image tag
az acr repository delete --name ramacrdotnet --image hello-world-api:v8 --yes
```

---

## 4. Azure Kubernetes Service (AKS) (`aks-cluster-ram`)

```bash
# Create single-nodepool, single-node cluster (Standard_B2s, Free tier, attached to ACR)
az aks create \
  --resource-group rg-ram-aks \
  --name aks-cluster-ram \
  --location eastus2 \
  --tier free \
  --nodepool-name ramnodepool \
  --node-vm-size Standard_B2s \
  --node-count 1 \
  --os-sku Ubuntu \
  --generate-ssh-keys \
  --attach-acr ramacrdotnet \
  --output none

# Check cluster state and power status
az aks show --resource-group rg-ram-aks --name aks-cluster-ram --query "{Name:name, Status:provisioningState, Power:powerState.code, K8sVersion:kubernetesVersion}" -o json

# Attach ACR to an existing cluster
az aks update --resource-group rg-ram-aks --name aks-cluster-ram --attach-acr ramacrdotnet --output none

# Stop the cluster (pauses VM billing without deleting cluster definition)
az aks stop --resource-group rg-ram-aks --name aks-cluster-ram

# Start a stopped cluster
az aks start --resource-group rg-ram-aks --name aks-cluster-ram

# Merge cluster credentials into ~/.kube/config
az aks get-credentials --resource-group rg-ram-aks --name aks-cluster-ram --overwrite-existing

# Delete cluster (destroys VMs, VMSS, Disks, and node resource group)
az aks delete --resource-group rg-ram-aks --name aks-cluster-ram --yes --output none
```

---

## 5. Kubernetes & Workload Management (`kubectl`)

```bash
# Check cluster node status
kubectl get nodes -o wide

# Check all resources in the 'dev' namespace
kubectl get all -n dev

# Inspect pods with container images
kubectl get pods -n dev -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.containers[*].image}{"\n"}{end}'

# Auto-reconnecting port forward (recovers automatically across rolling deployments)
while true; do kubectl port-forward -n dev service/hello-world-api 8080:8080; sleep 1; done

# Execute curl directly inside pod
kubectl exec -n dev deployment/hello-world-api -- curl -s http://localhost:8080/
kubectl exec -n dev deployment/hello-world-api -- curl -s http://localhost:8080/health

# View pod logs
kubectl logs -n dev deployment/hello-world-api --tail=50 -f

# Force restart pods
kubectl rollout restart deployment/hello-world-api -n dev

# Rollback deployment to previous replica set
kubectl rollout undo deployment/hello-world-api -n dev

# View rollout status and history
kubectl rollout status deployment/hello-world-api -n dev
kubectl rollout history deployment/hello-world-api -n dev
```

---

## 6. GitOps & ArgoCD Operations

```bash
# Check all ArgoCD control plane pods
kubectl get pods -n argocd

# Retrieve ArgoCD initial admin password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo

# Port-forward ArgoCD UI (https://localhost:8443)
kubectl port-forward svc/argocd-server -n argocd 8443:443

# Check ArgoCD application sync status and health
kubectl get applications -n argocd
kubectl get application -n argocd hello-world-dev -o jsonpath='Sync: {.status.sync.status}, Health: {.status.health.status}{"\n"}'

# Preview Kustomize build locally before pushing
kubectl kustomize k8s-gitops/overlays/dev

# Server-side apply ArgoCD manifests (avoids CRD 256KB annotation limits)
kubectl apply --server-side --force-conflicts -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Apply or update the GitOps application definition
kubectl apply -f argocd-dev-app.yaml
```

---

## 7. Security & Pre-Commit Scanning

```bash
# Run security scanner across all repository files
./scan-secrets.sh

# Run Python scanner directly
python3 ./scan-secrets.py
```

---

## 8. Lab Lifecycle Scripts Quick Reference

| Purpose | Command |
| :--- | :--- |
| **Inspect Assets & Billing** | `./list-ram-aks-resources.sh` |
| **Scan Secrets & Identifiers** | `./scan-secrets.sh` |
| **Full Spin-Up (AKS + ACR + ArgoCD)** | `./provision-ram-aks-resources.sh` |
| **Daily Teardown ($0/hr Compute, Keep ACR)** | `CONFIRM_DESTROY=YES KEEP_ACR=true ./destroy-ram-aks-resources.sh` |
| **Complete Destruction (All Resources)** | `CONFIRM_DESTROY=YES ./destroy-ram-aks-resources.sh` |
