# Document Format Standards

## PDF Standards
- **Page Size**: A4 (210×297mm) for international, Letter (8.5×11in) for US
- **Margins**: 1 inch (2.54cm) on all sides, 0.75 inch minimum
- **Fonts**: Use standard fonts (Helvetica, Times-Roman) or embed custom fonts
- **Resolution**: Images at 300 DPI minimum for print-quality
- **Color Space**: RGB for screen, CMYK for print
- **Accessibility**: Tag PDFs with structure for screen readers when possible

### PDF Report Structure
1. Cover page (title, date, author, logo)
2. Table of contents (for > 5 pages)
3. Executive summary (1 page max)
4. Body sections with headings
5. Appendices (raw data, methodology)
6. Footer with page numbers and document title

---

## DOCX Standards
- **Page Setup**: A4 or Letter, Portrait orientation
- **Margins**: Normal (1" all sides) or Narrow (0.5" all sides)
- **Font**: Arial 11pt or Calibri 11pt for body, larger for headings
- **Line Spacing**: 1.15 or 1.5 for readability
- **Paragraph Spacing**: 6pt after paragraphs, no spacing before

### DOCX Document Structure
- Use Heading 1, 2, 3 hierarchy — never manual bold for headings
- Table of Contents auto-generated from headings
- Page breaks between major sections (not multiple blank lines)
- Consistent table styling (Light Grid or Medium Shading)
- Alt text on all images for accessibility

---

## PPTX Standards
- **Slide Size**: Widescreen 16:9 (10×7.5in) or Standard 4:3 (10×7.5in)
- **Font Size**: Title 32-44pt, Body 18-24pt, Captions 14-16pt
- **Colors**: Use 3-5 colors max from brand palette
- **Bullet Points**: Max 6 per slide, max 7 words per bullet
- **Contrast**: Dark text on light background or vice versa (WCAG AA)

### PPTX Presentation Structure
1. Title slide (title, subtitle, date, presenter)
2. Agenda slide (optional, for long presentations)
3. Content slides (1 idea per slide)
4. Section dividers (visual break every 5-7 slides)
5. Summary/conclusion slide
6. Q&A or Thank You slide

### Slide Layout Best Practices
- Title at top, left-aligned or centered
- Content in left 60%, visual in right 40%
- White space is good — avoid crowding
- Consistent footer with slide numbers
- No paragraph text — only bullets or visuals

---

## XLSX Standards
- **Column Width**: Auto-fit or 10-15 characters default
- **Row Height**: 15-20pt for readability
- **Header Row**: Bold, background color, freeze panes
- **Data Types**: Numbers right-aligned, text left-aligned
- **Currency**: Always specify symbol ($, €, ₹) and 2 decimals

### XLSX Spreadsheet Structure
| Element | Format |
|---------|--------|
| Headers | Bold, background fill, centered, borders |
| Data rows | Alternating row colors for readability |
| Totals row | Bold, top border, SUM formulas |
| Numeric | Number format with thousands separator |
| Dates | ISO format (YYYY-MM-DD) or regional |
| Percentages | Percentage format with 1-2 decimals |

### Formula Best Practices
- Use named ranges for clarity: `=SUM(MonthlySales)` not `=SUM(B2:B50)`
- Lock absolute references with `$`: `=$B$1 * C2`
- Document complex formulas in adjacent comment cells
- Use `IFERROR()` to handle edge cases gracefully
- Avoid volatile functions (NOW, INDIRECT) in large sheets

---

## Chart Standards (All Formats)

### Bar Chart
- Use for comparing categories
- Horizontal bars for long labels, vertical for short
- Sort by value (descending) unless time series

### Line Chart
- Use for trends over time
- Always label axes with units
- Use different line styles if color-blind accessibility needed

### Pie Chart
- Use only for parts-of-whole (percentages summing to 100%)
- Max 5-7 slices — group "Other" if more
- Label slices with percentage + value

### Table vs Chart Decision
| Use Table | Use Chart |
|-----------|-----------|
| Exact values needed | Trends or comparisons matter |
| < 20 data points | > 20 data points |
| Lookup/reference use | Presentation/insight use |
