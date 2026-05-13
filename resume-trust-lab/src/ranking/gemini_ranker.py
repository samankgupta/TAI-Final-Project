"""Stage 4: Gemini API-based ranking (basic version)."""

import json
from typing import Dict, List
import pandas as pd
from pathlib import Path
import hashlib
import time
from collections import deque

from config import STAGE_4_OUTPUT, TOP_K_STAGE_4, GEMINI_API_KEY, USE_API_CACHE, CACHE_DIR, GEMINI_MODEL_NAME


class GeminiRanker:
    """Ranks resumes using Google Gemini API with rate limiting."""
    
    # Rate limiting: max 13 requests per minute = ~4.6 seconds per request
    MAX_REQUESTS_PER_MINUTE = 13
    MIN_INTERVAL_SECONDS = 60.0 / MAX_REQUESTS_PER_MINUTE  # ~4.6 seconds
    
    def __init__(self, api_key: str = GEMINI_API_KEY):
        self.api_key = api_key
        self.cache_dir = Path(CACHE_DIR)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_hits = 0
        self.cache_misses = 0
        self.api_requests = 0
        
        # Rate limiting queue: track last 13 request times
        self.request_times = deque(maxlen=self.MAX_REQUESTS_PER_MINUTE)
        self.last_request_time = 0
        
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
        
        # If we have 13 requests, check if the oldest was within the last minute
        if len(self.request_times) == self.MAX_REQUESTS_PER_MINUTE:
            oldest_time = self.request_times[0]
            time_since_oldest = current_time - oldest_time
            
            # If oldest request is less than 60 seconds old, we need to wait
            if time_since_oldest < 60.0:
                wait_time = 60.0 - time_since_oldest
                print(f"  [RATE LIMIT] Waiting {wait_time:.1f}s to stay under 13 req/min...")
                time.sleep(wait_time)
    
    def get_cache_key(self, job_description: str, resume: str) -> str:
        """Generate cache key."""
        combined = f"{job_description}|{resume}"
        return hashlib.md5(combined.encode()).hexdigest()
    
    def get_cached_response(self, cache_key: str) -> Dict or None:
        """Get cached response."""
        cache_file = self.cache_dir / f"{cache_key}.json"
        if cache_file.exists():
            try:
                with open(cache_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return None
    
    def save_cached_response(self, cache_key: str, response: Dict) -> None:
        """Save cached response."""
        try:
            cache_file = self.cache_dir / f"{cache_key}.json"
            with open(cache_file, 'w') as f:
                json.dump(response, f)
        except:
            pass
    
    def rank_resume_with_gemini(self, job_description: str, resume: str) -> Dict:
        """Rank a single resume using Gemini API."""
        cache_key = self.get_cache_key(job_description, resume)
        
        if USE_API_CACHE:
            cached = self.get_cached_response(cache_key)
            if cached:
                self.cache_hits += 1
                return cached
        
        self.cache_misses += 1
        
        # Enforce rate limiting before making API call (sliding window)
        self.enforce_rate_limit()
        
        max_retries = 4
        backoff_base = 3
        for attempt in range(1, max_retries + 1):
            try:
                # Build a shorter prompt to reduce model processing time
                prompt = (
                    f"Rate this resume match for the job (1-100). Return score and one-line reason only:\n\n"
                    f"JOB: {job_description[:300]}\n\n"
                    f"RESUME: {resume[:800]}\n\n"
                    f"Score (1-100) and one-line reason:"
                )
                response = self.client.models.generate_content(
                    model=GEMINI_MODEL_NAME,
                    contents=prompt,
                )
                # record last request time on success and track request timestamp
                now = time.time()
                self.last_request_time = now
                self.request_times.append(now)
                self.api_requests += 1

                text = getattr(response, 'text', '') or ''

                # parse integer score between 1 and 100
                score = None
                import re
                # look for patterns like '85/100' or '85 / 100' or '85'
                m = re.search(r'\b([1-9][0-9]?|100)\s*/\s*100\b', text)
                if m:
                    score = int(m.group(1))
                else:
                    m = re.search(r'(?:score|rating)[:\s]+([1-9][0-9]?|100)\b', text, re.IGNORECASE)
                    if m:
                        score = int(m.group(1))
                    else:
                        # fallback: find any standalone integer 1-100
                        for part in re.findall(r'\b\d{1,3}\b', text):
                            try:
                                num = int(part)
                                if 1 <= num <= 100:
                                    score = num
                                    break
                            except:
                                continue

                # If model returned 1-10 (common), scale to 1-100
                if score is None:
                    # default neutral score
                    score = 50
                elif 1 <= score <= 10:
                    score = score * 10
                else:
                    score = min(100, max(1, score))

                result = {'score': score, 'reasoning': text.splitlines()[0][:120] if text else '', 'is_mock': False}

                if USE_API_CACHE:
                    self.save_cached_response(cache_key, result)

                return result
            except Exception as e:
                err_str = str(e)
                # If transient (rate or service), backoff and retry
                if (('429' in err_str or 'UNAVAILABLE' in err_str or '503' in err_str)
                        and attempt < max_retries):
                    wait_time = backoff_base * attempt
                    print(f"  [TRANSIENT ERROR] {err_str}. Retry {attempt}/{max_retries} after {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                # Non-retriable or out of retries
                raise RuntimeError(f"Gemini scoring failed: {e}") from e
    
    def run(self, df: pd.DataFrame, job_description: str, top_k: int = TOP_K_STAGE_4) -> Dict:
        """Run Stage 4: Gemini-based ranking."""
        print(f"\n{'='*60}\nSTAGE 4: GEMINI RANKING (BASE)")
        print(f"Scoring {len(df)} resumes... (Rate limit: {self.MAX_REQUESTS_PER_MINUTE} req/min)")

        if df is None or df.empty:
            results = {
                'stage': 4,
                'stage_name': 'Gemini Ranking (Base)',
                'parameters': {'method': 'Gemini API', 'requested_top_k': top_k, 'rate_limit': f'{self.MAX_REQUESTS_PER_MINUTE}/min'},
                'cache_stats': {'hits': self.cache_hits, 'misses': self.cache_misses, 'api_requests': self.api_requests},
                'input_count': 0,
                'output_count': 0,
                'retention_rate': 0.0,
                'score_stats': {'min': 0, 'max': 0, 'mean': 0},
                'ranked_resumes': []
            }
            print("No resumes available for Stage 4; skipping Gemini ranking.")
            return results, df.copy() if df is not None else pd.DataFrame()
        
        scores = []
        reasonings = []
        for idx, (_, row) in enumerate(df.iterrows()):
            # Print progress for each resume so user sees current index out of total
            try:
                cid = int(row.get('candidate_id')) if 'candidate_id' in row else idx
            except Exception:
                cid = idx
            print(f"  Scoring {idx + 1}/{len(df)} (candidate {cid})")

            result = self.rank_resume_with_gemini(job_description, row['Resume'])
            scores.append(result['score'])
            reasonings.append(result.get('reasoning', ''))
        
        ranking_df = df.copy()
        ranking_df['gemini_score'] = scores
        ranking_df['gemini_reasoning'] = reasonings
        ranking_df = ranking_df.sort_values('gemini_score', ascending=False).reset_index(drop=True)

        # Prepare results that include ALL scored resumes (e.g., 50), with ranks
        scored_count = len(ranking_df)
        results = {
            'stage': 4,
            'stage_name': 'Gemini Ranking (Base)',
            'parameters': {
                'method': 'Gemini API',
                'requested_top_k': top_k,
                'scored_count': scored_count,
                'rate_limit': f'{self.MAX_REQUESTS_PER_MINUTE}/min'
            },
            'cache_stats': {'hits': self.cache_hits, 'misses': self.cache_misses, 'api_requests': self.api_requests},
            'input_count': len(df),
            'output_count': scored_count,
            'retention_rate': scored_count / len(df) if len(df) > 0 else 0,
            'score_stats': {'min': min(scores), 'max': max(scores), 'mean': sum(scores)/len(scores) if scores else 0},
            'ranked_resumes': []
        }

        for idx, (_, row) in enumerate(ranking_df.iterrows(), 1):
            results['ranked_resumes'].append({
                'rank': idx,
                'candidate_id': int(row['candidate_id']) if 'candidate_id' in row else idx - 1,
                'gemini_score': int(row['gemini_score']),
                'reasoning': row.get('gemini_reasoning', ''),
                'resume': row.get('Resume', ''),
                'job_description': job_description,
            })
        print(f"Input: {len(df)} | Scored: {scored_count}")
        print(f"API Requests: {self.api_requests} | Cache Hits: {self.cache_hits} | Cache Misses: {self.cache_misses}")
        
        return results, ranking_df
    
    def save_results(self, results: Dict, output_path: str = str(STAGE_4_OUTPUT)) -> None:
        """Save results."""
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"Results saved to {output_path}")
