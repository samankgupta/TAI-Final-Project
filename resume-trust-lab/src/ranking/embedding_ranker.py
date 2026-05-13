"""Stage 3: Embedding-based ranking using sentence-transformers."""

import json
from typing import Dict, List
import pandas as pd
from pathlib import Path
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from config import STAGE_3_OUTPUT, TOP_K_STAGE_3, EMBEDDING_MODEL


class EmbeddingRanker:
    """Ranks resumes using semantic embeddings."""
    
    def __init__(self, model_name: str = EMBEDDING_MODEL):
        print(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
    
    def compute_embedding_scores(self, job_description: str, resumes: List[str]) -> np.ndarray:
        """Compute embedding-based similarity scores."""
        jd_embedding = self.model.encode(job_description, convert_to_tensor=False)
        resume_embeddings = self.model.encode(resumes, convert_to_tensor=False)
        similarities = cosine_similarity([jd_embedding], resume_embeddings).flatten()
        return similarities
    
    def run(self, df: pd.DataFrame, job_description: str, top_k: int = TOP_K_STAGE_3) -> Dict:
        """Run Stage 3: Embedding-based ranking."""
        print(f"\n{'='*60}\nSTAGE 3: EMBEDDING RANKING")

        if df is None or df.empty:
            results = {
                'stage': 3,
                'stage_name': 'Embedding Ranking',
                'parameters': {'method': 'Sentence-Transformers', 'top_k': top_k},
                'input_count': 0,
                'output_count': 0,
                'retention_rate': 0.0,
                'score_stats': {'min': 0.0, 'max': 0.0, 'mean': 0.0},
                'ranked_resumes': []
            }
            print("No resumes available for Stage 3; skipping embedding ranking.")
            return results, df.copy() if df is not None else pd.DataFrame()
        
        resumes = df['Resume'].tolist()
        print(f"Computing embeddings for {len(resumes)} resumes...")
        scores = self.compute_embedding_scores(job_description, resumes)
        
        ranking_df = df.copy()
        ranking_df['embedding_score'] = scores
        ranking_df = ranking_df.sort_values('embedding_score', ascending=False).reset_index(drop=True)
        top_k_df = ranking_df.head(top_k)
        
        results = {
            'stage': 3,
            'stage_name': 'Embedding Ranking',
            'parameters': {'method': 'Sentence-Transformers', 'top_k': top_k},
            'input_count': len(df),
            'output_count': len(top_k_df),
            'retention_rate': len(top_k_df) / len(df),
            'score_stats': {'min': float(scores.min()), 'max': float(scores.max()), 'mean': float(scores.mean())},
            'ranked_resumes': []
        }
        
        for idx, (_, row) in enumerate(top_k_df.iterrows(), 1):
            results['ranked_resumes'].append({
                'rank': idx,
                'candidate_id': int(row['candidate_id']) if 'candidate_id' in row else idx - 1,
                'embedding_score': float(row['embedding_score']),
                'resume': row.get('Resume', ''),
            })
        print(f"Input: {len(df)} | Output: {len(top_k_df)}")
        
        return results, ranking_df
    
    def save_results(self, results: Dict, output_path: str = str(STAGE_3_OUTPUT)) -> None:
        """Save results."""
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"Results saved to {output_path}")
