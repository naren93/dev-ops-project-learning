# Azure Resource Inspector & FinOps Auditor

A strictly read-only toolkit for auditing Azure resource hierarchies, tracking budgets and spend, and flagging idle waste (unattached managed disks and orphaned public IPs).

---

## 📌 Executive Summary

- **Target Subscription Tested:** `***-SUBSCRIPTION-***` (`xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`)
- **Key Findings:** 8 Resource Groups, 14 active resources, 1 active budget (`budget-contractsai`: 3,000 INR limit, 0.00 INR spend), and 0 orphaned waste.
- **Primary Reporting Format:** Markdown ([`azure_hierarchy_report.md`](azure_hierarchy_report.md)) with built-in `Utilization Status` & `Utilization Metrics` columns to serve as a continuous tracking log (HTML generation disabled/commented out).

---

## 📂 Project Structure & Components

| File | Language / Runtime | Purpose |
| :--- | :--- | :--- |
| [`azure_inventory_hierarchy.py`](azure_inventory_hierarchy.py) | Python 3 (Native Azure SDK) | Audits `Subscription -> RG -> Resource` hierarchy, queries Azure Budgets via `azure-mgmt-consumption`, checks waste, and generates Markdown audit logs. |
| [`azure_orphan_scanner.py`](azure_orphan_scanner.py) | Python 3 (Azure CLI / SDK) | Standalone scanner for orphaned Public IPs and unattached disks via Azure CLI (`--cli`), Azure SDK (`--sdk`), or local file (`--file`). |
| [`azure-orphan-scanner.js`](azure-orphan-scanner.js) | Node.js (Zero deps) | Single-file CLI scanner evaluating mock fixtures and exported ARM JSON for idle IP/disk waste. |
| [`azure-resources.fixture.json`](azure-resources.fixture.json) | JSON | Sample Azure resource list containing attached and orphaned public IPs and disks for offline testing. |
| [`azure_hierarchy_report.md`](azure_hierarchy_report.md) | Markdown | Generated live audit log of your subscription hierarchy, budgets, and utilization matrix. |

---

## ⚙️ Prerequisites

1. **Azure CLI:** Logged in with read access:
   ```bash
   az login
   ```
2. **Python 3 & Native Azure SDKs:**
   ```bash
   pip3 install --user azure-identity azure-mgmt-resource azure-mgmt-network azure-mgmt-compute azure-mgmt-consumption
   ```

---

## 🚀 Usage Guide

### 1. Generate Resource Hierarchy & Utilization Audit Log (Markdown)

```bash
# Scan default active subscription and output azure_hierarchy_report.md
python3 azure_inventory_hierarchy.py

# Specify subscription name or ID explicitly
python3 azure_inventory_hierarchy.py --subscription "<YOUR_SUBSCRIPTION_NAME_OR_ID>"

# Specify custom output path
python3 azure_inventory_hierarchy.py --subscription "<YOUR_SUBSCRIPTION_NAME_OR_ID>" --output ./my_audit_log.md

# Machine-readable JSON export
python3 azure_inventory_hierarchy.py --format json --output ./inventory.json
```

### 2. Orphan Waste Scanner (Python)

```bash
# Live subscription scan via Azure CLI GET commands
python3 azure_orphan_scanner.py --cli

# Scan offline mock fixture
python3 azure_orphan_scanner.py --file azure-resources.fixture.json
```

### 3. Orphan Waste Scanner (Node.js)

```bash
# Scan offline mock fixture
node azure-orphan-scanner.js azure-resources.fixture.json

# Machine-readable JSON output
node azure-orphan-scanner.js azure-resources.fixture.json --json
```

---

## 🔒 Security & Safety Guarantee
All scripts perform **strictly read-only `GET` operations**. No resource creation, modification, or deletion calls exist in this codebase.
