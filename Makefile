# Makefile
# Customer Support AI - Project Makefile

.PHONY: help install install-dev train test run run-rag docker-build docker-up docker-down docker-logs clean lint format fix pre-commit

# ============================================
# HELP
# ============================================
help:
	@echo "╔══════════════════════════════════════════════════════════════╗"
	@echo "║         🤖 Customer Support AI - Makefile Commands          ║"
	@echo "╚══════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "📦 Installation:"
	@echo "  make install      - Install production dependencies"
	@echo "  make install-dev  - Install development dependencies"
	@echo ""
	@echo "🧠 Training:"
	@echo "  make train        - Train all ML models"
	@echo "  make train-priority - Train priority model only"
	@echo "  make train-category - Train category model only"
	@echo "  make train-sentiment - Train sentiment model only"
	@echo "  make build-faq    - Build FAQ database for RAG"
	@echo ""
	@echo "🚀 Running:"
	@echo "  make run          - Run main API server"
	@echo "  make run-rag      - Run RAG service"
	@echo "  make run-all      - Run both API and RAG (in background)"
	@echo ""
	@echo "🧪 Testing:"
	@echo "  make test         - Run all tests"
	@echo "  make test-api     - Run API tests only"
	@echo "  make test-models  - Run model tests only"
	@echo "  make test-coverage - Run tests with coverage report"
	@echo ""
	@echo "🎨 Code Quality:"
	@echo "  make lint         - Run linting checks (Flake8, Black, isort)"
	@echo "  make format       - Auto-format code (Black + isort)"
	@echo "  make fix          - Auto-fix linting issues"
	@echo "  make pre-commit   - Run pre-commit hooks"
	@echo ""
	@echo "🐳 Docker:"
	@echo "  make docker-build - Build Docker images"
	@echo "  make docker-up    - Start Docker containers (detached)"
	@echo "  make docker-down  - Stop Docker containers"
	@echo "  make docker-logs  - View Docker logs"
	@echo "  make docker-clean - Remove all Docker containers and images"
	@echo ""
	@echo "🧹 Cleanup:"
	@echo "  make clean        - Clean cache, logs, and temporary files"
	@echo "  make clean-all    - Deep clean (including virtual environment)"

# ============================================
# INSTALLATION
# ============================================
install:
	@echo "📦 Installing production dependencies..."
	pip install -r requirements.txt

install-dev:
	@echo "📦 Installing development dependencies..."
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	@echo "🔧 Installing pre-commit hooks..."
	pre-commit install

# ============================================
# TRAINING
# ============================================
train:
	@echo "🧠 Training all models..."
	python scripts/train_models.py

train-priority:
	@echo "🧠 Training priority model..."
	python -c "from scripts.train_models import train_priority_model; train_priority_model()"

train-category:
	@echo "🧠 Training category model..."
	python -c "from scripts.train_models import train_category_model; train_category_model()"

train-sentiment:
	@echo "🧠 Training sentiment model..."
	python -c "from scripts.train_models import train_sentiment_model; train_sentiment_model()"

build-faq:
	@echo "📚 Building FAQ database..."
	python scripts/build_faq_v2.py

# ============================================
# RUNNING
# ============================================
run:
	@echo "🚀 Starting API server..."
	python run.py

run-rag:
	@echo "🚀 Starting RAG service..."
	python run_rag.py

run-all:
	@echo "🚀 Starting both API and RAG services..."
	@echo "📡 RAG service on port 8001"
	@echo "📡 API service on port 8000"
	python run_rag.py & python run.py

# ============================================
# TESTING
# ============================================
test:
	@echo "🧪 Running all tests..."
	pytest tests/ -v

test-api:
	@echo "🧪 Running API tests..."
	pytest tests/test_api.py -v

test-models:
	@echo "🧪 Running model tests..."
	pytest tests/test_models.py -v

test-coverage:
	@echo "🧪 Running tests with coverage..."
	pytest tests/ -v --cov=app --cov-report=html --cov-report=term
	@echo "📊 Coverage report generated in htmlcov/index.html"

# ============================================
# CODE QUALITY
# ============================================
lint:
	@echo "🔍 Running linting checks..."
	@echo ""
	@echo "🎨 Black:"
	black --check app/ --line-length=120 || true
	@echo ""
	@echo "🧹 isort:"
	isort --check-only --profile black --line-length=120 app/ || true
	@echo ""
	@echo "🔍 Flake8:"
	flake8 app/ --config=.flake8 --count --statistics || true

format:
	@echo "🎨 Formatting code with Black..."
	black app/ --line-length=120
	@echo "🧹 Sorting imports with isort..."
	isort --profile black --line-length=120 app/
	@echo "✅ Formatting complete!"

fix:
	@echo "🔧 Auto-fixing linting issues..."
	@echo ""
	@echo "🎨 Running Black..."
	black app/ --line-length=120
	@echo ""
	@echo "🧹 Running isort..."
	isort --profile black --line-length=120 app/
	@echo ""
	@echo "🧹 Running autoflake..."
	autoflake --in-place --recursive --remove-all-unused-imports --remove-unused-variables app/ 2>/dev/null || true
	@echo ""
	@echo "✅ Fix complete!"

pre-commit:
	@echo "🔧 Running pre-commit hooks..."
	pre-commit run --all-files

# ============================================
# DOCKER
# ============================================
docker-build:
	@echo "🐳 Building Docker images..."
	docker-compose build

docker-up:
	@echo "🐳 Starting Docker containers..."
	docker-compose up -d
	@echo "✅ Services running!"
	@echo "   - Frontend: http://localhost:3000"
	@echo "   - API: http://localhost:8000"
	@echo "   - RAG: http://localhost:8001"

docker-down:
	@echo "🐳 Stopping Docker containers..."
	docker-compose down

docker-logs:
	@echo "🐳 Viewing Docker logs..."
	docker-compose logs -f

docker-clean:
	@echo "🐳 Removing all Docker containers and images..."
	docker-compose down -v
	docker system prune -f

# ============================================
# CLEANUP
# ============================================
clean:
	@echo "🧹 Cleaning cache and temporary files..."
	rm -rf __pycache__ .pytest_cache logs/*.log
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	@echo "✅ Clean complete!"

clean-all: clean
	@echo "🧹 Deep cleaning..."
	rm -rf .venv venv
	rm -rf htmlcov .coverage
	rm -rf .mypy_cache .ruff_cache
	@echo "✅ Deep clean complete!"
