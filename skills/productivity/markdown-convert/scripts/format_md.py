#!/usr/bin/env python3
"""
Markdown Format Script — cleans up raw markitdown output.
Usage: python format_md.py <input.md> <output.md> [--source-type pdf|docx|pptx|xlsx|image]
"""
import sys
import re
import argparse


def remove_noise(text: str) -> str:
    """Remove Python warnings, form feeds, page headers/footers."""
    lines = text.split("\n")

    # Remove leading Python warnings
    while lines and ("Warning" in lines[0] or "warnings" in lines[0] or lines[0].strip().startswith("import")):
        lines.pop(0)

    # Remove form feed characters
    lines = [l.replace("\x0c", "") for l in lines]

    # Remove trailing HẾT
    lines = [l for l in lines if l.strip().replace(" ", "") != "HẾT"]

    return "\n".join(lines)


def remove_page_artifacts(text: str) -> str:
    """Remove repeated page headers and standalone page numbers."""
    lines = text.split("\n")
    cleaned = []

    # Detect repeating header pattern (first ~3 pages)
    # A page header is a line that repeats multiple times
    line_counts = {}
    for l in lines:
        s = l.strip()
        if s and len(s) > 5:
            key = s.replace(" ", "")
            line_counts[key] = line_counts.get(key, 0) + 1

    repeated_headers = {k for k, v in line_counts.items() if v >= 3 and len(k) > 10}

    for line in lines:
        s = line.strip()
        nospace = s.replace(" ", "")

        # Skip repeated page headers
        if nospace in repeated_headers:
            continue

        # Skip standalone page numbers (digits 1-100)
        if s.isdigit() and 1 <= int(s) <= 100:
            continue

        cleaned.append(line)

    return "\n".join(cleaned)


def join_paragraphs(text: str) -> str:
    """Join paragraph fragments split by PDF column layout."""
    lines = text.split("\n")
    n = len(lines)

    structural_prefixes = (
        '#', '```', '---', '>', '•', '✦',
        'my-wiki', '├', '│', '└', '─',
    )

    def is_text_line(s):
        if not s or len(s) < 3:
            return False
        if s.startswith(structural_prefixes):
            return False
        if re.match(r'^\d+\.\d+\s', s):
            return False
        if re.match(r'^\d+\.\s', s):
            return False
        if re.match(r'^Chương \d+', s):
            return False
        if re.match(r'^Phụ lục [A-Z]', s):
            return False
        if re.match(r'^Phần [IVX]+', s):
            return False
        if re.match(r'^P H Ầ N', s):
            return False
        if s.startswith('"') or s.startswith('\u201c'):
            return False
        if s.startswith('—'):
            return False
        return True

    joined = []
    i = 0
    while i < n:
        line = lines[i]
        if not is_text_line(line):
            joined.append(line)
            i += 1
            continue
        # Collect consecutive text lines (skip blanks between them)
        parts = [re.sub(r' {2,}', ' ', line)]
        j = i + 1
        while j < n:
            if lines[j].strip() == "":
                j += 1
                continue
            if not is_text_line(lines[j]):
                break
            parts.append(re.sub(r' {2,}', ' ', lines[j]))
            j += 1
        joined.append(" ".join(parts))
        i = j

    return "\n".join(joined)


def collapse_blank_lines(text: str) -> str:
    """Remove excessive consecutive blank lines."""
    return re.sub(r'\n{3,}', '\n\n', text)


def add_structure(text: str) -> str:
    """Add markdown heading levels, quotes, bullets, etc."""
    lines = text.split("\n")
    n = len(lines)
    out = []
    i = 0

    def next_nonempty(idx):
        while idx < n and not lines[idx].strip():
            idx += 1
        return idx

    while i < n:
        line = lines[i]
        stripped = line.strip()

        # --- Quoted text with attribution ---
        if stripped.startswith('"') or stripped.startswith('\u201c'):
            qparts = [stripped]
            qi = i + 1
            while qi < n and lines[qi].strip() and not lines[qi].strip().startswith('—'):
                qparts.append(lines[qi].strip())
                qi += 1
            attr = ""
            if qi < n and lines[qi].strip().startswith('—'):
                attr = lines[qi].strip()
                qi += 1
            out.append("> " + " ".join(qparts))
            if attr:
                out.append(">")
                out.append(f"> {attr}")
            out.append("")
            i = qi
            continue

        # --- ✦ separators ---
        if stripped.startswith("✦"):
            out.append("")
            out.append("---")
            out.append("")
            i += 1
            continue

        # --- ALL CAPS callout ---
        if stripped.isupper() and len(stripped) > 8:
            out.append("")
            out.append(f"> **{stripped}**")
            out.append("")
            i += 1
            continue

        # --- Bullets ---
        if stripped.startswith('•'):
            out.append(f"- {stripped[1:].strip()}")
            i += 1
            continue

        # --- Chapters ---
        ch = re.match(r'^Chương (\d+)\s+(.*)', stripped)
        if ch:
            ch_title = ch.group(2).strip()
            ni = next_nonempty(i + 1)
            if ni < n and lines[ni].strip() and not re.match(r'^(\d+\.\d+|"|—|•)', lines[ni].strip()):
                ch_title += " " + lines[ni].strip()
                i = ni + 1
            else:
                i += 1
            out.append(f"\n## Chương {ch.group(1)}: {ch_title}\n")
            continue

        # --- Subsections ---
        sub = re.match(r'^(\d+\.\d+)\s+(.*)', stripped)
        if sub:
            sub_title = sub.group(2).strip()
            ni = next_nonempty(i + 1)
            if ni < n and lines[ni].strip() and not re.match(r'^(\d+\.\d+|"|—|•)', lines[ni].strip()):
                sub_title += " " + lines[ni].strip()
                i = ni + 1
            else:
                i += 1
            out.append(f"\n### {sub.group(1)} {sub_title}\n")
            continue

        # --- Phụ lục ---
        pl = re.match(r'^Phụ lục ([A-Z])\s+(.*)', stripped)
        if pl:
            out.append(f"\n## Phụ lục {pl.group(1)}: {pl.group(2).strip()}\n")
            i += 1
            continue

        # --- Part headers ---
        if re.match(r'^Phần [IVX]+', stripped):
            out.append(f"\n---\n\n# {stripped}\n")
            i += 1
            continue

        # --- Directory tree code block ---
        if stripped.startswith('my-wiki/') or stripped.startswith('├') or stripped.startswith('└'):
            if not (out and out[-1].strip() == "```"):
                out.append("```")
            out.append(stripped)
            i += 1
            # Close code block on blank line
            if i < n and not lines[i].strip():
                out.append("```")
                out.append("")
            continue

        # --- Known section headings (Vietnamese) ---
        section_headings = {
            'Về cuốn sách này': '## Về cuốn sách này',
            'Mục lục': '## Mục lục',
            'Lời mở đầu': '## Lời mở đầu',
            'Gợi ý cách đọc': '### Gợi ý cách đọc',
        }
        if stripped in section_headings:
            out.append(f"\n{section_headings[stripped]}\n")
            i += 1
            continue

        # --- Default ---
        out.append(line.rstrip())
        i += 1

    return "\n".join(out)


def final_cleanup(text: str) -> str:
    """Final trim and normalize."""
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = "\n".join(l.rstrip() for l in text.split("\n"))
    text = text.strip() + "\n"
    return text


def format_markdown(text: str, source_type: str = "pdf") -> str:
    """Main formatting pipeline."""
    text = remove_noise(text)

    if source_type == "pdf":
        text = remove_page_artifacts(text)

    text = join_paragraphs(text)
    text = collapse_blank_lines(text)
    text = add_structure(text)
    text = final_cleanup(text)
    return text


def main():
    parser = argparse.ArgumentParser(description="Format raw markitdown output to clean markdown")
    parser.add_argument("input", help="Input markdown file path")
    parser.add_argument("output", help="Output markdown file path")
    parser.add_argument("--source-type", default="pdf", choices=["pdf", "docx", "pptx", "xlsx", "image"],
                        help="Source file type for type-specific formatting")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        raw = f.read()

    result = format_markdown(raw, args.source_type)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(result)

    lines = result.count("\n")
    size_kb = len(result.encode("utf-8")) / 1024
    print(f"✅ Formatted: {args.output} ({size_kb:.1f}KB, {lines} lines)")


if __name__ == "__main__":
    main()
