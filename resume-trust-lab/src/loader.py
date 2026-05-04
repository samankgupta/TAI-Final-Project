"""Data loader for resumes and job descriptions."""

import pandas as pd
import json
from typing import List, Dict, Tuple
from pathlib import Path
import sys
import re

from config import DATASET_PATH, JOB_DESC_PATH, OUTPUT_DIR


class DataLoader:
    """Loads and manages resume and job description data."""
    
    def __init__(self, dataset_path: str = DATASET_PATH):
        """Initialize loader with dataset path."""
        self.dataset_path = dataset_path
        self.df = None
        self.job_description = None
        self.unique_roles = None

    @staticmethod
    def clean_resume_text(text: str) -> str:
        """Remove known boilerplate/template text from resumes."""
        if text is None:
            return ""

        cleaned = str(text)

        # Remove common generated intro headers.
        cleaned = re.sub(
            r"^\s*Here(?:'|’)s\s+(?:a\s+)?(?:professional\s+|sample\s+)?resume\s+for[^:]*:\s*",
            "",
            cleaned,
            flags=re.IGNORECASE,
        )
        cleaned = re.sub(
            r"^\s*Here\s+is\s+(?:a\s+)?(?:professional\s+|sample\s+)?resume\s+for[^:]*:\s*",
            "",
            cleaned,
            flags=re.IGNORECASE,
        )

        # Remove known generic disclaimer blocks that are not candidate data.
        boilerplate_patterns = [
            r"Note:\s*This is just a sample resume, and you should customize it to fit your specific experience and the job you\s*'?re applying for\.?",
            r"Also, make sure to proofread your resume multiple times for any grammar or formatting errors\.?",
            r"This is just a sample, but you can customize it to fit your specific experience and the job you\s*'?re applying for\.?",
            r"This is just a sample, and you should customize yours to fit your specific experience and the job you\s*'?re applying for\.?",
            r"Remember to use language from the job posting and highlight your achievements and skills that align with the requirements\.?",
            r"Good luck with your job search!?",
            r"I hope this helps!?",
            r"I hope this sample resume helps!?",
            r"Let me know if you\s*'?d like me to make any changes\.?",
            r"Remember to customize your resume to fit your specific experience and the job you\s*'?re applying for\.?",
        ]
        for pattern in boilerplate_patterns:
            cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)

        # Convert markdown-style email links to plain text.
        cleaned = re.sub(r"\[([^\]]+)\]\(mailto:[^)]+\)", r"\1", cleaned)

        # Normalize whitespace.
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        return cleaned
        
    def load_dataset(self, sample_size: int = None, random_seed: int = 42) -> pd.DataFrame:
        """Load resume dataset."""
        print(f"Loading dataset from {self.dataset_path}...")
        
        try:
            if sample_size:
                self.df = pd.read_csv(self.dataset_path, nrows=sample_size)
                print(f"Loaded {len(self.df)} resume samples")
            else:
                self.df = pd.read_csv(self.dataset_path)
                print(f"Loaded {len(self.df)} resumes total")
        
        except Exception as e:
            print(f"Error loading dataset: {e}")
            sys.exit(1)

        # Clean resume text before any downstream ranking stages.
        if 'Resume' in self.df.columns:
            self.df['Resume_raw'] = self.df['Resume'].astype(str)
            self.df['Resume'] = self.df['Resume'].apply(self.clean_resume_text)
            
        # Get unique roles
        self.unique_roles = self.df['Role'].unique().tolist()
        print(f"Found {len(self.unique_roles)} unique roles")
        print(f"Roles: {', '.join(self.unique_roles[:10])}")
        if len(self.unique_roles) > 10:
            print(f"... and {len(self.unique_roles) - 10} more")
            
        return self.df
    
    def load_job_description(self, role: str = None, custom_path: str = None) -> str:
        """Load job description."""
        path = custom_path or JOB_DESC_PATH
        
        if not Path(path).exists():
            print(f"Warning: Job description not found at {path}")
            return f"Job Description for {role or 'E-commerce Specialist'}"
        
        with open(path, 'r') as f:
            self.job_description = f.read()
            print(f"Loaded job description ({len(self.job_description)} chars)")
            
        return self.job_description
    
    def filter_by_role(self, role: str, fuzzy: bool = False) -> Tuple[pd.DataFrame, int]:
        """Filter resumes by role."""
        if self.df is None:
            raise ValueError("Dataset not loaded. Call load_dataset() first.")
        
        if fuzzy:
            mask = self.df['Role'].str.contains(role, case=False, na=False)
        else:
            mask = self.df['Role'].str.lower() == role.lower()
        
        filtered_df = self.df[mask].reset_index(drop=True)
        original_count = len(self.df)
        filtered_count = len(filtered_df)
        
        print(f"Filtered {original_count} resumes by role '{role}'")
        print(f"Result: {filtered_count} resumes ({100*filtered_count/original_count:.1f}%)")
        
        return filtered_df, original_count
    
    def get_ground_truth(self, df: pd.DataFrame) -> Dict:
        """Extract ground truth decisions from dataset."""
        if 'Decision' not in df.columns:
            return {}
        
        selected = int((df['Decision'].str.lower() == 'select').sum())
        rejected = int((df['Decision'].str.lower() == 'reject').sum())
        total = int(len(df))
        
        ground_truth = {
            'total': total,
            'selected': selected,
            'rejected': rejected,
            'select_rate': float(selected / total) if total > 0 else 0.0
        }
        
        print(f"\nGround truth distribution:")
        print(f"  Selected: {selected} ({100*ground_truth['select_rate']:.1f}%)")
        print(f"  Rejected: {rejected} ({100*(1-ground_truth['select_rate']):.1f}%)")
        
        return ground_truth
    
    def get_role_statistics(self) -> Dict:
        """Get statistics about roles in dataset."""
        if self.df is None:
            raise ValueError("Dataset not loaded")
            
        stats = self.df['Role'].value_counts().to_dict()
        return stats
