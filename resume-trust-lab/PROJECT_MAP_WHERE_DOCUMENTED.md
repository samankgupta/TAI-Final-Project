# Documentation Map — Where Everything is Mentioned

**Purpose:** Cross-reference guide showing where each topic, process, and technical goal is documented across all project files.

---

## Quick Lookup Table

| Topic                   | Main File                     | Secondary Files                         | Line/Section                     |
| ----------------------- | ----------------------------- | --------------------------------------- | -------------------------------- |
| Pipeline Architecture   | PROJECT_PROCESSES_COMPLETE.md | STAGE_4_METHODOLOGY.md                  | High-Level Architecture          |
| Stage 1: Role Filtering | PROJECT_PROCESSES_COMPLETE.md | COMPREHENSIVE_TRUSTWORTHINESS_REPORT.md | Stage-by-Stage Process → STAGE 1 |
| Stage 2: TF-IDF Ranking | PROJECT_PROCESSES_COMPLETE.md | STAGE_4_METHODOLOGY.md                  | Stage-by-Stage Process → STAGE 2 |
| Stage 3: Embeddings     | PROJECT_PROCESSES_COMPLETE.md | STAGE_4_METHODOLOGY.md                  | Stage-by-Stage Process → STAGE 3 |
| Stage 4: Gemini Scoring | PROJECT_PROCESSES_COMPLETE.md | STAGE_4_METHODOLOGY.md                  | Stage-by-Stage Process → STAGE 4 |
| Stage 5: Grounding      | PROJECT_PROCESSES_COMPLETE.md | STAGE_4_METHODOLOGY.md                  | Stage-by-Stage Process → STAGE 5 |
| Hallucination Detection | PROJECT_PROCESSES_COMPLETE.md | STAGE_4_METHODOLOGY.md                  | Ranking Algorithms → Algorithm 4 |
| Rate Limiting           | PROJECT_PROCESSES_COMPLETE.md | STAGE_4_METHODOLOGY.md                  | Rate Limiting & Performance      |
| Configuration           | PROJECT_PROCESSES_COMPLETE.md | src/config.py                           | Configuration & Parameters       |
| Metrics & Evaluation    | PROJECT_PROCESSES_COMPLETE.md | COMPREHENSIVE_TRUSTWORTHINESS_REPORT.md | Performance & Metrics            |
| Error Handling          | PROJECT_PROCESSES_COMPLETE.md | src/ranking/gemini_ranker.py            | Error Handling                   |
| Testing                 | PROJECT_PROCESSES_COMPLETE.md | src/test_harness.py                     | Testing & Validation             |

---

## Detailed Mapping by Topic

### PIPELINE & ARCHITECTURE

| Topic                        | Document                                | Section/File               | Details                   |
| ---------------------------- | --------------------------------------- | -------------------------- | ------------------------- |
| **5-Stage Funnel Overview**  | PROJECT_PROCESSES_COMPLETE.md           | High-Level Architecture    | Diagram + description     |
|                              | STAGE_4_METHODOLOGY.md                  | Pipeline Overview          | Stages 1-5 explained      |
|                              | COMPREHENSIVE_TRUSTWORTHINESS_REPORT.md | Problem Domain             | Architecture context      |
| **Data Flow Transformation** | PROJECT_PROCESSES_COMPLETE.md           | Data Flow & Transformation | Visual + code             |
|                              | STAGE_4_METHODOLOGY.md                  | The Full Funnel            | Each stage input/output   |
| **Funnel Sizing**            | PROJECT_PROCESSES_COMPLETE.md           | Configuration & Parameters | TOP_K values              |
|                              | STAGE_4_METHODOLOGY.md                  | Stage 4 Configuration      | Specific stage parameters |
|                              | STAGE_4_AUDIT_OVERVIEW.md               | Overview                   | Filtering at each stage   |

---

### STAGE 1: ROLE FILTERING

| Topic                       | Document                                | Section/File                 | Details                |
| --------------------------- | --------------------------------------- | ---------------------------- | ---------------------- |
| **Role Filtering Process**  | PROJECT_PROCESSES_COMPLETE.md           | Stage 1: Role Filtering      | 5-step process         |
|                             | src/filter_roles.py                     | Code                         | Implementation         |
|                             | STAGE_4_METHODOLOGY.md                  | Stage 1: Role Filtering      | High-level             |
| **Role Normalization**      | PROJECT_PROCESSES_COMPLETE.md           | Stage 1 → Role Normalization | Fuzzy matching logic   |
|                             | src/loader.py                           | Code                         | Role canonicalization  |
|                             | COMPREHENSIVE_TRUSTWORTHINESS_REPORT.md | Software Engineer Path       | Role matching issues   |
| **Ground Truth Extraction** | PROJECT_PROCESSES_COMPLETE.md           | Stage 1 → Cleaning           | Ground truth field     |
|                             | src/loader.py                           | Code                         | Implementation         |
|                             | COMPREHENSIVE_TRUSTWORTHINESS_REPORT.md | Evaluation                   | Accuracy metrics vs GT |
| **Resume Cleaning**         | PROJECT_PROCESSES_COMPLETE.md           | Stage 1 → Cleaning           | Boilerplate removal    |
|                             | src/filter_roles.py                     | Code                         | Clean function         |

---

### STAGE 2: KEYWORD MATCHING (TF-IDF)

| Topic                       | Document                       | Section/File                     | Details                |
| --------------------------- | ------------------------------ | -------------------------------- | ---------------------- |
| **TF-IDF Algorithm**        | PROJECT_PROCESSES_COMPLETE.md  | Ranking Algorithms → Algorithm 1 | How it works           |
|                             | STAGE_4_METHODOLOGY.md         | Stage 2: TF-IDF                  | Technical overview     |
|                             | src/ranking/baseline_ranker.py | Code                             | Implementation         |
| **Job Description Loading** | PROJECT_PROCESSES_COMPLETE.md  | Stage 2 → Load Job Description   | File loading           |
|                             | src/loader.py                  | Code                             | load_job_description() |
|                             | STAGE_4_METHODOLOGY.md         | Configuration & Inputs           | File paths             |
| **Vectorization & Scoring** | PROJECT_PROCESSES_COMPLETE.md  | Stage 2 → Vectorization          | Process steps          |
|                             | src/ranking/baseline_ranker.py | Code                             | run() method           |
| **Performance**             | PROJECT_PROCESSES_COMPLETE.md  | Performance & Metrics            | <1 second              |
|                             | STAGE_4_METHODOLOGY.md         | Stage 2 → Performance            | Timing                 |

---

### STAGE 3: SEMANTIC EMBEDDINGS

| Topic                      | Document                        | Section/File                     | Details                |
| -------------------------- | ------------------------------- | -------------------------------- | ---------------------- |
| **Embedding Model**        | PROJECT_PROCESSES_COMPLETE.md   | Stage 3 → Model Loading          | all-MiniLM-L6-v2       |
|                            | STAGE_4_METHODOLOGY.md          | Stage 3 → Technology             | Model details          |
|                            | src/config.py                   | Line 38                          | EMBEDDING_MODEL config |
| **Embedding Generation**   | PROJECT_PROCESSES_COMPLETE.md   | Stage 3 → Embedding Generation   | 384-dim vectors        |
|                            | src/ranking/embedding_ranker.py | Code                             | Implementation         |
| **Similarity Calculation** | PROJECT_PROCESSES_COMPLETE.md   | Stage 3 → Similarity Calculation | Cosine similarity      |
|                            | src/ranking/embedding_ranker.py | Code                             | Scoring logic          |
| **Performance**            | PROJECT_PROCESSES_COMPLETE.md   | Performance & Metrics            | 10–15 seconds          |
|                            | STAGE_4_METHODOLOGY.md          | Stage 3 → Performance            | Timing breakdown       |

---

### STAGE 4: GEMINI SCORING

| Topic                  | Document                      | Section/File                     | Details                |
| ---------------------- | ----------------------------- | -------------------------------- | ---------------------- |
| **Gemini API Setup**   | PROJECT_PROCESSES_COMPLETE.md | Stage 4 → Gemini Scoring         | Configuration          |
|                        | src/config.py                 | Line 36                          | GEMINI_MODEL_NAME      |
|                        | STAGE_4_METHODOLOGY.md        | Stage 4 → Technology             | API details            |
| **Rate Limiting**      | PROJECT_PROCESSES_COMPLETE.md | Stage 4 → Rate Limiting Setup    | 13 req/min             |
|                        | src/ranking/gemini_ranker.py  | Code                             | \_enforce_rate_limit() |
|                        | STAGE_4_METHODOLOGY.md        | Rate Limiting & Performance      | Sliding window         |
| **Scoring Logic**      | PROJECT_PROCESSES_COMPLETE.md | Stage 4 → Gemini Scoring         | Full process           |
|                        | STAGE_4_METHODOLOGY.md        | Stage 4: Gemini Ranking Base     | Detailed operation     |
|                        | src/ranking/gemini_ranker.py  | Code                             | score() method         |
| **Prompt Design**      | PROJECT_PROCESSES_COMPLETE.md | Stage 4 → Gemini Scoring → 3     | Prompt template        |
|                        | STAGE_4_METHODOLOGY.md        | Scoring Logic & Prompting        | Prompt template        |
|                        | STAGE_4_RECOMMENDATIONS.md    | Strategy 1                       | Improved prompt        |
| **Retry Logic**        | PROJECT_PROCESSES_COMPLETE.md | Stage 4 → Retry Logic            | Exponential backoff    |
|                        | src/ranking/gemini_ranker.py  | Code                             | Retry implementation   |
|                        | STAGE_4_METHODOLOGY.md        | Retry Logic for Transient Errors | Details                |
| **Caching**            | PROJECT_PROCESSES_COMPLETE.md | Stage 4 → Caching                | MD5-keyed cache        |
|                        | src/config.py                 | Line 45-46                       | Cache settings         |
|                        | STAGE_4_METHODOLOGY.md        | Caching & Optimization           | Strategy details       |
| **Output Format**      | PROJECT_PROCESSES_COMPLETE.md | Output & Results → Stage 4       | JSON structure         |
|                        | STAGE_4_METHODOLOGY.md        | Output Structure → Stage 4 JSON  | Fields                 |
| **Performance & Cost** | PROJECT_PROCESSES_COMPLETE.md | Performance & Metrics            | ~12 res/min, $0.003    |
|                        | STAGE_4_METHODOLOGY.md        | Performance                      | Throughput             |

---

### STAGE 5: GROUNDING & TRUST VALIDATION

| Topic                           | Document                                | Section/File                                         | Details                    |
| ------------------------------- | --------------------------------------- | ---------------------------------------------------- | -------------------------- |
| **Incomplete Resume Detection** | PROJECT_PROCESSES_COMPLETE.md           | Stage 5 → Incomplete Resume Detection                | Regex patterns             |
|                                 | src/ranking/improved_gemini_ranker.py   | Code                                                 | \_is_incomplete_resume()   |
|                                 | STAGE_4_METHODOLOGY.md                  | Stage 5 → Placeholder detection                      | Patterns                   |
| **Hallucination Detection**     | PROJECT_PROCESSES_COMPLETE.md           | Stage 5 → Skill Hallucination Detection              | Alias matching             |
|                                 | src/ranking/improved_gemini_ranker.py   | Code                                                 | Full implementation        |
|                                 | STAGE_4_METHODOLOGY.md                  | Stage 5 → Hallucination detection                    | Alias groups               |
|                                 | COMPREHENSIVE_TRUSTWORTHINESS_REPORT.md | Stage 5 Modification                                 | Grounding checks           |
| **Alias Matching**              | PROJECT_PROCESSES_COMPLETE.md           | Trustworthiness Validation → Hallucination Detection | Alias groups               |
|                                 | src/ranking/improved_gemini_ranker.py   | Code                                                 | alias_groups dictionary    |
| **Score Adjustment**            | PROJECT_PROCESSES_COMPLETE.md           | Stage 5 → Score Adjustment                           | Penalty formula            |
|                                 | src/ranking/improved_gemini_ranker.py   | Code                                                 | adjusted_score calculation |
|                                 | STAGE_4_METHODOLOGY.md                  | Stage 5 → Score Adjustment                           | Penalty thresholds         |
| **Re-scoring with Grounding**   | PROJECT_PROCESSES_COMPLETE.md           | Stage 5 → Grounding Re-scoring                       | Process                    |
|                                 | src/ranking/improved_gemini_ranker.py   | Code                                                 | Full run() method          |
| **Performance**                 | PROJECT_PROCESSES_COMPLETE.md           | Performance & Metrics                                | 5–7 minutes                |
|                                 | STAGE_4_METHODOLOGY.md                  | Stage 5 → Performance                                | Timing                     |

---

### RANKING ALGORITHMS

| Topic                            | Document                                | Section/File                       | Details             |
| -------------------------------- | --------------------------------------- | ---------------------------------- | ------------------- |
| **Algorithm 1: TF-IDF Baseline** | PROJECT_PROCESSES_COMPLETE.md           | Ranking Algorithms → Algorithm 1   | Pros/cons           |
|                                  | src/ranking/baseline_ranker.py          | Code                               | Implementation      |
|                                  | STAGE_4_METHODOLOGY.md                  | Stage 2 → Technology               | Overview            |
| **Algorithm 2: Embeddings**      | PROJECT_PROCESSES_COMPLETE.md           | Ranking Algorithms → Algorithm 2   | Pros/cons           |
|                                  | src/ranking/embedding_ranker.py         | Code                               | Implementation      |
|                                  | STAGE_4_METHODOLOGY.md                  | Stage 3 → Technology               | Overview            |
| **Algorithm 3: Gemini LLM**      | PROJECT_PROCESSES_COMPLETE.md           | Ranking Algorithms → Algorithm 3   | Pros/cons           |
|                                  | src/ranking/gemini_ranker.py            | Code                               | Implementation      |
|                                  | STAGE_4_METHODOLOGY.md                  | Stage 4: Gemini Ranking Base       | Detailed            |
| **Algorithm 4: Improved Gemini** | PROJECT_PROCESSES_COMPLETE.md           | Ranking Algorithms → Algorithm 4   | Pros/cons           |
|                                  | src/ranking/improved_gemini_ranker.py   | Code                               | Implementation      |
|                                  | STAGE_4_METHODOLOGY.md                  | Stage 5: Improved Grounding        | Detailed            |
| **Algorithm 5: Ensemble**        | PROJECT_PROCESSES_COMPLETE.md           | Ranking Algorithms → Algorithm 5   | Methods             |
|                                  | src/ranking/ensemble_ranker.py          | Code                               | Implementation      |
| **Algorithm Comparison**         | PROJECT_PROCESSES_COMPLETE.md           | Ranking Algorithms (summary table) | Comparison          |
|                                  | COMPREHENSIVE_TRUSTWORTHINESS_REPORT.md | Comparative Analysis               | Stage 4 vs 5        |
|                                  | STAGE_4_JOB1_ECOMMERCE_AUDIT.md         | Job 1 Findings                     | Ranking differences |

---

### TRUSTWORTHINESS & METRICS

| Topic                       | Document                                | Section/File                                         | Details                  |
| --------------------------- | --------------------------------------- | ---------------------------------------------------- | ------------------------ |
| **Hallucination Rate**      | PROJECT_PROCESSES_COMPLETE.md           | Trustworthiness Validation → Hallucination Rate      | Definition + calculation |
|                             | COMPREHENSIVE_TRUSTWORTHINESS_REPORT.md | Stage 5 Modification                                 | Metric calculation       |
|                             | STAGE_4_METHODOLOGY.md                  | Stage 5 Modification                                 | Grounding checks         |
| **Completeness Score**      | PROJECT_PROCESSES_COMPLETE.md           | Trustworthiness Validation → Completeness Score      | Checks                   |
|                             | src/ranking/improved_gemini_ranker.py   | Code                                                 | \_is_incomplete_resume() |
| **Score Consistency**       | PROJECT_PROCESSES_COMPLETE.md           | Trustworthiness Validation → Score Consistency       | Ratios                   |
|                             | COMPREHENSIVE_TRUSTWORTHINESS_REPORT.md | Evaluation                                           | Consistency analysis     |
| **Coverage**                | PROJECT_PROCESSES_COMPLETE.md           | Trustworthiness Validation → Coverage                | Calculation              |
|                             | COMPREHENSIVE_TRUSTWORTHINESS_REPORT.md | Metrics                                              | Coverage percentage      |
| **Tier Assignment**         | PROJECT_PROCESSES_COMPLETE.md           | Trustworthiness Validation → Tier Assignment         | Decision rules           |
|                             | src/ranking/improved_gemini_ranker.py   | Code                                                 | Tier logic               |
| **Pre-Registered Failures** | PROJECT_PROCESSES_COMPLETE.md           | Trustworthiness Validation → Pre-Registered Failures | 3 issues                 |
|                             | COMPREHENSIVE_TRUSTWORTHINESS_REPORT.md | Pre-Registered Failures                              | Detailed                 |
| **Metrics Output**          | PROJECT_PROCESSES_COMPLETE.md           | Output & Results → Metrics Output                    | JSON format              |
|                             | src/metrics/trust_metrics.py            | Code                                                 | Implementation           |

---

### CONFIGURATION & PARAMETERS

| Topic                     | Document                              | Section/File                               | Details             |
| ------------------------- | ------------------------------------- | ------------------------------------------ | ------------------- |
| **Dataset Configuration** | PROJECT_PROCESSES_COMPLETE.md         | Configuration & Parameters → Dataset       | Paths + sizing      |
|                           | src/config.py                         | Lines 11–27                                | Configuration code  |
|                           | STAGE_4_METHODOLOGY.md                | Configuration & Inputs                     | File paths          |
| **Model Configuration**   | PROJECT_PROCESSES_COMPLETE.md         | Configuration & Parameters → Model         | Model names         |
|                           | src/config.py                         | Lines 29–32                                | Model configuration |
| **Rate Limiting Config**  | PROJECT_PROCESSES_COMPLETE.md         | Configuration & Parameters → Rate Limiting | Quota + retry       |
|                           | src/config.py                         | Not shown; in code                         | Rate limiting       |
|                           | STAGE_4_METHODOLOGY.md                | Rate Limiting & Performance                | Configuration       |
| **Caching Config**        | PROJECT_PROCESSES_COMPLETE.md         | Configuration & Parameters → Caching       | Cache settings      |
|                           | src/config.py                         | Lines 45–46                                | Cache configuration |
| **Scoring Parameters**    | PROJECT_PROCESSES_COMPLETE.md         | Configuration & Parameters → Scoring       | Thresholds          |
|                           | src/ranking/improved_gemini_ranker.py | Code                                       | Penalty thresholds  |
| **Environment Variables** | PROJECT_PROCESSES_COMPLETE.md         | Configuration & Parameters                 | API keys            |
|                           | src/config.py                         | Line 1–5                                   | .env loading        |

---

### OUTPUT & RESULTS

| Topic                   | Document                      | Section/File                               | Details              |
| ----------------------- | ----------------------------- | ------------------------------------------ | -------------------- |
| **Stage 1 JSON Output** | PROJECT_PROCESSES_COMPLETE.md | Output & Results → Stage Outputs → Stage 1 | Example JSON         |
|                         | outputs/stage_1.json          | File                                       | Actual output        |
| **Stage 2 JSON Output** | PROJECT_PROCESSES_COMPLETE.md | Output & Results → Stage Outputs → Stage 2 | Example JSON         |
|                         | outputs/stage_2.json          | File                                       | Actual output        |
| **Stage 3 JSON Output** | PROJECT_PROCESSES_COMPLETE.md | Output & Results → Stage Outputs → Stage 3 | Example JSON         |
|                         | outputs/stage_3.json          | File                                       | Actual output        |
| **Stage 4 JSON Output** | PROJECT_PROCESSES_COMPLETE.md | Output & Results → Stage Outputs → Stage 4 | Example JSON         |
|                         | outputs/stage_4.json          | File                                       | Actual output        |
|                         | STAGE_4_METHODOLOGY.md        | Output Structure → Stage 4 JSON            | Fields               |
| **Stage 5 JSON Output** | PROJECT_PROCESSES_COMPLETE.md | Output & Results → Stage Outputs → Stage 5 | Example JSON         |
|                         | outputs/stage_5.json          | File                                       | Actual output        |
| **Metrics JSON**        | PROJECT_PROCESSES_COMPLETE.md | Output & Results → Metrics Output          | Example JSON         |
|                         | outputs/metrics.json          | File                                       | Actual output        |
| **CSV Exports**         | PROJECT_PROCESSES_COMPLETE.md | Output & Results → CSV Exports             | stage_4_expanded.csv |
|                         | outputs/\*.csv                | Files                                      | CSV outputs          |
| **Comparison Reports**  | PROJECT_PROCESSES_COMPLETE.md | Output & Results → Comparison Reports      | compare_stages.json  |
|                         | outputs/compare_stages.json   | File                                       | Actual output        |

---

### PERFORMANCE & METRICS

| Topic                  | Document                                | Section/File                               | Details                    |
| ---------------------- | --------------------------------------- | ------------------------------------------ | -------------------------- |
| **Execution Timeline** | PROJECT_PROCESSES_COMPLETE.md           | Performance & Metrics → Execution Timeline | Stage times                |
|                        | STAGE_4_METHODOLOGY.md                  | Performance                                | Per-stage timing           |
| **Memory Usage**       | PROJECT_PROCESSES_COMPLETE.md           | Performance & Metrics → Memory Usage       | Peak usage                 |
| **Quality Metrics**    | PROJECT_PROCESSES_COMPLETE.md           | Performance & Metrics → Quality Metrics    | Hallucination, accuracy    |
|                        | COMPREHENSIVE_TRUSTWORTHINESS_REPORT.md | Evaluation                                 | Detailed metrics           |
| **Ranking Stability**  | PROJECT_PROCESSES_COMPLETE.md           | Metrics → Ranking Stability                | Correlation                |
|                        | COMPREHENSIVE_TRUSTWORTHINESS_REPORT.md | Comparative Analysis                       | Stage-to-stage correlation |
| **Accuracy Metrics**   | PROJECT_PROCESSES_COMPLETE.md           | Metrics → Accuracy Metrics                 | Stage vs GT                |
|                        | COMPREHENSIVE_TRUSTWORTHINESS_REPORT.md | Evaluation                                 | Accuracy calculation       |
| **Cost Analysis**      | PROJECT_PROCESSES_COMPLETE.md           | Performance & Metrics → Execution Timeline | Cost per run               |
|                        | STAGE_4_METHODOLOGY.md                  | Stage 4 → Cost                             | Per-resume estimate        |

---

### ERROR HANDLING

| Topic                            | Document                                | Section/File                      | Details                 |
| -------------------------------- | --------------------------------------- | --------------------------------- | ----------------------- |
| **Transient Errors (Retryable)** | PROJECT_PROCESSES_COMPLETE.md           | Error Handling → Transient Errors | 503, 429 handling       |
|                                  | src/ranking/gemini_ranker.py            | Code                              | Retry implementation    |
|                                  | STAGE_4_METHODOLOGY.md                  | Retry Logic                       | Exponential backoff     |
| **Data Validation Errors**       | PROJECT_PROCESSES_COMPLETE.md           | Error Handling → Data Validation  | Empty DF, missing JD    |
|                                  | src/evaluation/experiment_runner.py     | Code                              | Validation checks       |
| **Parsing Errors**               | PROJECT_PROCESSES_COMPLETE.md           | Error Handling → Parsing Errors   | Gemini response parsing |
|                                  | src/ranking/gemini_ranker.py            | Code                              | Response parsing        |
| **Empty-Input Guards**           | PROJECT_PROCESSES_COMPLETE.md           | Error Handling → Data Validation  | Cascading skip logic    |
|                                  | src/evaluation/experiment_runner.py     | Code                              | Validation              |
|                                  | COMPREHENSIVE_TRUSTWORTHINESS_REPORT.md | Software Engineer Path            | Empty filtering         |

---

### TESTING & VALIDATION

| Topic                       | Document                                | Section/File                                   | Details            |
| --------------------------- | --------------------------------------- | ---------------------------------------------- | ------------------ |
| **Test Harness**            | PROJECT_PROCESSES_COMPLETE.md           | Testing & Validation → Test Harness            | Usage              |
|                             | src/test_harness.py                     | Code                                           | Implementation     |
| **Validation Checks**       | PROJECT_PROCESSES_COMPLETE.md           | Testing & Validation → Validation Checks       | 4 check types      |
|                             | src/evaluation/experiment_runner.py     | Code                                           | Implementation     |
| **Schema Validation**       | PROJECT_PROCESSES_COMPLETE.md           | Testing & Validation → Schema Validation       | Field checking     |
| **Ground Truth Comparison** | PROJECT_PROCESSES_COMPLETE.md           | Testing & Validation → Ground Truth Comparison | Accuracy metrics   |
|                             | COMPREHENSIVE_TRUSTWORTHINESS_REPORT.md | Evaluation                                     | GT comparison      |
| **Smoke Tests**             | PROJECT_PROCESSES_COMPLETE.md           | Operational Workflows → Workflow 1             | Quick test         |
|                             | COMPREHENSIVE_TRUSTWORTHINESS_REPORT.md | Software Engineer Path                         | Smoke test results |

---

### TECHNICAL GOALS

| Goal                                       | Document                                | Section/File                          | Details                  |
| ------------------------------------------ | --------------------------------------- | ------------------------------------- | ------------------------ |
| **Goal 1: Filter & Rank Efficiently**      | PROJECT_PROCESSES_COMPLETE.md           | Technical Goals → Primary Goals → 1   | Funnel design            |
|                                            | STAGE_4_METHODOLOGY.md                  | Pipeline Overview                     | 5-stage funnel           |
|                                            | COMPREHENSIVE_TRUSTWORTHINESS_REPORT.md | Problem Domain                        | System design            |
| **Goal 2: Improve Through Algorithms**     | PROJECT_PROCESSES_COMPLETE.md           | Technical Goals → Primary Goals → 2   | Multi-algorithm          |
|                                            | Ranking Algorithms (all)                | All algorithms                        | Implementation           |
|                                            | COMPREHENSIVE_TRUSTWORTHINESS_REPORT.md | Comparative Analysis                  | Stage 4 vs 5             |
| **Goal 3: Detect Hallucinations**          | PROJECT_PROCESSES_COMPLETE.md           | Technical Goals → Primary Goals → 3   | Grounding checks         |
|                                            | src/ranking/improved_gemini_ranker.py   | Code                                  | Implementation           |
|                                            | STAGE_4_METHODOLOGY.md                  | Stage 5 → Hallucination detection     | Logic                    |
| **Goal 4: Validate Data Quality**          | PROJECT_PROCESSES_COMPLETE.md           | Technical Goals → Primary Goals → 4   | Validation               |
|                                            | src/ranking/improved_gemini_ranker.py   | Code                                  | \_is_incomplete_resume() |
|                                            | STAGE_4_SYSTEMIC_ISSUES.md              | Issue 3                               | Incomplete resumes       |
| **Goal 5: Provide Trustworthiness Scores** | PROJECT_PROCESSES_COMPLETE.md           | Technical Goals → Primary Goals → 5   | Score design             |
|                                            | COMPREHENSIVE_TRUSTWORTHINESS_REPORT.md | Trustworthiness Evaluation            | Scoring approach         |
| **Goal 6: Support Multiple Roles**         | PROJECT_PROCESSES_COMPLETE.md           | Technical Goals → Secondary Goals → 1 | Role support             |
|                                            | src/loader.py                           | Code                                  | Role matching            |
|                                            | STAGE_4_METHODOLOGY.md                  | Stage 1 → Role Normalization          | Fuzzy matching           |
| **Goal 7: Enable Comparison**              | PROJECT_PROCESSES_COMPLETE.md           | Technical Goals → Secondary Goals → 2 | Comparative analysis     |
|                                            | src/evaluation/compare_stages.py        | Code                                  | Implementation           |
|                                            | COMPREHENSIVE_TRUSTWORTHINESS_REPORT.md | Comparative Analysis                  | Results                  |
| **Goal 8: Provide Audit Trail**            | PROJECT_PROCESSES_COMPLETE.md           | Technical Goals → Secondary Goals → 3 | Audit reports            |
|                                            | STAGE_4_JOB1_ECOMMERCE_AUDIT.md         | Full file                             | E-commerce audit         |
|                                            | STAGE_4_JOB2_SOFTWARE_ENGINEER_AUDIT.md | Full file                             | SE audit                 |
| **Goal 9: Optimize Cost**                  | PROJECT_PROCESSES_COMPLETE.md           | Technical Goals → Secondary Goals → 4 | Cost optimization        |
|                                            | STAGE_4_METHODOLOGY.md                  | Rate Limiting & Performance           | Cost estimates           |
|                                            | src/config.py                           | Cache settings                        | Caching for cost         |
| **Goal 10: Measure Trustworthiness**       | PROJECT_PROCESSES_COMPLETE.md           | Technical Goals → Secondary Goals → 5 | Metrics                  |
|                                            | COMPREHENSIVE_TRUSTWORTHINESS_REPORT.md | Quantitative Metrics                  | Metric details           |
|                                            | src/metrics/trust_metrics.py            | Code                                  | Implementation           |

---

### OPERATIONAL WORKFLOWS

| Workflow                            | Document                                | Section/File                       | Details           |
| ----------------------------------- | --------------------------------------- | ---------------------------------- | ----------------- |
| **Workflow 1: Smoke Test**          | PROJECT_PROCESSES_COMPLETE.md           | Operational Workflows → Workflow 1 | Quick test        |
|                                     | COMPREHENSIVE_TRUSTWORTHINESS_REPORT.md | Software Engineer Path             | Smoke test result |
| **Workflow 2: Full Production Run** | PROJECT_PROCESSES_COMPLETE.md           | Operational Workflows → Workflow 2 | Full pipeline     |
|                                     | src/main.py                             | Code                               | Entry point       |
| **Workflow 3: Audit & Comparison**  | PROJECT_PROCESSES_COMPLETE.md           | Operational Workflows → Workflow 3 | Comparison        |
|                                     | src/evaluation/compare_stages.py        | Code                               | Implementation    |
| **Workflow 4: Metrics & Reporting** | PROJECT_PROCESSES_COMPLETE.md           | Operational Workflows → Workflow 4 | Report generation |
|                                     | src/metrics/trust_metrics.py            | Code                               | Implementation    |

---

### AUDIT FINDINGS

| Finding                         | Document                                | Section/File                     | Details                     |
| ------------------------------- | --------------------------------------- | -------------------------------- | --------------------------- |
| **E-commerce Specialist Audit** | STAGE_4_JOB1_ECOMMERCE_AUDIT.md         | Full file                        | 50 candidates analyzed      |
|                                 | STAGE_4_AUDIT_OVERVIEW.md               | Job 1 section                    | Summary                     |
| **Software Engineer Audit**     | STAGE_4_JOB2_SOFTWARE_ENGINEER_AUDIT.md | Full file                        | 50 candidates analyzed      |
|                                 | STAGE_4_AUDIT_OVERVIEW.md               | Job 2 section                    | Summary                     |
| **Critical Errors**             | STAGE_4_JOB1_ECOMMERCE_AUDIT.md         | Critical Errors                  | 1 error                     |
|                                 | STAGE_4_JOB2_SOFTWARE_ENGINEER_AUDIT.md | Critical Errors                  | 3 errors                    |
| **Systemic Issues**             | STAGE_4_SYSTEMIC_ISSUES.md              | Full file                        | 6 issues identified         |
|                                 | STAGE_4_AUDIT_OVERVIEW.md               | Root Causes                      | Summary                     |
| **Recommendations**             | STAGE_4_RECOMMENDATIONS.md              | Full file                        | Immediate + short/long-term |
|                                 | STAGE_4_AUDIT_OVERVIEW.md               | Key Findings                     | Immediate actions           |
| **Score Clustering**            | STAGE_4_SYSTEMIC_ISSUES.md              | Issue 1                          | Detailed analysis           |
|                                 | STAGE_4_JOB1_ECOMMERCE_AUDIT.md         | Score Distribution               | 18 @ 95                     |
|                                 | STAGE_4_JOB2_SOFTWARE_ENGINEER_AUDIT.md | Score Distribution               | 24 @ 85                     |
| **AI Boilerplate**              | STAGE_4_SYSTEMIC_ISSUES.md              | Issue 2                          | Inconsistent penalty        |
|                                 | STAGE_4_JOB1_ECOMMERCE_AUDIT.md         | AI Template Boilerplate          | 12 examples                 |
|                                 | STAGE_4_JOB2_SOFTWARE_ENGINEER_AUDIT.md | AI Template Boilerplate          | 13 examples                 |
| **Incomplete Resumes**          | STAGE_4_SYSTEMIC_ISSUES.md              | Issue 3                          | 4 examples                  |
|                                 | STAGE_4_JOB1_ECOMMERCE_AUDIT.md         | Critical Errors → Courtney Walsh | Unfilled template           |
|                                 | STAGE_4_JOB2_SOFTWARE_ENGINEER_AUDIT.md | Critical Errors                  | 3 examples                  |

---

## File Cross-Reference Index

### By Filename

| File                                        | Purpose                          | Key Sections                               |
| ------------------------------------------- | -------------------------------- | ------------------------------------------ |
| **PROJECT_PROCESSES_COMPLETE.md**           | Main process documentation       | All stages, algorithms, goals              |
| **PROJECT_MAP_WHERE_DOCUMENTED.md**         | This file                        | Cross-reference guide                      |
| **STAGE_4_METHODOLOGY.md**                  | Stage 4 & pipeline context       | Architecture, rate limiting, configuration |
| **STAGE_4_AUDIT_OVERVIEW.md**               | Executive summary                | Critical issues, statistics                |
| **STAGE_4_JOB1_ECOMMERCE_AUDIT.md**         | E-commerce detailed audit        | 50 candidates, errors, recommendations     |
| **STAGE_4_JOB2_SOFTWARE_ENGINEER_AUDIT.md** | Software Engineer detailed audit | 50 candidates, errors, recommendations     |
| **STAGE_4_SYSTEMIC_ISSUES.md**              | Root cause analysis              | 6 systemic problems, impact                |
| **STAGE_4_RECOMMENDATIONS.md**              | Action plan                      | Immediate, short-term, long-term fixes     |
| **STAGE_4_AUDIT_INDEX.md**                  | Navigation guide                 | Reading paths, file organization           |
| **COMPREHENSIVE_TRUSTWORTHINESS_REPORT.md** | Assignment alignment             | Trust metrics, modifications, evaluation   |
| **src/config.py**                           | Configuration                    | Dataset, models, parameters                |
| **src/main.py**                             | Entry point                      | Interactive menu                           |
| **src/filter_roles.py**                     | Stage 1                          | Role filtering implementation              |
| **src/loader.py**                           | Data loading                     | Dataset + JD loading                       |
| **src/ranking/baseline_ranker.py**          | Stage 2                          | TF-IDF ranking                             |
| **src/ranking/embedding_ranker.py**         | Stage 3                          | Embedding ranking                          |
| **src/ranking/gemini_ranker.py**            | Stage 4                          | Gemini API scoring                         |
| **src/ranking/improved_gemini_ranker.py**   | Stage 5                          | Grounding + hallucination detection        |
| **src/ranking/ensemble_ranker.py**          | Optional                         | Algorithm combination                      |
| **src/metrics/trust_metrics.py**            | Metrics                          | Trustworthiness score calculation          |
| **src/evaluation/experiment_runner.py**     | Orchestration                    | Full pipeline runner                       |
| **src/evaluation/compare_stages.py**        | Analysis                         | Stage comparison                           |
| **src/test_harness.py**                     | Testing                          | Smoke tests                                |

---

## Search Guide — Find Topics By Keyword

### A

- **Accuracy:** COMPREHENSIVE_TRUSTWORTHINESS_REPORT.md (Evaluation); PROJECT_PROCESSES_COMPLETE.md (Performance & Metrics)
- **Algorithm:** PROJECT_PROCESSES_COMPLETE.md (Ranking Algorithms); STAGE_4_METHODOLOGY.md (Stage operations)
- **API:** STAGE_4_METHODOLOGY.md (Gemini API); src/config.py (API keys)

### B

- **Baseline:** PROJECT_PROCESSES_COMPLETE.md (Algorithm 1); src/ranking/baseline_ranker.py
- **Boilerplate:** STAGE_4_JOB1_ECOMMERCE_AUDIT.md; STAGE_4_JOB2_SOFTWARE_ENGINEER_AUDIT.md; STAGE_4_SYSTEMIC_ISSUES.md

### C

- **Caching:** PROJECT_PROCESSES_COMPLETE.md (Stage 4); STAGE_4_METHODOLOGY.md
- **Configuration:** PROJECT_PROCESSES_COMPLETE.md (Configuration & Parameters); src/config.py
- **Cost:** PROJECT_PROCESSES_COMPLETE.md (Performance & Metrics); STAGE_4_METHODOLOGY.md

### D

- **Data Quality:** PROJECT_PROCESSES_COMPLETE.md (Validation); STAGE_4_SYSTEMIC_ISSUES.md
- **Dataset:** PROJECT_PROCESSES_COMPLETE.md (Input); src/config.py

### E

- **Embedding:** PROJECT_PROCESSES_COMPLETE.md (Algorithm 2); src/ranking/embedding_ranker.py
- **Error Handling:** PROJECT_PROCESSES_COMPLETE.md (Error Handling); src/ranking/gemini_ranker.py
- **Evaluation:** COMPREHENSIVE_TRUSTWORTHINESS_REPORT.md; src/evaluation/

### F

- **Failure:** PROJECT_PROCESSES_COMPLETE.md (Pre-Registered Failures); COMPREHENSIVE_TRUSTWORTHINESS_REPORT.md
- **Filtering:** PROJECT_PROCESSES_COMPLETE.md (Stage 1); src/filter_roles.py
- **Funnel:** PROJECT_PROCESSES_COMPLETE.md (Pipeline); STAGE_4_METHODOLOGY.md

### G

- **Gemini:** PROJECT_PROCESSES_COMPLETE.md (Stage 4, Algorithm 3); src/ranking/gemini_ranker.py
- **Grounding:** PROJECT_PROCESSES_COMPLETE.md (Stage 5); src/ranking/improved_gemini_ranker.py
- **Ground Truth:** PROJECT_PROCESSES_COMPLETE.md (Validation); COMPREHENSIVE_TRUSTWORTHINESS_REPORT.md

### H

- **Hallucination:** PROJECT_PROCESSES_COMPLETE.md (Stage 5, Trustworthiness); src/ranking/improved_gemini_ranker.py

### I

- **Incomplete Resumes:** PROJECT_PROCESSES_COMPLETE.md (Stage 5); STAGE_4_SYSTEMIC_ISSUES.md

### J

- **Job Description:** PROJECT_PROCESSES_COMPLETE.md (Data Flow); STAGE_4_METHODOLOGY.md

### M

- **Metrics:** PROJECT_PROCESSES_COMPLETE.md (Trustworthiness Validation); COMPREHENSIVE_TRUSTWORTHINESS_REPORT.md
- **Memory:** PROJECT_PROCESSES_COMPLETE.md (Performance & Metrics)

### O

- **Output:** PROJECT_PROCESSES_COMPLETE.md (Output & Results); outputs/ directory

### P

- **Performance:** PROJECT_PROCESSES_COMPLETE.md (Performance & Metrics); STAGE_4_METHODOLOGY.md
- **Pipeline:** PROJECT_PROCESSES_COMPLETE.md (High-Level Architecture); STAGE_4_METHODOLOGY.md
- **Prompt:** PROJECT_PROCESSES_COMPLETE.md (Stage 4); STAGE_4_RECOMMENDATIONS.md

### R

- **Rate Limiting:** PROJECT_PROCESSES_COMPLETE.md (Stage 4); STAGE_4_METHODOLOGY.md
- **Ranking:** PROJECT_PROCESSES_COMPLETE.md (Ranking Algorithms); src/ranking/

### S

- **Schema:** PROJECT_PROCESSES_COMPLETE.md (Validation); outputs/
- **Scoring:** PROJECT_PROCESSES_COMPLETE.md (All stages); src/ranking/
- **Stage 1:** PROJECT_PROCESSES_COMPLETE.md; STAGE_4_METHODOLOGY.md; src/filter_roles.py
- **Stage 2:** PROJECT_PROCESSES_COMPLETE.md; STAGE_4_METHODOLOGY.md; src/ranking/baseline_ranker.py
- **Stage 3:** PROJECT_PROCESSES_COMPLETE.md; STAGE_4_METHODOLOGY.md; src/ranking/embedding_ranker.py
- **Stage 4:** PROJECT_PROCESSES_COMPLETE.md; STAGE_4_METHODOLOGY.md; STAGE_4_JOB\*\_AUDIT.md; src/ranking/gemini_ranker.py
- **Stage 5:** PROJECT_PROCESSES_COMPLETE.md; STAGE_4_METHODOLOGY.md; src/ranking/improved_gemini_ranker.py
- **Stability:** PROJECT_PROCESSES_COMPLETE.md (Ranking Stability); COMPREHENSIVE_TRUSTWORTHINESS_REPORT.md

### T

- **Test:** PROJECT_PROCESSES_COMPLETE.md (Testing & Validation); src/test_harness.py
- **TF-IDF:** PROJECT_PROCESSES_COMPLETE.md (Algorithm 1); src/ranking/baseline_ranker.py
- **Tier:** PROJECT_PROCESSES_COMPLETE.md (Tier Assignment); COMPREHENSIVE_TRUSTWORTHINESS_REPORT.md
- **Trust:** PROJECT_PROCESSES_COMPLETE.md (Trustworthiness Validation); COMPREHENSIVE_TRUSTWORTHINESS_REPORT.md

### V

- **Validation:** PROJECT_PROCESSES_COMPLETE.md (Testing & Validation); src/evaluation/experiment_runner.py

### W

- **Workflow:** PROJECT_PROCESSES_COMPLETE.md (Operational Workflows); src/main.py

---

## Quick Answer Guide

**Q: How does the pipeline work?**
A: See PROJECT_PROCESSES_COMPLETE.md → High-Level Architecture (diagram + stages)

**Q: What is Stage 4?**
A: See PROJECT_PROCESSES_COMPLETE.md → Stage 4: Gemini LLM Scoring + STAGE_4_METHODOLOGY.md

**Q: How is hallucination detected?**
A: See PROJECT_PROCESSES_COMPLETE.md → Stage 5 → Skill Hallucination Detection + src/ranking/improved_gemini_ranker.py

**Q: What are the critical errors found?**
A: See STAGE_4_JOB1_ECOMMERCE_AUDIT.md → Critical Errors + STAGE_4_JOB2_SOFTWARE_ENGINEER_AUDIT.md → Critical Errors

**Q: What should be fixed immediately?**
A: See STAGE_4_RECOMMENDATIONS.md → Immediate Actions

**Q: What are the technical goals?**
A: See PROJECT_PROCESSES_COMPLETE.md → Technical Goals

**Q: How are metrics calculated?**
A: See PROJECT_PROCESSES_COMPLETE.md → Trustworthiness Validation + COMPREHENSIVE_TRUSTWORTHINESS_REPORT.md

**Q: How does rate limiting work?**
A: See PROJECT_PROCESSES_COMPLETE.md → Configuration → Rate Limiting + STAGE_4_METHODOLOGY.md → Rate Limiting

**Q: What's the cost per run?**
A: See PROJECT_PROCESSES_COMPLETE.md → Performance & Metrics → Execution Timeline (~$0.30)

**Q: How is data quality validated?**
A: See PROJECT_PROCESSES_COMPLETE.md → Testing & Validation + src/ranking/improved_gemini_ranker.py

---

## File Tree for Reference

```
resume-trust-lab/
├── PROJECT_PROCESSES_COMPLETE.md         ← MAIN PROCESS DOCUMENTATION
├── PROJECT_MAP_WHERE_DOCUMENTED.md       ← THIS FILE (Cross-reference guide)
├── STAGE_4_AUDIT_OVERVIEW.md             ← Executive summary of audit
├── STAGE_4_AUDIT_INDEX.md                ← Navigation guide for audit reports
├── STAGE_4_METHODOLOGY.md                ← How Stage 4 works in detail
├── STAGE_4_JOB1_ECOMMERCE_AUDIT.md       ← E-commerce detailed audit
├── STAGE_4_JOB2_SOFTWARE_ENGINEER_AUDIT.md ← Software Engineer detailed audit
├── STAGE_4_SYSTEMIC_ISSUES.md            ← Root cause analysis
├── STAGE_4_RECOMMENDATIONS.md            ← Action plan for fixes
├── COMPREHENSIVE_TRUSTWORTHINESS_REPORT.md ← Assignment alignment + evaluation
├── src/
│   ├── config.py                         ← Configuration
│   ├── main.py                           ← Entry point
│   ├── filter_roles.py                   ← Stage 1
│   ├── loader.py                         ← Data loading
│   ├── ranking/
│   │   ├── baseline_ranker.py            ← Stage 2: TF-IDF
│   │   ├── embedding_ranker.py           ← Stage 3: Embeddings
│   │   ├── gemini_ranker.py              ← Stage 4: Gemini
│   │   ├── improved_gemini_ranker.py     ← Stage 5: Grounding
│   │   └── ensemble_ranker.py            ← Optional: Ensemble
│   ├── metrics/
│   │   ├── trust_metrics.py              ← Trust score calculation
│   │   └── failure_analysis.py           ← Failure categorization
│   ├── evaluation/
│   │   ├── experiment_runner.py          ← Pipeline orchestration
│   │   └── compare_stages.py             ← Stage comparison
│   └── test_harness.py                   ← Smoke tests
└── outputs/
    ├── stage_1.json                      ← Stage 1 results
    ├── stage_2.json                      ← Stage 2 results
    ├── stage_3.json                      ← Stage 3 results
    ├── stage_4.json                      ← Stage 4 results
    ├── stage_5.json                      ← Stage 5 results
    ├── metrics.json                      ← Calculated metrics
    ├── compare_stages.json               ← Comparison analysis
    └── failure_analysis.json             ← Failure categorization
```

---

_This mapping document enables quick navigation of all project documentation. For a specific topic, start with the "Quick Lookup Table" or "Search Guide" above._
