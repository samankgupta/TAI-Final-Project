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
        
        # Enforce rate limiting before making API call
        self.enforce_rate_limit()
        self.api_requests += 1
        
        max_retries = 5
        for attempt in range(max_retries):
            try:
                prompt = f"Rate this resume match for the job (1-10):\n\nJOB: {job_description[:500]}\n\nRESUME: {resume[:1000]}\n\nScore and brief reason:"
                response = self.client.models.generate_content(
                    model=GEMINI_MODEL_NAME,
                    contents=prompt,
                )
                text = response.text or ""

                score = 5
                import re
                match = re.search(r'\b([1-9]|10)\s*/\s*10\b', text)
                if match:
                    score = int(match.group(1))
                else:
                    match = re.search(r'(?:score|rating)[:\s]+([1-9]|10)\b', text, re.IGNORECASE)
                    if match:
                        score = int(match.group(1))
                    else:
                        for part in text.split():
                            try:
                                num = int(part.strip('.,;:()'))
                                if 1 <= num <= 10:
                                    score = num
                                    break
                            except:
                                pass
                score = min(10, max(1, score))
                result = {'score': score, 'reasoning': text[:150], 'is_mock': False}

                if USE_API_CACHE:
                    self.save_cached_response(cache_key, result)

                return result
            except Exception as e:
                if '429' in str(e) and attempt < max_retries - 1:
                    wait_time = 20 * (attempt + 1)
                    print(f"  [429 RETRY {attempt+1}/{max_retries-1}] Waiting {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    raise RuntimeError(f"Gemini scoring failed: {e}") from e
    
    def run(self, df: pd.DataFrame, job_description: str, top_k: int = TOP_K_STAGE_4) -> Dict:
        """Run Stage 4: Gemini-based ranking."""
        print(f"\n{'='*60}\nSTAGE 4: GEMINI RANKING (BASE)")
        print(f"Scoring {len(df)} resumes... (Rate limit: {self.MAX_REQUESTS_PER_MINUTE} req/min)")
        
        scores = []
        reasonings = []
        for idx, (_, row) in enumerate(df.iterrows()):
            if (idx + 1) % 5 == 0:
                print(f"  Scored {idx + 1}/{len(df)}")
            
            result = self.rank_resume_with_gemini(job_description, row['Resume'])
            scores.append(result['score'])
            reasonings.append(result.get('reasoning', ''))
        
        ranking_df = df.copy()
        ranking_df['gemini_score'] = scores
        ranking_df['gemini_reasoning'] = reasonings
        ranking_df = ranking_df.sort_values('gemini_score', ascending=False).reset_index(drop=True)
        top_k_df = ranking_df.head(top_k)
        
        results = {
            'stage': 4,
            'stage_name': 'Gemini Ranking (Base)',
            'parameters': {'method': 'Gemini API', 'top_k': top_k, 'rate_limit': f'{self.MAX_REQUESTS_PER_MINUTE}/min'},
            'cache_stats': {'hits': self.cache_hits, 'misses': self.cache_misses, 'api_requests': self.api_requests},
            'input_count': len(df),
            'output_count': len(top_k_df),
            'retention_rate': len(top_k_df) / len(df),
            'score_stats': {'min': min(scores), 'max': max(scores), 'mean': sum(scores)/len(scores)},
            'ranked_resumes': []
        }
        
        for idx, (_, row) in enumerate(top_k_df.iterrows(), 1):
            results['ranked_resumes'].append({
                'rank': idx,
                'candidate_id': int(row['candidate_id']) if 'candidate_id' in row else idx - 1,
                'gemini_score': int(row['gemini_score']),
                'reasoning': row.get('gemini_reasoning', ''),
            })
        print(f"Input: {len(df)} | Output: {len(top_k_df)}")
        print(f"API Requests: {self.api_requests} | Cache Hits: {self.cache_hits} | Cache Misses: {self.cache_misses}")
        
        return results, ranking_df
    
    def save_results(self, results: Dict, output_path: str = str(STAGE_4_OUTPUT)) -> None:
        """Save results."""
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"Results saved to {output_path}")
