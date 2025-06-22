import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys - Only need these two FREE APIs!
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    
    # Database - Uses SQLite (file-based, no server needed!)
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./resume_optimizer.db")
    
    # File Settings
    UPLOAD_FOLDER = "./data/resumes"
    MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", 10))
    ALLOWED_EXTENSIONS = {'pdf', 'docx'}
    
    # AI Models
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    GROQ_MODEL = "mixtral-8x7b-32768"
    
    # Security
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    
    @staticmethod
    def create_directories():
        """Create necessary directories if they don't exist"""
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs("./data/vector_db", exist_ok=True)
