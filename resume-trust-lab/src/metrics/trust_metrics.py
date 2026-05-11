"""Trust metrics for measuring ranking quality."""

import json
from typing import Dict, List
from pathlib import Path

from config import METRICS_OUTPUT, STAGE_1_OUTPUT


class TrustMetrics:
    """Computes trust metrics."""

    @staticmethod
    def top_k_stability_score(top_k_A: List[int], top_k_B: List[int]) -> float:
        """Jaccard overlap between two candidate_id lists."""
        set_a = set(top_k_A)
        set_b = set(top_k_B)
        union = set_a | set_b
        return len(set_a & set_b) / len(union) if union else 0.0

    @staticmethod
    def precision_at_k(candidate_ids: List[int], ground_truth: Dict[int, str]) -> float:
        """Fraction of top-k candidates that are ground-truth 'select'."""
        if not candidate_ids:
            return 0.0
        hits = sum(1 for cid in candidate_ids if ground_truth.get(cid, '').lower() == 'select')
        return hits / len(candidate_ids)

    @staticmethod
    def load_ground_truth() -> Dict[int, str]:
        """Load candidate_id -> decision map from Stage 1 output."""
        path = Path(STAGE_1_OUTPUT)
        if not path.exists():
            return {}
        with open(path) as f:
            s1 = json.load(f)
        return {r['id']: r.get('decision', '') for r in s1.get('resumes', [])}

    @staticmethod
    def compute_all_metrics(stage_results: Dict) -> Dict:
        """Compute TSS and precision@k for all stages."""
        ground_truth = TrustMetrics.load_ground_truth()

        metrics = {
            'stages_compared': list(stage_results.keys()),
            'tss_scores': {},
            'precision_at_k': {},
            'hallucination_rates': {}
        }

        stages = list(stage_results.items())

        for stage_name, data in stages:
            if 'ranked_resumes' not in data:
                continue
            cids = [r.get('candidate_id', r.get('id', -1)) for r in data['ranked_resumes']]
            if ground_truth:
                p_at_k = TrustMetrics.precision_at_k(cids, ground_truth)
                metrics['precision_at_k'][stage_name] = round(p_at_k, 3)

        for i in range(len(stages) - 1):
            stage_a_name, data_a = stages[i]
            stage_b_name, data_b = stages[i + 1]
            if 'ranked_resumes' in data_a and 'ranked_resumes' in data_b:
                ids_a = [r.get('candidate_id', r.get('id', -1)) for r in data_a['ranked_resumes']]
                ids_b = [r.get('candidate_id', r.get('id', -1)) for r in data_b['ranked_resumes']]
                tss = TrustMetrics.top_k_stability_score(ids_a, ids_b)
                metrics['tss_scores'][f"{stage_a_name}_vs_{stage_b_name}"] = round(tss, 3)

        if ground_truth:
            print(f"\nGround truth loaded: {len(ground_truth)} candidates")
            print("Precision@K per stage:")
            for stage, p in metrics['precision_at_k'].items():
                print(f"  {stage}: {p:.1%}")

        print("\nStage overlap (TSS):")
        for pair, score in metrics['tss_scores'].items():
            print(f"  {pair}: {score:.3f}")

        return metrics


def save_metrics(metrics: Dict, output_path: str = str(METRICS_OUTPUT)) -> None:
    """Save metrics."""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(metrics, f, indent=2)
    print(f"Metrics saved to {output_path}")
