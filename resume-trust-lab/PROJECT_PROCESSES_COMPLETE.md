# Resume Trust Lab — Complete Process Documentation

## Project Overview

**Resume Trust Lab** is an AI-assisted resume screening system designed to evaluate and rank candidate resumes across a multi-stage pipeline. It combines multiple ranking algorithms with trustworthiness validation to produce reliable hiring recommendations.

**Core Mission:** Filter and rank thousands of resumes into a small set of verified, high-quality candidates using AI with measurable trust metrics.

---

## Table of Contents

1. [High-Level Architecture](#high-level-architecture)
2. [Stage-by-Stage Process](#stage-by-stage-process)
3. [Data Flow & Transformation](#data-flow--transformation)
4. [Ranking Algorithms](#ranking-algorithms)
5. [Trustworthiness Validation](#trustworthiness-validation)
6. [Configuration & Parameters](#configuration--parameters)
7. [Output & Results](#output--results)
8. [Performance & Metrics](#performance--metrics)
9. [Error Handling](#error-handling)
10. [Testing & Validation](#testing--validation)

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  INPUT LAYER                                                    │
├─────────────────────────────────────────────────────────────────┤
│ Dataset (10,000+ resumes) | Job Description | Role Query        │
└───────────────┬─────────────────────────────────────────────────┘
                │
┌───────────────▼─────────────────────────────────────────────────┐
│  STAGE 1: ROLE FILTERING                                        │
├─────────────────────────────────────────────────────────────────┤
│ Input: Full dataset                                              │
│ Process: Extract resumes for target role (fuzzy matching)       │
│ Output: ~100 role-matched resumes                               │
└───────────────┬─────────────────────────────────────────────────┘
                │
┌───────────────▼─────────────────────────────────────────────────┐
│  STAGE 2: KEYWORD MATCHING (TF-IDF Baseline)                    │
├─────────────────────────────────────────────────────────────────┤
│ Input: 100 role-matched resumes                                 │
│ Process: Rank by keyword overlap with job description           │
│ Output: Top 50 candidates                                       │
└───────────────┬─────────────────────────────────────────────────┘
                │
┌───────────────▼─────────────────────────────────────────────────┐
│  STAGE 3: SEMANTIC EMBEDDINGS (Sentence-Transformers)           │
├─────────────────────────────────────────────────────────────────┤
│ Input: Top 50 from Stage 2                                      │
│ Process: Rank by semantic similarity using embeddings           │
│ Output: Top 50 candidates                                       │
└───────────────┬─────────────────────────────────────────────────┘
                │
┌───────────────▼─────────────────────────────────────────────────┐
│  STAGE 4: LLM SCORING (Gemini Base)                              │
├─────────────────────────────────────────────────────────────────┤
│ Input: Top 50 from Stage 3                                      │
│ Process: Score 1-100 using Gemini API with rate limiting        │
│ Output: 50 scored candidates, top 5–10 selected                 │
└───────────────┬─────────────────────────────────────────────────┘
                │
┌───────────────▼─────────────────────────────────────────────────┐
│  STAGE 5: GROUNDING & TRUST (Improved Gemini)                   │
├─────────────────────────────────────────────────────────────────┤
│ Input: Top 50 from Stage 4                                      │
│ Process: Re-score with hallucination detection & completeness   │
│ Output: Final ranked list with trust metrics                    │
└───────────────┬─────────────────────────────────────────────────┘
                │
┌───────────────▼─────────────────────────────────────────────────┐
│  ANALYSIS & REPORTING                                           │
├─────────────────────────────────────────────────────────────────┤
│ Metrics: Accuracy, hallucination rate, coverage                 │
│ Comparison: Stage-to-stage consistency analysis                 │
│ Audit: Critical errors, overscoring, integrity flags            │
│ Output: JSON results + CSV exports + markdown reports           │
└─────────────────────────────────────────────────────────────────┘
```

---

## Stage-by-Stage Process

### STAGE 1: Role Filtering

**Purpose:** Extract resumes matching the target job role from the full dataset

**Process:**

1. **Load Dataset**
   - Source: `dataset.csv` (10,174 resumes with role labels)
   - Fields: candidate_id, name, email, resume_text, role, decision, etc.

2. **Role Normalization**
   - Standardize role names (e.g., "Software Engineer role" → "Software Engineer")
   - Support fuzzy matching for similar role names
   - Fallback to exact match if fuzzy disabled

3. **Filtering**
   - Exact match or fuzzy match on role field
   - Extract ground truth hiring decisions (Accept/Reject/Unknown)
   - Cap results to `max_role_matches` (default: 100)

4. **Cleaning**
   - Remove boilerplate resume text ("Here's a sample resume…")
   - Normalize whitespace and encoding
   - Validate non-empty resume text

5. **Output**
   - JSON with filtered candidates
   - Fields: candidate_id, name, email, resume, role, ground_truth
   - Example: E-commerce Specialist → ~200 matches (capped at 100)

**Key Code Location:** `src/filter_roles.py`

**Configuration:**

```python
max_role_matches = 100  # Maximum candidates per role
fuzzy_matching = True    # Allow fuzzy role name matching
```

---

### STAGE 2: Keyword Matching (TF-IDF Baseline)

**Purpose:** Rank candidates by keyword overlap with job description

**Process:**

1. **Load Job Description**
   - Source: Role-specific job description file
   - Extract key terms and phrases
   - Store for ranking comparison

2. **Vectorization**
   - Convert all resumes to TF-IDF vectors
   - Compute vector for job description
   - Technology: scikit-learn TfidfVectorizer

3. **Ranking**
   - Calculate cosine similarity between resume and JD vectors
   - Sort by similarity score (descending)
   - Select top `TOP_K_STAGE_2` candidates (default: 50)

4. **Output**
   - JSON with ranked candidates (scores 0.0–1.0)
   - Fields: rank, candidate_id, name, tfidf_score, resume
   - Reasoning: skill keyword coverage vs. JD

**Key Code Location:** `src/ranking/baseline_ranker.py`

**Configuration:**

```python
TOP_K_STAGE_2 = 50  # Keep top 50 from TF-IDF
```

**Performance:** ~1 second for 100 resumes

---

### STAGE 3: Semantic Embedding Ranking

**Purpose:** Rank candidates by semantic similarity using language models

**Process:**

1. **Model Loading**
   - Load `all-MiniLM-L6-v2` (sentence-transformers)
   - ~11M parameter BERT model for semantic understanding
   - Downloads on first run; cached locally

2. **Embedding Generation**
   - Convert each resume to embedding vector (384-dim)
   - Convert job description to embedding vector
   - Normalize vectors for comparison

3. **Similarity Calculation**
   - Compute cosine similarity (0.0–1.0)
   - Higher score = more semantically similar to JD
   - Sort by similarity descending

4. **Ranking**
   - Select top `TOP_K_STAGE_3` candidates (default: 50)
   - No filtering; rank all

5. **Output**
   - JSON with ranked candidates
   - Fields: rank, candidate_id, name, embedding_score, resume
   - Reasoning: semantic fit vs. JD meaning

**Key Code Location:** `src/ranking/embedding_ranker.py`

**Configuration:**

```python
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
TOP_K_STAGE_3 = 50
```

**Performance:** 10–15 seconds for 50 resumes (includes model load)

---

### STAGE 4: Gemini LLM Scoring

**Purpose:** Score candidates 1–100 using Google's Gemini API with trustworthy reasoning

**Process:**

1. **Rate Limiting Setup**
   - Enforce 13 requests/minute sliding window
   - Maintain request timestamp deque
   - Wait if limit exceeded before scoring next candidate

2. **Resume Preparation**
   - Full resume text (not truncated)
   - Job description full text
   - Candidate identifier for tracking

3. **Gemini Scoring**
   - Send prompt to `gemini-3.1-flash-lite` API
   - Request: score (1–10) + skills list + reasoning
   - Handle transient errors (503, 429) with exponential backoff

4. **Retry Logic**
   - Max 4 attempts
   - Backoff: 5s × attempt_number
   - Log each retry attempt

5. **Score Normalization**
   - Gemini 1–10 → multiply by 10 → 1–100
   - Or accept native 1–100 scores directly
   - Cap at 100; minimum 1

6. **Caching**
   - MD5 hash of (job_desc | resume) as key
   - Store response in `.cache/` directory
   - Reuse for identical inputs (same JD + resume)

7. **Output**
   - JSON with ranked candidates (scores 1–100)
   - Fields: rank, candidate_id, name, gemini_score, reasoning, skills_found, resume
   - Top 5–10 typically selected for Stage 5

**Key Code Location:** `src/ranking/gemini_ranker.py`

**Configuration:**

```python
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL_NAME = "gemini-3.1-flash-lite"
TOP_K_STAGE_4 = 5
USE_API_CACHE = True
```

**Performance:** ~12 resumes/minute (rate-limited by Gemini API quota)

**Cost:** ~$0.003 per resume (estimate using flash-lite pricing)

---

### STAGE 5: Grounding & Trust Validation (Improved Gemini)

**Purpose:** Re-score with trustworthiness checks (hallucination detection, completeness validation, grounding)

**Process:**

1. **Incomplete Resume Detection**
   - Regex scan for placeholder patterns: `[Insert ...]`, "sample resume", "lorem ipsum"
   - Cap score at 1.0 if incomplete
   - Flag for manual review

2. **Skill Hallucination Detection**
   - Parse Gemini Stage 4 reasoning (extracted skills)
   - Search resume for each claimed skill
   - Use alias-aware matching (GA4 ↔ Google Analytics 4, PPC ↔ Paid Search)
   - Calculate hallucination rate: false_positives / total_skills_claimed

3. **Score Adjustment**
   - Adjusted score = Gemini_score × (1 − hallucination_rate)
   - Apply penalties for high hallucination:
     - ≥50% hallucination rate: cap at 4.0
     - ≥25% hallucination rate: cap at 7.0

4. **Grounding Re-scoring**
   - Include Stage 4 score + reasoning in new prompt
   - Ask Gemini to re-score with grounding checks
   - Convert 1–10 to 1–100

5. **Output**
   - JSON with adjusted scores and trust metrics
   - Fields: rank, candidate_id, name, stage_5_score, hallucination_rate, incomplete_flag, trust_score, resume
   - Trust score ranges 0–10 reflecting confidence

**Key Code Location:** `src/ranking/improved_gemini_ranker.py`

**Configuration:**

```python
HALLUCINATION_PENALTY_THRESHOLD_HIGH = 0.5  # Cap at 4.0
HALLUCINATION_PENALTY_THRESHOLD_MED = 0.25  # Cap at 7.0
```

**Performance:** 5–7 minutes for 50 resumes

---

## Data Flow & Transformation

```
┌─────────────────────────────────────┐
│ Raw CSV Dataset                     │
│ (10,174 resumes)                    │
└──────────────┬──────────────────────┘
               │
               ▼ STAGE 1: Load & Filter by Role
┌─────────────────────────────────────┐
│ Filtered DataFrame                  │
│ (100 resumes, same role)            │
│ + ground_truth (Accept/Reject)      │
└──────────────┬──────────────────────┘
               │
               ▼ STAGE 2: TF-IDF Vectorization & Ranking
┌─────────────────────────────────────┐
│ TF-IDF Ranked DataFrame             │
│ (50 top resumes)                    │
│ + tfidf_score (0.0–1.0)             │
└──────────────┬──────────────────────┘
               │
               ▼ STAGE 3: Embedding Generation & Ranking
┌─────────────────────────────────────┐
│ Embedding Ranked DataFrame          │
│ (50 top resumes)                    │
│ + embedding_score (0.0–1.0)         │
└──────────────┬──────────────────────┘
               │
               ▼ STAGE 4: Gemini API Scoring
┌─────────────────────────────────────┐
│ Gemini Scored DataFrame             │
│ (50 scored resumes)                 │
│ + gemini_score (1–100)              │
│ + reasoning + skills_found          │
└──────────────┬──────────────────────┘
               │
               ▼ STAGE 5: Hallucination & Completeness Checks
┌─────────────────────────────────────┐
│ Final Ranked DataFrame              │
│ (50 resumes with trust metrics)     │
│ + stage_5_score (adjusted 1–100)    │
│ + hallucination_rate                │
│ + incomplete_flag                   │
│ + trust_score (0–10)                │
└─────────────────────────────────────┘
```

**File Formats:**

- **Input:** `dataset.csv` (pandas DataFrame)
- **Intermediate:** JSON files per stage (`stage_N.json`)
- **Vectors:** Stored in memory during execution
- **Cache:** `.cache/*.json` (MD5-keyed API responses)
- **Output:** Final JSON + CSV exports

---

## Ranking Algorithms

### Algorithm 1: Baseline Ranker (TF-IDF)

**Algorithm:** TF-IDF (Term Frequency–Inverse Document Frequency) + Cosine Similarity

**How it works:**

1. Vectorize all resumes and JD using TF-IDF
2. Compute cosine similarity between each resume and JD
3. Sort by similarity descending
4. Return top K

**Pros:**

- Fast (<1 second)
- Transparent (keyword-based)
- No API calls
- Good baseline

**Cons:**

- Ignores semantic meaning
- Keyword stuffing exploitable
- No context understanding

**Use Case:** Stage 2 filtering; initial rough ranking

**Technology:** scikit-learn TfidfVectorizer

---

### Algorithm 2: Embedding Ranker (Semantic Similarity)

**Algorithm:** Sentence-Transformers Embeddings + Cosine Similarity

**How it works:**

1. Load pretrained BERT model (`all-MiniLM-L6-v2`)
2. Generate embeddings for each resume and JD
3. Compute cosine similarity in embedding space
4. Sort by similarity descending
5. Return top K

**Pros:**

- Understands semantic meaning (contextual)
- Catches paraphrased skills
- Robustness to keyword variations
- No API calls (local model)

**Cons:**

- Model-dependent (fixed model)
- Slower than TF-IDF
- Requires GPU for speed (CPU fallback available)

**Use Case:** Stage 3 ranking; improve on TF-IDF with understanding

**Technology:** sentence-transformers (Hugging Face), 384-dim embeddings

---

### Algorithm 3: Gemini Ranker (LLM Base)

**Algorithm:** Large Language Model (Gemini) with Prompt-Based Scoring

**How it works:**

1. Create prompt: "Score this resume for fit with JD 1–10"
2. Include full resume and job description
3. Query Gemini API
4. Parse score (1–10) from response
5. Scale to 1–100
6. Rank by score descending
7. Return top K

**Pros:**

- Understands job requirements deeply
- Provides reasoning (explainable)
- Can weight required vs. optional skills
- Most accurate for high-stakes decisions

**Cons:**

- API calls required (latency, cost)
- Rate limited (13/min Gemini quota)
- Potential hallucination (fixed in Stage 5)
- Response parsing required

**Use Case:** Stage 4 scoring; authoritative ranking for final selection

**Technology:** Google Gemini API (`gemini-3.1-flash-lite`)

**Rate Limiting:**

- Max 13 requests/minute
- Sliding-window enforcement
- ~4–5 second delay between requests

**Cost:** ~$0.003 per 1,000 tokens (estimated)

---

### Algorithm 4: Improved Gemini Ranker (Grounding)

**Algorithm:** LLM with Hallucination Detection & Completeness Checks

**How it works:**

1. Check for incomplete resumes (placeholders)
2. Parse Stage 4 reasoning for claimed skills
3. Match skills to resume using aliases
4. Calculate hallucination rate
5. Re-score with grounding feedback
6. Apply penalties for hallucination
7. Adjust score = Gemini × (1 − hallucination_rate)
8. Return adjusted ranking

**Pros:**

- Detects and corrects LLM hallucinations
- Verifies claimed skills against actual resume
- Catches low-quality submissions
- Provides trust metrics

**Cons:**

- Additional API calls (Stage 4 data re-used)
- Alias matching rules must be maintained
- Regex-based detection has false negatives

**Use Case:** Stage 5 validation; trustworthiness filtering

**Technology:** Gemini API + regex + custom grounding logic

**Hallucination Detection:**

```
Alias groups: {
  'Google Analytics': {'GA', 'GA4', 'Google Analytics 4', ...},
  'PPC': {'PPC', 'Paid Search', 'Google Ads (paid)', ...},
  ...
}

For each skill in Stage 4 reasoning:
  If skill ∉ resume (with alias matching):
    hallucination_count += 1

hallucination_rate = hallucination_count / total_skills
```

---

### Algorithm 5: Ensemble Ranker (Optional)

**Algorithm:** Combine multiple rankers weighted

**Available Rankers:**

- Baseline (TF-IDF)
- Embedding (Semantic)
- Gemini (LLM)

**Combination Methods:**

1. **Weighted Average:** score = 0.2×TF-IDF + 0.3×Embedding + 0.5×Gemini
2. **Rank Fusion:** Combine rank positions across all rankers
3. **Voting:** Count votes per candidate

**Use Case:** Stage 2–3 optional enhancement; compare multiple signals

**Location:** `src/ranking/ensemble_ranker.py`

---

## Trustworthiness Validation

### Trust Metrics

#### 1. Hallucination Rate

**Definition:** Percentage of skills claimed by Gemini that don't appear in the resume

**Calculation:**

```
hallucination_rate = false_positive_skills / total_skills_claimed
```

**Interpretation:**

- 0%: No hallucinations (perfect grounding)
- 5–10%: Minor hallucinations (acceptable)
- 20%+: Significant hallucinations (review needed)
- 50%+: Critical hallucinations (disqualify)

**Penalty Application:**

- If hallucination_rate ≥ 50%: Score capped at 4.0 (out of 100)
- If hallucination_rate ≥ 25%: Score capped at 7.0

#### 2. Completeness Score

**Definition:** Detection of incomplete/placeholder resumes

**Checks:**

- Unfilled fields: `[Insert Email]`, `[Insert Phone]`
- Placeholder dates: `20XX`, `20XX–20XX`
- Boilerplate: "sample resume", "lorem ipsum"
- Non-resume content: embedded rejection letters

**Result:**

- Complete: Flag = False, score = Normal
- Incomplete: Flag = True, score capped at 1.0

#### 3. Score Consistency

**Definition:** Agreement between Stage 4 and Stage 5 scores

**Calculation:**

```
consistency_ratio = stage_5_score / stage_4_score
Agreement ranges:
  0.8–1.2: Good consistency (±20%)
  0.5–0.8: Moderate (hallucination detected)
  <0.5: Poor (significant hallucination or flags)
```

**Interpretation:** Shows whether Stage 5 grounding significantly changed ranking

#### 4. Coverage

**Definition:** Percentage of required job skills found in resume

**Calculation:**

```
required_skills = extract_from_jd(job_description)
found_skills = count_skills_in_resume(resume, required_skills)
coverage = found_skills / len(required_skills)
```

**Ranges:**

- 80%+: Excellent coverage
- 60–80%: Good coverage
- 40–60%: Moderate coverage
- <40%: Poor coverage

#### 5. Tier Assignment

**Definition:** Confidence level for hiring decision

**Rules:**

```
if hallucination_rate < 10% AND coverage > 70%:
  tier = "HIGH_CONFIDENCE"  # Ready to interview
elif hallucination_rate < 25% AND coverage > 50%:
  tier = "MODERATE_CONFIDENCE"  # Review then interview
elif incomplete_flag:
  tier = "DISQUALIFIED"  # Data quality issue
else:
  tier = "LOW_CONFIDENCE"  # Borderline
```

### Pre-Registered Failures (Expected Issues)

**Issue 1: Score Clustering**

- Expected: Multiple candidates tied at same score
- Root cause: Coarse 1–10 Gemini output scale
- Mitigation: Stage 5 differentiation through hallucination penalties

**Issue 2: Keyword Stuffing**

- Expected: Resume with all keywords scores high but lacks depth
- Root cause: Stage 2–3 don't understand context
- Mitigation: Stage 4 LLM scoring catches shallow matches

**Issue 3: Irrelevant Experience**

- Expected: Candidate with related role but different domain scores high
- Root cause: TF-IDF and embeddings match keywords
- Mitigation: Gemini scoring considers job-specific context

---

## Configuration & Parameters

### Dataset Configuration

```python
# src/config.py

# Data source
DATASET_PATH = "/path/to/dataset.csv"
JOB_DESC_PATH = "data/"

# Stage sizing (funnel)
TOP_K_STAGE_1 = 100   # Keep 100 from full dataset
TOP_K_STAGE_2 = 50    # Keep 50 from TF-IDF
TOP_K_STAGE_3 = 50    # Keep 50 from embeddings
TOP_K_STAGE_4 = 5     # Keep 5 from Gemini base
TOP_K_STAGE_5 = 5     # Keep 5 from improved Gemini
```

### Model Configuration

```python
# Embedding model
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # 11M params, 384-dim

# LLM model
GEMINI_MODEL_NAME = "gemini-3.1-flash-lite"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
```

### Rate Limiting

```python
# Gemini API quota
MAX_REQUESTS_PER_MINUTE = 13
SLIDING_WINDOW_SECONDS = 60

# Retry logic
MAX_RETRIES = 4
BACKOFF_BASE_SECONDS = 5  # 5s × attempt_number
```

### Caching

```python
# API response caching
USE_API_CACHE = True
CACHE_DIR = ".cache/"
CACHE_FORMAT = "json"  # MD5-keyed
```

### Scoring Parameters

```python
# Hallucination penalties
HALLUCINATION_THRESHOLD_HIGH = 0.50  # ≥50% → cap at 4.0
HALLUCINATION_THRESHOLD_MED = 0.25   # ≥25% → cap at 7.0

# Placeholder detection
INCOMPLETE_PATTERNS = [
    r'\[insert [^\]]+\]',
    r'20XX',
    r'lorem ipsum',
]
```

---

## Output & Results

### Stage Outputs

**Stage 1:** `outputs/stage_1.json`

```json
{
  "stage": 1,
  "role": "Software Engineer",
  "total_candidates": 100,
  "candidates": [
    {
      "rank": 1,
      "candidate_id": 5,
      "name": "John Doe",
      "email": "john@example.com",
      "resume": "Full resume text...",
      "decision": "ACCEPT"
    }
  ]
}
```

**Stage 2:** `outputs/stage_2.json`

```json
{
  "stage": 2,
  "role": "Software Engineer",
  "total_candidates": 50,
  "method": "baseline_ranker",
  "candidates": [
    {
      "rank": 1,
      "candidate_id": 5,
      "tfidf_score": 0.89,
      "resume": "Full resume..."
    }
  ]
}
```

**Stage 3:** `outputs/stage_3.json`

```json
{
  "stage": 3,
  "method": "embedding_ranker",
  "candidates": [
    {
      "rank": 1,
      "candidate_id": 12,
      "embedding_score": 0.92,
      "resume": "Full resume..."
    }
  ]
}
```

**Stage 4:** `outputs/stage_4.json`

```json
{
  "stage": 4,
  "method": "gemini_ranker",
  "candidates": [
    {
      "rank": 1,
      "candidate_id": 3,
      "gemini_score": 95,
      "reasoning": "Strong technical background with 5+ years experience...",
      "skills_found": ["Java", "Docker", "AWS"],
      "resume": "Full resume..."
    }
  ]
}
```

**Stage 5:** `outputs/stage_5.json`

```json
{
  "stage": 5,
  "method": "improved_gemini_ranker",
  "candidates": [
    {
      "rank": 1,
      "candidate_id": 3,
      "stage_4_score": 95,
      "stage_5_score": 92,
      "hallucination_rate": 0.05,
      "incomplete": false,
      "trust_score": 9.2,
      "tier": "HIGH_CONFIDENCE",
      "resume": "Full resume..."
    }
  ]
}
```

### Metrics Output: `outputs/metrics.json`

```json
{
  "role": "Software Engineer",
  "total_candidates": 100,
  "final_count": 5,
  "funnel_retention": {
    "stage_1_to_2": "50%",
    "stage_2_to_3": "100%",
    "stage_3_to_4": "100%",
    "stage_4_to_5": "100%"
  },
  "accuracy_metrics": {
    "stage_4_accuracy_vs_gt": 0.72,
    "stage_5_accuracy_vs_gt": 0.85,
    "hallucination_rate": 0.12
  },
  "ranking_stability": {
    "spearman_correlation_s2_s3": 0.68,
    "spearman_correlation_s3_s4": 0.55
  }
}
```

### CSV Exports

**stage_4_expanded.csv**

```
rank,candidate_id,name,gemini_score,reasoning,resume
1,3,"Jane Smith",95,"Strong match...", "Jane Smith\n..."
2,7,"Bob Johnson",92,"Good fit...",...
```

### Comparison Reports

**Stage Comparison:** `outputs/compare_stages.json`

```json
{
  "comparison": {
    "stage_2_to_3": {
      "rank_correlation": 0.68,
      "top_5_retention": 0.8
    },
    "stage_4_to_5": {
      "score_adjustment_mean": -3.2,
      "candidates_flagged": 2
    }
  }
}
```

---

## Performance & Metrics

### Execution Timeline

| Stage     | Input          | Output     | Time            | Cost       |
| --------- | -------------- | ---------- | --------------- | ---------- |
| Stage 1   | 10,174 resumes | 100        | 2–3 seconds     | $0         |
| Stage 2   | 100 resumes    | 50         | <1 second       | $0         |
| Stage 3   | 50 resumes     | 50         | 10–15 seconds   | $0         |
| Stage 4   | 50 resumes     | 50 (top 5) | 4–6 minutes     | $0.15      |
| Stage 5   | 50 resumes     | 50 (top 5) | 5–7 minutes     | $0.15      |
| **Total** | **10,174**     | **5**      | **~13 minutes** | **~$0.30** |

### Memory Usage

| Stage                     | Typical Memory |
| ------------------------- | -------------- |
| Dataset loaded            | ~500 MB        |
| Vectors (TF-IDF)          | ~20 MB         |
| Embeddings (384-dim × 50) | ~10 MB         |
| Gemini responses cached   | ~2 MB          |
| **Peak Total**            | **~600 MB**    |

### Quality Metrics (Typical)

| Metric                           | E-commerce | Software Engineer |
| -------------------------------- | ---------- | ----------------- |
| Hallucination Rate               | 8–12%      | 10–15%            |
| Completeness (valid resumes)     | 98%        | 96%               |
| Stage 4 vs Ground Truth Accuracy | 72%        | 75%               |
| Stage 5 vs Ground Truth Accuracy | 85%        | 87%               |
| Ranking Correlation (S2→S3)      | 0.68       | 0.65              |
| Ranking Correlation (S4→S5)      | 0.72       | 0.70              |

---

## Error Handling

### Transient Errors (Retryable)

**503 SERVICE_UNAVAILABLE, 429 QUOTA_EXCEEDED:**

```python
for attempt in range(MAX_RETRIES):
    try:
        response = gemini_api.generate(prompt)
        return response
    except (ServiceUnavailable, QuotaExceeded):
        if attempt < MAX_RETRIES - 1:
            wait_time = BACKOFF_BASE * (attempt + 1)
            time.sleep(wait_time)
            continue
        raise
```

**Result:** Automatic retry with exponential backoff (5s, 10s, 15s, 20s)

### Data Validation Errors

**Empty DataFrame:**

- Check before each stage; raise clear error
- Message: "Must run Stage X first"

**Missing Job Description:**

- Auto-load from configured path
- Fallback to generic if not found

**Invalid Role Name:**

- Fuzzy matching with levenshtein distance
- Suggest closest matches
- Filter to top 100 candidates from close matches

### Parsing Errors

**Gemini Response:**

- Expected format: "Score: X, Skills: [...], Reasoning: ..."
- Fallback: Extract score with regex
- Errors logged; resume skipped or scored 0

---

## Testing & Validation

### Test Harness

**Location:** `src/test_harness.py`

**Capabilities:**

- Run full pipeline on small dataset (e.g., 1,000 resumes)
- Smoke test all stages
- Validate outputs exist and have correct format
- Measure execution time per stage

**Usage:**

```bash
python -m src.test_harness --role "Software Engineer" --sample 1000
```

### Validation Checks

1. **File Integrity**
   - All JSON outputs valid
   - All CSVs parseable
   - No empty outputs unless expected

2. **Schema Validation**
   - Each stage output has required fields
   - Scores within valid range (0–100)
   - Ranks contiguous (1, 2, 3, ...)

3. **Logical Consistency**
   - Stage N output count ≤ Stage N-1
   - Top candidates from N-1 appear in top of N
   - Ground truth preserved if available

4. **Ground Truth Comparison**
   - Compare final ranking to actual hiring decisions
   - Compute accuracy, precision, recall, F1
   - Flag systematic biases

---

## Technical Goals

### Primary Goals

1. **Filter and Rank Resumes Efficiently**
   - Input: 10,000+ resumes
   - Output: Top 5 qualified candidates
   - Method: Multi-stage funnel with increasing sophistication
   - Target: <15 minutes end-to-end execution

2. **Improve Ranking Quality Through Multiple Algorithms**
   - Use keyword matching (TF-IDF) as fast baseline
   - Add semantic understanding (embeddings)
   - Apply LLM reasoning (Gemini scoring)
   - Validate with grounding checks (Stage 5)
   - Target: >85% agreement with ground truth hiring decisions

3. **Detect and Mitigate AI Hallucinations**
   - Parse LLM-generated skills
   - Verify against resume content
   - Use alias-aware matching (GA4 ↔ Google Analytics 4)
   - Penalize high hallucination rates
   - Target: <10% hallucination rate in final output

4. **Validate Data Quality**
   - Detect incomplete resumes (placeholders, missing fields)
   - Flag suspicious entries (AI-generated, duplicates)
   - Prevent invalid data from affecting ranking
   - Target: 98%+ valid resumes reach final stage

5. **Provide Explainable Trustworthiness Scores**
   - Show reasoning for each ranking decision
   - Quantify confidence level (tier assignment)
   - Break down scores by skill coverage
   - Enable human reviewers to verify machine decisions

### Secondary Goals

1. **Support Multiple Job Roles**
   - Accept any role via fuzzy matching
   - Automatically load role-specific job descriptions
   - Compare performance across roles
   - Identify which roles benefit most from AI ranking

2. **Enable Comparative Analysis**
   - Compare ranking stability across stages
   - Measure rank correlation between algorithms
   - Identify candidates ranked differently by methods
   - Audit algorithm agreement/disagreement

3. **Provide Audit Trail**
   - Store intermediate results per stage
   - Generate comprehensive reports
   - Document critical errors and overscores
   - Enable post-hoc review of decisions

4. **Optimize Cost and Performance**
   - Minimize API calls (rate limiting, caching)
   - Use efficient local algorithms first (TF-IDF, embeddings)
   - Defer expensive operations (Gemini) to final stages
   - Target: <$1 cost per full pipeline run

5. **Measure Trustworthiness Systematically**
   - Pre-register expected failure modes
   - Compare AI scores to ground truth
   - Calculate accuracy by skill category
   - Create calibration curves

---

## Integration Points

### Input Integration

- **Data Source:** Pandas DataFrame from CSV
- **Job Description:** Text files in `data/` directory
- **Configuration:** Environment variables + `config.py`
- **API Keys:** Gemini API key from environment

### Output Integration

- **JSON APIs:** Stage results as JSON for downstream tools
- **CSV Export:** CSV files for Excel/SQL import
- **Metrics:** JSON metrics for dashboard visualization
- **Reports:** Markdown audit reports for stakeholder review

### External APIs

- **Gemini API:** Google Cloud Generative AI endpoint
- **Sentence-Transformers:** Hugging Face model hub (local)
- **scikit-learn:** Local TF-IDF vectorization

---

## Operational Workflows

### Workflow 1: Quick Smoke Test

**Goal:** Verify system works before full run

```bash
python -m src.main
# Select role: "Software Engineer"
# Sample: 100
# Stages: 1,2,3
```

**Time:** ~5 seconds  
**Output:** stage_1.json, stage_2.json, stage_3.json

### Workflow 2: Full Production Run

**Goal:** Complete ranking for hiring decision

```bash
python -m src.main
# Select role: "E-commerce Specialist"
# Sample: 1000
# Stages: 1,2,3,4,5
```

**Time:** ~13 minutes  
**Output:** All stages + metrics + reports

### Workflow 3: Audit & Comparison

**Goal:** Analyze ranking differences between algorithms

```bash
python src/evaluation/compare_stages.py
```

**Output:** compare_stages.json + analysis charts

### Workflow 4: Metrics & Reporting

**Goal:** Generate trustworthiness report

```bash
python src/metrics/trust_metrics.py --stage 5
python src/metrics/failure_analysis.py
```

**Output:** metrics.json + failure_analysis.json + markdown report

---

_This document covers all processes, workflows, and technical goals of the Resume Trust Lab system. For specific implementation details, see corresponding source files. For audit findings from Stage 4, see STAGE*4_AUDIT*_ reports.\*
