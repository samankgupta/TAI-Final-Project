"""Compare stage outputs."""

import json
from typing import Dict, List
from pathlib import Path

from config import OUTPUT_DIR
from metrics.trust_metrics import TrustMetrics


class StageComparator:
    """Compares outputs across stages."""
    
    @staticmethod
    def load_stage_results(stage_num: int) -> Dict:
        """Load stage results."""
        output_file = OUTPUT_DIR / f"stage_{stage_num}.json"
        if not output_file.exists():
            raise FileNotFoundError(f"Stage {stage_num} not found")
        
        with open(output_file, 'r') as f:
            return json.load(f)
    
    @staticmethod
    def compare_rankings(stage_a: int, stage_b: int) -> Dict:
        """Compare two stages."""
        print(f"\nComparing Stage {stage_a} vs Stage {stage_b}...")
        
        results_a = StageComparator.load_stage_results(stage_a)
        results_b = StageComparator.load_stage_results(stage_b)
        
        top_k_a = [r['id'] for r in results_a.get('ranked_resumes', [])]
        top_k_b = [r['id'] for r in results_b.get('ranked_resumes', [])]
        
        k = min(len(top_k_a), len(top_k_b), 5)
        tss = TrustMetrics.top_k_stability_score(top_k_a, top_k_b, k)
        
        return {
            'stage_a': results_a.get('stage_name'),
            'stage_b': results_b.get('stage_name'),
            'tss_top_k': tss,
            'overlap': len(set(top_k_a) & set(top_k_b)),
            'stage_a_only': len(set(top_k_a) - set(top_k_b)),
            'stage_b_only': len(set(top_k_b) - set(top_k_a))
        }
    
    @staticmethod
    def save_comparison(comparison: Dict, output_path: str = None) -> None:
        """Save comparison."""
        if output_path is None:
            output_path = OUTPUT_DIR / "comparison.json"
        
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(comparison, f, indent=2)
        print(f"Comparison saved to {output_path}")
