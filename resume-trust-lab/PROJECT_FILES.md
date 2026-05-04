# Resume Trust Lab - Complete File Manifest

## Core Configuration
- **config.py** - Configuration, paths, model settings, API keys
- **.env** - Environment variables (API key template)
- **requirements.txt** - Python dependencies

## Data & Loading
- **loader.py** - DataLoader class for loading/filtering resumes from dataset.csv

## Stage Implementations

### Stage 1: Role Filtering
- **filter_roles.py** - RoleFilter class for role-based filtering

### Stage 2-5: Ranking Methods
- **ranking/baseline_ranker.py** - TF-IDF keyword-based ranking
- **ranking/embedding_ranker.py** - Sentence-Transformers semantic ranking  
- **ranking/gemini_ranker.py** - Google Gemini LLM-based ranking
- **ranking/improved_gemini_ranker.py** - Gemini with grounding & hallucination detection

## Metrics & Analysis
- **metrics/trust_metrics.py** - TrustMetrics class for computing:
  - Top-K Stability Score
  - Ranking Drift
  - Hallucination Rate
  - Coverage Loss
- **metrics/failure_analysis.py** - FailureAnalysis class for identifying:
  - False Positives
  - False Negatives
  - Mismatches
  - Hallucinations

## Pipeline Orchestration
- **evaluation/experiment_runner.py** - ExperimentRunner orchestrating all stages
- **evaluation/compare_stages.py** - StageComparator for cross-stage analysis

## Interfaces
- **main.py** - Interactive terminal interface
- **cli.py** - Command-line interface (Click-based)

## Package Markers
- **src/__init__.py** - Python package marker
- **ranking/__init__.py** - Ranking subpackage marker
- **metrics/__init__.py** - Metrics subpackage marker
- **evaluation/__init__.py** - Evaluation subpackage marker

## Directories
- **data/** - Job descriptions (empty, for future use)
- **outputs/** - Results from running stages (stage_1.json through stage_5.json)

## Documentation
- **README.md** - Comprehensive project documentation
- **QUICK_START.md** - 5-minute setup guide
- **SETUP_VERIFICATION.md** - Verification checklist
- **PROJECT_FILES.md** - This file

## Build Summary
- **../BUILD_SUMMARY.txt** - Overview of what was built

---

## File Purposes Summary

| File | Purpose | Key Classes/Functions |
|------|---------|----------------------|
| config.py | Paths, settings, constants | DATASET_PATH, TOP_K_*, OUTPUT_DIR |
| loader.py | Dataset loading | DataLoader.load_dataset(), filter_by_role() |
| filter_roles.py | Stage 1 | RoleFilter.run() |
| baseline_ranker.py | Stage 2 | BaselineRanker.run() |
| embedding_ranker.py | Stage 3 | EmbeddingRanker.run() |
| gemini_ranker.py | Stage 4 | GeminiRanker.run() |
| improved_gemini_ranker.py | Stage 5 | ImprovedGeminiRanker.run() |
| trust_metrics.py | Metrics | TrustMetrics.top_k_stability_score() |
| failure_analysis.py | Failures | FailureAnalysis.generate_failure_report() |
| experiment_runner.py | Orchestration | ExperimentRunner.run_all(), run_stage_N() |
| compare_stages.py | Comparison | StageComparator.compare_rankings() |
| main.py | Interactive UI | main() |
| cli.py | CLI | run_stage(), run_all(), compare(), status() |

---

## Pipeline Data Flow

```
dataset.csv (614K resumes)
    ↓
[Stage 1: Role Filtering] → stage_1.json
    ↓ (1,200 resumes)
[Stage 2: TF-IDF] → stage_2.json (50)
    ↓
[Stage 3: Embeddings] → stage_3.json (25)
    ↓
[Stage 4: Gemini] → stage_4.json (5)
    ↓
[Stage 5: Gemini+Grounding] → stage_5.json (5)
    ↓
[Metrics] → metrics.json
[Failure Analysis] → failure_analysis.json
```

---

## Total Lines of Code

- Core modules: ~1,500 lines
- Ranking stages: ~800 lines
- Metrics/Analysis: ~400 lines
- CLI/Main: ~300 lines
- Total: ~3,000 lines of production code

---

## Dependencies (from requirements.txt)

- pandas (data handling)
- numpy (numerical computing)
- scikit-learn (TF-IDF, similarity)
- sentence-transformers (embeddings)
- google-generativeai (Gemini API)
- click (CLI framework)
- python-dotenv (environment variables)

---

**Generated**: May 3, 2026
**Location**: /Users/samankgupta/Downloads/TAI Final Project/resume-trust-lab/
