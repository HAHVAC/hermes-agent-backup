# KTX Daily Report — Reference

## Sender Mapping (open_id → tên)

| Open ID | Tên | Vai trò |
|---------|-----|---------|
| `ou_dcae1fcf640febfba998addc9e77b579` | Nguyễn Văn Phúc | Đội Toản (ống lồng / thi công) |
| `ou_feb04970c3c442a8f7fdd61a2daa0f78` | Lê An Thụy | Báo cháy |
| `ou_82b3294ee4ddff2abb7a94828e9397aa` | Đào Văn Đạt | Báo cháy / Bảo dưỡng |
| `ou_49810a6bc1eec25883d0d0807b57bcfe` | TA Mẫn Văn Hà | Manager / Boss |
| `ou_3c2f50cddac87e6945fe5f8f751fed77` | TA Nguyễn Sinh Hùng | Giám sát (Supervision) |
| `ou_6601b14e9cc7b9af394e6f2ab44c4621` | Phùng Xuân Quang | QA/QC |

- **Thư mục gốc chứa ảnh:** `RgFvfLbrlllgSsdg7VzlZz59ggg` (URL: https://pccctruongan.sg.larksuite.com/drive/folder/RgFvfLbrlllgSsdg7VzlZz59ggg)

- **Cron Job ID**: `865fd3e18751`
- **Delivery Target**: `feishu:oc_e6167ab9a7424fab1a2db2442fd98581` (Chat ID cá nhân của Boss để nhận duyệt báo cáo)

## Quản lý hoạt động tự động hóa & Cron Job

### 1. Tránh lỗi gửi tin nhắn (`[99992402] field validation failed`)
Khi cấu hình cron job qua công cụ `cronjob`, nếu tham số `deliver` là `origin` hoặc bare platform, hệ thống có thể gặp lỗi phân phối trên Feishu (đặc biệt khi chạy tự động hoàn toàn). Luôn chỉ định rõ chat ID chính xác dạng `feishu:chat_id` (ví dụ: `feishu:oc_e6167ab9a7424fab1a2db2442fd98581`) để đảm bảo tin nhắn được đẩy thẳng tới đúng nơi nhận mà không bị lỗi.

### 2. Thiết lập cơ chế im lặng khi không có dữ liệu (`[SILENT]`)
Để tránh gửi tin nhắn rác khi công trường hôm đó không có cập nhật:
- Prompt của job cần hướng dẫn agent: *"Nếu kết quả script trả về 0 báo cáo và 0 ảnh, hãy trả về chính xác từ khóa `[SILENT]` và không viết thêm gì khác."*
- Hệ thống cronjob của Hermes sẽ tự động nhận diện `[SILENT]` từ response của agent để hủy gửi tin, giữ cho hộp thoại của Boss luôn gọn gàng.

## Keyword phân loại hệ thống

Script phân loại tin nhắn text vào 4 hệ dựa trên keyword matching:

### 🔴 Báo cháy
`báo cháy`, `báo chày`, `bc`, `báo động`, `chuông báo`, `khói`, `nhiệt`, `đầu báo`, `đặt âm`, `ống âm`, `dải ống`, `ống lồng`, `đặt ống`

**Fallback:** Nếu không match keyword nào nhưng nội dung chứa `ống`, `thi công`, `hiện trường`, `nghiệm thu`, `tiến độ`, `zone`, `tầng`, `sàn` → mặc định classify là Báo cháy (vì hiện tại hầu hết activity trong thread KTX là hệ báo cháy).

### 🔵 Chữa cháy
`chữa cháy`, `bình chữa`, `vòi chữa`, `van`, `hệ nước`, `bơm`, `hydrant`, `sprinkler`, `hose reel`

### 🟢 Thông gió
`thông gió`, `điều hòa`, `điều hoà`, `ống gió`, `fan`, `ahu`, `fcu`, `diffuser`, `cửa gió`

### 🟡 Điện
`điện`, `điện nhẹ`, `cáp`, `ống điện`, `tủ điện`, `máng cáp`, `cable tray`, `đèn`, `chiếu sáng`, `công tắc`, `ổ cắm`, `đi dây`

## Zones & Scope (KTX)

Theo thread info từ Boss:
- **Zone 1**: Floor 1-3 (Trục 1-9/L-P)
- **Zone 4**: Floor 2
- **Zone 5**: Floor 2

## Script Details

**Path:** `/root/.hermes/scripts/ktx_daily_report.py`

**Tính năng tải & quản lý hình ảnh hiện trường:**
- Script tự động quét các tin nhắn dạng hình ảnh (`msg_type == "image"`) trong thread.
- Nếu tin nhắn ảnh được gửi bởi cùng một người ngay sau tin nhắn báo cáo (text), ảnh đó sẽ được nhóm vào báo cáo đó để lấy thông tin nội dung mô tả phục vụ cho việc đặt tên.
- Các ảnh được tải về máy (relative path) bằng API `messages-resources-download` và đổi tên theo chuẩn `yyyy-mm-dd-noidung.png` (bỏ tiếng Việt có dấu, khoảng trắng đổi thành `-`, viết thường).
- Toàn bộ ảnh được upload lên một thư mục Lark Drive con tự động tạo theo ngày dạng `Báo cáo KTX yyyy-mm-dd`. Link folder này được nhúng ở đầu báo cáo trong Lark Doc để người dùng tiện tra cứu.
- Việc tải và upload ảnh được thực hiện **song song với số lượng luồng vừa phải (max_workers=2) và có delay 1 giây** giữa các luồng để tránh đụng trần giới hạn tần suất API (Rate Limit `99991400: request trigger frequency limit` của Lark).

**Usage:**
```bash
# Báo cáo hôm nay (default)
python3 /root/.hermes/scripts/ktx_daily_report.py

# Báo cáo ngày cụ thể
python3 /root/.hermes/scripts/ktx_daily_report.py 2026-06-06
```

**Output:**
- Append XML (1 dòng tổng hợp cho mỗi hệ) vào Lark Doc `KD8Xd3KUjouzhzxq2xolyWAmgkI`
- Save XML debug copy tại `/tmp/ktx_daily_report_latest.xml`
- Print tóm tắt ra stdout (số báo cáo, số ảnh, URL doc, URL Drive folder)

## Lark Doc XML Structure (Cấu trúc mới rút gọn)

Doc XML được tạo theo format:
```xml
<h1>📅 Báo cáo ngày DD/MM/YYYY</h1>
<callout emoji="📊" background-color="light-gray" border-color="light-blue">
  <p><b>Tổng quân số KTX:</b> X người</p>
  <p><b>Folder hình ảnh hiện trường:</b> <a href="DRIVE_URL">Xem trên Lark Drive</a></p>
</callout>
<table>
  <colgroup>...</colgroup>
  <thead>
    <tr>
      <th background-color="light-gray">Hệ thống</th>
      <th background-color="light-gray">Khu vực</th>
      <th background-color="light-gray">Nội dung báo cáo chi tiết</th>
      <th background-color="light-gray">Quân số</th>
    </tr>
  </thead>
  <tbody>
    <!-- Mỗi ngày tối đa 4 dòng tương ứng với 4 hệ kỹ thuật chính -->
    <tr>
      <td><b>🔴 Hệ Báo cháy</b></td>
      <td>Khu vực thi công (ví dụ: Zone 1, Zone 4 Tầng 3)</td>
      <td>Các gạch đầu dòng tổng hợp tin nhắn chữ của hệ này</td>
      <td>Quân số (nếu có) hoặc "Có"/"—"</td>
    </tr>
    ...
  </tbody>
</table>
<hr/>
```
