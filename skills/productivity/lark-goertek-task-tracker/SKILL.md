---
name: lark-goertek-task-tracker
description: "Quản lý các nhóm Lark GOERTEK (giao việc, báo cáo tiến độ, tài liệu). Tracker quét GOERTEK_TRAO ĐỔI CÔNG VIỆC lúc 19:00 VN, nhận diện giao việc (@mention), ghi Lark Sheet, gửi DM. Cũng dùng khi cần đọc/tìm kiếm tin nhắn trong nhóm GOERTEK_BÁO CÁO CÔNG VIỆC hoặc GOERTEK_BẢN VẼ."
triggers:
  - theo dõi nhóm goertek
  - quét giao việc lark
  - nhắc việc feishu
  - báo cáo hiện trường goertek
  - đọc tin nhắn nhóm goertek
---

# GOERTEK Task Tracker

Xem chi tiết cách tìm kiếm thread và thông tin chủ đề KTX tại [goertek-threads.md](references/goertek-threads.md).

## Các nhóm Goertek

| Nhóm | Chat ID | External | Ghi chú |
|------|---------|----------|---------|
| GOERTEK_TRAO ĐỔI CÔNG VIỆC | `oc_c00846108437ef7596beaec09dfccbed` | ✅ | Nhóm chính để giao việc, có cron tracker |
| GOERTEK_BÁO CÁO CÔNG VIỆC | `oc_c999ede161bd4f500eb83c8dfaf92dd0` | ✅ | Báo cáo tiến độ hiện trường, ~5000+ tin nhắn |
| GOERTEK_BẢN VẼ, HỒ SƠ, TÀI LIỆU | `oc_efd5beedc7f525f57e6c182f3562429a` | ✅ | Tài liệu/bản vẽ |

Cả 3 nhóm đều external (tenant Goertek `7468234470941409312`), owner `ou_49810a6bc1eec25883d0d0807b57bcfe`.

## Thông tin cố định (Task Tracker)

| Mục | Giá trị |
|-----|---------|
| Lark Sheet Token | `WmeUsSghGhoYH8tAMqcleIMIgJf` |
| Sheet URL | https://pccctruongan.sg.larksuite.com/sheets/WmeUsSghGhoYH8tAMqcleIMIgJf |
| Cron | `0 12 * * *` (UTC) = 19:00 VN |
| Script | `/root/.hermes/scripts/goertek_task_tracker.py` |

## Cột Lark Sheet

STT | Nội dung công việc | Người giao | Người được giao | Hạn hoàn thành | Tình trạng | Ghi chú | Ngày giao

## Logic nhận diện giao việc

1. Tin nhắn có **@mention** ít nhất 1 người
2. Nội dung chứa từ khoá công việc: làm, hoàn thành, gửi, kiểm tra, chuẩn bị, báo cáo, xử lý, liên hệ, thực hiện, phụ trách, deadline, trước ngày, v.v.
3. **Người giao** = sender của tin nhắn
4. **Người được giao** = các @mention trong tin
5. **Hạn hoàn thành** = tự extract ngày từ nội dung (regex: ngày DD/MM, trước DD.MM.YYYY, v.v.)
6. Tránh duplicate: check nội dung + sender + timestamp đã ghi chưa

## Gửi DM cá nhân

- Dùng `lark-cli im +messages-send --chat-id <user_open_id> --as user --text "..."`
- **Cross-tenant (Goertek)**: KHÔNG gửi được vào bất kỳ nhóm nào có `"external": true` — lỗi **230027 Permission denied**. Đây là hạn chế cứng của Lark API, không phải lỗi token.
- **Nội bộ Thăng Long**: gửi DM thành công

## ⚠️ Pitfall: Cross-tenant error 230027

Khi gửi vào nhóm Goertek (external, tenant_key `7468234470941409312`), API trả về:
```
{"code": 230027, "message": "Permission denied"}
```
Nguyên nhân: nhóm `external: true` không cho phép gửi tin qua API của tenant khác.

**Workaround đã xác nhận:** Gửi báo cáo vào nhóm nội bộ thay thế:
- Nhóm: **CÔNG TY CP CƠ ĐIỆN VÀ PCCC TRƯỜNG AN**
- Chat ID: `oc_622742929d2cc9f410fb22de6ff07c68`
- `"external": false` — gửi thành công

Báo cáo cuối ngày khi không có giao việc mới → gửi vào nhóm nội bộ này.

## ⚠️ Pitfall: External chat API limitations

Nhóm external (`"external": true`, cross-tenant) có các hạn chế API:

1. **`chats.get` lỗi 232033**: "The operator or invited bots does NOT have the authority to manage external chats." → Cả user lẫn bot identity đều lỗi. Không lấy được chi tiết nhóm.
2. **`+chat-messages-list --as user` vẫn hoạt động**: Có thể đọc tin nhắn bình thường bằng user identity. Đây là cách duy nhất để đọc nội dung nhóm external.
3. **`+messages-search` cần scope `search:message`**: Nếu chưa authorize scope này thì không tìm kiếm nội dung được. **Workaround**: Dùng `+chat-messages-list` phân trang + grep nội dung.
4. **Bot không search được external**: `+chat-search --as bot` trả về 0 kết quả cho nhóm external. Luôn dùng `--as user` để tìm nhóm external.

## Lưu ý

- Quyền cần có: `im:message`, `im:message.send_as_user`, `sheets:spreadsheet`
- App ID: `cli_a950ce435521ded1`
- Login user: TA Mẫn Văn Hà
- Lark CLI version: v1.0.46 (latest v1.0.47 available)
- Lệnh gửi đúng: `lark-cli im +messages-send --chat-id <id> --as user --text "<msg>"`
  - Không dùng `lark im send` (sai lệnh)
  - `--text` thay vì `--content` (content yêu cầu JSON hợp lệ)
- PATH cần có: `/root/.nvm/versions/node/v24.13.0/bin`
