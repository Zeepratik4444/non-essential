---
name: Skill Name
description: One-sentence description of what this skill enables.
version: 1.0.0
author: your-name
triggers:
  - keyword1
  - keyword2
---

## Purpose
What problem this skill solves and when to use it.

## Protocol
Step-by-step instructions the agent MUST follow when using this skill.

1. **Step 1** — Description
2. **Step 2** — Description
3. **Step 3** — Description

## Tools Available
List any scripts in scripts/ and what they do.

| Script | Purpose | Usage |
|--------|---------|-------|
| `validate.py` | Validates output format | `run_script('validate.py', '<arg>')` |

## References
List any docs in references/ and what they contain.

| File | Contents |
|------|----------|
| `guide.md` | Detailed how-to guide |
| `examples.md` | Worked examples |

## Output Format
Describe the exact format the agent must return.

## Constraints
- What the agent must NOT do
- Edge cases to handle
- Error handling expectations
