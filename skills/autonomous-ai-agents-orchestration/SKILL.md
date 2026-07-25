---
name: autonomous-ai-agents-orchestration
description: Guidelines for orchestrating, debugging, and running subagents or developer CLIs such as Claude Code, Codex, and OpenCode.
category: autonomous-ai-agents
---

# Autonomous AI Agents & Orchestration

This skill covers the configuration, runtime orchestration, and debugging patterns of developer-focused AI command-line interfaces (`claude-code`, `codex`, `opencode`) inside terminal environments, as well as installing and leveraging specialized multi-tool agent community rosters like **The Agency (`msitarzewski/agency-agents`)**.

## Supported Agents & Integration Guides

### 1. The Agency Roster (`msitarzewski/agency-agents`)
- **Core Concept**: A repository containing 230+ specialized, role-playing AI agent specifications (Markdown frontmatter format) representing various disciplines (Engineering, Design, Testing, Support, etc.).
- **Multi-Tool Conversion**: It includes a `./scripts/convert.sh` pipeline which renders these Markdown profiles into target formats for other developer tools (e.g. `.mdc` files for Cursor, custom TOML configs for Codex, skill directories for Antigravity, `.windsurfrules` for Windsurf, or plugins for Hermes).
- **CLI Installer**: Run `./scripts/install.sh --tool <tool>` or `./scripts/install.sh --tool <tool> --division <engineering|security>` to deploy specific subsets. Use the `--dry-run` flag to inspect targets before copying files.
- **Reference**: High-value specialist profiles (e.g., `engineering-feishu-integration-developer.md`) can serve as starting points or templates when crafting custom skills for specific integrations.

### 2. Claude Code CLI (`claude-code`) (claude-code)
- **Execution Mode**: Prefer running single tasks via pipe/print mode:
  ```bash
  claude -p "Your single-shot instruction"
  ```
- **Interactive Loops**: For long-running execution sequences, wrap Claude Code inside a `tmux` session to retain context and allow polling/attaching.
- **Commands**: Read the complete integration reference at `references/claude-code.md`.

### 2. Codex CLI (`codex`)
- **Requirement**: Codex CLI requires a valid Git repository to execute commands and track changes.
- **Auth Configuration**: Credentials must be configured in `~/.codex/auth.json` or supplied via the `OPENAI_API_KEY` environment variable.
- **Commands**: Read the integration and setup details at `references/codex.md`.

### 3. OpenCode CLI (`opencode`)
- **Execution Mode**: Prefer `opencode run` for singular automated executions.
- **TUI Management**: When managing an interactive TUI session, exit gracefully using `Ctrl+C` (`\x03`) or `process(action="kill")`. Avoid typing `/exit` directly in the script, as it triggers a feedback prompt.
- **Commands**: Read the integration patterns at `references/opencode.md`.

### 4. Matt Pocock Skills (`mattpocock/skills`)
- **Core Concept**: A workflow framework of 20+ specialized user-invoked and model-invoked agent skills designed to transition from "vibe coding" to structured "real engineering" via step-by-step interviews, domain glossary creation (`CONTEXT.md` / ADRs), vertical-slice ticket generation (`/to-tickets`), test-driven implementation (`/tdd`), and rigorous debugging loops (`/diagnosing-bugs`).
- **Reference**: Read the detailed workflow patterns, installation methods, and spec/ticket structures at `references/mattpocock-skills.md`.

---

## Shared Best Practices

1. **Isolation**: Always run agent actions within project-scoped directories.
2. **Safety Guards**: Ensure destructive CLI edits are reviewed through diff files before pushing changes.
3. **Environment Checks**: Set active provider keys (`OPENROUTER_API_KEY`, etc.) before spawning processes.
