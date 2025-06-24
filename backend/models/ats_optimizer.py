from typing import Dict, List
import json
import re
import os
import groq

class ATSOptimizer:
    def __init__(self):
        """Initialize ATS optimizer with AI client"""
        self.groq_client = None
        self._initialize_ai_client()
        
    def _initialize_ai_client(self):
        """Initialize Groq AI client"""
        try:
            groq_api_key = os.getenv("GROQ_API_KEY")
            if groq_api_key:
                # Initialize Groq client without proxies parameter
                self.groq_client = groq.Groq(api_key=groq_api_key)
                print("✅ Initialized Groq AI client for ATS optimization")
            else:
                print("⚠️ Warning: GROQ_API_KEY not found. ATS optimization will use basic analysis.")
                self.groq_client = None
        except Exception as e:
            print(f"❌ Error initializing Groq client for ATS: {e}")
            self.groq_client = None
    
    def optimize_resume(self, resume_text: str, job_description: str) -> Dict:
        """Optimize resume for ATS and job description"""
        try:
            if self.groq_client:
                return self._ai_optimize_resume(resume_text, job_description)
            else:
                return self._basic_optimize_resume(resume_text, job_description)
        except Exception as e:
            print(f"Error optimizing resume: {e}")
            return {
                'error': str(e),
                'basic_analysis': self._basic_optimize_resume(resume_text, job_description)
            }
    
    def _ai_optimize_resume(self, resume_text: str, job_description: str) -> Dict:
        """Use AI to optimize resume"""
        try:
            prompt = f"""
            As an ATS (Applicant Tracking System) expert and HR professional, analyze this resume against the job description and provide optimization recommendations.
            
            RESUME:
            {resume_text[:2000]}...
            
            JOB DESCRIPTION:
            {job_description[:1000]}...
            
            Please provide a detailed JSON response with the following structure:
            {{
                "ats_score": <score_out_of_100>,
                "missing_keywords": [<list_of_important_keywords_missing_from_resume>],
                "keyword_optimization": {{
                    "add_keywords": [<keywords_to_add>],
                    "improve_sections": [<sections_that_need_keyword_improvement>]
                }},
                "format_improvements": [<list_of_formatting_suggestions>],
                "content_suggestions": [<list_of_content_improvement_suggestions>],
                "skills_gap": [<skills_mentioned_in_job_but_missing_from_resume>],
                "strengths": [<existing_strengths_that_match_job>],
                "action_items": [<specific_actionable_recommendations>]
            }}
            
            Focus on:
            1. ATS-friendly formatting
            2. Keyword optimization
            3. Skills alignment
            4. Content structure
            5. Quantifiable achievements
            """
            
            response = self.groq_client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=0.3
            )
            
            # Try to parse JSON response
            try:
                result = json.loads(response.choices[0].message.content)
                return result
            except json.JSONDecodeError:
                # If JSON parsing fails, return the raw response
                return {
                    'ai_response': response.choices[0].message.content,
                    'parsing_error': 'Could not parse AI response as JSON'
                }
                
        except Exception as e:
            print(f"Error in AI optimization: {e}")
            return self._basic_optimize_resume(resume_text, job_description)
    
    def _basic_optimize_resume(self, resume_text: str, job_description: str) -> Dict:
        """Basic resume optimization without AI"""
        try:
            # Extract keywords from job description
            job_keywords = self._extract_keywords(job_description)
            resume_keywords = self._extract_keywords(resume_text)
            
            # Find missing keywords
            missing_keywords = [kw for kw in job_keywords if kw not in resume_keywords]
            
            # Basic ATS score calculation
            keyword_match_score = (len(job_keywords) - len(missing_keywords)) / len(job_keywords) * 100 if job_keywords else 0
            format_score = self._calculate_format_score(resume_text)
            ats_score = (keyword_match_score * 0.7 + format_score * 0.3)
            
            return {
                'ats_score': round(ats_score, 1),
                'missing_keywords': missing_keywords[:10],  # Top 10 missing keywords
                'keyword_optimization': {
                    'add_keywords': missing_keywords[:5],
                    'improve_sections': ['Skills', 'Experience', 'Summary']
                },
                'format_improvements': self._get_format_suggestions(resume_text),
                'content_suggestions': self._get_content_suggestions(resume_text, job_description),
                'skills_gap': missing_keywords[:7],
                'strengths': list(set(job_keywords) & set(resume_keywords))[:5],
                'action_items': self._generate_action_items(missing_keywords, resume_text)
            }
            
        except Exception as e:
            return {
                'error': f'Basic optimization failed: {str(e)}',
                'ats_score': 0,
                'missing_keywords': [],
                'recommendations': 'Please check your resume format and try again.'            }

    def _extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords from text using comprehensive analysis"""
        # Comprehensive keywords pool organized by category
        keywords_pool = {
            'programming_languages': [
                'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'php', 'ruby', 'go', 
                'rust', 'kotlin', 'swift', 'r', 'matlab', 'scala', 'perl', 'shell', 'bash',
                'powershell', 'lua', 'dart', 'elixir', 'clojure', 'haskell', 'f#'
            ],
            'web_technologies': [
                'html', 'css', 'react', 'angular', 'vue', 'node.js', 'express', 'next.js', 
                'nuxt.js', 'gatsby', 'svelte', 'bootstrap', 'tailwind', 'sass', 'less', 
                'webpack', 'vite', 'parcel', 'rollup', 'jquery', 'backbone.js', 'ember.js',
                'react native', 'flutter', 'ionic', 'cordova', 'phonegap'
            ],
            'databases': [
                'mysql', 'postgresql', 'mongodb', 'redis', 'sqlite', 'oracle', 'sql server',
                'cassandra', 'dynamodb', 'elasticsearch', 'neo4j', 'firebase', 'supabase',
                'mariadb', 'couchdb', 'influxdb', 'clickhouse', 'bigquery'
            ],
            'frameworks_libraries': [
                'django', 'flask', 'fastapi', 'spring', 'spring boot', 'laravel', 'rails',
                'express.js', 'nest.js', 'asp.net', 'xamarin', '.net', 'entity framework',
                'hibernate', 'struts', 'play framework', 'symfony', 'codeigniter'
            ],
            'cloud_devops': [
                'aws', 'azure', 'gcp', 'google cloud', 'docker', 'kubernetes', 'jenkins', 
                'gitlab ci', 'github actions', 'terraform', 'ansible', 'chef', 'puppet', 
                'vagrant', 'nginx', 'apache', 'linux', 'ubuntu', 'centos', 'redhat',
                'heroku', 'digitalocean', 'cloudflare', 'lambda', 'ec2', 's3', 'rds'
            ],
            'data_science_ml': [
                'machine learning', 'deep learning', 'artificial intelligence', 'data science',
                'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'keras',
                'matplotlib', 'seaborn', 'plotly', 'jupyter', 'anaconda', 'spark', 'hadoop',
                'tableau', 'power bi', 'looker', 'qlik', 'nlp', 'computer vision', 'opencv'
            ],
            'tools_platforms': [
                'git', 'github', 'gitlab', 'bitbucket', 'jira', 'confluence', 'slack',
                'trello', 'asana', 'notion', 'figma', 'sketch', 'adobe xd', 'photoshop',
                'illustrator', 'postman', 'insomnia', 'vs code', 'intellij', 'eclipse',
                'sublime', 'atom', 'vim', 'emacs'
            ],
            'methodologies': [
                'agile', 'scrum', 'kanban', 'waterfall', 'devops', 'ci/cd', 'tdd', 'bdd',
                'microservices', 'monolith', 'api', 'rest', 'restful', 'graphql', 'soap', 
                'json', 'xml', 'yaml', 'oauth', 'jwt', 'websockets'
            ],
            'soft_skills': [
                'leadership', 'communication', 'teamwork', 'collaboration', 'problem solving', 
                'critical thinking', 'project management', 'time management', 'analytical', 
                'creative', 'adaptable', 'innovative', 'strategic', 'detail oriented',
                'mentoring', 'coaching', 'presentation', 'negotiation'
            ],
            'business_domains': [
                'fintech', 'healthcare', 'e-commerce', 'education', 'gaming', 'media',
                'telecommunications', 'automotive', 'retail', 'logistics', 'real estate',
                'insurance', 'banking', 'saas', 'b2b', 'b2c', 'startup', 'enterprise'
            ]
        }
        
        text_lower = text.lower()
        found_keywords = []
        
        # Flatten all keyword categories
        all_keywords = []
        for category, keywords in keywords_pool.items():
            all_keywords.extend(keywords)
        
        # Find keywords using word boundaries for accuracy
        for keyword in all_keywords:
            # Use regex with word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
            if re.search(pattern, text_lower):
                found_keywords.append(keyword)
        
        # Also extract domain-specific terms (job titles, experience levels, etc.)
        additional_patterns = [
            r'\b(senior|junior|lead|principal|staff|architect)\s+\w+',
            r'\b\d+\+?\s*years?\s*(?:of\s*)?(?:experience|exp)\b',
            r'\b(?:bachelor|master|phd|degree|certification)\s+\w+',
            r'\b(?:full.?stack|front.?end|back.?end|full.?time|part.?time)\b'
        ]
        
        for pattern in additional_patterns:
            matches = re.findall(pattern, text_lower)
            found_keywords.extend(matches)
        
        # Remove duplicates and sort by frequency in text
        keyword_counts = {}
        for kw in found_keywords:
            kw_clean = kw.strip().lower()
            if kw_clean:
                keyword_counts[kw_clean] = keyword_counts.get(kw_clean, 0) + 1
          # Return keywords sorted by frequency (most frequent first)
        sorted_keywords = sorted(keyword_counts.keys(), key=lambda x: keyword_counts[x], reverse=True)
        
        return sorted_keywords[:30]  # Return top 30 keywords
    
    def _calculate_format_score(self, resume_text: str) -> float:
        """Calculate basic format score for ATS compatibility"""
        score = 100
        
        # Check for common ATS-unfriendly elements
        if len(resume_text.split()) < 100:
            score -= 20  # Too short
        
        if len(resume_text.split()) > 1000:
            score -= 10  # Too long
        
        # Check for email
        if not re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', resume_text):
            score -= 15
        
        # Check for phone
        if not re.search(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', resume_text):
            score -= 10
        
        # Check for common sections
        sections = ['experience', 'education', 'skills']
        for section in sections:
            if section.lower() not in resume_text.lower():
                score -= 10
        
        return max(0, score)
    
    def _get_format_suggestions(self, resume_text: str) -> List[str]:
        """Get formatting suggestions for ATS optimization"""
        suggestions = []
        
        # Check common issues
        if not re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', resume_text):
            suggestions.append("Add a professional email address")
        
        if not re.search(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', resume_text):
            suggestions.append("Include a phone number")
        
        if len(resume_text.split()) < 200:
            suggestions.append("Resume appears too short - add more detail to experience and skills")
        
        if len(resume_text.split()) > 800:
            suggestions.append("Resume may be too long - consider condensing to 1-2 pages")
        
        # Standard formatting suggestions
        suggestions.extend([
            "Use standard section headers (Experience, Education, Skills)",
            "Use bullet points for achievements and responsibilities",
            "Include quantifiable achievements (numbers, percentages, metrics)",
            "Use consistent date formatting",
            "Avoid headers, footers, and graphics that ATS can't read"
        ])
        
        return suggestions
    
    def _get_content_suggestions(self, resume_text: str, job_description: str) -> List[str]:
        """Get content improvement suggestions"""
        suggestions = [
            "Tailor your professional summary to match the job requirements",
            "Use action verbs to describe your accomplishments",
            "Include specific technologies and tools mentioned in the job posting",
            "Quantify your achievements with numbers and metrics",
            "Match your experience descriptions to job requirements",
            "Include relevant certifications and training",
            "Use industry-specific terminology from the job description"
        ]
        
        return suggestions
    
    def _generate_action_items(self, missing_keywords: List[str], resume_text: str) -> List[str]:
        """Generate specific action items for optimization"""
        action_items = []
        
        if missing_keywords:
            action_items.append(f"Add these key skills to your resume: {', '.join(missing_keywords[:5])}")
        
        if 'experience' not in resume_text.lower():
            action_items.append("Add a dedicated 'Experience' or 'Work History' section")
        
        if 'skills' not in resume_text.lower():
            action_items.append("Create a 'Skills' section with relevant technical and soft skills")
        
        action_items.extend([
            "Review job description and incorporate exact phrases where truthful",
            "Add quantifiable achievements to each role",
            "Ensure your resume is in a simple, ATS-friendly format",
            "Proofread for spelling and grammatical errors",
            "Save resume as both PDF and Word document"
        ])
        
        return action_items
    
    def analyze_job_keywords(self, job_description: str) -> Dict:
        """Analyze and extract key information from job description"""
        try:
            keywords = self._extract_keywords(job_description)
            
            return {
                'total_keywords': len(keywords),
                'top_keywords': keywords[:15],
                'technical_skills': [kw for kw in keywords if kw in [
                    'python', 'java', 'javascript', 'react', 'node.js', 'sql', 'aws', 'docker'
                ]],
                'experience_level': self._extract_experience_level(job_description),
                'job_type': self._extract_job_type(job_description)
            }
        except Exception as e:
            return {'error': str(e)}
    
    def _extract_experience_level(self, job_description: str) -> str:
        """Extract experience level from job description"""
        text_lower = job_description.lower()
        
        if any(word in text_lower for word in ['senior', 'lead', 'principal', '5+ years', '7+ years']):
            return 'Senior'
        elif any(word in text_lower for word in ['mid level', '3+ years', '2-4 years']):
            return 'Mid-level'
        elif any(word in text_lower for word in ['junior', 'entry level', 'associate', 'graduate']):
            return 'Entry-level'
        else:
            return 'Not specified'
    
    def _extract_job_type(self, job_description: str) -> str:
        """Extract job type from description"""
        text_lower = job_description.lower()
        
        job_types = []
        if 'remote' in text_lower:
            job_types.append('Remote')
        if 'hybrid' in text_lower:
            job_types.append('Hybrid')
        if 'full-time' in text_lower or 'full time' in text_lower:
            job_types.append('Full-time')
        if 'part-time' in text_lower or 'part time' in text_lower:
            job_types.append('Part-time')
        if 'contract' in text_lower:
            job_types.append('Contract')
        
        return ', '.join(job_types) if job_types else 'Not specified'
