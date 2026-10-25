#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

ACR_NAME="${ACR_NAME:-ramacrdotnet}"
RESOURCE_GROUP="${RESOURCE_GROUP:-rg-ram-aks}"
LOCATION="${LOCATION:-eastus2}"
AKS_CLUSTER_NAME="${AKS_CLUSTER_NAME:-aks-cluster-ram}"
NODEPOOL_NAME="${NODEPOOL_NAME:-ramnodepool}"
NODE_VM_SIZE="${NODE_VM_SIZE:-Standard_B2s}"
NODE_COUNT="${NODE_COUNT:-1}"
K8S_NAMESPACE="${K8S_NAMESPACE:-dev}"

if [[ -t 1 ]]; then
  BLUE=$'\033[0;34m'
  GREEN=$'\033[0;32m'
  YELLOW=$'\033[0;33m'
  RED=$'\033[0;31m'
  RESET=$'\033[0m'
else
  BLUE=''
  GREEN=''
  YELLOW=''
  RED=''
  RESET=''
fi

info() {
  printf '%sINFO%s %s\n' "$BLUE" "$RESET" "$1"
}

success() {
  printf '%sSUCCESS%s %s\n' "$GREEN" "$RESET" "$1"
}

warn() {
  printf '%sWARN%s %s\n' "$YELLOW" "$RESET" "$1" >&2
}

error() {
  printf '%sERROR%s %s\n' "$RED" "$RESET" "$1" >&2
}

command -v az >/dev/null 2>&1 || {
  error "Azure CLI (az) is required."
  exit 1
}

az account show >/dev/null 2>&1 || {
  error "Azure CLI is not logged in. Run: az login"
  exit 1
}

info "Ensuring resource group ${RESOURCE_GROUP} exists in ${LOCATION}..."
if ! az group show --name "$RESOURCE_GROUP" >/dev/null 2>&1; then
  az group create \
    --name "$RESOURCE_GROUP" \
    --location "$LOCATION" \
    --output none
  info "Resource group ${RESOURCE_GROUP} created."
else
  info "Resource group ${RESOURCE_GROUP} already exists."
fi

info "Ensuring ACR ${ACR_NAME} exists in ${RESOURCE_GROUP}..."
if ! az acr show --name "$ACR_NAME" --resource-group "$RESOURCE_GROUP" >/dev/null 2>&1; then
  az acr create \
    --resource-group "$RESOURCE_GROUP" \
    --name "$ACR_NAME" \
    --sku Basic \
    --admin-enabled false \
    --output none
  info "ACR ${ACR_NAME} created."
else
  info "ACR ${ACR_NAME} already exists."
fi

# Step: Ensure v8 and v10 container images exist in ACR without rewriting if already present
info "Checking container images in ${ACR_NAME}..."

if az acr repository show --name "$ACR_NAME" --image "hello-world-api:v8" >/dev/null 2>&1; then
  info "Image hello-world-api:v8 already exists in ${ACR_NAME}. Skipping build."
else
  info "Building and pushing hello-world-api:v8 to ${ACR_NAME} via ACR Tasks..."
  az acr build \
    --registry "$ACR_NAME" \
    --image "hello-world-api:v8" \
    "${SCRIPT_DIR}/HelloWorldApi-v8"
  success "hello-world-api:v8 pushed to ${ACR_NAME}."
fi

if az acr repository show --name "$ACR_NAME" --image "hello-world-api:v10" >/dev/null 2>&1; then
  info "Image hello-world-api:v10 already exists in ${ACR_NAME}. Skipping build."
else
  info "Building and pushing hello-world-api:v10 to ${ACR_NAME} via ACR Tasks..."
  az acr build \
    --registry "$ACR_NAME" \
    --image "hello-world-api:v10" \
    "${SCRIPT_DIR}/HelloWorldApi-v10"
  success "hello-world-api:v10 pushed to ${ACR_NAME}."
fi

# Step: Ensure single-nodepool AKS cluster exists
info "Ensuring single-nodepool AKS cluster ${AKS_CLUSTER_NAME} exists..."
if ! az aks show --resource-group "$RESOURCE_GROUP" --name "$AKS_CLUSTER_NAME" >/dev/null 2>&1; then
  info "Creating single-nodepool AKS cluster ${AKS_CLUSTER_NAME}..."
  info "Settings: nodepool=${NODEPOOL_NAME}, size=${NODE_VM_SIZE}, count=${NODE_COUNT}, tier=free, attached to ${ACR_NAME}."
  az aks create \
    --resource-group "$RESOURCE_GROUP" \
    --name "$AKS_CLUSTER_NAME" \
    --location "$LOCATION" \
    --tier free \
    --nodepool-name "$NODEPOOL_NAME" \
    --node-vm-size "$NODE_VM_SIZE" \
    --node-count "$NODE_COUNT" \
    --os-sku Ubuntu \
    --generate-ssh-keys \
    --attach-acr "$ACR_NAME" \
    --output none
  success "AKS cluster ${AKS_CLUSTER_NAME} created."
else
  info "AKS cluster ${AKS_CLUSTER_NAME} already exists."
  info "Ensuring AKS is attached to ${ACR_NAME}..."
  az aks update \
    --resource-group "$RESOURCE_GROUP" \
    --name "$AKS_CLUSTER_NAME" \
    --attach-acr "$ACR_NAME" \
    --output none
fi

# Step: Fetch credentials and configure namespace + manifests
info "Fetching cluster credentials for kubectl..."
if [[ -f ~/.kube/config ]] && ! grep -q 'clusters:' ~/.kube/config 2>/dev/null; then
  warn "Existing ~/.kube/config was incomplete/invalid; backed up to ~/.kube/config.bak"
  cp ~/.kube/config ~/.kube/config.bak 2>/dev/null || true
  rm -f ~/.kube/config
fi

az aks get-credentials \
  --resource-group "$RESOURCE_GROUP" \
  --name "$AKS_CLUSTER_NAME" \
  --overwrite-existing

if command -v kubectl >/dev/null 2>&1; then
  # Ensure namespace dev exists
  info "Ensuring namespace '${K8S_NAMESPACE}' exists..."
  kubectl create namespace "$K8S_NAMESPACE" --dry-run=client -o yaml | kubectl apply -f -

  # Step: Ensure ArgoCD is installed
  info "Ensuring ArgoCD is installed in 'argocd' namespace..."
  kubectl create namespace argocd --dry-run=client -o yaml | kubectl apply -f -
  kubectl apply --server-side --force-conflicts -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

  if [[ -f "${SCRIPT_DIR}/argocd-dev-app.yaml" ]]; then
    info "Ensuring ArgoCD dev application is configured..."
    kubectl apply -f "${SCRIPT_DIR}/argocd-dev-app.yaml" || true
  fi
fi

info "AKS environment, workloads, and ArgoCD are ready."
printf 'ACR: %s (contains hello-world-api:v8 and hello-world-api:v10)\n' "$ACR_NAME"
printf 'AKS cluster: %s\n' "$AKS_CLUSTER_NAME"
printf 'Single Node pool: %s (%s, %s node)\n' "$NODEPOOL_NAME" "$NODE_VM_SIZE" "$NODE_COUNT"
printf 'Namespace: %s (v8 running)\n' "$K8S_NAMESPACE"
printf 'GitOps: ArgoCD running in namespace "argocd"\n'
