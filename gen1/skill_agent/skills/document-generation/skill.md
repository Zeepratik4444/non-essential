---
name: document-generation
description: >
  Generate professional documents in multiple formats: PDF reports,
  Word documents (DOCX), PowerPoint presentations (PPTX), and Excel
  spreadsheets (XLSX). Use when user needs formatted business documents,
  reports, presentations, data exports, or templates with proper styling.
triggers:
  - "create a PDF"
  - "generate report"
  - "word document"
  - "powerpoint presentation"
  - "excel spreadsheet"
  - "export to PDF"
  - "generate slides"
  - "create document"
  - "format as DOCX"
---

# Document Generation

## When to Use
- Creating PDF reports with charts, tables, and branding
- Generating Word documents (DOCX) with structured content
- Building PowerPoint presentations (PPTX) with slides
- Exporting data to Excel (XLSX) with formatting and formulas
- Converting structured data into professional documents
- Creating templates or boilerplates

## Protocol
1. Identify the document type (PDF, DOCX, PPTX, XLSX)
2. Identify the content structure (report, presentation, data export, template)
3. Load references/format_standards.md for formatting requirements
4. Generate content following the document type's best practices
5. Return code that produces the document + usage instructions

## Document Type Decision Tree
| User Need | Format | Library |
|-----------|--------|---------|
| Business report with charts/tables | PDF | ReportLab or WeasyPrint (HTML→PDF) |
| Editable text document | DOCX | python-docx |
| Slide presentation | PPTX | python-pptx |
| Data export with formulas | XLSX | openpyxl or xlsxwriter |
| Invoice, receipt, form | PDF | ReportLab or Weasyprint |
| Multi-page narrative report | DOCX or PDF | python-docx or WeasyPrint |

## Python Libraries by Format
```python
# PDF
from reportlab.lib.pagesizes import A4, letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, Image
from reportlab.lib.styles import getSampleStyleSheet
# OR for HTML-based PDF
from weasyprint import HTML

# DOCX
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

# PPTX
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN

# XLSX
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border
from openpyxl.chart import BarChart, LineChart, PieChart
```


## PDF Report Template (ReportLab)

```python
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib import colors

def generate_pdf_report(filename: str, title: str, data: dict):
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    # Title
    story.append(Paragraph(title, styles['Title']))
    story.append(Spacer(1, 0.3*inch))

    # Summary section
    story.append(Paragraph("Executive Summary", styles['Heading1']))
    story.append(Paragraph(data['summary'], styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))

    # Data table
    story.append(Paragraph("Key Metrics", styles['Heading1']))
    table_data = [['Metric', 'Value', 'Change']] + data['metrics']
    table = Table(table_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    story.append(table)

    doc.build(story)
    return filename
```


## DOCX Document Template (python-docx)

```python
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def generate_word_document(filename: str, content: dict):
    doc = Document()

    # Title
    title = doc.add_heading(content['title'], level=0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Metadata
    doc.add_paragraph(f"Date: {content['date']}")
    doc.add_paragraph(f"Author: {content['author']}")
    doc.add_paragraph()  # blank line

    # Sections
    for section in content['sections']:
        doc.add_heading(section['heading'], level=1)
        for para in section['paragraphs']:
            p = doc.add_paragraph(para)
            p.style = 'BodyText'

        # Add table if present
        if 'table' in section:
            table = doc.add_table(rows=1, cols=len(section['table']['headers']))
            table.style = 'Light Grid Accent 1'
            
            # Header row
            hdr_cells = table.rows.cells
            for i, header in enumerate(section['table']['headers']):
                hdr_cells[i].text = header
            
            # Data rows
            for row_data in section['table']['rows']:
                row_cells = table.add_row().cells
                for i, cell_data in enumerate(row_data):
                    row_cells[i].text = str(cell_data)

    # Footer
    section = doc.sections[0]
    footer = section.footer
    footer.paragraphs[0].text = f"{content['footer_text']}\t\tPage "

    doc.save(filename)
    return filename
```


## PPTX Presentation Template (python-pptx)

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN

def generate_presentation(filename: str, content: dict):
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)

    # Title slide
    title_slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(title_slide_layout)
    title = slide.shapes.title
    subtitle = slide.placeholders[1]
    title.text = content['title']
    subtitle.text = f"{content['subtitle']}\n{content['date']}"

    # Content slides
    for slide_content in content['slides']:
        bullet_slide_layout = prs.slide_layouts[1]  # Title and Content
        slide = prs.slides.add_slide(bullet_slide_layout)
        
        # Title
        title = slide.shapes.title
        title.text = slide_content['title']
        
        # Body
        body = slide.placeholders[1]
        tf = body.text_frame
        
        for bullet_point in slide_content['bullets']:
            p = tf.add_paragraph()
            p.text = bullet_point
            p.level = 0
            p.font.size = Pt(18)

        # Add chart if present
        if 'chart_data' in slide_content:
            # Chart implementation (BarChart, LineChart, etc.)
            pass

    # Closing slide
    blank_slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_slide_layout)
    left = top = Inches(2)
    width = height = Inches(6)
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.text = "Thank You"
    p = tf.paragraphs[0]
    p.font.size = Pt(48)
    p.alignment = PP_ALIGN.CENTER

    prs.save(filename)
    return filename
```


## XLSX Spreadsheet Template (openpyxl)

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import BarChart, Reference

def generate_excel_report(filename: str, data: dict):
    wb = Workbook()
    ws = wb.active
    ws.title = data['sheet_name']

    # Header styling
    header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
    header_font = Font(color="FFFFFF", bold=True, size=12)
    border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )

    # Write headers
    for col_num, header in enumerate(data['headers'], 1):
        cell = ws.cell(row=1, column=col_num)
        cell.value = header
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal='center', vertical='center')
        cell.border = border

    # Write data rows
    for row_num, row_data in enumerate(data['rows'], 2):
        for col_num, value in enumerate(row_data, 1):
            cell = ws.cell(row=row_num, column=col_num)
            cell.value = value
            cell.border = border
            
            # Format numbers
            if isinstance(value, (int, float)) and col_num > 1:
                cell.number_format = '#,##0.00'

    # Auto-adjust column widths
    for column in ws.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            if cell.value:
                max_length = max(max_length, len(str(cell.value)))
        ws.column_dimensions[column_letter].width = max_length + 2

    # Add chart if data supports it
    if data.get('add_chart'):
        chart = BarChart()
        chart.title = data['chart_title']
        chart.x_axis.title = data['x_axis']
        chart.y_axis.title = data['y_axis']
        
        data_ref = Reference(ws, min_col=2, min_row=1, max_row=len(data['rows'])+1)
        cats = Reference(ws, min_col=1, min_row=2, max_row=len(data['rows'])+1)
        chart.add_data(data_ref, titles_from_data=True)
        chart.set_categories(cats)
        
        ws.add_chart(chart, "E2")

    # Add formulas for totals
    if data.get('add_totals'):
        last_row = len(data['rows']) + 2
        ws.cell(row=last_row, column=1).value = "TOTAL"
        ws.cell(row=last_row, column=1).font = Font(bold=True)
        for col in range(2, len(data['headers']) + 1):
            cell = ws.cell(row=last_row, column=col)
            cell.value = f"=SUM({chr(64+col)}2:{chr(64+col)}{last_row-1})"
            cell.font = Font(bold=True)
            cell.border = border

    wb.save(filename)
    return filename
```


## Output Format

### Document Generation Task

**Format**: {PDF | DOCX | PPTX | XLSX}
**Purpose**: {report | presentation | data export | template}

#### Generated Code

```python
{complete working code to generate the document}
```


#### Usage Example

```python
# Example data structure
data = {
    "title": "Q4 2025 Sales Report",
    "date": "2026-02-18",
    ...
}

# Generate document
filename = generate_{format}(
    filename="output.{ext}",
    content=data
)
print(f"Document created: {filename}")
```


#### Required Dependencies

```bash
pip install reportlab weasyprint python-docx python-pptx openpyxl
```


#### Sample Output Preview

{description of what the generated document will look like}

## Best Practices by Format

### PDF Reports

- Use A4 or Letter page size consistently
- Include page numbers in footer
- Add company logo/branding in header
- Use tables for structured data, not text layouts
- Generate table of contents for reports > 10 pages
- Consider WeasyPrint for complex HTML→PDF conversions


### DOCX Documents

- Use built-in styles (Heading 1, BodyText) for consistency
- Add table of contents with `doc.add_paragraph('TOC', 'TOC Heading')`
- Include page breaks between major sections
- Set margins: `section.top_margin = Inches(1)`
- Use track changes for review workflows when needed


### PPTX Presentations

- Maximum 6 bullet points per slide
- Use 24pt+ font for body text
- Include slide numbers
- Maintain consistent layout across slides
- Add speaker notes: `slide.notes_slide.notes_text_frame.text = "..."`
- Limit animations — focus on content clarity


### XLSX Spreadsheets

- Freeze header row: `ws.freeze_panes = 'A2'`
- Use data validation for dropdowns
- Protect sheets with sensitive formulas
- Name ranges for complex formulas
- Use conditional formatting for highlighting
- Add filters to header row: `ws.auto_filter.ref = ws.dimensions`


## Rules

- Never hardcode file paths — accept filename as parameter
- Always handle file write errors with try/except
- Return the filename after successful creation
- For large datasets (> 10k rows), stream write to avoid memory issues
- Include proper metadata (author, title, creation date)
- Test generated files open correctly in target applications
- Sanitise user input before embedding in documents (XSS in HTML→PDF)


## References

- Formatting standards by document type: read references/format_standards.md
- Chart and visualization guide: read references/chart_guide.md
- Brand and style template specs: read references/brand_guidelines.md
