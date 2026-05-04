# Resume Trust Lab System

**A multi-stage AI resume screening and trust evaluation system** that demonstrates how different ranking methods perform, measure their reliability, and detect LLM hallucinations in AI-driven hiring.

## 🎯 What This Does

This is a **research-grade system** that:

1. **Filters** resumes by job role
2. **Ranks** resumes using 4 different methods:
   - Baseline: TF-IDF keyword similarity
   - Embeddings: Semantic similarity  
   - Gemini Base: LLM ranking
   - Gemini Improved: LLM with hallucination detection
3. **Compares** methods using trust metrics
4. **Tracks** failures, hallucinations, and ranking disagreements
5. **Measures** system improvement incrementally

## 🚀 Quick Start

### Installation

```bash
cd resume-trust-lab
pip install -r requirements.txt
```

### Run

**Interactive Mode (easiest):**
```bash
cd src
python main.py
```

**Command Line:**
```bash
python cli.py run-all --role "E-commerce Specialist" --sample-size 1000
```

**Individual Stages:**
```bash
python cli.py run-stage --stage 1 --role "E-commerce Specialist"
python cli.py run-stage --stage 2 --top-k 50
python cli.py run-stage --stage 3 --top-k 25
python cli.py compare --stage1 2 --stage2 3
python cli.py status
```

## 📊 Pipeline Stages

### Stage 1: Role Filtering
Filters dataset by job role  
Input: 10,000+ resumes → Output: ~1,200 matching role

### Stage 2: Baseline Ranking (TF-IDF)
Keyword-based TF-IDF similarity  
Input: 1,200 resumes → Output: Top 50

### Stage 3: Embedding Ranking
Semantic similarity (all-MiniLM-L6-v2)  
Input: 50 resumes → Output: Top 25  
TSS vs Stage 2: typically 0.80+

### Stage 4: Gemini Ranking (Basic)
LLM-based scoring (1-10)  
Input: 25 resumes → Output: Top 5

### Stage 5: Improved Gemini (With Grounding)
LLM with hallucination detection  
- Enforces skills must be in resume
- Detects hallucinated claims
- Penalizes scores for hallucinations
- Input: 5 resumes → Output: Top 5

## 📈 Trust Metrics

System measures:

- **Top-K Stability (TSS)**: Overlap of top-5 between stages
- **Hallucination Rate**: % of LLM claims not in resume
- **Coverage Loss**: Good resumes removed early
- **Accuracy vs Ground Truth**: Precision/recall against dataset decisions

## 📁 Project Structure

```
resume-trust-lab/
├── data/
├── outputs/          # Stage results (JSON)
├── src/
│   ├── config.py     # Configuration
│   ├── loader.py     # Data loading
│   ├── main.py       # Interactive entry point
│   ├── cli.py        # Command line interface
│   │
│   ├── filter_roles.py           # Stage 1
│   ├── ranking/
│   │   ├── baseline_ranker.py   # Stage 2: TF-IDF
│   │   ├── embedding_ranker.py  # Stage 3: Embeddings
│   │   ├── gemini_ranker.py     # Stage 4: Gemini base
│   │   └── improved_gemini_ranker.py  # Stage 5: Gemini+grounding
│   ├── metrics/
│   │   ├── trust_metrics.py     # Metric computation
│   │   └── failure_analysis.py  # Failure detection
│   └── evaluation/
│       ├── experiment_runner.py # Pipeline orchestration
│       └── compare_stages.py    # Cross-stage comparison
│
├── requirements.txt
├── .env              # API key configuration
└── README.md
```

## 📊 Output Files

Each stage produces `outputs/stage_N.json` with:

```json
{
  "stage": 2,
  "stage_name": "Baseline Ranking (TF-IDF)",
  "input_count": 1234,
  "output_count": 50,
  "retention_rate": 0.041,
  "ranked_resumes": [
    {
      "rank": 1,
      "id": 0,
      "baseline_score": 0.95,
      "ground_truth_decision": "select"
    }
  ]
}
```

## 🔍 Example Insights

### Hallucination Detection (Stage 5)

```
Resume mentions: Python, SQL, Excel
Gemini claims: Python, SQL, Kubernetes, Docker
Hallucinations: 2/4 (50%)
Score: 8 → 7 (penalized for hallucinations)
```

### Ranking Comparison

```
Top-5 Stage 2 (TF-IDF): [1, 2, 3, 4, 5]
Top-5 Stage 3 (Embeddings): [1, 2, 6, 7, 8]
Overlap: 2/5 = 40%
Mismatch indicates keyword-semantic disagreement
```

## 🔧 Configuration

Edit `src/config.py`:

```python
TOP_K_STAGE_2 = 50    # Keep top N from baseline
TOP_K_STAGE_3 = 25    # Keep top N from embeddings
TOP_K_STAGE_4 = 5     # Keep top N from Gemini
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
USE_API_CACHE = True  # Cache Gemini responses
```

## 🔑 Using Gemini API

1. Get API key from https://makersuite.google.com/app/apikey
2. Edit `.env`:
   ```
   GEMINI_API_KEY=your_key_here
   ```
3. Stages 4-5 will use real Gemini. Without key, they use mock scoring.

## 📈 Typical Results

For E-commerce Specialist role:

```
Stage 1: 10,000 → 1,234 resumes (12.3% selected)
Stage 2: 1,234 → 50 resumes (TF-IDF: 0.35 avg score)
Stage 3: 50 → 25 resumes (Embedding: 0.62 avg score, TSS: 0.80)
Stage 4: 25 → 5 resumes (Gemini: 7.2/10 avg score)
Stage 5: 5 → 5 resumes (Improved: 6.1/10 after hallucination penalty)

Metrics:
- TSS (2→3): 0.80 (good agreement)
- TSS (4→5): 0.90 (very high agreement)
- Hallucination rate: 0.15 (15%)
```

## 📚 Dataset Format

Uses `/Users/samankgupta/Downloads/TAI Final Project/dataset.csv` with columns:
- `Role`: Job position
- `Resume`: Full resume text
- `Decision`: 'select' or 'reject' (ground truth)
- `Reason_for_decision`: Why selected/rejected
- `Job_Description`: Position requirements

## ⚙️ Troubleshooting

**"GEMINI_API_KEY not set"** - Not an error. System uses mock scoring. Add key to `.env` for real API.

**"Model download in progress"** - First run downloads embedding model (~80MB), cached afterwards.

**"Memory error with large dataset"** - Use `--sample-size` to limit resumes.

**"API rate limit"** - System adds delays between requests. Uses cached responses.

## 🎓 Research Use

This system demonstrates:
- ✅ Different ranking methods pros/cons
- ✅ How to measure AI system trustworthiness
- ✅ LLM hallucination detection in production systems
- ✅ Accuracy-trust tradeoffs in hiring AI
- ✅ Multi-stage filtering with ground truth validation

## 📝 Citation

```
Resume Trust Lab System
Multi-stage AI Resume Screening & Trust Evaluation
TAI Final Project - Trustworthy AI
```

---

**Start exploring:** `python src/main.py`
