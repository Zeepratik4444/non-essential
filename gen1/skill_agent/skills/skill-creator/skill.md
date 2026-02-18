---
name: skill-creator
description: >
  Create, design, and package new skill modules for the skill_agent system.
  Use when a user asks to create a new skill, add a skill for a new domain,
  improve an existing skill, or needs guidance on how to structure a skill.
  Triggers: "create a skill", "add a skill", "new skill for X", "build a skill",
  "skill template", "skill structure", "improve this skill".
triggers:
  - "create a skill"
  - "add a skill"
  - "new skill for"
  - "build a skill"
  - "skill template"
  - "improve this skill"
  - "skill structure"
---

# Skill Creator

Create effective, lean skill modules for the skill_agent system.

## Core Principles

- **Concise is key** — the context window is shared. Only include what Claude doesn't already know.
- **Progressive disclosure** — metadata always loads; SKILL.md body loads on trigger; references/scripts load only when needed.
- **Match freedom to fragility** — narrow instructions for error-prone steps, broad instructions for judgment-based steps.

## Skill Anatomy

```

skill-name/
├── skill.md           # Required — YAML frontmatter + instructions
├── references/        # Optional — docs loaded into context as needed
├── scripts/           # Optional — executable Python/Bash utilities
└── assets/            # Optional — output files (templates, icons, boilerplate)

```

### skill.md Frontmatter (required)

```yaml
---
name: skill-name
description: >
  What this skill does AND when to use it. This is the trigger mechanism —
  be explicit about use cases and trigger phrases here.
  Do NOT add extra YAML fields beyond name and description.
---
```

> Put ALL "when to use" context in the description — the body only loads after triggering.

## Creation Protocol

### Step 1 — Understand with Examples

Ask the user for 2–3 concrete example tasks this skill should handle. Clarify:

- What would a user say to trigger this skill?
- What does a good output look like?
- Are there domain-specific rules, schemas, or templates involved?


### Step 2 — Plan Reusable Contents

For each example, identify what would be rewritten repeatedly:

- Repeated code → `scripts/`
- Reference docs, schemas, API specs → `references/`
- Output templates, boilerplate, assets → `assets/`


### Step 3 — Create the Skill Directory

Create the directory under `./skills/<skill-name>/` with:

- `skill.md` (required)
- `references/`, `scripts/`, `assets/` only if needed

Via API:

```bash
POST /api/v1/skills
{ "name": "skill-name", "content": "<skill.md content>" }
```

Via filesystem (agent picks it up immediately, no restart needed).

### Step 4 — Write skill.md

**Frontmatter**: Clear `name` and comprehensive `description` with trigger phrases.

**Body guidelines**:

- Use imperative/infinitive form ("Load references/schema.md", "Return a JSON object")
- Keep body under 500 lines
- Reference bundled files explicitly: "See references/patterns.md for X"
- Move detailed content to `references/` — keep `skill.md` lean
- See `references/workflows.md` for multi-step process patterns
- See `references/output-patterns.md` for output format patterns


### Step 5 — Validate Before Delivering

Check:

- [ ] Frontmatter has `name` and `description` — nothing else
- [ ] Description covers what + when + trigger phrases
- [ ] Body is under 500 lines
- [ ] Every referenced file actually exists in the skill folder
- [ ] No README.md, CHANGELOG.md, or auxiliary docs included
- [ ] Scripts are self-contained and tested


### Step 6 — Iterate

After the user tests the skill on real tasks, refine based on:

- Steps the agent struggled with → add more guidance
- Context the agent hallucinated → add a `references/` file
- Code the agent rewrote repeatedly → move to `scripts/`


## What NOT to Include

- `README.md`, `INSTALLATION.md`, `CHANGELOG.md` — never
- Information Claude already knows (general Python syntax, standard REST patterns, etc.)
- Duplicate content between `skill.md` and `references/` — pick one location
- Deeply nested reference chains — keep references one level deep from `skill.md`


## Output Format

Deliver the skill as a set of files with full content. For each file show:

```
### `skills/<skill-name>/skill.md`
<full file content>

### `skills/<skill-name>/references/example.md`  
<full file content>
```

Then provide the folder structure summary:

```
skills/<skill-name>/
├── skill.md
├── references/
│   └── example.md
└── scripts/
    └── example.py
```
