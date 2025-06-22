from typing import Dict, List
import json
import re
from backend.models.embeddings import EmbeddingManager
import groq
import os

class JobMatcher:
    def __init__(self):
        """Initialize job matcher with AI client and embedding manager"""
        self.groq_client = None
        self.embedding_manager = EmbeddingManager()
        self._initialize_ai_client()
        
    def _initialize_ai_client(self):
        """Initialize Groq AI client"""
        try:
            groq_api_key = os.getenv("GROQ_API_KEY")
            if groq_api_key:
                self.groq_client = groq.Groq(api_key=groq_api_key)
                print("Initialized Groq AI client")
            else:
                print("Warning: GROQ_API_KEY not found. AI features will be limited.")
        except Exception as e:
            print(f"Error initializing Groq client: {e}")
    
    def create_resume_index(self, resumes: List[Dict]):
        """Create searchable index of resumes"""
        try:
            self.embedding_manager.add_resume_embeddings(resumes)
            return True
        except Exception as e:
            print(f"Error creating resume index: {e}")
            return False
    
    def match_resumes_to_job(self, job_description: str, top_k: int = 3) -> Dict:
        """Find top matching resumes for job description"""
        try:
            # Search similar resumes using embeddings
            matches = self.embedding_manager.search_similar_resumes(job_description, top_k)
            
            if not matches:
                return {
                    'matches': [],
                    'reasoning': 'No matching resumes found in the database.',
                    'job_requirements': self._extract_job_requirements(job_description)
                }
            
            # Generate AI reasoning for matches
            reasoning = self._generate_matching_reasoning(job_description, matches)
            
            # Extract job requirements
            job_requirements = self._extract_job_requirements(job_description)
            
            # Format matches for response
            formatted_matches = []
            for file_name, match_data in matches:
                formatted_matches.append({
                    'file_name': file_name,
                    'score': round(match_data['best_score'], 4),
                    'avg_score': round(match_data['avg_score'], 4),
                    'match_count': match_data['match_count'],
                    'metadata': match_data['metadata'],
                    'best_match_text': match_data['best_match_text'][:200] + "..." if len(match_data['best_match_text']) > 200 else match_data['best_match_text']
                })
            
            return {
                'matches': formatted_matches,
                'reasoning': reasoning,
                'job_requirements': job_requirements,
                'total_candidates': len(matches)
            }
            
        except Exception as e:
            print(f"Error matching resumes to job: {e}")
            return {
                'matches': [],
                'reasoning': f'Error occurred during matching: {str(e)}',
                'job_requirements': {}
            }
    
    def _generate_matching_reasoning(self, job_description: str, matches: List) -> str:
        """Generate AI reasoning for why resumes match the job"""
        if not self.groq_client:
            return self._generate_basic_reasoning(job_description, matches)
        
        try:
            # Prepare match summaries
            match_summaries = []
            for i, (file_name, match_data) in enumerate(matches[:3]):
                metadata = match_data['metadata']
                summary = f"""
                Resume {i+1}: {file_name}
                - Name: {metadata.get('name', 'Not specified')}
                - Skills: {metadata.get('skills', 'Not specified')}
                - Experience: {metadata.get('experience_years', 'Not specified')} years
                - Match Score: {match_data['best_score']:.4f}
                - Best Match Text: {match_data['best_match_text'][:300]}...
                """
                match_summaries.append(summary)
            
            prompt = f"""
            As an HR expert, analyze why these resumes are good matches for the given job description.
            
            Job Description:
            {job_description[:800]}...
            
            Top Matching Resumes:
            {chr(10).join(match_summaries)}
            
            Please provide:
            1. Overall assessment of the matches
            2. Key skills alignment for each candidate
            3. Strengths and potential concerns for each candidate
            4. Ranking recommendation with justification
            
            Keep the response concise but informative (max 400 words).
            """
            
            response = self.groq_client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.3
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error generating AI reasoning: {e}")
            return self._generate_basic_reasoning(job_description, matches)
    
    def _generate_basic_reasoning(self, job_description: str, matches: List) -> str:
        """Generate basic reasoning without AI"""
        if not matches:
            return "No matching resumes found."
        
        reasoning = "Resume Matching Analysis:\n\n"
        
        for i, (file_name, match_data) in enumerate(matches[:3]):
            metadata = match_data['metadata']
            reasoning += f"{i+1}. {file_name}\n"
            reasoning += f"   - Match Score: {match_data['best_score']:.4f} (lower is better)\n"
            reasoning += f"   - Skills: {metadata.get('skills', 'Not specified')}\n"
            reasoning += f"   - Experience: {metadata.get('experience_years', 'Not specified')} years\n"
            reasoning += f"   - Email: {metadata.get('email', 'Not specified')}\n\n"
        
        return reasoning
    
    def _extract_job_requirements(self, job_description: str) -> Dict:
        """Extract key requirements from job description"""
        try:
            # Extract skills using common patterns
            skills_section = self._extract_skills_from_job(job_description)
            
            # Extract experience requirements
            experience_req = self._extract_experience_requirement(job_description)
            
            # Extract education requirements
            education_req = self._extract_education_requirement(job_description)
            
            return {
                'required_skills': skills_section.get('required', []),
                'preferred_skills': skills_section.get('preferred', []),
                'experience_years': experience_req,
                'education_level': education_req,
                'job_type': self._extract_job_type(job_description)
            }
            
        except Exception as e:
            print(f"Error extracting job requirements: {e}")
            return {}
    
    def _extract_skills_from_job(self, job_description: str) -> Dict:
        """Extract skills from job description"""
        # Common technical skills
        tech_skills = [
            'python', 'java', 'javascript', 'react', 'node.js', 'sql', 'mysql', 'postgresql',
            'mongodb', 'git', 'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'machine learning',
            'data science', 'html', 'css', 'bootstrap', 'tailwind', 'express', 'django',
            'flask', 'fastapi', 'tensorflow', 'pytorch', 'pandas', 'numpy', 'scikit-learn',
            'vue.js', 'angular', 'spring', 'hibernate', 'redis', 'elasticsearch'
        ]
        
        text_lower = job_description.lower()
        found_skills = []
        
        for skill in tech_skills:
            if skill in text_lower:
                found_skills.append(skill)
        
        return {
            'required': found_skills[:10],  # Limit to top matches
            'preferred': []
        }
    
    def _extract_experience_requirement(self, job_description: str) -> str:
        """Extract experience requirements from job description"""
        experience_patterns = [
            r'(\d+)\+?\s*years?\s*(?:of\s*)?experience',
            r'(\d+)\+?\s*years?\s*(?:of\s*)?work',
            r'minimum\s*(?:of\s*)?(\d+)\+?\s*years?',
            r'at least\s*(\d+)\+?\s*years?'
        ]
        
        text_lower = job_description.lower()
        for pattern in experience_patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                return f"{matches[0]}+ years"
        
        # Check for entry level indicators
        entry_level_keywords = ['entry level', 'junior', 'associate', 'graduate', 'new grad']
        for keyword in entry_level_keywords:
            if keyword in text_lower:
                return "Entry Level"
        
        return "Not specified"
    
    def _extract_education_requirement(self, job_description: str) -> str:
        """Extract education requirements from job description"""
        education_keywords = {
            'phd': 'PhD',
            'doctorate': 'PhD',
            'master': 'Masters',
            'msc': 'Masters',
            'mba': 'MBA',
            'bachelor': 'Bachelors',
            'degree': 'Bachelors',
            'diploma': 'Diploma',
            'high school': 'High School'
        }
        
        text_lower = job_description.lower()
        for keyword, level in education_keywords.items():
            if keyword in text_lower:
                return level
        
        return "Not specified"
    
    def _extract_job_type(self, job_description: str) -> str:
        """Extract job type from description"""
        job_types = {
            'full-time': 'Full-time',
            'part-time': 'Part-time',
            'contract': 'Contract',
            'internship': 'Internship',
            'freelance': 'Freelance',
            'remote': 'Remote',
            'hybrid': 'Hybrid'
        }
        
        text_lower = job_description.lower()
        found_types = []
        
        for keyword, job_type in job_types.items():
            if keyword in text_lower:
                found_types.append(job_type)
        
        return ', '.join(found_types) if found_types else "Not specified"
    
    def get_statistics(self) -> Dict:
        """Get matching statistics"""
        try:
            return self.embedding_manager.get_collection_stats()
        except Exception as e:
            return {'error': str(e)}
