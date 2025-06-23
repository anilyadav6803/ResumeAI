import streamlit as st
import requests
import json
import pandas as pd
from typing import List, Dict
import plotly.express as px

# Configure Streamlit page
st.set_page_config(
    page_title="ResumeAI - AI Resume Optimizer & Matcher",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Modern CSS with improved aesthetics and usability
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    html, body, .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        color: #1a202c;
        min-height: 100vh;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu, footer, header, .stDeployButton, .stDecoration {
        visibility: hidden;
    }
    .css-1d391kg, .stSidebar, section[data-testid="stSidebar"] {
        display: none;
    }
    
    /* Main container styling */
    .main-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 1rem;
    }
    
    /* Header styling */
    .app-header {
        text-align: center;
        margin-bottom: 2rem;
        padding: 3rem 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        position: relative;
        overflow: hidden;
    }
    
    .app-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="50" cy="50" r="1" fill="rgba(255,255,255,0.1)"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
        opacity: 0.3;
    }
    
    .app-title {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
    }
    
    .app-subtitle {
        font-size: 1.2rem;
        opacity: 0.95;
        max-width: 600px;
        margin: 0 auto;
        font-weight: 400;
        line-height: 1.6;
        position: relative;
        z-index: 1;
    }
    
    /* Card styling */
    .card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 25px rgba(0,0,0,0.08);
        border: 1px solid rgba(226, 232, 240, 0.8);
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
        position: relative;
        overflow: hidden;
    }
    
    .card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.12);
    }
    
    .card-title {
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 1rem;
        color: #2d3748;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
      /* Fix text visibility in all elements */
    p, div, span, h1, h2, h3, h4, h5, h6 {
        color: #1a202c !important;
    }
    
    .stMarkdown {
        color: #1a202c !important;
    }
    
    .stMarkdown p, .stMarkdown div, .stMarkdown span {
        color: #1a202c !important;
    }
    
    /* Fix specific Streamlit components text color */
    .stInfo, .stSuccess, .stWarning, .stError {
        color: #1a202c !important;
    }
    
    .stInfo div, .stSuccess div, .stWarning div, .stError div {
        color: inherit !important;
    }
    
    /* Ensure expandable content is visible */
    .streamlit-expanderContent div,
    .streamlit-expanderContent p,
    .streamlit-expanderContent span {
        color: #1a202c !important;
    }
    
    /* Card text visibility */
    .card p, .card li {
        color: #4a5568 !important;
        line-height: 1.7;
        font-size: 1rem;
    }
    
    .card ul {
        margin-top: 1rem;
        padding-left: 1.5rem;
    }
    
    .card li {
        margin-bottom: 0.5rem;
        color: #4a5568 !important;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.8rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
        text-transform: none !important;
        letter-spacing: 0.5px !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6) !important;
        background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%) !important;
    }
    
    .stButton>button:active {
        transform: translateY(-1px) !important;
    }
    
    .stButton>button:disabled {
        background: #e2e8f0 !important;
        color: #a0aec0 !important;
        cursor: not-allowed !important;
        transform: none !important;
        box-shadow: none !important;
    }
      /* Form elements */
    .stTextArea>div>div>textarea, 
    .stTextInput>div>div>input {
        border: 2px solid #e2e8f0 !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        font-size: 1rem !important;
        color: #2d3748 !important;
        background: white !important;
        transition: all 0.2s ease !important;
    }
    
    .stTextArea>div>div>textarea:focus, 
    .stTextInput>div>div>input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
        outline: none !important;
    }
    
    /* Fix all form element labels and text */
    label, .stSelectbox label, .stNumberInput label, .stTextInput label, .stTextArea label {
        color: #2d3748 !important;
        font-weight: 600 !important;
    }
    
    /* Slider text */
    .stSlider label {
        color: #2d3748 !important;
        font-weight: 500 !important;
    }
    
    .stSlider p {
        color: #2d3748 !important;
        font-weight: 500 !important;
    }
    
    /* Form container styling */
    .stForm > div {
        background: rgba(255, 255, 255, 0.9) !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        border: 1px solid #e2e8f0 !important;
    }
    
    /* Additional text visibility improvements */
    .stForm .stMarkdown p,
    .stForm .stMarkdown div,
    .stForm .stMarkdown span,
    .stForm label {
        color: #2d3748 !important;
    }
    
    /* Column headers */
    .stMarkdown h3 {
        color: #2d3748 !important;
        font-weight: 600 !important;
        margin-bottom: 1rem !important;
    }
      .stFileUploader>div {
        border: 3px dashed #667eea !important;
        border-radius: 16px !important;
        background: rgba(255,255,255,0.95) !important;
        padding: 3rem 2rem !important;
        text-align: center !important;
        transition: all 0.3s ease !important;
    }
    
    .stFileUploader>div:hover {
        border-color: #5a67d8 !important;
        background: rgba(102, 126, 234, 0.1) !important;
    }
    
    /* File uploader text visibility */
    .stFileUploader label,
    .stFileUploader .stMarkdown p,
    .stFileUploader .stMarkdown div,
    .stFileUploader .stMarkdown span {
        color: #2d3748 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    
    .stFileUploader>div>div>div>button {
        background: #667eea !important;
        color: white !important;
        border: 2px solid #667eea !important;
        border-radius: 8px !important;
        padding: 1rem 2rem !important;
        font-weight: 600 !important;
    }
    
    .stFileUploader>div>div>div>button:hover {
        background: #5a67d8 !important;
        border-color: #5a67d8 !important;
    }
    
    /* Metrics styling */
    [data-testid="metric-container"] {
        border: 1px solid #e2e8f0 !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
        background: white !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05) !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="metric-container"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(0,0,0,0.1) !important;
    }
    
    [data-testid="metric-container"] > div {
        color: #2d3748 !important;
    }
    
    [data-testid="metric-container"] [data-testid="metric-value"] {
        color: #667eea !important;
        font-weight: 700 !important;
        font-size: 1.8rem !important;
    }
    
    /* Progress bar */
    .stProgress>div>div>div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%) !important;
        border-radius: 10px !important;
        height: 12px !important;
    }
    
    .stProgress>div>div {
        background: #e2e8f0 !important;
        border-radius: 10px !important;
        height: 12px !important;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: rgba(255,255,255,0.8);
        padding: 0.5rem;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 0.8rem 1.5rem !important;
        border-radius: 10px !important;
        transition: all 0.2s ease !important;
        font-weight: 500 !important;
        color: #4a5568 !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3) !important;
    }
    
    /* Slider styling */
    .stSlider>div>div>div>div {
        background-color: #667eea !important;
    }
    
    .stSlider>div>div>div>div>div {
        color: #2d3748 !important;
        font-weight: 600 !important;
    }
    
    .stSlider p {
        color: #2d3748 !important;
        font-weight: 500 !important;
    }
    
    /* Alert and info boxes */
    .stAlert {
        border-radius: 12px !important;
        border: none !important;
        padding: 1rem 1.5rem !important;
        margin: 1rem 0 !important;
    }
    
    .stSuccess {
        background: rgba(72, 187, 120, 0.1) !important;
        color: #2f855a !important;
        border-left: 4px solid #48bb78 !important;
    }
    
    .stWarning {
        background: rgba(237, 137, 54, 0.1) !important;
        color: #c05621 !important;
        border-left: 4px solid #ed8936 !important;
    }
    
    .stError {
        background: rgba(245, 101, 101, 0.1) !important;
        color: #c53030 !important;
        border-left: 4px solid #f56565 !important;
    }
    
    .stInfo {
        background: rgba(102, 126, 234, 0.1) !important;
        color: #553c9a !important;
        border-left: 4px solid #667eea !important;
    }
      /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(255,255,255,0.95) !important;
        border-radius: 12px !important;
        border: 1px solid #e2e8f0 !important;
        color: #2d3748 !important;
        font-weight: 600 !important;
        padding: 1rem !important;
    }
    
    .streamlit-expanderContent {
        background: white !important;
        border-radius: 0 0 12px 12px !important;
        border: 1px solid #e2e8f0 !important;
        border-top: none !important;
        color: #1a202c !important;
        padding: 1rem !important;
    }
    
    .streamlit-expanderContent p, 
    .streamlit-expanderContent div,
    .streamlit-expanderContent span,
    .streamlit-expanderContent label {
        color: #1a202c !important;
    }
    
    /* Force expander content to be visible */
    details[open] summary ~ * {
        animation: fadeIn 0.3s ease-in-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* Responsive design */
    @media (max-width: 1024px) {
        .main-container {
            padding: 1rem 0.5rem;
        }
        
        .app-header {
            padding: 2rem 1.5rem;
        }
        
        .app-title {
            font-size: 2.5rem;
        }
        
        .card {
            padding: 1.5rem;
        }
    }
    
    @media (max-width: 768px) {
        .app-title {
            font-size: 2.2rem;
        }
        
        .app-subtitle {
            font-size: 1.1rem;
        }
        
        .card {
            padding: 1.25rem;
            margin-bottom: 1.5rem;
        }
        
        .card-title {
            font-size: 1.25rem;
        }
        
        .main-container {
            padding: 0.5rem;
        }
        
        .stButton>button {
            padding: 0.7rem 1.5rem !important;
            font-size: 0.95rem !important;
        }
    }
    
    @media (max-width: 576px) {
        .app-title {
            font-size: 1.9rem;
        }
        
        .app-subtitle {
            font-size: 1rem;
            padding: 0 1rem;
        }
        
        .card-title {
            font-size: 1.1rem;
            flex-direction: column;
            gap: 0.5rem;
            text-align: center;
        }
        
        .card {
            padding: 1rem;
        }
        
        .app-header {
            padding: 1.5rem 1rem;
            margin-bottom: 1rem;
        }
        
        [data-testid="metric-container"] {
            padding: 1rem !important;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 0.6rem 1rem !important;
            font-size: 0.9rem !important;
        }
    }
    
    /* Footer styling */
    .app-footer {
        text-align: center;
        padding: 3rem 2rem;
        margin-top: 3rem;
        background: white;
        border-radius: 20px 20px 0 0;
        color: #4a5568;
        border-top: 1px solid #e2e8f0;
        box-shadow: 0 -5px 15px rgba(0,0,0,0.05);
    }
    
    .footer-content {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 1rem;
    }
    
    .footer-links {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin-bottom: 1.5rem;
        flex-wrap: wrap;
    }
    
    .footer-links a {
        color: #4a5568;
        text-decoration: none;
        font-weight: 500;
        transition: all 0.2s ease;
        padding: 0.5rem 1rem;
        border-radius: 8px;
    }
    
    .footer-links a:hover {
        color: #667eea;
        background: rgba(102, 126, 234, 0.1);
    }
    
    .copyright {
        font-size: 0.9rem;
        opacity: 0.8;
        margin-top: 1rem;
        color: #718096;
    }
    
    @media (max-width: 576px) {
        .footer-links {
            gap: 1rem;
        }
        
        .footer-links a {
            padding: 0.4rem 0.8rem;
            font-size: 0.9rem;
        }
        
        .app-footer {
            padding: 2rem 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# API Configuration
API_BASE_URL = "http://127.0.0.1:8000"

# Helper functions
def call_api(endpoint: str, method: str = "GET", data=None, files=None):
    """Make API calls to the backend"""
    try:
        url = f"{API_BASE_URL}{endpoint}"
        
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            if files:
                response = requests.post(url, data=data, files=files)
            else:
                response = requests.post(url, data=data)
        elif method == "DELETE":
            response = requests.delete(url)
        
        if response.status_code == 200:
            return response.json(), None
        else:
            return None, f"API Error: {response.status_code} - {response.text}"
    
    except requests.exceptions.ConnectionError:
        return None, "Cannot connect to API. Please make sure the backend server is running."
    except Exception as e:
        return None, f"Error: {str(e)}"

def display_resume_matches(matches: List[Dict]):
    """Display resume matches in a formatted way"""
    if not matches:
        st.warning("No matching resumes found.")
        return
    
    for i, match in enumerate(matches):        # Convert score to percentage, handle values that might be > 1.0
        raw_score = match['score']
        if raw_score <= 1.0:
            score_percent = int(raw_score * 100)
        else:
            # If score is > 1.0, treat it as already a percentage or normalize it
            score_percent = min(int(raw_score * 100), 100) if raw_score < 10 else min(int(raw_score), 100)
        
        # Determine score color
        if score_percent >= 80:
            score_color = "#22c55e"  # Green
            score_icon = "🏆"
        elif score_percent >= 60:
            score_color = "#f59e0b"  # Amber
            score_icon = "⭐"
        else:
            score_color = "#ef4444"  # Red
            score_icon = "📋"
          # Create candidate card
        st.markdown(f"""
        <div class="card" style="border-left: 4px solid {score_color}; margin-bottom: 1rem; background: white !important; color: #1a202c !important;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; flex-wrap: wrap; gap: 1rem;">
                <h3 style="margin: 0; color: #2d3748 !important; font-size: 1.2rem;">
                    {score_icon} Rank #{i+1}: {match['file_name']}
                </h3>
                <div style="background: {score_color}; color: white; padding: 0.5rem 1rem; border-radius: 20px; font-weight: 600;">
                    {score_percent}% Match
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
          # Expandable details
        with st.expander(f"View detailed information for {match['file_name']}", expanded=(i==0)):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**👤 Candidate Information**")
                candidate_name = match['metadata'].get('name', 'Not specified')
                candidate_email = match['metadata'].get('email', 'Not specified')
                candidate_experience = match['metadata'].get('experience_years', 'Not specified')
                
                st.markdown(f"""
                <div style="color: #1a202c !important;">
                <strong>Name:</strong> {candidate_name}<br>
                <strong>Email:</strong> {candidate_email}<br>
                <strong>Experience:</strong> {candidate_experience} years
                </div>                """, unsafe_allow_html=True)
                
                # Skills
                skills = match['metadata'].get('skills', 'Not specified')
                if skills and skills != 'Not specified':
                    st.markdown("**🛠️ Skills:**")
                    if isinstance(skills, list):
                        skills_html = "<div style='color: #1a202c !important;'>"
                        for skill in skills[:8]:  # Show first 8 skills
                            skills_html += f"• {skill}<br>"
                        if len(skills) > 8:
                            skills_html += f"... and {len(skills) - 8} more skills"
                        skills_html += "</div>"
                        st.markdown(skills_html, unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div style='color: #1a202c !important;'>• {skills}</div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown("**📊 Match Analysis**")
                st.markdown(f"""
                <div style="color: #1a202c !important;">
                <strong>Overall Score:</strong> {score_percent}%<br>
                <strong>Raw Score:</strong> {match['score']:.4f}<br>
                <strong>Match Quality:</strong> {match.get('match_count', 0)} segments<br>
                <strong>Average Score:</strong> {match.get('avg_score', 0):.4f}
                </div>
                """, unsafe_allow_html=True)
                
                # Progress bar for visual score representation
                st.markdown("**Score Breakdown:**")
                # Ensure progress value is between 0 and 1
                progress_value = min(max(match['score'], 0.0), 1.0)
                st.progress(progress_value)
              # Best matching text
            st.markdown("**🎯 Best Matching Content:**")
            match_text = match.get('best_match_text', 'No matching text available')
            st.markdown(f"""
            <div style="background: rgba(102, 126, 234, 0.1); padding: 1rem; border-radius: 8px; color: #1a202c !important;">
            💡 {match_text}
            </div>
            """, unsafe_allow_html=True)
            
            # Add a divider between candidates
            if i < len(matches) - 1:
                st.markdown("---")

def display_optimization_results(results: Dict):
    """Display ATS optimization results"""
    if 'error' in results:
        st.error(f"Optimization Error: {results['error']}")
        return
    
    # ATS Score
    ats_score = results.get('ats_score', 0)
    st.write("### 📊 Optimization Results")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("ATS Score", f"{ats_score}/100")
    with col2:
        st.metric("Missing Keywords", len(results.get('missing_keywords', [])))
    with col3:
        st.metric("Strengths", len(results.get('strengths', [])))
    
    # Progress bar for ATS score
    st.progress(ats_score / 100)
    
    # Score interpretation
    if ats_score >= 80:
        st.success("🎉 Excellent! Your resume is well-optimized for ATS systems.")
    elif ats_score >= 60:
        st.warning("⚠️ Good, but there's room for improvement.")
    else:
        st.error("🚨 Your resume needs significant optimization for ATS systems.")
    
    # Detailed results in tabs
    tab1, tab2, tab3 = st.tabs(["🔍 Missing Keywords", "✅ Strengths", "🔧 Improvements"])
    
    with tab1:
        missing_keywords = results.get('missing_keywords', [])
        if missing_keywords:
            st.write("**Keywords to add to your resume:**")
            for keyword in missing_keywords:
                st.write(f"• {keyword}")
        else:
            st.success("Great! No critical keywords are missing.")
    
    with tab2:
        strengths = results.get('strengths', [])
        if strengths:
            st.write("**Your resume already includes these important keywords:**")
            for strength in strengths:
                st.write(f"✅ {strength}")
        else:
            st.info("Consider adding more relevant keywords from the job description.")
    
    with tab3:
        improvements = results.get('format_improvements', []) + results.get('content_suggestions', [])
        if improvements:
            st.write("**Suggested Improvements:**")
            for item in improvements:
                st.write(f"• {item}")
        else:
            st.info("No specific improvement suggestions available.")

# Main App
def main():
    # Initialize session state for navigation and advanced options
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Home"
    if 'advanced_options_expanded' not in st.session_state:
        st.session_state.advanced_options_expanded = True
    
    # Header
    st.markdown("""
    <div class="main-container">
        <div class="app-header">
            <h1 class="app-title">ResumeAI</h1>
            <p class="app-subtitle">AI-powered Resume Optimization and Matching System</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Check API connection
    health_data, health_error = call_api("/health/")
    if health_error:
        st.warning(f"⚠️ Backend API Connection Issue: {health_error}")
        st.info("Some features may not work properly. Please make sure the backend server is running at http://127.0.0.1:8000")
    else:
        st.success("✅ Backend API is connected and healthy")
    
    # Navigation buttons
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.current_page = "Home"
            st.rerun()
    with col2:
        if st.button("📋 Screening", use_container_width=True):
            st.session_state.current_page = "Resume Screening"
            st.rerun()
    with col3:
        if st.button("✨ Optimization", use_container_width=True):
            st.session_state.current_page = "ATS Optimization"
            st.rerun()
    with col4:
        if st.button("📊 Stats", use_container_width=True):
            st.session_state.current_page = "Statistics"
            st.rerun()
    
    # Main content based on current page
    if st.session_state.current_page == "Home":
        show_home_page()
    elif st.session_state.current_page == "Resume Screening":
        show_resume_screening()
    elif st.session_state.current_page == "ATS Optimization":
        show_ats_optimization()
    elif st.session_state.current_page == "Statistics":
        show_statistics()
    
    # Footer
    st.markdown("""
    <div class="app-footer">
        <div class="footer-content">
            <div class="footer-links">
                <a href="mailto:support@resumeai.com">📧 Contact</a>
                <a href="#">📖 Documentation</a>
                <a href="#">🔒 Privacy Policy</a>
                <a href="#">📋 Terms of Service</a>
                <a href="#">❓ Help</a>
            </div>
            <div class="copyright">
                © 2025 ResumeAI. All rights reserved. | Made with ❤️ using Streamlit
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_home_page():
    st.markdown("""
    <div class="main-container">
        <div class="card">
            <h2 class="card-title">🚀 Welcome to ResumeAI</h2>
            <p>ResumeAI helps recruiters find the best candidates and job seekers optimize their resumes for Applicant Tracking Systems (ATS).</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature cards in columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h2 class="card-title">📋 Resume Screening</h2>
            <p>Upload multiple resumes and match them against job descriptions to find the most qualified candidates.</p>
            <ul>
                <li>AI-powered semantic matching</li>
                <li>Detailed candidate ranking</li>
                <li>Skills and experience extraction</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Try Resume Screening", key="home_screening", use_container_width=True):
            st.session_state.current_page = "Resume Screening"
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="card">
            <h2 class="card-title">✨ ATS Optimization</h2>
            <p>Get your resume optimized to pass through Applicant Tracking Systems and get more interviews.</p>
            <ul>
                <li>ATS compatibility score</li>
                <li>Missing keywords identification</li>
                <li>Format improvement suggestions</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Optimize Your Resume", key="home_optimization", use_container_width=True):
            st.session_state.current_page = "ATS Optimization"
            st.rerun()

def show_resume_screening():
    st.markdown("""
    <div class="main-container">
        <div class="card">
            <h2 class="card-title">📋 Resume Screening</h2>
            <p>Upload resumes and match them against a job description to find the best candidates.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)    
    
    # Initialize session state for form validation
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = None
    if 'job_description' not in st.session_state:
        st.session_state.job_description = ""
    
    with st.form("resume_screening_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📤 Upload Resumes")
            uploaded_files = st.file_uploader(
                "Choose resume files (PDF or DOCX)",
                accept_multiple_files=True,
                type=['pdf', 'docx'],
                help="Upload multiple resumes to screen (up to 20 files)"
            )
            
            if uploaded_files:
                st.success(f"✅ {len(uploaded_files)} files selected")
                st.session_state.uploaded_files = uploaded_files
                
                # Show file preview
                with st.expander("📋 Selected Files Preview", expanded=False):
                    for i, file in enumerate(uploaded_files[:5]):  # Show first 5 files
                        file_size = len(file.getvalue()) / 1024  # Size in KB
                        st.write(f"{i+1}. {file.name} ({file_size:.1f} KB)")
                    if len(uploaded_files) > 5:
                        st.info(f"... and {len(uploaded_files) - 5} more files")
        
        with col2:
            st.markdown("### 📝 Job Description")
            job_description = st.text_area(
                "Paste the job description here",
                height=300,
                placeholder="Enter the job description to match against...",
                help="The more detailed the job description, the better the matching results"
            )
            st.session_state.job_description = job_description
              # Advanced options - always visible with session state persistence
            with st.expander("⚙️ Advanced Options", expanded=st.session_state.get('advanced_options_expanded', True)):
                match_threshold = st.slider(
                    "Minimum match threshold",
                    min_value=0.0,
                    max_value=1.0,
                    value=0.5,
                    step=0.05,
                    help="Set higher to get only the best matches"
                )
                max_results = st.slider(
                    "Maximum results to show",
                    min_value=1,
                    max_value=20,
                    value=5,
                    help="Limit the number of candidates to display"
                )
        
        # Submit button
        submit_button = st.form_submit_button(
            "🔍 Match Resumes",
            type="primary",
            use_container_width=True
        )
    
    # Process form submission
    if submit_button:
        if not uploaded_files:
            st.error("Please upload at least one resume file")
            return
        
        if not job_description.strip():
            st.error("Please enter a job description")
            return
        
        with st.spinner("🔍 Analyzing resumes..."):
            # Prepare files for API
            files = [("files", (file.name, file.getvalue(), file.type)) for file in uploaded_files]
            data = {
                "job_description": job_description,
                "match_threshold": str(match_threshold),
                "max_results": str(max_results)
            }
              # Step 1: Upload resumes first
            files_for_upload = [("files", (file.name, file.getvalue(), file.type)) for file in uploaded_files]
            
            upload_response, upload_error = call_api(
                "/upload-resumes/",
                method="POST",
                files=files_for_upload
            )
            
            if upload_error:
                st.error(f"Error uploading resumes: {upload_error}")
                return
            
            st.info(f"✅ Successfully uploaded {upload_response['successful_parses']} resumes")
            
            # Step 2: Match resumes to job description
            match_data = {
                "job_description": job_description,
                "top_k": str(max_results)
            }            
            response, error = call_api(
                "/match-resumes/",
                method="POST",
                data=match_data
            )
            
            if error:
                st.error(f"Error during matching: {error}")
                return
            
            # Display results
            st.success("✅ Matching completed successfully!")
            
            # Check if matches exist in response
            matches = response.get('matches', [])
            if not matches:
                st.warning("No matching candidates found. Try adjusting your search criteria.")
                return
                
            st.markdown(f"### 🏆 Top {len(matches)} Matches")
            
            # Show metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Resumes Processed", response.get('total_candidates_in_db', len(uploaded_files)))
            with col2:
                st.metric("Qualified Candidates", len(matches))
            with col3:
                avg_score = sum(match['score'] for match in matches) / len(matches) if matches else 0
                st.metric("Average Match Score", f"{avg_score:.1%}")
            
            # Display matches
            display_resume_matches(matches)

def show_ats_optimization():
    st.markdown("""
    <div class="main-container">
        <div class="card">
            <h2 class="card-title">✨ ATS Resume Optimization</h2>
            <p>Upload your resume and a job description to get optimization suggestions for better ATS performance.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("ats_optimization_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📄 Upload Your Resume")
            resume_file = st.file_uploader(
                "Choose your resume file",
                type=['pdf', 'docx'],
                help="Upload your resume in PDF or DOCX format"
            )
            
            if resume_file:
                st.success(f"✅ {resume_file.name} selected")
                
                # Show file info
                file_size = len(resume_file.getvalue()) / 1024  # Size in KB
                st.info(f"File size: {file_size:.1f} KB")
        
        with col2:
            st.markdown("### 📝 Job Description")
            job_description = st.text_area(
                "Paste the job description to optimize for",
                height=300,
                placeholder="Enter the job description you're applying for...",
                help="The more detailed the job description, the better the optimization"
            )
            
            # Advanced options
            with st.expander("⚙️ Advanced Options", expanded=False):
                strictness = st.slider(
                    "Optimization Strictness",
                    min_value=1,
                    max_value=5,
                    value=3,
                    help="Higher values will suggest more changes for better ATS compatibility"
                )
        
        # Submit button
        submit_button = st.form_submit_button(
            "✨ Optimize Resume",
            type="primary",
            use_container_width=True
        )
    
    # Process form submission
    if submit_button:
        if not resume_file:
            st.error("Please upload your resume file")
            return
        
        if not job_description.strip():
            st.error("Please enter a job description")
            return
        
        with st.spinner("✨ Optimizing your resume..."):
            # Prepare file for API
            files = [("resume", (resume_file.name, resume_file.getvalue(), resume_file.type))]
            data = {
                "job_description": job_description,
                "strictness": str(strictness)
            }
            
            # Call API
            response, error = call_api(
                "/optimize/",
                method="POST",
                data=data,
                files=files
            )
            
            if error:
                st.error(f"Error during optimization: {error}")
                return
            
            # Display results
            st.success("✅ Optimization completed successfully!")
            display_optimization_results(response)
            
            # Download optimized resume if available
            if 'optimized_resume_url' in response:
                st.markdown("### 📥 Download Optimized Resume")
                st.markdown(
                    f"Your optimized resume is ready! [Download here]({API_BASE_URL}{response['optimized_resume_url']})",
                    unsafe_allow_html=True
                )

def show_statistics():
    st.markdown("""
    <div class="main-container">
        <div class="card">
            <h2 class="card-title">📊 Statistics & Analytics</h2>
            <p>View insights and analytics about your resume screening and optimization activities.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Get stats from API
    stats_data, error = call_api("/stats/")
    
    if error:
        st.warning(f"Could not load statistics: {error}")
        st.info("Statistics will appear after you've processed some resumes")
        return
    
    if not stats_data or 'total_resumes' not in stats_data:
        st.info("No statistics available yet. Process some resumes to see analytics.")
        return
    
    # Display key metrics
    st.markdown("### 📈 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Resumes Processed", stats_data['total_resumes'])
    with col2:
        st.metric("Average Match Score", f"{stats_data['avg_match_score']:.1%}")
    with col3:
        st.metric("Average Optimization Score", f"{stats_data['avg_optimization_score']}/100")
    with col4:
        st.metric("Most Common Skill", stats_data['most_common_skill'] or "N/A")
    
    # Charts section
    st.markdown("### 📊 Visualization")
    
    tab1, tab2, tab3 = st.tabs(["Match Scores", "Skill Distribution", "Optimization Trends"])
    
    with tab1:
        if stats_data.get('match_score_distribution'):
            df_scores = pd.DataFrame({
                'Score Range': ['0-20%', '20-40%', '40-60%', '60-80%', '80-100%'],
                'Count': stats_data['match_score_distribution']
            })
            fig = px.bar(
                df_scores,
                x='Score Range',
                y='Count',
                title='Resume Match Score Distribution',
                color='Count',
                color_continuous_scale='Bluyl'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No match score data available yet")
    
    with tab2:
        if stats_data.get('top_skills'):
            df_skills = pd.DataFrame({
                'Skill': [skill['name'] for skill in stats_data['top_skills']],
                'Count': [skill['count'] for skill in stats_data['top_skills']]
            })
            fig = px.pie(
                df_skills,
                names='Skill',
                values='Count',
                title='Top 10 Skills Across Resumes',
                hole=0.3
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No skill data available yet")
    
    with tab3:
        if stats_data.get('optimization_trends') and len(stats_data['optimization_trends']) > 1:
            df_trends = pd.DataFrame({
                'Date': [item['date'] for item in stats_data['optimization_trends']],
                'Score': [item['score'] for item in stats_data['optimization_trends']]
            })
            fig = px.line(
                df_trends,
                x='Date',
                y='Score',
                title='Average Optimization Score Over Time',
                markers=True
            )
            fig.update_yaxes(range=[0, 100])
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Not enough data to show optimization trends")

if __name__ == "__main__":
    main()