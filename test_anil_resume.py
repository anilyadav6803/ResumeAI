import requests
import json

# Test with Anil Yadav's resume
BASE_URL = "http://localhost:8000"
UPLOAD_URL = f"{BASE_URL}/upload-resumes/"
MATCH_URL = f"{BASE_URL}/match-resumes/"

def test_anil_resume():
    print("🔄 Testing Anil Yadav's resume...")
    
    # Upload Anil's resume
    with open('anil_yadav_resume.txt', 'rb') as f:
        files = {'files': ('anil_yadav_resume.txt', f, 'text/plain')}
        response = requests.post(UPLOAD_URL, files=files)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Upload successful: {result['message']}")
        print(f"   Skills found: {result['processed_resumes'][0]['skills_count']}")
        print(f"   Word count: {result['processed_resumes'][0]['word_count']}")
    else:
        print(f"❌ Upload failed: {response.status_code} - {response.text}")
        return
    
    # Test with Software Developer job description
    job_description = """
    Senior Software Developer - Remote Position
    
    We are seeking a talented Senior Software Developer to join our dynamic team. The ideal candidate will have strong experience in full-stack development and modern technologies.
    
    Required Skills:
    • 5+ years of software development experience
    • Proficiency in Python and JavaScript
    • Experience with React.js and Node.js
    • Knowledge of Django or Flask frameworks
    • Experience with PostgreSQL and MongoDB databases
    • Familiarity with AWS cloud services
    • Experience with Docker and containerization
    • Knowledge of machine learning and AI technologies
    • Experience with Agile/Scrum methodologies
    • Strong problem-solving and debugging skills
    
    Preferred Skills:
    • Experience with TensorFlow or PyTorch
    • Knowledge of microservices architecture
    • Experience with CI/CD pipelines
    • AWS certifications
    • Experience mentoring junior developers
    
    What We Offer:
    • Competitive salary and benefits
    • Remote work flexibility
    • Professional development opportunities
    • Modern tech stack and tools
    """
    
    # Test matching
    data = {
        'job_description': job_description,
        'top_k': 5
    }
    
    response = requests.post(MATCH_URL, data=data)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Matching successful!")
        print(f"   Total candidates: {result.get('total_candidates_in_db', 0)}")
        print(f"   Total matches: {result.get('total_matches', 0)}")
        
        if 'matches' in result:
            for i, match in enumerate(result['matches'], 1):
                print(f"   {i}. {match.get('file_name', 'Unknown')}")
                print(f"      - Match Score: {match.get('score', 0):.3f}")
                print(f"      - Similarity Score: {match.get('similarity_score', 0):.3f}")
                print(f"      - Keyword Match Ratio: {match.get('keyword_match_ratio', 0):.3f}")
                print(f"      - Matched Keywords: {match.get('matched_keywords', [])[:5]}...")
                print()
    else:
        print(f"❌ Matching failed: {response.status_code} - {response.text}")

if __name__ == "__main__":
    test_anil_resume()
