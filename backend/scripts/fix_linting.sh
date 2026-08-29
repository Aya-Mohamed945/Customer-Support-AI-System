#!/bin/bash
# backend/scripts/fix_linting.sh
# Auto-fix linting issues

echo "🔧 Fixing linting issues..."

# Run black to format code
echo "🎨 Running Black..."
black app/ --line-length=120

# Run isort to sort imports
echo "🧹 Running isort..."
isort app/ --profile black --line-length=120

# Run autoflake to remove unused imports
echo "🧹 Running autoflake..."
autoflake --in-place --recursive --remove-all-unused-imports --remove-unused-variables app/

# Check remaining issues
echo "🔍 Checking remaining issues with Flake8..."
flake8 app/ --config=.flake8 --count --statistics

echo "✅ Done!"