# Skill Marketplaces

Always check both before writing a skill from scratch.

## skills.sh

**Homepage**: https://skills.sh
**Skill URL**: `https://skills.sh/{owner}/skills/{skill-name}`

### Known Collections

| Owner | Domain |
|-------|--------|
| `anthropics/skills` | General, document gen, code review, MCP |
| `obra/superpowers` | Debugging, git, planning |
| `wshobson/agents` | FastAPI, PostgreSQL, Python |
| `vercel-labs/agent-skills` | React, Next.js, frontend |
| `coreyhaines31/marketingskills` | SEO, copywriting, CRO |
| `antfu/skills` | Vue, Vite, Vitest |
| `expo/skills` | React Native, mobile |

### Fetch Strategy
1. `web_fetch(action='search_skills_sh', topic='<keyword>')` — get candidate URLs
2. `web_fetch(action='fetch_skill', skill_name='<slug>', source='skills.sh')` — auto-tries all owners
3. `web_fetch(action='fetch_url', url='https://skills.sh/<owner>/skills/<slug>')` — direct

---

## skillhub.club

**Homepage**: https://skillhub.club
**Total**: 21,000+ skills
**Skill URL**: `https://skillhub.club/{author}/{skill-name}`

### Fetch Strategy
```python
web_fetch(action='fetch_url', url='https://skillhub.club')
web_fetch(action='fetch_skill', skill_name='<slug>', source='skillhub.club')
```

### Top Reference Skills (S-rank 9.0+)
- `systematic-debugging` — structured debugging protocol
- `skill-creator` — meta skill creation
- `file-search` — codebase search
- `backend-models-standards` — database schema standards

---

## What to Extract

When you fetch a marketplace skill, pull:
- **Protocol**: Steps, order, branching logic
- **Output**: Template with concrete example
- **References**: What domain knowledge is bundled
- **Rules**: Hard constraints
- **Triggers**: Phrases that activate the skill

**Adapt — do NOT copy verbatim.** Customize for user's context.

## Attribution
Add at top of `skill.md` body:
`<!-- Adapted from: https://skills.sh/anthropics/skills/code-review -->`
