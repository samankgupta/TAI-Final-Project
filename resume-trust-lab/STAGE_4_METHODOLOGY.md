# Stage 4 Methodology — Pipeline Architecture & Scoring Process

**Document Purpose:** Explain the full resume screening pipeline, Stage 4's role within it, and how Gemini scoring operates  
**Audience:** Technical stakeholders, auditors, resume program managers

---

## Table of Contents

1. [Pipeline Overview](#pipeline-overview)
2. [The Full Funnel (Stages 1–5)](#the-full-funnel-stages-1--5)
3. [Stage 4: Gemini Ranking Base](#stage-4-gemini-ranking-base)
4. [Scoring Logic & Prompting](#scoring-logic--prompting)
5. [Rate Limiting & Performance](#rate-limiting--performance)
6. [Caching & Optimization](#caching--optimization)
7. [Configuration & Inputs](#configuration--inputs)

---

## Pipeline Overview

The resume screening system is a **5-stage funnel** that progressively ranks and filters candidates:

```
Raw Dataset (10,174 resumes, 45 roles)
          ↓
[Stage 1] Role Filtering
          → 100 candidates per role
          ↓
[Stage 2] TF-IDF Keyword Matching
          → 50 candidates (ranked by job description relevance)
          ↓
[Stage 3] Semantic Embedding Ranking
          → 50 candidates (ranked by semantic similarity to JD)
          ↓
[Stage 4] Gemini API Ranking (AUDIT FOCUS)
          → Top 50 scored 1–100; top 10 selected for final review
          ↓
[Stage 5] Improved Grounding (Trust Validation)
          → Top 50 re-scored with hallucination detection & completeness checks
          ↓
Final Ranking (Top 10 candidates for hiring decision)
```

Each stage acts as a filter, reducing candidate pool while increasing scoring sophistication.

---

## The Full Funnel (Stages 1–5)

### Stage 1: Role Filtering

**Purpose:** Extract candidates matching the target job role  
**Input:** `dataset.csv` (10,174 resumes with role labels)  
**Output:** Up to 100 resumes for the specified role  
**Logic:**

- Load dataset and filter by normalized role name (e.g., "Software Engineer")
- Extract ground truth (hiring decision) from `Decision` column if available
- Return resumes sorted by their original dataset order

**E-commerce Specialist results:** ~200 matching resumes (limited to 100)  
**Software Engineer results:** 787 matching resumes (limited to 100)

### Stage 2: TF-IDF Keyword Matching

**Purpose:** Rank candidates by keyword overlap with job description  
**Input:** 100 resumes from Stage 1 + job description text  
**Output:** Top 50 resumes (TF-IDF scored and ranked)  
**Logic:**

- Extract job description keywords (Shopify, PPC, Email Marketing, etc.)
- Compute TF-IDF vectors for each resume
- Rank by cosine similarity to job description vector
- Return top 50

**Technology:** scikit-learn (TfidfVectorizer)  
**Typical runtime:** <1 second for 100 resumes

### Stage 3: Semantic Embedding Ranking

**Purpose:** Rank candidates by semantic similarity to job description  
**Input:** Top 50 resumes from Stage 2 + job description  
**Output:** Top 50 resumes (semantic scored and ranked)  
**Logic:**

- Convert each resume and job description to embeddings using `all-MiniLM-L6-v2` model
- Compute cosine similarity between each resume and job description embeddings
- Rank by similarity score (0.0 to 1.0)
- Return top 50

**Technology:** sentence-transformers (Hugging Face)  
**Typical runtime:** 10–15 seconds for 50 resumes (model loading + embedding generation)

### Stage 4: Gemini Ranking Base (THIS AUDIT)

**Purpose:** Use LLM (Gemini) to score each resume against job description  
**Input:** Top 50 resumes from Stage 3 + job description  
**Output:** 50 resumes with Gemini scores (1–100) and reasoning  
**Logic:** _(see detailed section below)_

**Technology:** Google Gemini API (`gemini-3.1-flash-lite`)  
**Typical runtime:** 4–6 minutes for 50 resumes at 13 requests/minute rate limit

### Stage 5: Improved Grounding (Trust Validation)

**Purpose:** Re-score top resumes using grounding checks and hallucination detection  
**Input:** Top 50 from Stage 4 (Gemini scores + reasoning)  
**Output:** 50 resumes with adjusted scores (1–10 scale, then converted to 1–100) reflecting trustworthiness  
**Logic:**

- Check for incomplete/placeholder resumes (caps score at 1.0)
- Detect skills claimed in reasoning but missing from resume (hallucination detection)
- Use alias-aware matching (GA4 ↔ Google Analytics 4, PPC ↔ Paid Search) to validate claimed skills
- Re-score with penalty for hallucination rate
- Apply score caps based on hallucination severity

**Technology:** Gemini API + regex + custom grounding logic  
**Typical runtime:** 5–7 minutes for 50 resumes

---

## Stage 4: Gemini Ranking Base

### Scoring Process

#### Input Data

```json
{
  "resume": "Full resume text...",
  "job_description": "Full job description...",
  "candidate_id": 5,
  "role": "E-commerce Specialist"
}
```

#### Gemini Prompt (Simplified)

```
You are an expert recruiter. Score this resume for fit with the job description on a scale of 1-10
(where 1 = not qualified, 10 = excellent fit).

Job Description:
[Full JD text]

Resume:
[Full resume text]

Provide:
1. Score (1-10)
2. List of key skills found in the resume
3. One-line reasoning for the score
```

#### Scoring Output

```json
{
  "candidate_id": 5,
  "name": "Candidate Name",
  "gemini_score": 95,
  "reasoning": "Strong e-commerce background with Shopify, Google Analytics, and PPC experience.",
  "skills_found": ["Shopify", "Google Analytics", "PPC", "Email Marketing"],
  "rank": 1,
  "resume": "Full resume text..."
}
```

#### Score Scaling

- Gemini returns scores on 1–10 scale
- Scaled to 1–100 by multiplying by 10
- Example: Gemini score of 9.5 → output as 95

### Current Issues with Stage 4 Scoring

1. **No distinction between required and optional skills**
   - Resume missing Shopify (explicitly required) is scored similar to resume with it
   - Keyword presence is rewarded; keyword absence is not proportionally penalized

2. **No penalty for AI-generated boilerplate**
   - 25 resumes contain obvious template text ("Remember to tailor your resume…")
   - These appear at all score levels (35–95) with no consistent deduction

3. **No completeness checks**
   - Resumes with unfilled fields (`[Insert Email]`) are scored as if valid
   - Resumes with embedded rejection letters or meta-commentary are not rejected

4. **Score clustering / insufficient granularity**
   - E-commerce: 18 candidates at 95; Software Engineer: 24 at 85
   - Makes differentiation impossible within large tied bands

---

## Scoring Logic & Prompting

### Prompt Template

The actual prompt sent to Gemini includes:

1. **Context:** Explicit instruction to act as expert recruiter
2. **Job description:** Full text of the target job
3. **Resume:** Full text of the candidate's resume
4. **Request:** Score 1–10 + skills list + reasoning

### Key Assumptions in Current Prompt

- Gemini has consistent interpretation of "job fit"
- Gemini weights all skills equally
- Gemini penalizes missing required skills adequately
- Resume text directly maps to skills (no hallucination)

### Known Limitations

- **Gemini may hallucinate skills** not actually present in resume (addressed in Stage 5)
- **Prompt does not specify point values** for each skill area (contributes to clustering)
- **No grounding against resume text** in Stage 4 (deferred to Stage 5)
- **Single prompt per resume** — no opportunity for refinement or structured breakdown

---

## Rate Limiting & Performance

### Rate Limit: 13 Requests Per Minute

Gemini API quota enforces a maximum of 13 requests per minute per project. The Stage 4 engine implements sliding-window enforcement:

```python
def _enforce_rate_limit(self):
    """Ensure no more than 13 requests in the past 60 seconds."""
    if len(self.request_times) == 13:
        oldest = self.request_times[0]
        wait_time = 60 - (time.time() - oldest)
        if wait_time > 0:
            time.sleep(wait_time)
        self.request_times.popleft()
    self.request_times.append(time.time())
```

### Throughput Calculation

- **Rate limit:** 13 requests/minute = 1 request every ~4.6 seconds
- **Typical Gemini response time:** 2–3 seconds
- **Effective throughput:** ~12 resumes per minute (with overhead)
- **Expected runtime for 50 resumes:** 4–6 minutes

### Retry Logic for Transient Errors

If Gemini returns 503 (SERVICE_UNAVAILABLE) or 429 (QUOTA_EXCEEDED):

```python
max_retries = 4
backoff_base = 5  # seconds
for attempt in range(max_retries):
    try:
        score = call_gemini_api(resume, jd)
        return score
    except (ServiceUnavailable, QuotaExceeded) as e:
        if attempt < max_retries - 1:
            wait = backoff_base * (attempt + 1)
            sleep(wait)
            continue
        raise
```

- **Attempt 1 failure:** wait 5 seconds, retry
- **Attempt 2 failure:** wait 10 seconds, retry
- **Attempt 3 failure:** wait 15 seconds, retry
- **Attempt 4 failure:** wait 20 seconds, retry
- **Attempt 5 failure:** raise exception and log error

This approach recovers most transient errors without manual intervention.

---

## Caching & Optimization

### Cache Key Strategy

Each resume-job pair is cached using MD5 hash of: `job_description_text | resume_text`

```python
cache_key = hashlib.md5(f"{job_desc}|{resume}".encode()).hexdigest()
cache_path = f".cache/{cache_key}.json"
```

**Benefits:**

- Avoids redundant API calls if same candidate re-scored for same job
- Dramatically speeds up re-runs and debugging

**Location:** `.cache/` directory relative to project root  
**Format:** JSON (one file per resume-job pair)  
**Typical size:** 100 files after full run (each ~1 KB)

### Cache Invalidation

Cache is **not used** if:

- Resume or job description text is modified
- API credentials change
- `USE_API_CACHE=false` in config

After JSON outputs are generated, cache files are typically deleted to save disk space.

---

## Configuration & Inputs

### Required Configuration

Located in `src/config.py`:

```python
# Input data
DATASET_PATH = "dataset.csv"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Stage sizing
TOP_K_STAGE_1 = 100
TOP_K_STAGE_2 = 50
TOP_K_STAGE_3 = 50
TOP_K_STAGE_4 = 50
TOP_K_SELECT_FROM_STAGE_4 = 10

# Options
USE_API_CACHE = True
```

### Input Files

| File                                         | Purpose                               | Used by    |
| -------------------------------------------- | ------------------------------------- | ---------- |
| `dataset.csv`                                | Raw resumes + role labels + decisions | Stage 1    |
| `data/job_description_ecommerce.txt`         | E-commerce Specialist JD              | Stages 2–5 |
| `data/job_description_software_engineer.txt` | Software Engineer JD                  | Stages 2–5 |

### Environment Variables

```bash
export GEMINI_API_KEY="your-api-key-here"
```

If not set, Stage 4/5 will fail with authentication error.

### Example Run Command

```bash
cd resume-trust-lab
python -m src.evaluation.experiment_runner \
  --role "Software Engineer" \
  --stages 4 5
```

Output will be written to `outputs/stage_4.json` and `outputs/stage_5.json`.

---

## Output Structure

### Stage 4 JSON Output

```json
{
  "stage": 4,
  "role": "E-commerce Specialist",
  "total_candidates": 50,
  "timestamp": "2026-05-13T14:23:45.123456",
  "candidates": [
    {
      "rank": 1,
      "candidate_id": 29,
      "name": "John Crawford",
      "gemini_score": 95,
      "reasoning": "Strong e-commerce background with 5+ years experience in marketplaces and SEO.",
      "skills_found": ["SEO", "Product Listing", "Keyword Research", "Google Analytics"],
      "resume": "Full resume text...",
      "resume_preview": "John Crawford\n..."
    },
    ...
  ]
}
```

### Stage 4 CSV Output (Optional)

If `match_stage4_to_stage1.py` is run post-scoring:

```
rank,candidate_id,gemini_score,reasoning,role,resume
1,29,95,"Strong e-commerce background...",E-commerce Specialist,"John Crawford\n..."
...
```

---

## Validation & Quality Checks

### Pre-Stage-4 Validation (Currently NOT Implemented)

**Recommended:** Before sending resumes to Stage 4, screen for:

- [ ] Unfilled contact fields (`[Insert Email]`, `[Insert Phone]`)
- [ ] Date placeholders (`20XX`)
- [ ] Malformed email addresses (backslash escapes, special chars)
- [ ] Embedded non-resume content (AI rejection letters, AI narration)
- [ ] Duplicate email addresses (deduplication)

### Post-Stage-4 Validation (Implemented in Stage 5)

Stage 5 checks:

- Placeholder text patterns (`[Insert ...]`, `lorem ipsum`, "sample resume")
- Skill hallucinations (skills in Stage 4 reasoning not found in resume)
- Alias matching (GA4 ↔ Google Analytics 4) to validate claimed skills

---

## Known Limitations & Future Work

### Current Limitations

1. **No structured scoring rubric** — all skills weighted equally
2. **Required vs. optional skills not distinguished** in prompt
3. **No explicit penalties** for missing critical skills
4. **Floating-point precision** in score calculations (95.000 vs 95.001 treated as tied)
5. **Resume format sensitivity** — plain text resumes score differently than formatted PDFs

### Recommended Improvements

**Immediate (before next run):**

- Add pre-Stage-4 validation for incomplete resumes
- Implement email deduplication
- Apply consistent −5 to −10 point penalty for AI boilerplate

**Short-term (design improvements):**

- Break scoring into skill-by-skill evaluation (0–10 per skill)
- Weight required skills 2× optional skills
- Generate finer-grained score distribution

**Long-term (architecture changes):**

- Multi-turn prompting for score justification
- Structured output (JSON) directly from Gemini (no text parsing)
- Feedback loop: compare Stage 4 scores to ground truth hiring decisions; measure calibration

---

## Glossary

| Term                  | Definition                                                                   |
| --------------------- | ---------------------------------------------------------------------------- |
| **TF-IDF**            | Term Frequency–Inverse Document Frequency; measures keyword importance       |
| **Embedding**         | Vector representation of text capturing semantic meaning                     |
| **Cosine Similarity** | Measure of similarity between two vectors (0.0 = unrelated, 1.0 = identical) |
| **Gemini API**        | Google's large language model API; used for intelligent scoring              |
| **Rate Limit**        | Maximum number of API requests allowed per unit time (13/min here)           |
| **Hallucination**     | LLM generating facts not supported by input data                             |
| **Ground Truth**      | Actual hiring decision for a candidate (accept/reject)                       |

---

_For detailed candidate-level findings, see [STAGE_4_JOB1_ECOMMERCE_AUDIT.md](STAGE_4_JOB1_ECOMMERCE_AUDIT.md) and [STAGE_4_JOB2_SOFTWARE_ENGINEER_AUDIT.md](STAGE_4_JOB2_SOFTWARE_ENGINEER_AUDIT.md)_
