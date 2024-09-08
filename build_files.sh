#!/bin/bash

# Install Python (if not installed)
apt-get update
apt-get install -y python3 python3-pip

# Upgrade pip
pip3 install --upgrade pip

# Install your dependencies
pip3 install -r requirements.txt

# Your build commands
python3.9 manage.py collectstatic
