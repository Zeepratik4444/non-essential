# Architecture

## Overview

```

Client (HTTP)
│
▼
┌─────────────────────────────────┐
│         FastAPI (main.py)       │
│  /api/v1/run  /api/v1/skills    │
└────────────┬────────────────────┘
│
▼
┌─────────────────────────────────┐
│        SkillsCrew (crew.py)     │
│   CrewAI @CrewBase, sequential  │
└────────────┬────────────────────┘
│
▼
┌─────────────────────────────────┐
│      skills_operator (Agent)    │
│  LLM: gemini/gemini-2.5-flash   │
│  memory=True, cache=True        │
│  max_iter=25, max_retry=3       │
└────────────┬────────────────────┘
│  uses
▼
┌─────────────────────────────────┐
│      SkillsManagerTool          │
│  list_skills → load_skill →     │
│  list_resources → read_resource │
│  → run_script → create_skill    │
└────────────┬────────────────────┘
│  reads
▼
┌─────────────────────────────────┐
│       ./skills/ directory       │
│   each subdirectory = 1 skill   │
│   skill.md (YAML front-matter)  │
│   references/  scripts/         │
└─────────────────────────────────┘

```

## Skill Discovery Flow

1. On first tool call, `SkillsManagerTool` scans `./skills/` directory
2. Each subdirectory with a `skill.md` is parsed — YAML front-matter gives `name`, `description`, `triggers`
3. Metadata is cached in-memory; cache auto-refreshes if the directory `mtime` changes
4. Agent calls `list_skills` → gets a formatted registry → picks the right skill → calls `load_skill`

## Cache Invalidation

The tool tracks the `mtime` of the `./skills/` directory. Any new skill added on disk is picked up on the next tool call automatically — no restart needed.

## Path Safety

All file reads inside skills are traversal-safe: paths are resolved and verified to stay within the skill's own directory before any read or script execution.

## Skill Structure

```

skills/<skill-name>/
├── skill.md          \# Required — YAML front-matter + instructions
├── references/       \# Optional — extra .md or .txt reference docs
└── scripts/          \# Optional — runnable .py utility scripts

```

### skill.md Front-Matter Schema

```yaml
name: skill-name          # Used as the lookup key
description: >            # Shown in list_skills output
  One paragraph describing when to use this skill.
triggers:                 # Keyword phrases that suggest this skill
  - "phrase one"
  - "phrase two"
```