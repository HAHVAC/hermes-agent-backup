# Google Drive Office `.xlsx` links: edit workflow when Sheets API/openpyxl fail

Use this when a Google Docs/Sheets URL points to an Office Excel file rather than a native Google Sheet.

## Symptoms

- Google Sheets API metadata/read fails with:
  - `This operation is not supported for this document. The document must not be an Office file.`
- Drive API may return `404 File not found` if the file is shared publicly but not accessible to the authenticated token.
- `openpyxl` may be unusable in this Hermes environment when NumPy import fails:
  - `RuntimeError: NumPy was built with baseline optimizations: (X86_V2) but your machine doesn't support: (X86_V2)`

## Reliable workflow

1. Export/download the Office workbook directly from the docs URL:

```python
import requests
sid = "SPREADSHEET_OR_FILE_ID"
url = f"https://docs.google.com/spreadsheets/d/{sid}/export?format=xlsx"
r = requests.get(url, timeout=30)
r.raise_for_status()
open('/tmp/input.xlsx', 'wb').write(r.content)
```

2. If `openpyxl` works, edit normally and recalc with the xlsx skill's `scripts/recalc.py`.

3. If `openpyxl` fails because of NumPy, edit the `.xlsx` as a ZIP of XML files using only the Python standard library:
   - Read workbook/sheet mapping from `xl/workbook.xml` and `xl/_rels/workbook.xml.rels`.
   - Resolve strings from `xl/sharedStrings.xml`.
   - Modify `xl/worksheets/sheet*.xml` directly.
   - Add formulas as `<f>FORMULA</f>` cells.
   - Preserve existing cell styles by copying the `s` attribute from nearby/header cells.
   - Update `<dimension ref="A1:...">` after adding columns.

4. Recalculate formulas with LibreOffice when `recalc.py` cannot run:

```bash
mkdir -p /tmp/lo_out
libreoffice --headless --convert-to xlsx --outdir /tmp/lo_out /tmp/edited.xlsx
```

5. Verify formulas/errors by scanning the resulting workbook XML:
   - Count cells containing `<f>`.
   - Scan `<v>` values for Excel error strings beginning with `#` such as `#REF!`, `#DIV/0!`, `#VALUE!`, `#NAME?`.

## Example formulas for price/profit workbooks

When adding comparison columns:

- `Tỷ lệ lợi nhuận`: `IFERROR((Đơn giá vật tư - Giá vốn vật liệu) / Giá vốn vật liệu, "")`
- `Thành tiền`: `IFERROR(Khối lượng * Đơn giá vật tư, "")`
- `Đơn giá thị trường`: leave blank for user input unless a market-price source is provided.

Always detect columns by header text per sheet because the same field may be in different columns across sheets.