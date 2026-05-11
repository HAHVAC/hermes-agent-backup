---
name: lark-goertek-task-tracker
description: Quét tin nhắn nhóm GOERTEK_TRAO ĐỔI CÔNG VIỆC lúc 19:00 VN, nhận diện giao việc (@mention), ghi Lark Sheet, gửi DM cho từng người được giao
triggers:
  - theo dõi nhóm goertek
  - quét giao việc lark
  - nhắc việc feishu
---

# GOERTEK Task Tracker

## Thông tin cố định

| Mục | Giá trị |
|-----|---------|
| Nhóm chat | GOERTEK_TRAO ĐỔI CÔNG VIỆC |
| Chat ID | `oc_c00846108437ef7596beaec09dfccbed` |
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

## Lưu ý

- Quyền cần có: `im:message`, `im:message.send_as_user`, `sheets:spreadsheet`
- App ID: `cli_a950ce435521ded1`
- Login user: TA Mẫn Văn Hà
- Lark CLI version: v1.0.23 (latest v1.0.27 available — có thể nâng cấp)
- Lệnh gửi đúng: `lark-cli im +messages-send --chat-id <id> --as user --text "<msg>"`
  - Không dùng `lark im send` (sai lệnh)
  - `--text` thay vì `--content` (content yêu cầu JSON hợp lệ)
- PATH cần có: `/root/.nvm/versions/node/v24.13.0/bin`
