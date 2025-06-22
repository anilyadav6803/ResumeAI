import streamlit as st

def show_home_page_modern():
    """Show the modern, beautiful home page"""
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <div class="hero-badge">🤖 Powered by Advanced AI</div>
        <h1 class="hero-title">ResumeAI</h1>
        <p class="hero-subtitle">
            Transform your hiring process with intelligent resume analysis and optimization. 
            Our AI-powered platform screens, analyzes, and matches candidates with 
            unprecedented accuracy and speed.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats Section
    st.markdown("""
    <div class="stats-container">
        <div class="stat-item">
            <span class="stat-number">95%</span>
            <span class="stat-label">Accuracy Rate</span>
        </div>
        <div class="stat-item">
            <span class="stat-number">10x</span>
            <span class="stat-label">Faster Screening</span>
        </div>
        <div class="stat-item">
            <span class="stat-number">50K+</span>
            <span class="stat-label">Resumes Analyzed</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature Cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📋</div>
            <h3 class="feature-title">Smart Resume Screening</h3>
            <p class="feature-description">
                Upload multiple resumes and find the perfect candidates using AI-powered semantic matching
            </p>
            <ul class="feature-list">
                <li>Process up to 20 resumes simultaneously</li>
                <li>AI-powered candidate ranking</li>
                <li>Comprehensive skills extraction</li>
                <li>Detailed match explanations</li>
                <li>Export results in multiple formats</li>
            </ul>
        </div>        """, unsafe_allow_html=True)
        
        st.info("⬆️ Use the navigation bar above to access Resume Screening!")
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">✨</div>
            <h3 class="feature-title">ATS Optimization</h3>
            <p class="feature-description">
                Optimize resumes for Applicant Tracking Systems with detailed AI recommendations
            </p>
            <ul class="feature-list">
                <li>ATS compatibility score (0-100)</li>
                <li>Missing keywords identification</li>
                <li>Format improvement suggestions</li>
                <li>Content enhancement advice</li>
                <li>Specific action items</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.info("⬆️ Use the navigation bar above to access ATS Optimization!")
    
    # How It Works Section
    st.markdown("---")
    st.markdown("## 🚀 How It Works")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="process-step">
            <span class="step-number">1</span>
            <div class="step-title">Upload & Process</div>
            <p>Upload your resumes or job descriptions. Our AI instantly processes and analyzes the content.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="process-step">
            <span class="step-number">3</span>
            <div class="step-title">Get Results</div>
            <p>Receive detailed analysis with scores, recommendations, and actionable insights.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="process-step">
            <span class="step-number">2</span>
            <div class="step-title">AI Analysis</div>
            <p>Advanced algorithms analyze skills, experience, and compatibility with job requirements.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="process-step">
            <span class="step-number">4</span>
            <div class="step-title">Take Action</div>
            <p>Implement recommendations to improve hiring decisions or resume performance.</p>
        </div>
        """, unsafe_allow_html=True)
