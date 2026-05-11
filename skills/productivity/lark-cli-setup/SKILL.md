---
name: lark-cli-setup
description: Install and configure the official Lark/Feishu CLI (larksuite/cli) — 200+ commands, 23 AI Agent Skills covering Messenger, Base, Docs, Sheets, Calendar, Mail, Tasks, Approval, and more. Use this whenever the user wants to interact with Lark/Feishu programmatically.
version: 1.0.0
author: agent
tags: [lark, feishu, cli, lark-base, lark-calendar, lark-task, lark-approval, lark-im]
---

# lark-cli Setup

Official CLI for Lark/Feishu: https://github.com/larksuite/cli  
**v1.0.14+** — 200+ commands, 23 AI Agent Skills, MIT license.

## When to use
- User wants to interact with Lark Base, Calendar, Task, Approval, IM, Docs, Sheets, Mail, Wiki, etc.
- Needed before any `lark-*` skill (lark-im, lark-base, lark-calendar, etc.) can function.

## Step 1 — Install CLI + Skills

```bash
# Install CLI binary
npm install -g @larksuite/cli

# Verify
lark-cli --version  # should print e.g. "lark-cli version 1.0.14"

# Install all 23 AI Agent Skills (installs to ~/.agents/skills/ and symlinks for Claude Code, OpenClaw, Codex)
npx skills add larksuite/cli -y -g
```

Both commands are non-interactive and complete in under 2 minutes.

## Step 2 — Create Lark App (one-time, requires browser)

Run in background and extract the URL:

```bash
lark-cli config init --new > /tmp/lark_init.log 2>&1 &
sleep 5
cat /tmp/lark_init.log
```

This prints a URL like:
```
https://open.feishu.cn/page/cli?user_code=XXXX-XXXX&lpv=1.0.14&ocv=1.0.14&from=cli
```

**Send this URL to the user.** They must open it in a browser to:
1. Log in to their Feishu/Lark account
2. Create a new internal Lark App (auto-configured by the CLI wizard)

The background process waits and exits automatically after the user completes setup. URL expires in a few minutes — if it times out, re-run the command to get a fresh URL.

## Step 3 — Auth Login (requires browser)

Same pattern — run in background and extract the URL:

```bash
lark-cli auth login --recommend > /tmp/lark_auth.log 2>&1 &
sleep 5
cat /tmp/lark_auth.log
```

`--recommend` auto-selects the most commonly used OAuth scopes. Send the auth URL to the user. After they approve in the browser, the process exits.

For specific domains only:
```bash
lark-cli auth login --domain calendar,task,im,base,approval --no-wait
```

## Step 4 — Verify

```bash
lark-cli auth status
```

Should show authenticated user + granted scopes.

## Step 5 — Test

```bash
# Quick smoke test
lark-cli calendar +agenda
lark-cli im +chat-list --format table
```

## Installed Skills Location

```
~/.agents/skills/lark-approval
~/.agents/skills/lark-base
~/.agents/skills/lark-calendar
~/.agents/skills/lark-contact
~/.agents/skills/lark-doc
~/.agents/skills/lark-drive
~/.agents/skills/lark-event
~/.agents/skills/lark-im
~/.agents/skills/lark-mail
~/.agents/skills/lark-minutes
~/.agents/skills/lark-okr
~/.agents/skills/lark-sheets
~/.agents/skills/lark-slides
~/.agents/skills/lark-task
~/.agents/skills/lark-vc
~/.agents/skills/lark-whiteboard
~/.agents/skills/lark-wiki
~/.agents/skills/lark-shared        ← auto-loaded by all other lark-* skills
~/.agents/skills/lark-workflow-meeting-summary
~/.agents/skills/lark-workflow-standup-report
~/.agents/skills/lark-openapi-explorer
~/.agents/skills/lark-skill-maker
~/.agents/skills/lark-attendance
```

These are symlinked into Claude Code's skill directory automatically.

## Command Structure

Three layers of granularity:

```bash
# 1. Shortcuts (+ prefix) — human & AI friendly, smart defaults
lark-cli calendar +agenda
lark-cli im +messages-send --chat-id "oc_xxx" --text "Hello"

# 2. API Commands — 1:1 mapped to platform endpoints
lark-cli calendar events list

# 3. Raw API — any of 2500+ Lark APIs
lark-cli api GET /open-apis/calendar/v4/calendars
```

## Useful Flags

```bash
--format json|pretty|table|ndjson|csv
--page-all          # auto-paginate
--as user|bot       # identity switching
--dry-run           # preview before executing
```

## Pitfalls (confirmed by real usage)

- **URL expires fast** — `config init --new` polls max ~200 attempts (~10 phút). Nếu timeout, chạy lại để lấy URL mới.
- **config init success detection** — Không có exit message rõ ràng. Dấu hiệu thành công: log có `"appSecret": "****"`. Poll bằng `tail /tmp/lark_init.log`.
- **auth login: dùng --no-wait + --device-code** — Cách đáng tin cậy nhất cho AI agent:
  ```bash
  lark-cli auth login --recommend --no-wait > /tmp/lark_login.log 2>&1 &
  sleep 5 && cat /tmp/lark_login.log
  # Lấy verification_url gửi user, rồi:
  lark-cli auth login --device-code "<CODE>"  # blocks đến khi user xác nhận
  ```
- **`npx skills add` output is long** — 23 skills + security reports, bình thường.
- **Skills ở ~/.agents/skills/** — khác với Hermes skills (~/.hermes/skills/). Đọc bằng `cat ~/.agents/skills/lark-im/SKILL.md`.
- **`lark-shared` là bắt buộc** — chứa auth + config, tất cả lark-* skills đều depend vào.
- **Bot vs User identity** — `--as user` cho tài nguyên cá nhân (chat, lịch, docs). `--as bot` cho app-level.
- **+chat-search dùng --query** — KHÔNG phải `--keyword`. Flag sai → error.
- **+chat-messages-list dùng --page-size** — KHÔNG phải `--limit`. Max 50.
- **sheets +create không có --format và không có --sheet-title** — Dùng `--title` (tên file) và `--headers` (header row JSON array).
- **Token expiry** — `expiresAt` ~2h tự refresh. `refreshExpiresAt` 7 ngày — quá hạn phải login lại.
