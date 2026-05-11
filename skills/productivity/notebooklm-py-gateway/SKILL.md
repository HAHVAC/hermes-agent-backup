---
name: notebooklm-py-gateway
description: Set up and operate a NotebookLM automation gateway using the unofficial notebooklm-py CLI/API, including isolated auth storage, PoC wrapper scripts, and Feishu/Hermes integration planning. Use when the user asks to connect, automate, sync, or query Google NotebookLM.
---

# NotebookLM-py Gateway

Use this skill when building or operating a Google NotebookLM automation workflow via [`notebooklm-py`](https://github.com/teng-lin/notebooklm-py). This is useful for connecting NotebookLM to Hermes, Feishu/Lark, Google Drive, file pipelines, or scheduled sync/report workflows.

## Important constraints

- `notebooklm-py` is **unofficial** and uses undocumented Google/NotebookLM APIs. Treat as PoC/internal automation, not a guaranteed enterprise API.
- Pin a stable version instead of installing from `main`.
- Google login is cookie/session based. Do **not** ask for the user's Google password.
- If login must happen on a headless server, a normal headed browser may fail due to no X server. Use a machine with a browser, `xvfb-run`, or import a `storage_state.json` generated elsewhere.
- The auth cookie file is sensitive. Prefer a dedicated Google automation account.
- Large files around 20MB+ may timeout; split or convert to Markdown/text before upload.
- Some `notebooklm-py` docs mention commands like `doctor` or `profile`; verify with `notebooklm --help` because installed versions may differ.

## Recommended setup

1. Install pinned package and browser runtime:

```bash
python3 -m pip install --upgrade 'notebooklm-py==0.3.4' playwright
python3 -m playwright install chromium
```

2. Create isolated storage per account/project:

```bash
export NOTEBOOKLM_HOME=/root/.notebooklm-ACCOUNT_ALIAS
```

For Boss's NotebookLM integration, default to:

```bash
export NOTEBOOKLM_HOME=/root/.notebooklm-hahvac
# Google account: hahvac@gmail.com
```

3. Check commands actually available:

```bash
notebooklm --version
notebooklm --help
notebooklm auth --help
```

4. Check auth status:

```bash
NOTEBOOKLM_HOME=/root/.notebooklm-hahvac notebooklm auth check
```

## Login flow

Preferred login on a machine with a GUI browser:

```bash
NOTEBOOKLM_HOME=./notebooklm-hahvac notebooklm login
```

Then transfer this file to the server:

```text
./notebooklm-hahvac/storage_state.json
```

Place it at:

```text
/root/.notebooklm-hahvac/storage_state.json
```

Verify:

```bash
NOTEBOOKLM_HOME=/root/.notebooklm-hahvac notebooklm auth check --test
NOTEBOOKLM_HOME=/root/.notebooklm-hahvac notebooklm list --json
```

If running login on a headless server fails with a missing X server error, use:

```bash
NOTEBOOKLM_HOME=/root/.notebooklm-hahvac xvfb-run -a notebooklm login
```

but prefer user-controlled browser login when Google security challenges are likely.

## Gateway PoC structure

Create a small project directory:

```bash
mkdir -p /root/notebooklm-gateway/{scripts,config,data/staging,outputs,logs}
```

Example config:

```json
{
  "account": "hahvac@gmail.com",
  "notebooklm_home": "/root/.notebooklm-hahvac",
  "notebooks": {
    "pccc_test": {
      "title": "[PCCC] Test Quy trinh noi bo",
      "id": null,
      "description": "PoC NotebookLM cho tai lieu PCCC noi bo"
    }
  }
}
```

A wrapper script should call the `notebooklm` CLI with `NOTEBOOKLM_HOME` set from config and expose stable subcommands:

- `status` → `notebooklm auth check` and `notebooklm status`
- `list` → `notebooklm list --json`
- `create <key>` → `notebooklm create <title> --json`, then save returned notebook ID into config
- `add-source <key|id> <content> [--type file|text|url|youtube] [--title ...]`
- `ask <key|id> <question>` → `notebooklm ask ... --json`
- `report <key|id> --format briefing-doc --language vi --wait --json`

Use explicit notebook IDs in automation rather than relying on `notebooklm use`, because CLI context files can be overwritten by concurrent agents or cron jobs.

## Useful commands

```bash
# Create notebook
NOTEBOOKLM_HOME=/root/.notebooklm-hahvac notebooklm create "[PCCC] Test Quy trinh noi bo" --json

# Add sources
NOTEBOOKLM_HOME=/root/.notebooklm-hahvac notebooklm source add ./file.pdf --notebook NOTEBOOK_ID --type file --json
NOTEBOOKLM_HOME=/root/.notebooklm-hahvac notebooklm source add "https://example.com" --notebook NOTEBOOK_ID --type url --json
NOTEBOOKLM_HOME=/root/.notebooklm-hahvac notebooklm source add "Text content" --title "Title" --notebook NOTEBOOK_ID --type text --json

# Ask questions
NOTEBOOKLM_HOME=/root/.notebooklm-hahvac notebooklm ask "Tóm tắt tài liệu này" --notebook NOTEBOOK_ID --json

# Generate Vietnamese briefing report
NOTEBOOKLM_HOME=/root/.notebooklm-hahvac notebooklm generate report --notebook NOTEBOOK_ID --format briefing-doc --language vi --wait --json

# Download latest report
NOTEBOOKLM_HOME=/root/.notebooklm-hahvac notebooklm download report --notebook NOTEBOOK_ID --latest --force ./outputs/report.md
```

## Feishu/Hermes integration pattern

Use NotebookLM indirectly through a gateway:

```text
Feishu Docs / Drive / Google Drive / files
        ↓
staging + conversion + checksum
        ↓
notebooklm-py gateway
        ↓
NotebookLM notebook
        ↓
ask/report/artifact generation
        ↓
Feishu / Telegram response
```

Recommended first PoC:

1. Use a dedicated Google account, e.g. `hahvac@gmail.com`.
2. Create one notebook such as `[PCCC] Test Quy trinh noi bo`.
3. Add 5-10 non-sensitive PDFs/DOCX/Markdown files.
4. Test `ask` and `generate report`.
5. Only after auth and PoC work, build scheduled Feishu sync.

## Verification checklist

- `notebooklm --version` shows the expected pinned version.
- `notebooklm auth check --test` passes with the intended `NOTEBOOKLM_HOME`.
- `notebooklm list --json` returns valid JSON.
- A notebook can be created and its ID saved.
- At least one source can be added.
- `ask --json` returns an answer and references.
- Report generation with `--wait --json` completes.

## Troubleshooting

- `ModuleNotFoundError: No module named 'notebooklm.notebooklm_cli'`: stale/broken CLI on PATH or wrong package; reinstall pinned `notebooklm-py` in the active Python environment and re-check `which notebooklm`.
- `No such command 'doctor'` or `No such command 'profile'`: installed version may not support docs' commands; rely on `notebooklm --help` for the live command surface.
- `Storage file not found`: login has not been completed or `NOTEBOOKLM_HOME` points to the wrong directory.
- Playwright says it launched a headed browser without XServer: use GUI machine login, import `storage_state.json`, or use `xvfb-run -a notebooklm login`.
- Unauthorized/login redirect: cookies expired; run login again.
