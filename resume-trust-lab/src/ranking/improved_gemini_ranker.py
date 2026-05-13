"""Stage 5: Improved Gemini ranking with hallucination detection."""

import json
from typing import Dict, List, Optional, Tuple
import pandas as pd
from pathlib import Path
import hashlib
import time
import re
from collections import deque

from config import STAGE_5_OUTPUT, TOP_K_STAGE_4, GEMINI_API_KEY, USE_API_CACHE, CACHE_DIR, GEMINI_MODEL_NAME


class ImprovedGeminiRanker:
    """Ranks resumes with grounding rules and hallucination detection."""
    
    # Rate limiting: max 13 requests per minute
    MAX_REQUESTS_PER_MINUTE = 13
    MIN_INTERVAL_SECONDS = 60.0 / MAX_REQUESTS_PER_MINUTE
    
    def __init__(self, api_key: str = GEMINI_API_KEY):
        self.api_key = api_key
        self.cache_dir = Path(CACHE_DIR)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_hits = 0
        self.cache_misses = 0
        self.api_requests = 0
        self.hallucinations_detected = 0
        
        # Rate limiting queue
        self.request_times = deque(maxlen=self.MAX_REQUESTS_PER_MINUTE)
        
        if not api_key:
            raise ValueError("GEMINI_API_KEY is required for Gemini ranking")

        try:
            from google import genai
            self.client = genai.Client(api_key=api_key)
        except Exception as exc:
            raise RuntimeError(
                "google-genai is required. Install google-genai and retry."
            ) from exc
    
    def enforce_rate_limit(self) -> None:
        """Enforce rate limiting: max 13 requests per minute."""
        current_time = time.time()
        self.request_times.append(current_time)
        
        if len(self.request_times) == self.MAX_REQUESTS_PER_MINUTE:
            oldest_time = self.request_times[0]
            time_since_oldest = current_time - oldest_time
            
            if time_since_oldest < 60.0:
                wait_time = 60.0 - time_since_oldest
                print(f"  [RATE LIMIT] Waiting {wait_time:.1f}s to stay under 13 req/min...")
                time.sleep(wait_time)
    
    def detect_hallucinations(self, resume: str, claimed_skills: List[str]) -> Dict:
        """Detect hallucinated skills."""
        resume_lower = self._normalize_text(resume)
        hallucinated = []
        grounded = []

        alias_groups = {
            'google analytics': {'google analytics', 'google analytics 4', 'ga4', 'ga-4'},
            'seo': {'seo', 'search engine optimization'},
            'ppc': {'ppc', 'paid search', 'paid media'},
            'email marketing': {'email marketing', 'email campaigns'},
            'ux': {'ux', 'user experience', 'website ux'},
            'shopify': {'shopify', 'shopify plus'},
            'elementor': {'elementor'},
            'excel': {'excel', 'pivot tables', 'vlookups', 'vlookup'},
        }

        def is_present(skill: str) -> bool:
            normalized = self._normalize_text(skill)
            if normalized in resume_lower:
                return True
            for canonical, aliases in alias_groups.items():
                if normalized == canonical or normalized in aliases:
                    if any(alias in resume_lower for alias in aliases):
                        return True
            return False
        
        for skill in claimed_skills:
            if is_present(skill):
                grounded.append(skill)
            else:
                hallucinated.append(skill)
        
        return {
            'hallucinated': hallucinated,
            'count': len(hallucinated),
            'rate': len(hallucinated) / len(claimed_skills) if claimed_skills else 0
        }

    def _normalize_text(self, text: str) -> str:
        """Normalize text for lightweight matching."""
        text = (text or "").lower()
        text = re.sub(r"[^a-z0-9\s\+]+", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def _is_incomplete_resume(self, resume: str) -> bool:
        """Detect obvious placeholder/sample resumes before scoring."""
        if not resume:
            return True

        placeholder_patterns = [
            r"\[insert [^\]]+\]",
            r"here'?s a sample",
            r"this is just a sample",
            r"lorem ipsum",
            r"placeholder",
        ]
        lower = resume.lower()
        return any(re.search(pattern, lower) for pattern in placeholder_patterns)
    
    def rank_resume_improved(self, job_description: str, resume: str, prev_gemini_reasoning: Optional[str] = None, prev_gemini_score: Optional[float] = None) -> Dict:
        """Rank resume with grounding."""
        cache_key = hashlib.md5(f"{job_description}|{resume}|{prev_gemini_reasoning}|{prev_gemini_score}|improved_v5".encode()).hexdigest()
        
        if USE_API_CACHE:
            cache_file = self.cache_dir / f"{cache_key}.json"
            if cache_file.exists():
                with open(cache_file, 'r') as f:
                    self.cache_hits += 1
                    return json.load(f)
        
        self.cache_misses += 1

        # Hard stop for obviously incomplete resumes so they do not get inflated scores.
        if self._is_incomplete_resume(resume):
            result = {
                'score': 1.0,
                'raw_score': 1,
                'hallucinated': [],
                'hallucination_rate': 1.0,
                'reasoning': 'Incomplete/placeholder resume detected; score capped.',
                'is_mock': True,
                'resume_quality_flag': 'incomplete',
            }
            if USE_API_CACHE:
                try:
                    cache_file = self.cache_dir / f"{cache_key}.json"
                    with open(cache_file, 'w') as f:
                        json.dump(result, f)
                except:
                    pass
            return result
        
        # Enforce rate limiting before API call
        self.enforce_rate_limit()
        self.api_requests += 1
        
        max_retries = 5
        for attempt in range(max_retries):
            try:
                # Build prompt that includes previous Gemini reasoning (if available)
                prev_block = ""
                if prev_gemini_score is not None or prev_gemini_reasoning:
                    prev_block = (
                        f"PREVIOUS_STAGE4_SCORE: {prev_gemini_score if prev_gemini_score is not None else 'NA'}\n"
                        f"PREVIOUS_STAGE4_REASONING: {prev_gemini_reasoning or ''}\n\n"
                    )
                prompt = (
                    f"Score this resume only on evidence that appears in the text. Be strict.\n"
                    f"Give a 1-10 score and keep the reason to one sentence.\n"
                    f"Do not exceed 8 unless the resume explicitly supports nearly all requirements.\n\n"
                    f"{prev_block}"
                    f"JOB: {job_description[:1400]}\n\nRESUME: {resume[:4000]}\n\n"
                    f"Respond exactly in this format:\nScore: X\nSkills: skill1, skill2, skill3\nReason: one sentence"
                )
                response = self.client.models.generate_content(
                    model=GEMINI_MODEL_NAME,
                    contents=prompt,
                )
                text = response.text or ""

                score = 5
                skills = []
                for line in text.split('\n'):
                    line_lower = line.lower().strip()
                    if line_lower.startswith('score:'):
                        try:
                            raw = line.split(':', 1)[1].strip().split()[0]
                            score = min(10, max(1, int(raw.split('/')[0])))
                        except:
                            pass
                    elif line_lower.startswith('skills:'):
                        skills_str = line.split(':', 1)[1].strip()
                        skills = [s.strip() for s in skills_str.split(',') if s.strip()]

                hallucination_result = self.detect_hallucinations(resume, skills)
                self.hallucinations_detected += hallucination_result['count']
                adjusted_score = round(score * (1 - hallucination_result['rate']), 2)

                # Cap scores if the model claims too much relative to available evidence.
                if hallucination_result['rate'] >= 0.5:
                    adjusted_score = min(adjusted_score, 4.0)
                elif hallucination_result['rate'] >= 0.25:
                    adjusted_score = min(adjusted_score, 7.0)

                result = {
                    'score': adjusted_score,
                    'raw_score': score,
                    'hallucinated': hallucination_result['hallucinated'],
                    'hallucination_rate': hallucination_result['rate'],
                    'reasoning': text.splitlines()[0][:120] if text else '',
                    'is_mock': False
                }

                try:
                    cache_file = self.cache_dir / f"{cache_key}.json"
                    with open(cache_file, 'w') as f:
                        json.dump(result, f)
                except:
                    pass

                return result
            except Exception as e:
                err = str(e)
                if ('429' in err or '503' in err) and attempt < max_retries - 1:
                    wait_time = 20 * (attempt + 1)
                    code = '429' if '429' in err else '503'
                    print(f"  [{code} RETRY {attempt+1}/{max_retries-1}] Waiting {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    raise RuntimeError(f"Improved Gemini scoring failed: {e}") from e

        raise RuntimeError("Improved Gemini scoring failed after all retries")
    
    def run(self, df: pd.DataFrame, job_description: str, top_k: int = TOP_K_STAGE_4) -> Tuple[Dict, pd.DataFrame]:
        """Run Stage 5."""
        print(f"\n{'='*60}\nSTAGE 5: IMPROVED GEMINI (WITH GROUNDING)")
        print(f"Scoring {len(df)} resumes... (Rate limit: {self.MAX_REQUESTS_PER_MINUTE} req/min)")

        if df is None or df.empty:
            results = {
                'stage': 5,
                'stage_name': 'Improved Gemini (With Grounding)',
                'parameters': {'method': 'Gemini with Grounding', 'top_k': top_k, 'rate_limit': f'{self.MAX_REQUESTS_PER_MINUTE}/min'},
                'cache_stats': {'hits': self.cache_hits, 'misses': self.cache_misses, 'api_requests': self.api_requests},
                'hallucination_stats': {'detected': self.hallucinations_detected, 'avg_rate': 0.0},
                'input_count': 0,
                'output_count': 0,
                'retention_rate': 0.0,
                'score_stats': {'min': 0, 'max': 0, 'mean': 0},
                'ranked_resumes': []
            }
            print("No resumes available for Stage 5; skipping improved Gemini ranking.")
            return results, df.copy() if df is not None else pd.DataFrame()
        
        scores = []
        raw_scores = []
        hallucination_rates = []
        reasonings = []

        for idx, (_, row) in enumerate(df.iterrows()):
            if (idx + 1) % 5 == 0:
                print(f"  Scored {idx + 1}/{len(df)}")

            prev_reasoning = row.get('gemini_reasoning') or row.get('reasoning') or ''
            raw_prev_score = row.get('gemini_score')
            prev_score = float(raw_prev_score) if raw_prev_score is not None else None
            result = self.rank_resume_improved(job_description, row['Resume'], prev_gemini_reasoning=prev_reasoning, prev_gemini_score=prev_score)
            scores.append(result['score'])
            raw_scores.append(result['raw_score'])
            hallucination_rates.append(result['hallucination_rate'])
            reasonings.append(result.get('reasoning', ''))

        ranking_df = df.copy()
        ranking_df['improved_score'] = scores
        ranking_df['raw_score'] = raw_scores
        ranking_df['hallucination_rate'] = hallucination_rates
        ranking_df['improved_reasoning'] = reasonings
        ranking_df = ranking_df.sort_values('improved_score', ascending=False).reset_index(drop=True)
        top_k_df = ranking_df.head(top_k)
        
        results = {
            'stage': 5,
            'stage_name': 'Improved Gemini (With Grounding)',
            'parameters': {'method': 'Gemini with Grounding', 'top_k': top_k, 'rate_limit': f'{self.MAX_REQUESTS_PER_MINUTE}/min'},
            'cache_stats': {'hits': self.cache_hits, 'misses': self.cache_misses, 'api_requests': self.api_requests},
            'hallucination_stats': {'detected': self.hallucinations_detected, 'avg_rate': sum(hallucination_rates) / len(hallucination_rates) if hallucination_rates else 0},
            'input_count': len(df),
            'output_count': len(top_k_df),
            'retention_rate': len(top_k_df) / len(df),
            'score_stats': {'min': min(scores) if scores else 0, 'max': max(scores) if scores else 0, 'mean': sum(scores) / len(scores) if scores else 0},
            'ranked_resumes': []
        }
        
        for idx, (_, row) in enumerate(top_k_df.iterrows(), 1):
            results['ranked_resumes'].append({
                'rank': idx,
                'candidate_id': int(row['candidate_id']) if 'candidate_id' in row else idx - 1,
                'improved_score': float(row['improved_score']),
                'raw_score': int(row['raw_score']) if 'raw_score' in row else int(row['improved_score']),
                'hallucination_rate': float(row['hallucination_rate']),
                'reasoning': row.get('improved_reasoning', ''),
                'resume': row.get('Resume', ''),
            })
        print(f"Input: {len(df)} | Output: {len(top_k_df)}")
        print(f"API Requests: {self.api_requests} | Cache Hits: {self.cache_hits} | Cache Misses: {self.cache_misses}")
        
        return results, ranking_df
    
    def save_results(self, results: Dict, output_path: str = str(STAGE_5_OUTPUT)) -> None:
        """Save results."""
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"Results saved to {output_path}")
