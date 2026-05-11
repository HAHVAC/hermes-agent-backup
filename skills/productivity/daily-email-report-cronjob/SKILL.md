---
name: daily-email-report-cronjob
description: Cron job báo cáo email hàng ngày cho pcccthanglong.tlc@gmail.com — gửi vào nhóm Lark BÁO CÁO EMAIL lúc 20:00 tối (GMT+7). Script thu thập raw JSON, AI prompt dịch + format Markdown.
tags: [email, gmail, cronjob, lark, report, daily]
---

# Daily Email Report Cron Job — Thăng Long

## Thông tin cố định

| Thông số | Giá trị |
|---|---|
| Job ID | `bfa0b5c4fd56` |
| Gmail account | `pcccthanglong.tlc@gmail.com` |
| Schedule | `0 13 * * *` (13:00 UTC = 20:00 GMT+7) — **chạy lúc 20:00 VN** |
| Deliver | `feishu:oc_909e2f33b96a2bfd5da948caf8563d95` (nhóm **BÁO CÁO EMAIL**) |
| Script | `/root/.hermes/scripts/daily_email_report.py` |

> ✅ Schedule `0 13 * * *` = 13:00 UTC = **20:00 GMT+7**.

## Kiến trúc: Tách script và prompt

**Pattern quan trọng:** Script chỉ thu thập và output **raw JSON** — KHÔNG format text. AI prompt nhận JSON và xử lý dịch thuật + format Markdown.

```
Script (Python) → raw JSON → AI prompt → Markdown report → Lark group
```

Lý do:
- Script chạy nhanh, deterministic
- AI xử lý dịch tiếng Anh/Trung → Việt tốt hơn khi có đủ context
- Dễ thay đổi format mà không sửa script

## Format báo cáo (đã chốt với anh)

```markdown
📧 **BÁO CÁO EMAIL HÀNG NGÀY**
**Tài khoản:** pcccthanglong.tlc@gmail.com
**📅 {day}, {date} | Cập nhật lúc {time} (GMT+7)**
**📊 Tổng quan:** {inbox_count} thư đến · {sent_count} thư đã gửi

---

## I. 📥 Hộp thư đến ({inbox_count} email)

**1. [Tiêu đề dịch tiếng Việt]**
- **Từ:** ...
- **Thời gian:** ...
- **Nội dung:** [tóm tắt, dịch VN]

---

## II. 📤 Thư đã gửi ({sent_count} email)

**1. [Tiêu đề dịch tiếng Việt]**
- **Đến:** ...
- **Thời gian:** ...
- **Nội dung:** [tóm tắt, dịch VN]
```

**Quy tắc format:**
- Tiêu đề + nội dung PHẢI dịch sang tiếng Việt nếu là tiếng Anh/Trung
- KHÔNG hiển thị URL, link, chữ ký, footer, cuống thư
- Nội dung tóm tắt ngắn gọn, tối đa 3-4 dòng/email

## Script: clean_body() — lọc footer

Script dùng heuristic lọc các dòng chứa: `unsubscribe`, `https://`, `www.`, `©`, `sent from my`, `---`, `___` ... để loại link/chữ ký trước khi đưa vào JSON.

## Tệp đính kèm (cập nhật 26/04/2026)

Script `/root/.hermes/scripts/daily_email_report.py` hiện xử lý attachment như sau:
- **KHÔNG tải, KHÔNG lưu local, KHÔNG upload Drive, KHÔNG đọc PDF** (đã bỏ để tránh timeout)
- Chỉ liệt kê metadata: `filename`, `mime_type`, `size_bytes`
- Prompt AI phải dịch nghĩa tên file sang tiếng Việt trong báo cáo, nhưng vẫn giữ tên file gốc

## Cập nhật cron job

```bash
# Xem job hiện tại
mcp_cronjob(action='list')

# Chạy thử ngay
mcp_cronjob(action='run', job_id='bfa0b5c4fd56')

# Đổi delivery target
mcp_cronjob(action='update', job_id='bfa0b5c4fd56', deliver='feishu:oc_xxx')

# Tìm chat_id nhóm Lark
lark-cli im +chat-search --query "TÊN_NHÓM" --format json
```

## Pitfalls

- **Schedule UTC vs GMT+7**: `0 13 * * *` = 20:00 VN. Nếu muốn giờ Việt khác, luôn đổi từ UTC sang GMT+7 trước khi set cron
- **Script output phải là valid JSON**: Nếu script print thêm gì ngoài JSON (debug log, progress), AI prompt sẽ bị lỗi parse
- **gmail search `newer_than:1d`**: Lấy 24h gần nhất tính từ lúc chạy, không phải ngày calendar
