# Stage 4 Audit Report — Job 1: E-commerce Specialist

**Role:** E-commerce Specialist  
**Total Candidates Scored:** 50  
**Score Range:** 75–95  
**Mean Score:** 90.72  
**Median Score:** 95

---

## Table of Contents

1. [Job Description Summary](#job-description-summary)
2. [Score Distribution Analysis](#score-distribution-analysis)
3. [Critical Errors](#critical-errors)
4. [Overscored Candidates](#overscored-candidates)
5. [Underscored Candidates](#underscored-candidates)
6. [Integrity & Quality Flags](#integrity--quality-flags)
7. [Key Findings](#key-findings)

---

## Job Description Summary

### Core Responsibilities

- Write and edit product content for e-commerce websites/portals
- Set standards and best practices for product listings
- Cross-team collaboration (product, graphics, sales)
- Support across: **PPC, Email Marketing, SEO, Keyword Research, Google Analytics, UX, and Paid Social Media**
- Identify SEO best practices for inventory, pre-orders, and pricing
- Monitor product sales using web analytics and Excel (pivot tables, VLOOKUPs)

### Requirements

- **3+ years** in a fast-paced e-commerce business
- Experience with **e-commerce website builders** (Shopify, Elementor)
- Knowledge of digital sales strategies and website conversions
- Familiarity with **web design**
- BSc in Marketing or relevant field

### Key Skills (Explicitly Required)

| Skill                | Importance                                  |
| -------------------- | ------------------------------------------- |
| Shopify or Elementor | Core (website builder)                      |
| Google Analytics     | Core (analytics mentioned twice)            |
| PPC                  | Core (paid advertising)                     |
| Email Marketing      | Core (listed separately)                    |
| Paid Social Media    | Core (listed separately)                    |
| Excel                | Core (explicitly for pivot tables/VLOOKUPs) |
| SEO                  | Important                                   |
| UX                   | Important                                   |
| Web Design           | Required                                    |

---

## Score Distribution Analysis

### Breakdown by Score Band

| Score | Count | Percentage | Ranks |
| ----- | ----- | ---------- | ----- |
| 95    | 18    | 36%        | 1–18  |
| 92    | 8     | 16%        | 19–26 |
| 90    | 12    | 24%        | 27–38 |
| 85    | 11    | 22%        | 39–49 |
| 75    | 1     | 2%         | 50    |

### Key Observation: Score Clustering

**18 out of 50 candidates (36%) share an identical score of 95.**

Among these 18 candidates tied at 95, skill coverage varies dramatically:

| Candidate          | Shopify | Google Analytics | PPC | Email Marketing | Paid Social | Excel | Score |
| ------------------ | :-----: | :--------------: | :-: | :-------------: | :---------: | :---: | ----- |
| John Crawford (29) |    ✗    |        ✓         |  ✗  |        ✗        |      ✗      |   ✗   | 95    |
| Ryan Bradley (69)  |    ✓    |        ✓         |  ✓  |        ✓        |      ✗      |   ✗   | 95    |
| Lisa Aguirre (19)  |    ✓    |        ✓         |  ✓  |        ✓        |      ✓      |   ✓   | 95    |

**Conclusion:** The scoring engine cannot differentiate between candidates with 2 core skills vs. 6 core skills when both cluster at 95. This makes the ranking unreliable for hiring decisions.

---

## Critical Errors

### Candidate 61: Courtney Walsh | Rank 22 | Score: 92 → **Should be: DISQUALIFIED**

#### Resume Fragment

```
Contact Information:
Address: [Insert Address]
Phone: [Insert Phone Number]
Email: [Insert Email]
LinkedIn: [Insert LinkedIn Profile URL]
```

#### Issue

This resume is a **raw template that was never completed**. All contact fields are unfilled placeholders. The candidate did not submit a real resume — either an AI tool generated this and it was submitted without being finished, or the pipeline ingested a template file in error.

#### Impact

- Scoring a blank-contact template at 92 is the most egregious error in the E-commerce dataset
- Ranks this incomplete submission 22nd out of 50 candidates ahead of real applicants
- Creates significant credibility issue: hiring managers would contact non-existent email

#### Recommendation

**Remove immediately before using this ranking.** Implement pre-Stage-4 validation to catch unfilled fields.

---

## Overscored Candidates

### Candidate 29: John Crawford | Rank 1 | Score: 95 → **Should be: ~80**

#### Profile Summary

- Background: Marketplace specialist (Amazon, eBay, Walmart)
- Experience: 5+ years in e-commerce
- Certifications: Google Analytics, HubSpot

#### Skills Analysis

| Required Skill      | Present? | Notes                                                 |
| ------------------- | -------- | ----------------------------------------------------- |
| Shopify / Elementor | ✗        | Critical gap — focuses on marketplaces not web stores |
| Google Analytics    | ✓        | Strong (certified)                                    |
| PPC                 | ✗        | Not mentioned                                         |
| Email Marketing     | ✗        | Not mentioned                                         |
| Paid Social Media   | ✗        | Not mentioned                                         |
| Excel               | ✗        | Not mentioned                                         |
| Web Design          | ✗        | Not mentioned                                         |

#### Assessment

John is a strong **marketplace e-commerce specialist** but the role explicitly requests broad marketing support across PPC, Email, Paid Social, and **Shopify-based web stores**. His expertise is narrowly focused on third-party marketplace platforms (Amazon, eBay, Walmart), not self-hosted Shopify implementations.

A candidate who covers all required areas should rank above John. Placing him #1 is incorrect.

**Suggested adjustment:** 95 → 80

---

### Candidate 22: Sarah Myers | Rank 8 | Score: 95 → **Should be: ~85**

#### Profile Summary

- Role: E-commerce Manager
- Background: Online retail and marketing

#### Skills Analysis

| Required Skill      | Present? | Notes                |
| ------------------- | -------- | -------------------- |
| Shopify / Elementor | ✗        | **Missing**          |
| Google Analytics    | ✓        | Present              |
| PPC                 | ✗        | Not mentioned        |
| Email Marketing     | ✓        | Mentioned in passing |
| Paid Social Media   | ✗        | Not mentioned        |
| Excel               | ✗        | **Missing**          |
| Web Design          | ✗        | **Missing**          |

#### AI Template Detection

Resume contains: _"Let me know if you have any questions or need any further modifications"_

This is a telltale AI-generated closing line found in multiple resumes across the dataset. No penalty was applied.

#### Assessment

Missing Shopify (explicitly required) and Excel (explicitly required for pivot tables/VLOOKUPs). Scoring at 95 (tied with full-stack candidates) is not justified.

**Suggested adjustment:** 95 → 85

---

### Candidate 78: Daniel Lee | Rank 10 | Score: 95 → **Should be: ~82**

#### Profile Summary

- Prior role: Inventory Manager at wholesaler
- Background: Product listing and supply chain

#### Skills Analysis

| Required Skill      | Present? | Notes                           |
| ------------------- | -------- | ------------------------------- |
| Shopify / Elementor | ✗        | Not mentioned                   |
| Google Analytics    | ✗        | **Missing despite JD emphasis** |
| PPC                 | ✗        | Not mentioned                   |
| Email Marketing     | ✗        | Not mentioned                   |
| Paid Social Media   | ✗        | Not mentioned                   |
| Excel               | ✓        | Present                         |
| Web Design          | ✗        | Not mentioned                   |

#### Assessment

Product listing experience looks strong on the surface, but lacks the multi-channel marketing support that the JD emphasizes (PPC, Email, Paid Social). Inventory management background is lower-relevance for a content-heavy e-commerce role. Missing Google Analytics (explicitly named in JD) is a significant gap.

**Suggested adjustment:** 95 → 82

---

### Candidate 65: Susan Haynes | Rank 12 | Score: 95 → **Should be: ~83**

#### Profile Summary

- Role: PPC Specialist
- Background: Google Ads, advertising strategy

#### Skills Analysis

| Required Skill      | Present? | Notes                               |
| ------------------- | -------- | ----------------------------------- |
| Shopify / Elementor | ✗        | Not mentioned                       |
| Google Analytics    | ✗        | **Missing** (lists Google Ads only) |
| PPC                 | ✓        | Strong (Google Ads)                 |
| Email Marketing     | ✗        | Not mentioned                       |
| Paid Social Media   | ✗        | Not mentioned                       |
| Excel               | ✗        | Not mentioned                       |
| Web Design          | ✗        | Not mentioned                       |

#### AI Template Detection

Resume contains: _"I hope it gives you an idea…"_ — AI-generated filler phrase.

#### Assessment

Narrow PPC expertise, but missing Google Analytics, Email, Paid Social, and Excel. Scoring at 95 (identical to candidates with broader coverage) is overestimation.

**Suggested adjustment:** 95 → 83

---

### Candidate 87: Tonya Lewis | Rank 15 | Score: 95 → **Should be: ~83**

#### Profile Summary

- Role: E-commerce Operations
- Platform: Shopify (strong)

#### Skills Analysis

| Required Skill      | Present? | Notes                                   |
| ------------------- | -------- | --------------------------------------- |
| Shopify / Elementor | ✓        | Present                                 |
| Google Analytics    | ✗        | **Missing despite explicit JD mention** |
| PPC                 | ✗        | Not mentioned                           |
| Email Marketing     | ✗        | Not mentioned                           |
| Paid Social Media   | ✗        | Not mentioned                           |
| Excel               | ✗        | **Missing**                             |
| Web Design          | ✗        | Not mentioned                           |

#### Assessment

Shopify is a plus, but missing 4 explicitly required/supported areas (GA, PPC, Email, Paid Social) plus Excel. Should rank in 85–88 band, not at 95.

**Suggested adjustment:** 95 → 83

---

### Candidate 48: Keith Richards | Rank 36 | Score: 90 → **Should be: ~65 or FLAG FOR REVIEW**

#### Resume Opening

> "Here's a sample professional resume for Keith Richards applying for the role of E-commerce Specialist"

#### Issue

This resume **explicitly frames itself as a sample/template**, not a real submission. The opening line indicates the document was generated as an example, not created by an actual applicant.

#### Profile Summary (If Real)

- Experience: 8+ years
- Shopify: Present
- Google Analytics: Present
- Google Ads: Present
- Excel: Present

#### Assessment

If the content were real (created by an actual person), this would be a solid candidate. However, the explicit "sample resume" framing creates authenticity doubt. This should either be:

1. **Heavily penalized** (−15 to −25 points) for being a template submission, OR
2. **Flagged for manual review** to determine if it's a real applicant or a sample accidentally ingested into the dataset

Current handling (90 score, no penalty) is inconsistent.

**Suggested adjustment:** 90 → 65 OR flag for manual verification

---

### Candidate 61: Courtney Walsh | Rank 22 | Score: 92 → **DISQUALIFIED**

_(See Critical Errors section above)_

---

## Underscored Candidates

### Candidate 53: Cynthia Cook | Rank 39 | Score: 85 → **Should be: ~92**

#### Profile Summary

- Experience: 5+ years e-commerce
- Platforms: Shopify, WooCommerce
- Education: Marketing degree

#### Skills Analysis

| Required Skill      | Present? | Notes                     |
| ------------------- | -------- | ------------------------- |
| Shopify / Elementor | ✓        | Shopify + WooCommerce     |
| Google Analytics    | ✓        | Plus SEMrush              |
| PPC                 | ✓        | Google Ads certified      |
| Email Marketing     | ✓        | Email marketing mentioned |
| Paid Social Media   | ✓        | Facebook Ads              |
| Excel               | ✓        | Plus Tableau, Power BI    |
| Web Design          | ✗        | Not explicitly mentioned  |

#### Coverage Assessment

Cynthia covers **6 out of 7** explicitly required areas. She's missing only web design, while many candidates ranked 92–95 are missing 3–4 areas.

**Comparison:**

- Sarah Myers (95, Rank 8): missing Shopify, PPC, Paid Social, Excel, Web Design = 5 skills missing
- Cynthia Cook (85, Rank 39): missing Web Design only = 1 skill missing
- Yet Cynthia scores 10 points lower

#### Assessment

Significant underscoring. Cynthia should rank in the 92 band based on skill coverage alone.

**Suggested adjustment:** 85 → 92

---

### Candidate 92: Michael Gutierrez | Rank 49 | Score: 85 → **Should be: ~92**

#### Profile Summary

- Education: UC Berkeley (Marketing degree)
- Experience: Digital Marketing Specialist
- Credentials: Google Analytics certified, Google Ads certified

#### Skills Analysis

| Required Skill      | Present? | Notes                         |
| ------------------- | -------- | ----------------------------- |
| Shopify / Elementor | ✓        | Shopify, WooCommerce, Magento |
| Google Analytics    | ✓        | Certified                     |
| PPC                 | ✓        | Google Ads certified          |
| Email Marketing     | ✓        | Email marketing specialist    |
| Paid Social Media   | ✓        | Social media advertising      |
| Excel               | ✓        | Data analysis mentioned       |
| Web Design          | ✓        | UX optimization mentioned     |

#### Coverage Assessment

Michael covers **all 7 required/supported skills**. He is one of the strongest marketing-and-e-commerce profiles in the entire dataset.

His credentials (Google Analytics cert, Google Ads cert) are formal proof of expertise in two of the JD's most emphasized areas.

#### Assessment

Dropping Michael to 85 places him behind multiple candidates with significantly narrower skill coverage. This is a clear underscoring error.

**Suggested adjustment:** 85 → 92

---

### Candidate 0: Jason Jones | Rank 50 | Score: 75 → **Should be: ~92 (Most Severe Underscoring Error)**

#### Profile Summary

- Experience: 5+ years e-commerce
- Credential: **Shopify Plus Certification** (premium credential)
- Role: Full-stack e-commerce management

#### Skills Analysis

| Required Skill      | Present? | Notes                              |
| ------------------- | -------- | ---------------------------------- |
| Shopify / Elementor | ✓        | Shopify Plus certified             |
| Google Analytics    | ✓        | Google Analytics present           |
| PPC                 | ✓        | Google Ads + Facebook Ads          |
| Email Marketing     | ✓        | Email campaign management          |
| Paid Social Media   | ✓        | Facebook Ads, Instagram Ads        |
| Excel               | ✓        | Spreadsheet analysis, pivot tables |
| Web Design          | ✓        | UX optimization                    |

#### Coverage Assessment

Jason covers **all 7 required areas**. His **Shopify Plus Certification** is a premium credential that sets him apart — it demonstrates specialized expertise in Shopify's enterprise platform.

#### The Scoring Error

Jason is ranked **dead last with 75 points** — a full **10 points below the next-lowest candidate** — despite having one of the most complete skill profiles in the dataset.

#### Impact

By ranking him 50th, the system places Jason:

- Below all 18 candidates at 95 (many of whom have fewer skills)
- Below Cynthia Cook (Rank 39, 85 pts) despite Jason having more skills
- Below Michael Gutierrez (Rank 49, 85 pts) despite Jason having certification proof

#### Assessment

This is the **most glaring underscoring error** in the E-commerce dataset. The 75 score appears to be a **scoring engine failure**, not a reflective assessment of Jason's fit.

**Suggested adjustment:** 75 → 92 (or higher, 95)

---

## Integrity & Quality Flags

### AI Template Boilerplate — 12 Resumes Affected

The following candidates have AI-generated sign-off or framing text. Currently, the scorer applies **no consistent penalty**:

| Rank | Candidate ID | Name               | Template Text                                                                | Score |
| ---- | ------------ | ------------------ | ---------------------------------------------------------------------------- | ----- |
| 1    | 29           | John Crawford      | "Let me know if you have any questions or if you'd like to make any changes" | 95    |
| 3    | 69           | Ryan Bradley       | "Remember to tailor your resume to the specific job description"             | 95    |
| 5    | 19           | Lisa Aguirre       | "Remember to tailor your resume"                                             | 95    |
| 8    | 22           | Sarah Myers        | "Let me know if you have any questions or need any further modifications"    | 95    |
| 16   | 42           | Kristin Madden     | "Let me know if you'd like to make any changes"                              | 95    |
| 17   | 41           | Cheyenne Douglas   | "Remember to tailor your resume"                                             | 95    |
| 31   | 4            | Dr. Robert Rosales | "Remember to tailor your resume to the specific job you're applying for"     | 90    |
| 33   | 99           | Mark Allen         | "Let me know if you have any questions"                                      | 90    |
| 34   | 6            | Raymond Hall       | "Let me know if you'd like any changes"                                      | 90    |
| 36   | 48           | Keith Richards     | _Opening line:_ "Here's a sample professional resume for Keith Richards…"    | 90    |
| 40   | 82           | Tamara Sanchez     | "Let me know if you have any questions"                                      | 85    |
| 42   | 24           | Denise Cole        | "Let me know if you have any questions or need further assistance"           | 85    |

#### Problem

The same AI-generated phrases appear across score bands 85–95 with **no systematic penalty applied**. A standardized deduction (e.g., −5 to −10 points) should apply to all resumes containing this boilerplate.

#### Recommendation

Implement a pre-scoring check: flag resumes containing known AI template phrases and apply consistent penalty.

---

### Experience Inversion

Both **Dr. Robert Rosales (Rank 31, 90pts)** and **Denise Cole (Rank 42, 85pts)** have **8+ years of e-commerce experience** yet score **below candidates with only 5-year backgrounds**.

Additional experience should not reduce a score. This suggests the scorer may be **penalizing complex resumes** or **not properly weighting experience level**.

---

### Score Compression at the Top

| Metric                    | Value        |
| ------------------------- | ------------ |
| Top candidate score       | 95           |
| 18th candidate score      | 95           |
| Candidates in top 5 bands | 49 out of 50 |
| Minimum score in top band | 85           |

**Well-calibrated scorers should produce wider spread:** top candidate 95, 18th best ~84, with meaningful gradation throughout.

Current clustering makes differentiation impossible.

---

## Key Findings

### Summary of Scoring Issues

| Issue                                   | Count | Severity |
| --------------------------------------- | ----- | -------- |
| Overscored candidates                   | 7     | High     |
| Underscored candidates                  | 3     | High     |
| Critical disqualification errors        | 1     | Critical |
| AI template boilerplate (not penalized) | 12    | Medium   |
| Score clustering (unusable ties)        | 18    | High     |

### Root Causes

1. **No skill-by-skill point values** — all skills weighted equally regardless of JD emphasis
2. **Keyword presence rewarded, absence underpenalized** — no proportional penalty for missing required skills
3. **No consistency penalty for AI boilerplate** — same phrases appear at all score levels
4. **Insufficient score granularity** — 1-10 scale mapped to 1-100 creates natural clustering
5. **No completeness checks** — resumes with unfilled fields scored as valid

### Recommended Immediate Actions (Before Using This Ranking)

- [ ] **Disqualify Courtney Walsh (Rank 22, 92pts)** — unfilled template
- [ ] **Review Jason Jones (Rank 50, 75pts)** — verify scoring error; likely should be ~92
- [ ] **Review Cynthia Cook (Rank 39, 85pts) and Michael Gutierrez (Rank 49, 85pts)** — both appear underscored by ~7 points

---

_For full pipeline methodology, see [STAGE_4_METHODOLOGY.md](STAGE_4_METHODOLOGY.md)_  
_For Software Engineer role audit, see [STAGE_4_JOB2_SOFTWARE_ENGINEER_AUDIT.md](STAGE_4_JOB2_SOFTWARE_ENGINEER_AUDIT.md)_  
_For cross-job analysis and recommendations, see [STAGE_4_SYSTEMIC_ISSUES.md](STAGE_4_SYSTEMIC_ISSUES.md) and [STAGE_4_RECOMMENDATIONS.md](STAGE_4_RECOMMENDATIONS.md)_
