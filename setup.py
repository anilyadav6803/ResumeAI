#!/usr/bin/env python3
"""
ResumeAI Setup Script
Handles installation of dependencies with fallback options for problematic packages.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description=""):
    """Run a shell command and return the result."""
    print(f"🔄 {description}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - Success")
            return True
        else:
            print(f"❌ {description} - Failed")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} - Exception: {e}")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} is not compatible. Requires Python 3.8+")
        return False

def install_requirements(requirements_file):
    """Install requirements from a specific file."""
    requirements_path = Path(requirements_file)
    if not requirements_path.exists():
        print(f"❌ Requirements file {requirements_file} not found")
        return False
    
    print(f"📦 Installing from {requirements_file}")
    
    # Try with pip install first
    if run_command(f"pip install -r {requirements_file}", f"Installing from {requirements_file}"):
        return True
    
    # If that fails, try with --only-binary for problematic packages
    print("🔄 Trying installation with binary wheels only...")
    if run_command(f"pip install --only-binary=sentencepiece,tokenizers -r {requirements_file}", 
                   "Installing with binary wheels"):
        return True
    
    return False

def main():
    """Main setup function."""
    print("🤖 ResumeAI Setup Script")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Try different requirements files in order of preference
    requirements_files = [
        "requirements.txt",
        "requirements-streamlit.txt", 
        "requirements-minimal.txt"
    ]
    
    success = False
    for req_file in requirements_files:
        if install_requirements(req_file):
            success = True
            print(f"✅ Successfully installed dependencies from {req_file}")
            break
        else:
            print(f"❌ Failed to install from {req_file}, trying next option...")
    
    if not success:
        print("❌ All installation attempts failed.")
        print("\n🔧 Manual Installation Steps:")
        print("1. Update pip: pip install --upgrade pip")
        print("2. Install system dependencies if on Linux:")
        print("   sudo apt-get install cmake pkg-config")
        print("3. Try installing minimal requirements:")
        print("   pip install fastapi uvicorn streamlit groq pandas numpy plotly")
        sys.exit(1)
    
    # Test the installation
    print("\n🧪 Testing installation...")
    test_imports = [
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"), 
        ("streamlit", "Streamlit"),
        ("groq", "Groq API"),
        ("pandas", "Pandas"),
        ("numpy", "NumPy"),
        ("plotly", "Plotly")
    ]
    
    failed_imports = []
    for module, name in test_imports:
        try:
            __import__(module)
            print(f"✅ {name} imported successfully")
        except ImportError:
            print(f"⚠️  {name} import failed")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\n⚠️  Some modules failed to import: {', '.join(failed_imports)}")
        print("The application may still work with reduced functionality.")
    else:
        print("\n🎉 All core modules imported successfully!")
    
    print("\n🚀 Setup complete! You can now start the application:")
    print("Backend: uvicorn backend.app:app --reload")
    print("Frontend: streamlit run frontend/streamlit_app.py")

if __name__ == "__main__":
    main()
