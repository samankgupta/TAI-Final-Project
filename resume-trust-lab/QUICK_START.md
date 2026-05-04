# Quick Start Guide

## 🚀 Setup (5 minutes)

### 1. Install Dependencies
```bash
cd resume-trust-lab
pip install -r requirements.txt
```

### 2. Configure Gemini API (optional)
```bash
# Edit .env file and add your API key
GEMINI_API_KEY=your_key_from_https://makersuite.google.com/app/apikey
```

### 3. Run System

**Option A: Interactive (easiest)**
```bash
cd src
python main.py
```

**Option B: Full pipeline in one command**
```bash
cd src
python cli.py run-all --role "E-commerce Specialist" --sample-size 1000
```

## 📊 What Happens

1. **Stage 1**: Filters 10,000+ resumes to ~1,200 matching your role
2. **Stage 2**: Ranks using TF-IDF, keeps top 50
3. **Stage 3**: Ranks using embeddings, keeps top 25
4. **Stage 4**: Ranks using Gemini LLM, keeps top 5
5. **Stage 5**: Improved Gemini with hallucination detection
6. **Metrics**: Computes trust scores and comparisons

## 📁 Results

All results saved to `outputs/`:
- `stage_1.json` - Filtered resumes
- `stage_2.json` - TF-IDF rankings
- `stage_3.json` - Embedding rankings
- `stage_4.json` - Gemini rankings  
- `stage_5.json` - Improved Gemini (with hallucination detection)
- `metrics.json` - Trust metrics
- `failure_analysis.json` - Failure cases

## 🎯 Available Roles

Run this to see available roles:
```bash
cd src
python cli.py list-roles
```

Common roles:
- E-commerce Specialist
- Software Engineer
- Data Analyst
- Project Manager
- Marketing Manager
- HR Manager
- Finance Manager
- Customer Success Manager

## ⚡ CLI Commands

```bash
# Run individual stages
python cli.py run-stage --stage 1 --role "E-commerce Specialist"
python cli.py run-stage --stage 2
python cli.py run-stage --stage 3
python cli.py run-stage --stage 4
python cli.py run-stage --stage 5

# Compare stages
python cli.py compare --stage1 2 --stage2 3

# View status
python cli.py status
```

## 📊 Key Concepts

- **Stage 1**: Role filtering (removes non-matching resumes)
- **Stage 2**: Keyword matching (TF-IDF similarity)
- **Stage 3**: Semantic ranking (embeddings, better than keywords)
- **Stage 4**: LLM ranking (Gemini scores 1-10)
- **Stage 5**: Improved LLM (detects when LLM hallucinates)
- **Metrics**: Measures stability and accuracy of rankings

## 🔍 Hallucination Detection Example

Stage 5 can detect when LLM mentions skills not in the resume:

```
Resume has: Python, SQL, Excel
Gemini claims: Python, SQL, Kubernetes, Docker
Result: 2/4 skills are hallucinations (50% hallucination rate)
Score adjusted: 8 → 7 (penalized for making things up)
```

## 💡 Tips

- First run takes longer (downloads embedding model ~80MB)
- Use `--sample-size 1000` for quick testing
- Gemini API calls are cached, so re-running is fast
- Without API key, Stages 4-5 use mock scoring
- Check `outputs/` for detailed JSON results

## 🆘 Troubleshooting

**Import error?** Make sure you're in the `src/` directory when running.

**No outputs?** Check `outputs/` directory is writable.

**Dataset not found?** Path is hardcoded to `/Users/samankgupta/Downloads/TAI Final Project/dataset.csv`

**API errors?** Without GEMINI_API_KEY in .env, system uses mock scoring (fine for testing).

---

**Next steps**: Run `python main.py` and follow the prompts!
