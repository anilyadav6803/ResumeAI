from typing import List, Dict, Optional
import numpy as np
from sentence_transformers import SentenceTransformer
import json
import os
import re

class JobMatcher:
    def __init__(self):
        """Initialize the JobMatcher with a sentence transformer model"""
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.resume_index = []  # Store processed resumes
        
    def process_job_description(self, job_description: str) -> Dict:
        """Process job description and extract key information"""
        processed = {
            'text': job_description,
            'embedding': self.model.encode([job_description])[0],
            'keywords': self.extract_keywords(job_description),
            'requirements': self.extract_requirements(job_description)
        }
        return processed
    
    def extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from job description"""
        keywords = []
        
        # Expanded technical keywords for better matching
        tech_keywords = [
            # Programming Languages
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust', 'swift', 'kotlin',
            'scala', 'perl', 'r', 'matlab', 'shell', 'bash', 'powershell',
            
            # Web Technologies
            'html', 'css', 'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask', 'spring', 'laravel',
            'rails', 'bootstrap', 'jquery', 'webpack', 'babel', 'sass', 'less',
            
            # Databases
            'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'oracle', 'sqlite', 'cassandra',
            'dynamodb', 'firebase',
            
            # Cloud & DevOps
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'git', 'github', 'gitlab', 'ci/cd', 'devops',
            'terraform', 'ansible', 'chef', 'puppet', 'vagrant',
            
            # Data Science & AI
            'machine learning', 'deep learning', 'ai', 'artificial intelligence', 'data science', 'tensorflow',
            'pytorch', 'keras', 'scikit-learn', 'pandas', 'numpy', 'matplotlib', 'jupyter',
            
            # Mobile Development
            'android', 'ios', 'flutter', 'react native', 'xamarin', 'cordova', 'ionic',
            
            # Other Technologies
            'api', 'rest', 'graphql', 'microservices', 'agile', 'scrum', 'kanban', 'linux', 'unix', 'windows',
            'testing', 'unit testing', 'integration testing', 'tdd', 'bdd',
            
            # Skills
            'software development', 'full stack', 'frontend', 'backend', 'full-stack', 'software engineer',
            'developer', 'programming', 'coding', 'debugging', 'troubleshooting', 'problem solving'
        ]
        
        text_lower = text.lower()
        for keyword in tech_keywords:
            if keyword in text_lower:
                keywords.append(keyword)
        
        # Extract skills mentioned with common patterns
        skill_patterns = [
            r'experience with ([a-zA-Z0-9\+\-\.\s]{2,30})',
            r'proficient in ([a-zA-Z0-9\+\-\.\s]{2,30})',
            r'knowledge of ([a-zA-Z0-9\+\-\.\s]{2,30})',
            r'familiar with ([a-zA-Z0-9\+\-\.\s]{2,30})',
            r'expertise in ([a-zA-Z0-9\+\-\.\s]{2,30})',
            r'skilled in ([a-zA-Z0-9\+\-\.\s]{2,30})',
            r'worked with ([a-zA-Z0-9\+\-\.\s]{2,30})',
            r'using ([a-zA-Z0-9\+\-\.\s]{2,30})',
        ]
        
        for pattern in skill_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                # Clean up the match
                cleaned = match.strip().split(',')[0].split(' and ')[0].strip()
                if len(cleaned) > 1 and cleaned.lower() not in keywords:
                    keywords.append(cleaned.lower())
        
        return list(set(keywords))
    
    def extract_requirements(self, text: str) -> List[str]:
        """Extract requirements from job description"""
        requirements = []
        
        # Look for bullet points or numbered lists
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('•') or line.startswith('-') or line.startswith('*'):
                req = line[1:].strip()
                if len(req) > 10:
                    requirements.append(req)
            elif re.match(r'^\d+\.', line):
                req = re.sub(r'^\d+\.\s*', '', line).strip()
                if len(req) > 10:
                    requirements.append(req)
        
        return requirements
    
    def calculate_match_score(self, resume_embedding: np.ndarray, job_embedding: np.ndarray) -> float:
        """Calculate cosine similarity between resume and job embeddings"""
        # Calculate cosine similarity
        dot_product = np.dot(resume_embedding, job_embedding)
        norm_a = np.linalg.norm(resume_embedding)
        norm_b = np.linalg.norm(job_embedding)
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
        
        similarity = dot_product / (norm_a * norm_b)
        return float(similarity)
    
    def match_resumes(self, resumes: List[Dict], job_description: str, top_k: int = 5) -> List[Dict]:
        """Match resumes against job description and return top matches with enhanced debugging"""
        try:
            print(f"[DEBUG] Starting match_resumes with {len(resumes)} resumes")
            print(f"[DEBUG] Job description preview: {job_description[:100]}...")
            
            job_data = self.process_job_description(job_description)
            matches = []
            
            print(f"[DEBUG] Job keywords extracted: {job_data['keywords'][:10]}...")  # Show first 10
            
            for i, resume in enumerate(resumes):
                print(f"[DEBUG] Processing resume {i+1}: {resume.get('file_name', 'Unknown')}")
                
                # Check if resume has text content
                resume_text = resume.get('text', '') or resume.get('full_text', '') or resume.get('content', '')
                
                if not resume_text:
                    print(f"[DEBUG] Skipping resume {i+1}: No text content found")
                    print(f"[DEBUG] Resume keys: {list(resume.keys())}")
                    continue
                
                print(f"[DEBUG] Resume {i+1} text preview: {resume_text[:100]}...")
                
                # Create embedding if not exists
                if 'embedding' not in resume or resume['embedding'] is None:
                    print(f"[DEBUG] Creating embedding for resume {i+1}")
                    resume['embedding'] = self.model.encode([resume_text])[0].tolist()
                
                # Calculate similarity score  
                resume_embedding = np.array(resume['embedding'])
                job_embedding = np.array(job_data['embedding'])
                
                similarity_score = self.calculate_match_score(resume_embedding, job_embedding)
                print(f"[DEBUG] Resume {i+1} similarity score: {similarity_score:.4f}")
                
                # Extract skills from resume for keyword matching
                resume_keywords = self.extract_keywords(resume_text)
                common_keywords = list(set(job_data['keywords']) & set(resume_keywords))
                
                # Calculate keyword match ratio
                keyword_match_ratio = len(common_keywords) / max(len(job_data['keywords']), 1) if job_data['keywords'] else 0
                
                # Combine similarity score with keyword matching
                # Weight: 60% similarity + 40% keyword matching
                combined_score = (0.6 * similarity_score) + (0.4 * keyword_match_ratio)
                
                print(f"[DEBUG] Resume {i+1} keyword matches ({len(common_keywords)}): {common_keywords[:5]}...")
                print(f"[DEBUG] Resume {i+1} combined score: {combined_score:.4f}")
                
                preview_text = resume_text[:200] + '...' if len(resume_text) > 200 else resume_text
                
                match = {
                    'file_name': resume.get('file_name', 'Unknown'),
                    'score': combined_score,
                    'similarity_score': float(similarity_score),
                    'keyword_match_ratio': keyword_match_ratio,
                    'matched_keywords': common_keywords,
                    'resume_keywords': resume_keywords[:10],  # Limit for display
                    'metadata': resume.get('metadata', {}),
                    'best_match_text': preview_text
                }
                matches.append(match)
            
            print(f"[DEBUG] Generated {len(matches)} matches before sorting")
            
            # Sort by combined score and return top_k
            matches.sort(key=lambda x: x['score'], reverse=True)
            
            # Always return results if any resumes were processed, even with low scores
            if matches:
                result = matches[:top_k]
                print(f"[DEBUG] Returning top {len(result)} matches")
                for i, match in enumerate(result):
                    print(f"[DEBUG] Match {i+1}: {match['file_name']} - Score: {match['score']:.4f}")
                return result
            else:
                print("[DEBUG] No matches generated - this might indicate an issue with resume processing")
                return []
                
        except Exception as e:
            print(f"[ERROR] Error in match_resumes: {str(e)}")
            import traceback
            traceback.print_exc()
            return []
    
    def create_resume_index(self, resumes: List[Dict]) -> Dict:
        """Create an index of resumes for efficient searching"""
        try:
            print(f"[DEBUG] Creating resume index for {len(resumes)} resumes")
            self.resume_index = []
            processed_count = 0
            
            for i, resume in enumerate(resumes):
                print(f"[DEBUG] Indexing resume {i+1}: {resume.get('file_name', 'Unknown')}")
                
                # Check both 'text' and 'full_text' keys for compatibility
                resume_text = resume.get('text', '') or resume.get('full_text', '') or resume.get('content', '')
                
                if resume_text:
                    print(f"[DEBUG] Resume {i+1} text length: {len(resume_text)}")
                    
                    # Create embedding if not exists
                    if 'embedding' not in resume or resume['embedding'] is None:
                        print(f"[DEBUG] Creating embedding for indexed resume {i+1}")
                        resume['embedding'] = self.model.encode([resume_text])[0].tolist()
                    
                    # Add to index
                    indexed_resume = {
                        'file_name': resume.get('file_name', f'resume_{len(self.resume_index)}'),
                        'text': resume_text,
                        'embedding': resume['embedding'],
                        'metadata': resume.get('metadata', {}),
                        'skills': self.extract_skills_from_text(resume_text),
                        'experience': self.extract_experience_from_text(resume_text)
                    }
                    self.resume_index.append(indexed_resume)
                    processed_count += 1
                else:
                    print(f"[DEBUG] Skipping resume {i+1}: No text content")
                    print(f"[DEBUG] Resume keys: {list(resume.keys())}")
            
            result = {
                'success': True,
                'message': f'Successfully indexed {processed_count} resumes',
                'total_resumes': len(self.resume_index)
            }
            print(f"[DEBUG] Index creation result: {result}")
            return result
            
        except Exception as e:
            print(f"[ERROR] Error creating resume index: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'message': f'Error creating resume index: {str(e)}',
                'total_resumes': 0
            }
    
    def extract_skills_from_text(self, text: str) -> List[str]:
        """Extract skills from resume text"""
        skills = []
        text_lower = text.lower()
        
        # Common technical skills (expanded)
        tech_skills = [
            'python', 'java', 'javascript', 'react', 'node.js', 'sql', 'mongodb',
            'aws', 'docker', 'kubernetes', 'git', 'agile', 'scrum', 'machine learning',
            'data science', 'ai', 'artificial intelligence', 'deep learning',
            'tensorflow', 'pytorch', 'pandas', 'numpy', 'api', 'rest', 'graphql',
            'html', 'css', 'bootstrap', 'angular', 'vue', 'typescript', 'c++', 'c#',
            'php', 'ruby', 'go', 'rust', 'swift', 'kotlin', 'flutter', 'django',
            'flask', 'spring', 'express', 'laravel', 'rails', 'excel', 'powerbi',
            'tableau', 'spark', 'hadoop', 'elasticsearch', 'redis', 'postgresql',
            'mysql', 'oracle', 'sqlite', 'linux', 'unix', 'windows', 'azure', 'gcp'
        ]
        
        for skill in tech_skills:
            if skill in text_lower:
                skills.append(skill)
        
        return skills
    
    def extract_experience_from_text(self, text: str) -> List[str]:
        """Extract experience information from resume text"""
        experience = []
        
        # Look for experience patterns
        exp_patterns = [
            r'(\d+)\+?\s*years?\s*(?:of\s*)?experience',
            r'experience\s*(?:of\s*)?(\d+)\+?\s*years?',
            r'(\d+)\+?\s*years?\s*in\s*([a-zA-Z\s]+)',
            r'worked\s*(?:as\s*)?([a-zA-Z\s]+)\s*for\s*(\d+)\+?\s*years?'
        ]
        
        for pattern in exp_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    experience.append(' '.join(str(m) for m in match))
                else:
                    experience.append(str(match))
        
        return experience
