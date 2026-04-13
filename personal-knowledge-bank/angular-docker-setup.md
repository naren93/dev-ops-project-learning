# Angular Development: The Ultra-Clean Docker Workflow

This document records the architecture and commands for developing Angular applications on a Mac with limited storage, using Docker to keep the host system clean of "node_modules" and global software.

## 1. Architectural Reasoning

### Problem: Storage Bloat
A single Angular project can consume **400MB - 600MB** of storage, primarily in the `node_modules` folder. This clutters the Mac's filesystem, slows down Spotlight indexing, and is difficult to clean up.

### Solution: Docker + Named Volumes
- **No Local Installs:** No Node.js, npm, or Angular CLI is installed on the Mac. Everything runs inside ephemeral Docker containers.
- **Hidden node_modules:** We use a **Named Docker Volume** (e.g., `angular-21-lts-modules`) to store the dependencies. This storage lives inside Docker's virtual disk, making it invisible to the Mac's filesystem but high-performance for the container.
- **Shared Storage:** Multiple Angular projects of the same version can mount the *same* volume to save space and avoid redundant downloads.
- **Live Editing:** Your source code (`src/`, `package.json`, etc.) stays on your Mac and is "mounted" into the container so you can use your local editor.

---

## 2. Command History (April 2026 Session)

### Setup Directories
```bash
mkdir -p 001-Angular/001-Hello-world
```

### Initialize Project (Angular 21 LTS)
This command creates a shared volume and scaffolds the app without leaving `node_modules` on your Mac.
```bash
docker volume create angular-21-lts-modules

docker run --rm \
  -v "$(pwd)/001-Angular/001-Hello-world:/app" \
  -v angular-21-lts-modules:/app/node_modules \
  -w /app \
  node:22-alpine \
  sh -c "corepack enable && npx -y @angular/cli@21 new hello-world --directory . --defaults --skip-git --package-manager pnpm"
```

### Start Development Server
Runs the app in the background and maps port 4200 to your Mac.
```bash
docker run -d --name angular-hello-world \
  -p 4200:4200 \
  -v "$(pwd)/001-Angular/001-Hello-world:/app" \
  -v angular-21-lts-modules:/app/node_modules \
  -w /app \
  node:22-alpine \
  sh -c "npx ng serve --host 0.0.0.0"
```

---

## 3. Future CLI References (Self-Help)

### View Running App Logs
If the site doesn't load or you want to see build errors:
```bash
docker logs -f angular-hello-world
```

### Stop the Development Server
```bash
docker stop angular-hello-world && docker rm angular-hello-world
```

### Create a New Project Using the Same Volume
Navigate to your root and run:
```bash
mkdir -p 001-Angular/my-new-app
docker run --rm \
  -v "$(pwd)/001-Angular/my-new-app:/app" \
  -v angular-21-lts-modules:/app/node_modules \
  -w /app \
  node:22-alpine \
  sh -c "corepack enable && npx -y @angular/cli@21 new my-new-app --directory . --defaults --skip-git"
```

### Add a Dependency (e.g., Bootstrap)
```bash
docker run --rm \
  -v "$(pwd)/001-Angular/001-Hello-world:/app" \
  -v angular-21-lts-modules:/app/node_modules \
  -w /app \
  node:22-alpine \
  pnpm add bootstrap
```

### Reclaim Storage (The "Nuke" Option)
If you want to delete all hidden dependencies and Docker "junk":
```bash
docker system prune -a --volumes
```
*(Warning: This deletes ALL images and volumes not currently in use)*

