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

**1. [Tiêu đề — dịch sang tiếng Việt nếu là tiếng Anh/Trung]**
- **Từ:** ...
- **Thời gian:** ...
- **Nội dung:** [Tóm tắt/trích nội dung chính — nếu là tiếng Anh hoặc tiếng Trung thì dịch sang tiếng Việt. Bỏ qua link, chữ ký, footer]
- **Tệp đính kèm:**
  - `[Tên file gốc]` → **[Dịch nghĩa tên file sang tiếng Việt]** · **Lưu Drive:** [Đã lưu: link Drive / hoặc Chưa lưu được: lý do ngắn gọn / hoặc Đã lưu cục bộ, chưa tải lên Drive được: lý do ngắn gọn]
  - [Nếu là PDF]: **Tóm tắt PDF:** [3-5 gạch đầu dòng nội dung chính bằng tiếng Việt / hoặc "Không trích xuất được nội dung PDF" nếu không có thông tin]

---

## II. 📤 Thư đã gửi ({sent_count} email)

**1. [Tiêu đề — dịch sang tiếng Việt nếu là tiếng Anh/Trung]**
- **Đến:** ...
- **Thời gian:** ...
- **Nội dung:** [Tóm tắt/trích nội dung chính — nếu là tiếng Anh hoặc tiếng Trung thì dịch sang tiếng Việt. Bỏ qua link, chữ ký, footer]
- **Tệp đính kèm:**
  - `[Tên file gốc]` → **[Dịch nghĩa tên file sang tiếng Việt]** · **Lưu Drive:** [Đã lưu: link Drive / hoặc Chưa lưu được: lý do ngắn gọn / hoặc Đã lưu cục bộ, chưa tải lên Drive được: lý do ngắn gọn]
  - [Nếu là PDF]: **Tóm tắt PDF:** [3-5 gạch đầu dòng nội dung chính bằng tiếng Việt / hoặc "Không trích xuất được nội dung PDF" nếu không có thông tin]
```

**Quy tắc format:**
- Tiêu đề email, nội dung email, và tên file đính kèm PHẢI dịch sang tiếng Việt nếu là tiếng Anh hoặc tiếng Trung.
- Với mỗi tệp đính kèm: luôn nêu tên file gốc + bản dịch nghĩa tiếng Việt của tên file.
- Với file PDF: tóm tắt nội dung chính của PDF (nếu có trường dữ liệu text); nếu không trích xuất được text thì ghi ngắn gọn: "Không trích xuất được nội dung PDF".
- Với Drive: nếu trạng thái là `uploaded`, ghi "Đã lưu" kèm `drive_link`; nếu upload lỗi, ghi "Đã lưu cục bộ, chưa tải lên Drive được" và lý do ngắn gọn (không hiển thị đường dẫn cục bộ).
- KHÔNG hiển thị URL/link trong nội dung email; chỉ được hiển thị link Drive của tệp đính kèm khi upload thành công.
- KHÔNG hiển thị chữ ký, footer, cuống thư.
- Nội dung tóm tắt email ngắn gọn, đủ ý, tối đa 3-4 dòng mỗi email.
- Nếu không có email nào: ghi "✅ Không có email trong 24h qua".

## Script: clean_body() — lọc footer

Script dùng heuristic lọc các dòng chứa: `unsubscribe`, `https://`, `www.`, `©`, `sent from my`, `---`, `___` ... để loại link/chữ ký trước khi đưa vào JSON.

## Tệp đính kèm (cập nhật 26/04/2026)

Script `/root/.hermes/scripts/daily_email_report.py` hiện xử lý attachment như sau:
- **KHÔNG tải, KHÔNG lưu local, KHÔNG upload Drive, KHÔNG đọc PDF** (đã bỏ để tránh timeout và soft guard chặn vì cần xác nhận của người dùng)
- Chỉ liệt kê metadata: `filename`, `mime_type`, `size_bytes`
- Prompt AI phải dịch nghĩa tên file sang tiếng Việt trong báo cáo, nhưng vẫn giữ tên file gốc

## Gmail Search & Slashes Pitfall
- **Symptom**: Gmail search matches alphanumeric terms but fails or drops messages when query contains slashes or complex special characters (e.g. searching exact file/reference IDs like `"3604/TD-PCCC"` or `"29/TD"`).
- **Fix**: Search for the alphanumeric fragments separately (e.g., query `"3604"` AND `"TD-PCCC"`, or search for broader keywords like `"Thái Bình"` / `"thẩm duyệt"`) and then parse and filter the returned messages in Python code to match the exact string.

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
