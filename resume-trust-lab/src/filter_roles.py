"""Stage 1: Role-based filtering."""

import json
from typing import Dict, List
import pandas as pd
from pathlib import Path

from config import STAGE_1_OUTPUT


class RoleFilter:
    """Filters resumes by job role."""
    
    def filter_by_role(self, df: pd.DataFrame, role: str, fuzzy: bool = False) -> pd.DataFrame:
        """Filter resumes by role."""
        if fuzzy:
            mask = df['Role'].str.contains(role, case=False, na=False)
        else:
            mask = df['Role'].str.lower() == role.lower()
        
        return df[mask].reset_index(drop=True)
    
    def run(self, df: pd.DataFrame, role: str, fuzzy: bool = False) -> Dict:
        """Run Stage 1 filtering."""
        original_count = len(df)
        filtered_df = self.filter_by_role(df, role, fuzzy)
        filtered_count = len(filtered_df)
        
        results = {
            'stage': 1,
            'stage_name': 'Role Filtering',
            'parameters': {'role': role, 'fuzzy_match': fuzzy},
            'input_count': original_count,
            'output_count': filtered_count,
            'retention_rate': filtered_count / original_count if original_count > 0 else 0,
            'resumes': []
        }
        
        for idx, row in filtered_df.iterrows():
            results['resumes'].append({
                'id': idx,
                'role': row['Role'],
                'resume': row['Resume'],
            })
        
        print(f"\n{'='*60}\nSTAGE 1: ROLE FILTERING")
        print(f"Input:  {original_count:,} resumes\nOutput: {filtered_count:,} resumes ({100*results['retention_rate']:.2f}%)")
        
        return results, filtered_df
    
    def save_results(self, results: Dict, output_path: str = str(STAGE_1_OUTPUT)) -> None:
        """Save stage results to JSON."""
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"Results saved to {output_path}")
