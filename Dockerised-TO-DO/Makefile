.PHONY: help build push run stop logs test clean

# Configuration
REGISTRY ?= your-docker-hub-username
IMAGE_NAME ?= todo-api
VERSION ?= 1.0.0
DOCKER_IMAGE := $(REGISTRY)/$(IMAGE_NAME):$(VERSION)
DOCKER_LATEST := $(REGISTRY)/$(IMAGE_NAME):latest

help: ## Display this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: ## Build Docker image with multi-stage Dockerfile
	@echo "Building $(DOCKER_IMAGE)..."
	docker build -t $(DOCKER_IMAGE) -t $(DOCKER_LATEST) .
	@echo "✓ Build complete"

push: build ## Push image to Docker Hub (requires login)
	@echo "Pushing $(DOCKER_IMAGE) to Docker Hub..."
	docker push $(DOCKER_IMAGE)
	docker push $(DOCKER_LATEST)
	@echo "✓ Push complete"

run: ## Run container locally
	@echo "Starting container..."
	docker-compose up -d
	@echo "✓ Container running on http://localhost:5000"

stop: ## Stop and remove container
	docker-compose down
	@echo "✓ Container stopped"

logs: ## Show container logs
	docker-compose logs -f

test: ## Test API endpoints
	@echo "Testing API..."
	curl -X GET http://localhost:5000/health
	@echo "\n✓ Health check passed"

clean: ## Remove all images and containers
	docker-compose down -v
	docker rmi $(DOCKER_IMAGE) $(DOCKER_LATEST) 2>/dev/null || true
	@echo "✓ Cleanup complete"

inspect: ## Inspect image size and layers
	docker image inspect $(DOCKER_IMAGE) --format='{{.Size}}'
	docker history $(DOCKER_IMAGE)

shell: ## Open shell in running container
	docker-compose exec todo-api sh

version: ## Show version information
	@echo "Image: $(DOCKER_IMAGE)"
	@echo "Registry: $(REGISTRY)"
	@echo "Version: $(VERSION)"
