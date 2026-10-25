#!/usr/bin/env python3
"""
scan-secrets.py - Security scanner & parser for secrets, tokens, and Azure identifiers.
Scans files in the workspace to ensure credentials, Azure Subscription/Tenant IDs,
tokens, passwords, and private keys are never committed or exposed.
"""

import os
import re
import sys
from pathlib import Path

# ANSI colors for terminal output
RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"
BLUE = "\033[0;34m"
BOLD = "\033[1m"
RESET = "\033[0m"

# Ignored directories and files
IGNORED_DIRS = {
    ".git",
    "bin",
    "obj",
    ".vscode",
    "node_modules",
    "__pycache__",
    ".gemini",
    "scratch",
}

IGNORED_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".ico",
    ".pdf",
    ".tar",
    ".gz",
    ".zip",
    ".exe",
    ".dll",
    ".so",
    ".dylib",
}

# Known benign placeholders to ignore
PLACEHOLDER_ALLOWLIST = {
    "00000000-0000-0000-0000-000000000000",
    "11111111-1111-1111-1111-111111111111",
    "<AZURE_SUBSCRIPTION_ID>",
    "<YOUR_SUBSCRIPTION_ID>",
    "<TENANT_ID>",
    "<CLIENT_SECRET>",
    "<PASSWORD>",
}

# Secret detection rules: (Rule Name, Regex Pattern, Severity)
RULES = [
    (
        "Azure Subscription / Tenant ID (GUID assignment)",
        re.compile(
            r"(?i)(?:subscription[_\s-]?id|tenant[_\s-]?id)\s*[:=]\s*['\"]?([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})['\"]?"
        ),
        "CRITICAL",
    ),
    (
        "Raw GUID (Potential Subscription/Tenant ID)",
        re.compile(
            r"\b(?!(?:00000000|11111111)-)[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b",
            re.IGNORECASE,
        ),
        "HIGH",
    ),
    (
        "Azure Storage Connection String",
        re.compile(
            r"DefaultEndpointsProtocol=[^;]+;AccountName=[^;]+;AccountKey=[^;\s]+",
            re.IGNORECASE,
        ),
        "CRITICAL",
    ),
    (
        "Azure Client Secret / Storage Account Key",
        re.compile(
            r"(?i)(?:accountkey|client[_\s-]?secret|app[_\s-]?key)\s*[:=]\s*['\"]?([A-Za-z0-9+/=]{32,100})['\"]?"
        ),
        "CRITICAL",
    ),
    (
        "Private Key File Header",
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY-----"),
        "CRITICAL",
    ),
    (
        "Generic Password / Secret in Code",
        re.compile(
            r"(?i)(?:password|passwd|secret[_\s-]?key|client[_\s-]?secret)\s*[:=]\s*['\"]([^'\"\s]{8,})['\"]"
        ),
        "HIGH",
    ),
    (
        "API Key / Bearer Token Assignment",
        re.compile(
            r"(?i)(?:api[_\s-]?key|auth[_\s-]?token|bearer[_\s-]?token)\s*[:=]\s*['\"]([^'\"\s]{12,})['\"]"
        ),
        "HIGH",
    ),
    (
        "GitHub Personal Access Token",
        re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{36,255}\b"),
        "CRITICAL",
    ),
    (
        "JSON Web Token (JWT)",
        re.compile(r"\beyJ[A-Za-z0-9-_=]+\.eyJ[A-Za-z0-9-_=]+\.[A-Za-z0-9-_.+/=]+\b"),
        "HIGH",
    ),
    (
        "Personal Email Address",
        re.compile(
            r"\b[A-Za-z0-9._%+-]+@(?!example\.com|noreply|localhost|domain\.com)[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
            re.IGNORECASE,
        ),
        "MEDIUM",
    ),
]


def mask_secret(text: str) -> str:
    """Masks secret characters for safe display."""
    if len(text) <= 6:
        return "***"
    return f"{text[:3]}...{text[-3:]}"


def scan_file(file_path: Path):
    """Scans an individual file line by line."""
    findings = []
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line_no, line in enumerate(f, start=1):
                # Skip comments explaining rules or placeholders
                if any(p in line for p in PLACEHOLDER_ALLOWLIST):
                    continue

                for rule_name, pattern, severity in RULES:
                    matches = pattern.findall(line)
                    if matches:
                        for match in matches:
                            matched_str = match if isinstance(match, str) else match[0] if match else ""
                            # Ignore self-matches inside scanner script itself
                            if file_path.name == "scan-secrets.py":
                                continue
                            if matched_str in PLACEHOLDER_ALLOWLIST:
                                continue

                            findings.append(
                                {
                                    "file": str(file_path),
                                    "line": line_no,
                                    "rule": rule_name,
                                    "severity": severity,
                                    "snippet": line.strip()[:100],
                                    "matched": mask_secret(matched_str) if matched_str else "MATCH",
                                }
                            )
    except Exception as e:
        print(f"{YELLOW}Warning reading {file_path}: {e}{RESET}", file=sys.stderr)

    return findings


def scan_directory(target_dir: Path):
    """Recursively scans the directory."""
    all_findings = []
    file_count = 0

    for root, dirs, files in os.walk(target_dir):
        # Prune ignored directories
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS and not d.startswith(".")]

        for file in files:
            file_path = Path(root) / file
            if file_path.suffix.lower() in IGNORED_EXTENSIONS:
                continue

            file_count += 1
            findings = scan_file(file_path)
            all_findings.extend(findings)

    return file_count, all_findings


def main():
    workspace = Path(__file__).resolve().parent
    print(f"\n{BOLD}=== Azure Secret & Identifier Scanner ==={RESET}")
    print(f"Scanning target: {workspace}\n")

    files_scanned, findings = scan_directory(workspace)

    print(f"Scanned {files_scanned} files across repository.")

    if not findings:
        print(f"\n{GREEN}✔ SUCCESS: No secrets, credentials, or Azure Subscription IDs found!{RESET}\n")
        sys.exit(0)

    print(f"\n{RED}{BOLD}✖ ALERT: Found {len(findings)} potential secret(s) or exposed identifier(s):{RESET}\n")

    for f in findings:
        sev_color = RED if f["severity"] == "CRITICAL" else YELLOW
        print(f"  {sev_color}[{f['severity']}]{RESET} {BOLD}{f['rule']}{RESET}")
        print(f"    File:   {f['file']}:{f['line']}")
        print(f"    Match:  {f['matched']}")
        print(f"    Line:   {f['snippet']}")
        print()

    print(f"{YELLOW}Remediation: Mask raw IDs/secrets with placeholders like <AZURE_SUBSCRIPTION_ID> or use environment variables.{RESET}\n")
    sys.exit(1)


if __name__ == "__main__":
    main()
