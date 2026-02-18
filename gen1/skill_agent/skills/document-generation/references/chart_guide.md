# Chart and Visualization Guide

## ReportLab Charts (PDF)
```python
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.charts.piecharts import Pie

# Bar Chart
drawing = Drawing(400, 200)
bc = VerticalBarChart()
bc.x = 50
bc.y = 50
bc.height = 125
bc.width = 300
bc.data = []
bc.categoryAxis.categoryNames = ['Q1', 'Q2', 'Q3', 'Q4']
bc.valueAxis.valueMin = 0
bc.valueAxis.valueMax = 250
drawing.add(bc)
```


## openpyxl Charts (XLSX)

```python
from openpyxl.chart import BarChart, LineChart, PieChart, Reference

# Bar Chart
chart = BarChart()
chart.title = "Sales by Quarter"
chart.x_axis.title = "Quarter"
chart.y_axis.title = "Revenue ($)"
data = Reference(ws, min_col=2, min_row=1, max_row=5)
cats = Reference(ws, min_col=1, min_row=2, max_row=5)
chart.add_data(data, titles_from_data=True)
chart.set_categories(cats)
ws.add_chart(chart, "E2")

# Line Chart
chart = LineChart()
chart.title = "Monthly Trends"
chart.style = 12  # Use built-in style
# ... same Reference pattern

# Pie Chart
chart = PieChart()
chart.title = "Market Share"
data = Reference(ws, min_col=2, min_row=1, max_row=6)
labels = Reference(ws, min_col=1, min_row=2, max_row=6)
chart.add_data(data, titles_from_data=True)
chart.set_categories(labels)
```


## Chart Color Palettes

```python
# Professional
COLORS = {
    'primary': '#2E86AB',    # Blue
    'secondary': '#A23B72',  # Purple
    'accent': '#F18F01',     # Orange
    'success': '#06A77D',    # Green
    'danger': '#C73E1D',     # Red
    'neutral': '#6C757D',    # Gray
}

# Corporate
COLORS = {
    'navy': '#003F5C',
    'teal': '#2F4B7C',
    'purple': '#665191',
    'pink': '#A05195',
    'orange': '#D45087',
    'coral': '#F95D6A',
    'yellow': '#FF7C43',
    'gold': '#FFA600',
}
```
