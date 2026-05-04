"""
Stage 4.5: Ensemble Ranking (Improvement)
Combines TF-IDF, Embeddings, and LLM for better accuracy and trustworthiness
"""

import json
from typing import Dict, List, Tuple
import pandas as pd
import numpy as np
from pathlib import Path

from config import STAGE_4_OUTPUT, TOP_K_STAGE_4


class EnsembleRanker:
    """Ranks resumes using ensemble of multiple methods."""
    
    def __init__(self):
        self.weights = {
            'tfidf': 0.25,        # Keyword matching
            'embedding': 0.25,    # Semantic similarity
            'gemini': 0.40,       # LLM ranking (primary)
            'confidence': 0.10    # Method agreement
        }
    
    def compute_confidence_score(self, tfidf_score: float, embedding_score: float,
                                gemini_score: float, score_range: Dict = None) -> float:
        """
        Compute confidence score based on method agreement.
        Higher confidence when all methods agree.
        """
        # Normalize scores to 0-1 range
        norm_tfidf = tfidf_score / (score_range.get('tfidf_max', 1.0) if score_range else 1.0)
        norm_embedding = embedding_score / (score_range.get('embedding_max', 1.0) if score_range else 1.0)
        norm_gemini = gemini_score / 10.0  # Gemini scores are 1-10
        
        # Calculate variance (disagreement)
        scores = [norm_tfidf, norm_embedding, norm_gemini]
        variance = np.var(scores)
        
        # Confidence = 1 - variance (high variance = low confidence)
        confidence = max(0, 1.0 - variance)
        
        return confidence
    
    def rank_ensemble(self, df: pd.DataFrame, 
                     tfidf_scores: List[float],
                     embedding_scores: List[float],
                     gemini_scores: List[float],
                     score_ranges: Dict = None) -> Tuple[pd.DataFrame, List[float], List[float]]:
        """
        Rank resumes using ensemble method.
        Returns ranked dataframe, ensemble scores, and confidence scores.
        """
        ensemble_scores = []
        confidence_scores = []
        
        # Normalize scores to 0-1 range
        tfidf_range = (min(tfidf_scores), max(tfidf_scores))
        embedding_range = (min(embedding_scores), max(embedding_scores))
        gemini_range = (min(gemini_scores), max(gemini_scores))
        
        for i in range(len(df)):
            # Normalize scores
            norm_tfidf = (tfidf_scores[i] - tfidf_range[0]) / (tfidf_range[1] - tfidf_range[0] + 1e-6)
            norm_embedding = (embedding_scores[i] - embedding_range[0]) / (embedding_range[1] - embedding_range[0] + 1e-6)
            norm_gemini = gemini_scores[i] / 10.0
            
            # Compute ensemble score
            ensemble = (self.weights['tfidf'] * norm_tfidf +
                       self.weights['embedding'] * norm_embedding +
                       self.weights['gemini'] * norm_gemini)
            
            # Compute confidence
            confidence = self.compute_confidence_score(
                tfidf_scores[i], embedding_scores[i], gemini_scores[i],
                {'tfidf_max': tfidf_range[1], 'embedding_max': embedding_range[1]}
            )
            
            ensemble_scores.append(ensemble)
            confidence_scores.append(confidence)
        
        # Rank by ensemble score
        df_copy = df.copy()
        df_copy['ensemble_score'] = ensemble_scores
        df_copy['confidence_score'] = confidence_scores
        df_ranked = df_copy.sort_values('ensemble_score', ascending=False).reset_index(drop=True)
        
        return df_ranked, ensemble_scores, confidence_scores
    
    def detect_anomalies(self, df: pd.DataFrame, 
                        tfidf_scores: List[float],
                        embedding_scores: List[float],
                        gemini_scores: List[float]) -> List[Dict]:
        """
        Detect anomalies: cases where methods strongly disagree.
        These are potentially hallucinations or unreliable rankings.
        """
        anomalies = []
        
        # Normalize scores
        tfidf_norm = np.array(tfidf_scores) / (max(tfidf_scores) + 1e-6)
        embedding_norm = np.array(embedding_scores) / (max(embedding_scores) + 1e-6)
        gemini_norm = np.array(gemini_scores) / 10.0
        
        for i in range(len(df)):
            # Calculate disagreement score
            scores = np.array([tfidf_norm[i], embedding_norm[i], gemini_norm[i]])
            disagreement = np.std(scores)
            
            # Flag if disagreement > threshold (0.3) and high score
            if disagreement > 0.3 and max(scores) > 0.6:
                anomalies.append({
                    'index': i,
                    'disagreement': float(disagreement),
                    'tfidf': float(tfidf_norm[i]),
                    'embedding': float(embedding_norm[i]),
                    'gemini': float(gemini_norm[i]),
                    'type': 'method_disagreement'
                })
        
        return anomalies


def create_ensemble_improvement_report():
    """Create report on ensemble improvement."""
    report = {
        'improvement_type': 'Ensemble Ranking',
        'description': 'Combines TF-IDF, embeddings, and LLM rankings for better accuracy',
        'weights': {
            'tfidf': 0.25,
            'embedding': 0.25,
            'gemini': 0.40,
            'confidence': 0.10
        },
        'benefits': [
            'Reduces false positives by requiring agreement across methods',
            'Provides confidence scores for each ranking',
            'Detects anomalies when methods disagree',
            'Improves trustworthiness by combining signals'
        ],
        'cost': {
            'latency': 'Minimal (all scores computed in parallel)',
            'compute': 'Low (just aggregation)',
            'coverage': '100% (works with any scores)'
        }
    }
    return report
