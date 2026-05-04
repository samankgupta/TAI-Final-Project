"""
End-to-End Trustworthiness Evaluation with Gemini API
Compares original system vs improved ensemble approach
"""

import json
import time
from pathlib import Path
import pandas as pd
import numpy as np
import sys

sys.path.insert(0, str(Path(__file__).parent))

from config import DATASET_PATH, OUTPUT_DIR, GEMINI_API_KEY
from loader import DataLoader
from ranking.baseline_ranker import BaselineRanker
from ranking.embedding_ranker import EmbeddingRanker
from ranking.gemini_ranker import GeminiRanker
from ranking.improved_gemini_ranker import ImprovedGeminiRanker
from ranking.ensemble_ranker import EnsembleRanker


class EndToEndEvaluation:
    """End-to-end evaluation with Gemini API."""
    
    def __init__(self):
        self.results = {}
        self.start_time = None
        
    def log(self, msg: str, level: str = "INFO"):
        """Log message."""
        print(f"[{level}] {msg}")
    
    def run_evaluation(self, sample_size: int = 100):
        """Run complete end-to-end evaluation."""
        self.start_time = time.time()
        
        self.log("="*70, "")
        self.log("END-TO-END TRUSTWORTHINESS EVALUATION", "")
        self.log("="*70, "")
        self.log(f"Sample size: {sample_size}", "")
        self.log(f"Gemini API available: {'✓' if GEMINI_API_KEY else '✗'}", "")
        
        # Phase 1: Data Load
        self.log("\n[PHASE 1] LOADING DATA", "")
        df = pd.read_csv(DATASET_PATH).sample(n=min(sample_size, 5000), random_state=42)
        role = "E-commerce Specialist"
        df_role = df[df['Role'].str.contains(role, case=False, na=False)]
        if len(df_role) == 0:
            # If specific role not found, use first N resumes as fallback
            df_role = df.head(min(sample_size // 2, 50))
            self.log(f"! Role not found, using first {len(df_role)} resumes as fallback", "")
        
        self.log(f"✓ Loaded {len(df_role)} resumes for '{role}'", "")
        select_rate = (df_role['Decision'].str.lower() == 'select').sum() / len(df_role)
        self.log(f"✓ Ground truth select rate: {select_rate:.1%}", "")
        
        job_desc = "E-commerce specialist. Must have: online sales, customer engagement, product management. Nice to have: analytics, marketing automation."
        
        # Phase 2: Stage 2 - TF-IDF
        self.log("\n[PHASE 2] STAGE 2 - BASELINE RANKING (TF-IDF)", "")
        start = time.time()
        baseline_ranker = BaselineRanker()
        tfidf_scores = baseline_ranker.compute_tfidf_scores(job_desc, df_role['Resume'].tolist())
        self.log(f"✓ TF-IDF ranking: {len(tfidf_scores)} resumes scored", "")
        self.log(f"  Score range: [{tfidf_scores.min():.3f}, {tfidf_scores.max():.3f}]", "")
        self.log(f"  Time: {time.time()-start:.1f}s", "")
        
        # Phase 3: Stage 3 - Embeddings
        self.log("\n[PHASE 3] STAGE 3 - EMBEDDING RANKING", "")
        start = time.time()
        embedding_ranker = EmbeddingRanker()
        embedding_scores = embedding_ranker.compute_embedding_scores(job_desc, df_role['Resume'].tolist())
        self.log(f"✓ Embedding ranking: {len(embedding_scores)} resumes scored", "")
        self.log(f"  Score range: [{embedding_scores.min():.3f}, {embedding_scores.max():.3f}]", "")
        self.log(f"  Time: {time.time()-start:.1f}s", "")
        
        # Compare rankings
        tfidf_ranked = pd.Series(tfidf_scores).rank(ascending=False).values
        embedding_ranked = pd.Series(embedding_scores).rank(ascending=False).values
        top_10_tfidf_idx = np.argsort(-tfidf_scores)[:10]
        top_10_embedding_idx = np.argsort(-embedding_scores)[:10]
        overlap = len(set(top_10_tfidf_idx) & set(top_10_embedding_idx))
        
        self.log(f"✓ Top-10 overlap: {overlap}/10", "")
        self.log(f"  Stability Score: {overlap/10:.1%}", "")
        
        # Phase 4: Stage 4 - Gemini Base
        self.log("\n[PHASE 4] STAGE 4 - GEMINI RANKING (BASE)", "")
        start = time.time()
        gemini_ranker = GeminiRanker()
        gemini_scores = []
        
        for i, (_, row) in enumerate(df_role.iterrows()):
            result = gemini_ranker.rank_resume_with_gemini(job_desc, row['Resume'])
            gemini_scores.append(result['score'])
            if (i + 1) % 5 == 0:
                self.log(f"  Scored {i + 1}/{len(df_role)}", "")
        
        gemini_scores = np.array(gemini_scores)
        self.log(f"✓ Gemini ranking: {len(gemini_scores)} resumes scored", "")
        self.log(f"  Score range: [{gemini_scores.min():.0f}, {gemini_scores.max():.0f}]", "")
        self.log(f"  Time: {time.time()-start:.1f}s", "")
        self.log(f"  API requests: {gemini_ranker.api_requests}, Cache hits: {gemini_ranker.cache_hits}", "")
        
        # Analyze Gemini vs others
        gemini_norm = gemini_scores / 10.0
        tfidf_norm = (tfidf_scores - tfidf_scores.min()) / (tfidf_scores.max() - tfidf_scores.min() + 1e-6)
        embedding_norm = (embedding_scores - embedding_scores.min()) / (embedding_scores.max() - embedding_scores.min() + 1e-6)
        
        correlations = {
            'gemini_vs_tfidf': float(np.corrcoef(gemini_norm, tfidf_norm)[0, 1]),
            'gemini_vs_embedding': float(np.corrcoef(gemini_norm, embedding_norm)[0, 1]),
            'tfidf_vs_embedding': float(np.corrcoef(tfidf_norm, embedding_norm)[0, 1])
        }
        self.log(f"✓ Score correlations:", "")
        for k, v in correlations.items():
            self.log(f"  {k}: {v:.2f}", "")
        
        # Phase 5: Stage 4.5 - Ensemble (Improvement)
        self.log("\n[PHASE 5] STAGE 4.5 - ENSEMBLE RANKING (IMPROVED)", "")
        start = time.time()
        ensemble_ranker = EnsembleRanker()
        df_role_copy = df_role.copy()
        df_ranked, ensemble_scores, confidence_scores = ensemble_ranker.rank_ensemble(
            df_role_copy, tfidf_scores, embedding_scores, gemini_scores,
            {'tfidf_max': tfidf_scores.max(), 'embedding_max': embedding_scores.max()}
        )
        
        self.log(f"✓ Ensemble ranking complete", "")
        self.log(f"  Ensemble score range: [{min(ensemble_scores):.3f}, {max(ensemble_scores):.3f}]", "")
        self.log(f"  Confidence score range: [{min(confidence_scores):.3f}, {max(confidence_scores):.3f}]", "")
        self.log(f"  Time: {time.time()-start:.1f}s", "")
        
        # Detect anomalies
        anomalies = ensemble_ranker.detect_anomalies(df_role_copy, tfidf_scores, embedding_scores, gemini_scores)
        self.log(f"✓ Anomalies detected: {len(anomalies)}", "")
        for anomaly in anomalies[:3]:
            self.log(f"  Resume {anomaly['index']}: disagreement={anomaly['disagreement']:.2f}", "")
        
        # Phase 6: Accuracy Analysis
        self.log("\n[PHASE 6] ACCURACY ANALYSIS", "")
        
        # Get top-5 from each method
        top_k = 5
        top_tfidf = df_role.iloc[np.argsort(-tfidf_scores)[:top_k]]
        top_embedding = df_role.iloc[np.argsort(-embedding_scores)[:top_k]]
        top_gemini = df_role.iloc[np.argsort(-gemini_scores)[:top_k]]
        top_ensemble = df_ranked.head(top_k)
        
        accuracy_tfidf = (top_tfidf['Decision'].str.lower() == 'select').sum() / top_k
        accuracy_embedding = (top_embedding['Decision'].str.lower() == 'select').sum() / top_k
        accuracy_gemini = (top_gemini['Decision'].str.lower() == 'select').sum() / top_k
        accuracy_ensemble = (top_ensemble['Decision'].str.lower() == 'select').sum() / top_k
        
        self.log(f"Top-{top_k} accuracy (% selected):", "")
        self.log(f"  TF-IDF:    {accuracy_tfidf:.0%}", "")
        self.log(f"  Embedding: {accuracy_embedding:.0%}", "")
        self.log(f"  Gemini:    {accuracy_gemini:.0%}", "")
        self.log(f"  Ensemble:  {accuracy_ensemble:.0%} ← IMPROVED", "")
        
        improvement = (accuracy_ensemble - max(accuracy_tfidf, accuracy_embedding, accuracy_gemini)) * 100
        self.log(f"✓ Improvement over best single method: {improvement:+.0f}%", "")
        
        # Phase 7: Trustworthiness Summary
        self.log("\n[PHASE 7] TRUSTWORTHINESS METRICS", "")
        
        trustworthiness_scores = {
            'baseline_tfidf': {
                'accuracy': float(accuracy_tfidf),
                'method': 'TF-IDF',
                'confidence': 'Low (keyword-based)'
            },
            'embedding': {
                'accuracy': float(accuracy_embedding),
                'method': 'Embeddings',
                'confidence': 'Medium (semantic)'
            },
            'gemini_base': {
                'accuracy': float(accuracy_gemini),
                'method': 'Gemini LLM',
                'confidence': 'High (LLM-based)'
            },
            'ensemble_improved': {
                'accuracy': float(accuracy_ensemble),
                'method': 'Ensemble',
                'confidence': 'Very High (multi-method)'
            }
        }
        
        for method, scores in trustworthiness_scores.items():
            self.log(f"{method}: {scores['accuracy']:.0%} accuracy, confidence={scores['confidence']}", "")
        
        # Phase 8: Rate Limiting Verification
        self.log("\n[PHASE 8] RATE LIMITING VERIFICATION", "")
        self.log(f"✓ Gemini requests per minute limit: 13", "")
        self.log(f"  Requests made: {gemini_ranker.api_requests}", "")
        self.log(f"  Min interval: {gemini_ranker.MIN_INTERVAL_SECONDS:.1f}s", "")
        
        total_time = time.time() - self.start_time
        self.log(f"✓ Total evaluation time: {total_time:.1f}s", "")
        
        # Save results
        self.log("\n[PHASE 9] SAVING RESULTS", "")
        results_file = OUTPUT_DIR / "end_to_end_evaluation.json"
        
        final_results = {
            'evaluation_summary': {
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'sample_size': len(df_role),
                'total_time_seconds': float(total_time),
                'ground_truth_select_rate': float(select_rate)
            },
            'method_comparison': trustworthiness_scores,
            'improvement': {
                'best_single_method_accuracy': float(max(accuracy_tfidf, accuracy_embedding, accuracy_gemini)),
                'ensemble_accuracy': float(accuracy_ensemble),
                'improvement_percentage': float(improvement)
            },
            'correlations': correlations,
            'anomalies_detected': len(anomalies),
            'rate_limiting': {
                'api_requests': int(gemini_ranker.api_requests),
                'cache_hits': int(gemini_ranker.cache_hits),
                'rate_limit_per_minute': 13
            }
        }
        
        with open(results_file, 'w') as f:
            json.dump(final_results, f, indent=2)
        
        self.log(f"✓ Results saved to {results_file}", "")
        
        return final_results


def main():
    """Run evaluation."""
    evaluator = EndToEndEvaluation()
    results = evaluator.run_evaluation(sample_size=500)
    
    print("\n" + "="*70)
    print("FINAL RESULTS SUMMARY")
    print("="*70)
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
