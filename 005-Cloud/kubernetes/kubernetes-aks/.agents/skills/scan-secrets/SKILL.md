---
name: scan-secrets
description: >-
  Scans the repository using scan-secrets.sh to detect and prevent committing
  secrets, passwords, API tokens, private keys, or Azure Subscription/Tenant IDs.
  Use when prompted to scan secrets, check security, or before performing git commit.
---

# Secret & Credential Scanner Skill

Use this skill whenever:
1. The user prompts to scan or verify secrets, tokens, or credentials.
2. An agent or developer is about to stage or commit files using `git commit`.
3. Validating new configuration files or scripts before pushing to remote repositories.

---

## 1. Execution Procedure

From the `kubernetes-aks` workspace directory:

```bash
./scan-secrets.sh
```

Or execute the Python scanner directly:
```bash
python3 ./scan-secrets.py
```

---

## 2. Interpreting Scanner Output

* **Exit Code `0` (Success):**
  ```text
  ✔ SUCCESS: No secrets, credentials, or Azure Subscription IDs found!
  ```
  The workspace is clean. It is safe to proceed with `git add` and `git commit`.

* **Exit Code `1` (Violations Detected):**
  ```text
  ✖ ALERT: Found X potential secret(s) or exposed identifier(s)
  ```
  The scanner outputs:
  - Exact file path and line number
  - Rule name and severity level (`CRITICAL`, `HIGH`, `MEDIUM`)
  - Masked snippet of the matched content

---

## 3. Pre-Commit Enforcement Checklist

Before running any `git commit` command:
1. Execute `./scan-secrets.sh`.
2. If violations are reported:
   - **DO NOT** proceed with `git commit`.
   - Replace raw Azure Subscription IDs or Tenant IDs with `<AZURE_SUBSCRIPTION_ID>` or `<TENANT_ID>`.
   - Replace actual passwords, API keys, or tokens with environment variable references (e.g. `"${MY_SECRET:-}"`).
   - Re-run `./scan-secrets.sh` to confirm 0 findings.
3. Only commit after `./scan-secrets.sh` exits with code `0`.
