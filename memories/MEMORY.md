Boss uses Lark international (larksuite.com / pccctruongan.sg.larksuite.com), not Feishu China; Lark CLI links/scopes should use the Lark international domain when possible.
§
NotebookLM integration for Boss should use the Google account hahvac@gmail.com unless changed.
§
AnyGen v0.1.0: working command is `anygen task create --data '{"operation":"<type>","prompt":"..."}'` (NOT `anygen generate`). API_KEY must be exported as env var, `anygen auth login` doesn't work headless. 9 skills + anygen-suite installed.
§
AnyGen full 9 skills + anygen-suite are installed on this Hermes instance (84 total skills after May 2026 cleanup). Deleted categories: all MLOps (entire category), gaming, red-teaming, smart-home, leisure; plus individual creative/media/social skills unused by Boss (comfyui, p5js, pixel-art, manim-video, ascii-art/video, baoyu-comic/infographic, songwriting, pretext, touchdesigner, spotify, heartmula, songsee, xitter, xurl, godmode, openhue, find-nearby, polymarket, llm-wiki, research-paper-writing)
§
Obsidian skills installed from kepano/obsidian-skills (category: obsidian): obsidian-markdown, obsidian-bases, defuddle CLI v0.18.1. User chose skills 1,2,5 — NOT json-canvas or obsidian-cli. Existing note-taking/obsidian umbrella patched to cross-reference them.
§
Boss's Obsidian vault path is unknown — ask when saving .md files to vault. Check ~/Obsidian* or common vault locations first.
§
gdown reliable download pattern: `gdown 'https://drive.google.com/uc?id={FILE_ID}' -O /tmp/output`. The `--fuzzy` flag is NOT supported in all versions — avoid it. Always use the full `uc?id=` URL format.
§
Vision analysis: for infographics/charts/lists, always use specific prompts like "read every line of text" — generic "describe everything" prompts produce structural descriptions instead of actual text content.