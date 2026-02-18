---
name: customer-support
description: >
  Handle customer support tasks including drafting responses to complaints,
  resolving tickets, writing FAQ answers, escalation handling, and
  tone-appropriate communication. Use when user needs to respond to
  customers, resolve issues, or build support content.
triggers:
  - "respond to customer"
  - "handle complaint"
  - "draft support reply"
  - "resolve ticket"
  - "write FAQ"
  - "customer escalation"
  - "refund request"
---

# Customer Support

## When to Use
- Drafting responses to customer complaints or queries
- Handling escalations and sensitive situations
- Writing FAQ entries or help centre articles
- Resolving billing disputes, refund requests, or technical issues
- Maintaining tone consistency across support channels

## Protocol
1. Identify the ticket/issue type (complaint, query, escalation, refund, technical)
2. Identify the emotional tone of the customer (frustrated, neutral, upset, confused)
3. Load references/tone_guide.md for tone calibration
4. Draft response using the correct template from references/response_templates.md
5. Review against quality checklist before returning

## Tone Guide (Quick Reference)
| Customer Tone | Response Tone              | Approach                          |
|---------------|----------------------------|-----------------------------------|
| Frustrated    | Empathetic, calm           | Acknowledge first, solve second   |
| Angry         | De-escalating, sincere     | No defensiveness, own the issue   |
| Confused      | Clear, patient, simple     | Step-by-step guidance             |
| Neutral       | Friendly, professional     | Direct and efficient              |
| Upset (loss)  | Highly empathetic, careful | Lead with empathy, avoid scripts  |

## Response Structure (Always Follow)
1. **Acknowledge**: Validate the customer's experience
2. **Apologise** (if warranted): Sincere, not deflecting
3. **Explain**: Brief, honest explanation (no jargon)
4. **Resolve**: Clear action steps or solution
5. **Close**: Offer further help, warm sign-off

## Output Format
### Support Response Draft

**Ticket Type**: {complaint | query | refund | escalation | technical}
**Customer Tone**: {frustrated | neutral | angry | confused}
**Channel**: {email | chat | social media}
**SLA Status**: {within SLA | breached — note urgency}

---
**Subject**: {if email}

Dear {Customer Name},

{Acknowledge — 1 sentence}

{Apologise if needed — 1 sentence}

{Explanation — 2–3 sentences max, plain language}

{Resolution — numbered steps or clear action}

{Closing — offer further help}

Warm regards,
{Agent Name}
{Team Name}

---

**Quality Check**
- [ ] Empathy shown before solution
- [ ] No blame or defensiveness
- [ ] Resolution is specific, not vague
- [ ] No jargon or internal terminology
- [ ] Tone matches customer's emotional state
- [ ] SLA breach acknowledged if applicable

## Rules
- Never promise outcomes you cannot guarantee
- Never share internal policies, pricing structures, or system details
- Always personalise — no pure copy-paste templates
- For legal threats or regulatory complaints: flag for human escalation immediately
- Refund decisions must follow company policy — do not commit without authority
- For social media responses: keep under 280 chars for Twitter/X, professional for LinkedIn

## References
- Tone calibration guide: read references/tone_guide.md
- Response templates by issue type: read references/response_templates.md
