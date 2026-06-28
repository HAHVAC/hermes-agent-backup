# Context loading and Boss/Doremon persona setup

Session learning from configuring Boss's Hermes instance.

## What Hermes reads before a task

`AIAgent._build_system_prompt()` in `run_agent.py` builds the system prompt once per session and caches it. Main layers:

1. Identity: `~/.hermes/SOUL.md` if present, otherwise `DEFAULT_AGENT_IDENTITY`.
2. Hermes help guidance and tool-specific guidance.
3. Caller/gateway system message when provided.
4. Built-in memories from `~/.hermes/memories/MEMORY.md` and `~/.hermes/memories/USER.md` when enabled.
5. External memory provider block if configured.
6. Skills index from installed `SKILL.md` / `DESCRIPTION.md` files, cached in `~/.hermes/.skills_prompt_snapshot.json`.
7. Project context files, unless skipped:
   - `.hermes.md` / `HERMES.md` walking from cwd up to git root, first match wins.
   - else `AGENTS.md` / `agents.md` in cwd only.
   - else `CLAUDE.md` / `claude.md` in cwd only.
   - else `.cursorrules` and `.cursor/rules/*.mdc` in cwd only.
8. Timestamp/session/model/provider, environment hints, platform hint.

Important: project context selection is first-match-wins; if `/root/.hermes.md` exists and `TERMINAL_CWD=/root`, gateway sessions load that lightweight Boss workspace context instead of accidentally loading the Hermes source repo `AGENTS.md`.

## Boss global setup pattern

For Boss's default `/root` workspace:

- Put global Doremon identity at `/root/.hermes/SOUL.md`.
- Keep durable user facts in `/root/.hermes/memories/USER.md`.
- Keep environment/tool quirks in `/root/.hermes/memories/MEMORY.md`.
- Put workspace routing/context in `/root/.hermes.md`.

After editing these, verify file existence and sizes, then remind Boss that new sessions/reset/restart gateway apply the full new system prompt most reliably because the prompt is cached per session.

## Safe compacting principles

- Preserve autonomy boundaries, names, company, timezone, TTS, and key tool quirks.
- Remove duplicated phrasing and one-off task progress.
- Keep memory declarative, not imperative; procedural workflows belong in skills.
- Do not delete or move files without approval; overwriting known config/memory files in-place is acceptable when explicitly requested.
