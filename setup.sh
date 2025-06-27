#!/bin/bash

# Setup script for Agent Coordinator
echo "Setting up Agent Coordinator..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

echo "Setup complete! To run the coordinator:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run tests: python -m pytest tests/ -v"
echo "3. Start the server: python run_dev.py"
