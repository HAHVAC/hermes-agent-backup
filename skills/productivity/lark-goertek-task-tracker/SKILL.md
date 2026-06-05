---
name: lark-goertek-task-tracker
description: "Quản lý các nhóm Lark GOERTEK (giao việc, báo cáo tiến độ, tài liệu). Tracker quét GOERTEK_TRAO ĐỔI CÔNG VIỆC lúc 19:00 VN, nhận diện giao việc (@mention), ghi Lark Sheet, gửi DM. Cũng dùng khi cần đọc/tìm kiếm tin nhắn trong nhóm GOERTEK_BÁO CÁO CÔNG VIỆC hoặc GOERTEK_BẢN VẼ."
triggers:
  - theo dõi nhóm goertek
  - quét giao việc lark
  - nhắc việc feishu
  - báo cáo hiện trường goertek
  - đọc tin nhắn nhóm goertek
  - báo cáo ktx
  - báo cáo tiến độ ktx
  - ktx daily report
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

## KTX Daily Report (Báo cáo tiến độ thi công KTX)

Tự động tổng hợp tin nhắn từ thread KTX-Báo cáo, phân loại theo 4 hệ thống (Báo cháy, Chữa cháy, Thông gió, Điện), và cập nhật vào 1 Lark Doc duy nhất mỗi ngày.

Xem chi tiết sender mapping, từ khóa phân loại hệ thống, và hướng dẫn mở rộng tại [ktx-daily-report.md](references/ktx-daily-report.md).

| Mục | Giá trị |
|-----|---------|
| Thread KTX | `omt_196c1eaf68cf1981` (trong nhóm GOERTEK_BÁO CÁO CÔNG VIỆC) |
| Lark Doc ID | `KD8Xd3KUjouzhzxq2xolyWAmgkI` |
| Doc URL | https://pccctruongan.sg.larksuite.com/docx/KD8Xd3KUjouzhzxq2xolyWAmgkI |
| Script | `/root/.hermes/scripts/ktx_daily_report.py` |
| Cron | `0 13 * * *` (UTC) = 20:00 VN |
| Cron Job ID | `865fd3e18751` |

### ⚠️ Quan trọng: Tránh lỗi phân phối tin nhắn và tin rác từ Cron Job
- **Cấu hình `deliver` cho KTX Daily Report:** Phải sử dụng Feishu chat ID cụ thể (ví dụ cá nhân của Boss: `feishu:oc_e6167ab9a7424fab1a2db2442fd98581`) thay vì các phương thức chung chung hay bare channel khi chạy cron, nhằm tránh lỗi `delivery error: Feishu send failed: [99992402] field validation failed`.
- **Tránh spam tin rác:** Prompt của cron job cần quy định rõ điều kiện: "Nếu ngày hôm đó không có bất kỳ báo cáo mới nào (0 báo cáo, 0 ảnh), trả về chính xác chuỗi `[SILENT]`". Điều này giúp hệ thống tự động lọc bỏ và không gửi tin nhắn rác cho Boss.

### Cách đọc thread messages

Dùng `lark-cli im +threads-messages-list` để đọc trực tiếp tin nhắn trong thread:
```bash
lark-cli im +threads-messages-list --thread omt_196c1eaf68cf1981 --as user --sort desc --page-size 50 --format json
```

### Cách resolve tên người gửi

`+threads-messages-list` không trả kèm `sender.name`. Dùng `+messages-mget` để lấy enriched data (bao gồm thread replies gốc có chứa `mentions` với tên):
```bash
lark-cli im +messages-mget --message-ids om_xxx,om_yyy --as user --format json
```
Trong enriched output, `thread_replies` chứa tin nhắn gốc của thread với `mentions[].name` — đây là nguồn resolve open_id → tên thật.

### Logic phân loại hệ thống

Script dùng keyword matching để phân loại tin nhắn vào 4 hệ. Xem đầy đủ keyword list trong [ktx-daily-report.md](references/ktx-daily-report.md).

### Flow hàng ngày

1. Cron 20:00 VN → chạy script
2. Script đọc thread messages của ngày hôm nay (VN time)
3. Phân loại theo hệ, extract Zone/Tầng
4. Append XML vào Lark Doc
5. Cron job gửi tóm tắt vào chat cho Boss duyệt

### ⚠️ Pitfall: Thread messages không có thread_id field khi dùng +chat-messages-list

Khi list tin nhắn group bằng `+chat-messages-list`, một số tin nhắn có `thread_id` field, nhưng tin nhắn trong thread (replies) thì không trả field này khi được list từ group-level. Phải dùng `+threads-messages-list` với thread_id hoặc `+messages-mget` để đảm bảo lấy đúng nội dung thread.

### ⚠️ Pitfall: Append tạo duplicate nếu chạy lại cùng ngày

Script hiện không check xem báo cáo ngày đó đã tồn tại trong doc chưa. Nếu cần chạy lại, nên tạo doc mới hoặc manually xóa duplicate. Script nhận tham số ngày: `python3 ktx_daily_report.py 2026-06-04`.
