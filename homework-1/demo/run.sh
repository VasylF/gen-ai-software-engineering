#!/bin/bash

# Banking Transactions API - Setup and Run Script
# This script installs dependencies and starts the Flask server

set -e  # Exit on error

echo "🏦 Banking Transactions API - Setup & Run"
echo "=========================================="

# Navigate to src directory
cd "$(dirname "$0")/../src"

echo "📦 Setting up Python environment..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing dependencies..."
pip install -q -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 Starting API server on http://localhost:8000"
echo "Press CTRL+C to stop the server"
echo ""
echo "📝 In another terminal, run:"
echo "   cd homework-1/demo"
echo "   python3 test_api.py"
echo ""
echo "=========================================="
echo ""

# Start the Flask app
python3 app.py
