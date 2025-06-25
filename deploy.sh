#!/bin/bash

# ResumeAI Deployment Script for Digital Ocean
# This script helps deploy your ResumeAI application to Digital Ocean

set -e

echo "🚀 ResumeAI Deployment Script"
echo "================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if required tools are installed
check_requirements() {
    echo -e "${BLUE}Checking requirements...${NC}"
    
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}Docker is not installed. Please install Docker first.${NC}"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        echo -e "${RED}Docker Compose is not installed. Please install Docker Compose first.${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✓ All requirements met${NC}"
}

# Setup environment variables
setup_env() {
    echo -e "${BLUE}Setting up environment variables...${NC}"
    
    if [ ! -f .env.production ]; then
        echo -e "${YELLOW}Creating .env.production file...${NC}"
        cp .env.production.template .env.production
        echo -e "${YELLOW}Please edit .env.production with your actual API keys${NC}"
        return 1
    fi
    
    echo -e "${GREEN}✓ Environment variables configured${NC}"
}

# Build and deploy
deploy() {
    echo -e "${BLUE}Building and deploying ResumeAI...${NC}"
    
    # Build the Docker image
    echo -e "${YELLOW}Building Docker image...${NC}"
    docker-compose -f docker-compose.production.yml build --no-cache
    
    # Stop any existing containers
    echo -e "${YELLOW}Stopping existing containers...${NC}"
    docker-compose -f docker-compose.production.yml down
    
    # Start the application
    echo -e "${YELLOW}Starting application...${NC}"
    docker-compose -f docker-compose.production.yml up -d
    
    # Wait for services to start
    echo -e "${YELLOW}Waiting for services to start...${NC}"
    sleep 30
    
    # Check if services are running
    if curl -f http://localhost/health > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Application deployed successfully!${NC}"
        echo -e "${GREEN}Frontend: http://your-domain.com${NC}"
        echo -e "${GREEN}API: http://your-domain.com/api${NC}"
        echo -e "${GREEN}Health Check: http://your-domain.com/health${NC}"
    else
        echo -e "${RED}❌ Deployment failed. Check logs with: docker-compose -f docker-compose.production.yml logs${NC}"
        exit 1
    fi
}

# Show logs
show_logs() {
    echo -e "${BLUE}Showing application logs...${NC}"
    docker-compose -f docker-compose.production.yml logs -f
}

# Main script
case "${1:-deploy}" in
    "check")
        check_requirements
        ;;
    "env")
        setup_env
        ;;
    "deploy")
        check_requirements
        setup_env
        if [ $? -eq 0 ]; then
            deploy
        else
            echo -e "${RED}Please configure your environment variables first${NC}"
            exit 1
        fi
        ;;
    "logs")
        show_logs
        ;;
    "stop")
        echo -e "${YELLOW}Stopping application...${NC}"
        docker-compose -f docker-compose.production.yml down
        echo -e "${GREEN}✓ Application stopped${NC}"
        ;;
    "restart")
        echo -e "${YELLOW}Restarting application...${NC}"
        docker-compose -f docker-compose.production.yml restart
        echo -e "${GREEN}✓ Application restarted${NC}"
        ;;
    *)
        echo "Usage: $0 {check|env|deploy|logs|stop|restart}"
        echo ""
        echo "Commands:"
        echo "  check   - Check if requirements are installed"
        echo "  env     - Setup environment variables"
        echo "  deploy  - Build and deploy the application"
        echo "  logs    - Show application logs"
        echo "  stop    - Stop the application"
        echo "  restart - Restart the application"
        exit 1
        ;;
esac
