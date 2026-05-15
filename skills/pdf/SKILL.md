---
name: pdf
description: Use this skill whenever the user wants to do anything with PDF files. This includes reading or extracting text/tables from PDFs, combining or merging multiple PDFs into one, splitting PDFs apart, rotating pages, adding watermarks, creating new PDFs, filling PDF forms, encrypting/decrypting PDFs, extracting images, and OCR on scanned PDFs to make them searchable. If the user mentions a .pdf file or asks to produce one, use this skill.
license: Proprietary. LICENSE.txt has complete terms
---

# PDF Processing Guide

## Overview

This guide covers essential PDF processing operations using Python libraries and command-line tools. For advanced features, JavaScript libraries, and detailed examples, see REFERENCE.md. If you need to fill out a PDF form, read FORMS.md and follow its instructions.

## Quick Start

```python
from pypdf import PdfReader, PdfWriter

# Read a PDF
reader = PdfReader("document.pdf")
print(f"Pages: {len(reader.pages)}")

# Extract text
text = ""
for page in reader.pages:
    text += page.extract_text()
```

## Python Libraries

### pypdf - Basic Operations

#### Merge PDFs
```python
from pypdf import PdfWriter, PdfReader

writer = PdfWriter()
for pdf_file in ["doc1.pdf", "doc2.pdf", "doc3.pdf"]:
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        writer.add_page(page)

with open("merged.pdf", "wb") as output:
    writer.write(output)
```

#### Split PDF
```python
reader = PdfReader("input.pdf")
for i, page in enumerate(reader.pages):
    writer = PdfWriter()
    writer.add_page(page)
    with open(f"page_{i+1}.pdf", "wb") as output:
        writer.write(output)
```

#### Extract Metadata
```python
reader = PdfReader("document.pdf")
meta = reader.metadata
print(f"Title: {meta.title}")
print(f"Author: {meta.author}")
print(f"Subject: {meta.subject}")
print(f"Creator: {meta.creator}")
```

#### Rotate Pages
```python
reader = PdfReader("input.pdf")
writer = PdfWriter()

page = reader.pages[0]
page.rotate(90)  # Rotate 90 degrees clockwise
writer.add_page(page)

with open("rotated.pdf", "wb") as output:
    writer.write(output)
```

### pdfplumber - Text and Table Extraction

#### Extract Text with Layout
```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        print(text)
```

#### Extract Tables
```python
with pdfplumber.open("document.pdf") as pdf:
    for i, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        for j, table in enumerate(tables):
            print(f"Table {j+1} on page {i+1}:")
            for row in table:
                print(row)
```

#### Advanced Table Extraction
```python
import pandas as pd

with pdfplumber.open("document.pdf") as pdf:
    all_tables = []
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            if table:  # Check if table is not empty
                df = pd.DataFrame(table[1:], columns=table[0])
                all_tables.append(df)

# Combine all tables
if all_tables:
    combined_df = pd.concat(all_tables, ignore_index=True)
    combined_df.to_excel("extracted_tables.xlsx", index=False)
```

### reportlab - Create PDFs

⚠️ PITFALL: As of reportlab >= 4.5.0 `TableOfContents` is imported from `reportlab.platypus.tableofcontents` NOT directly from platypus. Previous imports will fail.

#### Basic PDF Creation
```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

c = canvas.Canvas("hello.pdf", pagesize=letter)
width, height = letter

# Add text
c.drawString(100, height - 100, "Hello World!")
c.drawString(100, height - 120, "This is a PDF created with reportlab")

# Add a line
c.line(100, height - 140, 400, height - 140)

# Save
c.save()
```

#### Create PDF with Multiple Pages
```python
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("report.pdf", pagesize=letter)
styles = getSampleStyleSheet()
story = []

# Add content
title = Paragraph("Report Title", styles['Title'])
story.append(title)
story.append(Spacer(1, 12))

body = Paragraph("This is the body of the report. " * 20, styles['Normal'])
story.append(body)
story.append(PageBreak())

# Page 2
story.append(Paragraph("Page 2", styles['Heading1']))
story.append(Paragraph("Content for page 2", styles['Normal']))

# Build PDF
doc.build(story)
```

#### Subscripts and Superscripts

**IMPORTANT**: Never use Unicode subscript/superscript characters (₀₁₂₃₄₅₆₇₈₉, ⁰¹²³⁴⁵⁶⁷⁸⁹) in ReportLab PDFs. The built-in fonts do not include these glyphs, causing them to render as solid black boxes.

Instead, use ReportLab's XML markup tags in Paragraph objects:
```python
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet

styles = getSampleStyleSheet()

# Subscripts: use <sub> tag
chemical = Paragraph("H<sub>2</sub>O", styles['Normal'])

# Superscripts: use <super> tag
squared = Paragraph("x<super>2</super> + y<super>2</super>", styles['Normal'])
```

For canvas-drawn text (not Paragraph objects), manually adjust font the size and position rather than using Unicode subscripts/superscripts.

## Command-Line Tools

### pdftotext (poppler-utils)
```bash
# Extract text
pdftotext input.pdf output.txt

# Extract text preserving layout
pdftotext -layout input.pdf output.txt

# Extract specific pages
pdftotext -f 1 -l 5 input.pdf output.txt  # Pages 1-5
```

### qpdf
```bash
# Merge PDFs
qpdf --empty --pages file1.pdf file2.pdf -- merged.pdf

# Split pages
qpdf input.pdf --pages . 1-5 -- pages1-5.pdf
qpdf input.pdf --pages . 6-10 -- pages6-10.pdf

# Rotate pages
qpdf input.pdf output.pdf --rotate=+90:1  # Rotate page 1 by 90 degrees

# Remove password
qpdf --password=mypassword --decrypt encrypted.pdf decrypted.pdf
```

### pdftk (if available)
```bash
# Merge
pdftk file1.pdf file2.pdf cat output merged.pdf

# Split
pdftk input.pdf burst

# Rotate
pdftk input.pdf rotate 1east output rotated.pdf
```

## Common Tasks

### Extracting docs from Git repositories
⚠️ PITFALL: Almost all international documentation repositories use **full locale codes** not 2 letter language codes. Example: `vi-vn/` not `vi/`, `zh-cn/` not `zh/`, `en-us/` not `en/`. Always first list the actual directory names with `ls docs/` before trying to load content.

### Extract Text from Scanned PDFs
```python
# Requires: pip install pytesseract pdf2image
import pytesseract
from pdf2image import convert_from_path

# Convert PDF to images
images = convert_from_path('scanned.pdf')

# OCR each page
text = ""
for i, image in enumerate(images):
    text += f"Page {i+1}:\n"
    text += pytesseract.image_to_string(image)
    text += "\n\n"

print(text)
```

### Scanned/table PDFs when text extraction returns empty

If `pypdf`, `pdfplumber`, or `fitz.get_text()` returns little/empty text, treat the PDF as scanned/rotated image pages and inspect visually before concluding data is missing:

1. Check metadata/pages/rotation:
   ```bash
   pdfinfo input.pdf | head -30
   ```
2. Render pages to images with Poppler:
   ```bash
   mkdir -p /tmp/pdf_pages
   pdftoppm -png -r 200 input.pdf /tmp/pdf_pages/page
   # outputs /tmp/pdf_pages/page-1.png, page-2.png, ...
   ```
3. Use image/vision OCR for key pages, prompting specifically to read every line and table fields. For Vietnamese procurement tables, ask for: `STT, tên vật tư, model/mã hiệu/quy cách, nhãn hiệu/hãng, xuất xứ`.
4. When comparing a spreadsheet against a scanned PDF, match by model first, then brand/origin, because PDF row numbers may differ from the request sheet.

Pitfalls:
- A scanned PDF can have valid pages but zero extractable text; do not report “not found” until rendering pages or OCR/vision inspection is attempted.
- Some PDFs are rotated (e.g. `Page rot: 270`); `pdftoppm` still renders usable page images, while text extractors may fail.
- For table continuation pages, columns like brand/origin may appear only on the first visible row; inspect surrounding pages if a row is cut off.

### Add Watermark
```python
from pypdf import PdfReader, PdfWriter

# Create watermark (or load existing)
watermark = PdfReader("watermark.pdf").pages[0]

# Apply to all pages
reader = PdfReader("document.pdf")
writer = PdfWriter()

for page in reader.pages:
    page.merge_page(watermark)
    writer.add_page(page)

with open("watermarked.pdf", "wb") as output:
    writer.write(output)
```

### Extract Images
```bash
# Using pdfimages (poppler-utils)
pdfimages -j input.pdf output_prefix

# This extracts all images as output_prefix-000.jpg, output_prefix-001.jpg, etc.
```

### Password Protection
```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("input.pdf")
writer = PdfWriter()

for page in reader.pages:
    writer.add_page(page)

# Add password
writer.encrypt("userpassword", "ownerpassword")

with open("encrypted.pdf", "wb") as output:
    writer.write(output)
```

## Quick Reference

| Task | Best Tool | Command/Code |
|------|-----------|--------------|
| Merge PDFs | pypdf | `writer.add_page(page)` |
| Split PDFs | pypdf | One page per file |
| Extract text | pdfplumber | `page.extract_text()` |
| Extract tables | pdfplumber | `page.extract_tables()` |
| Create PDFs | reportlab | Canvas or Platypus |
| Command line merge | qpdf | `qpdf --empty --pages ...` |
| OCR scanned PDFs | pytesseract | Convert to image first |
| Fill PDF forms | pdf-lib or pypdf (see FORMS.md) | See FORMS.md |

## Google Drive PDF Downloads (Public Links)

For public Google Drive PDFs, the standard `drive.google.com/file/d/ID/view` URL may show a viewer page, login prompt, or virus-scan warning. Extract the file ID and try direct unauthenticated download before using Google Drive API OAuth, especially when OAuth only has `drive.file` scope:

```bash
# Given: https://drive.google.com/file/d/FILE_ID/view
FILE_ID="..."
python3 - <<'PY'
import os, requests
fid=os.environ['FILE_ID']
for url in [
    f'https://drive.google.com/uc?export=download&id={fid}',
    f'https://drive.usercontent.google.com/download?id={fid}&export=download&confirm=t',
]:
    r=requests.get(url, headers={'User-Agent':'Mozilla/5.0'}, allow_redirects=True, timeout=60)
    print(r.status_code, r.headers.get('content-type'), len(r.content), r.url)
    if r.status_code == 200 and 'html' not in (r.headers.get('content-type') or ''):
        open('/tmp/drive_pdf_download','wb').write(r.content)
        break
PY
file /tmp/drive_pdf_download
```

For very large files (>20MB), the `confirm=t` parameter bypasses the virus-scan interstitial. If that fails, try `confirm=t&uuid=random_string`.

⚠️ Exact-file pitfall: If the user gives a specific Drive file ID, do not search Drive by keywords and summarize a similar-looking file as a substitute. Verify the downloaded file corresponds to the exact ID, or clearly state that the exact file is inaccessible.

## Large Vietnamese / CJK Document Search

For multi-hundred-page Vietnamese government documents (quy hoạch, dự án, etc.):

1. **Use pymupdf (fitz)** — handles Vietnamese text extraction far better than pypdf for large files:
   ```python
   import fitz
   doc = fitz.open("file.pdf")
   for i, page in enumerate(doc):
       text = page.get_text()
   ```

2. **Multi-pass keyword search** — Vietnamese text requires careful matching:
   - Pass 1: Broad regex search for `(?i)huyện\s+thanh\s+oai` (district names with flexible whitespace)
   - Pass 2: Verify context — confirm the match is actually in the target district, not just referenced
   - Pass 3: Extract full project entries around confirmed matches

3. **Vietnamese-specific pitfalls:**
   - District names can appear as references in other districts' entries (e.g., "huyện Thanh Oai" mentioned in an Ứng Hòa project). Always verify the project's actual location via the "Đơn vị đăng ký" (registering organization) field.
   - Commune names may overlap with non-geographic names (e.g., "Bình Minh" can be a housing project name, not xã Bình Minh). Verify with context.
   - Search for `UBND xã <tên>` or `UBND huyện <tên>` for authoritative matches.

### Module Installation Pitfall

`pypdf` must be importable as `fitz`. On Hermes, the venv Python (`/root/.hermes/hermes-agent/venv/bin/python3`) is the `python3` in PATH. Install with:
```bash
python3 -m pip install pymupdf
```
**Do NOT use `pip install pymupdf`** (may install to system Python, invisible to the venv). The `execute_code` sandbox may not share the same environment as `python3 -c` — if `import fitz` fails in sandbox, use `terminal` with `python3 -c` instead.

### VitePress / Docsify Markdown Cleaning
When generating PDFs from documentation repositories, use this cleaning pattern before rendering:
```python
content = re.sub(r'<[^>]+>', '', content)
content = re.sub(r':::.*', '', content)
content = re.sub(r'^---.*?---', '', content, flags=re.DOTALL)
```
This removes frontmatter, custom markdown directives, and component tags which break PDF rendering.

## Next Steps

- For advanced pypdfium2 usage, see REFERENCE.md
- For JavaScript libraries (pdf-lib), see REFERENCE.md
- If you need to fill out a PDF form, follow the instructions in FORMS.md
- For troubleshooting guides, see REFERENCE.md
