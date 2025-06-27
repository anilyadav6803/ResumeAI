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
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://github.com/anilyadav6803/ResumeAI',
        'Report a bug': "https://github.com/anilyadav6803/ResumeAI/issues",
        'About': "# ResumeAI\nAI-powered Resume Optimization and Matching System"
    }
)

# Modern CSS with improved aesthetics and usability
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    html, body, .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        color: #1a202c;
        min-height: 100vh;
        overflow-x: hidden;
    }
    
    /* Animated background particles */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Ccircle cx='9' cy='9' r='1'/%3E%3Ccircle cx='49' cy='49' r='1'/%3E%3Ccircle cx='29' cy='29' r='1'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        animation: float 20s infinite linear;
        pointer-events: none;
        z-index: -1;
    }
    
    @keyframes float {
        0% { transform: translateY(0px) rotate(0deg); }
        100% { transform: translateY(-100vh) rotate(360deg); }
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
        max-width: 1400px;
        margin: 0 auto;
        padding: 1rem;
        position: relative;
        z-index: 1;
    }
    
    /* Header styling with glassmorphism */
    .app-header {
        text-align: center;
        margin-bottom: 2rem;
        padding: 4rem 2rem;
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
        border-radius: 25px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1), 0 5px 15px rgba(0,0,0,0.08);
        position: relative;
        overflow: hidden;
        animation: slideInDown 0.8s ease-out;
    }
    
    @keyframes slideInDown {
        from {
            opacity: 0;
            transform: translateY(-50px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .app-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    .app-title {
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        text-shadow: 0 4px 8px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
        background: linear-gradient(45deg, #fff, #e2e8f0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .app-subtitle {
        font-size: 1.3rem;
        opacity: 0.95;
        max-width: 600px;
        margin: 0 auto;
        font-weight: 400;
        line-height: 1.6;
        position: relative;
        z-index: 1;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    /* Navigation buttons with hover effects */
    .nav-container {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin-bottom: 2rem;
        flex-wrap: wrap;
    }
    
    /* Enhanced card styling with glassmorphism */
    .card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 20px;
        padding: 2.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1), 0 2px 8px rgba(0,0,0,0.05);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        animation: fadeInUp 0.6s ease-out;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        opacity: 0.8;
    }
    
    .card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 40px rgba(0,0,0,0.15), 0 8px 16px rgba(0,0,0,0.1);
        border-color: rgba(102, 126, 234, 0.3);
    }
    
    .card-title {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1.2rem;
        color: #2d3748;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        position: relative;
    }
    
    .card-title::after {
        content: '';
        position: absolute;
        bottom: -8px;
        left: 0;
        width: 50px;
        height: 3px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 2px;
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
    
    /* Enhanced button styling with modern effects */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 1rem 2.5rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4), 0 2px 8px rgba(0,0,0,0.1) !important;
        text-transform: none !important;
        letter-spacing: 0.5px !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton>button::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: -100% !important;
        width: 100% !important;
        height: 100% !important;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent) !important;
        transition: left 0.5s !important;
    }
    
    .stButton>button:hover::before {
        left: 100% !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px) scale(1.05) !important;
        box-shadow: 0 12px 30px rgba(102, 126, 234, 0.6), 0 4px 12px rgba(0,0,0,0.15) !important;
        background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%) !important;
    }
    
    .stButton>button:active {
        transform: translateY(-1px) scale(1.02) !important;
        transition: all 0.1s !important;
    }
    
    .stButton>button:disabled {
        background: linear-gradient(135deg, #e2e8f0 0%, #cbd5e0 100%) !important;
        color: #a0aec0 !important;
        cursor: not-allowed !important;
        transform: none !important;
        box-shadow: none !important;
    }
    
    /* Navigation buttons special styling */
    .nav-button {
        background: rgba(255, 255, 255, 0.2) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 0.8rem 1.5rem !important;
        margin: 0.2rem !important;
        transition: all 0.3s ease !important;
        font-weight: 500 !important;
    }
    
    .nav-button:hover {
        background: rgba(255, 255, 255, 0.3) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(0,0,0,0.2) !important;
    }
    /* Enhanced form elements with modern styling */
    .stTextArea>div>div>textarea, 
    .stTextInput>div>div>input,
    .stSelectbox>div>div>div>input {
        border: 2px solid rgba(226, 232, 240, 0.8) !important;
        border-radius: 15px !important;
        padding: 1.2rem !important;
        font-size: 1rem !important;
        color: #2d3748 !important;
        background: rgba(255, 255, 255, 0.9) !important;
        backdrop-filter: blur(10px) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important;
    }
    
    .stTextArea>div>div>textarea:focus, 
    .stTextInput>div>div>input:focus,
    .stSelectbox>div>div>div>input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1), 0 4px 12px rgba(102, 126, 234, 0.15) !important;
        outline: none !important;
        background: white !important;
        transform: translateY(-2px) !important;
    }
    
    /* Enhanced file uploader */
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
    
    /* Enhanced metrics with glassmorphism */
    [data-testid="metric-container"] {
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 20px !important;
        padding: 2rem 1.5rem !important;
        background: rgba(255, 255, 255, 0.9) !important;
        backdrop-filter: blur(15px) !important;
        -webkit-backdrop-filter: blur(15px) !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1), 0 2px 8px rgba(0,0,0,0.05) !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    [data-testid="metric-container"]::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        height: 4px !important;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #f093fb 100%) !important;
    }
    
    [data-testid="metric-container"]:hover {
        transform: translateY(-5px) scale(1.02) !important;
        box-shadow: 0 15px 40px rgba(0,0,0,0.15), 0 5px 15px rgba(0,0,0,0.1) !important;
        border-color: rgba(102, 126, 234, 0.4) !important;
    }
    
    [data-testid="metric-container"] > div {
        color: #2d3748 !important;
    }
    
    [data-testid="metric-container"] [data-testid="metric-value"] {
        color: #667eea !important;
        font-weight: 800 !important;
        font-size: 2rem !important;
        text-shadow: 0 2px 4px rgba(102, 126, 234, 0.2) !important;
    }
    
    /* Enhanced progress bar */
    .stProgress>div>div>div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #f093fb 100%) !important;
        border-radius: 15px !important;
        height: 16px !important;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stProgress>div>div>div::after {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: -100% !important;
        width: 100% !important;
        height: 100% !important;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent) !important;
        animation: progressShine 2s infinite !important;
    }
    
    @keyframes progressShine {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    .stProgress>div>div {
        background: rgba(226, 232, 240, 0.3) !important;
        border-radius: 15px !important;
        height: 16px !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Enhanced tabs with modern styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: rgba(255,255,255,0.2);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        padding: 0.8rem;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 1rem 2rem !important;
        border-radius: 15px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        font-weight: 500 !important;
        color: #4a5568 !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stTabs [data-baseweb="tab"]::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: -100% !important;
        width: 100% !important;
        height: 100% !important;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.1), transparent) !important;
        transition: left 0.5s !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover::before {
        left: 100% !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
        transform: translateY(-2px) !important;
    }
    
    .stTabs [aria-selected="true"]::before {
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent) !important;
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
    
    /* Enhanced alert boxes with modern styling */
    .stAlert {
        border-radius: 15px !important;
        border: none !important;
        padding: 1.5rem 2rem !important;
        margin: 1.5rem 0 !important;
        backdrop-filter: blur(15px) !important;
        -webkit-backdrop-filter: blur(15px) !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stAlert::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        width: 4px !important;
        height: 100% !important;
    }
    
    .stSuccess {
        background: rgba(72, 187, 120, 0.15) !important;
        color: #2f855a !important;
        border: 1px solid rgba(72, 187, 120, 0.3) !important;
    }
    
    .stSuccess::before {
        background: #48bb78 !important;
    }
    
    .stWarning {
        background: rgba(237, 137, 54, 0.15) !important;
        color: #c05621 !important;
        border: 1px solid rgba(237, 137, 54, 0.3) !important;
    }
    
    .stWarning::before {
        background: #ed8936 !important;
    }
    
    .stError {
        background: rgba(245, 101, 101, 0.15) !important;
        color: #c53030 !important;
        border: 1px solid rgba(245, 101, 101, 0.3) !important;
    }
    
    .stError::before {
        background: #f56565 !important;
    }
    
    .stInfo {
        background: rgba(102, 126, 234, 0.15) !important;
        color: #553c9a !important;
        border: 1px solid rgba(102, 126, 234, 0.3) !important;
    }
    
    .stInfo::before {
        background: #667eea !important;
    }
    
    /* Enhanced expander styling */
    .streamlit-expanderHeader {
        background: rgba(255,255,255,0.9) !important;
        backdrop-filter: blur(15px) !important;
        border-radius: 15px !important;
        border: 1px solid rgba(226, 232, 240, 0.5) !important;
        color: #2d3748 !important;
        font-weight: 600 !important;
        padding: 1.2rem 1.5rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(102, 126, 234, 0.05) !important;
        border-color: rgba(102, 126, 234, 0.3) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
    }
    
    .streamlit-expanderContent {
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 0 0 15px 15px !important;
        border: 1px solid rgba(226, 232, 240, 0.5) !important;
        border-top: none !important;
        color: #1a202c !important;
        padding: 1.5rem !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important;
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
    
    /* Enhanced footer styling */
    .app-footer {
        text-align: center;
        padding: 4rem 2rem;
        margin-top: 4rem;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 25px 25px 0 0;
        color: white;
        box-shadow: 0 -8px 25px rgba(0,0,0,0.1);
        position: relative;
        overflow: hidden;
    }
    
    .app-footer::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.05), transparent);
        animation: footerShimmer 4s infinite;
    }
    
    @keyframes footerShimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    .footer-content {
        max-width: 1400px;
        margin: 0 auto;
        padding: 0 1rem;
        position: relative;
        z-index: 1;
    }
    
    .footer-links {
        display: flex;
        justify-content: center;
        gap: 2.5rem;
        margin-bottom: 2rem;
        flex-wrap: wrap;
    }
    
    .footer-links a {
        color: rgba(255, 255, 255, 0.9);
        text-decoration: none;
        font-weight: 500;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        padding: 0.8rem 1.5rem;
        border-radius: 12px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .footer-links a:hover {
        color: white;
        background: rgba(255, 255, 255, 0.15);
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 8px 20px rgba(0,0,0,0.2);
        border-color: rgba(255, 255, 255, 0.3);
    }
    
    .copyright {
        font-size: 0.95rem;
        opacity: 0.8;
        margin-top: 1.5rem;
        color: rgba(255, 255, 255, 0.8);
        text-shadow: 0 1px 2px rgba(0,0,0,0.2);
    }
    
    /* Loading spinner animation */
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(255,255,255,0.3);
        border-radius: 50%;
        border-top-color: #667eea;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Status indicators */
    .status-indicator {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 500;
        backdrop-filter: blur(10px);
        margin-bottom: 1rem;
    }
    
    .status-success {
        background: rgba(72, 187, 120, 0.2);
        color: #2f855a;
        border: 1px solid rgba(72, 187, 120, 0.3);
    }
    
    .status-warning {
        background: rgba(237, 137, 54, 0.2);
        color: #c05621;
        border: 1px solid rgba(237, 137, 54, 0.3);
    }
    
    .status-error {
        background: rgba(245, 101, 101, 0.2);
        color: #c53030;
        border: 1px solid rgba(245, 101, 101, 0.3);
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

# API Configuration - Auto-detect based on environment
import os
if os.getenv('ENVIRONMENT') == 'production':
    API_BASE_URL = "/api"  # Use nginx proxy in production
else:
    API_BASE_URL = "http://127.0.0.1:8000"  # Local development

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
                # Get candidate info from the new structure
                candidate_info = match.get('candidate_info', {})
                candidate_name = candidate_info.get('name', 'Not specified')
                candidate_email = candidate_info.get('email', 'Not specified')
                candidate_experience = candidate_info.get('experience_years', 'Not specified')
                
                # Fallback to old metadata structure if candidate_info is empty
                if not candidate_info or candidate_name == 'Not specified':
                    candidate_name = match['metadata'].get('name', 'Not specified')
                    candidate_email = match['metadata'].get('email', 'Not specified')
                    candidate_experience = match['metadata'].get('experience_years', 'Not specified')
                
                st.markdown(f"""
                <div style="color: #1a202c !important;">
                <strong>Name:</strong> {candidate_name}<br>
                <strong>Email:</strong> {candidate_email}<br>
                <strong>Experience:</strong> {candidate_experience}{' years' if str(candidate_experience).isdigit() else ''}
                </div>                """, unsafe_allow_html=True)
                
                # Skills
                skills = candidate_info.get('skills', match['metadata'].get('skills', 'Not specified'))
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
                <strong>Matched Keywords:</strong> {len(match.get('matched_keywords', []))} found
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
        if missing_keywords and len(missing_keywords) > 0:
            st.write(f"**Found {len(missing_keywords)} keywords to add to your resume:**")
            for keyword in missing_keywords:
                st.write(f"• **{keyword}**")
        else:
            st.info("No missing keywords identified. Your resume appears well-optimized for this job.")
    
    with tab2:
        strengths = results.get('strengths', [])
        if strengths and len(strengths) > 0:
            st.write(f"**Your resume already includes {len(strengths)} important keywords:**")
            for strength in strengths:
                st.write(f"✅ **{strength}**")
        else:
            st.info("Consider adding more relevant keywords from the job description to strengthen your resume.")
    
    with tab3:
        improvements = results.get('format_improvements', []) + results.get('content_suggestions', [])
        if improvements:
            st.write("**Suggested Improvements:**")
            for item in improvements:
                st.write(f"• {item}")
        else:
            st.info("No specific improvement suggestions available.")

def show_loading_animation(message="Processing..."):
    """Display a loading animation with message"""
    st.markdown(f"""
    <div style="text-align: center; padding: 2rem;">
        <div class="loading-spinner"></div>
        <p style="margin-top: 1rem; color: #667eea; font-weight: 500;">{message}</p>
    </div>
    """, unsafe_allow_html=True)

def show_success_message(title, message, icon="🎉"):
    """Display a success message with animation"""
    st.markdown(f"""
    <div class="card" style="border-left: 4px solid #48bb78; background: rgba(72, 187, 120, 0.05) !important;">
        <div style="text-align: center; padding: 1rem;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">{icon}</div>
            <h3 style="color: #2f855a; margin-bottom: 0.5rem;">{title}</h3>
            <p style="color: #4a5568; margin: 0;">{message}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_feature_highlight(title, features, icon="✨"):
    """Display a feature highlight box"""
    features_html = "".join([f"""
        <div style="display: flex; align-items: center; gap: 0.75rem; margin: 0.75rem 0; color: #4a5568;">
            <span style="color: #667eea; font-size: 1.1rem;">•</span>
            <span>{feature}</span>
        </div>
    """ for feature in features])
    
    st.markdown(f"""
    <div class="card" style="border-left: 4px solid #667eea;">
        <h3 style="color: #2d3748; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">
            <span>{icon}</span>
            <span>{title}</span>
        </h3>
        {features_html}
    </div>
    """, unsafe_allow_html=True)

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
            <h1 class="app-title">🤖 ResumeAI</h1>
            <p class="app-subtitle">AI-powered Resume Optimization and Matching System</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Check API connection
    health_data, health_error = call_api("/health/")
    if health_error:
        st.markdown("""
        <div class="status-indicator status-warning">
            <span>⚠️</span>
            <span>Backend API Connection Issue</span>
        </div>
        """, unsafe_allow_html=True)
        st.info("Some features may not work properly. Please make sure the backend server is running at http://127.0.0.1:8000")
    else:
        st.markdown("""
        <div class="status-indicator status-success">
            <span>✅</span>
            <span>Backend API Connected</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Enhanced Navigation with icons and improved styling
    st.markdown('<div class="nav-container">', unsafe_allow_html=True)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button("🏠 Home", use_container_width=True, key="nav_home"):
            st.session_state.current_page = "Home"
            st.rerun()
    with col2:
        if st.button("📋 Screening", use_container_width=True, key="nav_screening"):
            st.session_state.current_page = "Resume Screening"
            st.rerun()
    with col3:
        if st.button("✨ Optimization", use_container_width=True, key="nav_optimization"):
            st.session_state.current_page = "ATS Optimization"
            st.rerun()
    with col4:
        if st.button("📂 Results", use_container_width=True, key="nav_results"):
            st.session_state.current_page = "Saved Results"
            st.rerun()
    with col5:
        if st.button("📊 Analytics", use_container_width=True, key="nav_stats"):
            st.session_state.current_page = "Statistics"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Main content based on current page
    if st.session_state.current_page == "Home":
        show_home_page()
    elif st.session_state.current_page == "Resume Screening":
        show_resume_screening()
    elif st.session_state.current_page == "ATS Optimization":
        show_ats_optimization()
    elif st.session_state.current_page == "Saved Results":
        show_saved_results_page()
    elif st.session_state.current_page == "Statistics":
        show_statistics()
    
    # Enhanced Footer with modern design
    st.markdown("""
    <div class="app-footer">
        <div class="footer-content">
            <div class="footer-links">
                <a href="mailto:support@resumeai.com">📧 Contact</a>
                <a href="https://github.com/anilyadav6803/ResumeAI">📖 Documentation</a>
                <a href="https://github.com/anilyadav6803/ResumeAI">� GitHub</a>
                <a href="#">� Privacy</a>
                <a href="#">❓ Help</a>
            </div>
            <div class="copyright">
                © 2025 ResumeAI - Powered by AI • Made with ❤️ using Streamlit & FastAPI
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_home_page():
    st.markdown("""
    <div class="main-container">
        <div class="card">
            <h2 class="card-title">🚀 Welcome to ResumeAI</h2>
            <p>ResumeAI leverages cutting-edge AI technology to help recruiters find the perfect candidates and empower job seekers to optimize their resumes for maximum ATS compatibility. Experience the future of recruitment and career advancement.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced feature cards with more visual appeal
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("""
        <div class="card">
            <h2 class="card-title">📋 Resume Screening</h2>
            <p>Upload multiple resumes and match them against job descriptions using advanced AI algorithms to find the most qualified candidates.</p>
            <div style="margin: 1.5rem 0;">
                <div style="display: flex; align-items: center; gap: 0.75rem; margin: 0.5rem 0; color: #4a5568;">
                    <span style="color: #667eea;">🤖</span>
                    <span>AI-powered semantic matching</span>
                </div>
                <div style="display: flex; align-items: center; gap: 0.75rem; margin: 0.5rem 0; color: #4a5568;">
                    <span style="color: #667eea;">🏆</span>
                    <span>Intelligent candidate ranking</span>
                </div>
                <div style="display: flex; align-items: center; gap: 0.75rem; margin: 0.5rem 0; color: #4a5568;">
                    <span style="color: #667eea;">🛠️</span>
                    <span>Skills and experience extraction</span>
                </div>
                <div style="display: flex; align-items: center; gap: 0.75rem; margin: 0.5rem 0; color: #4a5568;">
                    <span style="color: #667eea;">⚡</span>
                    <span>Batch processing up to 20 resumes</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔍 Try Resume Screening", key="home_screening", use_container_width=True):
            st.session_state.current_page = "Resume Screening"
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="card">
            <h2 class="card-title">✨ ATS Optimization</h2>
            <p>Get your resume optimized to pass through Applicant Tracking Systems and significantly increase your chances of landing interviews.</p>
            <div style="margin: 1.5rem 0;">
                <div style="display: flex; align-items: center; gap: 0.75rem; margin: 0.5rem 0; color: #4a5568;">
                    <span style="color: #667eea;">📊</span>
                    <span>ATS compatibility score (0-100)</span>
                </div>
                <div style="display: flex; align-items: center; gap: 0.75rem; margin: 0.5rem 0; color: #4a5568;">
                    <span style="color: #667eea;">🔑</span>
                    <span>Missing keywords identification</span>
                </div>
                <div style="display: flex; align-items: center; gap: 0.75rem; margin: 0.5rem 0; color: #4a5568;">
                    <span style="color: #667eea;">💡</span>
                    <span>Format improvement suggestions</span>
                </div>
                <div style="display: flex; align-items: center; gap: 0.75rem; margin: 0.5rem 0; color: #4a5568;">
                    <span style="color: #667eea;">📈</span>
                    <span>Content enhancement recommendations</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("⚡ Optimize Your Resume", key="home_optimization", use_container_width=True):
            st.session_state.current_page = "ATS Optimization"
            st.rerun()
    
    # Add a statistics preview section
    st.markdown("""
    <div class="card">
        <h2 class="card-title">📊 Quick Stats Overview</h2>
        <p>See how ResumeAI is helping users worldwide achieve their career goals.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick stats
    stats_data, _ = call_api("/stats/")
    if stats_data and 'total_resumes' in stats_data:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📄 Resumes Processed", stats_data.get('total_resumes', 0))
        with col2:
            st.metric("✅ Successful Parses", stats_data.get('successful_parses', 0))
        with col3:
            success_rate = stats_data.get('success_rate', 0)
            st.metric("📈 Success Rate", f"{success_rate:.1f}%")
        with col4:
            st.metric("🏆 Top Skill", stats_data.get('most_common_skill', 'Python')[:10] + "...")
    else:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📄 Resumes Processed", "1,000+")
        with col2:
            st.metric("✅ Success Rate", "94.7%")
        with col3:
            st.metric("🏆 Happy Users", "250+")
        with col4:
            st.metric("⚡ Avg Processing Time", "< 30s")

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
            show_loading_animation("Analyzing resumes with AI...")
            
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
            show_success_message(
                "Analysis Complete!", 
                f"Successfully analyzed {len(uploaded_files)} resumes and found {len(matches)} qualified candidates.",
                "🎯"
            )
            
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
            # Prepare file and form data for API
            files = [("file", (resume_file.name, resume_file.getvalue(), resume_file.type))]
            data = {
                "job_description": job_description
            }
            
            # Call API
            response, error = call_api(
                "/optimize-resume/",
                method="POST",
                data=data,
                files=files
            )
            
            if error:
                st.error(f"Error during optimization: {error}")
                return
            
            # Display results
            st.success("✅ Optimization completed successfully!")
            
            # Extract optimization results from the response
            optimization_results = response.get('optimization_results', {})
            if not optimization_results:
                st.error("No optimization results found in response")
                st.json(response)  # Debug: show full response
                return
                
            # Show result ID and saved status
            if response.get('result_id'):
                st.success(f"✅ Results saved with ID: `{response['result_id']}`")
                
                # Option to view saved results
                if st.button("📋 View My Saved Results"):
                    show_saved_ats_results(response.get('resume_info', {}).get('email', ''))
            
            display_optimization_results(optimization_results)
            
            # Download optimized resume if available
            if 'optimized_resume_url' in response:
                st.markdown("### 📥 Download Optimized Resume")
                st.markdown(
                    f"Your optimized resume is ready! [Download here]({API_BASE_URL}{response['optimized_resume_url']})",
                    unsafe_allow_html=True
                )

def show_saved_ats_results(email: str = None):
    """Show saved ATS optimization results"""
    st.markdown("### 📂 Saved ATS Optimization Results")
    
    if email:
        # Get user-specific results
        results_data, error = call_api(f"/ats-results/user/{email}")
    else:
        # Get recent results
        results_data, error = call_api("/ats-results/")
    
    if error:
        st.error(f"Error loading saved results: {error}")
        return
    
    if not results_data or not results_data.get('results'):
        st.info("No saved ATS optimization results found.")
        return
    
    results = results_data['results']
    st.write(f"Found {len(results)} saved optimization result(s)")
    
    # Display results in expandable sections
    for i, result in enumerate(results):
        timestamp = result.get('timestamp', '').split('T')[0]  # Get date only
        resume_name = result.get('resume_info', {}).get('name', 'Unknown')
        ats_score = result.get('optimization_results', {}).get('ats_score', 'N/A')
        
        with st.expander(f"📄 {resume_name} - ATS Score: {ats_score} (Saved: {timestamp})"):
            # Display resume info
            resume_info = result.get('resume_info', {})
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Resume Information:**")
                st.write(f"• **Name:** {resume_info.get('name', 'N/A')}")
                st.write(f"• **Email:** {resume_info.get('email', 'N/A')}")
                st.write(f"• **Word Count:** {resume_info.get('word_count', 'N/A')}")
                st.write(f"• **Skills Found:** {resume_info.get('skills_count', 'N/A')}")
            
            with col2:
                st.markdown("**Optimization Details:**")
                optimization = result.get('optimization_results', {})
                st.write(f"• **ATS Score:** {optimization.get('ats_score', 'N/A')}/100")
                st.write(f"• **Missing Keywords:** {len(optimization.get('missing_keywords', []))}")
                st.write(f"• **Match %:** {optimization.get('match_percentage', 'N/A')}%")
            
            # Job description snippet
            job_desc = result.get('job_description', '')
            if job_desc:
                st.markdown("**Job Description (snippet):**")
                st.text(job_desc[:200] + "..." if len(job_desc) > 200 else job_desc)
            
            # Show optimization details
            if st.button(f"🔍 View Full Optimization Details", key=f"details_{i}"):
                display_optimization_results(optimization)

def show_saved_screening_results(limit: int = 10):
    """Show saved resume screening results"""
    st.markdown("### 🔍 Saved Resume Screening Results")
    
    # Get recent screening results
    results_data, error = call_api(f"/screening-results/?limit={limit}")
    
    if error:
        st.error(f"Error loading saved screening results: {error}")
        return
    
    if not results_data or not results_data.get('results'):
        st.info("No saved resume screening results found.")
        return
    
    results = results_data['results']
    st.write(f"Found {len(results)} saved screening result(s)")
    
    # Display results in expandable sections
    for i, result in enumerate(results):
        timestamp = result.get('timestamp', '').split('T')[0]  # Get date only
        total_candidates = result.get('total_candidates', 0)
        actual_matches = result.get('actual_matches', 0)
        
        with st.expander(f"📋 Screening {i+1} - {actual_matches}/{total_candidates} matches (Saved: {timestamp})"):
            # Display screening info
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Screening Information:**")
                st.write(f"• **Total Candidates:** {total_candidates}")
                st.write(f"• **Matches Found:** {actual_matches}")
                st.write(f"• **Requested Matches:** {result.get('requested_matches', 'N/A')}")
                st.write(f"• **Timestamp:** {result.get('timestamp', 'N/A')}")
            
            with col2:
                st.markdown("**Job Description (snippet):**")
                job_desc = result.get('job_description', '')
                st.text(job_desc[:150] + "..." if len(job_desc) > 150 else job_desc)
            
            # Show matching candidates
            matches = result.get('matches', [])
            if matches:
                st.markdown("**🏆 Top Matching Candidates:**")
                
                # Create a DataFrame for better display
                candidates_data = []
                for match in matches:
                    candidates_data.append({
                        "Name": match.get('candidate_name', 'Unknown'),
                        "Email": match.get('candidate_email', 'N/A'),
                        "Score": f"{match.get('score', 0):.1f}",
                        "Similarity": f"{match.get('similarity_score', 0):.1f}",
                        "Keyword Match": f"{match.get('keyword_match_ratio', 0):.1f}%",
                        "Experience": f"{match.get('experience_years', 0)} years"
                    })
                
                if candidates_data:
                    candidates_df = pd.DataFrame(candidates_data)
                    st.dataframe(candidates_df, use_container_width=True)
                
                # Show matched keywords for top candidate
                if matches and matches[0].get('matched_keywords'):
                    st.markdown("**🔑 Top Keywords (Top Candidate):**")
                    keywords = matches[0]['matched_keywords'][:10]  # Show top 10
                    st.write(", ".join(keywords))

# ...existing code...
def show_saved_results_page():
    """Show saved results page with tabs for ATS and Screening results"""
    st.markdown("""
    <div class="main-container">
        <div class="card">
            <h2 class="card-title">📂 Saved Results</h2>
            <p>View and manage your previously saved ATS optimization and resume screening results.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Create tabs for different types of results
    tab1, tab2 = st.tabs(["✨ ATS Optimization Results", "🔍 Resume Screening Results"])
    
    with tab1:
        # Show ATS results directly
        show_saved_ats_results()
    
    with tab2:
        # Show screening results directly
        show_saved_screening_results()

def show_candidate_screening_history(email: str):
    """Show screening history for a specific candidate"""
    st.markdown(f"### 👤 Screening History for: {email}")
    
    # Get candidate screening history
    history_data, error = call_api(f"/screening-results/candidate/{email}")
    
    if error:
        st.error(f"Error loading candidate history: {error}")
        return
    
    if not history_data or not history_data.get('history'):
        st.info(f"No screening history found for {email}")
        return
    
    history = history_data['history']
    st.write(f"Found {len(history)} screening record(s) for this candidate")
    
    # Display history in chronological order (newest first)
    for i, record in enumerate(history):
        timestamp = record.get('timestamp', '').split('T')[0]  # Get date only
        score = record.get('score', 0)
        similarity = record.get('similarity_score', 0)
        
        with st.expander(f"📅 Screening {i+1} - Score: {score:.1f} (Date: {timestamp})"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Performance Metrics:**")
                st.write(f"• **Overall Score:** {score:.1f}")
                st.write(f"• **Similarity Score:** {similarity:.1f}")
                st.write(f"• **Keyword Match:** {record.get('keyword_match_ratio', 0):.1f}%")
                st.write(f"• **Date:** {timestamp}")
            
            with col2:
                # Show matched keywords
                keywords = record.get('matched_keywords', [])
                if keywords:
                    st.markdown("**🔑 Matched Keywords:**")
                    st.write(", ".join(keywords[:10]))  # Show top 10
                
                # Job description snippet
                job_desc = record.get('job_description', '')
                if job_desc:
                    st.markdown("**Job Description (snippet):**")
                    st.text(job_desc[:100] + "..." if len(job_desc) > 100 else job_desc)
    
    # Show performance trend if multiple records
    if len(history) > 1:
        st.markdown("### 📈 Performance Trend")
        
        # Create DataFrame for plotting
        trend_data = []
        for record in reversed(history):  # Reverse to show chronological order
            trend_data.append({
                "Date": record.get('timestamp', '').split('T')[0],
                "Score": record.get('score', 0),
                "Similarity": record.get('similarity_score', 0),
                "Keyword Match %": record.get('keyword_match_ratio', 0)
            })
        
        if trend_data:
            trend_df = pd.DataFrame(trend_data)
            
            # Plot performance over time
            fig = px.line(trend_df, x="Date", y=["Score", "Similarity", "Keyword Match %"], 
                         title=f"Performance Trend for {email}")
            st.plotly_chart(fig, use_container_width=True)

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
        st.info("No statistics available yet. Upload and process some resumes first!")
        return
    
    # Display main statistics
    st.markdown("### 📈 Overall Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Resumes", stats_data.get('total_resumes', 0))
    with col2:
        st.metric("Successful Parses", stats_data.get('successful_parses', 0))
    with col3:
        st.metric("Failed Parses", stats_data.get('failed_parses', 0))
    with col4:
        success_rate = stats_data.get('success_rate', 0)
        st.metric("Success Rate", f"{success_rate:.1f}%")
    
    # Get ATS and Screening statistics
    ats_stats_data, ats_error = call_api("/ats-statistics/")
    screening_stats_data, screening_error = call_api("/screening-statistics/")
    
    # Display detailed statistics in tabs
    tab1, tab2, tab3 = st.tabs(["📊 Resume Analysis", "✨ ATS Optimization", "🔍 Screening Results"])
    
    with tab1:
        st.markdown("### 📊 Resume Processing Analysis")
        
        if stats_data.get('top_skills'):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🔧 Top Skills Found")
                skills_data = stats_data['top_skills'][:10]  # Top 10 skills
                if skills_data:
                    skills_df = pd.DataFrame(skills_data)
                    fig = px.bar(skills_df, x='count', y='name', orientation='h',
                               title="Most Common Skills in Resumes")
                    fig.update_layout(yaxis={'categoryorder':'total ascending'})
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No skills data available yet")
            
            with col2:
                st.markdown("#### 📈 Resume Quality Metrics")
                
                # Additional metrics
                col2a, col2b = st.columns(2)
                with col2a:
                    st.metric("Avg Word Count", stats_data.get('average_word_count', 0))
                    st.metric("Resumes with Email", stats_data.get('resumes_with_email', 0))
                with col2b:
                    st.metric("Resumes with Phone", stats_data.get('resumes_with_phone', 0))
                    st.metric("Most Common Skill", stats_data.get('most_common_skill', 'N/A'))
                
                # Match score distribution if available
                if stats_data.get('match_score_distribution'):
                    st.markdown("#### 🎯 Score Distribution")
                    scores = stats_data['match_score_distribution']
                    score_df = pd.DataFrame({'Scores': scores})
                    fig = px.histogram(score_df, x='Scores', nbins=10, title="Resume Match Score Distribution")
                    st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Process some resumes to see detailed analysis")
    
    with tab2:
        st.markdown("### ✨ ATS Optimization Statistics")
        
        if not ats_error and ats_stats_data and ats_stats_data.get('statistics'):
            ats_stats = ats_stats_data['statistics']
            
            # ATS metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Optimizations", ats_stats.get('total_optimizations', 0))
            with col2:
                st.metric("Average ATS Score", f"{ats_stats.get('average_ats_score', 0):.1f}%")
            with col3:
                st.metric("Recent Activity", ats_stats.get('recent_activity', 0))
            with col4:
                st.metric("Total Users", ats_stats.get('total_users', 0))
            
            # Common issues
            if ats_stats.get('common_issues'):
                st.markdown("#### � Most Common ATS Issues")
                issues_df = pd.DataFrame(ats_stats['common_issues'])
                if not issues_df.empty:
                    st.dataframe(issues_df, use_container_width=True)
            
            # Optimization trends
            if stats_data.get('optimization_trends'):
                st.markdown("#### 📈 ATS Score Trends")
                trends = stats_data['optimization_trends']
                trends_df = pd.DataFrame(trends)
                if not trends_df.empty:
                    fig = px.line(trends_df, x='date', y='score', 
                                title="ATS Optimization Score Trends Over Time")
                    st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Run some ATS optimizations to see trends and statistics")
    
    with tab3:
        st.markdown("### 🔍 Resume Screening Statistics")
        
        if not screening_error and screening_stats_data and screening_stats_data.get('statistics'):
            screening_stats = screening_stats_data['statistics']
            
            # Screening metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Screenings", screening_stats.get('total_screenings', 0))
            with col2:
                st.metric("Candidates Screened", screening_stats.get('total_candidates_screened', 0))
            with col3:
                st.metric("Avg Matches/Screening", screening_stats.get('average_matches_per_screening', 0))
            with col4:
                st.metric("Recent Activity", screening_stats.get('recent_activity', 0))
            
            # Top candidates
            if screening_stats.get('top_candidates'):
                st.markdown("#### 🏆 Top Performing Candidates")
                candidates_df = pd.DataFrame(screening_stats['top_candidates'][:10])
                if not candidates_df.empty:
                    fig = px.bar(candidates_df, x='average_score', y='name', orientation='h',
                               title="Top Candidates by Average Score")
                    fig.update_layout(yaxis={'categoryorder':'total ascending'})
                    st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Run some resume screenings to see candidate performance statistics")

if __name__ == "__main__":
    main()