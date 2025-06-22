"""
ResumeAI Quick Start Script
This script will help you get started quickly!
"""

import os
import sys
import subprocess
import platform

def print_banner():
    print("=" * 60)
    print("🤖 RESUMEAI - AI Resume Optimizer & Screening Agent")
    print("=" * 60)
    print("📋 WHAT THIS PROJECT DOES:")
    print("• For HR: Upload resumes → AI finds best candidates")
    print("• For Job Seekers: Upload resume → Get ATS optimization tips")
    print("=" * 60)

def check_python():
    print("🐍 Checking Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor} found")
        return True
    else:
        print("❌ Python 3.8+ required")
        return False

def install_dependencies():
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def setup_directories():
    print("\n📁 Creating directories...")
    dirs = ["data", "data/resumes", "data/vector_db"]
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
    print("✅ Directories created!")

def check_api_keys():
    print("\n🔑 Checking API keys...")
    from dotenv import load_dotenv
    load_dotenv()
    
    groq_key = os.getenv("GROQ_API_KEY")
    google_key = os.getenv("GOOGLE_API_KEY")
    
    if groq_key and groq_key != "your_groq_api_key_here":
        print("✅ Groq API key found")
        return True
    elif google_key and google_key != "your_google_gemini_api_key_here":
        print("✅ Google Gemini API key found")
        return True
    else:
        print("⚠️  No API keys configured")
        print("📚 The app will work with limited features")
        print("🔗 Get FREE API keys from:")
        print("   • Groq: https://groq.com")
        print("   • Google Gemini: https://makersuite.google.com/app/apikey")
        return False

def start_services():
    print("\n🚀 READY TO START!")
    print("\n📋 TO START THE APPLICATION:")
    print("1️⃣  Backend API:")
    print("   uvicorn backend.app:app --reload")
    print("   (Will run on http://localhost:8000)")
    print()
    print("2️⃣  Frontend Web App:")
    print("   streamlit run frontend/streamlit_app.py")
    print("   (Will run on http://localhost:8501)")
    print()
    print("💡 TIP: Open two terminals and run each command")

def main():
    print_banner()
    
    if not check_python():
        return
    
    if not install_dependencies():
        return
    
    setup_directories()
    check_api_keys()
    start_services()
    
    print("\n" + "=" * 60)
    print("🎉 SETUP COMPLETED!")
    print("=" * 60)

if __name__ == "__main__":
    main()
