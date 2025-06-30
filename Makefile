.PHONY: help install run test deploy clean dev-setup lint format

# Default target
help:
	@echo "CoWorkly Partner Dashboard API - Available Commands:"
	@echo ""
	@echo "  install    - Install Python dependencies"
	@echo "  dev-setup  - Set up development environment"
	@echo "  run        - Run the API locally"
	@echo "  test       - Run API tests"
	@echo "  lint       - Run linting checks"
	@echo "  format     - Format code with black"
	@echo "  deploy     - Deploy to Firebase Functions"
	@echo "  clean      - Clean up generated files"
	@echo "  help       - Show this help message"

# Install dependencies
install:
	@echo "📦 Installing Python dependencies..."
	pip install -r requirements.txt

# Development setup
dev-setup: install
	@echo "📦 Installing development dependencies..."
	pip install -e ".[dev]"
	@echo "✅ Development environment setup complete!"
	@echo ""
	@echo "Next steps:"
	@echo "1. Copy config.example.py to config.py and update settings"
	@echo "2. Download your Firebase service account key as service-account-key.json"
	@echo "3. Run 'make run' to start the API locally"
	@echo "4. Run 'make test' to test the endpoints"

# Run the API locally
run:
	@echo "🚀 Starting CoWorkly Partner Dashboard API..."
	python main.py

# Run tests
test:
	@echo "🧪 Running API tests..."
	python -m pytest tests/ -v

# Run import tests
test-imports:
	@echo "🧪 Testing imports..."
	python tests/test_imports.py

# Run API tests
test-api:
	@echo "🧪 Testing API endpoints..."
	python tests/test_api.py

# Run linting
lint:
	@echo "🔍 Running linting checks..."
	flake8 src/ tests/
	mypy src/

# Format code
format:
	@echo "🎨 Formatting code..."
	black src/ tests/

# Deploy to Firebase Functions
deploy:
	@echo "🌐 Deploying to Firebase Functions..."
	./deploy.sh

# Clean up generated files
clean:
	@echo "🧹 Cleaning up..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/ 