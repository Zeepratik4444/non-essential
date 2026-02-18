---
name: legal-document-review
description: >
  Review, summarise, and identify risks in legal documents including
  contracts, NDAs, terms of service, employment agreements, and policies.
  Use when the user needs to understand legal obligations, spot red flags,
  or extract key clauses from a document.
triggers:
  - "review this contract"
  - "check this NDA"
  - "legal risks"
  - "what does this clause mean"
  - "summarise this agreement"
  - "red flags in this document"
---

# Legal Document Review

## When to Use
- Reviewing contracts, NDAs, SaaS agreements, employment terms
- Identifying unfavourable or unusual clauses
- Summarising long legal documents for non-lawyers
- Extracting specific obligations, deadlines, or penalties

## ⚠️ Disclaimer Protocol
ALWAYS include this disclaimer at the start of every output:
> ⚠️ This is an AI-assisted review for informational purposes only.
> It does not constitute legal advice. Consult a qualified lawyer
> before making any legal decisions.

## Protocol
1. Load references/clause_library.md to identify clause types
2. Read the document section by section
3. Extract and categorise all key clauses
4. Flag red flags using the risk matrix (references/risk_matrix.md)
5. Produce structured summary report

## Clause Categories to Always Check
- **Parties**: Who is bound, correct legal entities named
- **Term & Termination**: Duration, notice periods, auto-renewal
- **Payment**: Amounts, due dates, late fees, currency
- **IP Ownership**: Who owns work product, licensing terms
- **Confidentiality**: Scope, duration, exclusions
- **Liability**: Caps, exclusions, indemnification
- **Governing Law**: Which jurisdiction applies
- **Dispute Resolution**: Arbitration vs. litigation, venue
- **Non-Compete / Non-Solicit**: Scope, duration, geography
- **Force Majeure**: What events are covered

## Risk Flags
🔴 **High Risk** — Requires immediate legal attention
🟡 **Medium Risk** — Unfavourable but negotiable
🟢 **Low Risk** — Standard clause, acceptable

## Output Format
### Legal Document Review: {document title}

> ⚠️ AI-assisted review only. Not legal advice.

**Document Type**: {NDA | Contract | ToS | Employment | Other}
**Parties**: {Party A} ↔ {Party B}
**Effective Date**: {date}
**Governed by**: {jurisdiction}

#### Key Clauses Summary
| Clause         | Summary                        | Risk     |
|----------------|--------------------------------|----------|
| Term           | 2 years, auto-renews 30d notice| 🟡       |
| IP Ownership   | All work product owned by client| 🔴      |
| Liability Cap  | Capped at 1× annual fees       | 🟢       |

#### 🔴 Red Flags
1. **{Clause Name}**: {what it says} → {why it's risky} → {suggested alternative}

#### 🟡 Points to Negotiate
1. **{Clause Name}**: {concern} → {suggested revision}

#### ✅ Standard / Acceptable Clauses
{list of clauses that are normal and fair}

#### Recommended Actions
1. {specific action before signing}

## Rules
- Never give a definitive legal opinion — always qualify with disclaimer
- Quote the exact clause text when flagging risks
- Do not skip any clause category from the checklist
- If document is in a non-English language, note it and request translation

## References
- Common clause types and meanings: read references/clause_library.md
- Risk assessment matrix: read references/risk_matrix.md
