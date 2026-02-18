---
name: frontend-development
description: >
  Build, review, and debug frontend code including React, Next.js,
  HTML, CSS, and TypeScript. Use when user needs UI components,
  styling, state management, performance optimisation, or
  frontend architecture guidance.
triggers:
  - "build a component"
  - "react component"
  - "next.js"
  - "css styling"
  - "frontend bug"
  - "ui implementation"
  - "typescript frontend"
  - "state management"
---

# Frontend Development

## When to Use
- Building React or Next.js components
- CSS/Tailwind styling and responsive design
- TypeScript type definitions and interfaces
- State management (Zustand, Redux, Context API)
- Performance optimisation (lazy loading, memoisation)
- Debugging frontend issues

## Protocol
1. Identify the task type (build, review, debug, optimise)
2. Identify the stack (React/Next.js, styling library, state manager)
3. Load references/component_patterns.md for architecture patterns
4. Write or review code following the standards checklist
5. Return complete, working code with usage example

## Code Standards (Always Follow)
- TypeScript strict mode — no `any` types
- Functional components only — no class components
- Props always typed via `interface`, not `type` for components
- Named exports only — no default exports except pages
- No inline styles — use Tailwind or CSS modules
- `useCallback` and `useMemo` only when profiling shows need
- Error boundaries around async data components
- Loading and error states always handled

## Component Structure
```tsx
// 1. Imports (external → internal → types)
// 2. Interface definition
// 3. Component function
// 4. Subcomponents (if small enough to co-locate)
// 5. Named export
```

## Output Format

### Task: {build | review | debug | optimise}

**Stack**: {React | Next.js} + {Tailwind | CSS Modules} + {TypeScript}

#### Code

```tsx
{complete working code}
```

#### Usage Example

```tsx
{how to use the component}
```

#### Notes

- {any caveats, dependencies to install, or follow-up steps}

## Rules

- Always return complete, runnable code — no placeholders or TODOs
- Include all necessary imports
- Handle loading, error, and empty states
- Mobile-first responsive design by default
- Accessibility: semantic HTML, ARIA labels, keyboard navigation
- Never use deprecated APIs (e.g., componentDidMount, findDOMNode)

## References

- Component patterns and architecture: read references/component_patterns.md
- Performance checklist: read references/performance_checklist.md
- Accessibility standards: read references/accessibility_guide.md
