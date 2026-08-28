# Makefile for Customer Support AI

.PHONY: help install train test run run-rag clean

help:
	@echo "Customer Support AI - Commands:"
	@echo "  make install     - Install dependencies"
	@echo "  make train       - Train all models"
	@echo "  make run         - Run main API"
	@echo "  make run-rag     - Run RAG service"
	@echo "  make test        - Run tests"
	@echo "  make clean       - Clean cache and logs"

install:
	pip install -r requirements.txt

train:
	python scripts/train_models.py

run:
	python run.py

run-rag:
	python run_rag.py

test:
	pytest tests/ -v --cov=app

clean:
	rm -rf __pycache__ .pytest_cache logs/*.log
	find . -type d -name "__pycache__" -exec rm -rf {} +