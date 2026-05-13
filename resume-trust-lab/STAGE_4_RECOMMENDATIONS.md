# Stage 4 Recommendations — Action Plan

**Document Purpose:** Provide actionable recommendations to fix identified issues  
**Audience:** Engineering team, product managers, hiring stakeholders  
**Priority:** Organized by urgency (Immediate → Short-Term → Long-Term)

---

## Table of Contents

1. [Immediate Actions (Before Using Rankings)](#immediate-actions-before-using-rankings)
2. [Short-Term Improvements (Before Next Run)](#short-term-improvements-before-next-run)
3. [Long-Term Strategy (Architecture Changes)](#long-term-strategy-architecture-changes)
4. [Implementation Checklist](#implementation-checklist)
5. [Success Metrics](#success-metrics)

---

## Immediate Actions (Before Using Rankings)

**Timeline:** Today (complete within 24 hours)  
**Severity:** Blocking use of current rankings  
**Cost:** Minimal (manual review + configuration)

### Action 1: Disqualify Incomplete Resumes (4 candidates)

#### E-commerce Specialist

**Candidate 61: Courtney Walsh | Rank 22 | 92pts**

- **Issue:** Completely unfilled contact fields (`[Insert Email]`, `[Insert Phone]`, etc.)
- **Action:** Remove from ranking immediately
- **Justification:** Not a real resume; cannot contact candidate
- **Impact:** 92pt candidate eliminated; affects ranking below
- **Effort:** 5 minutes (delete from outputs, regenerate ranking)

**Code to identify and remove:**

```python
import json

def filter_incomplete_resumes(stage_4_json_path):
    """Remove resumes with unfilled placeholder fields."""
    with open(stage_4_json_path) as f:
        data = json.load(f)

    incomplete_patterns = [
        r'\[insert [^\]]+\]',
        r'20XX',
        r'\\[a-z@\.]+'  # malformed email with backslash
    ]

    filtered = []
    for candidate in data['candidates']:
        resume = candidate.get('resume', '').lower()
        if not any(re.search(pat, resume) for pat in incomplete_patterns):
            filtered.append(candidate)

    data['candidates'] = filtered
    # Re-rank
    for i, cand in enumerate(filtered):
        cand['rank'] = i + 1

    with open(stage_4_json_path, 'w') as f:
        json.dump(data, f, indent=2)
```

#### Software Engineer

**Candidate 87: Sonia | Rank 31 | 85pts**

- **Issue:** Resume body contains embedded AI rejection letter
- **Action:** Remove from ranking
- **Impact:** Eliminates 85pt candidate

**Candidate 90: Ananya | Rank 14 | 85pts**

- **Issue:** Unfilled placeholder dates (`20XX–20XX`), malformed email (`\ananya@email.com`)
- **Action:** Remove from ranking
- **Impact:** Eliminates 85pt candidate

**Candidate 95: Diya | Rank 50 | 35pts**

- **Issue:** Current undergraduate with internship only; no professional experience
- **Action:** Option A (recommended): Remove; Option B: Flag for "early-career track" separate from professional ranking
- **Impact:** Eliminates lowest-scoring candidate; reduces data quality issues

---

### Action 2: Handle Duplicate Candidate Entry

**Software Engineer: Candidates 92 & 93 (Both "Amara" at amara@email.com)**

#### Investigation

```python
# Identify exact duplicates
df_stage_4 = pd.read_json('outputs/stage_4.json')
duplicates = df_stage_4[df_stage_4.duplicated(subset=['email'], keep=False)]
# Result: Candidates 92 & 93 both have amara@email.com
```

#### Resolution

**Recommended:** Remove Candidate 93 (Rank 28) — keep the first submitted entry (Candidate 92, Rank 23)

**Alternative:** Contact applicant to clarify and resubmit with verified contact details.

**Action:**

```python
# Remove from outputs
data['candidates'] = [c for c in data['candidates'] if c['candidate_id'] != 93]
# Re-rank
for i, cand in enumerate(data['candidates']):
    cand['rank'] = i + 1
```

**Impact:** Removes 1 candidate; shifts Rank 29–50 up by one

---

### Action 3: Manually Review Bottom Outliers (2–3 candidates)

**Software Engineer: Victor Johnson (Rank 48, 45pts) and Steve King (Rank 49, 40pts)**

#### Why

Both have **strong technical profiles** (Master's degree, DevOps expertise, 5+ years) but score among the **lowest in the pool**. This suggests:

- Resume formatting issue causing parsing failure
- Gemini API error / transient hallucination
- Keyword mismatch in prompt

#### Manual Review Process

1. **Read full resume** for both candidates
2. **Score manually** against job description rubric
3. **Compare Gemini score** to manual score
4. **If significant gap (>20 points),** suspect parsing error
5. **Adjust score** if justified, OR flag as "manually reviewed"

#### Expected Outcome

- Victor Johnson: likely 75–85 (not 45)
- Steve King: likely 75–85 (not 40)

#### Implementation

```python
# Flag for manual review
flagged = [
    {'id': 53, 'name': 'Victor Johnson', 'score': 45, 'reason': 'Master\'s degree + DevOps but low score'},
    {'id': 21, 'name': 'Steve King', 'score': 40, 'reason': '5+ years experience but score near bottom'}
]

# Create review sheet
import pandas as pd
review_df = pd.DataFrame(flagged)
review_df.to_csv('manual_review_candidates.csv', index=False)
```

---

### Action 4: Generate Corrected Rankings

After Actions 1–3, regenerate outputs:

```bash
cd resume-trust-lab

# Remove disqualified candidates
python -c "
import json
# Load, filter, re-rank
# Save to outputs/stage_4_corrected.json
"

# Generate corrected CSV
python src/tools/match_stage4_to_stage1.py stage_4_corrected
```

**Output files:**

- `outputs/stage_4_corrected.json` (48–49 candidates instead of 50)
- `outputs/stage_4_corrected.csv` (with full resumes)

---

## Short-Term Improvements (Before Next Run)

**Timeline:** 1–2 weeks  
**Severity:** High (prevents recurrence)  
**Cost:** Low to Medium (engineering effort)  
**ROI:** High (fixes 25% of problems)

### Improvement 1: Add Pre-Stage-4 Validation Layer

Create a new validation script to run before Stage 4 scoring.

#### Validation Checks

```python
class PreStage4Validator:
    """Validate resumes before Gemini scoring."""

    def validate_candidate(self, resume_text, email, name):
        """Run all checks; return list of issues."""
        issues = []

        # Check 1: Unfilled fields
        if re.search(r'\[insert [^\]]+\]', resume_text.lower()):
            issues.append('unfilled_fields')

        # Check 2: Placeholder dates
        if re.search(r'20XX|XX–XX', resume_text):
            issues.append('placeholder_dates')

        # Check 3: Email format
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            issues.append('malformed_email')

        # Check 4: Non-resume content
        if 'we regret to inform you' in resume_text.lower():
            issues.append('rejection_letter_in_resume')

        if 'sample resume' in resume_text.lower():
            issues.append('sample_framing')

        # Check 5: Single name
        if len(name.split()) < 2:
            issues.append('single_name_identity')

        # Check 6: Experience threshold
        if self._extract_years_experience(resume_text) < 1:
            issues.append('no_professional_experience')

        return issues

    def _extract_years_experience(self, resume_text):
        """Heuristic: count years of continuous employment."""
        # Simplified; real implementation would parse dates
        return len(re.findall(r'20\d{2}', resume_text)) // 2
```

#### Usage

```python
validator = PreStage4Validator()

for candidate in candidates_from_stage_3:
    issues = validator.validate_candidate(
        candidate['resume'],
        candidate['email'],
        candidate['name']
    )

    if 'unfilled_fields' in issues:
        candidate['status'] = 'DISQUALIFY'
        candidate['reason'] = 'Incomplete template'

    elif 'rejection_letter_in_resume' in issues:
        candidate['status'] = 'DISQUALIFY'
        candidate['reason'] = 'Non-resume content detected'

    elif 'no_professional_experience' in issues and role_requires_professional:
        candidate['status'] = 'REJECT'
        candidate['reason'] = 'Insufficient experience'

    else:
        candidate['status'] = 'PASS'
        candidate['reason'] = 'Proceed to Stage 4'

# Score only PASS candidates in Stage 4
passing_candidates = [c for c in candidates if c['status'] == 'PASS']
stage_4_results = gemini_ranker.run(passing_candidates)
```

#### Success Metric

- Catch 100% of unfilled templates before scoring
- Eliminate 4+ problematic resumes before Stage 4
- Reduce downstream "invalid resume" flags in Stage 5

---

### Improvement 2: Email Deduplication Before Stage 4

Add deduplication to Stage 3 output or before Stage 4 input.

#### Implementation

```python
def deduplicate_by_email(candidates):
    """Keep first occurrence; flag duplicates for review."""
    seen = {}
    deduplicated = []
    duplicates = []

    for candidate in candidates:
        email = candidate.get('email', '').lower()
        if email in seen:
            duplicates.append({
                'email': email,
                'candidate_ids': [seen[email]['id'], candidate['id']],
                'names': [seen[email]['name'], candidate['name']]
            })
        else:
            seen[email] = {'id': candidate['id'], 'name': candidate['name']}
            deduplicated.append(candidate)

    # Log duplicates
    if duplicates:
        print(f"Duplicates detected: {duplicates}")
        # Save for manual review or flag to user

    return deduplicated
```

#### Integration

```python
# In Stage 3 output handling
stage_3_candidates = experiment_runner.ranked_dfs['stage_3']
stage_3_candidates_dedup = deduplicate_by_email(stage_3_candidates.to_dict('records'))

# Pass deduplicated list to Stage 4
stage_4_input = pd.DataFrame(stage_3_candidates_dedup)
```

---

### Improvement 3: Consistent AI Boilerplate Penalty

Apply standardized scoring deduction for detected AI templates.

#### Detection Patterns

```python
BOILERPLATE_PATTERNS = {
    'closing_template': [
        r"let me know if you have any questions",
        r"remember to tailor your resume",
        r"feel free to reach out",
        r"don't hesitate to contact",
    ],
    'opening_template': [
        r"here'?s a sample professional resume",
        r"this is a sample resume",
        r"example resume",
    ],
    'ai_meta_commentary': [
        r"note that i'?ve included some data",
        r"this is just an example",
        r"feel free to modify",
    ]
}
```

#### Penalty Application

```python
def apply_boilerplate_penalty(resume_text, gemini_score):
    """Deduct 10 points if AI boilerplate detected."""
    for pattern_group, patterns in BOILERPLATE_PATTERNS.items():
        if any(re.search(pat, resume_text.lower()) for pat in patterns):
            # Apply consistent penalty
            adjusted_score = max(1, gemini_score - 10)
            print(f"Boilerplate detected ({pattern_group}): {gemini_score} → {adjusted_score}")
            return adjusted_score

    return gemini_score
```

#### Integration into Stage 4

```python
def score_resume(self, resume, jd):
    """Score resume, apply boilerplate penalty."""
    raw_score = self._call_gemini(resume, jd)
    adjusted_score = apply_boilerplate_penalty(resume, raw_score)
    return adjusted_score
```

#### Success Metric

- All resumes with boilerplate receive −10 point deduction
- Score consistency improved; range widens

---

### Improvement 4: Experience Threshold Filtering at Stage 1

Implement minimum experience requirement at role filtering stage.

#### Configuration

```python
# src/config.py

EXPERIENCE_REQUIREMENTS = {
    'e-commerce specialist': 3,  # 3+ years required
    'software engineer': 5,      # 5+ years preferred
}

# Threshold: resumes with < X years experience filtered
FILTER_BY_MIN_EXPERIENCE = True
```

#### Implementation

```python
def filter_by_experience(candidates_df, role, min_years):
    """Remove candidates with insufficient experience."""
    def extract_years(resume_text):
        # Parse employment dates; sum continuous years
        dates = re.findall(r'(\d{4})', resume_text)
        if len(dates) < 2:
            return 0
        return int(dates[-1]) - int(dates[0])

    candidates_df['years_experience'] = candidates_df['resume'].apply(extract_years)
    filtered = candidates_df[candidates_df['years_experience'] >= min_years]

    if len(filtered) < len(candidates_df):
        print(f"Filtered {len(candidates_df) - len(filtered)} candidates with <{min_years} years")

    return filtered
```

#### Success Metric

- Diya (student) filtered out before Stage 4
- Only professional candidates reach scoring stage
- Dataset credibility improved

---

## Long-Term Strategy (Architecture Changes)

**Timeline:** 1–2 months  
**Severity:** Medium (improves reliability)  
**Cost:** Medium to High (significant engineering)  
**ROI:** Very High (fixes 70%+ of systemic issues)

### Strategy 1: Redesign Gemini Scoring Prompt

Replace single-score prompt with **skill-by-skill rubric**.

#### Current Prompt (Insufficient)

```
Score this resume for fit with the job description: 1-10
(1 = not qualified, 10 = excellent fit)

Job Description: [JD]
Resume: [Resume]
```

#### Improved Prompt (Skill-Based)

```
Evaluate this resume against the job description using the rubric below:

Job Description:
[JD]

Resume:
[Resume]

SCORING RUBRIC (Sum to get total):

1. Relevant Language/Framework (Java/Python/etc.)
   - 0 points: Not mentioned
   - 5 points: Mentioned but not emphasized
   - 10 points: Strong, primary focus

2. Algorithms & Data Structures
   - 0 points: Not mentioned
   - 5 points: Mentioned
   - 10 points: Strong, with examples

[... continue for DevOps, Testing, APIs, System Design ...]

7. Years of Experience
   - 0 points: <1 year
   - 3 points: 1-3 years
   - 5 points: 3-5 years
   - 10 points: 5+ years

CRITICAL: Apply these penalties:
- If resume contains unfilled fields or placeholder dates: DISQUALIFY
- If resume contains AI boilerplate phrases: Deduct 10 points
- If resume opening/closing is obviously AI-generated: Deduct 10 points

Total Score Calculation:
Sum all rubric points to get score out of 80 base + penalties/bonuses.
Round to nearest integer.

OUTPUT FORMAT (JSON):
{
  "rubric_scores": {
    "language": 10,
    "algorithms": 8,
    "devops": 10,
    ...
  },
  "penalties": {
    "boilerplate": -10,
    "unfilled_fields": 0
  },
  "total_score": 78,
  "reasoning": "Brief explanation of score",
  "recommendation": "HIRE / MAYBE / PASS"
}
```

#### Implementation

```python
def score_with_rubric(resume, jd):
    """Use improved rubric-based prompt."""
    prompt = create_rubric_prompt(resume, jd)
    response = gemini_client.generate_content(prompt)

    # Parse JSON output
    import json
    result = json.loads(response.text)

    return {
        'total_score': result['total_score'],
        'rubric_breakdown': result['rubric_scores'],
        'reasoning': result['reasoning']
    }
```

#### Expected Outcome

- Score range: 0–80+ (wider spread; less clustering)
- Traceable scoring logic (see rubric breakdown)
- Consistent penalty application (built into prompt)
- Easier to audit (JSON output with breakdown)

---

### Strategy 2: Request Finer-Grained Output from Gemini

Instead of 1–10 → 1–100 mapping, ask for 1–100 directly.

#### Current Flow

```
Gemini: 8.5
Scaling: 8.5 × 10 = 85
Result: 85 (tied with 24 others at 85)
```

#### Improved Flow

```
Gemini: 78 (direct 1-100 request)
Result: 78 (unique score; easier to differentiate)
```

#### Prompt Change

```
"Score this resume on a scale of 1-100, where:
- 1-20: Not qualified (major gaps)
- 21-40: Below target (significant gaps)
- 41-60: Potentially qualified (some gaps)
- 61-80: Good fit (minor gaps)
- 81-100: Excellent fit (complete match or bonus skills)"
```

#### Expected Outcome

- Natural spread: candidates at 45, 67, 78, 82, 91, 95 (instead of clustered at 85)
- No artificial banding
- Easier ranking differentiation

---

### Strategy 3: Implement Post-Scoring Audit Sample

Randomly review 5–10% of scored resumes for quality assurance.

#### Process

```python
import random

def post_stage_4_audit(stage_4_json, sample_rate=0.10):
    """Randomly review sample of scored resumes."""

    with open(stage_4_json) as f:
        data = json.load(f)

    candidates = data['candidates']
    sample_size = max(5, int(len(candidates) * sample_rate))
    sample = random.sample(candidates, sample_size)

    audit_results = []
    for candidate in sample:
        manual_score = human_reviewer.score(candidate['resume'], candidate['job_description'])
        diff = abs(manual_score - candidate['gemini_score'])

        audit_results.append({
            'candidate_id': candidate['candidate_id'],
            'gemini_score': candidate['gemini_score'],
            'manual_score': manual_score,
            'difference': diff,
            'status': 'PASS' if diff <= 10 else 'FLAG'
        })

    # Save audit report
    audit_df = pd.DataFrame(audit_results)
    audit_df.to_csv('stage_4_audit_sample.csv', index=False)

    # Print summary
    flagged = audit_df[audit_df['status'] == 'FLAG']
    print(f"Audit sample: {len(audit_results)} candidates")
    print(f"Flagged (diff > 10): {len(flagged)}")
    print(f"Mean difference: {audit_df['difference'].mean():.1f}")

    return audit_results
```

#### Success Metric

- Mean score difference < 5 points
- <5% of sample flagged as problematic
- Identify systematic biases in Gemini scoring

---

### Strategy 4: Calibration Against Ground Truth

Use hiring decision data to calibrate Gemini scoring.

#### Data Collection

```python
# After hiring decisions are made, collect feedback
hiring_feedback = {
    'candidate_id': [1, 2, 3, ...],
    'stage_4_score': [95, 75, 85, ...],
    'hired': [True, False, True, ...],
    'performance_rating': [4.5, None, 4.0, ...]  # if hired
}
```

#### Analysis

```python
import pandas as pd
import numpy as np

df = pd.DataFrame(hiring_feedback)

# Analyze score calibration
hired = df[df['hired'] == True]
rejected = df[df['hired'] == False]

print(f"Avg score (hired): {hired['stage_4_score'].mean():.1f}")
print(f"Avg score (rejected): {rejected['stage_4_score'].mean():.1f}")

# Correlation: stage 4 score vs performance
correlation = hired[['stage_4_score', 'performance_rating']].corr()
print(f"Score ↔ performance correlation: {correlation.iloc[0,1]:.2f}")

# Find threshold: score X → hire decision Y
thresholds = {}
for score_threshold in range(50, 100, 5):
    above_threshold = df[df['stage_4_score'] >= score_threshold]
    if len(above_threshold) > 0:
        hire_rate = above_threshold['hired'].mean()
        thresholds[score_threshold] = hire_rate
```

#### Improvement

Use calibration data to adjust future scores:

```python
# Example: if score 85 historically predicts 70% hire rate
# and score 75 predicts 40% hire rate
# Can use this to adjust prompt or post-process scores
```

---

## Implementation Checklist

### Phase 1: Immediate (This Week)

- [ ] Disqualify Courtney Walsh (E-commerce, unfilled template)
- [ ] Disqualify Sonia (SE, rejection letter)
- [ ] Disqualify Ananya 90 (SE, placeholder dates)
- [ ] Disqualify Diya (SE, student)
- [ ] Remove duplicate Amara entry
- [ ] Manually review Victor Johnson & Steve King
- [ ] Regenerate corrected rankings
- [ ] Document changes in audit report

### Phase 2: Short-Term (Weeks 2–3)

- [ ] Implement pre-Stage-4 validator class
- [ ] Add email deduplication to Stage 3
- [ ] Implement AI boilerplate penalty
- [ ] Add experience threshold filtering at Stage 1
- [ ] Test all changes on historical data
- [ ] Document changes in operational guide

### Phase 3: Long-Term (Weeks 4–8)

- [ ] Redesign Gemini prompt with rubric
- [ ] Change Gemini output format to JSON
- [ ] Test new prompt on sample of 20 resumes
- [ ] Compare new vs old scores; validate improvement
- [ ] Implement post-Stage-4 audit sampling
- [ ] Set up ground truth collection pipeline
- [ ] Document new methodology in STAGE_4_METHODOLOGY.md

---

## Success Metrics

### Short-Term Success (After Phase 1–2)

| Metric                             | Current      | Target          |
| ---------------------------------- | ------------ | --------------- |
| Invalid resumes reaching Stage 4   | 4–5          | 0               |
| Duplicate candidates in ranking    | 1–2          | 0               |
| Score range                        | E-com: 75–95 | E-com: 65–95+   |
| Score range                        | SE: 35–90    | SE: 40–100      |
| Largest tied band                  | 42% of pool  | <15% of pool    |
| AI boilerplate penalty consistency | Inconsistent | 100% consistent |
| Manual review time                 | High         | Low             |

### Long-Term Success (After Phase 3)

| Metric                          | Current   | Target                 |
| ------------------------------- | --------- | ---------------------- |
| Score distribution              | Clustered | Normal (bell curve)    |
| Rubric transparency             | Opaque    | Full breakdown visible |
| Audit sample flagging rate      | Unknown   | <5%                    |
| Score ↔ performance correlation | Unknown   | >0.7                   |
| Hiring manager confidence       | Medium    | High                   |

---

## Conclusion

**Immediate fixes (Phase 1):** Prevent use of invalid data  
**Short-term improvements (Phase 2):** Fix recurring issues  
**Long-term strategy (Phase 3):** Build systematic reliability

Together, these recommendations will transform Stage 4 from a source of ranking errors into a trustworthy, transparent, and auditable scoring system.

---

_For context on each issue, see:_

- [STAGE_4_OVERVIEW.md](STAGE_4_AUDIT_OVERVIEW.md)
- [STAGE_4_METHODOLOGY.md](STAGE_4_METHODOLOGY.md)
- [STAGE_4_SYSTEMIC_ISSUES.md](STAGE_4_SYSTEMIC_ISSUES.md)
- [STAGE_4_JOB1_ECOMMERCE_AUDIT.md](STAGE_4_JOB1_ECOMMERCE_AUDIT.md)
- [STAGE_4_JOB2_SOFTWARE_ENGINEER_AUDIT.md](STAGE_4_JOB2_SOFTWARE_ENGINEER_AUDIT.md)
