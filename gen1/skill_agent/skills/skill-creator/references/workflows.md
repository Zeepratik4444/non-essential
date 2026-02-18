# Workflow Patterns

Reference for designing multi-step processes in skills.

## Sequential Workflow Pattern

Use when steps must happen in a fixed order:

```markdown
## Protocol
1. Load references/schema.md to understand the data model
2. Validate the input against the schema
3. Transform the data using the rules in references/rules.md
4. Return the result in the Output Format below
```


## Conditional Workflow Pattern

Use when branching logic is needed:

```markdown
## Protocol
1. Identify the input type
   - If CSV → follow CSV path below
   - If JSON → follow JSON path below
   - If unknown → ask the user to clarify

### CSV Path
1. Parse headers from first row
2. ...

### JSON Path
1. Validate against schema in references/schema.md
2. ...
```


## Discovery-First Pattern

Use when the agent needs to discover context before acting (databases, APIs, filesystems):

```markdown
## Protocol
1. Read references/schema.md to understand available tables/endpoints
2. Identify which tables/endpoints are relevant to the request
3. Construct the query/request
4. Validate the result before returning
```


## Validation Checkpoint Pattern

Use for error-prone operations:

```markdown
## Protocol
1. Plan the operation — describe what you will do before doing it
2. Execute the operation
3. Verify the output matches the expected format
4. If verification fails, identify the error and retry once
5. If still failing, return the error with a clear explanation
```


## Freedom Calibration Guide

| Situation | Use |
| :-- | :-- |
| Multiple valid approaches, context-dependent | Text instructions (high freedom) |
| Preferred pattern exists, some variation OK | Pseudocode or parameterized script (medium) |
| Fragile operation, consistency critical | Specific script, exact steps (low freedom) |

## Progressive Disclosure Reference Linking

Always tell Claude explicitly when to read a reference and why:

```markdown
## Protocol
1. Read references/finance.md to understand the metric definitions
   - Read this ONLY if the query involves financial metrics
2. Read references/schema.md for the database layout
   - Always read this before writing any query
```
