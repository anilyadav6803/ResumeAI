import json
import os
import uuid
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

class ScreeningResultsStorage:
    """Storage system for resume screening/matching results"""
    
    def __init__(self, storage_path: str = "data/screening_results"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.results_file = self.storage_path / "screening_results.json"
        self._ensure_storage_exists()
    
    def _ensure_storage_exists(self):
        """Ensure storage file exists"""
        if not self.results_file.exists():
            with open(self.results_file, 'w') as f:
                json.dump([], f)
    
    def save_screening_result(self, 
                            job_description: str,
                            total_candidates: int,
                            matches: List[Dict],
                            top_k: int,
                            session_info: Dict = None) -> str:
        """Save resume screening result and return unique ID"""
        
        try:
            # Generate unique ID
            result_id = str(uuid.uuid4())
            
            # Create result record
            result_record = {
                "id": result_id,
                "timestamp": datetime.now().isoformat(),
                "job_description": job_description[:500] + "..." if len(job_description) > 500 else job_description,
                "job_description_hash": hash(job_description),
                "total_candidates": total_candidates,
                "requested_matches": top_k,
                "actual_matches": len(matches),
                "matches": [
                    {
                        "candidate_name": match.get("candidate_info", {}).get("name", "Unknown"),
                        "candidate_email": match.get("candidate_info", {}).get("email", ""),
                        "file_name": match.get("file_name", "Unknown"),
                        "score": match.get("score", 0),
                        "similarity_score": match.get("similarity_score", 0),
                        "keyword_match_ratio": match.get("keyword_match_ratio", 0),
                        "matched_keywords": match.get("matched_keywords", [])[:10],  # Top 10 keywords
                        "skills_count": match.get("candidate_info", {}).get("skills_count", 0),
                        "experience_years": match.get("candidate_info", {}).get("experience_years", 0)
                    }
                    for match in matches
                ],
                "session_info": session_info or {},
                "status": "completed"
            }
            
            # Read existing results
            results = self._load_results()
            
            # Add new result
            results.append(result_record)
            
            # Keep only last 50 screening results to manage storage
            if len(results) > 50:
                results = results[-50:]
            
            # Save back to file
            with open(self.results_file, 'w') as f:
                json.dump(results, f, indent=2)
            
            print(f"✅ Saved screening result with ID: {result_id}")
            return result_id
            
        except Exception as e:
            print(f"❌ Error saving screening result: {e}")
            return None
    
    def get_screening_result(self, result_id: str) -> Optional[Dict]:
        """Get screening result by ID"""
        try:
            results = self._load_results()
            for result in results:
                if result.get("id") == result_id:
                    return result
            return None
        except Exception as e:
            print(f"❌ Error retrieving screening result: {e}")
            return None
    
    def get_recent_results(self, limit: int = 10) -> List[Dict]:
        """Get recent screening results"""
        try:
            results = self._load_results()
            # Sort by timestamp descending and limit
            sorted_results = sorted(results, key=lambda x: x.get("timestamp", ""), reverse=True)
            return sorted_results[:limit]
        except Exception as e:
            print(f"❌ Error getting recent screening results: {e}")
            return []
    
    def get_results_by_job_hash(self, job_hash: int, limit: int = 5) -> List[Dict]:
        """Get screening results for similar job descriptions"""
        try:
            results = self._load_results()
            matching_results = [
                r for r in results 
                if r.get("job_description_hash") == job_hash
            ]
            # Sort by timestamp descending
            sorted_results = sorted(matching_results, key=lambda x: x.get("timestamp", ""), reverse=True)
            return sorted_results[:limit]
        except Exception as e:
            print(f"❌ Error getting results by job hash: {e}")
            return []
    
    def get_candidate_history(self, candidate_email: str, limit: int = 10) -> List[Dict]:
        """Get screening history for a specific candidate"""
        try:
            results = self._load_results()
            candidate_results = []
            
            for result in results:
                for match in result.get("matches", []):
                    if match.get("candidate_email", "").lower() == candidate_email.lower():
                        candidate_results.append({
                            "screening_id": result.get("id"),
                            "timestamp": result.get("timestamp"),
                            "job_description": result.get("job_description", "")[:200] + "...",
                            "score": match.get("score", 0),
                            "similarity_score": match.get("similarity_score", 0),
                            "keyword_match_ratio": match.get("keyword_match_ratio", 0),
                            "matched_keywords": match.get("matched_keywords", [])
                        })
            
            # Sort by timestamp descending
            sorted_results = sorted(candidate_results, key=lambda x: x.get("timestamp", ""), reverse=True)
            return sorted_results[:limit]
        except Exception as e:
            print(f"❌ Error getting candidate history: {e}")
            return []
    
    def get_statistics(self) -> Dict:
        """Get screening statistics"""
        try:
            results = self._load_results()
            
            if not results:
                return {
                    "total_screenings": 0,
                    "total_candidates_screened": 0,
                    "average_matches_per_screening": 0,
                    "top_candidates": [],
                    "recent_activity": 0
                }
            
            # Calculate statistics
            total_screenings = len(results)
            total_candidates = sum(r.get("total_candidates", 0) for r in results)
            total_matches = sum(r.get("actual_matches", 0) for r in results)
            
            # Calculate averages
            avg_matches = total_matches / total_screenings if total_screenings > 0 else 0
            avg_candidates_per_screening = total_candidates / total_screenings if total_screenings > 0 else 0
            
            # Get top performing candidates
            all_candidates = []
            for result in results:
                for match in result.get("matches", []):
                    all_candidates.append({
                        "name": match.get("candidate_name", "Unknown"),
                        "email": match.get("candidate_email", ""),
                        "average_score": match.get("score", 0),
                        "times_matched": 1
                    })
            
            # Aggregate candidate performance
            candidate_performance = {}
            for candidate in all_candidates:
                email = candidate["email"]
                if email in candidate_performance:
                    candidate_performance[email]["total_score"] += candidate["average_score"]
                    candidate_performance[email]["times_matched"] += 1
                else:
                    candidate_performance[email] = {
                        "name": candidate["name"],
                        "email": email,
                        "total_score": candidate["average_score"],
                        "times_matched": 1
                    }
            
            # Calculate average scores and sort
            top_candidates = []
            for email, data in candidate_performance.items():
                avg_score = data["total_score"] / data["times_matched"]
                top_candidates.append({
                    "name": data["name"],
                    "email": email,
                    "average_score": round(avg_score, 2),
                    "times_matched": data["times_matched"]
                })
            
            top_candidates = sorted(top_candidates, key=lambda x: x["average_score"], reverse=True)[:10]
            
            # Recent activity (last 7 days)
            from datetime import datetime, timedelta
            week_ago = datetime.now() - timedelta(days=7)
            recent_activity = len([
                r for r in results 
                if datetime.fromisoformat(r.get("timestamp", "1970-01-01")) > week_ago
            ])
            
            return {
                "total_screenings": total_screenings,
                "total_candidates_screened": total_candidates,
                "average_matches_per_screening": round(avg_matches, 1),
                "average_candidates_per_screening": round(avg_candidates_per_screening, 1),
                "top_candidates": top_candidates,
                "recent_activity": recent_activity,
                "success_rate": 100  # All completed screenings are successful
            }
            
        except Exception as e:
            print(f"❌ Error calculating screening statistics: {e}")
            return {
                "total_screenings": 0,
                "total_candidates_screened": 0,
                "average_matches_per_screening": 0,
                "top_candidates": [],
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
            print(f"❌ Error loading screening results: {e}")
            return []
    
    def clear_results(self):
        """Clear all stored results (for testing/maintenance)"""
        try:
            with open(self.results_file, 'w') as f:
                json.dump([], f)
            print("✅ Cleared all screening results")
        except Exception as e:
            print(f"❌ Error clearing screening results: {e}")
