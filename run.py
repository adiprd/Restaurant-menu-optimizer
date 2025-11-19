#!/usr/bin/env python3
"""
AI RESTAURANT MENU OPTIMIZER - Startup Script
"""

import os
import sys
import subprocess
import time

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'flask', 'pandas', 'numpy', 'scikit-learn', 'matplotlib', 
        'seaborn', 'plotly', 'faker', 'openpyxl'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    return missing_packages

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies from requirements.txt...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to install dependencies: {e}")
        return False

def main():
    print("AI RESTAURANT MENU OPTIMIZER - Starting Application...")
    print("=" * 60)
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("Python 3.7 or higher is required")
        sys.exit(1)
    
    # Check dependencies
    missing = check_dependencies()
    if missing:
        print(f"Missing packages: {', '.join(missing)}")
        if not install_dependencies():
            print("Please install dependencies manually: pip install -r requirements.txt")
            sys.exit(1)
    
    # Start the application
    print("Starting Restaurant Menu Optimizer...")
    print("Access the application at: http://localhost:5000")
    print("Press Ctrl+C to stop the application")
    print("=" * 60)
    
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("Application stopped by user")
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
