#!/bin/bash
# Build and push Docker image script

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
REGISTRY="${DOCKER_REGISTRY:-docker.io}"
IMAGE_NAME="${DOCKER_IMAGE:-farmland-agent}"
IMAGE_TAG="${IMAGE_TAG:-latest}"
FULL_IMAGE="${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}"

echo -e "${YELLOW}Building Docker image...${NC}"
echo "Image: ${FULL_IMAGE}"

# Build the image
docker build -t "${FULL_IMAGE}" .

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Build successful${NC}"
else
    echo -e "${RED}✗ Build failed${NC}"
    exit 1
fi

# Push to registry if credentials are available
if [ -n "$DOCKER_USERNAME" ] && [ -n "$DOCKER_PASSWORD" ]; then
    echo -e "${YELLOW}Logging in to Docker registry...${NC}"
    echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin

    echo -e "${YELLOW}Pushing image to registry...${NC}"
    docker push "${FULL_IMAGE}"

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Push successful${NC}"
    else
        echo -e "${RED}✗ Push failed${NC}"
        exit 1
    fi
else
    echo -e "${YELLOW}Docker registry credentials not found. Skipping push.${NC}"
fi

echo -e "${GREEN}✓ Done!${NC}"
