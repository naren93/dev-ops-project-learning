#!/usr/bin/env bash
set -euo pipefail

ACR_NAME="${ACR_NAME:-ramacrdotnet}"
RESOURCE_GROUP="${RESOURCE_GROUP:-rg-ram-aks}"
AKS_CLUSTER_NAME="${AKS_CLUSTER_NAME:-aks-cluster-ram}"
KEEP_ACR="${KEEP_ACR:-false}"
CONFIRM_DESTROY="${CONFIRM_DESTROY:-}"

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

if [[ "$CONFIRM_DESTROY" != "YES" ]]; then
  warn "This will destroy billable Azure assets in ${RESOURCE_GROUP}."
  if [[ "$KEEP_ACR" == "true" ]]; then
    info "Mode: KEEP_ACR=true (AKS cluster and compute resources deleted; ACR images preserved)."
  else
    info "Mode: Full teardown (AKS cluster, ACR registry, and resource group deleted)."
  fi
  printf '\nTo proceed, run:\n  CONFIRM_DESTROY=YES %s\n' "$0"
  printf 'Or to tear down compute only while preserving ACR images:\n  CONFIRM_DESTROY=YES KEEP_ACR=true %s\n\n' "$0"
  exit 1
fi

# 1. Clean up AKS cluster and associated Node Resource Group (VMSS, Load Balancer, Disks, VNets)
info "Checking for AKS cluster ${AKS_CLUSTER_NAME} in ${RESOURCE_GROUP}..."
if az aks show --resource-group "$RESOURCE_GROUP" --name "$AKS_CLUSTER_NAME" >/dev/null 2>&1; then
  # Find node resource group (e.g., MC_rg-ram-aks_aks-cluster-ram_eastus2)
  NODE_RG="$(az aks show --resource-group "$RESOURCE_GROUP" --name "$AKS_CLUSTER_NAME" --query nodeResourceGroup -o tsv 2>/dev/null || true)"
  
  info "Deleting AKS cluster ${AKS_CLUSTER_NAME} (this stops all VMs, disks, and load balancers)..."
  az aks delete \
    --resource-group "$RESOURCE_GROUP" \
    --name "$AKS_CLUSTER_NAME" \
    --yes \
    --output none
  success "AKS cluster ${AKS_CLUSTER_NAME} deleted."

  # Double-check if the managed node resource group still exists and delete if lingering
  if [[ -n "$NODE_RG" ]] && az group show --name "$NODE_RG" >/dev/null 2>&1; then
    info "Cleaning up residual node resource group ${NODE_RG}..."
    az group delete --name "$NODE_RG" --yes --no-wait --output none || true
  fi
else
  info "AKS cluster ${AKS_CLUSTER_NAME} does not exist."
fi

# Clean up local kubectl context
if command -v kubectl >/dev/null 2>&1; then
  kubectl config delete-context "$AKS_CLUSTER_NAME" >/dev/null 2>&1 || true
  kubectl config delete-cluster "$AKS_CLUSTER_NAME" >/dev/null 2>&1 || true
fi

# 2. Handle ACR and Resource Group
if [[ "$KEEP_ACR" == "true" ]]; then
  success "Kept ACR ${ACR_NAME} intact for future deployments."
  info "All compute assets (VMs, Disks, Load Balancer, Public IPs) have been eliminated."
else
  info "Checking ACR ${ACR_NAME}..."
  ACR_RESOURCE_GROUP="$(az acr show \
    --name "$ACR_NAME" \
    --query resourceGroup \
    --output tsv 2>/dev/null || true)"

  if [[ -n "$ACR_RESOURCE_GROUP" && "$ACR_RESOURCE_GROUP" != "$RESOURCE_GROUP" ]]; then
    info "Deleting standalone ACR ${ACR_NAME} from ${ACR_RESOURCE_GROUP}..."
    az acr delete --name "$ACR_NAME" --yes --output none
    success "ACR ${ACR_NAME} deleted."
  fi

  if az group show --name "$RESOURCE_GROUP" >/dev/null 2>&1; then
    info "Deleting resource group ${RESOURCE_GROUP} and all remaining resources..."
    az group delete \
      --name "$RESOURCE_GROUP" \
      --yes \
      --output none
    success "Resource group ${RESOURCE_GROUP} deleted."
  else
    info "Resource group ${RESOURCE_GROUP} does not exist."
  fi
fi

success "Teardown complete. All active billable resources have been destroyed."
