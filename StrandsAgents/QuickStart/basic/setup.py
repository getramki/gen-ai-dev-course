#!/usr/bin/env python3
"""
Setup script for StrandsAgents QuickStart
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("Installing StrandsAgents and dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False
    return True

def verify_installation():
    """Verify StrandsAgents is properly installed"""
    try:
        import strandsagents
        print(f"✅ StrandsAgents version {strandsagents.__version__} installed")
        return True
    except ImportError:
        print("❌ StrandsAgents not found")
        return False

def main():
    print("=== StrandsAgents QuickStart Setup ===\n")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Install dependencies
    if not install_requirements():
        sys.exit(1)
    
    # Verify installation
    if not verify_installation():
        sys.exit(1)
    
    print("\n=== Setup Complete ===")
    print("Run 'python basic_example.py' to test your installation")

if __name__ == "__main__":
    main()