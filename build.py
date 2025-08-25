#!/usr/bin/env python
"""
Build script for creating executable
"""
import os
import sys
import subprocess
import shutil

def build_executable():
    """Build the executable using PyInstaller"""
    
    # Install PyInstaller if not already installed
    try:
        import PyInstaller
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Clean previous builds
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    
    # Build command - simplified for faster builds
    cmd = [
        "pyinstaller",
        "--name", "SpanishSubjunctive",
        "--windowed",  # No console window
        "--onedir",   # Faster than onefile
        "--add-data", ".env.example;.",  # Include example env file
        "main.py"
    ]
    
    print("Building executable...")
    subprocess.check_call(cmd)
    
    print("\nBuild complete!")
    print("Executable location: dist/SpanishSubjunctive/")
    print("\nIMPORTANT: Users need to:")
    print("1. Create a .env file with their OpenAI API key")
    print("2. Place it in the dist/SpanishSubjunctive/ folder")
    print("3. Run SpanishSubjunctive.exe")

if __name__ == "__main__":
    build_executable()