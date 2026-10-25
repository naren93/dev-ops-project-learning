# Workspace Agent Instructions: AKS Lean Lab

## Security Guardrail: Pre-Commit Secret Scanning

Before executing any `git commit` command or when asked to check security/secrets:
1. Run `./scan-secrets.sh` (or `python3 ./scan-secrets.py`).
2. If any Azure Subscription IDs, Tenant IDs, API tokens, passwords, or keys are detected (exit code 1):
   - **Do not commit.**
   - Prompt the user and replace sensitive data with placeholders like `<AZURE_SUBSCRIPTION_ID>` or environment variables.
3. Only commit once `./scan-secrets.sh` completes cleanly with exit code 0.

Refer to [`.agents/skills/scan-secrets/SKILL.md`](file:///.agents/skills/scan-secrets/SKILL.md) for full details.
