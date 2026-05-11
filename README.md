# 🤖 Hermes Agent Backup

Auto-backup workspace Hermes Agent trên server HAHVAC, chạy mỗi ngày lúc **02:00 GMT+7**.

## 📦 Nội dung được backup

| Thư mục / File | Mô tả |
|---|---|
| `skills/` | Toàn bộ skills (84 skills, ~13MB) |
| `memories/MEMORY.md` | Bộ nhớ persistent của Agent |
| `memories/USER.md` | Profile người dùng |
| `cron/jobs.json` | Cấu hình cron jobs tự động hóa |
| `scripts/` | Scripts Python/Bash tùy chỉnh |
| `hooks/` | Custom hooks |
| `plugins/` | Plugins (~4.7MB) |
| `SOUL.md` | Personality & persona config |
| `config.yaml` | Config (API keys đã redact) |

## 🚫 Không backup (loại trừ)

- `auth.json` / `auth/` — Provider API keys & tokens
- `google_token.json` — OAuth Google
- `state.db` — SQLite session DB (>200MB)
- `sessions/` — Lịch sử chat
- `cache/` / `audio_cache/` — Cache tạm
- `state-snapshots/` / `migration/` — Snapshots nội bộ
- `email_attachments/` — File đính kèm email
- `hermes-agent/` — Source code Hermes (không cần backup)
- `.env` — Environment variables

## 🔄 Lịch backup

Hàng ngày **02:00 GMT+7** (= 19:00 UTC).  
Script: `~/.hermes/scripts/hermes_backup.sh`  
Cron ID: `d4f11333b3b5`

## 🔧 Khôi phục (Restore)

```bash
# Clone repo về
git clone https://github.com/HAHVAC/hermes-agent-backup.git ~/.hermes-restore

# Copy vào ~/.hermes/
rsync -av ~/.hermes-restore/ ~/.hermes/

# Khôi phục secrets từ nơi lưu trữ an toàn riêng:
# - auth.json (provider API keys)
# - google_token.json + google_client_secret.json
# - Cập nhật lại api_key trong config.yaml
```

## 📊 Thống kê

- **Lần backup đầu tiên:** 2026-05-11
- **Số files:** ~5,696 files
- **Repo:** https://github.com/HAHVAC/hermes-agent-backup (private)
