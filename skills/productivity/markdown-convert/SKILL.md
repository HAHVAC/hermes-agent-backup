---
name: markdown-convert
description: Convert any document (Google Drive, URL, local file, chat attachment) to clean, well-formatted Markdown using markitdown. Always formats output — joins paragraphs, fixes headings, tables, quotes, bullets, code blocks. Saves to /root/Downloads/markdown/ and sends file in chat.
version: 1.0.0
triggers:
  - "chuyển đổi sang markdown"
  - "convert to markdown"
  - "convert to md"
  - "markitdown"
  - "file này sang md"
  - "sang markdown"
tools:
  - terminal
  - file
---

# Markdown Convert

Convert any document to clean, well-formatted Markdown in one step.

## Pipeline

```
Input → Detect source → Download → Convert (markitdown) → Format → Ask filename → Save + Send
```

## Step 1: Detect Input Source

| Source Type | Detection | Action |
|---|---|---|
| Google Drive link | `drive.google.com` in URL | Use `gdown` to download |
| Direct URL (PDF/web) | Starts with `http://` or `https://` | `curl -sL -o` to download |
| Local file | Path exists on disk | Use directly |
| Chat attachment | Gateway provides path | Read from gateway path |

## Step 2: Download File (if needed)

### Google Drive
```bash
# Extract file ID from URL
FILE_ID="extracted_from_url"

# Get original filename
ORIG_NAME=$(curl -sI -L "https://drive.google.com/uc?export=download&id=${FILE_ID}" | grep -i "content-disposition" | sed 's/.*filename="\(.*\)".*/\1/' | sed 's/\r//g')

# Download
pip install -q gdown
gdown "https://drive.google.com/uc?id=${FILE_ID}" -O "/tmp/mc_input_file"
```

### Direct URL
```bash
curl -sL -o /tmp/mc_input_file "${URL}"
# Get filename from content-disposition or URL path
```

### Determine original filename
- Google Drive: parse `content-disposition` header
- Direct URL: parse URL path or content-disposition
- Local file: use `basename`
- Remove original extension, append `.md`

## Step 3: Convert with markitdown

### Prerequisites
```bash
pip install -q markitdown gdown
```

### Convert
```bash
markitdown /path/to/input > /tmp/mc_raw.md
```

### Error checking
- If exit code ≠ 0 → report error with details, suggest alternatives
- If output is empty or < 50 chars → report "unable to extract content", suggest:
  - For PDFs: try `pymupdf` (python fitz)
  - For images: try OCR with `tesseract` or `pymupdf`
  - For scanned PDFs: try `marker-pdf` or `ocrmypdf`

## Step 4: Format Markdown (ALWAYS run)

This is the most critical step. The raw markitdown output has many artifacts that must be cleaned.

### 4a. Remove noise (all file types)
- Remove Python warning lines at top (e.g., `RequestsDependencyWarning`)
- Remove `\f` (form feed / `\x0c`) characters
- Remove excessive blank lines (max 2 consecutive)

### 4b. PDF-specific cleanup
- **Page headers**: Remove repeated book/document title lines (spaced-out text like `B Ộ   N Ã O   T H Ứ   H A I`)
  - Detection: strip all spaces → compare against repeated pattern
- **Page numbers**: Remove standalone lines that are just digits (1-N)
- **Paragraph joining**: PDF column layout breaks paragraphs across lines with blank lines between fragments
  - Identify "text lines" (not headings, bullets, quotes, code, etc.)
  - Join consecutive text lines (skipping blank lines between them) into single paragraphs
  - Do NOT join lines starting with: `#`, `` ` ``, `---`, `>`, `•`, `✦`, tree chars (`├│└`), quotes (`"`), attribution (`—`), numbered/bulleted lists
- **Spacing normalization**: Replace multiple consecutive spaces with single space (`re.sub(r' {2,}', ' ', text)`)

### 4c. Add markdown structure

**Headings** (detect and add proper `#` levels):
- Book/document title → `# Title`
- Parts (Phần/Part) → `# Phần X` (with `---` separator before)
- Chapters (Chương/Chapter) → `## Chương N: Title`
- Subsections (N.N) → `### N.N Title`
- Appendices (Phụ lục/Appendix) → `## Phụ lục X: Title`
- Known section headings (About, TOC, Introduction) → `##`

**Quotes**: Detect text in quotation marks with attribution lines starting with `—`
```markdown
> "Quoted text here"
>
> — Author Name, Source
```

**Bullets**: Convert `•` to `-`

**Code blocks**: Wrap directory trees, file paths, code snippets in triple backticks

**Callout boxes**: ALL CAPS text → `> **TEXT**`

**Tables**: If table data is detected (columns with repeated separators), reconstruct as proper markdown tables with `|` and `---|---` headers

**Separators**: Convert `✦ ✦ ✦` patterns to `---`

**Table of Contents**: If present, format as clean nested bullet list

### 4d. DOCX/PPTX cleanup
- Normalize headings (already mostly correct from markitdown)
- Fix table formatting
- Standardize bullet styles

### 4e. XLSX cleanup
- Preserve table structure
- Format header row
- Wrap in code block if too wide for markdown table

### 4f. Final cleanup
- Remove trailing whitespace per line
- Ensure max 2 consecutive blank lines
- Trim file start/end

### Format script location
A Python format script is available at `scripts/format_md.py` — use it for the heavy lifting of Step 4.

## Step 5: Ask User for Filename

**ALWAYS ask the user before saving.** Use the `clarify` tool:

```
clarify(
  question="Anh/chị muốn đổi tên file không? Tên gốc là: {ORIGINAL_NAME}.md",
  choices=[
    f"Giữ nguyên: {ORIGINAL_NAME}.md",
    "Nhập tên khác (gõ bên dưới)"
  ]
)
```

**Behavior:**
- If user chooses "Giữ nguyên" → use `{ORIGINAL_NAME}.md`
- If user types a new name → use that name (append `.md` if not already)
- If user doesn't answer or says "không" → default to `{ORIGINAL_NAME}.md`
- Strip any invalid filename characters (`/`, `\`, `:`, `*`, `?`, `"`, `<`, `>`, `|`)

## Step 6: Save & Send

```bash
mkdir -p /root/Downloads/markdown/
cp /tmp/mc_output.md "/root/Downloads/markdown/${FINAL_NAME}.md"
```

### Report to user
- ✅ File saved path
- File size and line count
- Send file in chat using MEDIA: path

### Example response
```
✅ Đã chuyển đổi thành công!

📄 `/root/Downloads/markdown/BỘ NÃO THỨ 2 LLM WIKI.md`
- 47KB, 478 dòng
- PDF → Markdown (markitdown)
```

## Error Handling Summary

| Error | Action |
|---|---|
| markitdown not installed | `pip install markitdown` automatically |
| gdown fails for Google Drive | Try curl with direct download link |
| File too large (>50MB) | Warn user, ask to continue |
| Empty output | Report + suggest alternative tools |
| OCR failure (images/scanned PDF) | Suggest pymupdf, tesseract, marker-pdf |
| Unsupported file type | Report with list of supported types |

## Obsidian Markdown Output

When the user requests Obsidian-flavored Markdown (mentions "obsidian", "wikilinks", "callouts", "frontmatter", or references the `obsidian-markdown` skill), apply these additional transformations after Step 4:

### Frontmatter / Properties
```yaml
---
title: Document Title
date: YYYY-MM-DD
tags:
  - relevant
  - tags
aliases:
  - Alternative Name
author: Author Name (if detected)
language: vi (or en)
---
```

### Obsidian-specific formatting
- Wrap key insights/highlights with `==highlight==` syntax
- Use callouts for tips/warnings/quotes: `> [!tip] Title` / `> [!warning] Title` / `> [!quote] Title`
- Add `[[Wikilinks]]` for related topics at the bottom
- Use `> [!important]` for key takeaways
- Preserve emoji in headings for visual scanning
- Add `---` horizontal rules between major sections

### Cross-reference
Load the `obsidian-markdown` skill via `skill_view(name='obsidian-markdown')` for full syntax reference when producing Obsidian output.

## Language Support
- Vietnamese and English documents
- No special handling needed — markitdown handles both
- Formatting rules apply equally to both languages
- Keep original language, do not translate

## Delivery Pitfalls

> **⚠️ File delivery expectation:** When user says "đưa cho anh file .md" or "gửi file lên đây", they expect an actual downloadable file attachment in the chat — NOT inline pasted content. Always use `MEDIA:/path/to/file.md` to send the file. If the platform (e.g., Slack gateway) doesn't support file uploads, inform the user of the limitation immediately and offer alternatives (Telegram, scp, or provide server path for direct download).

> **⚠️ Don't paste full content then also send file.** The user wants the file, not a wall of text. A brief summary + the file attachment is the right pattern.
