#!/usr/bin/env python3
"""
azure_inventory_hierarchy.py
Read-only Azure Resource Hierarchy, Budget, and Utilization Log Auditor using native Azure Python SDKs.

Outputs:
 - Markdown (.md) report by default (optimal for Git tracking, diffs, and subsequent programmatic updates)
 - Optional HTML (.html) dashboard for rich browser viewing
 - Terminal summary
 - Machine-readable JSON

Authentication:
 - Uses AzureCliCredential from `azure-identity`. Seamlessly leverages your active `az login` context.
 - Strictly READ-ONLY GET operations. No writes or deletes.
"""

import sys
import os
import json
import argparse
import warnings
from datetime import datetime

# Suppress harmless OpenSSL LibreSSL warnings on macOS
warnings.filterwarnings("ignore")

try:
    from azure.identity import AzureCliCredential
    from azure.mgmt.resource import ResourceManagementClient
    from azure.mgmt.network import NetworkManagementClient
    from azure.mgmt.compute import ComputeManagementClient
    from azure.mgmt.consumption import ConsumptionManagementClient
except ImportError as err:
    print(f"Error: Missing required Azure SDK package: {err}", file=sys.stderr)
    print("Please run: pip3 install --user azure-identity azure-mgmt-resource azure-mgmt-network azure-mgmt-compute azure-mgmt-consumption", file=sys.stderr)
    sys.exit(1)


def is_public_ip_orphaned(pip) -> bool:
    has_ipc = bool(pip.ip_configuration)
    has_nat = bool(pip.nat_gateway)
    return not has_ipc and not has_nat


def is_disk_unattached(disk) -> bool:
    disk_state = str(disk.disk_state or "").lower()
    if disk_state:
        return disk_state in ("unattached", "reserved")
    return not disk.managed_by


def fetch_subscription_info(target_sub_id: str = None):
    import subprocess
    cmd = ["az", "account", "show", "--output", "json"]
    if target_sub_id:
        cmd.extend(["--subscription", target_sub_id])
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    acc = json.loads(res.stdout)
    class SubObj:
        def __init__(self, d):
            self.subscription_id = d["id"]
            self.display_name = d["name"]
    return SubObj(acc)


def collect_azure_inventory(subscription_id: str, credential):
    rm_client = ResourceManagementClient(credential, subscription_id)
    net_client = NetworkManagementClient(credential, subscription_id)
    comp_client = ComputeManagementClient(credential, subscription_id)
    cons_client = ConsumptionManagementClient(credential, subscription_id)

    # 1. Resource Groups
    rgs = list(rm_client.resource_groups.list())

    # 2. Resources by RG
    hierarchy = {}
    total_resources = 0
    all_types_summary = {}

    for rg in rgs:
        rg_resources = list(rm_client.resources.list_by_resource_group(rg.name))
        total_resources += len(rg_resources)

        rg_data = {
            "name": rg.name,
            "location": rg.location,
            "resourceCount": len(rg_resources),
            "resources": []
        }

        for res in rg_resources:
            res_type = res.type or "Unknown"
            all_types_summary[res_type] = all_types_summary.get(res_type, 0) + 1
            rg_data["resources"].append({
                "name": res.name,
                "type": res_type,
                "location": res.location,
                "id": res.id,
                # Utilization placeholders ready for metrics ingestion
                "utilization_status": "Active",
                "utilization_metrics": "N/A"
            })

        hierarchy[rg.name] = rg_data

    # 3. Azure Budgets & Spend
    budgets_list = []
    try:
        scope = f"/subscriptions/{subscription_id}"
        budgets_raw = list(cons_client.budgets.list(scope))
        for b in budgets_raw:
            spend_amount = 0.0
            currency = "N/A"
            if b.current_spend:
                spend_amount = getattr(b.current_spend, "amount", 0.0) or 0.0
                currency = getattr(b.current_spend, "unit", "") or ""

            budgets_list.append({
                "name": b.name,
                "amount": b.amount,
                "timeGrain": b.time_grain,
                "category": b.category,
                "currentSpend": spend_amount,
                "unit": currency
            })
    except Exception as e:
        budgets_list = [{"error": str(e)}]

    # 4. Waste Audit: Orphaned IPs & Unattached Disks
    orphaned_pips = []
    try:
        pips = list(net_client.public_ip_addresses.list_all())
        for pip in pips:
            if is_public_ip_orphaned(pip):
                orphaned_pips.append({
                    "name": pip.name,
                    "ipAddress": pip.ip_address or "Unassigned",
                    "location": pip.location,
                    "id": pip.id
                })
    except Exception as e:
        orphaned_pips = [{"error": str(e)}]

    unattached_disks = []
    try:
        disks = list(comp_client.disks.list())
        for disk in disks:
            if is_disk_unattached(disk):
                unattached_disks.append({
                    "name": disk.name,
                    "sizeGb": disk.disk_size_gb,
                    "diskState": disk.disk_state,
                    "location": disk.location,
                    "id": disk.id
                })
    except Exception as e:
        unattached_disks = [{"error": str(e)}]

    return {
        "resourceGroupsCount": len(rgs),
        "totalResourcesCount": total_resources,
        "typeDistribution": all_types_summary,
        "hierarchy": hierarchy,
        "budgets": budgets_list,
        "orphanedPublicIPs": orphaned_pips,
        "unattachedDisks": unattached_disks
    }


def generate_markdown_report(sub_info, data, timestamp: str) -> str:
    md = []
    md.append(f"# Azure Resource Hierarchy & Utilization Audit Log\n")
    md.append(f"- **Subscription Name:** `{sub_info.display_name}`")
    md.append(f"- **Subscription ID:** `{sub_info.subscription_id}`")
    md.append(f"- **Generated At:** `{timestamp}`")
    md.append(f"- **Total Resource Groups:** `{data['resourceGroupsCount']}`")
    md.append(f"- **Total Active Resources:** `{data['totalResourcesCount']}`\n")
    md.append("---\n")

    # 1. Budget Section
    md.append("## 1. Azure Budgets & Current Spend\n")
    if not data["budgets"]:
        md.append("> *No active budgets configured for this subscription.*\n")
    else:
        md.append("| Budget Name | Limit | Current Spend | % Consumed | Time Grain | Category |")
        md.append("| :--- | :--- | :--- | :--- | :--- | :--- |")
        for b in data["budgets"]:
            if "error" in b:
                md.append(f"| (Error fetching budget) | - | - | - | - | `{b['error']}` |")
            else:
                unit = b['unit'] or ''
                curr = b['currentSpend']
                limit = b['amount']
                pct = (curr / limit * 100) if limit > 0 else 0
                md.append(f"| **{b['name']}** | {limit:,.2f} {unit} | {curr:,.2f} {unit} | {pct:.1f}% | {b['timeGrain']} | {b['category']} |")
        md.append("\n")

    # 2. Resource Hierarchy & Utilization Tables
    md.append("## 2. Resource Hierarchy & Utilization Matrix\n")
    md.append("> *Note: This table serves as the audit log. The `Utilization Status` and `Utilization Metrics` columns track active capacity and can be updated across inspection cycles.*\n")

    for rg_name, rg_info in data["hierarchy"].items():
        count = rg_info["resourceCount"]
        loc = rg_info["location"]
        md.append(f"### 📁 Resource Group: `{rg_name}` ({loc}) — `{count}` resources\n")

        if count == 0:
            md.append("*No resources deployed in this resource group (Candidate for cleanup).*\n")
        else:
            md.append("| # | Resource Name | Resource Type | Region | Utilization Status | Utilization Metrics |")
            md.append("| :-: | :--- | :--- | :--- | :--- | :--- |")
            for idx, res in enumerate(rg_info["resources"], 1):
                clean_type = res['type'].replace("Microsoft.", "").replace("microsoft.", "")
                md.append(f"| {idx:02d} | **{res['name']}** | `{clean_type}` | {res['location']} | `{res['utilization_status']}` | {res['utilization_metrics']} |")
            md.append("\n")

    # 3. Waste Audit
    md.append("## 3. FinOps Waste & Idle Resource Audit\n")
    orphans_ip = data["orphanedPublicIPs"]
    unattached_disks = data["unattachedDisks"]

    md.append("### Orphaned Public IPs")
    if not orphans_ip:
        md.append("✅ **No orphaned public IPs detected.**\n")
    else:
        md.append("| Name | IP Address | Region | Resource ID |")
        md.append("| :--- | :--- | :--- | :--- |")
        for pip in orphans_ip:
            md.append(f"| {pip['name']} | `{pip['ipAddress']}` | {pip['location']} | `{pip['id']}` |")
        md.append("\n")

    md.append("### Unattached Managed Disks")
    if not unattached_disks:
        md.append("✅ **No unattached managed disks detected.**\n")
    else:
        md.append("| Name | Size (GB) | State | Region | Resource ID |")
        md.append("| :--- | :--- | :--- | :--- | :--- |")
        for d in unattached_disks:
            md.append(f"| {d['name']} | {d['sizeGb']} GB | `{d['diskState']}` | {d['location']} | `{d['id']}` |")
        md.append("\n")

    md.append("---\n*Audit report generated by Azure Resource Inspector*")
    return "\n".join(md)


def generate_html_report(sub_info, data, timestamp: str) -> str:
    # Rich, self-contained, responsive HTML table report
    rows_budget = ""
    for b in data["budgets"]:
        if "error" in b:
            rows_budget += f"<tr><td colspan='6' style='color:#c00;'>{b['error']}</td></tr>"
        else:
            unit = b['unit'] or ''
            curr = b['currentSpend']
            limit = b['amount']
            pct = (curr / limit * 100) if limit > 0 else 0
            rows_budget += f"""
            <tr>
              <td><strong>{b['name']}</strong></td>
              <td>{limit:,.2f} {unit}</td>
              <td>{curr:,.2f} {unit}</td>
              <td><span class="badge badge-success">{pct:.1f}%</span></td>
              <td>{b['timeGrain']}</td>
              <td>{b['category']}</td>
            </tr>
            """

    rg_sections = ""
    for rg_name, rg_info in data["hierarchy"].items():
        count = rg_info["resourceCount"]
        loc = rg_info["location"]
        if count == 0:
            content = "<p style='color:#777; font-style:italic;'>Empty resource group (No resources deployed).</p>"
        else:
            content = """
            <table class="styled-table">
              <thead>
                <tr>
                  <th style="width: 50px;">#</th>
                  <th>Resource Name</th>
                  <th>Resource Type</th>
                  <th>Region</th>
                  <th>Utilization Status</th>
                  <th>Utilization Metrics</th>
                </tr>
              </thead>
              <tbody>
            """
            for idx, res in enumerate(rg_info["resources"], 1):
                clean_type = res['type'].replace("Microsoft.", "").replace("microsoft.", "")
                content += f"""
                <tr>
                  <td>{idx:02d}</td>
                  <td><strong>{res['name']}</strong></td>
                  <td><code>{clean_type}</code></td>
                  <td>{res['location']}</td>
                  <td><span class="badge badge-active">{res['utilization_status']}</span></td>
                  <td>{res['utilization_metrics']}</td>
                </tr>
                """
            content += "</tbody></table>"

        rg_sections += f"""
        <div class="card">
          <div class="card-header">
            <h3>📁 Resource Group: <code>{rg_name}</code></h3>
            <span class="pill">{loc} &bull; {count} resources</span>
          </div>
          <div class="card-body">
            {content}
          </div>
        </div>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Azure Resource Inventory & Utilization: {sub_info.display_name}</title>
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background-color: #f4f6f9; color: #24292e; margin: 0; padding: 24px; }}
  .container {{ max-width: 1200px; margin: auto; }}
  .header {{ background: #0078d4; color: white; padding: 24px; border-radius: 8px; margin-bottom: 24px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
  .header h1 {{ margin: 0 0 8px 0; font-size: 24px; }}
  .header p {{ margin: 4px 0; font-size: 14px; opacity: 0.9; }}
  .card {{ background: white; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); overflow: hidden; }}
  .card-header {{ padding: 16px 20px; background: #fafbfc; border-bottom: 1px solid #e1e4e8; display: flex; justify-content: space-between; align-items: center; }}
  .card-header h3 {{ margin: 0; font-size: 16px; color: #1f2328; }}
  .pill {{ background: #e1e4e8; color: #444; padding: 4px 10px; border-radius: 12px; font-size: 12px; font-weight: 600; }}
  .card-body {{ padding: 20px; }}
  .styled-table {{ width: 100%; border-collapse: collapse; font-size: 13px; text-align: left; }}
  .styled-table th {{ background-color: #f6f8fa; color: #24292e; padding: 10px 12px; border-bottom: 2px solid #e1e4e8; font-weight: 600; }}
  .styled-table td {{ padding: 10px 12px; border-bottom: 1px solid #eaecef; }}
  .styled-table tr:hover {{ background-color: #f9fbfd; }}
  .badge {{ display: inline-block; padding: 3px 8px; border-radius: 10px; font-size: 11px; font-weight: 600; }}
  .badge-success {{ background: #d4edda; color: #155724; }}
  .badge-active {{ background: #cce5ff; color: #004085; }}
  code {{ font-family: SFMono-Regular, Menlo, Monaco, Consolas, monospace; background: #f0f3f6; padding: 2px 5px; border-radius: 3px; font-size: 12px; }}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>Azure Resource Hierarchy & Utilization Audit Log</h1>
    <p><strong>Subscription:</strong> {sub_info.display_name} (<code>{sub_info.subscription_id}</code>)</p>
    <p><strong>Generated:</strong> {timestamp} &bull; <strong>Resource Groups:</strong> {data['resourceGroupsCount']} &bull; <strong>Total Active Resources:</strong> {data['totalResourcesCount']}</p>
  </div>

  <div class="card">
    <div class="card-header">
      <h3>💰 Azure Budgets & Cost Tracking</h3>
    </div>
    <div class="card-body">
      <table class="styled-table">
        <thead>
          <tr>
            <th>Budget Name</th>
            <th>Limit</th>
            <th>Current Spend</th>
            <th>% Consumed</th>
            <th>Time Grain</th>
            <th>Category</th>
          </tr>
        </thead>
        <tbody>
          {rows_budget if rows_budget else "<tr><td colspan='6'>No budgets found.</td></tr>"}
        </tbody>
      </table>
    </div>
  </div>

  <h2>🏢 Resource Hierarchy & Utilization Matrix</h2>
  {rg_sections}

</div>
</body>
</html>
"""


def main():
    parser = argparse.ArgumentParser(description="Audits Azure resource hierarchy, budgets, and outputs an audit log in Markdown format.")
    parser.add_argument("--subscription", type=str, help="Subscription ID or Name (optional, defaults to active az account).")
    parser.add_argument("--format", choices=["md", "json"], default="md", help="Output format (default: md).")
    parser.add_argument("--output", type=str, help="Custom output file path. Defaults to azure_hierarchy_report.md.")
    parser.add_argument("--mask", action="store_true", default=True, help="Mask subscription ID and name for Git-safe reports (enabled by default).")
    parser.add_argument("--no-mask", dest="mask", action="store_false", help="Do not mask subscription ID and name.")
    args = parser.parse_args()

    credential = AzureCliCredential()

    try:
        sub_info = fetch_subscription_info(args.subscription)
    except Exception as e:
        print(f"Authentication Error: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Auditing subscription: {sub_info.display_name} ({sub_info.subscription_id})...")
    data = collect_azure_inventory(sub_info.subscription_id, credential)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Apply masking if requested
    report_sub_info = sub_info
    if args.mask:
        class MaskedSub:
            def __init__(self, orig):
                self.subscription_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
                self.display_name = "***-SUBSCRIPTION-***"
        report_sub_info = MaskedSub(sub_info)

    if args.format == "json":
        output_data = {
            "subscription": {
                "id": report_sub_info.subscription_id,
                "name": report_sub_info.display_name,
                "auditedAt": timestamp
            },
            **data
        }
        dest = args.output or os.path.join(script_dir, "azure_hierarchy_report.json")
        with open(dest, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2)
        print(f"✅ JSON report written to: {dest}")
        return

    # Generate Markdown (Primary Audit Format)
    md_content = generate_markdown_report(report_sub_info, data, timestamp)
    md_file = args.output if (args.output and args.output.endswith(".md")) else os.path.join(script_dir, "azure_hierarchy_report.md")
    with open(md_file, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"✅ Markdown report written to: {md_file}")

    # --- HTML generation disabled as requested (kept for future reference) ---
    # if args.format in ("html", "both"):
    #     html_content = generate_html_report(sub_info, data, timestamp)
    #     html_file = args.output if (args.output and args.output.endswith(".html")) else os.path.join(script_dir, "azure_hierarchy_report.html")
    #     with open(html_file, "w", encoding="utf-8") as f:
    #         f.write(html_content)
    #     print(f"✅ HTML report written to: {html_file}")


if __name__ == "__main__":
    main()
