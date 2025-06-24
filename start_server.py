#!/usr/bin/env python3
"""
Simple server startup script for debugging
"""
import sys
import traceback

def main():
    try:
        print("🔄 Starting ResumeAI Backend Server...")
        print("📦 Importing modules...")
        
        # Test imports
        from backend.app import app
        print("✅ Backend app imported successfully")
        
        from backend.models.ats_optimizer import ATSOptimizer
        print("✅ ATS Optimizer imported successfully")
        
        from backend.models.job_matcher import JobMatcher
        print("✅ Job Matcher imported successfully")
        
        from backend.models.resume_parser import ResumeParser
        print("✅ Resume Parser imported successfully")
        
        print("🚀 Starting Uvicorn server...")
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
        
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
