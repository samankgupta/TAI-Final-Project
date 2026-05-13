# Stage 4 Systemic Issues — Cross-Job Analysis

**Document Purpose:** Identify patterns and root causes that affect both job roles  
**Scope:** All 100 candidates (50 per role)  
**Focus:** Pipeline-level improvements, not role-specific fixes

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Issue 1: Score Clustering / Insufficient Granularity](#issue-1-score-clustering--insufficient-granularity)
3. [Issue 2: AI Template Boilerplate — Inconsistent Penalty](#issue-2-ai-template-boilerplate--inconsistent-penalty)
4. [Issue 3: Incomplete Resumes Entering the Ranking](#issue-3-incomplete-resumes-entering-the-ranking)
5. [Issue 4: Duplicate Candidate Entries](#issue-4-duplicate-candidate-entries)
6. [Issue 5: Underqualified Candidates Reaching Stage 4](#issue-5-underqualified-candidates-reaching-stage-4)
7. [Issue 6: Data Quality Deterioration Upstream](#issue-6-data-quality-deterioration-upstream)
8. [Root Cause Analysis](#root-cause-analysis)
9. [Impact Assessment](#impact-assessment)

---

## Executive Summary

Across both job roles, the Stage 4 scoring engine exhibits **6 major systemic problems** that indicate failures at earlier pipeline stages AND insufficient validation in Stage 4 itself.

### By the Numbers

| Issue                                             | E-commerce    | Software Engineer | Total   | % of Pool        |
| ------------------------------------------------- | ------------- | ----------------- | ------- | ---------------- |
| Score clustering (largest tied band)              | 18 @ 95 (36%) | 24 @ 85 (48%)     | 42      | 42%              |
| AI template boilerplate                           | 12            | 13                | 25      | 25%              |
| Critical disqualification errors                  | 1             | 3                 | **4**   | 4%               |
| Duplicate identities                              | 0             | 1                 | 1       | 1%               |
| Underqualified (entry-level in professional role) | 0             | 1                 | 1       | 1%               |
| **Total problem candidates**                      | **~16**       | **~19**           | **~35** | **~35% of pool** |

### Severity Assessment

- **Critical (blocking use of ranking):** 4 disqualification errors + duplicates
- **High (damages ranking reliability):** Score clustering + underscored/overscored candidates
- **Medium (reduces data quality):** AI boilerplate, identity verification issues

---

## Issue 1: Score Clustering / Insufficient Granularity

### The Problem

Nearly **half of each candidate pool shares a single score** despite meaningfully different skill profiles.

#### E-commerce Specialist

- **18 candidates at 95** (36% of pool)
- These 18 have skill coverage ranging from 2 core skills to 6+ core skills
- Example: John Crawford (95, missing Shopify/PPC/Email/Excel) tied with Lisa Aguirre (95, has all 6 core skills)

#### Software Engineer

- **24 candidates at 85** (48% of pool)
- These 24 range from candidates with 1–2 core skills to candidates with 7–8 core skills
- Example: Ananya with incomplete dates & no experience (85) tied with Christopher Spencer (85, AWS certified, open-source lead)

### Why This Happens

1. **Gemini scores on 1–10 scale** → mapped to 1–100 by ×10
   - 1.0 → 10, 1.5 → 15, 2.0 → 20, etc.
   - This creates natural banding every 10 points (10, 20, 30, … 90, 100)

2. **No skill-by-skill point breakdown**
   - All skills weighted equally
   - Resume with Shopify only (1 skill) scored same as resume with Shopify + GA + Excel + PPC (4 skills)

3. **Coarse grading rubric**
   - Prompt asks for single 1–10 score
   - No intermediate scoring for partial credit (e.g., "5 out of 7 required skills = 7 points")

### Impact on Hiring

| Scenario                                 | Current                                               | Ideal                                                              |
| ---------------------------------------- | ----------------------------------------------------- | ------------------------------------------------------------------ |
| Need to select top 10 from 50 candidates | 24 tied @ 85 makes selection arbitrary                | Wider spread (e.g., 70–90) enables differentiation                 |
| Need to fill 1 role                      | Must make tiebreaker choice among 18 identical scores | Could use scores 95, 94, 93 to pick 3 qualified > arbitrary choice |
| Manual review cost                       | High (need to examine all 18 tied candidates)         | Low (perhaps examine top 10 only)                                  |

### Comparison: Well-Calibrated Scorer

A well-calibrated scorer for 50 candidates should produce:

| Score     | Ideal Count | Current E-commerce | Current SE |
| --------- | ----------- | ------------------ | ---------- |
| 95–100    | 2–3         | 18                 | 0          |
| 90–94     | 4–5         | 8                  | 8          |
| 85–89     | 6–8         | 0                  | 24         |
| 80–84     | 8–10        | 0                  | 0          |
| 75–79     | 8–10        | 0                  | 7          |
| 70–74     | 8–10        | 0                  | 0          |
| <70       | 10–15       | 24                 | 11         |
| **Range** | **Full**    | **75–95**          | **35–90**  |

---

## Issue 2: AI Template Boilerplate — Inconsistent Penalty

### The Problem

**25 out of 100 resumes (25% of pool)** contain obvious AI-generated text. The same phrases appear across the **entire score range (35–95)** with **no systematic penalty**.

### Examples of Boilerplate

#### Phrase A: "Remember to tailor your resume"

Appears in:

- E-commerce: Candidate 69 (95pts), Candidate 19 (95pts), Candidate 41 (95pts), Candidate 4 (90pts)
- Software Engineer: Candidate 26 (90pts), Candidate 33 (85pts)
- **Score range affected:** 85–95

#### Phrase B: "Let me know if you have any questions"

Appears in:

- E-commerce: Candidates at ranks 1, 8, 16, 33, 40, 42 (scores: 95, 95, 95, 90, 85, 85)
- Software Engineer: Candidates at ranks 12, 49 (scores: 85, 40)
- **Score range affected:** 40–95 (entire range)
- **Problem:** Steve King at 40pts has this phrase; Erin Stout at 90pts has same phrase

#### Phrase C: "Here's a sample professional resume for [Name]"

Appears in:

- E-commerce: Candidate 48 (90pts) — explicitly marks resume as "sample"
- Software Engineer: Candidates 5, 12, 34, 42 (scores: 90, 65, 65, 65)
- **Pattern:** Opening-line framing, not closing line

### Impact

If AI boilerplate is a **quality issue** that should reduce scores:

- Steve King (40pts) and Erin Stout (90pts) should differ more than 50 points, but both have identical boilerplate
- Either (a) boilerplate doesn't matter (should be scored equally), or (b) it matters hugely (and Steve King should be ~70)

The **inconsistency** is the core problem. A scoring engine that doesn't consistently penalize a data quality issue is unreliable.

### Root Cause

The Gemini scoring prompt **does not mention AI boilerplate** as a penalty criteria. The engine may recognize phrases like "sample resume" but has no instruction to penalize them.

---

## Issue 3: Incomplete Resumes Entering the Ranking

### The Problem

**4 resumes are fundamentally incomplete** yet reach Stage 4 and receive scores.

### E-commerce Specialist

#### Candidate 61: Courtney Walsh | Rank 22 | 92pts

**Completely unfilled template:**

```
Address: [Insert Address]
Phone: [Insert Phone Number]
Email: [Insert Email]
LinkedIn: [Insert LinkedIn Profile URL]
```

**Issue:** This is a blank template, not a real resume. Scoring it at 92 and ranking it 22nd is unjustifiable.

### Software Engineer

#### Candidate 87: Sonia | Rank 31 | 85pts

**Resume ends with embedded rejection letter:**

> "After careful consideration, we regret to inform you that we will not be moving forward with your application for the Software Engineer position at this time."

**Issue:** This is not a resume; it's an AI output combining resume + rejection response.

#### Candidate 90: Ananya | Rank 14 | 85pts

**Placeholder dates throughout:**

```
Employment:
Company A: [20XX–20XX]
Company B: [20XX–20XX]
```

**Email malformed:** `\ananya@email.com` (contains backslash escape character)

**Issue:** Resume never completed; contains broken email; only projects/internships, no professional experience.

#### Candidate 95: Diya | Rank 50 | 35pts

**Status:** Current undergraduate (2020–2024 graduation)  
**Experience:** Internship + volunteer only  
**GPA:** 2.8 (below professional standard)

**Issue:** This is a student, not a professional. Should be filtered at Stage 1, not scored at Stage 4.

### Pre-Stage-4 Validation (Currently Missing)

| Check                        | Purpose                                  | Catches            |
| ---------------------------- | ---------------------------------------- | ------------------ |
| Unfilled fields pattern      | Reject `[Insert X]` placeholders         | Courtney Walsh     |
| Placeholder dates            | Reject `20XX` or incomplete date ranges  | Ananya (90)        |
| Email format validation      | Reject malformed addresses               | Ananya (90)        |
| Non-resume content detection | Reject embedded letters, meta-commentary | Sonia, Ananya (88) |
| Experience threshold         | Reject if <1 year or student status      | Diya               |

**Current status:** ✗ None implemented

---

## Issue 4: Duplicate Candidate Entries

### The Problem

**Software Engineer dataset contains duplicate identity:**

| Field                | Candidate 92         | Candidate 93         |
| -------------------- | -------------------- | -------------------- |
| Name                 | Amara                | Amara                |
| Email                | amara@email.com      | amara@email.com      |
| Both Ranked & Scored | Yes (Rank 23, 85pts) | Yes (Rank 28, 85pts) |

### Why This Matters

Only one person should appear in a ranking. Scoring both entries:

1. **Inflates their representation** — they occupy 2 of 50 candidate slots
2. **Reduces diversity** — a real second candidate loses a slot to a duplicate
3. **Creates hiring confusion** — which "Amara" do you hire? They're identical (same email)

### Root Cause

**No deduplication step before Stage 4.**

Earlier pipeline stages (1–3) should have detected this at candidate load time (Stage 1) or before Stage 4.

### How to Detect

Simple email deduplication:

```python
email_seen = set()
for candidate in candidates:
    if candidate.email in email_seen:
        flag_as_duplicate(candidate)
    email_seen.add(candidate.email)
```

---

## Issue 5: Underqualified Candidates Reaching Stage 4

### The Problem

**Diya (Software Engineer, Rank 50, 35pts)** is a current undergraduate student with only internship experience.

A professional software engineering role should not include students in the ranking.

### Details

| Criterion           | Requirement             | Diya               | Status |
| ------------------- | ----------------------- | ------------------ | ------ |
| Years of experience | 5+ (preferred)          | 0 (student)        | ✗      |
| Professional roles  | Required                | Internship only    | ✗      |
| GPA                 | Typically 3.0+          | 2.8                | ✗      |
| Education           | In progress or complete | In progress (2024) | ⚠      |

### Why She Reached Stage 4

1. **No experience filter at Stage 1** — role filtering accepts all resumes matching "Software Engineer" label regardless of experience
2. **No stage-specific minimum at Stages 2–3** — TF-IDF and embedding rankers don't filter by experience; they rank by relevance
3. **No pre-Stage-4 validation** — no minimum experience gate before Gemini scoring

### Impact

A current student occupies one of the top 50 candidates for a professional role. If hired, she would need onboarding that other 5-year engineers don't. This indicates a **filtering failure upstream** of Stage 4.

---

## Issue 6: Data Quality Deterioration Upstream

### Identity Verification Issues

**12 candidates (24% of Software Engineer pool) use only single names:**

Rajiv, Oliver, Lucas, Amara (×2), Ananya, Meera, Sonia, Kunal, Aarav, Diya

| Issue                      | Count        | Problem                                                 |
| -------------------------- | ------------ | ------------------------------------------------------- |
| Single-name entries        | 12           | Cannot legally hire; identity unverifiable              |
| Duplicate email addresses  | 1 (Amara ×2) | Same person submitted twice (or AI generation artifact) |
| **Total identity flagged** | ~13          | ~26% of Software Engineer pool                          |

### E-commerce Specialist Pool

No single-name entries detected, suggesting data quality may be better for this role or sourced differently.

### Implication

The Software Engineer dataset appears to have **been ingested from a less rigorous source** or **AI-generated bulk**, with poor identity verification.

---

## Root Cause Analysis

### Why Do These Issues Exist?

#### Root Cause 1: Insufficient Pipeline Validation

| Stage       | Should Filter                  | Currently Filters     |
| ----------- | ------------------------------ | --------------------- |
| Stage 1     | Role + experience + identity   | Role only             |
| Pre-Stage-4 | Data completeness + duplicates | Nothing               |
| Stage 4     | Scoring quality                | Passes through all    |
| Stage 5     | Trust validation               | Grounding checks only |

**Gap:** No pre-Stage-4 validation layer.

#### Root Cause 2: Gemini Prompt Lacks Detail

Current prompt asks for: `score 1-10 + skills list + reasoning`

**Missing from prompt:**

- Point-by-point rubric (e.g., "5 pts for Shopify, 3 pts for GA, 2 pts for PPC")
- Explicit penalty rules ("−10 if AI boilerplate detected")
- Required vs. optional skill distinction
- Tie-breaking criteria ("If score would be same, prefer candidate with DevOps")

#### Root Cause 3: Output Granularity Mismatch

- Gemini returns: 1–10 scale (10 possible values)
- Mapped to: 1–100 scale (100 possible values)
- Result: Clustering at 10-point intervals natural

**Fix needed:** Ask Gemini for finer-grained output (e.g., 1–100 directly, or structured breakdown).

---

## Impact Assessment

### Hiring Risk

If the top 50 from this ranking are forwarded for manual review:

| Risk                                      | Impact                                              | Mitigation                         |
| ----------------------------------------- | --------------------------------------------------- | ---------------------------------- |
| Select from 18 tied candidates @ 95       | Pick wrong one by luck, not merit                   | Wider score spread required        |
| Invite Courtney Walsh (unfilled template) | No contact info to reach her                        | Pre-validation filters             |
| Interview Diya (student)                  | Not immediately job-ready; requires ramp-up         | Experience filtering at Stage 1    |
| Confusion with duplicate Amara            | Unclear who to hire if both pass                    | Email deduplication before Stage 4 |
| Hire Victor Johnson @ 45pts               | Miss candidate with master's degree who scores well | Manual audit of bottom 10 scores   |

### Financial Impact

- **Tier 1:** Critical issues (missing Victor, hiring Diya) could result in poor hiring outcomes
- **Tier 2:** AI boilerplate inconsistency adds noise; increases manual review cost
- **Tier 3:** Score clustering forces binary tiebreaker decisions instead of merit-based ranking

---

## Severity Matrix

| Issue                         | Frequency      | Severity | Actionability | Fix Cost |
| ----------------------------- | -------------- | -------- | ------------- | -------- |
| **Score clustering**          | 42% of pool    | High     | Yes           | Medium   |
| **AI boilerplate penalty**    | 25% of pool    | Medium   | Yes           | Low      |
| **Incomplete resumes**        | 4% of pool     | Critical | Yes           | Low      |
| **Duplicate identities**      | 1% of pool     | Critical | Yes           | Low      |
| **Underqualified candidates** | 1% of pool     | High     | Yes           | Low      |
| **Data quality upstream**     | 26% of SE pool | Medium   | Partially     | High     |

---

## Recommended Action Plan (See STAGE_4_RECOMMENDATIONS.md for Details)

### Immediate (Before Using Ranking)

- [ ] Disqualify 4 incomplete resumes
- [ ] Verify/remove duplicate Amara entries
- [ ] Manually review Victor Johnson and Steve King scores

### Short-Term (Before Next Scoring Run)

- [ ] Add pre-Stage-4 validation layer
- [ ] Implement email deduplication
- [ ] Apply consistent AI boilerplate penalty
- [ ] Filter by experience threshold at Stage 1

### Long-Term (Architecture)

- [ ] Redesign Gemini prompt with skill-by-skill rubric
- [ ] Change output to finer-grained scale (1–100 directly)
- [ ] Implement structured scoring (JSON output from Gemini)
- [ ] Add feedback loop: compare scores to ground truth hiring decisions

---

_For specific candidate details, see [STAGE_4_JOB1_ECOMMERCE_AUDIT.md](STAGE_4_JOB1_ECOMMERCE_AUDIT.md) and [STAGE_4_JOB2_SOFTWARE_ENGINEER_AUDIT.md](STAGE_4_JOB2_SOFTWARE_ENGINEER_AUDIT.md)_  
_For actionable recommendations, see [STAGE_4_RECOMMENDATIONS.md](STAGE_4_RECOMMENDATIONS.md)_
