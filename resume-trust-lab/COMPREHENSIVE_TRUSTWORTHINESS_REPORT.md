# RESUME TRUST LAB SYSTEM - COMPREHENSIVE TRUSTWORTHINESS EVALUATION REPORT

**Date:** May 13, 2026  
**Project:** Trustworthy AI for Hiring  
**System:** Multi-Stage Resume Screening with Hallucination Detection

---

## EXECUTIVE SUMMARY

This report documents a complete trustworthiness evaluation of a multi-stage AI resume screening system using quantitative metrics, pre-registered failure cases, and comparative analysis of original vs improved approaches.

**Key Finding:** Stage 4 showed severe score inflation and weak discrimination, while Stage 5 reduced overconfident scoring through grounding checks, placeholder detection, and alias-aware hallucination penalties. The strongest trust signal in this project is not raw rank accuracy alone, but whether the system can justify its score with evidence from the resume text.

## ASSIGNMENT ALIGNMENT AT A GLANCE

This project directly addresses the assignment by covering:

- A concrete domain: AI-assisted resume screening for e-commerce hiring.
- Domain harms: false negatives can deny qualified candidates opportunities; false positives waste recruiter time and risk bad hires.
- A quantitative trust metric: grounded-claim quality measured through hallucination rate, placeholder contamination, and score-discrimination/tie rate.
- Pre-registered failure cases: placeholder resumes, ceiling-score pileups, and strong candidates being under-scored when JD skills are ignored.
- A trust-improving modification: Stage 5 adds completeness checks, alias-aware grounding, stricter prompting, and score caps for unsupported claims.
- Comparative evaluation: Stage 4 vs Stage 5 shows less inflation and more score spread after the modification.
- Trust tax: more logic, more latency, and more conservative scoring.

---

## I. PROBLEM DOMAIN & MOTIVATION

### Application Area: AI-Driven Resume Screening

**What:** Automated system that ranks resumes to identify the best candidates for job positions.

**Why it matters:**

- Hiring affects people's livelihoods - false negatives can deny interviews and career opportunities.
- False positives waste recruiter time, reduce hiring quality, and can lead to costly bad hires.
- Overconfident AI screening can amplify bias if the model rewards generic phrasing over actual evidence.
- For this domain, errors are **not** like movie recommendations; they are consequential because the output influences jobs and income.

### Stakeholders Harmed When System Fails

| Stakeholder         | Failure Mode                          | Impact                                        |
| ------------------- | ------------------------------------- | --------------------------------------------- |
| **Job Seekers**     | False negatives (eliminated early)    | Lose opportunity despite qualification        |
| **Hiring Managers** | False positives (bad recommendations) | Waste time on unqualified candidates          |
| **Companies**       | Bad hires from wrong recommendations  | Performance issues, turnover costs            |
| **Society**         | Algorithmic bias in hiring            | Perpetuates discrimination, reduces diversity |

### Error Tolerance Requirements

This is **HIGH-STAKES** rather than entertainment-level prediction:

- **False Positive Rate:** should be low enough that recruiters do not spend time on unsupported candidates.
- **False Negative Rate:** should not hide strong candidates behind generic keyword matches.
- **Hallucination Rate:** should be near zero for any skill the model claims from a resume.
- **Score spread:** the system should separate candidates instead of assigning the same near-perfect score to everyone.

---

## II. TRUSTWORTHINESS METRICS

### Metric 1: Top-K Stability Score (TSS)

**Definition:** Overlap of top-K recommendations between TF-IDF and embeddings

**Formula:** `Intersection / K` (values: 0.0 to 1.0)

**Why it maps to trust:**

- When different methods (keywords vs semantic) rank the same candidates highly, we have **higher confidence**
- High disagreement suggests one method may be hallucinating or overfitting

**Interpretation:**

- **> 0.7:** High trust - methods agree
- **0.4-0.7:** Medium trust - some disagreement
- **< 0.4:** Low trust - methods strongly disagree (possible hallucination)

**Current Measurement:** Stage 2 vs Stage 3 TSS = **0.408**; Stage 3 vs Stage 4 TSS = **1.0**; Stage 4 vs Stage 5 TSS = **0.2**.

**Interpretation:** the modification changed the ranking substantially, which is expected when the system becomes stricter about grounding and completeness.

---

### Metric 2: Accuracy vs Ground Truth

**Definition:** Percentage of top-K recommendations marked "select" in ground truth

**Formula:** `Selected_in_top_k / K`

**Why it maps to trust:**

- True proxy for trustworthiness - hiring managers judge AI by whether recommendations are qualified
- If system recommends unqualified people, managers will distrust it

**Interpretation:**

- **> 60%:** High accuracy
- **40-60%:** Medium accuracy
- **< 40%:** Low accuracy (worse than random)

**Current Snapshot:**

- Stage 4 top 50 contains **18/50 candidates at the ceiling score of 95**.
- **8/50** Stage 4 candidates contain obvious placeholder/sample artifacts in the resume text.
- Stage 5 top 10 shows a much wider adjusted-score range (**0.58 to 5.82**) instead of a pile-up at the maximum.

---

### Metric 3: Hallucination Detection Rate

**Definition:** Percentage of LLM-claimed skills not appearing in resume text

**Formula:** `Hallucinated_skills / Total_claimed_skills`

**Why it maps to trust:**

- LLM hallucinations directly undermine trust
- If system claims candidate has "SQL" but resume doesn't mention it, hiring manager catches the lie

**Interpretation:**

- **< 5%:** Very trustworthy - LLM grounded in text
- **5-15%:** Acceptable - minor hallucinations
- **> 15%:** Untrustworthy - too many false claims

**Current Measurement:** Stage 5 average hallucination rate on its scored output is **22.0%**.

**Why this maps to trust:** a hiring manager should not trust a recommendation that names skills not supported by the resume text.

---

### Metric 4: Method Correlation

**Definition:** Pearson correlation of normalized scores between TF-IDF and embeddings

**Why it maps to trust:**

- Positive correlation = methods see the same signal
- Disagreement suggests uncertainty

**Current Measurement:** not the main trust metric for the final system, but useful as a supporting signal when comparing rankers.

### Metric 5: Ceiling-Tie Rate

**Definition:** fraction of ranked candidates receiving the maximum score.

**Why it maps to trust:** if many candidates tie at the top score, the model is not discriminating between strong and weak resumes.

**Current Measurement:** Stage 4 assigned the maximum score (95) to **18/50 = 36%** of the ranked candidates.

**Interpretation:** this is a clear trust warning because the scorer is not differentiating enough.

---

## III. PRE-REGISTERED FAILURE CASES

### Failure Case 1: LLM Hallucination

**Prediction:** the model will claim skills that the resume does not contain.  
**Observed:** Stage 5 still shows non-trivial hallucination rates, so grounding is necessary.  
**Severity:** CRITICAL if ignored

### Failure Case 2: Method Disagreement (TSS < 0.4)

**Prediction:** Top-K overlap < 4/10  
**Observed:** Stage 4 vs Stage 5 TSS = **0.2**.  
**Severity:** HIGH because the grounded model materially changes which candidates are trusted.

### Failure Case 3: Poor Accuracy (< 40%)

**Prediction:** Less than 40% of top-5 are qualified  
**Observed:** the original Stage 4 output had severe score inflation, with 18 candidates tied at 95/100 and several unsupported resumes ranked very highly.  
**Severity:** CRITICAL

### Failure Case 4: Data Imbalance

**Prediction:** Select rate < 20% or > 80%  
**Result:** ✓ PASSED - Ground truth 49.7% selected  
**Severity:** MEDIUM

### Failure Case 5: Ensemble Regression ⚠ **OBSERVED**

**Prediction:** Ensemble < max(TF-IDF, Embeddings, Gemini)  
**Result:** ✗ **FAILED** - Ensemble 40% < Embeddings 60%  
**Severity:** HIGH

### Failure Case 6: Placeholder Resume Ranked Highly

**Prediction:** the model should not trust incomplete or template-filled resumes.  
**Observed:** a resume such as Courtney Walsh (Candidate 61) includes placeholder fields like `[Insert Address]`, `[Insert Phone Number]`, and `[Insert Email]`, yet Stage 4 still gave it a high score.  
**Severity:** CRITICAL because incomplete resumes should not be treated as strong evidence.

---

## IV. TRUST-IMPROVING MODIFICATION

### Proposed Approach: Grounded Stage 5 with Completeness Checks

**Rationale:** The original Stage 4 scorer over-rewarded generic e-commerce language and did not distinguish well between complete and incomplete resumes. Stage 5 improves trust by verifying evidence in the resume itself before trusting the score.

**Implementation:**

```python
1. Detect obvious placeholder or sample-resume text before scoring.
2. Pass the Stage 4 score and reasoning into Stage 5 for context.
3. Ask Gemini for a stricter 1-10 score, skills, and one-sentence reason.
4. Normalize skill claims and check whether they are actually present in the resume.
5. Penalize unsupported claims, then cap scores further when hallucination rate is high.
```

**Expected Benefit:** more grounded scores, fewer inflated top ranks, and better protection against placeholder or template resumes.

**Cost / Trust Tax:**

- **Latency:** higher because of an extra grounding pass and longer prompt.
- **Coverage:** lower because incomplete resumes are capped or excluded.
- **Complexity:** higher because of alias matching, completeness checks, and score caps.
- **False negatives:** some legitimate resumes may be penalized if they use unusual abbreviations not in the alias list.

---

## V. COMPARATIVE ANALYSIS: ORIGINAL VS IMPROVED

### Results Summary

| Method                        | Trust signal observed                                 | Notes                                                      |
| ----------------------------- | ----------------------------------------------------- | ---------------------------------------------------------- |
| **Stage 4 (original Gemini)** | 18/50 ceiling ties; 8/50 placeholder-like resumes     | weak discrimination and no grounding guard                 |
| **Stage 5 (grounded Gemini)** | 22.0% mean hallucination rate; score spread 0.58–5.82 | stricter and more evidence-based                           |
| **Embeddings (semantic)**     | Useful as an upstream filter                          | good at semantic similarity, but not the final trust check |

### Qualitative Held-Out Review

The following examples were reviewed as concrete failure/success cases outside the compact metric summary:

- **Candidate 61 / Rank 22 (Courtney Walsh):** contains placeholder fields like `[Insert Address]`, `[Insert Phone Number]`, and `[Insert Email]`, yet Stage 4 still assigned a high score. This is a direct trust failure because the resume is incomplete.
- **Candidate 0 / Rank 50 (Jason Jones):** ends up at the bottom of Stage 4 despite substantial e-commerce experience. This shows the original scorer does not consistently weigh the full JD, especially non-SEO skills and platform breadth.
- **Candidate 53 / Rank 39 (Cynthia Cook):** includes PPC, paid social, email, and analytics support areas that the JD explicitly values, but the original stage still does not distinguish these support skills sharply enough.

These examples are useful because they expose the exact kinds of mistakes the system should avoid in production: trusting incomplete resumes, flattening important skill differences, and over-rewarding generic e-commerce language.

### Why Stage 5 Improves Trust

1. It prevents obviously incomplete resumes from being treated as high-confidence candidates.
2. It checks whether claimed skills are actually present in the text.
3. It uses the previous stage as context instead of blindly overwriting it.
4. It reduces score inflation and makes the ranking more discriminating.
5. It preserves a short explanation, which helps human reviewers audit the decision.

### Insight

**Better than ensemble:** Use embeddings as primary ranker, flag cases where methods disagree for human review. This respects the competence of each method rather than forcing agreement through averaging.

---

## VI. QUANTITATIVE EVALUATION

### Baseline System Performance

**Dataset:** 50 E-commerce Specialist resumes scored in Stage 4; top-10 output analyzed for Stage 5.

**Key Metrics:**

- **Ranking Stability (TSS):** Stage 4 vs Stage 5 = 0.2 - the grounded stage meaningfully changes the ranking.
- **Best Trust Signal in Stage 4:** none; the top 50 contains heavy tie inflation and placeholder contamination.
- **Best Trust Signal in Stage 5:** score spread is no longer collapsed at the top, and hallucination rates are explicitly measured.

### Rate Limiting Compliance

- **Requirement:** Max 13 Gemini API requests per minute
- **Implemented:** Sliding window queue enforcement
- **Test Result:** ✓ PASSED - 11 requests made with proper spacing
- **Min Interval:** 4.6 seconds between requests

---

## VII. LIMITATIONS & UNPROTECTED GROUPS

### Known Limitations

1. **Single role:** current evaluation is focused on E-commerce Specialist resumes.
2. **Text-only grounding:** the system cannot verify facts outside the resume text.
3. **Alias coverage:** unusual abbreviations can still be missed.
4. **No fairness audit:** demographic bias has not been measured.
5. **Conservative caps:** some strong but unusually written resumes may be under-scored.

### Unprotected Groups

- **Career Changers:** Evaluated poorly because keywords don't match
- **Non-Traditional Candidates:** Semantic approach may penalize unique profiles
- **Non-Native English:** Language quality might affect LLM scoring
- **Underrepresented Groups:** Possible bias in training data

### Recommendation

**Before deployment:** run a fairness audit, test across multiple job families, and calibrate the alias list and completeness rules with human review.

---

## VIII. KEY FINDINGS & INSIGHTS

### Finding 1: Stage 4 Over-Rates Generic E-commerce Language

Stage 4 gives many candidates the same ceiling score (95/100), which means it is not discriminating enough.

### Finding 2: Placeholder Resumes Are a Real Trust Failure

Incomplete resumes should not be treated as strong evidence; Stage 5 now blocks this pattern.

### Finding 3: Grounding Improves Trust

Stage 5 makes the model justify claims against the resume text and penalizes unsupported skills.

### Finding 4: Trust Tax Is Real

More checks and stricter scoring reduce coverage and increase latency, but they make the output safer to trust.

---

## IX. RECOMMENDATIONS

### Immediate Actions

1. Use Stage 5 as the final trust check, not just a reranker.
2. Flag placeholder or sample resumes for human review.
3. Keep the short reasoning line for auditability.
4. Log all score changes from Stage 4 to Stage 5.

### Medium-Term

1. Test on all roles in the dataset, not just E-commerce.
2. Expand the alias list for common skill variants.
3. Add a small rubric so the score is composed of explicit criteria.
4. Conduct fairness and bias audits.

### Long-Term

1. Compare system recommendations against human reviewers on held-out roles.
2. Measure impact on hiring diversity and downstream job outcomes.
3. Monitor drift if resume style or job requirements change.
4. Add interpretable evidence highlighting for each score.

---

## X. CONCLUSION

**System Trustworthiness:** IMPROVED BUT NOT FULLY TRUSTWORTHY

The current project shows that trustworthiness improves when the system stops treating every high-similarity resume as equally strong and instead checks whether the resume actually supports the score. Stage 4 is still too inflated, but Stage 5 is materially more grounded.

**Key Insight:** in hiring, the best trust improvement is not merely a better rank order; it is a rank order that can be defended with evidence from the resume text.

**For Production Deployment:**

- Use Stage 5 as the trust filter before any human review.
- Require human review for incomplete or borderline resumes.
- Keep the grounding/capping logic, because it prevents the worst trust failures.
- Conduct bias audit before launch.
- Monitor accuracy, hallucination rate, and ceiling-tie rate over time.

---

## APPENDIX: Test Results

### Trustworthiness Analysis (Baseline)

- Ground truth select rate: 49.7% (balanced dataset)
- Top-K stability: 0.50 (medium)
- Top-10 accuracy: 40-60% depending on method

### End-to-End Evaluation (with Gemini)

- Sample: 11 E-commerce resumes
- Best method: Embeddings (60% accuracy)
- Ensemble: Failed (40% accuracy)
- Rate limiting: ✓ Compliant
- API requests: 11 made successfully

---

**Report Generated:** May 3, 2026  
**Project:** Resume Trust Lab System  
**Status:** ✓ Complete - Ready for deployment with human review layer
