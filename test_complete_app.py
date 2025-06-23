#!/usr/bin/env python3
"""
Comprehensive test script for ResumeAI application
Tests PDF parsing, resume screening, and ATS optimization
"""
import requests
import json
import os
from pathlib import Path
import time

# API endpoints
BASE_URL = "http://localhost:8000"
UPLOAD_URL = f"{BASE_URL}/upload-resumes/"
MATCH_URL = f"{BASE_URL}/match-resumes/"
OPTIMIZE_URL = f"{BASE_URL}/optimize-resume/"

def test_api_health():
    """Test if API is responding"""
    try:
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            print("✅ API is healthy")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"❌ API health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API health check failed: {e}")
        return False

def create_test_files():
    """Create test resume files"""
    # Create test directory
    test_dir = Path("test_data")
    test_dir.mkdir(exist_ok=True)
    
    # Create test text resume 1
    resume1_content = """
John Doe
Software Engineer
Email: john.doe@email.com
Phone: (555) 123-4567

SUMMARY
Experienced software engineer with 5+ years in Python development, machine learning, and web applications.

EXPERIENCE
Senior Software Engineer - Tech Corp (2020-2024)
• Developed Python applications using Django and Flask
• Implemented machine learning models with TensorFlow and PyTorch
• Built REST APIs and microservices
• Collaborated with cross-functional teams in Agile environment

Software Engineer - StartupXYZ (2018-2020)
• Created web applications using React and Node.js
• Worked with SQL databases and MongoDB
• Implemented CI/CD pipelines with Jenkins
• Experience with AWS cloud services

EDUCATION
Bachelor of Science in Computer Science
University of Technology (2014-2018)

SKILLS
• Programming: Python, JavaScript, Java, C++
• Frameworks: Django, Flask, React, Node.js
• Databases: PostgreSQL, MongoDB, MySQL
• Cloud: AWS, Docker, Kubernetes
• Tools: Git, Jenkins, Jira
• Machine Learning: TensorFlow, PyTorch, Scikit-learn
"""
    
    # Create test text resume 2
    resume2_content = """
Jane Smith
Data Scientist
Email: jane.smith@email.com
Phone: (555) 987-6543

SUMMARY
Data scientist with 4+ years experience in machine learning, data analysis, and statistical modeling.

EXPERIENCE
Data Scientist - DataCorp (2021-2024)
• Developed predictive models using Python and R
• Performed statistical analysis and data visualization
• Worked with big data technologies like Spark and Hadoop
• Created dashboards using Tableau and PowerBI

Junior Data Analyst - Analytics Inc (2019-2021)
• Analyzed large datasets using SQL and Python
• Created reports and visualizations
• Collaborated with business stakeholders
• Experience with Excel and statistical software

EDUCATION
Master of Science in Data Science
Data University (2017-2019)

Bachelor of Science in Statistics
Math College (2013-2017)

SKILLS
• Programming: Python, R, SQL
• Machine Learning: Scikit-learn, XGBoost, Random Forest
• Visualization: Tableau, PowerBI, Matplotlib, Seaborn
• Databases: SQL Server, PostgreSQL, MongoDB
• Big Data: Spark, Hadoop, Elasticsearch
• Statistics: Regression, Classification, Time Series
"""
    
    # Save resume files
    resume1_path = test_dir / "john_doe_resume.txt"
    resume2_path = test_dir / "jane_smith_resume.txt"
    
    with open(resume1_path, 'w', encoding='utf-8') as f:
        f.write(resume1_content)
    
    with open(resume2_path, 'w', encoding='utf-8') as f:
        f.write(resume2_content)
    
    print(f"✅ Created test resume files:")
    print(f"   - {resume1_path}")
    print(f"   - {resume2_path}")
    
    return [resume1_path, resume2_path]

def test_upload_resumes(resume_files):
    """Test resume upload functionality"""
    print("\n🔄 Testing resume upload...")
    
    try:
        files = []
        for resume_file in resume_files:
            files.append(('files', (resume_file.name, open(resume_file, 'rb'), 'text/plain')))
        
        response = requests.post(UPLOAD_URL, files=files)
        
        # Close file handles
        for _, (_, file_handle, _) in files:
            file_handle.close()
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Upload successful: {result}")
            return True
        else:
            print(f"❌ Upload failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Upload error: {e}")
        return False

def test_resume_matching():
    """Test resume matching functionality"""
    print("\n🔄 Testing resume matching...")
    
    job_description = """
We are looking for a Senior Python Developer with the following requirements:

• 3+ years of experience in Python development
• Experience with Django or Flask frameworks
• Knowledge of machine learning libraries (TensorFlow, PyTorch)
• Experience with REST API development
• Familiarity with cloud platforms (AWS preferred)
• Strong understanding of databases (SQL and NoSQL)
• Experience with Agile development methodologies
• Knowledge of CI/CD pipelines
• Bachelor's degree in Computer Science or related field

Nice to have:
• Experience with React.js
• Docker and Kubernetes knowledge
• Experience with data science libraries
"""
    
    try:
        data = {
            'job_description': job_description,
            'top_k': 3
        }
        
        response = requests.post(MATCH_URL, data=data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Matching successful:")
            print(f"   - Total candidates: {result.get('total_candidates_in_db', 0)}")
            print(f"   - Total matches: {result.get('total_matches', 0)}")
            
            if 'matches' in result:
                for i, match in enumerate(result['matches'], 1):
                    print(f"   {i}. {match.get('file_name', 'Unknown')} - Score: {match.get('score', 0):.3f}")
            
            return True
        else:
            print(f"❌ Matching failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Matching error: {e}")
        return False

def test_ats_optimization(resume_files):
    """Test ATS optimization functionality"""
    print("\n🔄 Testing ATS optimization...")
    
    if not resume_files:
        print("❌ No resume files available for ATS testing")
        return False
    
    job_description = """
Senior Python Developer Position

Requirements:
• 5+ years Python development experience
• Django/Flask framework expertise
• Machine learning experience with TensorFlow/PyTorch
• AWS cloud platform experience
• RESTful API development
• Database management (PostgreSQL, MongoDB)
• Agile/Scrum methodology experience
• CI/CD pipeline implementation
"""
    
    try:
        resume_file = resume_files[0]  # Use first resume for testing
        
        with open(resume_file, 'rb') as f:
            files = {'file': (resume_file.name, f, 'text/plain')}
            data = {'job_description': job_description}
            
            response = requests.post(OPTIMIZE_URL, files=files, data=data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ ATS optimization successful:")
            print(f"   - Original score: {result.get('original_score', 'N/A')}")
            print(f"   - Optimized score: {result.get('optimized_score', 'N/A')}")
            if 'suggestions' in result:
                print(f"   - Suggestions provided: {len(result['suggestions'])}")
            return True
        else:
            print(f"❌ ATS optimization failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ ATS optimization error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting comprehensive ResumeAI tests...")
    
    # Test API health
    if not test_api_health():
        print("❌ API is not responding. Make sure the backend is running.")
        return
    
    # Create test files
    resume_files = create_test_files()
    
    # Test upload
    if not test_upload_resumes(resume_files):
        print("❌ Upload test failed. Cannot proceed with other tests.")
        return
    
    # Wait a moment for processing
    print("\n⏳ Waiting for resume processing...")
    time.sleep(2)
    
    # Test matching
    if not test_resume_matching():
        print("❌ Matching test failed.")
    
    # Test ATS optimization
    if not test_ats_optimization(resume_files):
        print("❌ ATS optimization test failed.")
    
    print("\n🎉 All tests completed!")
    
    # Cleanup
    print("\n🧹 Cleaning up test files...")
    for resume_file in resume_files:
        try:
            os.remove(resume_file)
            print(f"   Removed: {resume_file}")
        except Exception as e:
            print(f"   Error removing {resume_file}: {e}")

if __name__ == "__main__":
    main()
