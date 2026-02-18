---
name: code-review
description: >
  Review code for correctness, security vulnerabilities, performance issues,
  maintainability, and best practices. Use when user submits code for review,
  asks for feedback, or needs a pull request reviewed across any language
  or framework.
triggers:
  - "review my code"
  - "check this code"
  - "code feedback"
  - "PR review"
  - "is this code correct"
  - "security review"
  - "refactor this"
---

# Code Review

## When to Use
- Reviewing any code for quality, correctness, or security
- Pull request reviews
- Security audits of code snippets
- Refactoring suggestions
- Performance improvement recommendations

## Protocol
1. Identify the language and framework
2. Load references/review_checklist.md for full checklist
3. Review the code systematically across all 5 dimensions
4. Categorise every finding by severity
5. Return structured report with specific line-level feedback
6. Provide corrected code for all High severity findings

## 5 Review Dimensions
- **Correctness**: Does it do what it's supposed to?
- **Security**: Any injection, exposure, or auth bypass risks?
- **Performance**: Any unnecessary loops, N+1, blocking calls?
- **Maintainability**: Is it readable, well-named, DRY?
- **Standards**: Does it follow language/framework conventions?

## Severity Levels
🔴 **Critical** — Bug or security issue. Must fix before merge.
🟠 **High** — Significant problem. Should fix before merge.
🟡 **Medium** — Improvement needed. Fix soon.
🟢 **Low** — Suggestion or nitpick. Optional.
💡 **Praise** — Highlight good patterns.

## Output Format
### Code Review: {language} / {framework}
**Lines reviewed**: {count}
**Overall**: ✅ Approve | 🔄 Request Changes | 🚫 Reject

#### Summary
{2–3 sentence overall assessment}

#### Findings

🔴 **Critical: SQL Injection (Line 34)**
```python
# Current — vulnerable
query = f"SELECT * FROM users WHERE id = {user_id}"

# Fixed
query = "SELECT * FROM users WHERE id = :user_id"
result = db.execute(query, {"user_id": user_id})
```

> Never interpolate user input into SQL strings.

🟡 **Medium: Magic Number (Line 12)**

```python
# Current
if retries > 3:

# Fixed
MAX_RETRIES = 3
if retries > MAX_RETRIES:
```

💡 **Praise: Good error handling (Line 56)**
> Clean try/except with specific exception types. Good pattern.

#### Corrected Code

```python
{full corrected version for Critical/High findings}
```

## Rules
- Quote the exact problematic code in every finding
- Always provide the fixed version for Critical and High findings
- Never nitpick style if it's a minor personal preference
- Security findings always rated Critical or High — no exceptions
- If the code has no issues, say so clearly — do not invent findings

## References
- Full review checklist by language: read references/review_checklist.md
- Security vulnerability patterns: read references/security_patterns.md
- Common performance anti-patterns: read references/performance_antipatterns.md
