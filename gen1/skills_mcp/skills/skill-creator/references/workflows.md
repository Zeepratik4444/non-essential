# Workflow Patterns

## Sequential
```markdown
## Protocol
1. Load references/schema.md
2. Validate input against schema
3. Transform using rules in references/rules.md
4. Return output in format below
```

## Conditional
```markdown
## Protocol
1. Identify input type
   - If CSV → CSV path
   - If JSON → JSON path
   - If unknown → ask user

### CSV Path
1. Parse headers...

### JSON Path
1. Validate against schema...
```

## Discovery-First (for APIs/DBs/filesystems)
```markdown
## Protocol
1. Read references/schema.md for available tables/endpoints
2. Identify relevant ones for the request
3. Construct query/request
4. Validate before returning
```

## Validation Checkpoint
```markdown
## Protocol
1. Plan — describe what you will do before doing it
2. Execute
3. Verify output matches expected format
4. If fails → identify error, retry once
5. If still fails → return error with explanation
```

## Freedom Calibration

| Situation | Use |
| :-- | :-- |
| Multiple valid approaches | Text instructions (high freedom) |
| Preferred pattern, variation OK | Pseudocode (medium) |
| Fragile, consistency critical | Exact script + steps (low freedom) |

## When to Read References
Always tell the agent explicitly:
1. Read references/finance.md (only if query involves financial metrics)
2. Read references/schema.md (always, before writing any query)
