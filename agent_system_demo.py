#!/usr/bin/env python3
"""
ResumeAI Multi-Agent System Implementation
Demonstrates the agentic architecture with working examples
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class AgentTask:
    """Task object passed between agents"""
    task_type: str
    payload: Dict[str, Any]
    priority: int = 1
    timestamp: datetime = datetime.now()
    request_id: str = ""

@dataclass
class AgentResponse:
    """Response object from agents"""
    agent_id: str
    status: str  # success, error, partial
    data: Dict[str, Any]
    confidence: float
    processing_time: float
    timestamp: datetime = datetime.now()

class BaseAgent(ABC):
    """Base class for all agents in the system"""
    
    def __init__(self, agent_id: str, config: Dict[str, Any]):
        self.agent_id = agent_id
        self.config = config
        self.logger = logging.getLogger(f"agent.{agent_id}")
        self.status = "ready"
        
    @abstractmethod
    async def process(self, task: AgentTask) -> AgentResponse:
        """Process assigned task and return response"""
        pass
        
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """Return list of agent capabilities"""
        pass
        
    async def health_check(self) -> bool:
        """Check agent health status"""
        return self.status == "ready"

class ParserAgent(BaseAgent):
    """Agent responsible for parsing and extracting information from resumes"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__("parser", config)
        
    def get_capabilities(self) -> List[str]:
        return ["parse_resume", "extract_text", "extract_entities"]
        
    async def process(self, task: AgentTask) -> AgentResponse:
        """Parse resume and extract structured information"""
        start_time = datetime.now()
        
        try:
            if task.task_type == "parse_resume":
                # Simulate resume parsing
                resume_data = await self._parse_resume(task.payload.get("resume_text", ""))
                
                processing_time = (datetime.now() - start_time).total_seconds()
                
                return AgentResponse(
                    agent_id=self.agent_id,
                    status="success",
                    data=resume_data,
                    confidence=0.95,
                    processing_time=processing_time
                )
            else:
                raise ValueError(f"Unknown task type: {task.task_type}")
                
        except Exception as e:
            processing_time = (datetime.now() - start_time).total_seconds()
            self.logger.error(f"Parser error: {e}")
            
            return AgentResponse(
                agent_id=self.agent_id,
                status="error",
                data={"error": str(e)},
                confidence=0.0,
                processing_time=processing_time
            )
    
    async def _parse_resume(self, resume_text: str) -> Dict[str, Any]:
        """Simulate resume parsing logic"""
        # In real implementation, this would use NLP libraries
        # For demo purposes, we'll simulate parsing
        
        return {
            "candidate_name": "John Smith",
            "email": "john.smith@email.com",
            "phone": "+1-555-0123",
            "skills": ["Python", "JavaScript", "React", "AWS", "Docker"],
            "experience": [
                {
                    "company": "TechCorp Inc.",
                    "position": "Senior Software Engineer",
                    "duration": "2020-2023",
                    "description": "Led development of microservices architecture, managed team of 5 developers"
                },
                {
                    "company": "StartupXYZ",
                    "position": "Full Stack Developer", 
                    "duration": "2018-2020",
                    "description": "Developed web applications using React and Node.js"
                }
            ],
            "education": [
                {
                    "degree": "Bachelor of Science in Computer Science",
                    "university": "Tech University",
                    "year": "2018"
                }
            ],
            "years_experience": 5
        }

class MatcherAgent(BaseAgent):
    """Agent responsible for matching resumes to job descriptions"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__("matcher", config)
        
    def get_capabilities(self) -> List[str]:
        return ["match_resume", "rank_candidates", "generate_explanations"]
        
    async def process(self, task: AgentTask) -> AgentResponse:
        """Match resumes against job description and rank candidates"""
        start_time = datetime.now()
        
        try:
            if task.task_type == "match_resumes":
                results = await self._match_resumes(
                    task.payload.get("resumes", []),
                    task.payload.get("job_description", ""),
                    task.payload.get("top_k", 5)
                )
                
                processing_time = (datetime.now() - start_time).total_seconds()
                
                return AgentResponse(
                    agent_id=self.agent_id,
                    status="success",
                    data=results,
                    confidence=0.92,
                    processing_time=processing_time
                )
            else:
                raise ValueError(f"Unknown task type: {task.task_type}")
                
        except Exception as e:
            processing_time = (datetime.now() - start_time).total_seconds()
            self.logger.error(f"Matcher error: {e}")
            
            return AgentResponse(
                agent_id=self.agent_id,
                status="error",
                data={"error": str(e)},
                confidence=0.0,
                processing_time=processing_time
            )
    
    async def _match_resumes(self, resumes: List[Dict], job_description: str, top_k: int) -> Dict[str, Any]:
        """Simulate resume matching logic"""
        # In real implementation, this would use semantic similarity
        # For demo purposes, we'll simulate matching with explanations
        
        candidates = [
            {
                "rank": 1,
                "candidate_name": "Sarah Chen",
                "match_score": 94,
                "email": "sarah.chen@email.com",
                "phone": "+1-555-0456",
                "ai_explanation": "Exceptional match with 7 years of experience. Perfect technical alignment: Python (6 years), React (4 years), AWS (5 years). Led microservices migration for 50+ services and managed team of 8 developers. Strong leadership experience with proven track record in scaling applications.",
                "key_strengths": [
                    "Leadership: Managed team of 8 developers",
                    "Architecture: Led microservices migration",
                    "AWS Expertise: 5 years with multiple services",
                    "Scaling: Handled 10x traffic growth"
                ],
                "skills_match": {
                    "Python": {"required": True, "candidate_has": True, "years": 6},
                    "React": {"required": True, "candidate_has": True, "years": 4},
                    "AWS": {"required": True, "candidate_has": True, "years": 5},
                    "Docker": {"required": True, "candidate_has": True, "years": 3}
                },
                "recommendation": "STRONG HIRE - Exceeds all requirements and brings leadership experience"
            },
            {
                "rank": 2,
                "candidate_name": "Michael Rodriguez",
                "match_score": 87,
                "email": "michael.rodriguez@email.com",
                "phone": "+1-555-0789",
                "ai_explanation": "Strong technical match with 6 years of experience. Solid Python/React/AWS foundation. Missing explicit leadership experience but demonstrates collaborative skills and mentoring. Recent experience with containerization and CI/CD pipelines.",
                "key_strengths": [
                    "Technical Skills: Strong Python and React expertise",
                    "DevOps: Docker and Kubernetes experience",
                    "Mentoring: Guided junior developers",
                    "Innovation: Implemented automated testing"
                ],
                "skills_match": {
                    "Python": {"required": True, "candidate_has": True, "years": 5},
                    "React": {"required": True, "candidate_has": True, "years": 3},
                    "AWS": {"required": True, "candidate_has": True, "years": 4},
                    "Docker": {"required": True, "candidate_has": True, "years": 2}
                },
                "recommendation": "GOOD HIRE - Solid technical contributor with growth potential"
            },
            {
                "rank": 3,
                "candidate_name": "Emily Johnson",
                "match_score": 82,
                "email": "emily.johnson@email.com",
                "phone": "+1-555-0321",
                "ai_explanation": "Good technical match with 4 years of experience. Strong React and frontend expertise. AWS experience is more limited but shows learning ability. Excellent communication skills and cross-functional collaboration.",
                "key_strengths": [
                    "Frontend: Expert-level React and JavaScript",
                    "UX Focus: User-centered design approach",
                    "Communication: Strong stakeholder management",
                    "Learning: Quick to adapt to new technologies"
                ],
                "skills_match": {
                    "Python": {"required": True, "candidate_has": True, "years": 2},
                    "React": {"required": True, "candidate_has": True, "years": 4},
                    "AWS": {"required": True, "candidate_has": True, "years": 1},
                    "Docker": {"required": True, "candidate_has": False, "years": 0}
                },
                "recommendation": "CONSIDER - Strong frontend skills, may need backend development"
            },
            {
                "rank": 4,
                "candidate_name": "David Kim",
                "match_score": 78,
                "email": "david.kim@email.com",
                "phone": "+1-555-0654",
                "ai_explanation": "Decent technical match with 3 years of experience. Good Python foundation but limited React experience. Strong backend and database skills. Would benefit from frontend development training.",
                "key_strengths": [
                    "Backend: Strong Python and database expertise",
                    "Performance: Optimized database queries",
                    "Problem Solving: Analytical approach",
                    "APIs: RESTful and GraphQL experience"
                ],
                "skills_match": {
                    "Python": {"required": True, "candidate_has": True, "years": 3},
                    "React": {"required": True, "candidate_has": True, "years": 1},
                    "AWS": {"required": True, "candidate_has": True, "years": 2},
                    "Docker": {"required": True, "candidate_has": True, "years": 1}
                },
                "recommendation": "MAYBE - Strong backend skills, needs frontend development"
            },
            {
                "rank": 5,
                "candidate_name": "Lisa Wang",
                "match_score": 71,
                "email": "lisa.wang@email.com",
                "phone": "+1-555-0987",
                "ai_explanation": "Moderate match with 2 years of experience. Recent graduate with strong academic background. Good Python skills but limited professional experience. Shows potential but may need mentoring.",
                "key_strengths": [
                    "Education: CS degree with honors",
                    "Algorithms: Strong problem-solving skills",
                    "Enthusiasm: Eager to learn and grow",
                    "Projects: Impressive personal projects"
                ],
                "skills_match": {
                    "Python": {"required": True, "candidate_has": True, "years": 2},
                    "React": {"required": True, "candidate_has": True, "years": 1},
                    "AWS": {"required": True, "candidate_has": False, "years": 0},
                    "Docker": {"required": True, "candidate_has": False, "years": 0}
                },
                "recommendation": "JUNIOR HIRE - High potential but needs experience and mentoring"
            }
        ]
        
        return {
            "total_candidates": len(candidates),
            "job_requirements": {
                "position": "Senior Software Engineer",
                "required_skills": ["Python", "React", "AWS", "Docker"],
                "experience_required": "5+ years",
                "team_size": "8 developers"
            },
            "ranked_candidates": candidates[:top_k],
            "matching_summary": {
                "avg_match_score": sum(c["match_score"] for c in candidates) / len(candidates),
                "strong_matches": len([c for c in candidates if c["match_score"] >= 85]),
                "good_matches": len([c for c in candidates if 75 <= c["match_score"] < 85]),
                "weak_matches": len([c for c in candidates if c["match_score"] < 75])
            }
        }

class OptimizerAgent(BaseAgent):
    """Agent responsible for ATS optimization and recommendations"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__("optimizer", config)
        
    def get_capabilities(self) -> List[str]:
        return ["optimize_resume", "analyze_ats", "generate_recommendations"]
        
    async def process(self, task: AgentTask) -> AgentResponse:
        """Optimize resume for ATS compatibility"""
        start_time = datetime.now()
        
        try:
            if task.task_type == "optimize_resume":
                optimization = await self._optimize_resume(
                    task.payload.get("resume_data", {}),
                    task.payload.get("job_description", "")
                )
                
                processing_time = (datetime.now() - start_time).total_seconds()
                
                return AgentResponse(
                    agent_id=self.agent_id,
                    status="success",
                    data=optimization,
                    confidence=0.88,
                    processing_time=processing_time
                )
            else:
                raise ValueError(f"Unknown task type: {task.task_type}")
                
        except Exception as e:
            processing_time = (datetime.now() - start_time).total_seconds()
            self.logger.error(f"Optimizer error: {e}")
            
            return AgentResponse(
                agent_id=self.agent_id,
                status="error",
                data={"error": str(e)},
                confidence=0.0,
                processing_time=processing_time
            )
    
    async def _optimize_resume(self, resume_data: Dict, job_description: str) -> Dict[str, Any]:
        """Simulate ATS optimization logic"""
        
        return {
            "ats_score": 78,
            "compatibility_analysis": {
                "format_score": 85,
                "keyword_score": 72,
                "structure_score": 80,
                "readability_score": 75
            },
            "missing_keywords": [
                "Docker containerization",
                "Kubernetes orchestration", 
                "CI/CD pipelines",
                "Microservices architecture",
                "Agile methodology"
            ],
            "keyword_recommendations": [
                {
                    "keyword": "Docker",
                    "suggestion": "Add 'Docker containerization' to your skills section",
                    "importance": "high",
                    "context": "Mentioned 3 times in job description"
                },
                {
                    "keyword": "Kubernetes",
                    "suggestion": "Include 'Kubernetes orchestration' experience if applicable",
                    "importance": "medium",
                    "context": "Required for container management"
                }
            ],
            "content_improvements": [
                {
                    "section": "Experience",
                    "current": "Developed web applications",
                    "improved": "Developed scalable web applications serving 100k+ users using React and Node.js",
                    "reason": "Quantify impact and add specific technologies"
                },
                {
                    "section": "Skills",
                    "current": "Python, JavaScript",
                    "improved": "Python (5+ years), JavaScript/React (4+ years), AWS (3+ years)",
                    "reason": "Include years of experience for each skill"
                }
            ],
            "formatting_suggestions": [
                "Use standard section headers (Experience, Education, Skills)",
                "Remove graphics and images for better ATS parsing",
                "Use bullet points for experience descriptions",
                "Ensure consistent date formatting (YYYY-MM)",
                "Use standard fonts (Arial, Calibri, Times New Roman)"
            ],
            "action_items": [
                {
                    "priority": "high",
                    "action": "Add Docker and Kubernetes experience to skills section",
                    "impact": "Could increase ATS score by 10-15 points"
                },
                {
                    "priority": "medium", 
                    "action": "Quantify achievements with specific metrics",
                    "impact": "Improves relevance and impact scoring"
                },
                {
                    "priority": "low",
                    "action": "Standardize date formatting across all sections",
                    "impact": "Improves ATS parsing accuracy"
                }
            ]
        }

class CoordinatorAgent(BaseAgent):
    """Main coordinator agent that orchestrates other agents"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__("coordinator", config)
        
        # Initialize specialist agents
        self.agents = {
            "parser": ParserAgent(config.get("parser", {})),
            "matcher": MatcherAgent(config.get("matcher", {})),
            "optimizer": OptimizerAgent(config.get("optimizer", {}))
        }
        
    def get_capabilities(self) -> List[str]:
        return ["coordinate_workflow", "screen_resumes", "optimize_resumes"]
        
    async def process(self, task: AgentTask) -> AgentResponse:
        """Coordinate multi-agent workflows"""
        start_time = datetime.now()
        
        try:
            if task.task_type == "screen_resumes":
                result = await self._screen_resumes_workflow(task.payload)
            elif task.task_type == "optimize_resume":
                result = await self._optimize_resume_workflow(task.payload)
            else:
                raise ValueError(f"Unknown task type: {task.task_type}")
                
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return AgentResponse(
                agent_id=self.agent_id,
                status="success",
                data=result,
                confidence=0.95,
                processing_time=processing_time
            )
            
        except Exception as e:
            processing_time = (datetime.now() - start_time).total_seconds()
            self.logger.error(f"Coordinator error: {e}")
            
            return AgentResponse(
                agent_id=self.agent_id,
                status="error",
                data={"error": str(e)},
                confidence=0.0,
                processing_time=processing_time
            )
    
    async def _screen_resumes_workflow(self, payload: Dict) -> Dict[str, Any]:
        """Orchestrate resume screening workflow"""
        
        # Step 1: Parse resumes (simulated)
        self.logger.info("Step 1: Parsing resumes...")
        parse_task = AgentTask("parse_resume", {"resume_text": "sample resume"})
        parse_response = await self.agents["parser"].process(parse_task)
        
        if parse_response.status != "success":
            raise Exception("Resume parsing failed")
            
        # Step 2: Match resumes against job description
        self.logger.info("Step 2: Matching resumes...")
        match_task = AgentTask("match_resumes", {
            "resumes": [parse_response.data],
            "job_description": payload.get("job_description", ""),
            "top_k": payload.get("top_k", 5)
        })
        match_response = await self.agents["matcher"].process(match_task)
        
        if match_response.status != "success":
            raise Exception("Resume matching failed")
            
        # Step 3: Compile final results
        self.logger.info("Step 3: Compiling results...")
        return {
            "workflow_type": "resume_screening",
            "status": "completed",
            "results": match_response.data,
            "processing_stats": {
                "parse_time": parse_response.processing_time,
                "match_time": match_response.processing_time,
                "total_agents_used": 2
            }
        }
    
    async def _optimize_resume_workflow(self, payload: Dict) -> Dict[str, Any]:
        """Orchestrate resume optimization workflow"""
        
        # Step 1: Parse resume
        self.logger.info("Step 1: Parsing resume...")
        parse_task = AgentTask("parse_resume", {"resume_text": payload.get("resume_text", "")})
        parse_response = await self.agents["parser"].process(parse_task)
        
        if parse_response.status != "success":
            raise Exception("Resume parsing failed")
            
        # Step 2: Optimize for ATS
        self.logger.info("Step 2: Optimizing resume...")
        optimize_task = AgentTask("optimize_resume", {
            "resume_data": parse_response.data,
            "job_description": payload.get("job_description", "")
        })
        optimize_response = await self.agents["optimizer"].process(optimize_task)
        
        if optimize_response.status != "success":
            raise Exception("Resume optimization failed")
            
        # Step 3: Compile final results
        self.logger.info("Step 3: Compiling optimization results...")
        return {
            "workflow_type": "resume_optimization",
            "status": "completed",
            "parsed_resume": parse_response.data,
            "optimization_results": optimize_response.data,
            "processing_stats": {
                "parse_time": parse_response.processing_time,
                "optimize_time": optimize_response.processing_time,
                "total_agents_used": 2
            }
        }

# Example usage and demonstration
async def main():
    """Demonstrate the multi-agent system in action"""
    
    print("🤖 ResumeAI Multi-Agent System Demo")
    print("=" * 50)
    
    # Initialize coordinator
    config = {
        "parser": {"model": "spacy"},
        "matcher": {"embedding_model": "sentence-transformers"},
        "optimizer": {"ats_rules": "standard"}
    }
    
    coordinator = CoordinatorAgent(config)
    
    # Demo 1: Resume Screening
    print("\n📋 Demo 1: Resume Screening Workflow")
    print("-" * 30)
    
    screening_task = AgentTask("screen_resumes", {
        "job_description": """
        Senior Software Engineer position requiring:
        - 5+ years of experience with Python
        - 3+ years of React experience
        - AWS cloud experience
        - Docker containerization
        - Team leadership experience
        """,
        "top_k": 3
    })
    
    screening_result = await coordinator.process(screening_task)
    
    if screening_result.status == "success":
        print("✅ Screening completed successfully!")
        print(f"📊 Processing time: {screening_result.processing_time:.2f}s")
        print(f"🔍 Found {len(screening_result.data['results']['ranked_candidates'])} top candidates")
        
        # Display top candidate
        top_candidate = screening_result.data['results']['ranked_candidates'][0]
        print(f"\n🥇 Top Candidate: {top_candidate['candidate_name']}")
        print(f"📈 Match Score: {top_candidate['match_score']}/100")
        print(f"💡 AI Explanation: {top_candidate['ai_explanation']}")
        
    # Demo 2: Resume Optimization
    print("\n⚡ Demo 2: Resume Optimization Workflow")
    print("-" * 30)
    
    optimization_task = AgentTask("optimize_resume", {
        "resume_text": "Sample resume text here...",
        "job_description": """
        Looking for a Full Stack Developer with:
        - React and Node.js experience
        - AWS deployment experience
        - Docker containerization
        - Agile development methodology
        """
    })
    
    optimization_result = await coordinator.process(optimization_task)
    
    if optimization_result.status == "success":
        print("✅ Optimization completed successfully!")
        print(f"📊 Processing time: {optimization_result.processing_time:.2f}s")
        
        opt_data = optimization_result.data['optimization_results']
        print(f"🎯 ATS Score: {opt_data['ats_score']}/100")
        print(f"📝 Missing Keywords: {', '.join(opt_data['missing_keywords'][:3])}")
        print(f"💡 Top Recommendation: {opt_data['action_items'][0]['action']}")
    
    print("\n🎉 Multi-Agent System Demo Complete!")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(main())
