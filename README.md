# ZKP System Project

This repository contains the Zero-Knowledge Proof (ZKP) project setup, Docker configuration, and instructions for local development.

---

## Branching Strategy

We are following **GitHub Flow** for our development process:

1. **Main Branch (`main`)**  
   - Always contains the stable, production-ready code.
2. **Feature Branches**  
   - Each new feature or experiment is developed in a separate branch, e.g., `feature/docker-setup`.  
   - Pull Requests (PRs) are created to merge feature branches into `main` once they are tested and approved.
3. **Merging**  
   - All changes are merged into `main` via PRs.  
   - Fast-forward merges are preferred to maintain a clean history.

**Example:**  
- `main` → stable branch  
- `feature/docker-setup` → branch for Docker configuration  
- Screenshots of branches in GitHub can be found in `/screenshots/branches.png`

---

## Local Development Tools

The project uses the following tools for local development:

| Tool                  | Version | Purpose |
|-----------------------|---------|---------|
| Node.js               | 18.x    | JavaScript runtime environment |
| npm                   | 11.x    | Package management |
| Docker Desktop         | Latest  | Containerization and local environment |
| VS Code               | Latest  | IDE for coding and terminal access |
| Express.js            | Latest  | Lightweight web server (for local testing) |

---

## Quick Start – Local Development

Follow these steps to get the project running locally using Docker:

### 1. Install Docker Desktop

- Download from: [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)  
- Install and ensure Docker is running. Verify with:

```bash
docker --version
docker-compose --version
```

### 2. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/zkp-system.git
cd zkp-system
```

### 3. Build and Run Docker Container
```bash
docker-compose up --build
```
The docker-compose.yml will:
-Build the Docker image from the Dockerfile
-Start the container named zkp-container
-Map port 3000 from container to host
If successful, you should see:
`zkp-container | ZKP Docker container running successfully!`
### 4. Access the App in Browser
Open your browser and navigate to:
```bash
http://localhost:3000
```
You should see:
`ZKP Docker container running successfully!`

### 5. Stop the Container
```bash
docker-compose down
```

---

## Screenshots (Proof of Setup)

- Docker build and run success:  
  ![Docker Build & Run](/screenshots/docker_run.png)
- App running on localhost:  
  ![App on Localhost](/screenshots/app_run.png)
- GitHub branches showing feature branch:  
  ![GitHub Branches](/screenshots/branches.png)

