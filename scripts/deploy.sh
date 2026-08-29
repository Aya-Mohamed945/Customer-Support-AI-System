#!/bin/bash
# scripts/deploy.sh

set -e

echo "============================================================"
echo "🚀 Customer Support AI - Deployment Script"
echo "============================================================"

ENVIRONMENT=${1:-staging}
PROJECT_DIR="/app/customer-support-ai"
DOCKER_COMPOSE_FILE="docker-compose.yml"

echo "📋 Environment: $ENVIRONMENT"
echo "📁 Project Directory: $PROJECT_DIR"

deploy_services() {
    echo ""
    echo "📦 Pulling latest images..."
    docker-compose -f "$DOCKER_COMPOSE_FILE" pull

    echo ""
    echo "🚀 Starting services..."
    docker-compose -f "$DOCKER_COMPOSE_FILE" up -d --force-recreate

    echo ""
    echo "🧹 Cleaning up..."
    docker system prune -f
}

health_check() {
    echo ""
    echo "✅ Running health checks..."

    echo "   Checking API..."
    curl -f http://localhost:8000/health || exit 1

    echo "   Checking RAG..."
    curl -f http://localhost:8001/health || exit 1

    echo "   Checking Frontend..."
    curl -f http://localhost:3000 || exit 1

    echo "   ✅ All services are healthy!"
}

cd "$PROJECT_DIR" || exit 1

case $ENVIRONMENT in
    staging)
        echo ""
        echo "🌱 Deploying to STAGING..."
        deploy_services
        health_check
        ;;
    production)
        echo ""
        echo "🔥 Deploying to PRODUCTION..."
        echo "⚠️ Are you sure? (yes/no)"
        read -r confirmation
        if [ "$confirmation" != "yes" ]; then
            echo "❌ Deployment cancelled."
            exit 1
        fi
        deploy_services
        health_check
        ;;
    rollback)
        echo ""
        echo "🔙 Rolling back..."
        docker-compose -f "$DOCKER_COMPOSE_FILE" down
        docker-compose -f "$DOCKER_COMPOSE_FILE" up -d
        ;;
    *)
        echo ""
        echo "❌ Invalid environment: $ENVIRONMENT"
        echo "Usage: ./deploy.sh [staging|production|rollback]"
        exit 1
        ;;
esac

echo ""
echo "============================================================"
echo "✅ Deployment completed successfully!"
echo "============================================================"