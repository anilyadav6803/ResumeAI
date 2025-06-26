@echo off
echo 🤖 ResumeAI Setup for Windows
echo ===============================

echo Creating virtual environment...
python -m venv resume_optimizer

echo Activating virtual environment...
call .\resume_optimizer\Scripts\activate.bat

echo Upgrading pip...
python -m pip install --upgrade pip

echo Installing dependencies...
python setup.py

echo.
echo ✅ Setup complete!
echo.
echo To start the application:
echo 1. Backend: uvicorn backend.app:app --reload
echo 2. Frontend: streamlit run frontend/streamlit_app.py
echo.
pause
