---
name: lark-cli
description: Official Lark/Feishu CLI tool (larksuite/cli) — 200+ commands covering Messenger, Docs, Base, Sheets, Calendar, Mail, Tasks, Approval, Meetings and more. Use for all Lark/Feishu interactions. 23 AI Agent Skills installed at ~/.agents/skills/lark-*.
version: 1.0.23
tags: [lark, feishu, calendar, base, task, approval, im, mail, sheets, docs]
---

# lark-cli — Official Lark/Feishu CLI

⚠️ **CRITICAL KNOWN BUG 26/04/2026**: Markdown import / document content push API currently only creates empty document headers and does NOT push actual content. This is an official upstream bug in lark CLI. Do not attempt automated markdown import. Prepare formatted content and instruct user to paste manually.

CLI chính chủ từ larksuite team. Đã cài và config cho tài khoản **TA Mẫn Văn Hà** (app: `cli_a950ce435521ded1`).

## Setup Status

- ✅ Installed: `lark-cli v1.0.23` (npm global, latest available: v1.0.27)
- ✅ Config: `/root/.lark-cli/config.json` — App ID `cli_a950ce435521ded1`
- ✅ Auth: user identity logged in (`lark-cli auth status`)
- ✅ 23 Agent Skills: `~/.agents/skills/lark-*`

## QUAN TRỌNG — Đọc skill chính chủ trước

Trước khi thực hiện bất kỳ tác vụ Lark nào, **phải đọc skill tương ứng** tại `~/.agents/skills/`:

```bash
cat ~/.agents/skills/lark-shared/SKILL.md      # Auth, identity, permission — ĐỌC TRƯỚC
cat ~/.agents/skills/lark-im/SKILL.md          # Chat, messages, groups
cat ~/.agents/skills/lark-base/SKILL.md        # Lark Base (tables, records)
cat ~/.agents/skills/lark-calendar/SKILL.md    # Calendar, events
cat ~/.agents/skills/lark-task/SKILL.md        # Tasks
cat ~/.agents/skills/lark-approval/SKILL.md    # Approval workflows
cat ~/.agents/skills/lark-mail/SKILL.md        # Mail
cat ~/.agents/skills/lark-sheets/SKILL.md      # Sheets
cat ~/.agents/skills/lark-doc/SKILL.md         # Docs
cat ~/.agents/skills/lark-contact/SKILL.md     # User lookup
```

## Command Structure — 3 lớp

### 1. Shortcuts (khuyến dùng — AI-friendly)
Prefix `+`, smart defaults, output đẹp:
```bash
lark-cli calendar +agenda
lark-cli im +messages-send --chat-id "oc_xxx" --text "Hello"
lark-cli im +chat-search --keyword "GOERTEK"
lark-cli im +chat-messages-list --chat-id "oc_xxx" --limit 50
lark-cli base +record-list --app-token "xxx" --table-id "tbl_xxx"
lark-cli task +task-list
lark-cli approval +task-list
```

### 2. API Commands (1:1 với platform API)
```bash
lark-cli calendar events list
lark-cli im chats list
lark-cli base apps list
```

### 3. Raw API (2500+ endpoints)
```bash
lark-cli api GET /open-apis/im/v1/chats
lark-cli api POST /open-apis/im/v1/messages --params '{"receive_id_type":"chat_id"}' \
  --data '{"receive_id":"oc_xxx","msg_type":"text","content":"{\"text\":\"Hi\"}"}'
```

## Identity — User vs Bot

```bash
lark-cli calendar +agenda --as user    # Xem lịch của user (mặc định)
lark-cli im +messages-send --as bot    # Gửi tin với danh nghĩa bot/app
```

- **User identity**: truy cập tài nguyên cá nhân (lịch, cloud docs, inbox)
- **Bot identity**: gửi tin nhắn app, truy cập tài nguyên app

## Output Formats
```bash
--format json      # JSON đầy đủ (mặc định)
--format pretty    # Human-friendly
--format table     # Bảng dễ đọc
--format ndjson    # Pipe-friendly
```

## Pagination
```bash
--page-all          # Lấy tất cả pages
--page-limit 5      # Tối đa 5 pages
```

## Auth Refresh

Token hết hạn sau ~2h, refresh token 7 ngày. Khi gặp lỗi auth:
```bash
lark-cli auth status                          # Kiểm tra
lark-cli auth login --recommend --no-wait     # Lấy URL → gửi cho user
lark-cli auth login --device-code <CODE>      # Hoàn thành login
```

## Installation (AI Agent flow)

```bash
# Step 1: Install CLI + Skills
npm install -g @larksuite/cli
npx skills add larksuite/cli -y -g

# Step 2: Config init — chạy background, extract URL gửi user
lark-cli config init --new > /tmp/lark_init.log 2>&1 &
sleep 5 && cat /tmp/lark_init.log   # URL dạng: https://open.feishu.cn/page/cli?user_code=XXXX

# Step 3: Sau khi user xong trên browser, kiểm tra:
cat /tmp/lark_init.log | tail -5    # Tìm "appSecret" = thành công

# Step 4: Auth login — chạy --no-wait để lấy URL ngay
lark-cli auth login --recommend --no-wait > /tmp/lark_login.log 2>&1 &
sleep 5 && cat /tmp/lark_login.log  # Lấy verification_url gửi user

# Step 5: Poll với device-code (blocks đến khi user xác nhận)
lark-cli auth login --device-code "<CODE_FROM_LOG>"

# Step 6: Verify
lark-cli auth status
lark-cli config show
```

## Pitfalls

- **config init timeout**: Process timeout sau ~200 poll (~10 phút). Nếu user chưa kịp làm xong, chạy lại `lark-cli config init --new` — URL mới sẽ được tạo.

- **Cross-tenant chats (error 230027)**: Gửi tin vào nhóm có `"external": true` luôn trả về `{"code": 230027, "message": "Permission denied"}` — đây là giới hạn cứng của Lark platform, không phải lỗi token. Kiểm tra bằng `lark-cli im +chat-search --query "<tên>" --as user`. Workaround: gửi vào nhóm nội bộ (`"external": false`).

- **Lệnh gửi tin đúng**: `lark-cli im +messages-send --chat-id <oc_xxx> --as user --text "msg"`. Dùng `--text` cho plain text; `--content` yêu cầu JSON hợp lệ. Cờ `--identity` không tồn tại — dùng `--as`.

- **PATH**: lark-cli nằm tại `/root/.nvm/versions/node/v24.13.0/bin/lark-cli`; cần thêm vào PATH trước khi gọi.
- **Lark quốc tế config URL**: Với workspace quốc tế, chạy `lark-cli config init --new --brand lark --lang en`. CLI vẫn có thể in link `https://open.feishu.cn/page/cli?...`; nếu user dùng Lark international và gặp Server error, đổi domain thủ công sang `https://open.larksuite.com/page/cli?...` giữ nguyên query (`user_code`, `lpv`, `ocv`, `from`).
- **Hermes bind may be bot-only**: `lark-cli config bind --source hermes` có thể tạo config `identity=bot-only`/strict bot, khiến `auth login --domain base` bị từ chối. Nếu cần ghi bằng user identity, chạy lại `config init --new --brand lark --lang en` để có app config Lark, rồi `lark-cli auth login --domain base`.
- **Base bot write 91403**: Ngay cả khi bot đọc được fields/records và user đã cấp quyền chỉnh sửa Base, ghi record có thể trả `91403 you don't have permission`. Chuyển sang user identity bằng `lark-cli auth login --domain base` rồi chạy `base +record-upsert --as user`.
- **config init success detection**: Không có exit message rõ ràng. Dấu hiệu thành công là log có `"appSecret": "****"` hoặc `OK: App configured! App ID: ...`. Poll bằng `process wait/log` hoặc `cat /tmp/lark_init.log | tail -5`.
- **Token expiry**: `expiresAt` ~2h, refresh token 7 ngày. Refresh tự động nếu còn trong hạn. Quá 7 ngày phải login lại.
- **Bot vs User**: Bot KHÔNG thấy tài nguyên user (lịch, docs cá nhân) và có thể không ghi được Base dù đọc được. Luôn dùng `--as user` cho tài nguyên cá nhân hoặc khi bot ghi Base gặp 91403.
- **Permission denied**: Đọc `permission_violations` trong error JSON, dùng `console_url` để mở developer console cấp scope. Nếu lỗi là `91403 you don't have permission` khi bot đã có scope nhưng không ghi được Base, nguyên nhân thường là bot/app chưa có quyền tài nguyên; chuyển sang user auth (`lark-cli auth login --domain base`) rồi chạy với `--as user`, hoặc yêu cầu cấp quyền trực tiếp cho app/bot vào Base.
- **Lark quốc tế vs Feishu**: Khi chạy `lark-cli config init --new --brand lark --lang en`, CLI vẫn có thể in link `https://open.feishu.cn/page/cli?...`. Với workspace Lark quốc tế, đổi domain thủ công sang `https://open.larksuite.com/page/cli?...` và giữ nguyên query (`user_code`, `lpv`, `ocv`, `from`). Link Feishu có thể báo Server error.
- **chat-id**: Dùng `lark-cli im +chat-search --query "TÊN_NHÓM"` để tìm chat_id (flag là `--query`, KHÔNG phải `--keyword`).
- **sheets +create**: Không có `--format` flag và không có `--sheet-title`. Dùng `--title` cho tên file, `--headers` cho header row.
- **Base shortcuts may not accept --format**: Một số `lark-cli base +...` shortcut không nhận `--format`; mặc định đã trả JSON, bỏ flag này nếu gặp `unknown flag: --format`.
- **drive +download output path**: `lark-cli drive +download --output` không cho absolute path; phải `cd` vào thư mục đích rồi dùng relative path, ví dụ `mkdir -p /tmp/lark_file && cd /tmp/lark_file && lark-cli drive +download --file-token <token> --output ./downloaded --overwrite`. Link dạng `/file/<token>` có thể tải trực tiếp bằng `drive +download --file-token <token>`; nếu thiếu tên/đuôi file, dùng `file ./downloaded` để xác định loại.
- **im +chat-messages-list**: Không có `--limit` flag. Dùng `--page-size` (max 50).
- **Dry run**: Dùng `--dry-run` để preview trước khi thực thi các lệnh có side effect.
- **23 Skills location**: Cài tại `~/.agents/skills/lark-*`. Đọc skill tương ứng trước khi dùng API (`cat ~/.agents/skills/lark-im/SKILL.md`).
- **❌ Doc shortcut typo**: Không có lệnh `lark-cli doc +create`. Đúng lệnh là `lark-cli docs +create` (số nhiều). Đây là lỗi phổ biến nhất, CLI trả lỗi `unknown command "doc" for "lark-cli"`.

## Known Working Config (Thăng Long)
- App ID: `cli_a950ce435521ded1`
- Config: `/root/.lark-cli/config.json`
- User: TA Mẫn Văn Hà (`ou_49810a6bc1eec25883d0d0807b57bcfe`)
- Feishu domain: `pccctruongan.sg.larksuite.com`
