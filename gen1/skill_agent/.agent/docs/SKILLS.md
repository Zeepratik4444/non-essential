# Skills Reference

Skills are self-contained instruction modules stored in `./skills/`. Each skill tells the agent exactly how to behave for a specific domain.

## Available Skills

| Skill | Description |
|-------|-------------|
| `api-development` | Design, build, and document REST/GraphQL APIs |
| `code-review` | Review code for correctness, security, performance, and maintainability |
| `customer-support` | Draft empathetic, professional customer-facing responses |
| `database-design` | Design schemas, write queries, optimize database structure |
| `document-generation` | Generate structured documents, reports, and templates |
| `financial-analysis` | Analyze financial metrics, margins, and business performance |
| `frontend-development` | Build UI components, layouts, and frontend logic |
| `hr-recruitment` | Draft JDs, screen criteria, and HR-related communications |
| `legal-document-review` | Review contracts and legal clauses for risk and standard language |
| `research_assistant` | Gather, synthesize, and summarize information on any topic |

## How the Agent Uses Skills

```

Agent receives task
│
▼
list_skills         ← discover what's available
│
▼
load_skill(<name>)  ← read full protocol from skill.md
│
▼
[optional] list_resources / read_resource / run_script
│
▼
Execute task following skill protocol exactly

```

## Adding a New Skill

### Option 1 — API (dynamic, no restart)

```bash
POST /api/v1/skills
{
  "name": "data-analysis",
  "content": "# Data Analysis\n\nProtocol here..."
}
```


### Option 2 — Manual (filesystem)

1. Create directory: `skills/my-new-skill/`
2. Create `skill.md` with YAML front-matter:
```markdown
***
name: my-new-skill
description: >
  What this skill does and when the agent should use it.
triggers:
  - "keyword that triggers this skill"
***

# My New Skill

## When to Use
...

## Protocol
1. Step one
2. Step two

## Output Format
...

## Rules
...
```

3. Optionally add `references/` and `scripts/` subdirectories
4. The agent picks it up immediately — no restart required

## Skill Authoring Rules

- Always include YAML front-matter (`name`, `description`, `triggers`)
- Write `description` as a single clear paragraph — it appears in `list_skills` output
- The `Protocol` section must be a numbered step list
- The `Output Format` section must define the exact structure the agent should return
- The `Rules` section should list hard constraints the agent must never break
- Scripts in `scripts/` must be self-contained Python files

```
