#!/bin/bash
# ============================================================
# Hermes Agent GitHub Backup Script
# Backup ~/.hermes/ → /root/hermes-backup-repo → GitHub
# Schedule: hàng ngày 02:00 GMT+7 (19:00 UTC)
# ============================================================

set -euo pipefail

HERMES_DIR="$HOME/.hermes"
BACKUP_REPO="/root/hermes-backup-repo"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
DATE_TAG=$(date '+%Y-%m-%d %H:%M')

echo "[$TIMESTAMP] ▶ Hermes backup bắt đầu..."

# ── Bước 1: Rsync ~/.hermes/ → backup repo ─────────────────
echo "[$TIMESTAMP] Syncing files..."
rsync -a --delete \
  --exclude='.git' \
  --filter=':- .gitignore' \
  "$HERMES_DIR/" "$BACKUP_REPO/"

echo "[$TIMESTAMP] Rsync hoàn thành."

# ── Bước 2: Redact secrets trong config.yaml ───────────────
if [ -f "$BACKUP_REPO/config.yaml" ]; then
  sed -i 's/api_key:.*/api_key: REDACTED/g' "$BACKUP_REPO/config.yaml"
  echo "[$TIMESTAMP] config.yaml: API key đã được redact."
fi

# ── Bước 3: Git commit & push ──────────────────────────────
cd "$BACKUP_REPO"
git add -A

# Chỉ commit nếu có thay đổi thực sự
if git diff --cached --quiet; then
  echo "[$TIMESTAMP] ✅ Không có thay đổi. Bỏ qua commit."
  exit 0
fi

CHANGED=$(git diff --cached --stat | tail -1)
git commit -m "backup: $DATE_TAG GMT+7 | $CHANGED"
git push origin main

echo "[$TIMESTAMP] ✅ Backup thành công → github.com/HAHVAC/hermes-agent-backup"
