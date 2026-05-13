# Stage 4 Audit Report — Job 2: Software Engineer

**Role:** Software Engineer  
**Total Candidates Scored:** 50  
**Score Range:** 35–90  
**Mean Score:** 78.4  
**Median Score:** 85

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

### Core Technical Requirements

| Skill Area                       | Specific Technologies                                                      |
| -------------------------------- | -------------------------------------------------------------------------- |
| **Primary Language**             | Java                                                                       |
| **Algorithms & Data Structures** | Algorithm design, complexity analysis, fundamental DS                      |
| **System Design**                | Microservices, scalability, distributed systems, event-driven architecture |
| **DevOps**                       | Docker, Kubernetes, Jenkins, CI/CD pipelines                               |
| **Web/Backend Development**      | Spring, Django, React, REST APIs                                           |
| **Version Control**              | Git, SVN                                                                   |
| **Testing**                      | JUnit, Mockito, integration testing, test automation                       |
| **API Design**                   | RESTful APIs, GraphQL, API gateways                                        |

### Preferred Qualifications

- Cloud platforms (AWS, Azure, Google Cloud)
- Agile methodologies (Scrum, Kanban)
- Mentoring/leadership experience
- **5+ years of professional experience**
- Computer Science degree

### Key Skills (Inferred from Resume Patterns)

All resumes in the dataset mention most of these. **Critical filtering factors:**

| Skill                                | Importance | Why                                                   |
| ------------------------------------ | ---------- | ----------------------------------------------------- |
| Java                                 | Core       | Primary language specified in JD                      |
| Algorithms/DS                        | Core       | Fundamental for software engineering roles            |
| System Design                        | Core       | Role likely involves architectural decisions          |
| DevOps (Docker, Kubernetes, Jenkins) | Core       | Modern backend roles require infrastructure knowledge |
| Testing                              | Core       | Explicitly mentioned in JD                            |
| APIs (REST/GraphQL)                  | Core       | Backend role requirement                              |
| Cloud                                | Important  | "Preferred" but increasingly standard                 |
| 5+ years experience                  | Important  | Professional maturity                                 |

---

## Score Distribution Analysis

### Breakdown by Score Band

| Score | Count | Percentage | Ranks |
| ----- | ----- | ---------- | ----- |
| 90    | 8     | 16%        | 1–8   |
| 85    | 24    | 48%        | 9–32  |
| 75    | 7     | 14%        | 33–39 |
| 65    | 7     | 14%        | 40–46 |
| 60    | 1     | 2%         | 47    |
| 45    | 1     | 2%         | 48    |
| 40    | 1     | 2%         | 49    |
| 35    | 1     | 2%         | 50    |

### Key Observation: Massive Score Clustering

**24 out of 50 candidates (48%) share an identical score of 85.**

This is even more severe than the E-commerce dataset (which had 36% at 95). Nearly half the pool is indistinguishable by score.

#### Skill Coverage Variation Within the 85 Band

| Rank | Name                     | DevOps? | System Design? | Testing? | Cloud? | Score |
| ---- | ------------------------ | ------- | -------------- | -------- | ------ | ----- |
| 9    | Robert Lambert (30)      | ✗       | ✗              | ✓        | ✗      | 85    |
| 14   | Ananya (90)              | ✗       | ✗              | ✗        | ✗      | 85    |
| 20   | Christopher Spencer (23) | ✓       | ✓              | ✓        | ✓      | 85    |
| 32   | [Multiple others]        | Varies  | Varies         | Varies   | Varies | 85    |

**Conclusion:** The 85 band includes candidates with 1–4 core skills, making the ranking essentially arbitrary within this band.

---

## Critical Errors

### Candidate 87: Sonia | Rank 31 | Score: 85 → **Should be: DISQUALIFIED**

#### Resume Issue

The resume body ends with an AI-generated rejection letter:

```
After careful consideration, we regret to inform you that we will not be
moving forward with your application for the Software Engineer position at
this time. While your technical skills and experience are impressive, our team
is looking for candidates with more direct experience in [specific area]. Thank
you for your interest in joining our team.
```

#### Problem

This is a **data quality failure**. An AI generator appended a rejection response to the candidate's own resume. The document is not a valid job application under any interpretation.

#### Additional Issues

- Only 3 years of experience (JD prefers 5+)
- Career gap: most recent role ended in 2020; no explanation for 2020–present
- No surname — identity unverifiable

#### Recommendation

**Disqualify and remove from ranking immediately.**

---

### Candidates 92 & 93: Duplicate Identity (Two "Amara" entries) | Ranks 23 & 28 | Both 85pts → **One Must Be Removed**

#### Duplicate Details

| Field      | Candidate 92 (Rank 23) | Candidate 93 (Rank 28) |
| ---------- | ---------------------- | ---------------------- |
| Name       | Amara                  | Amara                  |
| Email      | amara@email.com        | amara@email.com        |
| Score      | 85                     | 85                     |
| Experience | 3.6 years              | 5+ years (lead role)   |

#### Problem

**Two candidates share identical name and email address.** This is either:

1. **Same person submitted twice** with slightly different resumes, OR
2. **AI-generated personas** assigned the same identity by mistake

#### Impact

Only one entry can legitimately appear in a ranking. Scoring both is a deduplication failure at an earlier pipeline stage.

#### Recommendation

**Remove one entry. Require candidate to resubmit with unique, verifiable contact details if both are claimed to be real.**

---

### Candidate 95: Diya | Rank 50 | Score: 35 → **Should be: Filtered Out Before Stage 4**

#### Profile Summary

- Status: Current undergraduate (BSc Computer Science, 2020–2024)
- Experience: Internship only
  - Software Tester internship (Summer 2022)
  - Coding Club volunteer (2020–2022)
- GPA: 2.8 (below typical professional standard)
- Self-assessment: "basic programming skills"

#### Problem

Diya is a **current student, not a professional**. The role requires professional experience; she should have been filtered at Stage 1 or 2.

#### Scoring Assessment

The 35 score **correctly identifies her as the weakest candidate**, but the deeper issue is that **she should not appear in a ranked pool** for a professional software engineering role.

#### Recommendation

Implement experience threshold filtering at earlier stages. If role requires professional experience, automatically reject students and entry-level interns.

---

## Overscored Candidates

### Candidate 62: Debra Peck | Rank 1 | Score: 90 → **Should be: ~78**

#### Profile Summary

- Background: Backend and full-stack development
- Experience: 5+ years
- Focus: Web development with React

#### Skills Analysis

| Core Skill      | Present? | Notes                                                 |
| --------------- | -------- | ----------------------------------------------------- |
| Java            | ✓        | Present                                               |
| Algorithms/DS   | ✓        | Present                                               |
| System Design   | ✗        | **Missing**                                           |
| DevOps          | ✗        | **Missing entirely** — no Docker, Kubernetes, Jenkins |
| Testing         | ✓        | JUnit, TestNG                                         |
| APIs            | ✓        | RESTful, SOAP                                         |
| Cloud           | ✗        | Not mentioned                                         |
| Version Control | ✓        | Git                                                   |

#### Data Quality Issue

Resume contains unfilled placeholder: `[University Name]`

#### Assessment

Missing **two of the most important technical areas for senior engineering** — system design and DevOps. Other 90-scorers have both of these.

The placeholder university field also indicates incomplete data entry.

**Suggested adjustment:** 90 → 78

---

### Candidate 5: Erin Stout | Rank 5 | Score: 90 → **Should be: ~75**

#### Resume Opening

> "Here's a sample professional resume for Erin Stout"

#### Problem

**Explicit AI template framing** — this should trigger a penalty (see boilerplate section).

#### Skills Analysis

| Core Skill      | Present? | Notes                      |
| --------------- | -------- | -------------------------- |
| Java            | ✓        | Present                    |
| Algorithms/DS   | ✗        | **Not mentioned anywhere** |
| System Design   | ✗        | Not mentioned              |
| DevOps          | ✗        | Not mentioned              |
| Testing         | ✗        | Not mentioned              |
| APIs            | ✗        | Not mentioned              |
| Cloud           | ✗        | Not mentioned              |
| Version Control | ✓        | Git                        |

#### Assessment

- Missing algorithms/DS is a **fundamental gap** for a software engineering role
- Template framing should apply a penalty (~−10 to −15 points)
- Missing 5 out of 8 core skills yet scored at 90

**Suggested adjustment:** 90 → 75 (or lower if template penalty applied)

---

### Candidate 90: Ananya | Rank 14 | Score: 85 → **Should be: ~50 or Disqualified**

#### Resume Issues

| Issue                                                | Severity     |
| ---------------------------------------------------- | ------------ |
| Dates are placeholder: `20XX–20XX` throughout        | Critical     |
| Email contains backslash escape: `\ananya@email.com` | Critical     |
| No professional work experience                      | Critical     |
| Student/fresh graduate only                          | Data quality |

#### Skills Analysis

| Core Skill    | Present? | Notes                 |
| ------------- | -------- | --------------------- |
| Java          | ✗        | Not mentioned         |
| Algorithms/DS | ✗        | Not mentioned         |
| System Design | ✗        | Not mentioned         |
| DevOps        | ✗        | Not mentioned         |
| Testing       | ✗        | Not mentioned         |
| APIs          | ✗        | Not mentioned         |
| Cloud         | ✗        | Not mentioned         |
| Experience    | 0 years  | Student/projects only |

#### Assessment

This resume **has never been properly completed** (placeholder dates), contains a **broken email address**, and shows **no industry experience**.

Scoring it 85 and tying it with 5+ year engineers is a **fundamental error**.

**Recommendation:** Pre-Stage-4 validation should reject this before scoring.

**Suggested adjustment:** 85 → 50 (or disqualify)

---

### Candidate 92: Amara | Rank 23 | Score: 85 → **Should be: ~70**

#### Profile Summary

- Experience: 3.6 years only (JD prefers 5+)
- Title progression appears suspicious: "Lead Software Engineer" after only ~2 years total
- No surname — identity unverifiable

#### Skills Analysis

| Core Skill    | Present? | Notes         |
| ------------- | -------- | ------------- |
| DevOps        | ✗        | **Missing**   |
| Testing       | ✗        | **Missing**   |
| System Design | ✗        | Not mentioned |
| APIs          | ✓        | Present       |
| Java          | ✓        | Present       |

#### Additional Issues

Also flagged in Critical Errors section as a duplicate identity (shared email with Candidate 93).

#### Assessment

Only 3.6 years of experience, suspicious career progression, and missing critical skills (DevOps, testing). Scoring at 85 (same as 5+ year engineers) is unjustified.

**Suggested adjustment:** 85 → 70

---

### Candidate 30: Robert Lambert | Rank 9 | Score: 85 → **Should be: ~70**

#### AI Boilerplate Detection

Resume ends with AI template sign-off:

> "This is just a sample resume, and you should tailor your own resume… Remember to proofread your resume multiple times for any errors or formatting issues before submitting it."

#### Problem

This is **explicit AI-generated text appended to candidate's resume**. It should trigger a penalty (see boilerplate section for consistency issue).

#### Assessment

Even ignoring the boilerplate, the scorer should apply a **consistent penalty** for this pattern. Currently, same boilerplate appears in resumes ranging from 90 down to 65 with no clear logic.

**Suggested adjustment:** 85 → 70 (accounting for boilerplate penalty)

---

### Candidate 88: Ananya | Rank 26 | Score: 85 → **Should be: ~65**

#### Self-Referential Meta-Commentary

Resume includes:

> "Note that I've included some data that may be relevant for a senior-level position… I've also included some data that may be relevant for a junior-level position."

#### Problem

This is **the AI generator narrating its own output choices**, not a real candidate statement. This indicates AI generation artifact rather than authentic submission.

#### Skills Analysis

| Core Skill | Present? | Notes       |
| ---------- | -------- | ----------- |
| DevOps     | ✗        | **Missing** |
| API Design | ✗        | **Missing** |
| Testing    | ✗        | **Missing** |

#### Assessment

Missing 3 core areas + contains meta-commentary indicating AI generation. Scoring at 85 is not justified.

**Suggested adjustment:** 85 → 65

---

## Underscored Candidates

### Candidate 53: Victor Johnson | Rank 48 | Score: 45 → **Should be: ~78 (Most Severe Underscoring Error)**

#### Profile Summary

- Experience: Master's degree in Software Engineering
- Background: Full-stack backend development
- Languages: Java, Python, Node.js, Ruby, PHP

#### Skills Analysis

| Core Skill      | Present? | Notes                                           |
| --------------- | -------- | ----------------------------------------------- |
| Java            | ✓        | Primary language                                |
| Algorithms/DS   | ✓        | Explicit: algorithm design and implementation   |
| System Design   | ✓        | Microservices, event-driven, SOA                |
| DevOps          | ✓        | Docker, Kubernetes, Ansible, Jenkins, Travis CI |
| Testing         | ✓        | Unit and integration testing                    |
| APIs            | ✓        | RESTful, OAuth, JWT, API gateways, Swagger      |
| Cloud           | ✓        | Cloud database architecture                     |
| Version Control | ✓        | Multiple systems mentioned                      |

#### Coverage Summary

Victor covers **all 8 core technical areas**. His skill breadth is among the strongest in the entire dataset.

#### The Scoring Error

Victor is ranked **48th out of 50 with only 45 points** — below almost everyone except Diya (a current student with 35pts).

A score of 45 places Victor:

- Below 24 candidates in the 85 band (many of whom have 2–3 fewer skills)
- Below 7 candidates at 75 (despite having significantly more expertise)
- Only 10 points above Diya, the current undergraduate with internship experience

#### Assessment

**This is a critical scoring engine failure.** There is no defensible justification for scoring Victor Johnson at 45. Possible root causes:

1. **Resume format issue** — perhaps resume structure caused parsing failure
2. **Keyword mismatch** — maybe uses different terminology for skills
3. **Gemini API error** — transient LLM hallucination or rating collapse

#### Recommendation

**This candidate must be manually reviewed and rescored.** Victor should likely score 75–85 based on skill profile.

**Suggested adjustment:** 45 → 78 (minimum); possibly higher given Master's degree

---

### Candidate 21: Steve King | Rank 49 | Score: 40 → **Should be: ~80**

#### Profile Summary

- Experience: 5+ years professional
- Languages: Java, Python
- Specialization: Cloud data engineering and machine learning

#### Skills Analysis

| Core Skill    | Present? | Notes                                                          |
| ------------- | -------- | -------------------------------------------------------------- |
| Java          | ✓        | Present                                                        |
| Algorithms/DS | ✓        | Present                                                        |
| System Design | ✗        | Not explicitly mentioned, but implied in distributed data work |
| DevOps        | ✓        | Full stack: Docker, Kubernetes, Jenkins                        |
| Testing       | ✓        | Unit and integration testing                                   |
| APIs          | ✓        | RESTful APIs                                                   |
| Cloud         | ✓        | Apache Beam, BigQuery, cloud data engineering                  |
| ML/Advanced   | ✓        | scikit-learn, TensorFlow (bonus: not in JD but valuable)       |

#### AI Boilerplate

Resume contains minor sign-off: _"Let me know if you have any questions"_

This phrase appears across the full score range (35–95) and should trigger a consistent minor penalty, not a −45 point deduction.

#### Assessment

Steve is ranked **49th with 40 points** — only 5 points above Diya (a current student).

With 5+ years of experience, full DevOps stack, and cloud data engineering expertise, Steve should score **75–85 minimum**.

The −45 point gap between Steve (40pts) and the 85-band average is completely unjustified.

#### Recommendation

**This is another critical scoring failure.** Steve's resume may have triggered the same parsing issue as Victor Johnson's.

**Suggested adjustment:** 40 → 80 (minimum)

---

### Candidate 23: Christopher Spencer | Rank 45 | Score: 65 → **Should be: ~85**

#### Profile Summary

- Languages: Java, Python, C++
- Experience: System architecture, leadership, open-source contribution

#### Skills Analysis

| Core Skill    | Present? | Notes                                                 |
| ------------- | -------- | ----------------------------------------------------- |
| Java          | ✓        | Present                                               |
| Algorithms/DS | ✓        | Present                                               |
| System Design | ✓        | Microservices, event-driven, SOA                      |
| DevOps        | ✓        | Full stack: Jenkins, Docker, Kubernetes, GitLab CI/CD |
| Testing       | ✓        | Present                                               |
| APIs          | ✓        | REST + GraphQL                                        |
| Cloud         | ✓        | AWS + Azure                                           |
| Leadership    | ✓        | Bonus qualification                                   |

#### Credentials & Proof

- AWS DevOps Engineer Certified
- Certified Scrum Master
- Certified Java Developer
- Published technical articles
- Open-source contributor with **10,000+ GitHub stars** on Java library

#### Assessment

Christopher is **among the strongest candidates in the dataset**. He covers all core technical areas plus leadership and open-source experience.

A score of 65 places him below candidates with significantly narrower skill coverage. This underscoring is difficult to justify.

**Suggested adjustment:** 65 → 85 (or higher)

---

### Candidate 0: David Rivera | Rank 41 | Score: 65 → **Should be: ~82**

#### Profile Summary

- Experience: 5+ years
- Academic background: ACM ICPC participant, published research
- Languages: Java, C++, Python

#### Skills Analysis

| Core Skill    | Present? | Notes                                |
| ------------- | -------- | ------------------------------------ |
| Java          | ✓        | Present                              |
| Algorithms/DS | ✓        | ACM ICPC → strong fundamentals       |
| System Design | ✓        | Microservices, event-driven, RESTful |
| DevOps        | ✓        | Jenkins, Docker, CI/CD               |
| Testing       | ✓        | Present                              |
| APIs          | ✓        | REST + event-driven APIs             |
| Cloud         | ✓        | AWS + Azure                          |

#### Resume Quality

Clean, professional, complete. Only minor AI closing line: _"This is just an example…"_ — which should not justify −20 point deduction.

#### Assessment

David covers 7 out of 8 core areas and has research publication background. A 65 score is an underestimation; he should be in the 80–85 band.

**Suggested adjustment:** 65 → 82

---

### Candidate 40: Joshua Rodriguez | Rank 43 | Score: 65 → **Should be: ~80**

#### Profile Summary

- Experience: 5+ years
- Role: Senior engineer with mentoring responsibility
- Languages: Java, Python

#### Skills Analysis

| Core Skill    | Present? | Notes                       |
| ------------- | -------- | --------------------------- |
| Java          | ✓        | Primary language            |
| Algorithms/DS | ✓        | Present                     |
| System Design | ✗        | Not explicitly mentioned    |
| DevOps        | ✓        | Docker, Kubernetes, Jenkins |
| Testing       | ✓        | Present                     |
| APIs          | ✓        | REST + GraphQL              |
| Cloud         | ✗        | Not mentioned               |
| Leadership    | ✓        | Mentoring junior engineers  |

#### Assessment

Clean resume with 5+ years experience, strong DevOps coverage, and leadership experience. Missing system design and cloud explicitly, but otherwise solid.

Scoring at 65 (lower than the 75 band) is not well justified. Should be closer to 75–80.

**Suggested adjustment:** 65 → 80

---

## Integrity & Quality Flags

### AI Template Boilerplate — 13 Resumes Affected

| Rank | Candidate ID | Name               | Template Text                                                             | Score |
| ---- | ------------ | ------------------ | ------------------------------------------------------------------------- | ----- |
| 2    | 26           | David Roberson     | "Remember to tailor your resume to the specific job you're applying for"  | 90    |
| 5    | 5            | Erin Stout         | _Opening:_ "Here's a sample professional resume for Erin Stout"           | 90    |
| 6    | 7            | John Morgan        | "Note: This is just a sample resume…"                                     | 90    |
| 9    | 30           | Robert Lambert     | "This is just a sample resume… Remember to proofread…"                    | 85    |
| 12   | 20           | Kristen Young      | "Let me know if you have any questions or need any further modifications" | 85    |
| 24   | 33           | Christopher Rivera | "Note: This is just a sample resume…"                                     | 85    |
| 36   | 4            | Gregory Saunders   | "Note that this is just a sample resume…"                                 | 85    |
| 39   | 9            | Sheena Johnson     | "Note: The above resume is just a sample…"                                | 85    |
| 40   | 12           | Joseph Miller      | _Opening:_ "Here's a sample professional resume for Joseph Miller"        | 65    |
| 41   | 0            | David Rivera       | "This is just an example…"                                                | 65    |
| 42   | 34           | Leonard Cruz       | _Opening:_ "Here's a sample professional resume for Leonard Cruz"         | 65    |
| 47   | 27           | James Moore        | "This is just a sample resume…"                                           | 60    |
| 49   | 21           | Steve King         | "Let me know if you have any questions or need further modifications"     | 40    |

#### Problem

The same AI boilerplate phrases appear across **all score bands (40–90) with no consistent penalty**.

If a phrase appears in a 40-point resume (Steve King) and a 90-point resume (Erin Stout), the scoring engine is not consistently penalizing it.

#### Recommendation

Implement pre-scoring flag: identify AI boilerplate patterns and apply standardized −5 to −10 point penalty consistently.

---

### Single-Name Candidates — Identity Unverifiable

12 candidates use only a first name with no surname:

| Candidate ID | Name   | Rank | Score |
| ------------ | ------ | ---- | ----- |
| 89           | Rajiv  | 7    | 90    |
| 83           | Oliver | 10   | 90    |
| 85           | Lucas  | 13   | 85    |
| 92           | Amara  | 23   | 85    |
| 94           | Arjun  | 11   | 90    |
| 88           | Ananya | 26   | 85    |
| 91           | Meera  | 8    | 90    |
| 93           | Amara  | 28   | 85    |
| 87           | Sonia  | 31   | 85    |
| 99           | Kunal  | 25   | 85    |
| 86           | Aarav  | 27   | 85    |
| 95           | Diya   | 50   | 35    |

**Impact:** ~24% of the candidate pool has identity verification issues.

**Assessment:** Several of these appear to be **AI-generated personas** rather than real applicants. This creates significant hiring liability — you cannot legally hire someone whose real name is unverifiable.

#### Recommendation

Pre-Stage-4 validation should require full name (first + last) for all candidates. Flag single-name submissions for manual review or rejection.

---

### Rank 15: Career Switch (Medical Doctor to Software Engineer)

**Richard Cameron (Candidate 31, Rank 15, 85pts)**

- Professional background: 5 years as a medical doctor (2010–2015)
- Switched to software engineering: 2015–present (~11 years software)
- Score: 85

#### Assessment

The career switch context is notable but not an error — Richard now has 11 years of software engineering experience, which is solid.

Reviewers should note the career transition history, but the 85 score appears appropriate given his software engineering tenure.

---

### Rank 26: Self-Undermining Meta-Commentary

**Ananya (Candidate 88, Rank 26, 85pts)**

Resume includes:

> "Note that I've included some data that may be relevant for a senior-level position… I've also included some data that may be relevant for a junior-level position."

#### Problem

This is the AI generator **narrating its own output choices**. The candidate's actual seniority level is ambiguous because the AI couldn't decide.

#### Impact

Hiring managers cannot determine if this candidate is senior or junior level. This makes the resume essentially unusable for hiring decisions.

#### Recommendation

Pre-Stage-4 validation should reject resumes containing self-referential AI commentary.

---

## Key Findings

### Summary of Scoring Issues

| Issue                                   | Count | Severity     |
| --------------------------------------- | ----- | ------------ |
| Overscored candidates                   | 6     | High         |
| Underscored candidates                  | 5     | High         |
| Critical disqualification errors        | 3     | **Critical** |
| AI template boilerplate (not penalized) | 13    | Medium       |
| Score clustering (unusable ties)        | 24    | **Critical** |
| Single-name/identity unverifiable       | 12    | Medium       |

### Root Causes

1. **No skill-by-skill point values** — all skills weighted equally despite different importance
2. **DevOps and System Design underweighted** — candidates without these score same as those with them
3. **No consistency penalty for AI boilerplate** — same phrases appear at all score levels
4. **Insufficient score granularity** — 1-10 scale mapped to 1-100 creates catastrophic clustering
5. **No completeness checks** — resumes with placeholder dates, broken emails, no experience scored as valid
6. **Duplicate detection failed** — two Amara entries with same email both scored and ranked

### Most Severe Errors (Requiring Immediate Action)

| Rank  | Name           | Issue                                             | Current | Should be        |
| ----- | -------------- | ------------------------------------------------- | ------- | ---------------- |
| 31    | Sonia          | Embedded rejection letter + no career explanation | 85      | **Disqualified** |
| 23/28 | Amara (×2)     | Duplicate identity (same email)                   | Both 85 | One removed      |
| 48    | Victor Johnson | Strong profile, master's degree                   | 45      | ~78              |
| 49    | Steve King     | 5+ years, full DevOps, cloud data eng.            | 40      | ~80              |
| 50    | Diya           | Current student/intern                            | 35      | **Filter out**   |

---

## Recommended Immediate Actions (Before Using This Ranking)

- [ ] **Disqualify Sonia (Rank 31, 85pts)** — embedded rejection letter
- [ ] **Remove one Amara entry (Ranks 23 & 28, both 85pts)** — duplicate email address
- [ ] **Manually review Victor Johnson (Rank 48, 45pts)** — likely scoring error
- [ ] **Manually review Steve King (Rank 49, 40pts)** — likely scoring error
- [ ] **Filter out Diya (Rank 50, 35pts)** — current student should not be in professional ranking
- [ ] **Implement pre-Stage-4 data validation** — catch incomplete resumes, duplicate emails, placeholder dates

---

_For full pipeline methodology, see [STAGE_4_METHODOLOGY.md](STAGE_4_METHODOLOGY.md)_  
_For E-commerce role audit, see [STAGE_4_JOB1_ECOMMERCE_AUDIT.md](STAGE_4_JOB1_ECOMMERCE_AUDIT.md)_  
_For cross-job analysis and recommendations, see [STAGE_4_SYSTEMIC_ISSUES.md](STAGE_4_SYSTEMIC_ISSUES.md) and [STAGE_4_RECOMMENDATIONS.md](STAGE_4_RECOMMENDATIONS.md)_
