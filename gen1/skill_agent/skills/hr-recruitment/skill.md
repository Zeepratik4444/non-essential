---
name: hr-recruitment
description: >
  Assist with HR and recruitment tasks including writing job descriptions,
  screening resumes, drafting interview questions, creating offer letters,
  and building hiring workflows. Use when user needs hiring support,
  candidate evaluation, or HR document generation.
triggers:
  - "write a job description"
  - "screen resumes"
  - "interview questions"
  - "offer letter"
  - "hiring process"
  - "evaluate candidate"
  - "onboarding checklist"
---

# HR & Recruitment

## When to Use
- Writing job descriptions and role requirements
- Screening and scoring resumes against criteria
- Generating structured interview question sets
- Drafting offer letters and employment terms
- Building hiring pipelines and evaluation rubrics

## Protocol
1. Identify the specific HR task from the user's request
2. Load the relevant reference for that task type:
   - Job description writing → references/jd_templates.md
   - Resume screening → references/screening_rubric.md
   - Interview prep → references/interview_frameworks.md
3. Gather required inputs (role, level, skills, location, salary)
4. Execute task following the template exactly
5. Return structured output ready to use

## Task Quick Reference

### Job Description
Required inputs: Role title, level (Junior/Mid/Senior), department,
key responsibilities (3–5), required skills, nice-to-have skills,
location, salary range (optional), company culture note.

### Resume Screening
Required inputs: Job description or criteria, list of candidate resumes.
Output: Scored table with Pass / Review / Reject per candidate.

### Interview Questions
Required inputs: Role, level, key competencies to assess.
Output: 5 behavioural + 5 technical + 3 culture-fit questions with
expected answers and scoring rubric per question.

### Offer Letter
Required inputs: Candidate name, role, start date, salary, benefits,
reporting manager, office location or remote policy.

## Output Format

#### Job Description
**Role**: {title} | **Level**: {level} | **Location**: {location}

**About the Role**
{2–3 sentence hook}

**Responsibilities**
- {responsibility}

**Requirements**
- {must-have skills}

**Nice to Have**
- {bonus skills}

**What We Offer**
- {benefits / culture}

---

#### Resume Screening Matrix
| Candidate | Must-Have Match | Experience | Red Flags | Score /10 | Decision   |
|-----------|----------------|------------|-----------|-----------|------------|
| Name      | 4/5            | 3 yrs      | None      | 7.5       | ✅ Proceed |

## Rules
- Never fabricate candidate qualifications — only assess what is provided
- Always use inclusive, bias-free language in job descriptions
- Flag any potential discriminatory language if found in user input
- Offer letters must note: "subject to formal employment contract"
- Do not include salary if user did not provide it

## References
- JD templates by role type: read references/jd_templates.md
- Resume screening rubric: read references/screening_rubric.md
- Interview question frameworks: read references/interview_frameworks.md
