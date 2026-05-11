"""Experiment runner - orchestrates pipeline."""

import json
import time
from typing import Optional
import pandas as pd
from pathlib import Path

from config import STAGE_1_OUTPUT, STAGE_2_OUTPUT, STAGE_3_OUTPUT, STAGE_4_OUTPUT, STAGE_5_OUTPUT
from loader import DataLoader
from filter_roles import RoleFilter
from ranking.baseline_ranker import BaselineRanker
from ranking.embedding_ranker import EmbeddingRanker
from ranking.gemini_ranker import GeminiRanker
from ranking.improved_gemini_ranker import ImprovedGeminiRanker
from metrics.trust_metrics import TrustMetrics, save_metrics
from metrics.failure_analysis import FailureAnalysis, save_failure_analysis


class ExperimentRunner:
    """Runs complete pipeline."""
    
    def __init__(self, dataset_path: str = None, sample_size: int = None):
        # Let DataLoader use configured default path when dataset_path is not provided.
        self.loader = DataLoader(dataset_path) if dataset_path else DataLoader()
        self.sample_size = sample_size
        self.df = None
        self.job_description = None
        self.role = None
        self.stage_results = {}
        self.ranked_dfs = {}
    
    def run_stage_1(self, role: str, fuzzy: bool = False, max_role_matches: int = 100) -> None:
        """Run Stage 1."""
        if self.df is None:
            # Stage 1 should filter against the full dataset so role matches are not truncated
            # by any earlier sampling choice.
            self.df = self.loader.load_dataset()
        
        filtered_df, original_count = self.loader.filter_by_role(role, fuzzy)
        if max_role_matches is not None and len(filtered_df) > max_role_matches:
            filtered_df = filtered_df.head(max_role_matches).reset_index(drop=True)
        self.role = role
        ground_truth = self.loader.get_ground_truth(filtered_df)
        
        role_filter = RoleFilter()
        results, _ = role_filter.run(filtered_df, role, fuzzy)
        results['ground_truth'] = ground_truth
        results['parameters']['max_role_matches'] = max_role_matches
        role_filter.save_results(results, str(STAGE_1_OUTPUT))
        self.stage_results['stage_1'] = results
        self.df = filtered_df
        self.df['candidate_id'] = range(len(self.df))
    
    def run_stage_2(self, top_k: int = 50) -> None:
        """Run Stage 2."""
        if self.df is None:
            raise ValueError("Must run Stage 1 first")
        if self.job_description is None:
            self.load_job_description()
        
        ranker = BaselineRanker()
        results, ranked_df = ranker.run(self.df, self.job_description, top_k)
        ranker.save_results(results, str(STAGE_2_OUTPUT))
        self.stage_results['stage_2'] = results
        self.ranked_dfs['stage_2'] = ranked_df
    
    def run_stage_3(self, top_k: int = 30) -> None:
        """Run Stage 3."""
        if self.df is None:
            raise ValueError("Must run Stage 1 first")
        if self.job_description is None:
            self.load_job_description()
        
        input_df = self.ranked_dfs['stage_2'].head(100) if 'stage_2' in self.ranked_dfs else self.df
        ranker = EmbeddingRanker()
        results, ranked_df = ranker.run(input_df, self.job_description, top_k)
        ranker.save_results(results, str(STAGE_3_OUTPUT))
        self.stage_results['stage_3'] = results
        self.ranked_dfs['stage_3'] = ranked_df
    
    def run_stage_4(self, top_k: int = 10) -> None:
        """Run Stage 4."""
        if self.job_description is None:
            self.load_job_description()
        
        input_df = self.ranked_dfs['stage_3'].head(50) if 'stage_3' in self.ranked_dfs else self.df.head(50)
        ranker = GeminiRanker()
        results, ranked_df = ranker.run(input_df, self.job_description, top_k)
        ranker.save_results(results, str(STAGE_4_OUTPUT))
        self.stage_results['stage_4'] = results
        self.ranked_dfs['stage_4'] = ranked_df
    
    def run_stage_5(self, top_k: int = 10) -> None:
        """Run Stage 5."""
        if self.job_description is None:
            self.load_job_description()
        
        input_df = self.ranked_dfs['stage_4'].head(50) if 'stage_4' in self.ranked_dfs else self.df.head(50)
        ranker = ImprovedGeminiRanker()
        results, ranked_df = ranker.run(input_df, self.job_description, top_k)
        ranker.save_results(results, str(STAGE_5_OUTPUT))
        self.stage_results['stage_5'] = results
        self.ranked_dfs['stage_5'] = ranked_df
    
    def load_job_description(self, custom_path: Optional[str] = None) -> None:
        """Load job description."""
        self.job_description = self.loader.load_job_description(self.role, custom_path)
    
    def run_all(self, role: str, stages: list = None) -> None:
        """Run all stages."""
        if stages is None:
            stages = [1, 2, 3, 4, 5]
        
        if 1 in stages:
            self.run_stage_1(role)
        self.load_job_description()
        if 2 in stages:
            self.run_stage_2()
        if 3 in stages:
            self.run_stage_3()
        if 4 in stages:
            self.run_stage_4()
        if 5 in stages:
            if 4 in stages:
                print("\n[Cooldown] Waiting 65s for Gemini rate limit window to reset...")
                time.sleep(65)
            self.run_stage_5()
        
        print("\n" + "="*70 + "\nALL STAGES COMPLETED\n" + "="*70)
    
    def compute_metrics(self) -> None:
        """Compute metrics."""
        print("\n" + "="*70 + "\nCOMPUTING TRUST METRICS\n" + "="*70)
        metrics = TrustMetrics.compute_all_metrics(self.stage_results)
        save_metrics(metrics)
