#!/usr/bin/env python3
"""
azure_orphan_scanner.py
Read-only scanner for orphaned Azure resources (Public IPs and unattached Managed Disks).

Modes supported:
 1. Live mode via Azure CLI (`az`):
    Uses your existing `az login` context. Calls subscription-level Azure ARM REST GET
    endpoints via `az rest` (strictly read-only `GET` operations across the entire subscription).
 2. Live mode via Azure Python SDK (`azure-mgmt-network`, `azure-mgmt-compute`, `azure-identity`):
    Uses `DefaultAzureCredential` or `AzureCliCredential` to make direct REST GET calls.
 3. Offline / Mock mode:
    Scans a local JSON file or the fixture.

Zero state changes. Strictly read-only audit.
"""

import sys
import json
import argparse
import subprocess
from typing import Dict, Any, List, Optional


def check_sdk_availability() -> bool:
    try:
        import azure.identity  # noqa: F401
        import azure.mgmt.network  # noqa: F401
        import azure.mgmt.compute  # noqa: F401
        return True
    except ImportError:
        return False


def run_az_cli_command(args: List[str]) -> Any:
    cmd = ["az"] + args + ["--output", "json"]
    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except FileNotFoundError:
        print("Error: 'az' CLI binary not found in PATH.", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error executing Azure CLI: {e.stderr.strip()}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error parsing Azure CLI JSON output: {e}", file=sys.stderr)
        sys.exit(1)


def get_current_subscription() -> Dict[str, str]:
    data = run_az_cli_command(["account", "show"])
    return {
        "id": data.get("id", ""),
        "name": data.get("name", ""),
        "tenantId": data.get("tenantId", "")
    }


def is_public_ip_orphaned(pip: Dict[str, Any]) -> bool:
    props = pip.get("properties") or pip
    ip_config = props.get("ipConfiguration")
    nat_gw = props.get("natGateway")

    has_ip_config = bool(ip_config and (ip_config.get("id") if isinstance(ip_config, dict) else ip_config))
    has_nat_gw = bool(nat_gw and (nat_gw.get("id") if isinstance(nat_gw, dict) else nat_gw))

    return not has_ip_config and not has_nat_gw


def is_disk_unattached(disk: Dict[str, Any]) -> bool:
    props = disk.get("properties") or disk
    disk_state = str(props.get("diskState") or "").lower()
    managed_by = props.get("managedBy")

    if disk_state:
        return disk_state in ("unattached", "reserved")
    return not managed_by


def fetch_via_az_rest(sub_id: str):
    """
    Query subscription-wide ARM endpoints via `az rest`.
    This performs strictly GET requests and works across all resource groups in the subscription.
    """
    pip_url = f"https://management.azure.com/subscriptions/{sub_id}/providers/Microsoft.Network/publicIPAddresses?api-version=2023-11-01"
    disk_url = f"https://management.azure.com/subscriptions/{sub_id}/providers/Microsoft.Compute/disks?api-version=2023-10-02"

    pip_res = run_az_cli_command(["rest", "--method", "get", "--url", pip_url])
    disk_res = run_az_cli_command(["rest", "--method", "get", "--url", disk_url])

    pips = pip_res.get("value", []) if isinstance(pip_res, dict) else (pip_res if isinstance(pip_res, list) else [])
    disks = disk_res.get("value", []) if isinstance(disk_res, dict) else (disk_res if isinstance(disk_res, list) else [])

    return pips, disks


def fetch_via_azure_sdk(subscription_id: str):
    from azure.identity import AzureCliCredential, DefaultAzureCredential
    from azure.mgmt.network import NetworkManagementClient
    from azure.mgmt.compute import ComputeManagementClient

    try:
        credential = AzureCliCredential()
    except Exception:
        credential = DefaultAzureCredential()

    network_client = NetworkManagementClient(credential, subscription_id)
    compute_client = ComputeManagementClient(credential, subscription_id)

    # Strictly read-only list calls (GET)
    pips = [pip.as_dict() for pip in network_client.public_ip_addresses.list_all()]
    disks = [disk.as_dict() for disk in compute_client.disks.list()]

    return pips, disks


def parse_mock_file(filepath: str):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, list):
        items = data
    elif isinstance(data, dict):
        items = data.get("value") or data.get("data") or []
    else:
        items = []

    pips = [item for item in items if (item.get("type") or "").lower() == "microsoft.network/publicipaddresses"]
    disks = [item for item in items if (item.get("type") or "").lower() == "microsoft.compute/disks"]
    return pips, disks


def format_report(orphaned_pips: List[Dict[str, Any]], unattached_disks: List[Dict[str, Any]], meta: Dict[str, Any], as_json: bool):
    if as_json:
        report = {
            "metadata": meta,
            "summary": {
                "orphanedPublicIPsCount": len(orphaned_pips),
                "unattachedDisksCount": len(unattached_disks),
                "totalOrphans": len(orphaned_pips) + len(unattached_disks)
            },
            "orphanedPublicIPs": orphaned_pips,
            "unattachedDisks": unattached_disks
        }
        print(json.dumps(report, indent=2))
        return

    print("==========================================================")
    print("       AZURE RESOURCE ORPHAN SCANNER (PYTHON READ-ONLY)   ")
    print("==========================================================")
    print(f"Mode         : {meta.get('mode')}")
    if meta.get("subscription"):
        print(f"Subscription : {meta['subscription']['name']} ({meta['subscription']['id']})")
    if meta.get("file"):
        print(f"Source File  : {meta['file']}")
    print("==========================================================\n")

    print(f"🚩 Orphaned Public IPs ({len(orphaned_pips)}):")
    if not orphaned_pips:
        print("   ✅ None found.")
    else:
        for idx, pip in enumerate(orphaned_pips, 1):
            name = pip.get("name", "unnamed")
            props = pip.get("properties") or pip
            ip_addr = props.get("ipAddress") or "Unassigned"
            rg = pip.get("resourceGroup") or pip.get("id", "").split("/resourceGroups/")[-1].split("/")[0] if "/resourceGroups/" in pip.get("id", "") else "N/A"
            loc = pip.get("location", "N/A")
            res_id = pip.get("id", "N/A")
            print(f"   {idx}. [{name}]")
            print(f"      IP Address     : {ip_addr}")
            print(f"      Resource Group : {rg}")
            print(f"      Location       : {loc}")
            print(f"      Resource ID    : {res_id}")

    print(f"\n🚩 Unattached Managed Disks ({len(unattached_disks)}):")
    if not unattached_disks:
        print("   ✅ None found.")
    else:
        for idx, disk in enumerate(unattached_disks, 1):
            name = disk.get("name", "unnamed")
            props = disk.get("properties") or disk
            size = props.get("diskSizeGb") or props.get("diskSizeGB") or "N/A"
            state = props.get("diskState") or "Unattached"
            rg = disk.get("resourceGroup") or disk.get("id", "").split("/resourceGroups/")[-1].split("/")[0] if "/resourceGroups/" in disk.get("id", "") else "N/A"
            loc = disk.get("location", "N/A")
            res_id = disk.get("id", "N/A")
            print(f"   {idx}. [{name}]")
            print(f"      Size           : {size} GB")
            print(f"      State          : {state}")
            print(f"      Resource Group : {rg}")
            print(f"      Location       : {loc}")
            print(f"      Resource ID    : {res_id}")

    total = len(orphaned_pips) + len(unattached_disks)
    print("\n==========================================================")
    if total > 0:
        print(f"⚠️  Action recommended: {total} idle resource(s) found.")
    else:
        print("✅ No orphaned resources found in this subscription!")
    print("==========================================================")


def main():
    parser = argparse.ArgumentParser(
        description="Strictly read-only Azure scanner for orphaned Public IPs and unattached Managed Disks."
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--cli", action="store_true", help="Fetch live data via Azure CLI (az command).")
    group.add_argument("--sdk", action="store_true", help="Fetch live data using Azure Python SDK (azure-mgmt-*).")
    group.add_argument("--file", type=str, help="Scan an offline mock JSON fixture or resource export file.")

    parser.add_argument("--subscription", type=str, help="Specific subscription ID (defaults to current active az account).")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format.")

    args = parser.parse_args()

    mode = "file" if args.file else ("sdk" if args.sdk else "cli")
    meta: Dict[str, Any] = {"mode": mode}

    if mode == "file":
        meta["file"] = args.file
        pips, disks = parse_mock_file(args.file)
    elif mode == "sdk":
        if not check_sdk_availability():
            print("Error: Azure SDK packages are not installed in the current environment.", file=sys.stderr)
            print("Run: pip install azure-identity azure-mgmt-network azure-mgmt-compute", file=sys.stderr)
            sys.exit(1)
        sub_info = get_current_subscription()
        sub_id = args.subscription or sub_info["id"]
        meta["subscription"] = sub_info
        pips, disks = fetch_via_azure_sdk(sub_id)
    else:  # mode == "cli"
        sub_info = get_current_subscription()
        sub_id = args.subscription or sub_info["id"]
        meta["subscription"] = sub_info
        pips, disks = fetch_via_az_rest(sub_id)

    orphaned_pips = [p for p in pips if is_public_ip_orphaned(p)]
    unattached_disks = [d for d in disks if is_disk_unattached(d)]

    format_report(orphaned_pips, unattached_disks, meta, as_json=args.json)


if __name__ == "__main__":
    main()
