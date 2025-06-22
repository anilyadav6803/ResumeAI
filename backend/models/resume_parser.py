import pdfplumber
import docx
from typing import Dict, List, Optional
import re
import os
from pathlib import Path

class ResumeParser:
    def __init__(self):
        self.sections = ['experience', 'education', 'skills', 'projects', 'summary']
        
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF file"""
        text = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return ""
        return text
    
    def extract_text_from_docx(self, docx_path: str) -> str:
        """Extract text from DOCX file"""
        text = ""
        try:
            doc = docx.Document(docx_path)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            print(f"Error extracting text from DOCX: {e}")
            return ""
        return text
    
    def extract_text(self, file_path: str) -> str:
        """Extract text based on file extension"""
        file_extension = Path(file_path).suffix.lower()
        
        if file_extension == '.pdf':
            return self.extract_text_from_pdf(file_path)
        elif file_extension == '.docx':
            return self.extract_text_from_docx(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
    
    def extract_email(self, text: str) -> str:
        """Extract email address from text"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        return emails[0] if emails else ""
    
    def extract_phone(self, text: str) -> str:
        """Extract phone number from text"""
        phone_patterns = [
            r'[\+]?[1-9][0-9 .\-\(\)]{8,}[0-9]',
            r'\(\d{3}\)\s?\d{3}-\d{4}',
            r'\d{3}-\d{3}-\d{4}',
            r'\d{10}'
        ]
        
        for pattern in phone_patterns:
            phones = re.findall(pattern, text)
            if phones:
                return phones[0].strip()
        return ""
    
    def extract_name(self, text: str) -> str:
        """Extract name from resume (simple heuristic)"""
        lines = text.split('\n')
        for line in lines[:5]:  # Check first 5 lines
            line = line.strip()
            if line and len(line.split()) <= 4 and not '@' in line:
                # Remove common words that might appear in names
                words = line.split()
                filtered_words = [w for w in words if w.lower() not in ['resume', 'cv', 'curriculum', 'vitae']]
                if len(filtered_words) >= 2:
                    return ' '.join(filtered_words)
        return ""

    def extract_skills(self, text: str) -> List[str]:
        """Extract skills from resume text"""
        # Comprehensive skill keywords organized by category
        skill_keywords = {
            'programming_languages': [
                'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'php', 'ruby', 'go', 
                'rust', 'kotlin', 'swift', 'r', 'matlab', 'scala', 'perl', 'shell', 'bash'
            ],
            'web_technologies': [
                'html', 'css', 'react', 'angular', 'vue', 'node.js', 'express', 'next.js', 
                'nuxt.js', 'gatsby', 'svelte', 'bootstrap', 'tailwind', 'sass', 'less', 
                'webpack', 'vite', 'jquery', 'backbone.js', 'ember.js'
            ],
            'databases': [
                'mysql', 'postgresql', 'mongodb', 'redis', 'sqlite', 'oracle', 'sql server',
                'cassandra', 'dynamodb', 'elasticsearch', 'neo4j', 'firebase', 'supabase'
            ],
            'frameworks': [
                'django', 'flask', 'fastapi', 'spring', 'laravel', 'rails', 'express.js',
                'nest.js', 'asp.net', 'xamarin', 'react native', 'flutter', 'ionic'
            ],
            'cloud_devops': [
                'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'gitlab ci',
                'github actions', 'terraform', 'ansible', 'chef', 'puppet', 'vagrant',
                'nginx', 'apache', 'linux', 'ubuntu', 'centos', 'redhat'
            ],
            'data_science': [
                'machine learning', 'deep learning', 'artificial intelligence', 'data science',
                'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'keras',
                'matplotlib', 'seaborn', 'jupyter', 'anaconda', 'spark', 'hadoop',
                'tableau', 'power bi', 'looker', 'qlik'
            ],
            'tools': [
                'git', 'github', 'gitlab', 'bitbucket', 'jira', 'confluence', 'slack',
                'trello', 'asana', 'notion', 'figma', 'sketch', 'adobe xd', 'photoshop',
                'illustrator', 'postman', 'insomnia', 'vs code', 'intellij', 'eclipse'
            ],
            'methodologies': [
                'agile', 'scrum', 'kanban', 'waterfall', 'devops', 'ci/cd', 'tdd', 'bdd',
                'microservices', 'api', 'rest', 'graphql', 'soap', 'json', 'xml'
            ],
            'soft_skills': [
                'leadership', 'communication', 'teamwork', 'problem solving', 'critical thinking',
                'project management', 'time management', 'analytical', 'creative', 'adaptable'
            ]
        }
        
        text_lower = text.lower()
        found_skills = []
        
        # Flatten all skill categories
        all_skills = []
        for category, skills in skill_keywords.items():
            all_skills.extend(skills)
        
        for skill in all_skills:
            # Use word boundaries to avoid partial matches
            if re.search(r'\b' + re.escape(skill.lower()) + r'\b', text_lower):
                found_skills.append(skill.title())
        
        # Remove duplicates and sort
        found_skills = sorted(list(set(found_skills)))
        
        return found_skills
    
    def extract_experience_years(self, text: str) -> Optional[int]:
        """Extract years of experience from text"""
        experience_patterns = [
            r'(\d+)\+?\s*years?\s*(?:of\s*)?experience',
            r'(\d+)\+?\s*years?\s*(?:of\s*)?work',
            r'experience\s*(?:of\s*)?(\d+)\+?\s*years?'
        ]
        
        text_lower = text.lower()
        for pattern in experience_patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                return int(matches[0])
        
        return None
    
    def parse_resume(self, file_path: str) -> Dict:
        """Parse resume and extract all information"""
        try:
            text = self.extract_text(file_path)
            
            parsed_data = {
                'file_name': os.path.basename(file_path),
                'file_path': file_path,
                'full_text': text,
                'name': self.extract_name(text),
                'email': self.extract_email(text),
                'phone': self.extract_phone(text),
                'skills': self.extract_skills(text),
                'experience_years': self.extract_experience_years(text),
                'text_length': len(text),
                'word_count': len(text.split()),
                'parsing_status': 'success'
            }
            
            return parsed_data
            
        except Exception as e:
            return {
                'file_name': os.path.basename(file_path),
                'file_path': file_path,
                'parsing_status': 'error',
                'error_message': str(e),
                'full_text': '',
                'name': '',
                'email': '',
                'phone': '',
                'skills': [],
                'experience_years': None,
                'text_length': 0,
                'word_count': 0
            }
    
    def batch_parse_resumes(self, file_paths: List[str]) -> List[Dict]:
        """Parse multiple resumes"""
        results = []
        for file_path in file_paths:
            result = self.parse_resume(file_path)
            results.append(result)
        return results
