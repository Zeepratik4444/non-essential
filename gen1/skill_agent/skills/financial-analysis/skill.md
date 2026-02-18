---
name: financial-analysis
description: >
  Analyse financial statements, stock data, market trends, valuations,
  and investment metrics. Use when user asks about company financials,
  stock performance, P&L analysis, ratios, or investment decisions.
triggers:
  - "analyse financials"
  - "stock performance"
  - "valuation"
  - "revenue growth"
  - "P&L"
  - "investment analysis"
  - "financial ratios"
---

# Financial Analysis

## When to Use
- Analysing company income statements, balance sheets, cash flow
- Stock price performance and technical indicators
- Investment thesis building
- Financial ratio benchmarking
- Revenue/cost trend analysis

## Protocol
1. Identify the type of analysis requested (fundamental, technical, ratio)
2. Load references/financial_ratios.md for formula reference
3. Gather required data via tools (API or user-provided)
4. Run calculations step by step — show all workings
5. Benchmark against industry averages where possible
6. Produce structured report

## Key Ratios (Quick Reference)
| Ratio                | Formula                          | Healthy Range     |
|----------------------|----------------------------------|-------------------|
| P/E Ratio            | Price / EPS                      | 15–25 (varies)    |
| Debt-to-Equity       | Total Debt / Equity              | < 2.0             |
| Current Ratio        | Current Assets / Current Liab.   | 1.5–3.0           |
| Gross Margin         | (Revenue - COGS) / Revenue × 100 | > 40% (SaaS)      |
| ROE                  | Net Income / Shareholder Equity  | > 15%             |
| Free Cash Flow Yield | FCF / Market Cap × 100           | > 5% attractive   |
| EV/EBITDA            | Enterprise Value / EBITDA        | 10–15x (varies)   |

## Output Format
### Financial Analysis: {Company / Asset}

**Analysis Type**: {Fundamental | Technical | Ratio}
**Period**: {date range}

#### Financials Summary
{key figures table}

#### Ratio Analysis
{ratios with values, benchmarks, and interpretation}

#### Trend Analysis
{YoY or QoQ growth rates}

#### Investment Assessment
**Strengths**: {list}
**Risks**: {list}
**Verdict**: {Buy / Hold / Sell with reasoning}

## Rules
- Never fabricate financial figures — only use data from tools or user input
- Always show the formula and inputs for every ratio calculated
- Clearly state the data source and date
- Flag if data is older than 6 months
- Distinguish between GAAP and non-GAAP metrics when relevant

## References
- Full ratio formulas and benchmarks: read references/financial_ratios.md
- Valuation models (DCF, Comps): read references/valuation_models.md
