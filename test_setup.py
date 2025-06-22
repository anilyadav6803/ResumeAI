"""
Simple test to verify ResumeAI is working
"""

def test_basic_imports():
    print("🧪 Testing basic imports...")
    
    try:
        import fastapi
        print("✅ FastAPI imported successfully")
    except ImportError as e:
        print(f"❌ FastAPI import failed: {e}")
        return False
    
    try:
        import streamlit
        print("✅ Streamlit imported successfully")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        from backend.config import Config
        print("✅ Config imported successfully")
    except ImportError as e:
        print(f"❌ Config import failed: {e}")
        return False
    
    try:
        from backend.models.resume_parser import ResumeParser
        parser = ResumeParser()
        print("✅ ResumeParser created successfully")
    except ImportError as e:
        print(f"❌ ResumeParser import failed: {e}")
        return False
    
    return True

def test_directories():
    print("\n📁 Testing directories...")
    import os
    
    dirs = ["data", "data/resumes", "data/vector_db"]
    for dir_path in dirs:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
            print(f"✅ Created directory: {dir_path}")
        else:
            print(f"✅ Directory exists: {dir_path}")

def test_api_keys():
    print("\n🔑 Checking API keys...")
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    groq_key = os.getenv("GROQ_API_KEY")
    google_key = os.getenv("GOOGLE_API_KEY")
    
    if groq_key and groq_key != "your_groq_api_key_here":
        print("✅ Groq API key configured")
        return True
    elif google_key and google_key != "your_google_gemini_api_key_here":
        print("✅ Google Gemini API key configured")
        return True
    else:
        print("⚠️  No API keys configured (basic features will work)")
        return False

def main():
    print("=" * 60)
    print("🤖 RESUMEAI - TESTING SETUP")
    print("=" * 60)
    
    # Test basic imports
    if not test_basic_imports():
        print("\n❌ Setup failed - missing dependencies")
        return
    
    # Test directories
    test_directories()
    
    # Test API keys
    test_api_keys()
    
    print("\n" + "=" * 60)
    print("🎉 SETUP TEST COMPLETED!")
    print("=" * 60)
    print("\n🚀 READY TO START!")
    print("\n📋 TO START THE APPLICATION:")
    print("1️⃣  Backend: uvicorn backend.app:app --reload")
    print("2️⃣  Frontend: streamlit run frontend/streamlit_app.py")
    print("\n💻 ACCESS:")
    print("• API: http://localhost:8000")
    print("• Web App: http://localhost:8501")
    print("\n📚 WHAT YOU CAN DO:")
    print("• Upload resumes and find best candidates")
    print("• Get ATS optimization recommendations")
    print("• Batch process multiple resumes")

if __name__ == "__main__":
    main()
