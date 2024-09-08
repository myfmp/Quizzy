#!/bin/bash

# Update pip
python3.9 -m pip install --upgrade pip

# Create and activate virtual environment (if not already created)
if [ ! -d "venv" ]; then
    python3.9 -m venv venv
fi
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run Django management commands
python3.9 manage.py collectstatic

# Additional build steps (if any)
# e.g., python manage.py migrate, etc.

