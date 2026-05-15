Boss uses Lark international (larksuite.com / pccctruongan.sg.larksuite.com), not Feishu China; Lark CLI links/scopes should use the Lark international domain when possible.
§
NotebookLM integration for Boss should use the Google account hahvac@gmail.com unless changed.
§
AnyGen v0.1.0 command pattern: `anygen task create --data '{"operation":"<type>","prompt":"..."}'`; avoid `anygen generate`. API_KEY must be exported; `anygen auth login` does not work headless.
§
AnyGen suite is installed on this Hermes instance; Boss intentionally removed unused categories/skills including MLOps, gaming, red-teaming, smart-home, leisure, and many creative/media/social skills.
§
Obsidian skills installed from kepano/obsidian-skills: obsidian-markdown, obsidian-bases, defuddle CLI v0.18.1. Boss did not choose json-canvas or obsidian-cli.
§
Boss's Obsidian vault path is unknown; when saving .md files to vault, check common vault locations first then ask if still unknown.
§
gdown reliable download pattern: `gdown 'https://drive.google.com/uc?id={FILE_ID}' -O /tmp/output`; avoid `--fuzzy` because not all versions support it.
§
Vision analysis for infographics/charts/lists should ask specifically to "read every line of text"; generic description prompts miss text content.
§
Google Workspace/gws OAuth on this Hermes instance is tied to pcccthanglong.tlc@gmail.com; use that account context for Drive/Gmail/Sheets unless changed.