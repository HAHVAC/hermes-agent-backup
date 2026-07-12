---
name: media
description: "Media processing and retrieval: YouTube transcript fetching, video summarization, and Tenor GIF search."
version: 1.0.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [media, youtube, video, transcript, gif, search, tenor, download]
---

# Media Processing & Retrieval Skill

A collection of procedures for working with media files, downloading transcripts, and searching for visual media (GIFs).

## YouTube Video Summarization & Transcript Fetching

Extract transcripts from YouTube videos for summarization, drafting blog posts, or creating summaries.

### Usage

Use the python script `scripts/fetch_transcript.py` to extract the transcript:
```bash
python3 ~/.hermes/skills/media/scripts/fetch_transcript.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --output transcript.txt
```

### Supporting files
- `references/output-formats.md` outlines the structure and format of extracted transcript summaries.

---

## Tenor GIF Search & Downloading

Search and download animated GIFs from Tenor using curl and jq.

### Usage

Use curl to search Tenor:
```bash
# Search for 'happy cat' GIFs
curl -s "https://g.tenor.com/v1/search?q=happy+cat&key=LIVDTRZULEJH&limit=5" | jq -r '.results[].media[0].gif.url'
```
