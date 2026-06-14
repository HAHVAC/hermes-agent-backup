# Format Rules Reference

## PDF-Specific Rules

### Paragraph Joining Logic
PDFs break paragraphs into separate lines due to column layout. Rules for joining:

**JOIN (consecutive text lines):**
- Regular prose text separated by blank lines
- Lines that don't start with structural markers
- Lines between 3-500 chars that are normal text

**DO NOT JOIN:**
- Lines starting with `#` (headings)
- Lines starting with ` ``` ` (code blocks)
- Lines starting with `---` (horizontal rules)
- Lines starting with `>` (blockquote)
- Lines starting with `•` or `- ` (bullets)
- Lines starting with `✦` (decorative separators)
- Lines starting with `├`, `│`, `└` (tree characters)
- Lines starting with `"` or `"` (quoted text)
- Lines starting with `—` (attribution)
- Lines matching `N.N` pattern (subsections like `1.1`)
- Lines matching `Chương N` pattern (chapters)
- Lines matching `Phụ lục X` pattern (appendices)
- Lines matching `Phần X` pattern (parts)
- Lines matching `P H Ầ N` (spaced Vietnamese part headers)
- Lines that are ALL CAPS (callout boxes)
- Lines < 3 characters

### Page Header Detection
- Strip all spaces from a line
- Compare with other lines (similarly stripped)
- If a line appears 3+ times → it's a page header → remove all instances
- Common patterns: spaced-out book titles, chapter headings repeated at page tops

### Table Reconstruction
When table data is detected (columns with consistent separators or repeated short entries):
1. Identify column structure from header row
2. Reconstruct with `|` delimiters
3. Add `|---|---|` separator after header
4. If table is from a comparison/evaluation section, ensure all rows align

## Heading Level Convention

| Content | Level | Example |
|---|---|---|
| Book/document title | H1 `#` | `# Bộ Não Thứ Hai — LLM Wiki` |
| Part (Phần/Part) | H1 `#` | `# Phần I` |
| Chapter | H2 `##` | `## Chương 3: RAG không phải là câu trả lời cuối cùng` |
| Subsection (N.N) | H3 `###` | `### 3.2 Bốn vấn đề RAG không giải được` |
| Appendix | H2 `##` | `## Phụ lục A: Mẫu CLAUDE.md` |
| Sections within appendices | H3 `###` | `### Nguồn nền tảng` |
| Sub-subsections | Bold | `**Nguyên tắc nguyên tử**` |

## Quote Formatting
```markdown
> "Quoted text in a single paragraph"
>
> — Author Name, Source (Year)
```

- Join multi-line quotes into single paragraph within `>`
- Attribution line starts with `—`
- Always have blank `>` line before attribution

## Callout Boxes
ALL CAPS text > 8 chars → convert to blockquote:
```markdown
> **BA NGUYÊN LÝ TỪ MEMEX ĐẾN LLM WIKI**
```

## Separator Convention
- `✦ ✦ ✦` patterns → `---` (horizontal rule)
- Between major parts → `---` + blank line
- Between chapters → blank line only (no `---`)

## Code Block Rules
Wrap in triple backticks:
- Directory trees (my-wiki/, ├──, └──)
- YAML/frontmatter examples
- Command examples
- Config file snippets
- File path listings

## Language Handling
- Vietnamese text: keep as-is, do not translate
- English text: keep as-is
- Mixed content: preserve original mix
- Technical terms: keep original (RAG, LLM, MCP, etc.)
- Vietnamese technical terms with English equivalents: use whichever the source uses
