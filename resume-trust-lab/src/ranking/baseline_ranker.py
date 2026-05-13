"""Stage 2: Baseline keyword-based ranking using TF-IDF."""

import json
from typing import Dict, List
import pandas as pd
from pathlib import Path
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from config import STAGE_2_OUTPUT, TOP_K_STAGE_2


class BaselineRanker:
    """Ranks resumes using TF-IDF keyword overlap."""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=500, stop_words='english', lowercase=True, min_df=1)
    
    def compute_tfidf_scores(self, job_description: str, resumes: List[str]) -> np.ndarray:
        """Compute TF-IDF similarity scores."""
        texts = [job_description] + resumes
        tfidf_matrix = self.vectorizer.fit_transform(texts)
        similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
        return similarities
    
    def run(self, df: pd.DataFrame, job_description: str, top_k: int = TOP_K_STAGE_2) -> Dict:
        """Run Stage 2: Baseline ranking."""
        print(f"\n{'='*60}\nSTAGE 2: BASELINE RANKING (TF-IDF)")

        if df is None or df.empty:
            results = {
                'stage': 2,
                'stage_name': 'Baseline Ranking (TF-IDF)',
                'parameters': {'method': 'TF-IDF Cosine Similarity', 'top_k': top_k},
                'input_count': 0,
                'output_count': 0,
                'retention_rate': 0.0,
                'score_stats': {'min': 0.0, 'max': 0.0, 'mean': 0.0},
                'ranked_resumes': []
            }
            print("No resumes available for Stage 2; skipping ranking.")
            return results, df.copy() if df is not None else pd.DataFrame()
        
        resumes = df['Resume'].tolist()
        scores = self.compute_tfidf_scores(job_description, resumes)
        
        ranking_df = df.copy()
        ranking_df['baseline_score'] = scores
        ranking_df = ranking_df.sort_values('baseline_score', ascending=False).reset_index(drop=True)
        top_k_df = ranking_df.head(top_k)
        
        results = {
            'stage': 2,
            'stage_name': 'Baseline Ranking (TF-IDF)',
            'parameters': {'method': 'TF-IDF Cosine Similarity', 'top_k': top_k},
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
                'baseline_score': float(row['baseline_score']),
                'resume': row.get('Resume', ''),
            })
        print(f"Input: {len(df):,} | Output: {len(top_k_df)}")
        
        return results, ranking_df
    
    def save_results(self, results: Dict, output_path: str = str(STAGE_2_OUTPUT)) -> None:
        """Save stage results to JSON."""
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"Results saved to {output_path}")
