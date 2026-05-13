# Stage 4 Audit Report — Complete Documentation

**Report Date:** May 13, 2026  
**Status:** Analysis Complete | Ready for Action  
**Total Candidates Analyzed:** 100 (50 per role)  
**Issues Identified:** 6 systemic + 10+ role-specific  
**Files Created:** 6 comprehensive markdown reports

---

## Quick Navigation

### For Stakeholders (Busy Executives)

Start here: **[STAGE_4_AUDIT_OVERVIEW.md](STAGE_4_AUDIT_OVERVIEW.md)**

- 5-minute read
- Key statistics, critical issues, next steps
- Suitable for hiring manager or product lead

### For Engineering (Implementation Team)

1. **Understand the system:** [STAGE_4_METHODOLOGY.md](STAGE_4_METHODOLOGY.md)
   - Full pipeline architecture (Stages 1–5)
   - Stage 4 scoring logic & rate limiting
   - Configuration & inputs

2. **Identify what went wrong:** [STAGE_4_SYSTEMIC_ISSUES.md](STAGE_4_SYSTEMIC_ISSUES.md)
   - Root cause analysis
   - 6 major systemic problems
   - Cross-job patterns

3. **Implement fixes:** [STAGE_4_RECOMMENDATIONS.md](STAGE_4_RECOMMENDATIONS.md)
   - Immediate actions (today)
   - Short-term improvements (1–2 weeks)
   - Long-term strategy (1–2 months)
   - Code examples provided

### For Auditors (Compliance / QA)

1. **E-commerce Specialist audit:** [STAGE_4_JOB1_ECOMMERCE_AUDIT.md](STAGE_4_JOB1_ECOMMERCE_AUDIT.md)
   - 50 candidates analyzed
   - 7 overscored, 3 underscored, 1 critical error
   - JD requirements vs. actual skill coverage

2. **Software Engineer audit:** [STAGE_4_JOB2_SOFTWARE_ENGINEER_AUDIT.md](STAGE_4_JOB2_SOFTWARE_ENGINEER_AUDIT.md)
   - 50 candidates analyzed
   - 6 overscored, 5 underscored, 3 critical errors
   - Detailed candidate-by-candidate analysis

---

## Document Summary

### File: STAGE_4_AUDIT_OVERVIEW.md

**Purpose:** Entry point for all audiences  
**Length:** ~2,000 words | ~5 minutes  
**Contents:**

- Executive summary (key findings)
- Root cause summary
- Critical issues requiring action
- Key statistics
- File organization guide

**Key Takeaway:** 42% of candidates tied at single score; 4 resumes should be disqualified; fixes needed before using ranking.

---

### File: STAGE_4_METHODOLOGY.md

**Purpose:** Explain how the pipeline works end-to-end  
**Length:** ~3,500 words | ~12 minutes  
**Contents:**

- The 5-stage funnel (1: Role filter → 5: Grounding)
- Stage 4 detailed operation
- Scoring logic & Gemini prompting
- Rate limiting (13 req/min)
- Caching strategy
- Configuration & inputs
- Known limitations

**Key Takeaway:** Stage 4 scores on 1–10 scale (mapped to 1–100); no skill-by-skill rubric; AI boilerplate not penalized consistently.

---

### File: STAGE_4_JOB1_ECOMMERCE_AUDIT.md

**Purpose:** Detailed audit of E-commerce Specialist role  
**Length:** ~4,000 words | ~15 minutes  
**Contents:**

- Job description summary (responsibilities, requirements)
- Score distribution analysis (18 @ 95 clustering)
- 1 critical error (unfilled template)
- 7 overscored candidates (detailed analysis each)
- 3 underscored candidates (including most severe error: Jason Jones @ 75)
- 12 AI template boilerplate flags
- Integrity & quality flags

**Key Takeaway:** Jason Jones (Rank 50, 75pts) has Shopify Plus certification + full skill coverage but scores 10 points below cutoff — likely underscored by 15–20 points.

---

### File: STAGE_4_JOB2_SOFTWARE_ENGINEER_AUDIT.md

**Purpose:** Detailed audit of Software Engineer role  
**Length:** ~5,500 words | ~20 minutes  
**Contents:**

- Job description summary (Java, DevOps, system design, etc.)
- Score distribution analysis (24 @ 85 clustering)
- 3 critical errors (rejection letter, duplicates, student)
- 6 overscored candidates
- 5 underscored candidates (including Victor Johnson @ 45 and Steve King @ 40)
- 13 AI template boilerplate flags
- 12 single-name entries (identity unverifiable)
- Self-referential AI commentary

**Key Takeaway:** Victor Johnson (Master's in Software Engineering, DevOps expert) scores 45 — likely scoring engine failure; should be ~78.

---

### File: STAGE_4_SYSTEMIC_ISSUES.md

**Purpose:** Cross-job analysis; identify root causes not role-specific  
**Length:** ~3,500 words | ~12 minutes  
**Contents:**

- 6 systemic issues (with metrics)
- Issue 1: Score clustering (42% tied at single score)
- Issue 2: AI boilerplate inconsistency (25% have it, all score ranges)
- Issue 3: Incomplete resumes (unfilled templates, placeholder dates)
- Issue 4: Duplicate entries (deduplication failed)
- Issue 5: Underqualified candidates (students in professional ranking)
- Issue 6: Data quality upstream (24% identity unverifiable)
- Root cause analysis (insufficient validation, coarse scoring rubric)
- Impact assessment (hiring risk, financial impact)
- Severity matrix

**Key Takeaway:** Problems stem from insufficient pipeline validation (no pre-Stage-4 checks) and coarse scoring granularity (1–10 scale naturally clusters).

---

### File: STAGE_4_RECOMMENDATIONS.md

**Purpose:** Actionable fix plan with code examples  
**Length:** ~5,000 words | ~18 minutes  
**Contents:**

- **Immediate (today):**
  - Disqualify 4 resumes (code provided)
  - Remove duplicate Amara
  - Manually review Victor/Steve
  - Regenerate corrected rankings
- **Short-term (1–2 weeks):**
  - Pre-Stage-4 validator (with code)
  - Email deduplication (with code)
  - AI boilerplate penalty (with code)
  - Experience filtering (with code)
- **Long-term (1–2 months):**
  - Redesign Gemini prompt with rubric
  - Request finer-grained output (1–100 directly)
  - Post-Stage-4 audit sampling
  - Calibrate against ground truth hiring decisions
- Implementation checklist
- Success metrics (current vs target)

**Key Takeaway:** Fix clustered scoring by using rubric (skill-by-skill) instead of single score; validate data before Stage 4; measure against actual hiring outcomes.

---

## Cross-File Reading Paths

### Path 1: "I need to fix this TODAY" (Executive)

1. [Overview](STAGE_4_AUDIT_OVERVIEW.md) — 5 min — understand the crisis
2. [Recommendations → Immediate Actions](STAGE_4_RECOMMENDATIONS.md#immediate-actions-before-using-rankings) — 10 min — what to do now
3. [Job 1 audit](STAGE_4_JOB1_ECOMMERCE_AUDIT.md#critical-errors) + [Job 2 audit](STAGE_4_JOB2_SOFTWARE_ENGINEER_AUDIT.md#critical-errors) — 10 min — which candidates to remove

**Total time:** 25 minutes  
**Outcome:** Ready to issue immediate fix orders

---

### Path 2: "I need to prevent this NEXT TIME" (Engineer)

1. [Methodology](STAGE_4_METHODOLOGY.md) — 12 min — how scoring works
2. [Systemic Issues](STAGE_4_SYSTEMIC_ISSUES.md) — 12 min — what went wrong
3. [Recommendations → Short-Term](STAGE_4_RECOMMENDATIONS.md#short-term-improvements-before-next-run) — 15 min — code examples for fixes
4. [Recommendations → Implementation Checklist](STAGE_4_RECOMMENDATIONS.md#implementation-checklist) — 5 min — priority order

**Total time:** 45 minutes  
**Outcome:** Ready to implement short-term improvements

---

### Path 3: "I need to rebuild this RIGHT" (Architect)

1. [Methodology](STAGE_4_METHODOLOGY.md) — 12 min — current state
2. [Systemic Issues](STAGE_4_SYSTEMIC_ISSUES.md) — 12 min — root causes
3. [Recommendations → Long-Term Strategy](STAGE_4_RECOMMENDATIONS.md#long-term-strategy-architecture-changes) — 20 min — redesign options
4. Both job audits — 35 min — understand failure modes
5. [Recommendations → Success Metrics](STAGE_4_RECOMMENDATIONS.md#success-metrics) — 5 min — targets

**Total time:** 85 minutes  
**Outcome:** Design document for Stage 4 v2.0

---

### Path 4: "I need to audit a SPECIFIC CANDIDATE" (Recruiter)

1. [Overview](STAGE_4_AUDIT_OVERVIEW.md#most-severe-errors) — 2 min — check if they're highlighted
2. Find role in [Job 1](STAGE_4_JOB1_ECOMMERCE_AUDIT.md) or [Job 2](STAGE_4_JOB2_SOFTWARE_ENGINEER_AUDIT.md)
3. Search for candidate name in respective audit file
4. Read candidate entry (2–3 min per candidate)
5. Cross-reference with [Methodology](STAGE_4_METHODOLOGY.md#scoring-logic--prompting) if need to understand why they scored that way

**Example:**

```
Looking for: Victor Johnson (Software Engineer)
Search: STAGE_4_JOB2_SOFTWARE_ENGINEER_AUDIT.md for "Victor Johnson"
Result: Found in "Underscored Candidates" section
Finding: Ranks 48 out of 50 with 45 points
Issue: Master's degree + DevOps expertise should score ~78, not 45
Action: Flag for manual review / likely scoring engine error
```

---

## Key Statistics Summary

### E-commerce Specialist (50 candidates)

| Metric                 | Value          |
| ---------------------- | -------------- |
| Score range            | 75–95          |
| Mean score             | 90.72          |
| Largest cluster        | 18 @ 95 (36%)  |
| Overscored candidates  | 7              |
| Underscored candidates | 3              |
| Critical errors        | 1 (disqualify) |
| AI boilerplate         | 12 (24%)       |

### Software Engineer (50 candidates)

| Metric                 | Value                 |
| ---------------------- | --------------------- |
| Score range            | 35–90                 |
| Mean score             | 78.4                  |
| Largest cluster        | 24 @ 85 (48%)         |
| Overscored candidates  | 6                     |
| Underscored candidates | 5                     |
| Critical errors        | 3 (disqualify/review) |
| AI boilerplate         | 13 (26%)              |

### Combined (100 candidates)

| Metric                                 | Count | %     |
| -------------------------------------- | ----- | ----- |
| Problem candidates                     | ~35   | 35%   |
| Score clustered (unusable for ranking) | 42    | 42%   |
| AI boilerplate (inconsistent penalty)  | 25    | 25%   |
| Identity unverifiable                  | ~13   | 13%   |
| Need manual review                     | 5–10  | 5–10% |

---

## Critical Actions Summary

### STOP Using Current Rankings?

**Recommendation:** Do not make hiring decisions based on current Stage 4 output until:

1. ✅ Disqualify 4 invalid resumes (template, rejection letter, duplicate)
2. ✅ Manually review 2–3 likely scoring errors (Victor, Steve)
3. ✅ Regenerate ranking with cleaned data

**Estimated effort:** 2–3 hours for the engineering team

### Immediate Decisions

| Candidate      | Job   | Rank   | Score  | Action                         |
| -------------- | ----- | ------ | ------ | ------------------------------ |
| Courtney Walsh | E-com | 22     | 92     | Disqualify (unfilled)          |
| Sonia          | SE    | 31     | 85     | Disqualify (rejection letter)  |
| Ananya         | SE    | 14     | 85     | Disqualify (placeholder dates) |
| Diya           | SE    | 50     | 35     | Filter (student)               |
| Amara ×2       | SE    | 23, 28 | 85, 85 | Remove duplicate               |
| Victor Johnson | SE    | 48     | 45     | Manual review                  |
| Steve King     | SE    | 49     | 40     | Manual review                  |

---

## File Locations

All files are located in:

```
/Users/samankgupta/Downloads/TAI Final Project/resume-trust-lab/
```

### Report Files (Newly Created)

- `STAGE_4_AUDIT_OVERVIEW.md` ← **START HERE**
- `STAGE_4_METHODOLOGY.md` (pipeline architecture)
- `STAGE_4_JOB1_ECOMMERCE_AUDIT.md` (E-commerce audit)
- `STAGE_4_JOB2_SOFTWARE_ENGINEER_AUDIT.md` (Software Engineer audit)
- `STAGE_4_SYSTEMIC_ISSUES.md` (root causes)
- `STAGE_4_RECOMMENDATIONS.md` (action plan)

### Related Existing Files

- `outputs/stage_4.json` (raw Gemini scores)
- `outputs/stage_4.csv` (CSV export if available)
- `src/ranking/gemini_ranker.py` (Stage 4 implementation)
- `src/evaluation/experiment_runner.py` (pipeline orchestration)

---

## Feedback & Questions?

If you need clarification on any finding:

1. Check the relevant job-specific audit ([Job 1](STAGE_4_JOB1_ECOMMERCE_AUDIT.md) or [Job 2](STAGE_4_JOB2_SOFTWARE_ENGINEER_AUDIT.md))
2. Cross-reference with [Methodology](STAGE_4_METHODOLOGY.md) for scoring logic
3. See [Systemic Issues](STAGE_4_SYSTEMIC_ISSUES.md) for root cause explanation
4. Refer to [Recommendations](STAGE_4_RECOMMENDATIONS.md) for how to fix

---

## Next Steps

1. **Read** [STAGE_4_AUDIT_OVERVIEW.md](STAGE_4_AUDIT_OVERVIEW.md) (5 min)
2. **Decide** which files to deep-dive based on your role (executive/engineer/auditor)
3. **Act** on immediate recommendations before using rankings
4. **Plan** short-term and long-term improvements
5. **Track** success metrics after implementation

---

_Report generated from comprehensive audit of Stage 4 (Gemini Ranking Base) across 100 resumes (50 E-commerce Specialist, 50 Software Engineer). All data verified against job descriptions and resume content._

**Report Status:** ✅ Complete | ✅ Actionable | ⚠️ Urgent Review Needed
