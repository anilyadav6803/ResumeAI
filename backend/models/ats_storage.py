import json
import os
import uuid
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

class ATSResultsStorage:
    """Simple storage system for ATS optimization results"""
    
    def __init__(self, storage_path: str = "data/ats_results"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.results_file = self.storage_path / "ats_results.json"
        self._ensure_storage_exists()
    
    def _ensure_storage_exists(self):
        """Ensure storage file exists"""
        if not self.results_file.exists():
            with open(self.results_file, 'w') as f:
                json.dump([], f)
    
    def save_optimization_result(self, 
                                resume_info: Dict, 
                                job_description: str, 
                                optimization_results: Dict,
                                job_analysis: Dict = None) -> str:
        """Save ATS optimization result and return unique ID"""
        
        try:
            # Generate unique ID
            result_id = str(uuid.uuid4())
            
            # Create result record
            result_record = {
                "id": result_id,
                "timestamp": datetime.now().isoformat(),
                "resume_info": {
                    "file_name": resume_info.get("file_name", "Unknown"),
                    "name": resume_info.get("name", "Unknown"),
                    "email": resume_info.get("email", ""),
                    "word_count": resume_info.get("word_count", 0),
                    "skills_count": len(resume_info.get("skills_found", []))
                },
                "job_description": job_description[:500] + "..." if len(job_description) > 500 else job_description,
                "job_description_hash": hash(job_description),
                "optimization_results": optimization_results,
                "job_analysis": job_analysis or {},
                "status": "completed"
            }
            
            # Read existing results
            results = self._load_results()
            
            # Add new result
            results.append(result_record)
            
            # Keep only last 100 results to manage storage
            if len(results) > 100:
                results = results[-100:]
            
            # Save back to file
            with open(self.results_file, 'w') as f:
                json.dump(results, f, indent=2)
            
            print(f"✅ Saved ATS optimization result with ID: {result_id}")
            return result_id
            
        except Exception as e:
            print(f"❌ Error saving ATS optimization result: {e}")
            return None
    
    def get_optimization_result(self, result_id: str) -> Optional[Dict]:
        """Get optimization result by ID"""
        try:
            results = self._load_results()
            for result in results:
                if result.get("id") == result_id:
                    return result
            return None
        except Exception as e:
            print(f"❌ Error retrieving ATS result: {e}")
            return None
    
    def get_recent_results(self, limit: int = 10) -> List[Dict]:
        """Get recent optimization results"""
        try:
            results = self._load_results()
            # Sort by timestamp descending and limit
            sorted_results = sorted(results, key=lambda x: x.get("timestamp", ""), reverse=True)
            return sorted_results[:limit]
        except Exception as e:
            print(f"❌ Error getting recent results: {e}")
            return []
    
    def get_user_results(self, email: str, limit: int = 10) -> List[Dict]:
        """Get optimization results for a specific user by email"""
        try:
            results = self._load_results()
            user_results = [
                r for r in results 
                if r.get("resume_info", {}).get("email", "").lower() == email.lower()
            ]
            # Sort by timestamp descending
            sorted_results = sorted(user_results, key=lambda x: x.get("timestamp", ""), reverse=True)
            return sorted_results[:limit]
        except Exception as e:
            print(f"❌ Error getting user results: {e}")
            return []
    
    def get_statistics(self) -> Dict:
        """Get ATS optimization statistics"""
        try:
            results = self._load_results()
            
            if not results:
                return {
                    "total_optimizations": 0,
                    "average_ats_score": 0,
                    "common_issues": [],
                    "recent_activity": 0
                }
            
            # Calculate statistics
            total_optimizations = len(results)
            
            # Extract ATS scores
            ats_scores = []
            all_issues = []
            
            for result in results:
                opt_results = result.get("optimization_results", {})
                if "ats_score" in opt_results:
                    ats_scores.append(opt_results["ats_score"])
                
                # Collect common issues
                if "missing_keywords" in opt_results:
                    all_issues.extend(opt_results["missing_keywords"][:5])  # Top 5 issues
            
            average_ats_score = sum(ats_scores) / len(ats_scores) if ats_scores else 0
            
            # Count common issues
            issue_counts = {}
            for issue in all_issues:
                issue_counts[issue] = issue_counts.get(issue, 0) + 1
            
            common_issues = sorted(issue_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            
            # Recent activity (last 7 days)
            from datetime import datetime, timedelta
            week_ago = datetime.now() - timedelta(days=7)
            recent_activity = len([
                r for r in results 
                if datetime.fromisoformat(r.get("timestamp", "1970-01-01")) > week_ago
            ])
            
            return {
                "total_optimizations": total_optimizations,
                "average_ats_score": round(average_ats_score, 1),
                "common_issues": [{"issue": issue, "count": count} for issue, count in common_issues],
                "recent_activity": recent_activity,
                "success_rate": 100,  # All completed optimizations are successful
                "total_users": len(set(r.get("resume_info", {}).get("email", "") for r in results if r.get("resume_info", {}).get("email")))
            }
            
        except Exception as e:
            print(f"❌ Error calculating ATS statistics: {e}")
            return {
                "total_optimizations": 0,
                "average_ats_score": 0,
                "common_issues": [],
                "recent_activity": 0,
                "error": str(e)
            }
    
    def _load_results(self) -> List[Dict]:
        """Load results from storage file"""
        try:
            if self.results_file.exists():
                with open(self.results_file, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"❌ Error loading ATS results: {e}")
            return []
    
    def clear_results(self):
        """Clear all stored results (for testing/maintenance)"""
        try:
            with open(self.results_file, 'w') as f:
                json.dump([], f)
            print("✅ Cleared all ATS optimization results")
        except Exception as e:
            print(f"❌ Error clearing results: {e}")
