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
                'missing_keywords': missing_keywords[:15],  # Show top 15 missing keywords
                'keyword_optimization': {
                    'add_keywords': missing_keywords[:8],  # Top 8 to add
                    'improve_sections': ['Skills', 'Experience', 'Summary', 'Education']
                },
                'format_improvements': self._get_format_suggestions(resume_text),
                'content_suggestions': self._get_content_suggestions(resume_text, job_description),
                'skills_gap': missing_keywords[:10],  # Top 10 skills gap
                'strengths': list(set(job_keywords) & set(resume_keywords))[:8],  # Top 8 strengths
                'action_items': self._generate_action_items(missing_keywords, resume_text),
                'total_job_keywords': len(job_keywords),
                'total_resume_keywords': len(resume_keywords),
                'match_percentage': round((len(job_keywords) - len(missing_keywords)) / len(job_keywords) * 100, 1) if job_keywords else 0
            }
            
        except Exception as e:
            return {
                'error': f'Basic optimization failed: {str(e)}',
                'ats_score': 0,
                'missing_keywords': [],
                'recommendations': 'Please check your resume format and try again.'            }

    def _extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords from text using comprehensive analysis for ALL departments"""
        # Comprehensive keywords pool organized by department and category
        keywords_pool = {
            # TECHNOLOGY & ENGINEERING
            'programming_languages': [
                'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'php', 'ruby', 'go', 
                'rust', 'kotlin', 'swift', 'r', 'matlab', 'scala', 'perl', 'shell', 'bash',
                'powershell', 'lua', 'dart', 'elixir', 'clojure', 'haskell', 'f#', 'cobol', 'fortran'
            ],
            'web_technologies': [
                'html', 'css', 'react', 'angular', 'vue', 'node.js', 'express', 'next.js', 
                'nuxt.js', 'gatsby', 'svelte', 'bootstrap', 'tailwind', 'sass', 'less', 
                'webpack', 'vite', 'parcel', 'rollup', 'jquery', 'backbone.js', 'ember.js',
                'react native', 'flutter', 'ionic', 'cordova', 'phonegap', 'xamarin'
            ],
            'databases': [
                'mysql', 'postgresql', 'mongodb', 'redis', 'sqlite', 'oracle', 'sql server',
                'cassandra', 'dynamodb', 'elasticsearch', 'neo4j', 'firebase', 'supabase',
                'mariadb', 'couchdb', 'influxdb', 'clickhouse', 'bigquery', 'snowflake'
            ],
            'frameworks_libraries': [
                'django', 'flask', 'fastapi', 'spring', 'spring boot', 'laravel', 'rails',
                'express.js', 'nest.js', 'asp.net', 'xamarin', '.net', 'entity framework',
                'hibernate', 'struts', 'play framework', 'symfony', 'codeigniter', 'yii'
            ],
            'cloud_devops': [
                'aws', 'azure', 'gcp', 'google cloud', 'docker', 'kubernetes', 'jenkins', 
                'gitlab ci', 'github actions', 'terraform', 'ansible', 'chef', 'puppet', 
                'vagrant', 'nginx', 'apache', 'linux', 'ubuntu', 'centos', 'redhat',
                'heroku', 'digitalocean', 'cloudflare', 'lambda', 'ec2', 's3', 'rds'
            ],
            'data_science_ai': [
                'machine learning', 'deep learning', 'artificial intelligence', 'data science',
                'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'keras',
                'matplotlib', 'seaborn', 'plotly', 'jupyter', 'anaconda', 'spark', 'hadoop',
                'tableau', 'power bi', 'looker', 'qlik', 'nlp', 'computer vision', 'opencv',
                'neural networks', 'lstm', 'cnn', 'transformers', 'bert', 'gpt'
            ],
            
            # MARKETING & DIGITAL MARKETING
            'digital_marketing': [
                'seo', 'sem', 'ppc', 'google ads', 'facebook ads', 'instagram marketing',
                'linkedin marketing', 'twitter marketing', 'youtube marketing', 'tiktok marketing',
                'content marketing', 'email marketing', 'affiliate marketing', 'influencer marketing',
                'social media marketing', 'growth hacking', 'conversion optimization', 'cro'
            ],
            'marketing_tools': [
                'google analytics', 'google tag manager', 'hubspot', 'salesforce marketing cloud',
                'mailchimp', 'constant contact', 'hootsuite', 'buffer', 'sprout social',
                'canva', 'adobe creative suite', 'photoshop', 'illustrator', 'indesign',
                'figma', 'sketch', 'wordpress', 'shopify', 'magento', 'woocommerce'
            ],
            'marketing_metrics': [
                'cpa', 'cpc', 'cpm', 'ctr', 'roi', 'roas', 'ltv', 'cac', 'conversion rate',
                'bounce rate', 'engagement rate', 'impressions', 'reach', 'frequency',
                'organic traffic', 'paid traffic', 'lead generation', 'lead nurturing'
            ],
            
            # SALES & BUSINESS DEVELOPMENT
            'sales_skills': [
                'prospecting', 'lead qualification', 'cold calling', 'cold emailing',
                'relationship building', 'account management', 'territory management',
                'pipeline management', 'forecasting', 'negotiation', 'closing deals',
                'upselling', 'cross-selling', 'customer retention', 'b2b sales', 'b2c sales'
            ],
            'sales_tools': [
                'salesforce', 'hubspot crm', 'pipedrive', 'zoho crm', 'freshsales',
                'outreach.io', 'salesloft', 'linkedin sales navigator', 'zoominfo',
                'apollo.io', 'clearbit', 'gong', 'chorus', 'calendly', 'docusign'
            ],
            
            # FINANCE & ACCOUNTING
            'finance_skills': [
                'financial analysis', 'budgeting', 'forecasting', 'financial modeling',
                'variance analysis', 'cost accounting', 'management accounting', 'tax accounting',
                'audit', 'compliance', 'risk management', 'investment analysis', 'valuation',
                'cash flow management', 'accounts payable', 'accounts receivable', 'payroll'
            ],
            'finance_tools': [
                'excel', 'quickbooks', 'sap', 'oracle financials', 'netsuite', 'xero',
                'sage', 'peachtree', 'bloomberg terminal', 'refinitiv', 'factset',
                'tableau', 'power bi', 'sql', 'python', 'r', 'vba', 'pivot tables'
            ],
            'finance_certifications': [
                'cpa', 'cfa', 'frm', 'cma', 'cia', 'acca', 'cfp', 'pmp', 'six sigma'
            ],
            
            # HUMAN RESOURCES
            'hr_skills': [
                'recruitment', 'talent acquisition', 'interviewing', 'onboarding',
                'performance management', 'employee relations', 'compensation', 'benefits',
                'training and development', 'succession planning', 'diversity and inclusion',
                'employee engagement', 'hr analytics', 'change management', 'conflict resolution'
            ],
            'hr_tools': [
                'workday', 'successfactors', 'bamboohr', 'adp', 'paychex', 'greenhouse',
                'lever', 'indeed', 'linkedin recruiter', 'glassdoor', 'ziprecruiter',
                'applicant tracking system', 'ats', 'hris', 'hrms', 'payroll systems'
            ],
            'hr_certifications': [
                'phr', 'sphr', 'shrm-cp', 'shrm-scp', 'hrci', 'cipd', 'chrp'
            ],
            
            # OPERATIONS & SUPPLY CHAIN
            'operations_skills': [
                'process improvement', 'lean manufacturing', 'six sigma', 'kaizen',
                'supply chain management', 'logistics', 'inventory management', 'procurement',
                'vendor management', 'quality assurance', 'quality control', 'production planning',
                'capacity planning', 'demand forecasting', 'warehouse management'
            ],
            'operations_tools': [
                'erp systems', 'sap', 'oracle', 'microsoft dynamics', 'netsuite',
                'tableau', 'power bi', 'minitab', 'jmp', 'arena simulation',
                'autocad', 'solidworks', 'catia', 'ansys', 'matlab', 'r', 'python'
            ],
            
            # CUSTOMER SERVICE & SUPPORT
            'customer_service': [
                'customer support', 'technical support', 'help desk', 'call center',
                'live chat', 'email support', 'ticket management', 'escalation handling',
                'customer satisfaction', 'customer retention', 'complaint resolution',
                'service level agreements', 'sla', 'first call resolution', 'fcr'
            ],
            'customer_service_tools': [
                'zendesk', 'freshdesk', 'servicenow', 'jira service desk', 'salesforce service cloud',
                'intercom', 'drift', 'livechat', 'helpscout', 'kayako', 'desk.com'
            ],
            
            # HEALTHCARE & MEDICAL
            'healthcare_skills': [
                'patient care', 'clinical assessment', 'medical records', 'emr', 'ehr',
                'healthcare compliance', 'hipaa', 'medical coding', 'icd-10', 'cpt codes',
                'medical billing', 'insurance claims', 'patient education', 'care coordination',
                'quality improvement', 'infection control', 'medication administration'
            ],
            'medical_specialties': [
                'nursing', 'physician', 'surgeon', 'cardiologist', 'neurologist', 'oncologist',
                'pediatrician', 'psychiatrist', 'radiologist', 'anesthesiologist', 'pharmacist',
                'physical therapy', 'occupational therapy', 'respiratory therapy', 'laboratory'
            ],
            
            # LEGAL
            'legal_skills': [
                'legal research', 'contract drafting', 'contract negotiation', 'litigation',
                'corporate law', 'intellectual property', 'employment law', 'real estate law',
                'tax law', 'criminal law', 'family law', 'immigration law', 'compliance',
                'regulatory affairs', 'due diligence', 'legal writing', 'brief writing'
            ],
            'legal_tools': [
                'westlaw', 'lexisnexis', 'bloomberg law', 'practical law', 'clio',
                'mycase', 'practice panther', 'timeslips', 'billing software', 'document management'
            ],
            
            # EDUCATION & TRAINING
            'education_skills': [
                'curriculum development', 'lesson planning', 'classroom management',
                'student assessment', 'educational technology', 'e-learning', 'lms',
                'instructional design', 'training delivery', 'adult learning', 'pedagogy',
                'differentiated instruction', 'special needs education', 'esl', 'tutoring'
            ],
            'education_tools': [
                'moodle', 'blackboard', 'canvas', 'google classroom', 'zoom', 'teams',
                'articulate storyline', 'captivate', 'camtasia', 'loom', 'kahoot', 'quizlet'
            ],
            
            # CONSTRUCTION & ENGINEERING
            'construction_skills': [
                'project management', 'construction management', 'site supervision',
                'building codes', 'safety regulations', 'osha', 'blueprint reading',
                'cost estimation', 'scheduling', 'quality control', 'subcontractor management',
                'materials management', 'structural engineering', 'civil engineering'
            ],
            'construction_tools': [
                'autocad', 'revit', 'sketchup', 'primavera', 'ms project', 'procore',
                'planswift', 'bluebeam', 'sage construction', 'viewpoint', 'buildertrend'
            ],
            
            # RETAIL & E-COMMERCE
            'retail_skills': [
                'merchandising', 'inventory management', 'pos systems', 'customer service',
                'sales techniques', 'visual merchandising', 'loss prevention', 'cash handling',
                'product knowledge', 'upselling', 'cross-selling', 'store operations',
                'e-commerce', 'online retail', 'marketplace management', 'dropshipping'
            ],
            'retail_tools': [
                'shopify', 'magento', 'woocommerce', 'bigcommerce', 'square', 'clover',
                'lightspeed', 'netsuite', 'amazon seller central', 'ebay', 'etsy', 'walmart marketplace'
            ],
            
            # HOSPITALITY & FOOD SERVICE
            'hospitality_skills': [
                'guest services', 'hotel management', 'front desk operations', 'housekeeping',
                'food and beverage', 'restaurant management', 'event planning', 'catering',
                'revenue management', 'hospitality technology', 'customer experience',
                'food safety', 'servsafe', 'wine knowledge', 'bartending', 'culinary arts'
            ],
            
            # GENERAL BUSINESS & SOFT SKILLS
            'business_skills': [
                'project management', 'strategic planning', 'business analysis', 'process improvement',
                'change management', 'stakeholder management', 'vendor management', 'budget management',
                'performance metrics', 'kpi', 'dashboard creation', 'reporting', 'presentations',
                'business development', 'partnership development', 'market research', 'competitive analysis'
            ],
            'soft_skills': [
                'leadership', 'communication', 'teamwork', 'collaboration', 'problem solving', 
                'critical thinking', 'analytical thinking', 'creativity', 'innovation', 'adaptability',
                'flexibility', 'time management', 'organization', 'attention to detail',
                'customer focus', 'results oriented', 'self motivated', 'initiative',
                'mentoring', 'coaching', 'training', 'presentation skills', 'public speaking',
                'negotiation', 'conflict resolution', 'decision making', 'strategic thinking'
            ],
            'certifications_general': [
                'pmp', 'agile', 'scrum master', 'six sigma', 'lean', 'itil', 'prince2',
                'microsoft certified', 'google certified', 'aws certified', 'azure certified',
                'salesforce certified', 'hubspot certified', 'google analytics certified'
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
            r'\b(senior|junior|lead|principal|staff|architect|manager|director|vp|chief)\s+\w+',
            r'\b\d+\+?\s*years?\s*(?:of\s*)?(?:experience|exp)\b',
            r'\b(?:bachelor|master|phd|mba|degree|certification|diploma)\s*\w*',
            r'\b(?:full.?stack|front.?end|back.?end|full.?time|part.?time|remote|hybrid)\b',
            r'\b(?:entry.?level|mid.?level|senior.?level|executive.?level)\b',
            r'\b(?:bilingual|multilingual|fluent|native|proficient)\b',
            r'\b(?:cpa|cfa|pmp|mba|phd|md|jd|pe|rn|cna|lpn)\b'
        ]
        
        for pattern in additional_patterns:
            matches = re.findall(pattern, text_lower)
            found_keywords.extend(matches)
        
        # Remove duplicates and sort by frequency in text
        keyword_counts = {}
        for kw in found_keywords:
            kw_clean = kw.strip().lower()
            if kw_clean and len(kw_clean) > 1:  # Avoid single characters
                keyword_counts[kw_clean] = keyword_counts.get(kw_clean, 0) + 1
        
        # Return keywords sorted by frequency (most frequent first)
        sorted_keywords = sorted(keyword_counts.keys(), key=lambda x: keyword_counts[x], reverse=True)
        
        return sorted_keywords[:50]  # Return top 50 keywords (increased from 30)
    
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
