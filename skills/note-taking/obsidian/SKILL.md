---
name: obsidian
description: Read, search, create, and edit notes in the Obsidian vault.
---

# Obsidian Vault

Use this skill for filesystem-first Obsidian vault work: reading notes, listing notes, searching note files, creating notes, appending content, and adding wikilinks.

## Related sub-skills (load for specialized tasks)

These are installed under the `obsidian` skill category and provide deep Obsidian-specific knowledge:

- **`obsidian-markdown`** — Full Obsidian Flavored Markdown syntax: wikilinks, embeds, callouts, properties, comments, highlights. Load when creating/editing `.md` files with Obsidian-specific features. Has references: CALLOUTS.md, PROPERTIES.md, EMBEDS.md.
- **`obsidian-bases`** — Obsidian Bases (`.base` files): database views with filters, formulas, summaries (table/cards/list/map). Load when creating `.base` files or the user mentions Bases. Has reference: FUNCTIONS_REFERENCE.md.
- **`defuddle`** — Extract clean markdown from web pages via `defuddle parse <url> --md`. Prefer over generic web fetch for articles/docs. CLI installed globally (v0.18.1+).

## Reference files

- `references/100-ai-agents-enterprise.md` — Index of 100 AI Agent use cases (10 categories × 10 agents) with full workflow details. Useful when user asks about AI automation strategy, agent workflows, or enterprise AI planning.

## Vault path

Use a known or resolved vault path before calling file tools.

The documented vault-path convention is the `OBSIDIAN_VAULT_PATH` environment variable, for example from `~/.hermes/.env`. If it is unset, use `~/Documents/Obsidian Vault`.

File tools do not expand shell variables. Do not pass paths containing `$OBSIDIAN_VAULT_PATH` to `read_file`, `write_file`, `patch`, or `search_files`; resolve the vault path first and pass a concrete absolute path. Vault paths may contain spaces, which is another reason to prefer file tools over shell commands.

If the vault path is unknown, `terminal` is acceptable for resolving `OBSIDIAN_VAULT_PATH` or checking whether the fallback path exists. Once the path is known, switch back to file tools.

## Read a note

Use `read_file` with the resolved absolute path to the note. Prefer this over `cat` because it provides line numbers and pagination.

## List notes

Use `search_files` with `target: "files"` and the resolved vault path. Prefer this over `find` or `ls`.

- To list all markdown notes, use `pattern: "*.md"` under the vault path.
- To list a subfolder, search under that subfolder's absolute path.

## Search

Use `search_files` for both filename and content searches. Prefer this over `grep`, `find`, or `ls`.

- For filenames, use `search_files` with `target: "files"` and a filename `pattern`.
- For note contents, use `search_files` with `target: "content"`, the content regex as `pattern`, and `file_glob: "*.md"` when you want to restrict matches to markdown notes.

## Create a note

Use `write_file` with the resolved absolute path and the full markdown content. Prefer this over shell heredocs or `echo` because it avoids shell quoting issues and returns structured results.

## Append to a note

Prefer a native file-tool workflow when it is not awkward:

- Read the target note with `read_file`.
- Use `patch` for an anchored append when there is stable context, such as adding a section after an existing heading or appending before a known trailing block.
- Use `write_file` when rewriting the whole note is clearer than constructing a fragile patch.

For an anchored append with `patch`, replace the anchor with the anchor plus the new content.

For a simple append with no stable context, `terminal` is acceptable if it is the clearest safe option.

## Targeted edits

Use `patch` for focused note changes when the current content gives you stable context. Prefer this over shell text rewriting.

## Large-scale content generation (50+ KB notes)

When generating very large Obsidian notes (e.g., 100-item catalogs, comprehensive reference docs that may exceed 50-100 KB):

1. **Do NOT use `delegate_task` with >3 subagents** — `max_concurrent_children` defaults to 3 and large content tasks often timeout (600s limit).
2. **Prefer direct `write_file`** — Write each section directly. It is faster and more reliable than subagent delegation for content-heavy tasks.
3. **If you must delegate** — Split into max 3 tasks, keep each under ~30 items. Use `role: leaf` with `toolsets: ["file"]`.
4. **Combine with `execute_code`** — After writing sections to temp files, use a Python script via `execute_code` to read all parts and `write_file` the combined result.

## Wikilinks

Obsidian links notes with `[[Note Name]]` syntax. When creating notes, use these to link related content.
