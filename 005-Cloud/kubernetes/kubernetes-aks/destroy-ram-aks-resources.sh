#!/usr/bin/env bash
set -euo pipefail

ACR_NAME="${ACR_NAME:-ramacrdotnet}"
RESOURCE_GROUP="${RESOURCE_GROUP:-rg-ram-aks}"
CONFIRM_DESTROY="${CONFIRM_DESTROY:-}"

command -v az >/dev/null 2>&1 || {
  echo "Azure CLI (az) is required." >&2
  exit 1
}

az account show >/dev/null 2>&1 || {
  echo "Azure CLI is not logged in. Run: az login" >&2
  exit 1
}

if [[ "$CONFIRM_DESTROY" != "YES" ]]; then
  echo "This deletes resource group ${RESOURCE_GROUP} and its contents." >&2
  echo "To continue, run: CONFIRM_DESTROY=YES $0" >&2
  exit 1
fi

echo "Checking ACR ${ACR_NAME}..."
ACR_RESOURCE_GROUP="$(az acr show \
  --name "$ACR_NAME" \
  --query resourceGroup \
  --output tsv 2>/dev/null || true)"

if [[ -n "$ACR_RESOURCE_GROUP" && "$ACR_RESOURCE_GROUP" != "$RESOURCE_GROUP" ]]; then
  echo "Deleting ACR ${ACR_NAME} from resource group ${ACR_RESOURCE_GROUP}..."
  az acr delete --name "$ACR_NAME" --yes --output none
elif [[ -n "$ACR_RESOURCE_GROUP" ]]; then
  echo "ACR ${ACR_NAME} is inside ${RESOURCE_GROUP}; the resource group deletion will remove it."
else
  echo "ACR ${ACR_NAME} does not exist in the current subscription."
fi

if az group show --name "$RESOURCE_GROUP" >/dev/null 2>&1; then
  echo "Deleting resource group ${RESOURCE_GROUP} and all contained resources..."
  az group delete \
    --name "$RESOURCE_GROUP" \
    --yes \
    --output none
  echo "Resource group ${RESOURCE_GROUP} deleted."
else
  echo "Resource group ${RESOURCE_GROUP} does not exist."
fi
