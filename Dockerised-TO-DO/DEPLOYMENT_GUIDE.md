# 🚀 Deployment Guide - Build & Push to Docker Hub

## Prerequisites Checklist

- ✅ Docker Desktop installed and running
- ✅ Docker Hub account (register at https://hub.docker.com)
- ✅ Docker CLI authenticated
- ✅ Git repository cloned locally

---

## Step 1: Verify Docker Installation

```powershell
docker --version
docker run hello-world
```

Expected output:
```
Docker version 24.x.x or higher
Hello from Docker!
```

---

## Step 2: Configure Docker Hub Credentials

### Option A: Using Docker CLI (Recommended)
```powershell
docker login

# Follow prompts:
# Username: your-docker-hub-username
# Password: your-docker-hub-personal-access-token
# (Generate PAT at: https://hub.docker.com/settings/security)
```

### Option B: Using Makefile
Edit `Makefile` and update:
```makefile
REGISTRY ?= burhanuddin10  # Replace with your Docker Hub username
IMAGE_NAME ?= todo-api
VERSION ?= 1.0.0
```

---

## Step 3: Build Docker Image

### Using Makefile (Recommended)
```powershell
cd C:\Users\STA-MADH-54\todo-docker
make build
```

### Manual Docker Build
```powershell
cd C:\Users\STA-MADH-54\todo-docker

# Build with tags
docker build -t burhanuddin10/todo-api:1.0.0 `
             -t burhanuddin10/todo-api:latest .
```

### Verify Build Success
```powershell
# Check image was created
docker images | grep todo-api

# Expected output:
# burhanuddin10/todo-api   1.0.0      <image-id>   <size>   <date>
# burhanuddin10/todo-api   latest     <image-id>   <size>   <date>
```

---

## Step 4: Test Image Locally

```powershell
# Run container
docker run -d --name todo-test -p 5000:5000 burhanuddin10/todo-api:1.0.0

# Test health endpoint
curl http://localhost:5000/health

# Test create todo
curl -X POST http://localhost:5000/todos `
  -H "Content-Type: application/json" `
  -d '{\"task\": \"Test task\", \"completed\": false}'

# View logs
docker logs todo-test

# Stop container
docker stop todo-test
docker rm todo-test
```

---

## Step 5: Push to Docker Hub

### Using Makefile (Recommended)
```powershell
make push
```

### Manual Push
```powershell
# Push version tag
docker push burhanuddin10/todo-api:1.0.0

# Push latest tag
docker push burhanuddin10/todo-api:latest
```

### Verify Push Success
```powershell
# Check Docker Hub - navigate to:
# https://hub.docker.com/repository/docker/burhanuddin10/todo-api/general

# Or verify via CLI
docker search burhanuddin10/todo-api

# Pull from Docker Hub
docker pull burhanuddin10/todo-api:1.0.0

# Run pulled image
docker run -p 5000:5000 burhanuddin10/todo-api:1.0.0
```

---

## Step 6: Semantic Versioning for Future Releases

### Update Version
```powershell
# Edit Makefile
VERSION := 1.0.1  # Patch update (bug fixes)
# or
VERSION := 1.1.0  # Minor update (new features)
# or
VERSION := 2.0.0  # Major update (breaking changes)
```

### Build & Tag New Version
```powershell
# Build with new version
make build VERSION=1.0.1

# Push
make push VERSION=1.0.1
```

### Tag in Git
```powershell
git tag -a v1.0.1 -m "Release v1.0.1 - Bug fixes and improvements"
git push origin v1.0.1
```

---

## Step 7: Docker Hub Organization (Optional)

Create organization for multiple projects:
```powershell
# On Docker Hub website: https://hub.docker.com/orgs

# Tag image with organization
docker tag todo-api:1.0.0 myorg/todo-api:1.0.0

# Push to organization
docker push myorg/todo-api:1.0.0
```

---

## Troubleshooting

### Docker Build Fails
```powershell
# Verbose build with no cache
docker build --progress=plain --no-cache `
  -t burhanuddin10/todo-api:1.0.0 .

# Check Dockerfile syntax
docker build -t test --dry-run .
```

### Push Authentication Error
```powershell
# Clear credentials and re-authenticate
docker logout
docker login

# Verify login
docker info | grep Username
```

### Image Size Too Large
```powershell
# Check image layers
docker history burhanuddin10/todo-api:1.0.0

# Optimize by removing unnecessary files (add to .dockerignore)
# Rebuild
make clean build
```

### Port Already in Use
```powershell
# Find process using port 5000
netstat -ano | findstr :5000

# Kill process (replace PID)
taskkill /PID <PID> /F

# Or use different port
docker run -p 5001:5000 burhanuddin10/todo-api:1.0.0
```

---

## Quick Reference Commands

```powershell
# Full workflow
make clean build test push

# Or step by step
make help           # Show all commands
make build          # Build image
make run            # Start container
make test           # Test health endpoint
make logs           # View logs
make inspect        # Check image size
make push           # Push to Docker Hub
make stop           # Stop container
make clean          # Cleanup
```

---

## CI/CD Automation (GitHub Actions)

Add `.github/workflows/docker-build.yml`:

```yaml
name: Build & Push Docker Image

on:
  push:
    branches: [main]
    tags: ['v*']

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
      
      - name: Login to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      
      - name: Extract version
        run: echo "VERSION=${GITHUB_REF#refs/tags/v}" >> $GITHUB_ENV
      
      - name: Build and Push
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: |
            ${{ secrets.DOCKER_USERNAME }}/todo-api:${{ env.VERSION }}
            ${{ secrets.DOCKER_USERNAME }}/todo-api:latest
```

Setup GitHub Secrets:
1. Go to Settings → Secrets → New Repository Secret
2. Add `DOCKER_USERNAME` and `DOCKER_PASSWORD`
3. Push tag to trigger: `git push origin v1.0.0`

---

## Production Deployment Checklist

- [ ] Code reviewed and tested locally
- [ ] All tests passing (`make test`)
- [ ] Version bumped in Makefile
- [ ] Git commit created
- [ ] Docker image built successfully
- [ ] Image tested locally (`docker run`)
- [ ] Image pushed to Docker Hub
- [ ] Docker Hub visibility set (public/private)
- [ ] Git tag created and pushed
- [ ] README updated with new version
- [ ] Kubernetes manifests updated (if applicable)

---

## Image Inspection

```powershell
# View image metadata
docker inspect burhanuddin10/todo-api:1.0.0

# Check image size
docker image ls burhanuddin10/todo-api:1.0.0

# View layers and sizes
docker history burhanuddin10/todo-api:1.0.0

# Scan for vulnerabilities
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock `
  aquasec/trivy image burhanuddin10/todo-api:1.0.0
```

---

## Support

**Documentation:** See README.md  
**GitHub:** https://github.com/BurhanuddinLokhandwala10/TODO_DOCKER  
**Docker Hub:** https://hub.docker.com/r/burhanuddin10/todo-api  

**Last Updated:** June 5, 2026
