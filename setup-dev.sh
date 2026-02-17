#!/bin/bash
# Development environment setup script

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}Setting up development environment...${NC}"

# Create .env file from template
if [ ! -f .env ]; then
    echo -e "${YELLOW}Creating .env file from .env.example...${NC}"
    cp .env.example .env
    echo -e "${GREEN}✓ .env created. Please update it with your API keys.${NC}"
fi

# Start services
echo -e "${YELLOW}Starting Docker Compose services...${NC}"
docker-compose up -d

echo -e "${GREEN}✓ Services started!${NC}"
echo "Application available at: http://localhost:5000"
echo "Redis available at: localhost:6379"
echo ""
echo -e "${YELLOW}Useful commands:${NC}"
echo "  docker-compose logs -f app        # View application logs"
echo "  docker-compose exec app bash      # Access application container"
echo "  docker-compose down               # Stop all services"
echo "  docker-compose ps                 # View running services"
