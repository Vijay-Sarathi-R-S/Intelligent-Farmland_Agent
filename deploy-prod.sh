#!/bin/bash
# Production deployment script

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Check if .env file exists
if [ ! -f .env.prod ]; then
    echo -e "${RED}Error: .env.prod file not found. Please create it from .env.example${NC}"
    exit 1
fi

# Load environment variables
export $(cat .env.prod | xargs)

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  Intelligent Farmland Agent Deployment ${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"

echo ""
echo -e "${YELLOW}Deployment Configuration:${NC}"
echo "  Environment: Production"
echo "  Registry: ${DOCKER_REGISTRY}"
echo "  Image: ${DOCKER_IMAGE}:${IMAGE_TAG}"
echo "  Database: ${DB_NAME}"

# Step 1: Build and push image
echo ""
echo -e "${YELLOW}Step 1: Building Docker image...${NC}"
docker-compose -f docker-compose.prod.yml build

echo -e "${GREEN}✓ Build complete${NC}"

# Step 2: Start services
echo ""
echo -e "${YELLOW}Step 2: Starting services...${NC}"
docker-compose -f docker-compose.prod.yml up -d

echo -e "${GREEN}✓ Services started${NC}"

# Step 3: Wait for services to be healthy
echo ""
echo -e "${YELLOW}Step 3: Waiting for services to be healthy...${NC}"
for i in {1..30}; do
    if docker-compose -f docker-compose.prod.yml exec -T app curl -f http://localhost:5000/ > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Application is healthy${NC}"
        break
    fi
    echo "  Attempt $i/30..."
    sleep 2
done

# Step 4: Verify deployments
echo ""
echo -e "${YELLOW}Step 4: Verifying deployment...${NC}"
docker-compose -f docker-compose.prod.yml ps

echo ""
echo -e "${GREEN}✓ Deployment complete!${NC}"
echo ""
echo -e "${BLUE}Service URLs:${NC}"
echo "  Application: http://localhost:80"
echo "  API Health: http://localhost:80/health"
echo ""
echo -e "${BLUE}Useful commands:${NC}"
echo "  docker-compose -f docker-compose.prod.yml logs -f app"
echo "  docker-compose -f docker-compose.prod.yml exec app bash"
echo "  docker-compose -f docker-compose.prod.yml down"
