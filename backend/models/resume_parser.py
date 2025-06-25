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
    
    def extract_text_from_txt(self, txt_path: str) -> str:
        """Extract text from TXT file"""
        text = ""
        try:
            with open(txt_path, 'r', encoding='utf-8') as file:
                text = file.read()
        except Exception as e:
            print(f"Error extracting text from TXT: {e}")
            try:
                # Try with different encoding
                with open(txt_path, 'r', encoding='latin-1') as file:
                    text = file.read()
            except Exception as e2:
                print(f"Error extracting text from TXT with latin-1: {e2}")
                return ""
        return text
    
    def extract_text(self, file_path: str) -> str:
        """Extract text based on file extension"""
        file_extension = Path(file_path).suffix.lower()
        
        if file_extension == '.pdf':
            return self.extract_text_from_pdf(file_path)
        elif file_extension == '.docx':
            return self.extract_text_from_docx(file_path)
        elif file_extension == '.txt':
            return self.extract_text_from_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
    
    def extract_email(self, text: str) -> str:
        """Extract email address from text (improved)"""
        # Multiple email patterns to catch different formats
        email_patterns = [
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            r'Email[:\s]*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})',
            r'E-mail[:\s]*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})'
        ]
        
        for pattern in email_patterns:
            emails = re.findall(pattern, text, re.IGNORECASE)
            if emails:
                # Return the first valid email found
                email = emails[0] if isinstance(emails[0], str) else emails[0]
                # Validate email format
                if '@' in email and '.' in email.split('@')[1]:
                    return email.lower()
        return ""
    
    def extract_phone(self, text: str) -> str:
        """Extract phone number from text (improved)"""
        phone_patterns = [
            r'Phone[:\s]*([+]?[\d\s\-\(\)\.]{10,})',
            r'Mobile[:\s]*([+]?[\d\s\-\(\)\.]{10,})',
            r'Cell[:\s]*([+]?[\d\s\-\(\)\.]{10,})',
            r'Tel[:\s]*([+]?[\d\s\-\(\)\.]{10,})',
            r'[\+]?[1-9][0-9 .\-\(\)]{8,}[0-9]',
            r'\(\d{3}\)\s?\d{3}-\d{4}',
            r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}',
            r'\+\d{1,3}[-.\s]?\d{3,4}[-.\s]?\d{3,4}[-.\s]?\d{3,4}',
            r'\d{10}'
        ]
        
        for pattern in phone_patterns:
            phones = re.findall(pattern, text, re.IGNORECASE)
            if phones:
                phone = phones[0] if isinstance(phones[0], str) else phones[0]
                # Clean up the phone number
                phone = re.sub(r'[^\d+\-\(\)\.\s]', '', phone)
                # Remove extra spaces
                phone = ' '.join(phone.split())
                if len(re.sub(r'[^\d]', '', phone)) >= 10:  # At least 10 digits
                    return phone.strip()
        return ""
    
    def extract_name(self, text: str) -> str:
        """Extract name from resume (improved heuristic)"""
        lines = text.split('\n')
        
        # Common words to filter out
        filter_words = {'resume', 'cv', 'curriculum', 'vitae', 'profile', 'summary', 'contact', 
                       'information', 'phone', 'email', 'address', 'linkedin', 'github', 'portfolio'}
        
        # Try to find name in first 10 lines
        for line in lines[:10]:
            line = line.strip()
            if not line:
                continue
                
            # Skip lines with email, phone, or URLs
            if '@' in line or 'http' in line.lower() or re.search(r'\d{3}[-\.\s]?\d{3}[-\.\s]?\d{4}', line):
                continue
                
            # Split into words and filter
            words = line.split()
            if len(words) < 2 or len(words) > 5:  # Names usually 2-5 words
                continue
                
            # Check if line contains mostly alphabetic characters
            alpha_ratio = sum(c.isalpha() or c.isspace() for c in line) / len(line)
            if alpha_ratio < 0.7:
                continue
                
            # Filter out common resume words
            filtered_words = [w for w in words if w.lower() not in filter_words and not w.isdigit()]
            
            if len(filtered_words) >= 2:
                # Check if words look like names (start with capital letters)
                if all(word[0].isupper() for word in filtered_words if word):
                    return ' '.join(filtered_words)
        
        # Fallback: try to extract from filename if it looks like a name
        filename = text.split('\n')[0] if text else ""
        if filename and not any(word in filename.lower() for word in filter_words):
            name_match = re.search(r'^([A-Z][a-z]+\s+[A-Z][a-z]+)', filename)
            if name_match:
                return name_match.group(1)
                
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
        """Extract years of experience from text (improved and more accurate)"""
        experience_patterns = [
            r'(\d+)\+?\s*years?\s*(?:of\s*)?(?:professional\s*)?(?:work\s*)?experience',
            r'(\d+)\+?\s*years?\s*(?:of\s*)?(?:work\s*)?experience',
            r'(\d+)\+?\s*years?\s*(?:of\s*)?(?:relevant\s*)?experience',
            r'(\d+)\+?\s*years?\s*(?:of\s*)?(?:expertise|specialization)',
            r'with\s*(\d+)\+?\s*years?\s*(?:of\s*)?(?:expertise|experience)',
            r'experience[:\s]*(\d+)\+?\s*years?',
            r'(\d+)\+?\s*years?\s*(?:of\s*)?work',
            r'over\s*(\d+)\s*years?\s*(?:of\s*)?experience',
            r'more\s*than\s*(\d+)\s*years?\s*(?:of\s*)?experience',
            r'(\d+)\+\s*years?\s*(?:professional\s*)?(?:experience|background)',
            r'total\s*(?:of\s*)?(\d+)\s*years?\s*experience'
        ]
        
        text_lower = text.lower()
        
        # First, try to find explicit experience statements
        for pattern in experience_patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                years = int(matches[0])
                # Reasonable bounds check (0-50 years)
                if 0 <= years <= 50:
                    print(f"[DEBUG] Found explicit experience: {years} years from pattern: {pattern}")
                    return years
        
        # Only try date range calculation if we find work-related context
        work_context_patterns = [
            r'(?:employment|work|job|position|role|career).*?(\d{4})\s*[-–—]\s*(\d{4})',
            r'(?:employment|work|job|position|role|career).*?(\d{4})\s*[-–—]\s*(?:present|current)',
            r'(?:employment|work|job|position|role|career).*?(\d{4})\s*to\s*(\d{4})',
            r'(?:employment|work|job|position|role|career).*?(\d{4})\s*to\s*(?:present|current)',
            r'(?:software engineer|developer|analyst|manager|coordinator).*?(\d{4})\s*[-–—]\s*(\d{4})',
            r'(?:software engineer|developer|analyst|manager|coordinator).*?(\d{4})\s*[-–—]\s*(?:present|current)'
        ]
        
        total_years = 0
        current_year = 2025
        work_experience_found = False
        
        # Check for work-related date ranges
        for pattern in work_context_patterns:
            matches = re.findall(pattern, text_lower)
            for match in matches:
                if len(match) == 2:
                    start_year = int(match[0])
                    end_year = int(match[1]) if match[1].isdigit() else current_year
                    
                    # Reasonable year bounds and ensure it's not education dates
                    if 1980 <= start_year <= current_year and start_year <= end_year <= current_year:
                        years = end_year - start_year
                        if years > 0:  # Only count if there's actual duration
                            total_years += years
                            work_experience_found = True
                            print(f"[DEBUG] Found work experience from {start_year} to {end_year}: {years} years")
        
        # If no work context found, be more conservative with general date patterns
        if not work_experience_found:
            # Look for education years to exclude them
            education_patterns = [
                r'(?:university|college|school|education|degree|bachelor|master|phd|institute|iit|mit|stanford).*?(\d{4})\s*[-–—]\s*(\d{4})',
                r'(?:university|college|school|education|degree|bachelor|master|phd|institute|iit|mit|stanford).*?(\d{4})',
                r'(?:graduated|graduation).*?(\d{4})',
                r'(?:b\.?[as]\.?|m\.?[as]\.?|ph\.?d\.?).*?(\d{4})\s*[-–—]\s*(\d{4})',
                r'(?:b\.?[as]\.?|m\.?[as]\.?|ph\.?d\.?).*?(\d{4})'
            ]
            
            education_years = set()
            for pattern in education_patterns:
                matches = re.findall(pattern, text_lower)
                for match in matches:
                    if isinstance(match, tuple):
                        education_years.update([int(year) for year in match if year.isdigit()])
                    else:
                        education_years.add(int(match))
            
            print(f"[DEBUG] Found education years: {education_years}")
            
            # Only use general date patterns if they don't overlap with education
            general_date_patterns = [
                r'(\d{4})\s*[-–—]\s*(\d{4})',
                r'(\d{4})\s*[-–—]\s*(?:present|current)',
                r'(\d{4})\s*to\s*(\d{4})',
                r'(\d{4})\s*to\s*(?:present|current)'
            ]
            
            for pattern in general_date_patterns:
                matches = re.findall(pattern, text_lower)
                for match in matches:
                    if len(match) == 2:
                        start_year = int(match[0])
                        end_year = int(match[1]) if match[1].isdigit() else current_year
                        
                        # Skip if these years overlap with education
                        if start_year in education_years or end_year in education_years:
                            print(f"[DEBUG] Skipping {start_year}-{end_year} as it overlaps with education")
                            continue
                            
                        if 1980 <= start_year <= current_year and start_year <= end_year <= current_year:
                            years = end_year - start_year
                            if years > 0 and years <= 15:  # Be conservative, max 15 years from general dates
                                total_years += years
                                print(f"[DEBUG] Added general date range {start_year}-{end_year}: {years} years")
        
        if total_years > 0:
            final_years = min(total_years, 50)  # Cap at 50 years
            print(f"[DEBUG] Final calculated experience: {final_years} years")
            return final_years
        
        print(f"[DEBUG] No experience found")
        return None
    
    def parse_resume(self, file_path: str) -> Dict:
        """Parse resume and extract all information"""
        try:
            text = self.extract_text(file_path)
            
            # Extract original filename from the unique filename
            # Format: originalname_timestamp_uniqueid.ext
            filename = os.path.basename(file_path)
            original_filename = filename
            
            # Try to extract original name if it follows our naming pattern
            if '_' in filename:
                parts = filename.split('_')
                if len(parts) >= 3:
                    # Remove timestamp and unique ID, keep original name
                    original_name_parts = parts[:-2]  # Remove last 2 parts (timestamp, uniqueid)
                    if original_name_parts:
                        original_filename = '_'.join(original_name_parts) + os.path.splitext(filename)[1]
            
            parsed_data = {
                'file_name': original_filename,  # Display original filename
                'unique_file_name': filename,    # Store unique filename for reference
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
    
    def debug_extraction(self, file_path: str) -> Dict:
        """Debug method to see what's being extracted from each step"""
        try:
            text = self.extract_text(file_path)
            
            # Show first 500 characters of text
            preview_text = text[:500] + "..." if len(text) > 500 else text
            
            debug_info = {
                'file_name': os.path.basename(file_path),
                'text_preview': preview_text,
                'text_length': len(text),
                'first_10_lines': text.split('\n')[:10],
                'extracted_name': self.extract_name(text),
                'extracted_email': self.extract_email(text),
                'extracted_phone': self.extract_phone(text),
                'extracted_experience': self.extract_experience_years(text),
                'extracted_skills_count': len(self.extract_skills(text)),
                'extracted_skills_sample': self.extract_skills(text)[:10]  # First 10 skills
            }
            
            return debug_info
            
        except Exception as e:
            return {
                'error': str(e),
                'file_name': os.path.basename(file_path)
            }
