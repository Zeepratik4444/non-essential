---
name: content-idea-generator
description: Generates creative content ideas for various online platforms and topics.
triggers:
  - "generate content ideas"
  - "content ideas for"
  - "help with content"
  - "brainstorm content"
---

# Content Idea Generator Skill

This skill assists in generating multiple creative content ideas based on a given topic or platform.

## Protocol

1. **Receive Topic/Platform**: The user provides a topic (e.g., "social media marketing," "healthy recipes") or a specific platform (e.g., "YouTube," "Instagram," "blog").
2. **Generate Ideas**: Use the `generate_ideas.py` script to brainstorm and output a list of diverse content ideas.
3. **Present Ideas**: Display the generated ideas in a clear, formatted list.

## Output Format

The output will be a Markdown-formatted list of content ideas:

### Content Ideas for "[User's Topic/Platform]"

- Idea 1: [Brief description of the idea]
- Idea 2: [Brief description of the idea]
- Idea 3: [Brief description of the idea]
- ... (up to 5-10 ideas)

## Rules

- Always generate at least 5 distinct ideas.
- Ideas should be relevant to the provided topic or platform.
- Avoid repetitive or generic ideas. Strive for creativity and uniqueness.
- If no topic or platform is provided, ask the user for clarification.

## References

- `scripts/generate_ideas.py`: Python script for generating content ideas.
