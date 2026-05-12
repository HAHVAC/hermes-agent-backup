# Hermes Agent GitHub Backup Pattern
# Proven working pattern from 2026-05-11 session

## 1. .gitignore standard

```
# === SECRETS & CREDENTIALS ===
auth.json
auth.lock
google_token.json
google_client_secret.json
*.env
.env*
pairing/
whatsapp/
auth/

# === DATABASE & RUNTIME STATE ===
state.db
state.db-shm
state.db-wal
kanban.db
*.db
*.db-shm
*.db-wal
gateway.pid
gateway.lock
gateway_state.json
processes.json
feishu_seen_message_ids.json
models_dev_cache.json
ollama_cloud_models_cache.json
.skills_prompt_snapshot.json

# === CACHE & TEMP ===
cache/
audio_cache/
image_cache/
images/
logs/
tmp/
*.lock

# === SESSION & HISTORY ===
sessions/
sandboxes/
email_attachments/

# === LARGE SOURCE CODE
hermes-agent/

# === SNAPSHOTS & MIGRATION ===
state-snapshots/
migration/
```

## 2. Backup script pattern

```bash
#!/bin/bash
set -euo pipefail

HERMES_DIR="$HOME/.hermes"
BACKUP_REPO="/root/hermes-backup-repo"

rsync -a --delete \
  --exclude='.git' \
  --filter=':- .gitignore' \
  "$HERMES_DIR/" "$BACKUP_REPO/"

# Redact API keys
sed -i 's/api_key:.*/api_key: REDACTED/g' "$BACKUP_REPO/config.yaml"

cd "$BACKUP_REPO"
git add -A

if ! git diff --cached --quiet; then
  git commit -m "backup: $(date '+%Y-%m-%d %H:%M') GMT+7"
  git push origin main
fi
```

## 3. Cron schedule

Schedule: `0 19 * * *` = 02:00 GMT+7 daily
Script: `hermes_backup.sh`
Mode: `no_agent: true`
Delivery: `local`
