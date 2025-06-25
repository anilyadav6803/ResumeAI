# 🤖 ResumeAI - AI-Powered Resume Optimization & Matching

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

ResumeAI is an intelligent resume screening and optimization platform that helps recruiters find the best candidates and job seekers optimize their resumes for Applicant Tracking Systems (ATS).

![ResumeAI Demo](https://via.placeholder.com/800x400/667eea/ffffff?text=ResumeAI+Demo)

## ✨ Features

### 🎯 For Recruiters - Resume Screening
- **AI-Powered Matching**: Upload multiple resumes and match them against job descriptions
- **Semantic Analysis**: Advanced NLP to understand skills, experience, and qualifications
- **Candidate Ranking**: Get ranked candidates with detailed match scores (out of 100)
- **Bulk Processing**: Screen multiple resumes simultaneously
- **Detailed Analytics**: View candidate information, skills, and matching content

### 🚀 For Job Seekers - ATS Optimization
- **ATS Compatibility Score**: Get a score out of 100 for ATS compatibility
- **Missing Keywords**: Identify keywords missing from your resume
- **Format Optimization**: Get suggestions for better resume formatting
- **Content Improvements**: Receive detailed recommendations for content enhancement

### 📊 Analytics & Insights
- **Processing Statistics**: Track resume processing success rates
- **Skills Analytics**: Most common skills found in resumes
- **Performance Metrics**: System performance and processing times

## 🏗️ Architecture

```
ResumeAI/
├── backend/                 # FastAPI Backend
│   ├── app.py              # Main FastAPI application
│   ├── config.py           # Configuration settings
│   └── models/             # AI Models
│       ├── resume_parser.py    # Resume parsing logic
│       ├── job_matcher.py      # Job matching algorithms
│       ├── ats_optimizer.py    # ATS optimization engine
│       └── embeddings.py       # Vector embeddings
├── frontend/               # Streamlit Frontend
│   └── streamlit_app.py    # Web application
├── data/                   # Data storage
│   ├── resumes/           # Uploaded resumes
│   ├── vector_db/         # Vector database
│   └── logs/              # Application logs
└── requirements.txt        # Python dependencies
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### 1. Clone the Repository
```bash
git clone https://github.com/anilyadav6803/ResumeAI.git
cd ResumeAI
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
Create a `.env` file in the root directory:
```env
# AI API Keys (at least one required)
GROQ_API_KEY=your_groq_api_key_here
GOOGLE_API_KEY=your_google_gemini_api_key_here

# Optional: Database configurations
DATABASE_URL=sqlite:///./resumeai.db
```

### 4. Test Setup
```bash
python test_setup.py
```

### 5. Start the Application

#### Option A: Start Both Services
```bash
# Terminal 1 - Backend API
uvicorn backend.app:app --host 127.0.0.1 --port 8000 --reload

# Terminal 2 - Frontend Web App
streamlit run frontend/streamlit_app.py --server.port 8501
```

#### Option B: Use Docker (Coming Soon)
```bash
docker-compose up
```

### 6. Access the Application
- **Web Application**: http://localhost:8501
- **API Documentation**: http://localhost:8000/docs
- **API Health Check**: http://localhost:8000/health

## 💻 Usage

### Resume Screening Workflow
1. Navigate to the **Resume Screening** page
2. Upload multiple resume files (PDF or DOCX)
3. Enter the job description
4. Adjust settings (number of candidates, minimum score)
5. Click "Find Best Candidates"
6. View ranked candidates with detailed match analysis

### ATS Optimization Workflow
1. Go to the **ATS Optimization** page
2. Upload your resume (PDF or DOCX)
3. Paste the target job description
4. Click "Analyze & Optimize"
5. Review your ATS score and recommendations

## 🔧 Configuration

### API Keys Setup
ResumeAI supports multiple AI providers. You need at least one:

#### Groq API (Recommended)
1. Sign up at [Groq](https://groq.com/)
2. Get your API key
3. Add to `.env`: `GROQ_API_KEY=your_key_here`

#### Google Gemini API
1. Sign up at [Google AI Studio](https://makersuite.google.com/)
2. Get your API key
3. Add to `.env`: `GOOGLE_API_KEY=your_key_here`

### Customization
- Modify `backend/config.py` for system settings
- Adjust UI themes in `frontend/streamlit_app.py`
- Configure vector database settings in `backend/models/embeddings.py`

## 📁 Project Structure

```
ResumeAI/
├── backend/
│   ├── app.py                    # FastAPI main application
│   ├── config.py                 # Configuration management
│   └── models/
│       ├── ats_optimizer.py      # ATS optimization algorithms
│       ├── embeddings.py         # Vector embedding management
│       ├── job_matcher.py        # Resume-job matching logic
│       └── resume_parser.py      # Resume parsing utilities
├── frontend/
│   └── streamlit_app.py          # Streamlit web interface
├── data/
│   ├── logs/                     # Application logs
│   ├── resumes/                  # Uploaded resume storage
│   ├── vector_db/                # Vector database files
│   └── sample_job_description.txt
├── .env.example                  # Environment variables template
├── .gitignore                    # Git ignore rules
├── docker-compose.yml            # Docker composition
├── Dockerfile                    # Docker configuration
├── requirements.txt              # Python dependencies
├── test_setup.py                 # Setup verification script
└── README.md                     # This file
```

## 🛠️ API Endpoints

### Core Endpoints
- `GET /` - API information
- `GET /health/` - Health check
- `POST /upload-resumes/` - Upload multiple resumes
- `POST /match-resumes/` - Match resumes to job description
- `POST /optimize-resume/` - Optimize single resume for ATS
- `GET /stats/` - Get system statistics

### Example API Usage
```python
import requests

# Upload resumes
files = [("files", open("resume1.pdf", "rb"))]
response = requests.post("http://localhost:8000/upload-resumes/", files=files)

# Match resumes
data = {"job_description": "Software Engineer...", "top_k": 5}
response = requests.post("http://localhost:8000/match-resumes/", data=data)
```

## 🔍 Troubleshooting

### Common Issues

#### 1. Import Errors
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

#### 2. API Connection Failed
- Ensure backend is running on port 8000
- Check firewall settings
- Verify `API_BASE_URL` in frontend configuration

#### 3. Empty Results
- Verify API keys are configured correctly
- Check that resumes are being parsed successfully
- Review logs in `data/logs/` directory

#### 4. Streamlit Port Issues
```bash
# Use different port
streamlit run frontend/streamlit_app.py --server.port 8502
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup
```bash
# Clone your fork
git clone https://github.com/yourusername/ResumeAI.git

# Install development dependencies
pip install -r requirements.txt

# Run tests
python test_setup.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the robust backend framework
- [Streamlit](https://streamlit.io/) for the beautiful frontend interface
- [Sentence Transformers](https://www.sbert.net/) for semantic embeddings
- [ChromaDB](https://www.trychroma.com/) for vector database capabilities
- [Groq](https://groq.com/) for fast AI inference

## 📞 Support

- 📧 Email: support@resumeai.com
- 🐛 Issues: [GitHub Issues](https://github.com/anilyadav6803/ResumeAI/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/anilyadav6803/ResumeAI/discussions)

## 🗺️ Roadmap

- [ ] Docker containerization
- [ ] Cloud deployment guides (AWS, GCP, Azure)
- [ ] Advanced analytics dashboard
- [ ] Integration with job boards
- [ ] Mobile application
- [ ] Enterprise features

---

⭐ **Star this repository if you find it helpful!**

Made with ❤️ by [Anil Yadav](https://github.com/anilyadav6803) - AI Resume Optimizer & Screening Agent

A comprehensive AI-powered tool for resume screening and ATS optimization built with FastAPI, Streamlit, and modern AI technologies.

## 🚀 Features

### For HR/Recruiters - Resume Screening
- **Batch Upload**: Process up to 20 resumes simultaneously
- **AI-Powered Matching**: Semantic similarity search to find best candidates
- **Smart Ranking**: AI-generated reasoning for candidate rankings
- **Information Extraction**: Automatically extract contact info, skills, and experience
- **Job Analysis**: Extract key requirements from job descriptions

### For Job Seekers - ATS Optimization
- **ATS Score**: Get a compatibility score out of 100
- **Keyword Analysis**: Identify missing keywords from job descriptions
- **Format Optimization**: Suggestions for ATS-friendly formatting
- **Content Improvement**: AI-powered recommendations for better content
- **Action Items**: Specific, actionable steps for improvement

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Sentence Transformers** - For semantic embeddings
- **ChromaDB** - Vector database for similarity search
- **Groq API** - Fast AI inference
- **PDFPlumber** - PDF text extraction
- **Python-docx** - Word document processing

### Frontend
- **Streamlit** - Interactive web interface
- **Plotly** - Data visualization
- **Pandas** - Data manipulation

### AI/ML
- **LangChain** - AI application framework
- **Hugging Face Transformers** - Pre-trained models
- **ChromaDB** - Vector storage and retrieval

## 📋 Prerequisites

- Python 3.8+
- pip package manager
- Git

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/ResumeAI.git
cd ResumeAI
```

### 2. Set up Virtual Environment
```bash
# Create virtual environment
python -m venv resume_optimizer
# Activate virtual environment
# On Windows:
.\resume_optimizer\Scripts\activate
# On macOS/Linux:
source resume_optimizer/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory:
```env
# AI API Keys (Get free keys from the providers)
GROQ_API_KEY=your_groq_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_API_KEY=your_google_gemini_api_key_here

# Database Configuration
DATABASE_URL=sqlite:///./resume_optimizer.db

# Application Settings
MAX_FILE_SIZE_MB=10
ALLOWED_FILE_TYPES=pdf,docx
MAX_RESUMES_PER_UPLOAD=20
```

### 5. Start the Backend API
```bash
uvicorn backend.app:app --reload
```
The API will be available at `http://localhost:8000`

### 6. Start the Frontend
```bash
streamlit run frontend/streamlit_app.py
```
The web interface will be available at `http://localhost:8501`

## 🔑 Free API Keys for Students

### Groq API (Recommended)
1. Sign up at [groq.com](https://groq.com)
2. Free tier: 60 queries/minute
3. Fast inference with Mixtral-8x7B model

### Google Gemini API
1. Get API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Free tier available
3. Powerful language model capabilities

### OpenAI API
1. Sign up at [openai.com](https://openai.com)
2. Free credits available via [GitHub Student Pack](https://education.github.com/pack)
3. GPT-3.5 and GPT-4 access

### Hugging Face (Always Free)
1. Sign up at [huggingface.co](https://huggingface.co)
2. Free inference API
3. Access to thousands of open-source models

## 📚 Usage Guide

### Resume Screening (HR/Recruiters)
1. **Upload Resumes**: Go to "Resume Screening" tab
2. **Select Files**: Upload multiple PDF/DOCX files
3. **Process**: Click "Process Resumes" to parse and index
4. **Job Description**: Enter the job description
5. **Find Matches**: Get AI-powered candidate rankings

### ATS Optimization (Job Seekers)
1. **Upload Resume**: Go to "ATS Optimization" tab
2. **Select File**: Upload your resume (PDF/DOCX)
3. **Job Description**: Paste the target job description
4. **Optimize**: Get detailed optimization recommendations

## 🏗️ Project Structure

```
ResumeAI/
├── backend/
│   ├── app.py                 # FastAPI application
│   ├── config.py              # Configuration settings
│   └── models/
│       ├── resume_parser.py   # Resume parsing logic
│       ├── job_matcher.py     # AI job matching
│       ├── embeddings.py      # Vector embeddings
│       └── ats_optimizer.py   # ATS optimization
├── frontend/
│   └── streamlit_app.py       # Web interface
├── data/
│   ├── resumes/              # Uploaded resumes
│   └── vector_db/            # Vector database
├── requirements.txt           # Python dependencies
├── .env                      # Environment variables
└── README.md                 # This file
```

## 🔧 Configuration

### Environment Variables
- `GROQ_API_KEY`: Groq API key for AI inference
- `OPENAI_API_KEY`: OpenAI API key (optional)
- `GOOGLE_API_KEY`: Google Gemini API key (optional)
- `MAX_FILE_SIZE_MB`: Maximum file size for uploads (default: 10)
- `MAX_RESUMES_PER_UPLOAD`: Maximum number of resumes per batch (default: 20)

### API Endpoints
- `GET /`: API information
- `POST /upload-resumes/`: Upload and process resumes
- `POST /match-resumes/`: Find matching candidates
- `POST /optimize-resume/`: Optimize single resume
- `GET /stats/`: System statistics
- `GET /health/`: Health check

## 🧪 Testing

### Test the API
```bash
# Test health endpoint
curl http://localhost:8000/health/

# Test with sample data
curl -X POST "http://localhost:8000/upload-resumes/" \
  -F "files=@sample_resume.pdf"
``` 