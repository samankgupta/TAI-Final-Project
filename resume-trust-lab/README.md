# Resume Trust Lab

A multi-stage AI resume screening pipeline that evaluates trustworthiness and ranking quality across progressively smarter methods — from keyword matching to LLM-based scoring with hallucination detection.

## What It Does

Given a job role and a dataset of resumes, the system runs candidates through five sequential filtering and ranking stages, narrowing the pool at each step. After all stages complete, it computes trust metrics to evaluate how well each stage performed and how consistent the rankings were across stages.

## Pipeline Stages

```
All resumes in dataset
        │
  [Stage 1] Role Filter  (exact/fuzzy match on job title)
        │  → up to 100 candidates
  [Stage 2] Baseline Ranking  (TF-IDF cosine similarity vs job description)
        │  → top 50
  [Stage 3] Embedding Ranking  (sentence-transformers, all-MiniLM-L6-v2)
        │  → top 30
  [Stage 4] Gemini Ranking  (Gemini LLM, 1-100 score)
        │  → top 10
  [Stage 5] Improved Gemini  (Gemini + hallucination penalty)
             → top 10 final candidates
```

### Stage 1 — Role Filter
Loads the full dataset and keeps resumes where the candidate's job title matches the target role (exact or fuzzy). Also loads ground-truth hiring decisions (`select` / `reject`) that are used later for precision metrics.

### Stage 2 — TF-IDF Baseline
Ranks filtered resumes using TF-IDF cosine similarity against the job description. Fast and purely keyword-based — no understanding of meaning. Keeps top 50.

### Stage 3 — Embedding Ranking
Re-ranks Stage 2's top candidates using semantic embeddings (`all-MiniLM-L6-v2` via `sentence-transformers`). Captures meaning rather than just keyword overlap. Keeps top 30.

### Stage 4 — Gemini Ranking (Base)
Sends each resume to the Gemini API (`gemini-3.1-flash-lite`) with the job description and asks for a 1–100 score plus reasoning. Rate-limited to 13 requests/minute. Responses are cached to avoid redundant API calls. Keeps top 10.

### Stage 5 — Improved Gemini (With Grounding)
Same as Stage 4 but adds **hallucination detection**: after Gemini returns a list of skills it identified in the resume, each skill is checked against the actual resume text. Skills not present in the resume are flagged as hallucinations. The raw score is penalized proportionally:

```
adjusted_score = raw_score × (1 − hallucination_rate)
```

This discounts scores that relied on fabricated evidence, making the final ranking more faithful to what is actually on the resume. Keeps top 10.

## Trust Metrics

After all stages complete, two metrics are computed:

**Precision@K** — fraction of the top-K candidates selected by a stage that are ground-truth `select` decisions. Higher is better.

**Top-K Stability Score (TSS)** — Jaccard overlap between the candidate sets selected by adjacent stages. Measures agreement between consecutive ranking methods. Lower values mean the methods disagree substantially on who the best candidates are.

Most recent run (E-commerce Specialist, 1000 resumes, all stages):

| Stage | Method | Precision@K |
|---|---|---|
| Stage 2 | TF-IDF | 58.0% |
| Stage 3 | Embeddings | 50.0% |
| Stage 4 | Gemini base | 70.0% |
| Stage 5 | Gemini + grounding | 60.0% |

| Transition | TSS |
|---|---|
| Stage 2 → Stage 3 | 0.333 |
| Stage 3 → Stage 4 | 0.143 |
| Stage 4 → Stage 5 | 0.111 |

Low TSS across all transitions means each method selects a substantially different set of candidates — the choice of ranking method has a large effect on who gets hired.

## Project Structure

```
resume-trust-lab/
├── src/
│   ├── main.py                        # Interactive CLI entry point
│   ├── config.py                      # Paths, model names, API keys, top-K values
│   ├── loader.py                      # Dataset and job description loading
│   ├── filter_roles.py                # Stage 1: role filtering
│   ├── ranking/
│   │   ├── baseline_ranker.py         # Stage 2: TF-IDF
│   │   ├── embedding_ranker.py        # Stage 3: sentence-transformers
│   │   ├── gemini_ranker.py           # Stage 4: Gemini API
│   │   └── improved_gemini_ranker.py  # Stage 5: Gemini + hallucination detection
│   ├── metrics/
│   │   ├── trust_metrics.py           # Precision@K and TSS computation
│   │   └── failure_analysis.py        # Failure case analysis
│   └── evaluation/
│       └── experiment_runner.py       # Orchestrates the full pipeline
├── data/
│   ├── job_description_ecommerce.txt
│   └── job_description_software_engineer.txt
├── outputs/                           # JSON results per stage + metrics.json
├── .cache/                            # Cached Gemini API responses (MD5-keyed)
├── .env                               # API keys and dataset path (not committed)
└── requirements.txt
```

## Setup

```bash
pip install -r requirements.txt
```

Create a `.env` file:
```
GEMINI_API_KEY=your_key_here
DATASET_PATH=/path/to/dataset.csv
```

The dataset CSV should have columns: `Role`, `Resume`, `Decision` (select/reject), `Job_Description`.

A Gemini API key is required for Stages 4 and 5.

## Running

```bash
cd resume-trust-lab
python src/main.py
```

The interactive prompt asks for:
- **Role** — job title to screen for (e.g. `E-commerce Specialist`)
- **Sample size** — how many resumes to load from the dataset (default 1000)
- **Stages** — comma-separated list like `1,2,3` or `A` for all five

Outputs are written to `outputs/` as JSON files: `stage_1.json` through `stage_5.json` and `metrics.json`.

## Caching

Gemini API calls are cached in `.cache/` using an MD5 hash of the (job description + resume) pair. Re-running with the same inputs uses cached responses and skips API calls entirely.

## Key Design Decisions

**Funnel architecture** — Each stage operates on the survivors of the previous stage, reducing the pool progressively so expensive LLM calls are only made on already-promising resumes.

**Hallucination penalty** — Stage 5 grounds LLM claims against the actual resume text. Skills the model claims to have seen but that don't appear in the text are penalized, making scoring more faithful to the resume.

**Rate limiting** — Gemini stages enforce 13 req/min. There is a mandatory 65-second cooldown between Stages 4 and 5 to avoid hitting quota limits across back-to-back runs.

**Ground truth evaluation** — The dataset includes hiring decisions, enabling objective Precision@K comparison across ranking methods rather than relying on subjective judgment.
