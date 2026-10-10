#!/usr/bin/env bash
set -euo pipefail

ACR_NAME="${ACR_NAME:-ramacrdotnet}"
NODEPOOL_NAME="ram-nodepool-01"
RESOURCE_GROUP="${RESOURCE_GROUP:-rg-ram-aks}"
LOCATION="${LOCATION:-eastus2}"
AKS_CLUSTER_NAME="${AKS_CLUSTER_NAME:-aks-cluster-ram}"
NODE_VM_SIZE="${NODE_VM_SIZE:-Standard_B2s}"
NODE_COUNT="${NODE_COUNT:-1}"

if [[ -t 1 ]]; then
  BLUE=$'\033[0;34m'
  YELLOW=$'\033[0;33m'
  RED=$'\033[0;31m'
  RESET=$'\033[0m'
else
  BLUE=''
  YELLOW=''
  RED=''
  RESET=''
fi

info() {
  printf '%sINFO%s %s\n' "$BLUE" "$RESET" "$1"
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

info "Ensuring resource group ${RESOURCE_GROUP} exists..."
if ! az group show --name "$RESOURCE_GROUP" >/dev/null 2>&1; then
  az group create \
    --name "$RESOURCE_GROUP" \
    --location "$LOCATION" \
    --output none
fi

info "Ensuring ACR ${ACR_NAME} exists..."
if ! az acr show --name "$ACR_NAME" >/dev/null 2>&1; then
  az acr create \
    --resource-group "$RESOURCE_GROUP" \
    --name "$ACR_NAME" \
    --sku Basic \
    --admin-enabled false \
    --output none
else
  info "ACR ${ACR_NAME} already exists."
fi

info "Checking AKS cluster ${AKS_CLUSTER_NAME}..."
if ! az aks show \
  --resource-group "$RESOURCE_GROUP" \
  --name "$AKS_CLUSTER_NAME" \
  --output none >/dev/null 2>&1; then
  error "AKS cluster ${AKS_CLUSTER_NAME} was not found in ${RESOURCE_GROUP}."
  warn "Set RESOURCE_GROUP to the cluster resource group and rerun."
  exit 1
fi

info "Ensuring node pool ${NODEPOOL_NAME} exists..."
if ! az aks nodepool show \
  --resource-group "$RESOURCE_GROUP" \
  --cluster-name "$AKS_CLUSTER_NAME" \
  --name "$NODEPOOL_NAME" \
  --output none >/dev/null 2>&1; then
  az aks nodepool add \
    --resource-group "$RESOURCE_GROUP" \
    --cluster-name "$AKS_CLUSTER_NAME" \
    --name "$NODEPOOL_NAME" \
    --mode User \
    --node-count "$NODE_COUNT" \
    --node-vm-size "$NODE_VM_SIZE" \
    --os-type Linux \
    --max-pods 30 \
    --output none
else
  info "Node pool ${NODEPOOL_NAME} already exists."
fi

info "Ensuring AKS can pull from ${ACR_NAME}..."
az aks update \
  --resource-group "$RESOURCE_GROUP" \
  --name "$AKS_CLUSTER_NAME" \
  --attach-acr "$ACR_NAME" \
  --output none

info "AKS resources are ready."
printf 'ACR: %s\n' "$ACR_NAME"
printf 'AKS cluster: %s\n' "$AKS_CLUSTER_NAME"
printf 'Node pool: %s (%s, %s node)\n' "$NODEPOOL_NAME" "$NODE_VM_SIZE" "$NODE_COUNT"
