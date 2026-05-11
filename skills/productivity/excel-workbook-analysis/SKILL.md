---
name: excel-workbook-analysis
description: "Analyze uploaded Excel workbooks (.xlsx): inspect sheets, read specific worksheets, extract tables, totals, formulas/cached values, and produce Vietnamese business summaries. Includes workaround for openpyxl importing NumPy on incompatible CPUs."
---

# Excel Workbook Analysis

Use this skill when the user uploads or references an `.xlsx` file and asks to read a sheet, summarize rows/columns, verify totals, identify formula issues, or calculate ratios from workbook data.

## Workflow

1. **Locate the workbook path** from the user message or document metadata.
2. **Inspect workbook sheets and dimensions** using `openpyxl`.
3. Load two copies when formulas matter:
   - `data_only=False` to inspect formulas and headers.
   - `data_only=True` to read cached calculated values.
4. Print/inspect merged ranges and non-empty cells around the target sheet to understand header structure.
5. Identify the relevant columns by header text, not just by assumed column letters.
6. Extract rows under the relevant section, skipping section totals/headers unless requested.
7. For totals, verify workbook formulas against the extracted data; flag formula ranges that omit valid rows.
8. For ratios, calculate with Python rather than mental arithmetic. Format Vietnamese currency with dot thousand separators and percentages with comma decimals if replying in Vietnamese.

## Python pattern

```python
import sys
sys.modules['numpy'] = None  # prevents openpyxl from importing a broken NumPy build in Hermes env
from openpyxl import load_workbook

path = '/path/to/workbook.xlsx'
wb_formula = load_workbook(path, data_only=False)
wb_values = load_workbook(path, data_only=True)

wsf = wb_formula['SheetName']
wsv = wb_values['SheetName']

print(wb_formula.sheetnames)
print(wsf.max_row, wsf.max_column)
print(list(map(str, wsf.merged_cells.ranges)))

for r in range(1, wsf.max_row + 1):
    vals = []
    for c in range(1, wsf.max_column + 1):
        v = wsv.cell(r, c).value
        f = wsf.cell(r, c).value
        if v is not None or f is not None:
            vals.append((c, v, f if isinstance(f, str) and f.startswith('=') else None))
    if vals:
        print(r, vals)
```

## Pitfalls / Lessons Learned

- In the Hermes Python environment, importing `openpyxl` may fail because it tries to import a NumPy wheel requiring unsupported `X86_V2` CPU optimizations. Workaround: set `sys.modules['numpy'] = None` before `from openpyxl import load_workbook`.
- Do not trust visible totals blindly. In the Lite On payment workbook, the total cell for advance requests used `SUM(U7:U13)` and omitted later valid rows (`U14`, `U16`), so the workbook total understated the extracted total.
- A cell can contain text like `Bỏ` in an otherwise numeric column; treat only positive numeric values as monetary requests unless the user says otherwise.
- Use `data_only=True` for calculated displayed values, but use `data_only=False` to catch formulas/range errors.

## Vietnamese business summary conventions

- Address the user as “Anh” if matching Boss profile.
- Present tables with columns: STT, Đội/Nhà thầu, key monetary columns, tỷ lệ.
- Money: `2.000.000.000` (no currency symbol unless needed).
- Percent: `39,43%` in final Vietnamese prose.
- Explicitly call out any formula discrepancy or excluded rows.
