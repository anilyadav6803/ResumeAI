from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import os
import shutil
from pathlib import Path
import json

# Import our models
from .config import Config
from .models.resume_parser import ResumeParser
from .models.job_matcher import JobMatcher
from .models.ats_optimizer import ATSOptimizer

# Initialize FastAPI app
app = FastAPI(
    title="ResumeAI - AI Resume Optimizer & Screening Agent",
    description="An AI-powered tool for resume screening and ATS optimization",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
Config.create_directories()
resume_parser = ResumeParser()
job_matcher = JobMatcher()
ats_optimizer = ATSOptimizer()

# Global storage for processed resumes (in production, use a database)
processed_resumes = []

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to ResumeAI API",
        "version": "1.0.0",
        "features": [
            "Resume parsing and analysis",
            "AI-powered job matching",
            "ATS optimization recommendations",
            "Bulk resume processing"
        ],
        "endpoints": {
            "upload_resumes": "/upload-resumes/",
            "match_resumes": "/match-resumes/",
            "optimize_resume": "/optimize-resume/",
            "health": "/health/",
            "stats": "/stats/"
        }
    }

@app.get("/health/")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "api_version": "1.0.0",
        "total_processed_resumes": len(processed_resumes)
    }

@app.post("/upload-resumes/")
async def upload_resumes(files: List[UploadFile] = File(...)):
    """Upload and process multiple resume files"""
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded")
    
    if len(files) > 20:  # Limit to prevent abuse
        raise HTTPException(status_code=400, detail="Maximum 20 files allowed per upload")
    
    uploaded_files = []
    parsing_results = []
    
    try:
        for file in files:
            # Validate file type
            if not file.filename.lower().endswith(('.pdf', '.docx', '.txt')):
                continue
            
            # Save uploaded file
            file_path = os.path.join(Config.UPLOAD_FOLDER, file.filename)
            
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            uploaded_files.append(file_path)
        
        # Parse all uploaded resumes
        if uploaded_files:
            parsing_results = resume_parser.batch_parse_resumes(uploaded_files)
            
            # Add to global storage (replace with database in production)
            global processed_resumes
            processed_resumes.extend(parsing_results)
            
            # Create searchable index for job matching
            success = job_matcher.create_resume_index(parsing_results)
            
            # Prepare response
            successful_parses = [r for r in parsing_results if r['parsing_status'] == 'success']
            failed_parses = [r for r in parsing_results if r['parsing_status'] == 'error']
            
            return {
                "message": f"Successfully processed {len(successful_parses)} out of {len(files)} files",
                "total_uploaded": len(files),
                "successful_parses": len(successful_parses),
                "failed_parses": len(failed_parses),
                "index_created": success,
                "processed_resumes": [
                    {
                        "file_name": r['file_name'],
                        "name": r['name'],
                        "email": r['email'],
                        "skills_count": len(r['skills']),
                        "word_count": r['word_count'],
                        "status": r['parsing_status']
                    } for r in parsing_results
                ],
                "failed_files": [
                    {
                        "file_name": r['file_name'],
                        "error": r.get('error_message', 'Unknown error')
                    } for r in failed_parses
                ]
            }
        else:
            raise HTTPException(status_code=400, detail="No valid PDF, DOCX, or TXT files found")
            
    except Exception as e:
        # Clean up uploaded files on error
        for file_path in uploaded_files:
            if os.path.exists(file_path):
                os.remove(file_path)
        
        raise HTTPException(status_code=500, detail=f"Error processing files: {str(e)}")

@app.post("/match-resumes/")
async def match_resumes(job_description: str = Form(...), top_k: int = Form(3)):
    """Find resumes that best match a job description"""
    if not job_description.strip():
        raise HTTPException(status_code=400, detail="Job description cannot be empty")
    
    if not processed_resumes:
        raise HTTPException(status_code=400, detail="No resumes uploaded yet. Please upload resumes first.")
    
    if top_k < 1 or top_k > 10:
        raise HTTPException(status_code=400, detail="top_k must be between 1 and 10")
    
    try:
        # Get matching results
        matches = job_matcher.match_resumes(processed_resumes, job_description, top_k)
        
        return {
            "success": True,
            "job_description_length": len(job_description),
            "total_candidates_in_db": len(processed_resumes),
            "matches": matches,
            "total_matches": len(matches)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error matching resumes: {str(e)}")

@app.post("/optimize-resume/")
async def optimize_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    """Optimize a single resume for ATS and job description"""
    if not file.filename.lower().endswith(('.pdf', '.docx', '.txt')):
        raise HTTPException(status_code=400, detail="Only PDF, DOCX, and TXT files are supported")
    
    if not job_description.strip():
        raise HTTPException(status_code=400, detail="Job description cannot be empty")
    
    temp_file_path = None
    
    try:
        # Save uploaded file temporarily
        temp_file_path = os.path.join(Config.UPLOAD_FOLDER, f"temp_{file.filename}")
        
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Parse the resume
        parsed_resume = resume_parser.parse_resume(temp_file_path)
        
        if parsed_resume['parsing_status'] != 'success':
            raise HTTPException(
                status_code=400, 
                detail=f"Failed to parse resume: {parsed_resume.get('error_message', 'Unknown error')}"
            )
        
        # Get optimization suggestions
        optimization_results = ats_optimizer.optimize_resume(
            parsed_resume['full_text'], 
            job_description
        )
        
        # Analyze job description
        job_analysis = ats_optimizer.analyze_job_keywords(job_description)
        
        return {
            "success": True,
            "resume_info": {
                "file_name": parsed_resume['file_name'],
                "name": parsed_resume['name'],
                "email": parsed_resume['email'],
                "word_count": parsed_resume['word_count'],
                "skills_found": parsed_resume['skills']
            },
            "job_analysis": job_analysis,
            "optimization_results": optimization_results
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error optimizing resume: {str(e)}")
    
    finally:
        # Clean up temporary file
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@app.get("/stats/")
async def get_statistics():
    """Get system statistics"""
    try:
        # Get job matcher statistics
        matcher_stats = job_matcher.get_statistics()
        
        # Calculate processing statistics
        successful_resumes = [r for r in processed_resumes if r['parsing_status'] == 'success']
        failed_resumes = [r for r in processed_resumes if r['parsing_status'] == 'error']
        
        # Get skill statistics
        all_skills = []
        for resume in successful_resumes:
            all_skills.extend(resume['skills'])
        
        skill_counts = {}
        for skill in all_skills:
            skill_counts[skill] = skill_counts.get(skill, 0) + 1
        
        top_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            "total_resumes_processed": len(processed_resumes),
            "successful_parses": len(successful_resumes),
            "failed_parses": len(failed_resumes),
            "success_rate": round(len(successful_resumes) / len(processed_resumes) * 100, 2) if processed_resumes else 0,
            "vector_store_stats": matcher_stats,
            "top_skills_found": top_skills,
            "average_word_count": round(sum(r['word_count'] for r in successful_resumes) / len(successful_resumes)) if successful_resumes else 0,
            "resumes_with_email": len([r for r in successful_resumes if r['email']]),
            "resumes_with_phone": len([r for r in successful_resumes if r['phone']])
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting statistics: {str(e)}")

@app.delete("/clear-data/")
async def clear_all_data():
    """Clear all processed resumes and vector store (useful for testing)"""
    try:
        global processed_resumes
        processed_resumes.clear()
        
        # Clear vector store
        job_matcher.embedding_manager.clear_collection()
        
        # Clean up uploaded files
        if os.path.exists(Config.UPLOAD_FOLDER):
            for file in os.listdir(Config.UPLOAD_FOLDER):
                file_path = os.path.join(Config.UPLOAD_FOLDER, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        
        return {
            "message": "All data cleared successfully",
            "resumes_cleared": True,
            "vector_store_cleared": True,
            "files_cleaned": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing data: {str(e)}")

@app.get("/resume-list/")
async def get_resume_list():
    """Get list of all processed resumes"""
    try:
        resume_list = []
        for resume in processed_resumes:
            resume_list.append({
                "file_name": resume['file_name'],
                "name": resume['name'],
                "email": resume['email'],
                "phone": resume['phone'],
                "skills_count": len(resume['skills']),
                "experience_years": resume['experience_years'],
                "word_count": resume['word_count'],
                "parsing_status": resume['parsing_status']
            })
        
        return {
            "total_resumes": len(resume_list),
            "resumes": resume_list
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting resume list: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
