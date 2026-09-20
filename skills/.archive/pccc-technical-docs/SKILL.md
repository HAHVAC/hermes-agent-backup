---
name: pccc-technical-docs
description: "Tạo tài liệu kỹ thuật PCCC / MEP / Điện nhẹ: biện pháp thi công, checklist, biên bản nghiệm thu, bản vẽ kỹ thuật dạng SVG/HTML. Dùng cho Công ty CP Cơ điện và PCCC Thăng Long."
version: 1.0.0
author: Doremon / PCCC Thăng Long
license: internal
metadata:
  hermes:
    tags: [pccc, fire-alarm, mep, construction, vietnam, technical-docs, infographic]
---

# PCCC Technical Docs Skill

Tạo tài liệu kỹ thuật chuyên ngành PCCC, điện nhẹ, cơ điện cho Công ty CP Cơ điện và PCCC Thăng Long. Bao gồm: biện pháp thi công, bản vẽ kỹ thuật SVG, checklist, biên bản nghiệm thu.

## Trigger conditions

Dùng skill này khi Boss hỏi về:
- Biện pháp thi công hệ thống PCCC, báo cháy, chữa cháy, exit, loa PA, điện nhẹ
- Đặt ống âm sàn / âm tường / trên trần trong kết cấu bê tông
- Lắp đặt thiết bị đầu báo, chuông, nút nhấn, tủ trung tâm
- Hệ thống chữa cháy: sprinkler, FM200, CO2, mist
- Bản vẽ kỹ thuật mặt cắt, sơ đồ tuyến ống, sơ đồ nguyên lý
- Biên bản nghiệm thu, checklist thi công, hồ sơ hoàn công
- Tiêu chuẩn áp dụng: TCVN, QCVN, NFPA, BS EN

## Output format

Mặc định tạo **HTML infographic** dark-themed gồm:
1. SVG mặt cắt kỹ thuật (có chú thích màu theo hệ thống)
2. Cards thông số từng hệ thống
3. Grid quy trình thi công theo bước
4. Risk table (phòng ngừa + xử lý)

Font: `Be Vietnam Pro` — tải từ Google Fonts.  
Export PNG bằng Playwright (xem pitfall #1).

## Color coding chuẩn

| Hệ thống | Màu | Hex |
|---|---|---|
| Báo cháy / Fire Alarm | Đỏ | `#ef4444` |
| Exit Sign / Đèn thoát nạn | Xanh lá | `#10b981` |
| Loa PA / Thông báo | Tím | `#8b5cf6` |
| Sprinkler / Chữa cháy nước | Xanh dương | `#3b82f6` |
| Gas suppression (FM200/CO2) | Vàng cam | `#f59e0b` |
| Nguồn điện / Power | Cam | `#f97316` |
| Thép cốt / Rebar | Vàng | `#fbbf24` |
| Pull box / Hộp nối | Cyan | `#22d3ee` |

## Workflow chuẩn

1. **Phân tích yêu cầu**: xác định hệ thống, loại tài liệu (biện pháp / checklist / biên bản / bản vẽ)
2. **Tìm kiếm thông tin kỹ thuật** nếu cần (tiêu chuẩn, quy định mới nhất)
3. **Tạo HTML** với SVG + CSS grid (xem references/dat-am-san-betong.md để tham khảo cấu trúc)
4. **Export PNG** bằng Playwright full-page:
   ```python
   from playwright.sync_api import sync_playwright
   with sync_playwright() as p:
       browser = p.chromium.launch()
       page = browser.new_page(viewport={"width": 1200, "height": 900})
       page.goto("file:///tmp/output.html")
       page.wait_for_timeout(1500)
       page.screenshot(path="/tmp/output.png", full_page=True)
       browser.close()
   ```
5. **Gửi PNG** qua Slack/Telegram; đính kèm link file HTML

## Tiêu chuẩn tham chiếu (VN)

- **TCVN 3905:2013** — Nhà và công trình, phòng cháy chữa cháy (thi công, nghiệm thu)
- **TCVN 5738:2021** — Hệ thống báo cháy tự động
- **TCVN 7336:2021** — Hệ thống sprinkler
- **QCVN 06:2022/BXD** — An toàn cháy nhà và công trình
- **Thông tư 06/2021/TT-BXD** — Hồ sơ hoàn công, nghiệm thu che khuất
- **NFPA 72** — Fire Alarm (tham chiếu quốc tế)
- **NFPA 70 Art.300** — Conduit fill, bending radius

## Pitfalls

### #1 — Playwright full-page screenshot (NOT browser_vision)
- `browser_vision_ide` chỉ capture viewport hiện tại, không phải full page
- Dùng Playwright script (Python) để chụp `full_page=True`
- `page.wait_for_timeout(1500)` bắt buộc để Google Fonts load xong
- Playwright đã cài trên instance này

### #2 — Ống âm sàn: lưu ý pháp lý quan trọng
- Đây là **hạng mục che khuất** theo Thông tư 06/2021/TT-BXD
- **Bắt buộc nghiệm thu TVGS ký** trước khi đổ bê tông
- Thiếu biên bản = rủi ro pháp lý khi thanh quyết toán + PCCC kiểm tra
- Luôn nhắc Anh về điều này khi đề cập đặt ống âm sàn

### #3 — Cáp chuyên dụng từng hệ thống
- Báo cháy: **FPH / FPLP** (fire-rated, không được thay bằng cáp thường)
- Loa PA: cáp **100V line**, cần shielded nếu đi gần cáp động lực
- Exit: cần cáp có backup ắc-quy riêng
- Khoảng cách tuyến PA vs động lực: ≥ 300 mm

### #4 — Bán kính uốn ống
- Tối thiểu **6× đường kính ống**
- Uốn nguội bằng máy chuyên dụng, không dùng nhiệt
- Cứ 2 góc 90° phải có 1 pull box trung gian
- Chiều dài thẳng giữa 2 pull box: ≤ 30 m

## References

- `references/dat-am-san-betong.md` — Kiến thức chi tiết: đặt ống âm sàn bê tông cho hệ thống báo cháy/exit/loa PA
