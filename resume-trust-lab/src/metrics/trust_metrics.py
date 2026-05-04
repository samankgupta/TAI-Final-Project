"""Trust metrics for measuring ranking quality."""

import json
from typing import Dict, List, Set
import numpy as np
from pathlib import Path

from config import METRICS_OUTPUT


class TrustMetrics:
    """Computes trust metrics."""
    
    @staticmethod
    def top_k_stability_score(top_k_A: List[int], top_k_B: List[int], k: int = 5) -> float:
        """Top-K Stability Score (overlap between top-K)."""
        set_a = set(top_k_A[:k])
        set_b = set(top_k_B[:k])
        intersection = len(set_a & set_b)
        return intersection / k if k > 0 else 0
    
    @staticmethod
    def compute_all_metrics(stage_results: Dict) -> Dict:
        """Compute comprehensive metrics."""
        metrics = {
            'stages_compared': list(stage_results.keys()),
            'tss_scores': {},
            'hallucination_rates': {}
        }
        
        stages = list(stage_results.items())
        for i in range(len(stages) - 1):
            stage_a_name, data_a = stages[i]
            stage_b_name, data_b = stages[i + 1]
            
            if 'ranked_resumes' in data_a and 'ranked_resumes' in data_b:
                top_k_a = [r['id'] for r in data_a['ranked_resumes']]
                top_k_b = [r['id'] for r in data_b['ranked_resumes']]
                tss = TrustMetrics.top_k_stability_score(top_k_a, top_k_b, len(top_k_b))
                metrics['tss_scores'][f"{stage_a_name}_vs_{stage_b_name}"] = tss
        
        return metrics


def save_metrics(metrics: Dict, output_path: str = str(METRICS_OUTPUT)) -> None:
    """Save metrics."""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(metrics, f, indent=2)
    print(f"Metrics saved to {output_path}")
