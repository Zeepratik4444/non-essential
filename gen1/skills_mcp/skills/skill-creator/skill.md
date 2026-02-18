---
name: skill-creator
description: >
  Creates new skill modules for the skill_agent system on explicit user request only.
  Use when user says: "create a skill for X", "add a skill for X", "build a skill",
  "make a new skill for Y", "I need a skill that does Z", "improve this skill".
  Always searches skill marketplaces first. Writes and tests any scripts before saving.
  Never self-triggers — only runs when user explicitly requests skill creation.
triggers:
  - "create a skill"
  - "add a skill for"
  - "build a skill"
  - "make a skill"
  - "new skill for"
  - "i need a skill that"
  - "improve this skill"
  - "update this skill"
---

# Skill Creator

Creates well-structured, marketplace-informed, code-tested skill modules on explicit user request.

## Core Principles

- **Marketplace-first**: Search skills.sh and skillhub.club before writing from scratch
- **Test before write**: All scripts must pass code_executor before being saved to a skill
- **Concise**: Only include what the agent doesn't already know
- **Progressive**: metadata → skill.md → references/scripts (loaded only as needed)
- **Never self-trigger**: Only create when user explicitly asks

## Creation Protocol

### Step 1 — Clarify
If not already clear, ask:
- What domain/task should this skill handle?
- 2–3 example tasks it should execute
- What should a good output look like?
Ask one question at a time.

### Step 2 — Search Marketplaces
Read references/marketplaces.md for URLs and fetch strategy.

```python
web_fetch(action='search_skills_sh', topic='<domain keyword>')
web_fetch(action='fetch_skill', skill_name='<slug>', source='skills.sh')
web_fetch(action='fetch_url', url='https://skillhub.club/<slug>')
```

Extract from findings:
- Protocol steps and order
- Output format template
- References/scripts bundled
- Hard rules/constraints
- Trigger phrases

### Step 3 — Plan Structure
Decide what to include:
- Repeated logic → `scripts/` (must be tested)
- Reference docs, schemas, API specs → `references/`
- Output templates → `assets/`
Only create dirs that have real content.

### Step 4 — Write and Test Scripts (if any)
For every script in the skill:
1. Generate the Python code.
2. Test using `code_executor(action='run_python', code='...')`.
3. If it fails, fix and repeat until exit code is 0.
4. If missing packages, use `code_executor(action='install_package', package_name='...')`.

### Step 5 — Create the Skill
Create the base skill:
```python
skills_manager(action='create_skill', skill_name='<name>', skill_content='<full skill.md content>')
```

`skill.md` structure:
- Name and Description (with triggers) in frontmatter.
- Protocol (numbered).
- Output Format (concrete example).
- Rules (hard constraints).
- Attribution Link.

### Step 6 — Write Reference/Script Files
```python
skills_manager(action='write_file', skill_name='<name>', file_path='references/guide.md', file_content='...')
skills_manager(action='write_file', skill_name='<name>', file_path='scripts/helper.py', file_content='...')
```

### Step 7 — Test Scripts In-Skill
Run the script from its final location:
```python
skills_manager(action='run_script', skill_name='<name>', script_name='helper.py')
```

### Step 8 — Confirm and Reload
```python
skills_manager(action='refresh_cache')
skills_manager(action='list_skills')
```

## Output Format

Report the successful creation:

✅ **Skill Created**: `<skill-name>`
**Source**: `<marketplace URL or 'Original'>`

### `skills/<skill-name>/skill.md`
<content>

### `skills/<skill-name>/references/<file>`
<content>

***
*Trigger for testing: "<example task from Step 1>"*
