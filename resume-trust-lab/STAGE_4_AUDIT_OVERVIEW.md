# Stage 4 Audit Report — Overview

**Report Date:** May 13, 2026  
**Scope:** Resume scoring across 2 job roles (E-commerce Specialist, Software Engineer) using Gemini API ranking engine  
**Total Candidates Analyzed:** 100 resumes (50 per role)  
**Data Source:** Stage 4 (Gemini Ranking Base) JSON outputs

---

## Executive Summary

The Stage 4 scoring engine (Gemini API) produced several categories of systematic errors across both job roles:

| Issue Type                              | E-commerce | Software Engineer | Total |
| --------------------------------------- | ---------- | ----------------- | ----- |
| Overscored resumes                      | 7          | 6                 | 13    |
| Underscored resumes                     | 3          | 5                 | 8     |
| **Critical disqualification errors**    | 1          | 3                 | **4** |
| AI template boilerplate (not penalized) | 12         | 13                | 25    |
| Score clustering (tied candidates)      | 18 @ 95    | 24 @ 85           | 42    |

### Root Causes

1. **Insufficient score granularity:** 36–48% of each job's pool shares a single score, rendering ranking unreliable
2. **Inconsistent AI template penalties:** 25 resumes with obvious AI-generated boilerplate receive varying scores (35–95 range)
3. **Incomplete resumes not filtered:** Templates with unfilled fields, placeholder dates, and malformed data reach Stage 4
4. **Duplicate entries not deduplicated:** Multiple candidates share identical identities (email + name)
5. **Scoring bias:** Missing required skills not penalized proportionally; keyword presence rewarded but absence underpenalized

### Critical Issues Requiring Action Before Use

- **E-commerce Specialist, Rank 22:** Courtney Walsh — unfilled contact fields; blank template scored as 92
- **Software Engineer, Rank 31:** Sonia — embedded AI rejection letter in resume body; scored 85
- **Software Engineer, Ranks 23 & 28:** Two "Amara" entries with identical email; duplicate submission
- **Software Engineer, Ranks 48 & 49:** Victor Johnson (45pts) and Steve King (40pts) — likely engine failures despite strong profiles

---

## Key Statistics

### E-commerce Specialist

- **Total candidates:** 50
- **Score range:** 75–95
- **Mean score:** 90.72
- **Median score:** 95
- **Largest tied band:** 18 candidates at 95 (36% of pool)

### Software Engineer

- **Total candidates:** 50
- **Score range:** 35–90
- **Mean score:** 78.4
- **Median score:** 85
- **Largest tied band:** 24 candidates at 85 (48% of pool)

---

## File Organization

This audit is organized into the following reports:

| File                                                                               | Contents                                                                                                 |
| ---------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| [STAGE_4_METHODOLOGY.md](STAGE_4_METHODOLOGY.md)                                   | Pipeline architecture, Stage 4 operation, scoring logic, configuration                                   |
| [STAGE_4_JOB1_ECOMMERCE_AUDIT.md](STAGE_4_JOB1_ECOMMERCE_AUDIT.md)                 | E-commerce role: JD summary, score distribution, critical errors, scoring errors, integrity flags        |
| [STAGE_4_JOB2_SOFTWARE_ENGINEER_AUDIT.md](STAGE_4_JOB2_SOFTWARE_ENGINEER_AUDIT.md) | Software Engineer role: JD summary, score distribution, critical errors, scoring errors, integrity flags |
| [STAGE_4_SYSTEMIC_ISSUES.md](STAGE_4_SYSTEMIC_ISSUES.md)                           | Cross-job patterns, root cause analysis, pipeline improvement areas                                      |
| [STAGE_4_RECOMMENDATIONS.md](STAGE_4_RECOMMENDATIONS.md)                           | Immediate actions, short-term improvements, long-term strategy                                           |

---

## Findings Summary

### Most Severe Errors

#### 1. Software Engineer: Victor Johnson (Rank 48, 45pts → Should be ~78)

Victor has one of the broadest technical profiles in the set:

- Java, Python, Node.js, Ruby
- DevOps: Docker, Kubernetes, Jenkins, Ansible, Travis CI
- Algorithms, APIs, multiple databases
- Master's degree in Software Engineering

Scoring him 45 places him below a current undergraduate. **This is a scoring engine failure.**

#### 2. E-commerce Specialist: Jason Jones (Rank 50, 75pts → Should be ~92)

Jason has a complete skill profile:

- Shopify + WooCommerce
- Google Analytics, Excel
- Paid Social, UX, SEO
- **Shopify Plus Certification** (premium credential)
- 5+ years experience

Ranked dead last with 75 despite stronger profile than many 92–95 candidates. **Significant underscoring error.**

#### 3. E-commerce Specialist: Courtney Walsh (Rank 22, 92pts → Should be Disqualified)

Resume has completely unfilled contact fields:

```
Address: [Insert Address]
Phone: [Insert Phone Number]
Email: [Insert Email]
LinkedIn: [Insert LinkedIn Profile URL]
```

This is a raw template that was never completed. **Critical data quality issue.**

#### 4. Software Engineer: Sonia (Rank 31, 85pts → Should be Disqualified)

Resume body ends with an AI-generated rejection letter:

> "After careful consideration, we regret to inform you that we will not be moving forward with your application..."

This is not a valid resume submission. **Critical data quality issue.**

---

## Next Steps

1. **Read [STAGE_4_METHODOLOGY.md](STAGE_4_METHODOLOGY.md)** for understanding of how Stage 4 scores resumes and current configuration
2. **Review job-specific audits:** [STAGE_4_JOB1_ECOMMERCE_AUDIT.md](STAGE_4_JOB1_ECOMMERCE_AUDIT.md) and [STAGE_4_JOB2_SOFTWARE_ENGINEER_AUDIT.md](STAGE_4_JOB2_SOFTWARE_ENGINEER_AUDIT.md)
3. **Understand systemic issues:** [STAGE_4_SYSTEMIC_ISSUES.md](STAGE_4_SYSTEMIC_ISSUES.md)
4. **Implement recommendations:** [STAGE_4_RECOMMENDATIONS.md](STAGE_4_RECOMMENDATIONS.md)

---

_Full audit data with candidate details, skill coverage analysis, and comparative assessment available in role-specific reports._
