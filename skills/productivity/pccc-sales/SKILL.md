---
name: pccc-sales
description: >
  Chào thầu, báo giá, đấu thầu PCCC / MEP / Điện nhẹ cho Công ty CP Cơ điện
  và PCCC Thăng Long. Nghiên cứu chủ đầu tư, soạn hồ sơ dự thầu, tính báo giá,
  draft email chào hàng, phân tích đối thủ cạnh tranh, forecast doanh thu.
  Dùng khi nói về "chào thầu", "báo giá", "hồ sơ dự thầu", "đấu thầu",
  "chủ đầu tư", "phân tích đối thủ", "forecast", "pipeline sales", "cold email",
  "warm intro", hoặc "tiếp cận khách hàng".
version: 1.0.0
author: Doremon / PCCC Thăng Long
license: internal
metadata:
  hermes:
    tags: [pccc, mep, sales, bidding, quotation, tender, construction, vietnam]
---

# PCCC Sales — Chào thầu & Báo giá

Quản lý toàn diện quy trình sales PCCC/MEP: từ tiếp cận khách hàng → nghiên cứu CDT → soạn hồ sơ dự thầu → báo giá → đàm phán → ký hợp đồng.

## Trigger conditions

Dùng skill này khi Boss nói về:
- "Chào thầu / báo giá / đấu thầu"
- "Hồ sơ dự thầu / hồ sơ chào hàng"
- "Chủ đầu tư / phân tích CDT"
- "Phân tích đối thủ cạnh tranh"
- "Forecast doanh thu / pipeline sales"
- "Email chào hàng / tiếp cận khách hàng"
- "Cold email / warm intro"
- "Bảng giá / định mức / đơn giá PCCC"
- "Pre-qual / Hạng năng lực / Chứng chỉ"
- "Kết quả đấu thầu / trúng thầu / trượt thầu"

## Workflow chính

### 1. Nghiên cứu Chủ đầu tư (Account Research)

Phân tích toàn diện CDT trước khi chào thầu hoặc gặp gỡ.

**Cách dùng:** "research CDT [tên]", "phân tích [tên công ty]", "tìm hiểu về [chủ đầu tư]"

**Input:** Tên công ty CDT, hoặc URL website, hoặc mô tả dự án.

**Execution flow:**

1. **Web search (luôn chạy):**
   - `[Company] + xây dựng / dự án` — tìm dự án đang triển khai
   - `[Company] + PCCC / phòng cháy` — xem đã có hệ thống chưa
   - `[Company] + đấu thầu` — tìm thông tin mời thầu gần đây
   - `[Company] + tin tức` — tình hình tài chính, pháp lý
   - `[Company] + lãnh đạo` — người ra quyết định

2. **Phân tích chỉ dấu dự án:**
   - Dự án mới xây / cải tạo → cần PCCC mới
   - Dự án đang thi công kết cấu → timing tốt cho chào thầu PCCC
   - Dự án đã nghiệm thu → cơ hội bảo trì / nâng cấp
   - Công ty mở rộng chi nhánh → nhiều dự án tiềm năng

3. **Phân tích quyết định:**
   - Ai là người ra quyết định? (Giám đốc / Kỹ thuật / Mua hàng)
   - Tiêu chí chọn nhà thầu? (giá / năng lực / quan hệ)
   - Đã từng làm việc với đối thủ nào chưa?

**Output format:**

```markdown
# Nghiên cứu CDT: [Tên Công ty]

**Ngày:** [Date] | **Nguồn:** Web Search

---

## Tổng quan nhanh

[2-3 câu: Công ty gì, quy mô, cơ hội PCCC cho Thăng Long, góc tiếp cận tốt nhất]

---

## Hồ sơ công ty

| Trường | Giá trị |
|---------|---------|
| **Tên** | [Tên công ty] |
| **Loại hình** | [Nhà nước / TNHH / CP / FDI /...] |
| **Ngành** | [Bất động sản / Sản xuất / Khách sạn /...] |
| **Quy mô** | [Vốn điều lệ / Doanh thu nếu biết] |
| **Trụ sở** | [Địa chỉ] |
| **Website** | [URL] |

---

## Dự án đang triển khai

| Dự án | Loại | Quy mô | Giai đoạn | Cơ hội PCCC |
|-------|------|--------|-----------|-------------|
| [Tên] | [Chung cư / Khách sạn /...] | [X] tầng / [X] m² | [Thiết kế / Thi công /...] | [Mô tả] |

---

## Chỉ dấu PCCC

- ✅ [Tín hiệu tích cực — ví dụ: "Dự án 25 tầng, bắt buộc PCCC theo QCVN 06:2022"]
- ✅ [Tín hiệu tích cực]
- ⚠️ [Điều cần lưu ý — ví dụ: "Đã có nhà thầu PCCC từ dự án trước"]
- ❓ [Cần hỏi thêm — ví dụ: "Chưa rõ hệ thống nào yêu cầu"]

---

## Người ra quyết định

### [Tên] — [Chức danh]
- **Vai trò:** [Người quyết định / Người ảnh hưởng / Người liên hệ]
- **Background:** [Quá trình công tác nếu tìm được]
- **Talking point:** [Điểm chạm khi gặp]

---

## Đề xuất tiếp cận

**Kênh tốt nhất:** [Email / Giới thiệu / Gặp trực tiếp / Tham gia đấu thầu]
**Hook:** [Lý do liên hệ — dự án cụ thể / luật bắt buộc / case study tương tự]
**Bước tiếp theo:** [Hành động cụ thể]
```

---

### 2. Soạn Hồ sơ dự thầu / Chào hàng

Hướng dẫn soạn hồ sơ dự thầu hoặc hồ sơ chào hàng PCCC/MEP.

**Cách dùng:** "soạn hồ sơ dự thầu", "hồ sơ chào hàng PCCC", "chuẩn bị bidding"

**Workflow:**

1. **Xác định loại hồ sơ:**
   - **Hồ sơ dự thầu chính thức** (đấu thầu rộng rãi / hạn chế / chào hàng cạnh tranh)
   - **Hồ sơ chào hàng** (tự gửi, không qua đấu thầu)
   - **Hồ sơ năng lực** (pre-qualification)

2. **Phân tích yêu cầu E-HSMT** (nếu đấu thầu):
   - Đọc kỹ E-HSMT trên Hệ thống mạng đấu thầu quốc gia
   - Liệt kê yêu cầu bắt buộc (năng lực, kinh nghiệm, tài chính)
   - Tính điểm kỹ thuật + điểm tài chính
   - Xác định chiến lược: thắng bằng giá hay thắng bằng kỹ thuật

3. **Cấu trúc hồ sơ dự thầu chuẩn:**

```
Hồ sơ dự thầu/
├── Đơn dự thầu
├── Hợp đồng mẫu (đã điền)
├── Bảo lãnh dự thầu
├── Hồ sơ năng lực/
│   ├── Đăng ký kinh doanh
│   ├── Chứng chỉ Hạng I/II/III PCCC
│   ├── Chứng chỉ ISO 9001
│   ├── Bằng cấp CBGV PCCC
│   ├── Danh sách thiết bị
│   └── Danh sách công trình tương tự (3 năm gần nhất)
├── Hồ sơ kỹ thuật/
│   ├── Phương án kỹ thuật
│   ├── Biện pháp thi công
│   ├── Tổ chức nhân sự
│   ├── Tiến độ thi công (Gantt)
│   ├── Bản vẽ kỹ thuật (shop drawing)
│   ├── Catalogue thiết bị
│   └── Chứng nhận conformité thiết bị
├── Hồ sơ tài chính/
│   ├── Báo giá tổng hợp
│   ├── Báo giá chi tiết (BOQ)
│   ├── Báo cáo tài chính 3 năm
│   └── Cam kết tài chính
└── Các tài liệu khác/
    ├── Tài liệu sử dụng GOVP
    ├── Chứng chỉ CO/CQ thiết bị
    └── Văn bản pháp lý khác
```

4. **Kiểm tra trước khi nộp:**
   - [ ] Tất cả trang ký nhảy số / đóng dấu
   - [ ] Bảo lãnh dự thầu đúng mẫu, đúng số tiền, đúng thời hạn
   - [ ] Giá trị Bảo lãnh ≥ 1-3% giá gói thầu (theo LLT)
   - [ ] Thời gian bảo hành ≥ yêu cầu HSMT
   - [ ] Địa chỉ E-hsmt nộp đúng hạn (trước giờ đóng thầu)
   - [ ] File E-HSMT không quá dung lượng cho phép

---

### 3. Tính Báo giá (Quotation)

Hỗ trợ tính báo giá PCCC/MEP có cấu trúc, chính xác, kèm điều khoản thương mại.

**Cách dùng:** "tính báo giá [dự án]", "báo giá hệ thống [tên]", "BOQ PCCC"

**Báo giá gồm:**

```markdown
# BÁO GIÁ — [Tên dự án]

**Khách hàng:** [Tên CDT]
**Hệ thống:** [PCCC / MEP / Điện nhẹ]
**Ngày:** [Date]
**Hiệu lực báo giá:** 30 ngày

---

## A. BÁO GIÁ TỔNG HỢP

| STT | Hạng mục | ĐVT | Số lượng | Đơn giá (VNĐ) | Thành tiền (VNĐ) |
|-----|----------|-----|----------|---------------|-------------------|
| I | Hệ thống báo cháy | Gói | 1 | [X] | [X] |
| II | Hệ thống sprinkler | Gói | 1 | [X] | [X] |
| III | Đèn thoát nạn | Gói | 1 | [X] | [X] |
| IV | Loa PA/EVAC | Gói | 1 | [X] | [X] |
| | **TỔNG CỘNG** | | | | **[X]** |
| | VAT 10% | | | | **[X]** |
| | **TỔNG CỘNG CÓ VAT** | | | | **[X]** |

---

## B. BOQ CHI TIẾT (theo hệ thống)

### I. Hệ thống báo cháy tự động

| STT | Vật tư / Thiết bị | Hãng | Model | ĐVT | SL | ĐG | TT |
|-----|-------------------|------|-------|-----|----|----|-----|
| 1 | Tủ trung tâm báo cháy | [Hãng] | [Model] | Bộ | [N] | [X] | [X] |
| 2 | Đầu báo khói photoelectric | [Hãsg] | [Model] | Cái | [N] | [X] | [X] |
| 3 | Đầu báo nhiệt | [Hãng] | [Model] | Cái | [N] | [X] | [X] |
| 4 | Chuông báo cháy | [Hãng] | [Model] | Cái | [N] | [X] | [X] |
| 5 | Nút nhấn thủ công | [Hãng] | [Model] | Cái | [N] | [X] | [X] |
| 6 | Module cách ly | [Hãng] | [Model] | Cái | [N] | [X] | [X] |
| 7 | Cáp FPH 2x1.5 | [Hãng] | | m | [N] | [X] | [X] |
| 8 | Ống EMC + phụ kiện | | | m | [N] | [X] | [X] |
| 9 | Nhân công thi công | | | Gói | 1 | [X] | [X] |
| 10 | Kiểm tra & Vận hành | | | Gói | 1 | [X] | [X] |
| | **Cộng hệ thống I** | | | | | | **[X]** |

[... Tương tự cho các hệ thống II, III, IV ...]

---

## C. ĐIỀU KHOẢN THƯƠNG MẠI

1. **Thanh toán:** Theo tiến độ:
   - Đợt 1: [30%] — Ký hợp đồng
   - Đợt 2: [30%] — Giao vật tư đến công trường
   - Đợt 3: [30%] — Nghiệm thu hoàn thành
   - Đợt 4: [10%] — Bảo hành (giữ lại, trả sau 12 tháng)

2. **Thời gian thi công:** [N] ngày kể từ ngày nhận mặt bằng

3. **Bảo hành:** [24] tháng kể từ ngày nghiệm thu

4. **Giá trên chưa bao gồm:**
   - Chi phí xin giấy phép PCCC (CDT chịu)
   - Nguồn điện cấp cho hệ thống (CDT cung cấp)
   - Nước cấp cho hệ thống sprinkler (CDT cung cấp)

5. **Hiệu lực báo giá:** 30 ngày kể từ ngày lập

6. **Điều kiện khác:** [Theo thỏa thuận]
```

**Lưu ý khi tính báo giá:**
- Luôn kèm VAT 10% (hoặc theo yêu cầu CDT)
- Chi phí nhân công: tính theo định mức hoặc gói
- Chi phí vật tư: cập nhật giá mới nhất (liên hệ nhà cung cấp nếu cần)
- Dự phòng: 5-10% cho phát sinh (nếu thi công chưa rõ ràng)
- Biên độ lợi nhuận: tùy chiến lược (thắng giá vs thắng kỹ thuật)

---

### 4. Email chào hàng / Tiếp cận khách hàng

Soạn email hoặc văn bản chào hàng PCCC/MEP, cá nhân hóa theo CDT.

**Cách dùng:** "soạn email chào hàng [tên CDT]", "tiếp cận [công ty]", "gửi email chào PCCC"

**Phân loại tiếp cận:**

| Loại | Mô tả | Template |
|------|-------|----------|
| **Cold email** | Chưa có mối quan hệ, chủ động tìm đến | Template 1 |
| **Warm intro** | Có người giới thiệu, hoặc đã gặp qua sự kiện | Template 2 |
| **Follow-up đấu thầu** | Đã nộp HS dự thầu, theo dõi kết quả | Template 3 |
| **Re-engage** | Đã từng làm việc, giới thiệu dự án mới | Template 4 |

**Xem chi tiết templates tại:** `references/sales-email-templates.md`

**Nguyên tắc viết email chào hàng:**
- Subject line < 50 ký tự, không spam words
- Mở đầu bằng điều cụ thể (tên dự án, tin tức, người giới thiệu)
- 1 giá trị cốt lõi, 1 CTA rõ ràng
- Plain text, không markdown
- Dưới 150 từ cho cold email
- Kèm case study nếu có (công trình tương tự đã làm)

---

### 5. Phân tích đối thủ cạnh tranh (Competitive Intelligence)

Phân tích đối thủ PCCC trong đấu thầu hoặc cạnh tranh chung.

**Cách dùng:** "phân tích đối thủ [tên]", "so sánh với [công ty]", "đối thủ PCCC"

**Output format:**

```markdown
# Phân tích đối thủ: [Tên công ty]

## Hồ sơ

| Trường | Giá trị |
|---------|---------|
| **Tên** | [Tên công ty] |
| **Hạng PCCC** | [I / II / III / chưa rõ] |
| **Năng lực** | [Mô tả] |
| **Thị trường** | [Khu vực hoạt động chính] |

## Điểm mạnh
- ✅ [Điểm mạnh 1 — ví dụ: Hạng I PCCC, làm được mọi gói thầu]
- ✅ [Điểm mạnh 2]

## Điểm yếu
- ⚠️ [Điểm yếu 1 — ví dụ: Chỉ chuyên sprinkler, yếu báo cháy]
- ⚠️ [Điểm yếu 2]

## So sánh với Thăng Long

| Tiêu chí | Thăng Long | [Đối thủ] |
|----------|-----------|-----------|
| Hạng PCCC | [X] | [X] |
| Kinh nghiệm | [X] năm | [X] năm |
| Hệ thống mạnh | [Báo cháy + MEP] | [X] |
| Giá | [Cạnh tranh] | [Cao hơn / Thấp hơn] |
| Quan hệ CDT | [Có / Chưa] | [Có / Chưa] |

## Chiến lược đề xuất

**Khi đấu thầu cùng:**
1. [Điểm nhấn kỹ thuật Thăng Long hơn đối thủ]
2. [Case study Thăng Long có mà đối thủ chưa chắc làm được]
3. [Giá thầu — nên thấp hơn hay cạnh tranh bằng kỹ thuật]

**Khi tiếp cận CDT đang dùng đối thủ:**
1. [Lý do chuyển — bảo trì kém, giá cao, thi công chậm...]
2. [Giá trị Thăng Long thêm được — gói trọn PCCC+MEP, một nhà thầu]
```

---

### 6. Sales Pipeline & Forecast

Theo dõi pipeline sales, forecast doanh thu, phân tích gap.

**Cách dùng:** "pipeline sales", "forecast doanh thu", "xem cơ hội đang theo"

**Stage probabilities (mặc định):**

| Stage | Xác suất | Mô tả |
|-------|----------|-------|
| 🔍 Lead | 10% | Có thông tin CDT, chưa liên hệ |
| 📞 Tiếp cận | 20% | Đã liên hệ, chờ phản hồi |
| 🤝 Đàm phán | 40% | Đang trao đổi yêu cầu kỹ thuật |
| 📋 Báo giá | 60% | Đã gửi báo giá, chờ quyết định |
| ⚖️ Đấu thầu | 50% | Đã nộp HS dự thầu, chờ kết quả |
| ✅ Commit | 80% | CDT đã đồng ý, chờ ký HĐ |
| 🎉 Won | 100% | Đã ký hợp đồng |
| ❌ Lost | 0% | Thất bại |

**Output format:**

```markdown
# Sales Forecast — [Tháng/Quý]

## Tổng quan

| Chỉ số | Giá trị |
|---------|---------|
| **Target** | [X] tỷ VND |
| **Đã ký** | [X] tỷ ([X]% target) |
| **Pipeline mở** | [X] tỷ |
| **Weighted forecast** | [X] tỷ |
| **Gap to target** | [X] tỷ |
| **Coverage ratio** | [X]x |

## Phân tích kịch bản

| Kịch bản | Doanh thu | % Target | Giả định |
|----------|-----------|----------|----------|
| **Tốt nhất** | [X] tỷ | [X]% | Tất cả deal đều win |
| **Khả dĩ** | [X] tỷ | [X]% | Theo xác suất stage |
| **Xấu nhất** | [X] tỷ | [X]% | Chỉ commit deal win |

## Deal cần tập trung

### Commit (Độ tin cao)
| Dự án | CDT | Giá trị | Stage | Ngày dự kiến ký | Ghi chú |
|-------|-----|---------|-------|-----------------|---------|
| [Tên] | [CDT] | [X] tỷ | Commit | [Ngày] | [Ghi chú] |

### Upside (Có thể win)
| Dự án | CDT | Giá trị | Stage | Xác suất | Rủi ro |
|-------|-----|---------|-------|----------|--------|
| [Tên] | [CDT] | [X] tỷ | [Stage] | [X]% | [Rủi ro] |

## Gap Analysis

**Cần thêm [X] tỷ để đạt target.**

**Đề xuất:**
1. [Accelerate deal X] — Đang ở [stage], giá trị [X] tỷ
2. [Revive deal Y] — Quên từ [Ngày], cần re-engage
3. [New pipeline] — Cần thêm [X] tỷ pipeline mới, coverage [X]x
```

---

## Framework đánh giá cơ hội sales

Khi Anh nêu tên dự án/CĐT, tự động đánh giá:

| Yếu tố | Trọng số | Câu hỏi |
|--------|----------|---------|
| **Quy mô dự án** | 25% | Bao nhiêu tầng/m²? Hệ thống nào? |
| **Năng lực Thăng Long** | 25% | Có đủ hạng, nhân sự, kinh nghiệm không? |
| **Cạnh tranh** | 20% | Có bao nhiêu đối thủ? Lợi thế Thăng Long? |
| **Quan hệ** | 15% | Đã từng làm việc với CDT chưa? |
| **Timing** | 15% | Đúng giai đoạn chào thầu chưa? |

---

## Công cụ kết nối (Hermes)

| Công cụ | Mục đích |
|---------|----------|
| **web_search** | Nghiên cứu CDT, đối thủ, đấu thầu |
| **Google Drive/Sheets** | Đọc/ghi bảng theo dõi sales, báo giá |
| **Gmail** | Gửi email chào hàng, nhận phản hồi |
| **Lark CLI** | Trích xuất thông tin từ group dự án |
| **Telegram/Slack** | Gửi cảnh báo deadline thầu, kết quả |
| **xlsx skill** | Xuất báo giá Excel, BOQ |
| **pccc-technical-docs** | Tạo biện pháp thi công cho HS dự thầu |
| **docx skill** | Xuất hồ sơ dự thầu Word |
| **vietnam-contract-review** | Review hợp đồng sau khi trúng thầu |

---

## Pitfalls

### #1 — Deadline nộp thầu
- Hệ thống E-HSMT đóng đúng giờ, **không gia hạn**
- Nộp trước ít nhất 2 tiếng để xử lý sự cố kỹ thuật
- Kiểm tra file upload không quá dung lượng
- Luôn check lại E-HSMT đã nộp thành công chưa

### #2 — Bảo lãnh dự thầu
- Số tiền BL ≥ 1-3% giá gói thầu (theo quy định LLT)
- Hiệu lực BL ≥ thời gian xét thầu + 30 ngày
- Nếu trúng mà không ký HĐ → mất tiền BL
- Luôn chuẩn bị BL trước 3-5 ngày

### #3 — Chứng chỉ năng lực
- Hạng I PCCC: gói thầu không giới hạn giá
- Hạng II PCCC: gói thầu ≤ 15 tỷ (theo quy định hiện hành)
- Hạng III PCCC: gói thầu ≤ 5 tỷ
- Phải kiểm tra Hạng còn hiệu lực hay không trước khi nộp HS

### #4 — Báo giá quá thấp
- Báo giá < 80% giá gói thầu → có thể bị loại (báo giá thấp bất thường)
- Phải giải trình nếu yêu cầu
- Định giá cẩn thận, kèm điều khoản "phát sinh ngoài phạm vi"

### #5 — Thiết bị thay thế
- Nếu thay thiết bị so với HSMT → phải có chứng từ tương đương
- Catalogue thiết bị thay thế phải nộp kèm
- Không tự ý thay thiết bị sau khi trúng thầu (cầnapproval CDT)

### #6 — Lark vs Feishu
- Công ty dùng **Lark international**, không phải Feishu China

---

## Related skills

- **pccc-project-management** — Quản lý dự án sau khi ký HĐ
- **pccc-technical-docs** — Tạo biện pháp thi công, bản vẽ cho HS dự thầu
- **vietnam-contract-review** — Review hợp đồng PCCC/xây dựng
- **lark-cli** — Trích xuất thông tin từ Lark
- **google-workspace** — Drive, Sheets, Gmail
- **xlsx** — Xuất báo giá, BOQ
- **docx** — Xuất hồ sơ dự thầu Word

---

## References

- `references/sales-email-templates.md` — 4 mẫu email chào hàng (cold, warm, follow-up, re-engage)
- `references/bidding-checklist.md` — Checklist nộp hồ sơ dự thầu
- `references/brand-profile.md` — Hồ sơ năng lực tóm tắt Thăng Long (dùng cho chào hàng)
- `references/pricing-guide.md` — Hướng dẫn định giá & biên độ lợi nhuận PCCC
