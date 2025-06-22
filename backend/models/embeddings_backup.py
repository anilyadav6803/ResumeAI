from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import numpy as np
from typing import List, Dict
import os

class EmbeddingManager:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """Initialize embedding manager with sentence transformer model"""
        self.model_name = model_name
        self.model = None
        self.chroma_client = None
        self.collection = None
        self._initialize_model()
        self._initialize_vector_store()
    
    def _initialize_model(self):
        """Initialize the sentence transformer model"""
        try:
            self.model = SentenceTransformer(self.model_name)
            print(f"Loaded embedding model: {self.model_name}")
        except Exception as e:
            print(f"Error loading embedding model: {e}")
            raise
    
    def _initialize_vector_store(self):
        """Initialize ChromaDB vector store"""
        try:
            # Create persistent ChromaDB client
            persist_directory = "./data/vector_db"
            os.makedirs(persist_directory, exist_ok=True)
            
            self.chroma_client = chromadb.PersistentClient(path=persist_directory)
            
            # Get or create collection
            try:
                self.collection = self.chroma_client.get_collection("resumes")
                print("Loaded existing resume collection")
            except:
                self.collection = self.chroma_client.create_collection(
                    name="resumes",
                    metadata={"description": "Resume embeddings for job matching"}
                )
                print("Created new resume collection")
                
        except Exception as e:
            print(f"Error initializing vector store: {e}")
            raise
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts"""
        try:
            embeddings = self.model.encode(texts, convert_to_tensor=False)
            return embeddings.tolist()
        except Exception as e:
            print(f"Error generating embeddings: {e}")
            raise
    
    def add_resume_embeddings(self, resumes: List[Dict]):
        """Add resume embeddings to vector store"""
        try:
            # Clear existing collection
            self.collection.delete()
            
            documents = []
            metadatas = []
            ids = []
            
            for i, resume in enumerate(resumes):
                if resume['parsing_status'] == 'success' and resume['full_text']:
                    # Split resume into chunks for better matching
                    chunks = self._split_text(resume['full_text'])
                    
                    for j, chunk in enumerate(chunks):
                        documents.append(chunk)
                        metadatas.append({
                            'file_name': resume['file_name'],
                            'name': resume['name'],
                            'email': resume['email'],
                            'phone': resume['phone'],
                            'skills': ','.join(resume['skills']),
                            'experience_years': str(resume['experience_years']) if resume['experience_years'] else '0',
                            'chunk_id': j
                        })
                        ids.append(f"{resume['file_name']}_{j}")
            
            if documents:
                # Add to collection
                self.collection.add(
                    documents=documents,
                    metadatas=metadatas,
                    ids=ids
                )
                print(f"Added {len(documents)} resume chunks to vector store")
            else:
                print("No valid resumes to add to vector store")
                
        except Exception as e:
            print(f"Error adding resume embeddings: {e}")
            raise
    
    def search_similar_resumes(self, job_description: str, top_k: int = 5) -> List[Dict]:
        """Search for resumes similar to job description"""
        try:
            results = self.collection.query(
                query_texts=[job_description],
                n_results=min(top_k * 3, 20)  # Get more results to filter unique resumes
            )
            
            if not results['documents'][0]:
                return []
            
            # Group results by resume file
            resume_scores = {}
            
            for i, (doc, metadata, distance) in enumerate(zip(
                results['documents'][0],
                results['metadatas'][0],
                results['distances'][0]
            )):
                file_name = metadata['file_name']
                
                if file_name not in resume_scores:
                    resume_scores[file_name] = {
                        'metadata': metadata,
                        'best_score': distance,
                        'best_match_text': doc,
                        'total_score': distance,
                        'match_count': 1
                    }
                else:
                    # Update with better score if found
                    if distance < resume_scores[file_name]['best_score']:
                        resume_scores[file_name]['best_score'] = distance
                        resume_scores[file_name]['best_match_text'] = doc
                    
                    resume_scores[file_name]['total_score'] += distance
                    resume_scores[file_name]['match_count'] += 1
            
            # Calculate average scores and sort
            for file_name in resume_scores:
                resume_scores[file_name]['avg_score'] = (
                    resume_scores[file_name]['total_score'] / 
                    resume_scores[file_name]['match_count']
                )
            
            # Sort by best score (lower is better for distance)
            sorted_resumes = sorted(
                resume_scores.items(),
                key=lambda x: x[1]['best_score']
            )
            
            # Return top K unique resumes
            return sorted_resumes[:top_k]
            
        except Exception as e:
            print(f"Error searching similar resumes: {e}")
            return []
    
    def _split_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """Split text into overlapping chunks"""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = ' '.join(words[i:i + chunk_size])
            if chunk.strip():
                chunks.append(chunk)
        
        return chunks if chunks else [text]  # Return original text if no chunks created
      def get_collection_stats(self) -> Dict:
        """Get statistics about the vector store collection"""
        try:
            count = self.collection.count()
            return {
                'total_chunks': count,
                'collection_name': self.collection.name
            }
        except Exception as e:
            return {'error': str(e)}
    
    def clear_collection(self):
        """Clear all data from the collection"""
        try:
            # Get all IDs first, then delete them
            all_data = self.collection.get()
            if all_data and all_data.get('ids'):
                self.collection.delete(ids=all_data['ids'])
                print("Cleared resume collection")
            else:
                print("Collection already empty")
        except Exception as e:
            print(f"Error clearing collection: {e}")
            # Try alternative method
            try:
                self.collection.delete(where={})
                print("Cleared resume collection using alternative method")
            except Exception as e2:
                print(f"Alternative clear method also failed: {e2}")
