# Hermes Agent Backup to GitHub — Implementation Plan

**Goal:** Backup toàn bộ workspace Hermes Agent (`~/.hermes/`) lên repo GitHub `HAHVAC/hermes-agent-backup` một cách an toàn, tự động hàng ngày.

**Repo target:** https://github.com/HAHVAC/hermes-agent-backup.git
**Schedule:** Hàng ngày, 02:00 GMT+7 (19:00 UTC ngày hôm trước)
**GitHub account:** HAHVAC (đã auth via `gh`)

---

## ⚠️ Audit Bảo Mật — Những file KHÔNG được backup

Các file/thư mục chứa secrets cần đưa vào `.gitignore`:

| File/Thư mục | Lý do loại trừ |
|---|---|
| `auth.json` / `auth.lock` | Chứa credential_pool + provider API keys |
| `config.yaml` → backup version riêng đã redact | `api_key: sk-aba...` |
| `google_token.json` / `google_client_secret.json` | OAuth token Google |
| `state.db` / `state.db-shm` / `state.db-wal` | SQLite DB chứa session data |
| `sessions/` | Toàn bộ lịch sử chat |
| `cache/` / `audio_cache/` / `image_cache/` | Cache tạm, không cần backup |
| `images/` | Ảnh tạm |
| `logs/` | Log hệ thống |
| `gateway.pid` / `gateway.lock` / `gateway_state.json` | Runtime state |
| `processes.json` | Runtime processes |
| `pairing/` | Pairing tokens |
| `sandboxes/` | Sandbox data tạm |
| `hermes-agent/` | Source code Hermes (rất lớn, không cần backup) |
| `migration/` | Migration state nội bộ |
| `state-snapshots/` | Snapshots cũ có chứa `auth.json` |
| `whatsapp/` | Session WhatsApp |
| `feishu_seen_message_ids.json` | Runtime state Feishu |
| `models_dev_cache.json` / `ollama_cloud_models_cache.json` | Cache models |
| `.skills_prompt_snapshot.json` | Snapshot tạm |
| `skills/openclaw-imports/*/briefing_data*.json` | Data cache động |

**✅ Những gì SẼ được backup:**

| Thư mục/File | Nội dung |
|---|---|
| `skills/` | Toàn bộ skills (13MB) |
| `memories/MEMORY.md` + `USER.md` | Bộ nhớ persistent |
| `cron/jobs.json` | Cấu hình cron jobs |
| `scripts/` | Scripts tự động hóa (64KB) |
| `hooks/` | Hooks tùy chỉnh |
| `plugins/` | Plugins (4.7MB) |
| `SOUL.md` | Personality file |
| `config.yaml` (redacted) | Config đã xóa API keys |

---

## 📋 Kế Hoạch Thực Hiện — 5 Tasks

### Task 1: Tạo `.gitignore` và cấu hình repo local

**Mục tiêu:** Clone repo về máy, thiết lập `.gitignore` đúng để không push secrets.

**Thực hiện:**
```bash
# Clone repo backup về thư mục riêng
git clone https://github.com/HAHVAC/hermes-agent-backup.git /root/hermes-backup-repo

# Tạo .gitignore
cat > /root/hermes-backup-repo/.gitignore << 'EOF'
# === SECRETS & CREDENTIALS ===
auth.json
auth.lock
google_token.json
google_client_secret.json
*.env
.env*

# === DATABASE & RUNTIME STATE ===
state.db
state.db-shm
state.db-wal
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
pairing/
sandboxes/
whatsapp/

# === LARGE SOURCE CODE ===
hermes-agent/

# === SNAPSHOTS (chứa auth.json) ===
state-snapshots/
migration/

# === DYNAMIC DATA (không cần backup) ===
cron/output/
skills/openclaw-imports/news-aggregator-skill/briefing_data*.json
skills/openclaw-imports/news-aggregator-skill/briefing_data_final.json
email_attachments/
kanban.db
slak-manifest.json
channel_directory.json
EOF
```

**Verification:** `cat /root/hermes-backup-repo/.gitignore` — kiểm tra đủ 5 section.

---

### Task 2: Tạo script backup `hermes_backup.sh`

**Mục tiêu:** Script rsync từ `~/.hermes/` → repo local → commit → push.

**File:** `~/.hermes/scripts/hermes_backup.sh`

```bash
#!/bin/bash
# Hermes Agent GitHub Backup Script
# Chạy hàng ngày lúc 02:00 GMT+7

set -euo pipefail

HERMES_DIR="$HOME/.hermes"
BACKUP_REPO="/root/hermes-backup-repo"
LOG_FILE="/tmp/hermes_backup_$(date +%Y%m%d).log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S %Z')

echo "[$TIMESTAMP] Starting Hermes backup..." | tee "$LOG_FILE"

# Bước 1: Rsync ~/.hermes/ → backup repo (tôn trọng .gitignore)
rsync -av --delete \
  --exclude='.git' \
  --filter=':- .gitignore' \
  "$HERMES_DIR/" "$BACKUP_REPO/" \
  >> "$LOG_FILE" 2>&1

# Bước 2: Redact config.yaml (xóa API key trước khi commit)
if [ -f "$BACKUP_REPO/config.yaml" ]; then
  sed -i 's/api_key:.*/api_key: REDACTED/g' "$BACKUP_REPO/config.yaml"
  echo "[INFO] config.yaml redacted" | tee -a "$LOG_FILE"
fi

# Bước 3: Git commit & push
cd "$BACKUP_REPO"
git add -A

# Chỉ commit nếu có thay đổi
if git diff --cached --quiet; then
  echo "[$TIMESTAMP] No changes detected. Skipping commit." | tee -a "$LOG_FILE"
  exit 0
fi

COMMIT_MSG="backup: $(date '+%Y-%m-%d %H:%M') GMT+7 — auto backup"
git commit -m "$COMMIT_MSG" >> "$LOG_FILE" 2>&1
git push origin main >> "$LOG_FILE" 2>&1

echo "[$TIMESTAMP] Backup completed successfully." | tee -a "$LOG_FILE"
```

**Verification:** `bash -n ~/.hermes/scripts/hermes_backup.sh` — syntax OK.

---

### Task 3: Test chạy thủ công lần đầu

**Mục tiêu:** Verify script hoạt động, không push secrets.

```bash
chmod +x ~/.hermes/scripts/hermes_backup.sh
bash ~/.hermes/scripts/hermes_backup.sh

# Kiểm tra repo sau backup
cd /root/hermes-backup-repo
git log --oneline -3
git show --stat HEAD

# Double-check: không có secrets
grep -r "sk-\|gho_\|ya29\." . --include="*.yaml" --include="*.json" 2>/dev/null | grep -v ".git" || echo "✅ No secrets found"
```

**Expected:** 1 commit mới, `config.yaml` có `api_key: REDACTED`, không có file `auth.json`.

---

### Task 4: Tạo Cron Job tự động hàng ngày

**Mục tiêu:** Chạy backup mỗi ngày lúc 02:00 GMT+7 (19:00 UTC).

**Cron schedule:** `0 19 * * *` (19:00 UTC = 02:00 GMT+7)

**Cron job config:**
- Name: `🔄 Hermes Backup → GitHub Daily`
- Script: `hermes_backup.sh`
- Schedule: `0 19 * * *`
- Delivery: `local` (không cần notify, chỉ log)
- Model: không cần LLM (`no_agent: true`)

---

### Task 5: Thêm README.md vào repo backup

**Mục tiêu:** Tài liệu hóa nội dung backup.

**File:** `/root/hermes-backup-repo/README.md`

```markdown
# Hermes Agent Backup

Auto-backup của workspace Hermes Agent trên server HAHVAC.

## Nội dung được backup
- `skills/` — Toàn bộ skills (prompts, workflows)
- `memories/` — Bộ nhớ persistent (MEMORY.md, USER.md)
- `cron/jobs.json` — Cấu hình cron jobs
- `scripts/` — Scripts tự động hóa
- `hooks/` — Custom hooks
- `plugins/` — Plugins
- `SOUL.md` — Personality configuration
- `config.yaml` (API keys đã redact)

## Không backup (loại trừ)
- Secrets: `auth.json`, `google_token.json`, API keys
- Sessions & cache: `sessions/`, `cache/`, `logs/`
- Source code Hermes: `hermes-agent/`
- Runtime state: DB files, PID files

## Lịch backup
Hàng ngày lúc **02:00 GMT+7** (19:00 UTC).

## Khôi phục
```bash
git clone https://github.com/HAHVAC/hermes-agent-backup.git
rsync -av hermes-agent-backup/ ~/.hermes/
# Khôi phục auth.json + google_token.json từ nơi lưu trữ an toàn riêng
```
```

---

## 🗂️ Tóm Tắt Kế Hoạch

```
Task 1: Tạo .gitignore → bảo vệ secrets
Task 2: Viết script hermes_backup.sh → rsync + redact + push
Task 3: Test thủ công → verify an toàn
Task 4: Tạo cron job → tự động hàng ngày 02:00 GMT+7
Task 5: Thêm README.md → tài liệu hóa
```

**Thời gian ước tính:** 15–20 phút thực hiện
**Rủi ro:** API key trong `config.yaml` → xử lý bằng `sed` redact tự động trước commit
**Lưu ý:** `auth.json` chứa toàn bộ provider tokens — KHÔNG bao giờ được commit
