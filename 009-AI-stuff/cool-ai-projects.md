Here are three 10–15 minute side projects you can build and ship right now, paired with your newly configured `agy` setup:

---

### 1. Build an Ephemeral Cloud Cost Canary (CLI Tool)

Create a single-file Go or Node.js script that queries a mock Azure/AWS billing export or cloud resource JSON and alerts if any unattached disk or idle public IP exceeds a cost threshold.

* **What to test with your new setup:** Run `agy` in an empty directory and prompt:
```text
Create a single-file Node CLI that scans a mock Azure resource list JSON and flags orphaned public IPs and unattached managed disks. Include a sample JSON fixture.

```


* **Why it fits:** Ponytail keeps it to a single script without bloated dependencies, while Caveman skips the preamble so you can run it immediately with `node index.js`.

---

### 2. Auto-Generating Markdown Architecture ADR Generator

A lightweight bash or PowerShell tool that creates structured **Architecture Decision Records (ADRs)** with timestamps, context, alternatives considered, and status tags (`Proposed`, `Accepted`, `Deprecated`).

* **Quick prompt for `agy`:**
```text
Write a shell script `new-adr.sh <title>` that auto-numbers and generates an ADR markdown template into an `docs/adr/` directory with frontmatter metadata.

```


* **Why it's cool:** It instantly standardizes how you document technical spikes or infrastructure choices in your personal Git repos or Obsidian vaults.

---

### 3. SQLite "Fast-Log" Scratchpad with Auto-Vacuum

A tiny CLI scratchpad that writes structured quick thoughts, terminal commands, or debugging snippets into a local SQLite database file with tags and full-text search.

* **Quick prompt for `agy`:**
```text
Build a zero-dependency Python CLI tool `scratch.py` using sqlite3 that supports two commands: add "note text" --tag "devops" and search "query".

```


* **Why it's cool:** It takes under 3 minutes to test, runs anywhere with standard library Python/SQLite, and tests whether Ponytail respects standard library constraints.

---

### 4. Polyglot Secret & Credential Redactor (Pre-Commit Sanitizer)

A polyglot parser and redactor CLI that recursively scans multi-format project files across backend and config ecosystems (`.py`, `.js`, `.ts`, `.go`, `.rs`, `.java`, `.cs`, `.json`, `.yaml`, `.yml`, `.md`, `.env`, `.sh`) to detect and mask API keys, cloud subscription IDs, bearer tokens, private keys, connection strings, and login credentials before Git commits.

* **Quick prompt for `agy`:**
```text
Build a zero-dependency Python CLI tool `secret_redactor.py` that recursively scans a target directory for common secrets (cloud subscription IDs, AWS/Azure keys, JWTs, private keys, connection strings, emails/passwords) across polyglot source code files (.go, .rs, .java, .cs, .py, .js, .ts), configuration (.json, .yaml, .env), shell scripts (.sh), and documentation (.md). It should support two modes: `--dry-run` (report file paths, line numbers, and findings) and `--mask` (in-place redaction with deterministic masked placeholders).
```

* **Why it's cool:** Solves the exact real-world pain point of leaking cloud subscription IDs, auth tokens, or private credentials into public Git repos, while handling Go, Rust, Java, C#, Python, TypeScript, and config formats simultaneously.

