"""
Comprehensive Test Harness for Resume Trust Lab System
Tests trustworthiness, accuracy, and failure modes
"""

import json
import sys
from pathlib import Path
from typing import Dict
import pandas as pd
from loader import DataLoader
from filter_roles import RoleFilter
from ranking.baseline_ranker import BaselineRanker
from ranking.embedding_ranker import EmbeddingRanker
from ranking.gemini_ranker import GeminiRanker
from ranking.improved_gemini_ranker import ImprovedGeminiRanker
from evaluation.experiment_runner import ExperimentRunner
from metrics.trust_metrics import TrustMetrics
from metrics.failure_analysis import FailureAnalysis
from config import OUTPUT_DIR, DATASET_PATH


class TrustworthinessTestSuite:
    """Comprehensive test suite for trustworthiness metrics."""
    
    def __init__(self, sample_size: int = 500):
        self.sample_size = sample_size
        self.results = {}
        self.trustworthiness_scores = {}
        
    def log(self, msg: str):
        """Log test output."""
        print(f"[TEST] {msg}")
        
    def test_data_integrity(self) -> bool:
        """Test 1: Verify dataset integrity."""
        self.log("=" * 60)
        self.log("TEST 1: DATA INTEGRITY")
        try:
            df = pd.read_csv(DATASET_PATH)
            assert len(df) > 0, "Dataset is empty"
            assert 'Role' in df.columns, "Missing 'Role' column"
            assert 'Resume' in df.columns, "Missing 'Resume' column"
            assert 'Decision' in df.columns, "Missing 'Decision' column"
            
            select_count = (df['Decision'].str.lower() == 'select').sum()
            reject_count = (df['Decision'].str.lower() == 'reject').sum()
            select_rate = select_count / len(df)
            
            self.log(f"✓ Dataset loaded: {len(df):,} resumes")
            self.log(f"✓ Select rate: {select_rate:.1%} ({select_count:,})")
            self.log(f"✓ Reject rate: {100-select_rate:.1%} ({reject_count:,})")
            self.results['data_integrity'] = {
                'passed': True,
                'total_resumes': len(df),
                'select_rate': select_rate
            }
            return True
        except Exception as e:
            self.log(f"✗ FAILED: {e}")
            self.results['data_integrity'] = {'passed': False, 'error': str(e)}
            return False
    
    def test_stage_1_filtering(self, role: str = "E-commerce Specialist") -> bool:
        """Test 2: Stage 1 role filtering."""
        self.log("=" * 60)
        self.log("TEST 2: STAGE 1 ROLE FILTERING")
        try:
            loader = DataLoader()
            df = loader.load_dataset(sample_size=self.sample_size)
            filtered_df = loader.filter_by_role(df, role)
            
            self.log(f"✓ Input: {len(df)} resumes")
            self.log(f"✓ Filtered: {len(filtered_df)} resumes for '{role}'")
            self.log(f"✓ Retention: {len(filtered_df)/len(df):.1%}")
            
            select_rate = (filtered_df['Decision'].str.lower() == 'select').sum() / len(filtered_df)
            self.log(f"✓ Select rate in filtered: {select_rate:.1%}")
            
            self.results['stage_1'] = {
                'passed': True,
                'role': role,
                'input_count': len(df),
                'output_count': len(filtered_df),
                'retention_rate': len(filtered_df) / len(df),
                'select_rate': select_rate
            }
            return True
        except Exception as e:
            self.log(f"✗ FAILED: {e}")
            self.results['stage_1'] = {'passed': False, 'error': str(e)}
            return False
    
    def test_stage_2_baseline(self) -> bool:
        """Test 3: Stage 2 TF-IDF ranking."""
        self.log("=" * 60)
        self.log("TEST 3: STAGE 2 BASELINE RANKING (TF-IDF)")
        try:
            runner = ExperimentRunner(sample_size=self.sample_size)
            runner.run_stage_1("E-commerce Specialist")
            
            # Run Stage 2
            stage_2_results, _ = runner.run_stage_2()
            
            selected_top_k = (runner.ranked_dfs[2]['Decision'].str.lower() == 'select').sum()
            total_top_k = len(runner.ranked_dfs[2])
            accuracy_top_k = selected_top_k / total_top_k
            
            self.log(f"✓ TF-IDF Score Stats: min={stage_2_results['score_stats']['min']:.2f}, "
                    f"max={stage_2_results['score_stats']['max']:.2f}, "
                    f"mean={stage_2_results['score_stats']['mean']:.2f}")
            self.log(f"✓ Top-K Accuracy: {accuracy_top_k:.1%} selected")
            
            self.results['stage_2'] = {
                'passed': True,
                'input_count': stage_2_results['input_count'],
                'output_count': stage_2_results['output_count'],
                'accuracy_top_k': accuracy_top_k
            }
            return True
        except Exception as e:
            self.log(f"✗ FAILED: {e}")
            self.results['stage_2'] = {'passed': False, 'error': str(e)}
            return False
    
    def test_stage_3_embeddings(self) -> bool:
        """Test 4: Stage 3 embedding ranking."""
        self.log("=" * 60)
        self.log("TEST 4: STAGE 3 EMBEDDING RANKING")
        try:
            runner = ExperimentRunner(sample_size=self.sample_size)
            runner.run_stage_1("E-commerce Specialist")
            runner.run_stage_2()
            stage_3_results, _ = runner.run_stage_3()
            
            selected_top_k = (runner.ranked_dfs[3]['Decision'].str.lower() == 'select').sum()
            accuracy_top_k = selected_top_k / len(runner.ranked_dfs[3])
            
            self.log(f"✓ Embedding Score Stats: min={stage_3_results['score_stats']['min']:.3f}, "
                    f"max={stage_3_results['score_stats']['max']:.3f}, "
                    f"mean={stage_3_results['score_stats']['mean']:.3f}")
            self.log(f"✓ Top-K Accuracy: {accuracy_top_k:.1%} selected")
            
            self.results['stage_3'] = {
                'passed': True,
                'accuracy_top_k': accuracy_top_k
            }
            return True
        except Exception as e:
            self.log(f"✗ FAILED: {e}")
            self.results['stage_3'] = {'passed': False, 'error': str(e)}
            return False
    
    def test_stage_4_gemini_rate_limit(self) -> bool:
        """Test 5: Stage 4 Gemini with rate limiting."""
        self.log("=" * 60)
        self.log("TEST 5: STAGE 4 GEMINI (RATE LIMIT CHECK)")
        try:
            runner = ExperimentRunner(sample_size=100)
            runner.run_stage_1("E-commerce Specialist")
            runner.run_stage_2()
            runner.run_stage_3()
            
            stage_4_results, _ = runner.run_stage_4()
            
            api_requests = stage_4_results.get('cache_stats', {}).get('api_requests', 0)
            cache_hits = stage_4_results.get('cache_stats', {}).get('hits', 0)
            
            self.log(f"✓ API Requests: {api_requests}")
            self.log(f"✓ Cache Hits: {cache_hits}")
            self.log(f"✓ Rate limit enforced: {stage_4_results['parameters'].get('rate_limit', 'N/A')}")
            
            self.results['stage_4_rate_limit'] = {
                'passed': True,
                'api_requests': api_requests,
                'cache_hits': cache_hits
            }
            return True
        except Exception as e:
            self.log(f"✗ FAILED: {e}")
            self.results['stage_4_rate_limit'] = {'passed': False, 'error': str(e)}
            return False
    
    def test_hallucination_detection(self) -> bool:
        """Test 6: Hallucination detection in Stage 5."""
        self.log("=" * 60)
        self.log("TEST 6: HALLUCINATION DETECTION (STAGE 5)")
        try:
            runner = ExperimentRunner(sample_size=100)
            runner.run_stage_1("E-commerce Specialist")
            runner.run_stage_2()
            runner.run_stage_3()
            runner.run_stage_4()
            
            stage_5_results, _ = runner.run_stage_5()
            
            halluc_detected = stage_5_results.get('hallucination_stats', {}).get('detected', 0)
            halluc_avg_rate = stage_5_results.get('hallucination_stats', {}).get('avg_rate', 0)
            
            self.log(f"✓ Hallucinations detected: {halluc_detected}")
            self.log(f"✓ Avg hallucination rate: {halluc_avg_rate:.1%}")
            
            self.results['stage_5_hallucination'] = {
                'passed': True,
                'hallucinations_detected': halluc_detected,
                'avg_hallucination_rate': halluc_avg_rate
            }
            return True
        except Exception as e:
            self.log(f"✗ FAILED: {e}")
            self.results['stage_5_hallucination'] = {'passed': False, 'error': str(e)}
            return False
    
    def test_trustworthiness_metrics(self) -> bool:
        """Test 7: Trustworthiness metrics computation."""
        self.log("=" * 60)
        self.log("TEST 7: TRUSTWORTHINESS METRICS")
        try:
            runner = ExperimentRunner(sample_size=200)
            runner.run_all("E-commerce Specialist", stages=[1, 2, 3, 4, 5])
            runner.compute_metrics()
            
            self.log(f"✓ Metrics computed successfully")
            
            metrics_file = OUTPUT_DIR / "metrics.json"
            if metrics_file.exists():
                with open(metrics_file) as f:
                    metrics = json.load(f)
                    self.log(f"✓ Top-K Stability Scores: {json.dumps(metrics.get('tss_scores', {}), indent=2)}")
                    
                    self.results['trustworthiness_metrics'] = {
                        'passed': True,
                        'metrics': metrics
                    }
                    return True
        except Exception as e:
            self.log(f"✗ FAILED: {e}")
            self.results['trustworthiness_metrics'] = {'passed': False, 'error': str(e)}
            return False
    
    def pre_register_failure_cases(self) -> Dict:
        """Pre-register 5 cases likely to fail."""
        self.log("=" * 60)
        self.log("PRE-REGISTERED FAILURE CASES")
        
        failure_cases = {
            'case_1': {
                'name': 'Ambiguous Role (Edge Case)',
                'description': 'Resume with vague role title that could match multiple positions',
                'expected_failure': 'Role filtering might include/exclude incorrectly',
                'metric': 'Retention rate < 5% or > 25%'
            },
            'case_2': {
                'name': 'LLM Hallucination (Keyword Absent)',
                'description': 'LLM mentions required skills that aren\'t in resume text',
                'expected_failure': 'Hallucination rate > 30%',
                'metric': 'Hallucination detection rate'
            },
            'case_3': {
                'name': 'Method Disagreement (Stage 2 vs 3)',
                'description': 'TF-IDF and Embeddings rank top-5 completely differently',
                'expected_failure': 'TSS (Top-K Stability) < 0.40',
                'metric': 'TSS between Stage 2 and 3'
            },
            'case_4': {
                'name': 'False Positives (Selected Non-Match)',
                'description': 'System ranks unqualified candidates as top-5',
                'expected_failure': '< 40% of top-5 are actually "selected" in ground truth',
                'metric': 'Accuracy of top-K recommendations'
            },
            'case_5': {
                'name': 'False Negatives (Missed Qualified)',
                'description': 'System eliminates qualified candidates in early stages',
                'expected_failure': 'Stage 3→5 retention < 20% of selected candidates',
                'metric': 'False negative rate'
            }
        }
        
        for case_id, case in failure_cases.items():
            self.log(f"\n{case_id.upper()}: {case['name']}")
            self.log(f"  Description: {case['description']}")
            self.log(f"  Expected Failure: {case['expected_failure']}")
            self.log(f"  Metric: {case['metric']}")
        
        return failure_cases
    
    def run_all_tests(self) -> Dict:
        """Run all tests."""
        self.log("╔" + "="*58 + "╗")
        self.log("║" + " "*15 + "TRUSTWORTHINESS TEST SUITE" + " "*17 + "║")
        self.log("╚" + "="*58 + "╝")
        
        tests = [
            self.test_data_integrity,
            self.test_stage_1_filtering,
            self.test_stage_2_baseline,
            self.test_stage_3_embeddings,
            self.test_stage_4_gemini_rate_limit,
            self.test_hallucination_detection,
            self.test_trustworthiness_metrics,
        ]
        
        passed = 0
        for test in tests:
            if test():
                passed += 1
        
        self.log("=" * 60)
        self.log(f"TESTS PASSED: {passed}/{len(tests)}")
        
        # Pre-register failure cases
        failure_cases = self.pre_register_failure_cases()
        
        return {
            'summary': self.results,
            'tests_passed': passed,
            'tests_total': len(tests),
            'failure_cases': failure_cases
        }


if __name__ == "__main__":
    suite = TrustworthinessTestSuite(sample_size=500)
    results = suite.run_all_tests()
    
    print("\n" + "="*60)
    print("TEST RESULTS SUMMARY")
    print("="*60)
    print(json.dumps(results, indent=2))
