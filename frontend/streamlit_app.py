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
    
    .card p, .card li {
        color: #4a5568;
        line-height: 1.7;
        font-size: 1rem;
    }
    
    .card ul {
        margin-top: 1rem;
        padding-left: 1.5rem;
    }
    
    .card li {
        margin-bottom: 0.5rem;
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
    
    .stFileUploader>div {
        border: 3px dashed #cbd5e0 !important;
        border-radius: 16px !important;
        background: rgba(255,255,255,0.8) !important;
        padding: 3rem 2rem !important;
        text-align: center !important;
        transition: all 0.3s ease !important;
    }
    
    .stFileUploader>div:hover {
        border-color: #667eea !important;
        background: rgba(102, 126, 234, 0.05) !important;
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
        background: rgba(255,255,255,0.8) !important;
        border-radius: 12px !important;
        border: 1px solid #e2e8f0 !important;
        color: #2d3748 !important;
        font-weight: 600 !important;
    }
    
    .streamlit-expanderContent {
        background: white !important;
        border-radius: 0 0 12px 12px !important;
        border: 1px solid #e2e8f0 !important;
        border-top: none !important;
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
        return None, f"Error: {str(e)}"

def display_resume_matches(matches: List[Dict]):
    """Display resume matches in a formatted way"""
    if not matches:
        st.warning("No matching resumes found.")
        return
    
    for i, match in enumerate(matches):
        # Convert score to percentage
        score_percent = int(match['score'] * 100)
        
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
        <div class="card" style="border-left: 4px solid {score_color}; margin-bottom: 1rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <h3 style="margin: 0; color: #2d3748; font-size: 1.2rem;">
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
                - **Name:** {candidate_name}
                - **Email:** {candidate_email}
                - **Experience:** {candidate_experience} years
                """)
                
                # Skills
                skills = match['metadata'].get('skills', 'Not specified')
                if skills and skills != 'Not specified':
                    st.markdown("**🛠️ Skills:**")
                    if isinstance(skills, list):
                        for skill in skills[:8]:  # Show first 8 skills
                            st.markdown(f"• {skill}")
                        if len(skills) > 8:
                            st.markdown(f"... and {len(skills) - 8} more skills")
                    else:
                        st.markdown(f"• {skills}")
            
            with col2:
                st.markdown("**📊 Match Analysis**")
                st.markdown(f"""
                - **Overall Score:** {score_percent}%
                - **Raw Score:** {match['score']:.4f}
                - **Match Quality:** {match.get('match_count', 0)} segments
                - **Average Score:** {match.get('avg_score', 0):.4f}
                """)
                
                # Progress bar for visual score representation
                st.markdown("**Score Breakdown:**")
                st.progress(match['score'])
            
            # Best matching text
            st.markdown("**🎯 Best Matching Content:**")
            match_text = match.get('best_match_text', 'No matching text available')
            st.info(f"💡 {match_text}")
            
            # Add a divider between candidates
            if i < len(matches) - 1:
                st.markdown("---")
        st.markdown(f"""
        <div class="card" style="border-left: 4px solid {score_color}; margin-bottom: 1rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; flex-wrap: wrap; gap: 1rem;">
                <h3 style="margin: 0; color: #2d3748; font-size: 1.2rem;">
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
                - **Name:** {candidate_name}
                - **Email:** {candidate_email}
                - **Experience:** {candidate_experience} years
                """)
                
                # Skills
                skills = match['metadata'].get('skills', 'Not specified')
                if skills and skills != 'Not specified':
                    st.markdown("**🛠️ Skills:**")
                    if isinstance(skills, list):
                        for skill in skills[:8]:  # Show first 8 skills
                            st.markdown(f"• {skill}")
                        if len(skills) > 8:
                            st.markdown(f"... and {len(skills) - 8} more skills")
                    else:
                        st.markdown(f"• {skills}")
            
            with col2:
                st.markdown("**📊 Match Analysis**")
                st.markdown(f"""
                - **Overall Score:** {score_percent}%
                - **Raw Score:** {match['score']:.4f}
                - **Match Quality:** {match.get('match_count', 0)} segments
                - **Average Score:** {match.get('avg_score', 0):.4f}
                """)
                
                # Progress bar for visual score representation
                st.markdown("**Score Breakdown:**")
                st.progress(match['score'])
            
            # Best matching text
            st.markdown("**🎯 Best Matching Content:**")
            match_text = match.get('best_match_text', 'No matching text available')
            st.info(f"💡 {match_text}")
            
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
    # Initialize session state for navigation
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Home"
    
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
                        st.write(f"{i+1}. **{file.name}** ({file_size:.1f} KB)")
                    if len(uploaded_files) > 5:
                        st.write(f"... and {len(uploaded_files) - 5} more files")
            else:
                st.session_state.uploaded_files = None
        
        with col2:
            st.markdown("### 💼 Job Description")
            job_description = st.text_area(
                "Paste the job description here",
                height=200,
                placeholder="Include job title, required skills, experience, and responsibilities...",
                help="Provide a detailed job description for better matching results"
            )
            st.session_state.job_description = job_description
            
            st.markdown("### ⚙️ Settings")
            col2a, col2b = st.columns(2)
            with col2a:
                st.markdown("**Number of Top Candidates:**")
                top_k = st.slider("Select number of candidates", 1, 10, 1, help="Number of best candidates to show", key="top_k_slider", label_visibility="collapsed")
                st.write(f"Show top **{top_k}** candidates")
            with col2b:
                st.markdown("**Minimum Match Score:**")
                min_score = st.slider("Select minimum score", 0, 100, 50, help="Minimum match score threshold", key="min_score_slider", label_visibility="collapsed")
                st.write(f"Minimum score: **{min_score}%**")
        
        # Check if form is ready for submission
        form_ready = bool(uploaded_files and job_description.strip())
        
        # Always show validation messages
        st.markdown("---")
        col_info1, col_info2 = st.columns(2)
        
        with col_info1:
            if not uploaded_files:
                st.info("📄 Please upload resume files to continue")
            else:
                st.success(f"✅ {len(uploaded_files)} resume files ready")
        
        with col_info2:
            if not job_description.strip():
                st.info("📝 Please enter a job description to continue")
            else:
                st.success(f"✅ Job description ready ({len(job_description)} characters)")
        
        # Submit button - disabled state handled by Streamlit form
        submitted = st.form_submit_button(
            "🚀 Find Best Candidates", 
            type="primary", 
            use_container_width=True,
            disabled=not form_ready
        )
        
        # Show button status for debugging
        if not form_ready:
            st.caption("⚠️ Button is disabled. Please complete both upload and job description fields.")
        else:
            st.caption("✅ Ready to analyze candidates!")
        
        if submitted and form_ready:
            with st.spinner("🔍 Analyzing candidates..."):
                # Progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    # Step 1: Upload resumes
                    status_text.text("📤 Uploading resumes...")
                    progress_bar.progress(25)
                    
                    files = [("files", (file.name, file.getvalue(), file.type)) for file in uploaded_files]
                    upload_result, upload_error = call_api("/upload-resumes/", "POST", files=files)
                    
                    if upload_error:
                        st.error(f"❌ Upload failed: {upload_error}")
                        return
                    
                    # Step 2: Process matching
                    status_text.text("🤖 AI analyzing candidates...")
                    progress_bar.progress(50)
                    
                    data = {"job_description": job_description, "top_k": top_k}
                    match_result, match_error = call_api("/match-resumes/", "POST", data=data)
                    
                    progress_bar.progress(75)
                    
                    if match_error:
                        st.error(f"❌ Matching failed: {match_error}")
                        return
                    
                    # Step 3: Display results
                    status_text.text("✅ Preparing results...")
                    progress_bar.progress(100)
                    
                    # Clear progress indicators
                    progress_bar.empty()
                    status_text.empty()
                    
                    st.success("🎉 Analysis completed successfully!")
                    
                    # Show results
                    matches = match_result.get('matches', [])
                    if matches:
                        # Filter by minimum score
                        filtered_matches = [m for m in matches if (m['score'] * 100) >= min_score]
                        
                        if filtered_matches:
                            st.markdown(f"""
                            <h2 style="font-family: 'Inter', sans-serif; color: #2d3748; margin: 1.5rem 0 1rem 0;">
                                🏆 Top {len(filtered_matches)} Candidates (Min Score: {min_score}%)
                            </h2>
                            """, unsafe_allow_html=True)
                            
                            display_resume_matches(filtered_matches)
                        else:
                            st.warning(f"⚠️ No candidates found with score ≥ {min_score}%. Try lowering the minimum score threshold.")
                    else:
                        st.warning("⚠️ No matching candidates found. Try adjusting your job description or uploading different resumes.")
                        
                except Exception as e:
                    st.error(f"❌ An error occurred: {str(e)}")
                finally:
                    # Clean up progress indicators
                    progress_bar.empty()
                    status_text.empty()

def show_ats_optimization():
    st.markdown("""
    <div class="main-container">
        <div class="card">
            <h2 class="card-title">✨ ATS Resume Optimization</h2>
            <p>Upload your resume and a job description to get optimization recommendations.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("ats_optimization_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("### 📄 Your Resume")
            uploaded_file = st.file_uploader(
                "Upload your resume (PDF or DOCX)",
                type=['pdf', 'docx']
            )
            
            if uploaded_file:
                st.success(f"✅ {uploaded_file.name} uploaded")
        
        with col2:
            st.write("### 💼 Target Job Description")
            job_description = st.text_area(
                "Paste the job description you're applying for",
                height=200,
                placeholder="Include required skills, qualifications, and responsibilities"
            )
        
        submitted = st.form_submit_button("🚀 Analyze & Optimize", type="primary")
        
        if submitted:
            if not uploaded_file:
                st.error("Please upload your resume")
            elif not job_description.strip():
                st.error("Please enter a job description")
            else:
                with st.spinner("Analyzing your resume..."):
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    data = {"job_description": job_description}
                    
                    result, error = call_api("/optimize-resume/", "POST", data=data, files=files)
                    
                    if error:
                        st.error(f"Analysis failed: {error}")
                    else:
                        st.success("Analysis completed!")
                        
                        # Show resume info
                        resume_info = result.get('resume_info', {})
                        st.write("## 📄 Resume Overview")
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Word Count", resume_info.get('word_count', 'N/A'))
                        with col2:
                            st.metric("Skills Found", len(resume_info.get('skills_found', [])))
                        with col3:
                            st.metric("Contact Info", "✅" if resume_info.get('email') else "❌")
                        
                        # Show optimization results
                        display_optimization_results(result.get('optimization_results', {}))

def show_statistics():
    st.markdown("""
    <div class="main-container">
        <div class="card">
            <h2 class="card-title">📊 System Statistics</h2>
            <p>View analytics and metrics about processed resumes.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    stats_data, stats_error = call_api("/stats/")
    
    if stats_error:
        st.error(stats_error)
    else:
        # Overview metrics
        st.write("## 📈 Overview")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Resumes", stats_data.get('total_resumes_processed', 0))
        with col2:
            st.metric("Success Rate", f"{stats_data.get('success_rate', 0):.1f}%")
        with col3:
            st.metric("Avg Processing Time", f"{stats_data.get('avg_processing_time', 0):.1f}s")
        
        # Charts
        st.write("## 📊 Charts")
        
        # Parsing success chart
        parsing_data = {
            'Status': ['Successful', 'Failed'],
            'Count': [
                stats_data.get('successful_parses', 0),
                stats_data.get('failed_parses', 0)
            ]
        }
        fig = px.pie(parsing_data, values='Count', names='Status', 
                    title="Resume Parsing Success Rate",
                    color_discrete_sequence=['#667eea', '#764ba2'])
        st.plotly_chart(fig, use_container_width=True)
        
        # Top skills chart
        if stats_data.get('top_skills_found'):
            skills_df = pd.DataFrame(stats_data['top_skills_found'], columns=['Skill', 'Count'])
            fig = px.bar(skills_df.head(10), x='Count', y='Skill', 
                        title="Top 10 Skills Found",
                        color_discrete_sequence=['#667eea'])
            st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()