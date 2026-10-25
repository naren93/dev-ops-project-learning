#!/usr/bin/env bash
set -euo pipefail

RESOURCE_GROUP="${RESOURCE_GROUP:-rg-ram-aks}"
AKS_CLUSTER_NAME="${AKS_CLUSTER_NAME:-aks-cluster-ram}"

if [[ -t 1 ]]; then
  BLUE=$'\033[0;34m'
  GREEN=$'\033[0;32m'
  YELLOW=$'\033[0;33m'
  RED=$'\033[0;31m'
  BOLD=$'\033[1m'
  RESET=$'\033[0m'
else
  BLUE=''
  GREEN=''
  YELLOW=''
  RED=''
  BOLD=''
  RESET=''
fi

info() {
  printf '%sINFO%s %s\n' "$BLUE" "$RESET" "$1"
}

command -v az >/dev/null 2>&1 || {
  echo "Azure CLI (az) is required." >&2
  exit 1
}

az account show >/dev/null 2>&1 || {
  echo "Azure CLI is not logged in. Run: az login" >&2
  exit 1
}

printf '\n%s=== Azure Resource Inspection for: %s ===%s\n\n' "$BOLD" "$RESOURCE_GROUP" "$RESET"

if ! az group show --name "$RESOURCE_GROUP" >/dev/null 2>&1; then
  printf '%sResource group %s does not exist.%s\n' "$YELLOW" "$RESOURCE_GROUP" "$RESET"
  echo "All assets in this resource group are destroyed."
  exit 0
fi

info "Resources inside parent group: ${RESOURCE_GROUP}"
RESOURCES="$(az resource list --resource-group "$RESOURCE_GROUP" --query "[].{Name:name, Type:type, Location:location}" -o table)"

if [[ -z "$RESOURCES" ]]; then
  echo "  (No resources found in ${RESOURCE_GROUP})"
else
  echo "$RESOURCES"
fi

echo ""
info "Checking for AKS Node Resource Groups (MC_${RESOURCE_GROUP}_*)..."
NODE_RGS="$(az group list --query "[?starts_with(name, 'MC_${RESOURCE_GROUP}_')].name" -o tsv)"

if [[ -n "$NODE_RGS" ]]; then
  for nrg in $NODE_RGS; do
    printf '%sFound managed node resource group: %s%s\n' "$YELLOW" "$nrg" "$RESET"
    az resource list --resource-group "$nrg" --query "[].{Name:name, Type:type}" -o table
  done
else
  printf '%sNo compute node resource groups found (MC_%s_* is absent).%s\n' "$GREEN" "$RESOURCE_GROUP" "$RESET"
fi

echo ""
printf '%s=== Cost & Teardown Summary ===%s\n' "$BOLD" "$RESET"
HAS_AKS="$(az resource list --resource-group "$RESOURCE_GROUP" --resource-type "Microsoft.ContainerService/managedClusters" --query "[].name" -o tsv 2>/dev/null || true)"
HAS_ACR="$(az resource list --resource-group "$RESOURCE_GROUP" --resource-type "Microsoft.ContainerRegistry/registries" --query "[].name" -o tsv 2>/dev/null || true)"

if [[ -z "$HAS_AKS" && -z "$NODE_RGS" ]]; then
  printf '%s✔ COMPUTE: Inactive ($0/hr). No running VMs, disks, or load balancers.%s\n' "$GREEN" "$RESET"
else
  printf '%s⚠ COMPUTE: Active. AKS cluster / node resources are running.%s\n' "$YELLOW" "$RESET"
fi

if [[ -n "$HAS_ACR" ]]; then
  printf '%s✔ REGISTRY: Preserved (ACR: %s). Images are safely stored for next spin up.%s\n' "$BLUE" "$HAS_ACR" "$RESET"
else
  printf '%s- REGISTRY: Absent (No ACR in %s).%s\n' "$YELLOW" "$RESOURCE_GROUP" "$RESET"
fi
echo ""
