# Pre-Commit Security & Secret Prevention Rule

Always enforce security scanning before performing any Git commit operation.

## Mandatory Guardrail

Before executing any `git commit` command:
1. Always run `./scan-secrets.sh` from the `kubernetes-aks` directory first.
2. If `./scan-secrets.sh` returns exit code 1 or identifies any secrets, Azure Subscription IDs, or credentials:
   - **HALT** the commit immediately.
   - Do not stage or commit the affected files.
   - Inform the user of the flagged items and sanitize them using placeholders (e.g., `<AZURE_SUBSCRIPTION_ID>`) or environment variables.
   - Re-run `./scan-secrets.sh` to confirm zero violations before proceeding.
