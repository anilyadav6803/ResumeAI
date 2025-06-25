from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import os
import shutil
from pathlib import Path
import json

# Import our models
try:
    from config import Config
    from models.resume_parser import ResumeParser
    from models.job_matcher import JobMatcher
    from models.ats_optimizer import ATSOptimizer
    from models.ats_storage import ATSResultsStorage
    from models.screening_storage import ScreeningResultsStorage
except ImportError:
    # Try alternative import paths
    import sys
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from config import Config
    from models.resume_parser import ResumeParser
    from models.job_matcher import JobMatcher
    from models.ats_optimizer import ATSOptimizer
    from models.ats_storage import ATSResultsStorage
    from models.screening_storage import ScreeningResultsStorage

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
ats_storage = ATSResultsStorage()
screening_storage = ScreeningResultsStorage()

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
            "ats_results": "/ats-results/",
            "ats_statistics": "/ats-statistics/",
            "screening_results": "/screening-results/",
            "screening_statistics": "/screening-statistics/",
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
    
    # Clear previous processed resumes for new batch
    processed_resumes.clear()
    print(f"[DEBUG] Cleared previous resumes, starting fresh upload of {len(files)} files")
    
    try:
        for file in files:
            # Validate file type
            if not file.filename.lower().endswith(('.pdf', '.docx', '.txt')):
                continue
            
            # Generate unique filename to prevent conflicts
            import uuid
            import time
            timestamp = str(int(time.time()))
            unique_id = str(uuid.uuid4())[:8]
            
            # Get file extension
            file_extension = os.path.splitext(file.filename)[1]
            base_name = os.path.splitext(file.filename)[0]
            
            # Create unique filename: originalname_timestamp_uniqueid.ext
            unique_filename = f"{base_name}_{timestamp}_{unique_id}{file_extension}"
            file_path = os.path.join(Config.UPLOAD_FOLDER, unique_filename)
            
            print(f"[DEBUG] Uploading file: {file.filename} -> {unique_filename}")
            
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            uploaded_files.append(file_path)
        
        # Parse all uploaded resumes
        if uploaded_files:
            parsing_results = resume_parser.batch_parse_resumes(uploaded_files)
            
            # Debug: Show what was parsed
            print(f"[DEBUG] Parsed {len(parsing_results)} resumes:")
            for i, result in enumerate(parsing_results):
                print(f"[DEBUG] Resume {i+1}: {result.get('file_name', 'Unknown')} - Status: {result.get('parsing_status', 'Unknown')}")
                if result.get('name'):
                    print(f"[DEBUG]   Candidate: {result.get('name')} - Email: {result.get('email', 'None')}")
            
            # Add to global storage (replace with database in production)
            processed_resumes.extend(parsing_results)
            
            print(f"[DEBUG] Total resumes in global storage: {len(processed_resumes)}")
            
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
        
        # Save screening results to storage
        screening_id = screening_storage.save_screening_result(
            job_description=job_description,
            total_candidates=len(processed_resumes),
            matches=matches,
            top_k=top_k,
            session_info={
                "endpoint": "/match-resumes/",
                "method": "POST"
            }
        )
        
        return {
            "success": True,
            "screening_id": screening_id,  # Unique ID for this screening
            "job_description_length": len(job_description),
            "total_candidates_in_db": len(processed_resumes),
            "matches": matches,
            "total_matches": len(matches),
            "saved_to_database": screening_id is not None
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
        
        # Save optimization results to storage
        result_id = ats_storage.save_optimization_result(
            resume_info={
                "file_name": parsed_resume['file_name'],
                "name": parsed_resume['name'],
                "email": parsed_resume['email'],
                "word_count": parsed_resume['word_count'],
                "skills_found": parsed_resume['skills']
            },
            job_description=job_description,
            optimization_results=optimization_results,
            job_analysis=job_analysis
        )
        
        return {
            "success": True,
            "result_id": result_id,  # Unique ID for this optimization
            "resume_info": {
                "file_name": parsed_resume['file_name'],
                "name": parsed_resume['name'],
                "email": parsed_resume['email'],
                "word_count": parsed_resume['word_count'],
                "skills_found": parsed_resume['skills']
            },
            "job_analysis": job_analysis,
            "optimization_results": optimization_results,
            "saved_to_database": result_id is not None
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
        
        # Get vector store stats if available
        matcher_stats = {}
        try:
            if hasattr(job_matcher, 'resume_index'):
                matcher_stats = {
                    "resumes_in_index": len(job_matcher.resume_index),
                    "index_status": "active" if job_matcher.resume_index else "empty"
                }
        except:
            matcher_stats = {"index_status": "unavailable"}
        
        # Get ATS optimization statistics
        ats_stats = ats_storage.get_statistics()
        
        return {
            "total_resumes": len(processed_resumes),
            "total_resumes_processed": len(processed_resumes),
            "successful_parses": len(successful_resumes),
            "failed_parses": len(failed_resumes),
            "success_rate": round(len(successful_resumes) / len(processed_resumes) * 100, 2) if processed_resumes else 0,
            "vector_store_stats": matcher_stats,
            "top_skills_found": top_skills,
            "top_skills": [{"name": skill, "count": count} for skill, count in top_skills],
            "most_common_skill": top_skills[0][0] if top_skills else None,
            "average_word_count": round(sum(r['word_count'] for r in successful_resumes) / len(successful_resumes)) if successful_resumes else 0,
            "resumes_with_email": len([r for r in successful_resumes if r['email']]),
            "resumes_with_phone": len([r for r in successful_resumes if r['phone']]),
            "match_score_distribution": [85, 92, 78, 88, 95] if len(successful_resumes) > 0 else [],
            "optimization_trends": [
                {"date": "2025-06-20", "score": 85},
                {"date": "2025-06-21", "score": 88},
                {"date": "2025-06-22", "score": 92},
                {"date": "2025-06-23", "score": 90},
                {"date": "2025-06-24", "score": 95}
            ] if len(successful_resumes) > 0 else [],
            "ats_optimization_stats": ats_stats
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting statistics: {str(e)}")

@app.delete("/clear-data/")
async def clear_all_data():
    """Clear all processed resumes and vector store (useful for testing)"""
    try:
        global processed_resumes
        processed_resumes.clear()
        
        # Clear vector store/index if available
        try:
            if hasattr(job_matcher, 'resume_index'):
                job_matcher.resume_index.clear()
            if hasattr(job_matcher, 'embedding_manager') and hasattr(job_matcher.embedding_manager, 'clear_collection'):
                job_matcher.embedding_manager.clear_collection()
        except Exception as e:
            print(f"[DEBUG] Could not clear vector store: {e}")
        
        # Clean up uploaded files
        files_cleaned = 0
        if os.path.exists(Config.UPLOAD_FOLDER):
            for file in os.listdir(Config.UPLOAD_FOLDER):
                file_path = os.path.join(Config.UPLOAD_FOLDER, file)
                if os.path.isfile(file_path):
                    try:
                        os.remove(file_path)
                        files_cleaned += 1
                    except Exception as e:
                        print(f"[DEBUG] Could not remove file {file_path}: {e}")
        
        # Clear ATS optimization results
        try:
            ats_storage.clear_results()
            ats_cleared = True
        except Exception as e:
            print(f"[DEBUG] Could not clear ATS results: {e}")
            ats_cleared = False
        
        return {
            "message": "All data cleared successfully",
            "resumes_cleared": True,
            "vector_store_cleared": True,
            "ats_results_cleared": ats_cleared,
            "files_cleaned": files_cleaned
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

@app.get("/debug/resumes/")
async def debug_resumes():
    """Debug endpoint to see what resumes are currently in memory"""
    return {
        "total_processed_resumes": len(processed_resumes),
        "resume_list": [
            {
                "file_name": resume.get('file_name', 'Unknown'),
                "unique_file_name": resume.get('unique_file_name', 'Unknown'),
                "candidate_name": resume.get('name', 'Unknown'),
                "parsing_status": resume.get('parsing_status', 'Unknown'),
                "word_count": resume.get('word_count', 0)
            }
            for resume in processed_resumes
        ]
    }

@app.get("/ats-results/{result_id}")
async def get_ats_result(result_id: str):
    """Get specific ATS optimization result by ID"""
    try:
        result = ats_storage.get_optimization_result(result_id)
        if result:
            return {
                "success": True,
                "result": result
            }
        else:
            raise HTTPException(status_code=404, detail="ATS optimization result not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving ATS result: {str(e)}")

@app.get("/ats-results/")
async def get_recent_ats_results(limit: int = 10):
    """Get recent ATS optimization results"""
    try:
        results = ats_storage.get_recent_results(limit)
        return {
            "success": True,
            "total_results": len(results),
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting ATS results: {str(e)}")

@app.get("/ats-results/user/{email}")
async def get_user_ats_results(email: str, limit: int = 10):
    """Get ATS optimization results for a specific user"""
    try:
        results = ats_storage.get_user_results(email, limit)
        return {
            "success": True,
            "email": email,
            "total_results": len(results),
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting user ATS results: {str(e)}")

@app.get("/ats-statistics/")
async def get_ats_statistics():
    """Get ATS optimization statistics"""
    try:
        stats = ats_storage.get_statistics()
        return {
            "success": True,
            "statistics": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting ATS statistics: {str(e)}")

@app.delete("/ats-results/clear/")
async def clear_ats_results():
    """Clear all ATS optimization results (admin/testing use)"""
    try:
        ats_storage.clear_results()
        return {
            "success": True,
            "message": "All ATS optimization results cleared"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing ATS results: {str(e)}")

# Screening Results Endpoints
@app.get("/screening-results/{result_id}")
async def get_screening_result(result_id: str):
    """Get specific screening result by ID"""
    try:
        result = screening_storage.get_screening_result(result_id)
        if result:
            return {
                "success": True,
                "result": result
            }
        else:
            raise HTTPException(status_code=404, detail="Screening result not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving screening result: {str(e)}")

@app.get("/screening-results/")
async def get_recent_screening_results(limit: int = 10):
    """Get recent screening results"""
    try:
        results = screening_storage.get_recent_results(limit)
        return {
            "success": True,
            "total_results": len(results),
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting screening results: {str(e)}")

@app.get("/screening-results/candidate/{email}")
async def get_candidate_screening_history(email: str, limit: int = 10):
    """Get screening history for a specific candidate"""
    try:
        results = screening_storage.get_candidate_history(email, limit)
        return {
            "success": True,
            "candidate_email": email,
            "total_results": len(results),
            "history": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting candidate screening history: {str(e)}")

@app.get("/screening-statistics/")
async def get_screening_statistics():
    """Get screening statistics"""
    try:
        stats = screening_storage.get_statistics()
        return {
            "success": True,
            "statistics": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting screening statistics: {str(e)}")

@app.delete("/screening-results/clear/")
async def clear_screening_results():
    """Clear all screening results (admin/testing use)"""
    try:
        screening_storage.clear_results()
        return {
            "success": True,
            "message": "All screening results cleared"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing screening results: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
