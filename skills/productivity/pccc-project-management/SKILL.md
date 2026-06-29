---
name: pccc-project-management
description: >
  Quản lý dự án PCCC / MEP / Điện nhẹ cho Công ty CP Cơ điện và PCCC Thăng Long.
  Theo dõi tiến độ, tổng hợp công nợ, báo cáo tuần, checklist nghiệm thu,
  cảnh báo rủi ro工期/pháp lý, hỗ trợ quyết sách dự án. Dùng khi nói về
  "tiến độ dự án", "báo cáo tuần", "công nợ", "nghiệm thu", "rủi ro dự án",
  "pipeline dự án", "deadline", "gói thầu", hoặc "tổng hợp công trình".
version: 1.0.0
author: Doremon / PCCC Thăng Long
license: internal
metadata:
  hermes:
    tags: [pccc, mep, construction, project-management, pipeline, debt-tracking, vietnam]
---

# PCCC Project Management

Quản lý toàn diện pipeline dự án PCCC/MEP/Điện nhẹ cho Công ty Thăng Long.

## Trigger conditions

Dùng skill này khi Boss nói về:
- "Tiến độ dự án / công trình"
- "Báo cáo tuần / friday brief / daily brief"
- "Công nợ / thanh toán / quyết toán"
- "Pipeline dự án / danh sách công trình"
- "Nghiệm thu / checklist nghiệm thu"
- "Rủi ro dự án / pháp lý / chậm tiến độ"
- "Gói thầu / đấu thầu / chào giá"
- "Deadline / lịch thi công"
- "Tổng hợp tình hình các công trình"

## Workflow chính

### 1. Pipeline Review (Review danh sách dự án)

Phân tích sức khỏe toàn bộ pipeline dự án, ưu tiên hành động, phát hiện rủi ro.

**Cách dùng:** "review pipeline", "tổng hợp các công trình", "xem tình hình dự án"

**Input từ Anh:**
- Mô tả các dự án đang thực hiện
- Hoặc paste từ bảng Excel/Lark
- Hoặc nêu tên cụ thể công trình cần review

**Output format:**

```markdown
# Pipeline Dự Án PCCC — [Ngày]

**Tổng dự án:** [N] | **Giá trị pipeline:** [X] tỷ VND
**Đang thi công:** [N] | **Đang nghiệm thu:** [N] | **Đã hoàn thành:** [N]

---

## Pipeline Health Score: [X/100]

| Dimension | Score | Vấn đề |
|-----------|-------|--------|
| **Tiến độ** | [X]/25 | [N] dự án behind schedule |
| **Thanh toán** | [X]/25 | [N] dự án công nợ quá hạn 30+ ngày |
| **Hồ sơ pháp lý** | [X]/25 | [N] dự án thiếu biên bản nghiệm thu che khuất |
| **Phạm vi** | [X]/25 | [N] dự án có phát sinh chưa ký补充协议 |

---

## Ưu tiên hành động tuần này

### 1. [Dự án ưu tiên cao nhất]
**Lý do:** [Lý do — giá trị lớn, deadline gần, rủi ro cao]
**Hành động:** [Bước tiếp theo cụ thể]
**Giá trị:** [X] tỷ VND

### 2. [Dự án thứ hai]
**Lý do:** [Lý do]
**Hành động:** [Bước tiếp theo]

### 3. [Dự án thứ ba]
**Lý do:** [Lý do]
**Hành động:** [Bước tiếp theo]

---

## Phân loại dự án

### Đang thi công — Cần tập trung
| Dự án | Giá trị | Hệ thống | Tiến độ | Deadline | Vấn đề |
|-------|---------|----------|---------|----------|--------|
| [Tên] | [X] tỷ | PCCC/MEP | [%] | [Ngày] | [Mô tả] |

### Đang nghiệm thu / Thanh quyết toán
| Dự án | Giá trị | Còn phải thu | Ngày hết hạn | Trạng thái |
|-------|---------|---------------|--------------|------------|
| [Tên] | [X] tỷ | [X] tỷ | [Ngày] | [Trạng thái] |

### Đã completed / Bảo hành
| Dự án | Giá trị | Hết BH | Ghi chú |
|-------|---------|--------|---------|
| [Tên] | [X] tỷ | [Ngày] | [Ghi chú] |

---

## Cảnh báo rủi ro

### 🔴 Rủi ro cao
| Dự án | Rủi ro | Hành động đề xuất |
|-------|--------|-------------------|
| [Tên] | [Mô tả rủi ro] | [Đề xuất xử lý] |

### 🟡 Cần theo dõi
| Dự án | Vấn đề | Hành động |
|-------|--------|-----------|
| [Tên] | [Mô tả] | [Đề xuất] |

### 🟢 Ổn định
| Dự án | Ghi chú |
|-------|---------|
| [Tên] | Đang đúng tiến độ |
```

---

### 2. Daily Briefing (Tóm tắt ngày)

Tóm tắt công việc dự án trong ngày: meeting, deadline, công nợ sắp đến hạn.

**Cách dùng:** "brief ngày", "hôm nay có gì", "daily brief"

**Output format:**

```markdown
# Daily Brief — [Ngày]

## #1 Ưu tiên hôm nay
**[Việc quan trọng nhất]**
[Lý do và hành động cụ thể]

---

## Công nợ sắp đến hạn (7 ngày)
| Dự án | Khách hàng | Số tiền | Hạn thanh toán | Trạng thái |
|-------|------------|---------|----------------|------------|
| [Tên] | [Chủ đầu tư] | [X] triệu | [Ngày] | [Đã gửi hóa đơn/chưa] |

---

## Deadline thi công
| Dự án | Hệ thống | Deadline | Còn lại | Tiến độ |
|-------|----------|----------|---------|---------|
| [Tên] | [Hệ thống] | [Ngày] | [N] ngày | [%] |

---

## Hành động đề xuất
1. **[Hành động]** — [Lý do]
2. **[Hành động]** — [Lý do]
3. **[Hành động]** — [Lý do]
```

---

### 3. Friday Brief (Báo cáo cuối tuần)

Tóm tắt tuần: thắng/bài học, doanh thu, công nợ, rủi ro, kế hoạch tuần tới.

**Cách dùng:** "friday brief", "báo cáo tuần", "tổng hợp cuối tuần"

**Output format:**

```markdown
# Friday Brief — Tuần [Ngày bắt đầu] → [Ngày kết thúc]

## ✅ Thắng tuần này
• [Thắng 1 — ví dụ: Nghiệm thu xong hệ thống báo cháy toà A]
• [Thắng 2 — ví dụ: Thu được [X] triệu từ dự án Y]
• [Thắng 3]

## ⚠️ Cần theo dõi
• [Vấn đề 1] — [Hành động đề xuất]
• [Vấn đề 2] — [Hành động đề xuất]

## 💰 Doanh thu tuần: [X] triệu VND
• Đã thu: [X] triệu
• Phải thu còn lại: [X] triệu

## 📋 Kế hoạch tuần tới
1. [ ] [Hành động ưu tiên 1]
2. [ ] [Hành động ưu tiên 2]
3. [ ] [Hành động ưu tiên 3]
```

---

### 4. Nghiệm thu Checklist

Checklist nghiệm thu theo hệ thống PCCC/MEP, dựa trên TCVN 3905:2013.

**Cách dùng:** "checklist nghiệm thu [tên dự án]", "nghiệm thu hệ thống [tên]"

**Categories checklist:**

| Category | Mục kiểm tra | Tiêu chuẩn |
|----------|-------------|------------|
| **Hệ thống báo cháy** | Đầu báo khói/nhiệt, chuông, tủ trung tâm | TCVN 5738:2021 |
| **Hệ thống chữa cháy nước** | Sprinkler, van, bơm, bể chứa | TCVN 7336:2021 |
| **Hệ thống gas suppression** | FM200/CO2 cylinder, nozzle, panel | NFPA 2001 |
| **Đèn thoát nạn** | Đèn exit, bảng chỉ dẫn, pin backup | TCVN 3890:2023 |
| **Loa PA/Evacuation** | Loa, amplifier, mic, cáp | TCVN 6761:2000 |
| **Hồ sơ che khuất** | Biên bản TVGS, ảnh thi công, bản vẽ hoàn công | TT 06/2021/TT-BXD |

---

### 5. Công nợ Tracking

Theo dõi công nợ theo dự án, cảnh báo quá hạn, đề xuất hành động thu hồi.

**Cách dùng:** "công nợ", "phải thu", "theo dõi thanh toán"

**Output format:**

```markdown
# Công nợ — [Ngày]

## Tổng quan
| Chỉ số | Giá trị |
|--------|---------|
| **Tổng phải thu** | [X] triệu VND |
| **Quá hạn 30+ ngày** | [X] triệu |
| **Quá hạn 60+ ngày** | [X] triệu |
| **Quá hạn 90+ ngày** | [X] triệu |

## Chi tiết theo dự án
| Dự án | Chủ đầu tư | Tổng HĐ | Đã thu | Còn lại | Hạn TT | Quá hạn | Hành động |
|-------|------------|---------|--------|---------|--------|---------|-----------|
| [Tên] | [CDT] | [X] | [X] | [X] | [Ngày] | [N] ngày | [Đề xuất] |

## Đề xuất thu hồi
1. **[Dự án]** — Gửi công văn nhắc nợ (mẫu sẵn). Quá hạn [N] ngày.
2. **[Dự án]** — Gọi điện cho kế toán CDT. Hóa đơn đã gửi [Ngày].
3. **[Dự án]** — Cân nhắc tạm ngưng thi công phần chưa thi công. Cần ý kiến pháp lý.
```

---

## Framework phân loại rủi ro dự án

| Yếu tố | Trọng số | Đánh giá |
|--------|----------|----------|
| **Giá trị HĐ** | 25% | Dự án lớn = cần giám sát chặt |
| **Tiến độ** | 25% | Behind schedule = ưu tiên hành động |
| **Công nợ** | 25% | Quá hạn = rủi ro dòng tiền |
| **Hồ sơ pháp lý** | 15% | Thiếu biên bản = rủi ro thanh quyết toán |
| **Phạm vi phát sinh** | 10% | Chưa ký补充 = rủi ro không được thanh toán |

---

## Công cụ kết nối (Hermes)

Skill này tận dụng được tốt nhất khi kết hợp:

| Công cụ | Mục đích |
|---------|----------|
| **Lark CLI** | Trích xuất task/conversation từ group dự án |
| **Google Sheets/Drive** | Đọc bảng theo dõi dự án, HĐ, công nợ |
| **Gmail** | Tìm email liên quan HĐ, thanh toán |
| **Telegram** | Gửi cảnh báo rủi ro, reminder |
| **Slack** | Gửi báo cáo tuần, daily brief |
| **web_search** | Tra cứu quy định PCCC mới nhất |
| **xlsx skill** | Xuất báo cáo ra Excel |
| **pccc-technical-docs skill** | Tạo biện pháp thi công, checklist, biên bản |

---

## Prioritization logic

Khi Anh nói "tổng hợp tình hình" hoặc "review pipeline", tự động:

1. **Hỏi input** nếu chưa có dữ liệu: "Anh cho em danh sách dự án, hoặc em tìm trong Lark/Drive?"
2. **Phân tích** theo framework rủi ro ở trên
3. **Xếp hạng** ưu tiên hành động (ưu tiên giá trị lớn + deadline gần + công nợ quá hạn)
4. **Đề xuất** hành động cụ thể cho từng dự án
5. **Hỏi** "Anh muốn em gửi báo cáo ra Telegram/Slack không?"

---

## Pitfalls

### #1 — Biên bản nghiệm thu che khuất
- Hạng mục âm sàn/âm tường là **bắt buộc nghiệm thu trước khi lấp**
- Theo TT 06/2021/TT-BXD, thiếu biên bản TVGS = không được thanh quyết toán
- Luôn cảnh báo nếu dự án có hạng mục che khuất chưa có biên bản

### #2 — Phát sinh chưa ký bổ sung hợp đồng
- Phạm vi phát sinh thực tế mà chưa ký补充协议 = rủi ro không được thanh toán
- Flag ngay khi phát hiện scope change chưa có giấy tờ

### #3 — Công nợ 90+ ngày
- Cảnh báo mạnh nếu công nợ quá 90 ngày — cân nhắc ngưng thi công phần chưa thi công
- Theo Nghị định 06/2021/NĐ-CP, có thể dùng biện pháp bảo đảm thanh toán

### #4 — Bảo hành hệ thống PCCC
- BH PCCC thường 12-24 tháng, nhưng phải có bảo trì định kỳ (6 tháng/lần)
- Nếu dự án hết BH mà chưa có hợp đồng bảo trì = rủi ro khi PCCC kiểm tra

### #5 — Lark vs Feishu domain
- Công ty dùng **Lark international** (larksuite.com), không phải Feishu China
- Lark CLI link phải dùng domain đúng

---

## Related skills

- **pccc-technical-docs** — Tạo biện pháp thi công, checklist, biên bản, bản vẽ SVG
- **vietnam-contract-review** — Review hợp đồng xây dựng/PCCC Việt Nam
- **lark-cli** — Trích xuất thông tin từ group chat Lark
- **google-workspace** — Đọc Sheets, Drive, Gmail
- **xlsx** — Xuất báo cáo Excel

---

## References

- `references/project-tracker-template.md` — Mẫu theo dõi dự án PCCC
- `references/debt-collection-template.md` — Mẫu công văn nhắc nợ, email thu hồi công nợ
- `references/inspection-checklist-template.md` — Mẫu checklist nghiệm thu đầy đủ theo TCVN
- `references/construction-cost-management-2026.md` — Hướng Dẫn Pháp Lý và Quản Lý Chi Phí Đầu Tư Xây Dựng 2026 (Áp Dụng Từ 01/07/2026)
