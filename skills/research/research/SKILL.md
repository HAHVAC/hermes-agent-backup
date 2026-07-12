---
name: research
description: "Information research and content discovery: arXiv academic paper search and RSS/Atom feed monitoring."
version: 1.0.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [research, arxiv, papers, RSS, Atom, blogwatcher, feeds, monitoring]
---

# Research & Content Discovery Skill

A collection of procedures for fetching academic papers and monitoring web feeds.

## arXiv Academic Paper Search

Search and download academic papers from arXiv by keyword, author, category, or ID.

### Usage

Use the python search script:
```bash
python3 ~/.hermes/skills/research/research/scripts/search_arxiv.py --query "quantum computing" --limit 5
```

Alternatively, search by author or category:
```bash
python3 ~/.hermes/skills/research/research/scripts/search_arxiv.py --author "Yann LeCun" --limit 3
python3 ~/.hermes/skills/research/research/scripts/search_arxiv.py --category cs.LG --limit 5
```

---

## RSS/Atom Blog Monitoring (blogwatcher)

Monitor blogs and RSS/Atom feeds using the `blogwatcher-cli` tool.

### Usage

Check all configured feeds:
```bash
blogwatcher check
```

Add a new feed:
```bash
blogwatcher add "https://example.com/feed.xml" --name "Example Blog"
```

List all tracked feeds:
```bash
blogwatcher list
```
