# ResumeAI - AI Resume Optimizer & Screening Agent

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

### Run Frontend Tests
```bash
streamlit run frontend/streamlit_app.py
```

## 📊 Features in Detail

### Resume Parsing
- Extract text from PDF and DOCX files
- Identify contact information (email, phone)
- Extract skills and experience
- Calculate resume metrics

### Job Matching
- Semantic similarity search using embeddings
- AI-powered candidate ranking
- Detailed match explanations
- Skill gap analysis

### ATS Optimization
- Keyword optimization analysis
- Format compatibility scoring
- Content improvement suggestions
- Actionable recommendations

## 🚀 Deployment Options

### Free Deployment Platforms

#### Backend (FastAPI)
- **Railway.app**: Free tier with 512MB RAM
- **Render.com**: Free tier with auto-sleep
- **Fly.io**: Generous free tier

#### Frontend (Streamlit)
- **Streamlit Cloud**: Free for public apps
- **Heroku**: Free tier (limited hours)

#### Database
- **PlanetScale**: Free MySQL database
- **Supabase**: Free PostgreSQL with vector support

### Deployment Commands

#### Railway
```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy backend
railway login
railway init
railway up
```

#### Streamlit Cloud
1. Push code to GitHub
2. Connect at [share.streamlit.io](https://share.streamlit.io)
3. Deploy directly from repository

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Common Issues

1. **API Connection Error**: Make sure the backend is running on port 8000
2. **Import Errors**: Ensure all dependencies are installed (`pip install -r requirements.txt`)
3. **File Upload Issues**: Check file size limits and supported formats
4. **AI Features Not Working**: Verify API keys are set in `.env` file

### Getting Help

- 📧 Email: your-email@example.com
- 💬 Discord: [Join our community](#)
- 📝 Issues: [GitHub Issues](https://github.com/yourusername/ResumeAI/issues)

## 🔮 Future Enhancements

- [ ] Multi-language support
- [ ] Resume templates generation
- [ ] Interview question suggestions
- [ ] Salary analysis integration
- [ ] Advanced analytics dashboard
- [ ] Mobile app development

## 🙏 Acknowledgments

- **Hugging Face** for open-source models
- **ChromaDB** for vector database
- **Streamlit** for rapid frontend development
- **FastAPI** for modern Python web framework
- **Groq** for fast AI inference

---

**Built with ❤️ for the community**

*This project is designed to help job seekers and recruiters leverage AI for better hiring outcomes.*
#   R e s u m e A I  
 