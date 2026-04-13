# ProgsFolio: Cloud-Native & DevOps Portfolio

Welcome to my professional engineering portfolio. This repository tracks my journey across development, infrastructure-as-code, and system orchestration, with a strict focus on **architectural purity** and **minimal-storage development workflows**.

## 🏗️ Core Philosophy: The Ultra-Clean Docker Workflow
To maintain a high-performance development environment on storage-limited hardware, this portfolio follows a **Docker-First** mandate:
- **Zero Host Bloat:** No local installation of Node.js, npm, or global CLIs.
- **Hidden Dependencies:** Project dependencies (`node_modules`) live in named Docker volumes, invisible to the host filesystem.
- **Shared LTS Volumes:** Multiple projects of the same version reuse standardized Docker volumes to minimize redundant storage.

---

## 📂 Portfolio Roadmap

### [001-Angular](./001-Angular)
**The Documentation Portal.** An Angular 21 project that serves as its own technical manual. It demonstrates containerized frontend development and a "no-nonsense" approach to delivering value.

### [002-Python](./002-Python)
**Engineering Foundations.** A comprehensive collection of Python, Java, and C++ implementations. Covers 100 days of coding, Data Structures & Algorithms (DSA), and automation scripts.

### [004-Scripting](./004-Scripting)
**System Automation.** Practical shell scripting and system-level "glue" code that automates repetitive tasks and optimizes environment setup.

### [005-Cloud](./005-Cloud)
**Infrastructure & Orchestration.** The "Heavy Hitter" section featuring:
- **Kubernetes:** CKA-level deployments and service definitions.
- **Terraform:** Modularized Infrastructure-as-Code (IaC) for Azure.
- **CI/CD:** Jenkins pipelines and GitLab CI workflows.

### [007-Git](./007-Git)
**Cloud-Native Standards.** Implementation of the **12-Factor App** principles and best practices for version control and containerized deployment.

### [008-DBMS](./008-DBMS)
**Persistence Layer.** Practical guides and setup scripts for PostgreSQL and database management on macOS.

### [personal-knowledge-bank](./personal-knowledge-bank)
**Architectural Ledger.** The strategic core of the portfolio, containing:
- [Ultra-Clean Docker Setup](./personal-knowledge-bank/angular-docker-setup.md)
- [Performance Assessment Reports](./personal-knowledge-bank/performance-report.md)
- [Interview Preparation Plans](./personal-knowledge-bank/InterviewPrepPlan.txt)

---

## 🚀 Quick Start: Run the Documentation Portal
To see my "Ultra-Clean" Angular setup in action:
```bash
docker run -d --name angular-docs \
  -p 4200:4200 \
  -v "$(pwd)/001-Angular/001-Hello-world:/app" \
  -v angular-21-lts-modules:/app/node_modules \
  -w /app \
  node:22-alpine \
  sh -c "npx ng serve --host 0.0.0.0"
```
Then visit `http://localhost:4200` on your Mac.

---
*Generated and Maintained by Gemini CLI Orchestrator - April 2026*
