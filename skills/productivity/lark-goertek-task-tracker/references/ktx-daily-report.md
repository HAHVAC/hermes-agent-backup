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

**Tính năng tải & chèn hình ảnh hiện trường (Phương án 1):**
- Script tự động quét các tin nhắn dạng hình ảnh (`msg_type == "image"`) trong thread.
- Nếu tin nhắn ảnh được gửi bởi cùng một người ngay sau tin nhắn báo cáo (text), ảnh đó sẽ được nhóm trực tiếp vào báo cáo đó.
- Các ảnh được tải về máy (relative path) bằng API `messages-resources-download` và upload lên Lark Drive bằng Drive Media API (`parent_type="docx_image"`).
- Việc tải và upload ảnh được thực hiện **đồng thời (concurrently)** sử dụng `ThreadPoolExecutor` (mặc định 8 workers) để tối ưu hóa thời gian xử lý (hoàn thành 32 ảnh trong vòng ~16 giây thay vì hơn 1 phút nếu chạy tuần tự).
- Các ảnh sau khi upload lấy được `file_token` sẽ được chèn trực tiếp dưới dòng text báo cáo bên trong bảng XML bằng thẻ `<img src="TOKEN" width="200" />`.

**Usage:**
```bash
# Báo cáo hôm nay (default)
python3 /root/.hermes/scripts/ktx_daily_report.py

# Báo cáo ngày cụ thể
python3 /root/.hermes/scripts/ktx_daily_report.py 2026-06-04
```

**Output:**
- Append XML vào Lark Doc `KD8Xd3KUjouzhzxq2xolyWAmgkI`
- Save XML debug copy tại `/tmp/ktx_daily_report_latest.xml`
- Print tóm tắt ra stdout (số báo cáo, số ảnh, URL doc)

## Lark Doc XML Structure

Doc XML được tạo theo format:
```xml
<title>Báo cáo tiến độ thi công KTX GOERTEK</title>
<callout emoji="📌">Mô tả doc</callout>

<!-- Mỗi ngày append thêm 1 section -->
<h1>📅 Báo cáo ngày DD/MM/YYYY</h1>
<h2>🔴 Hệ Báo cháy</h2>
  <callout>Tóm tắt sender + số báo cáo</callout>
  <table>Chi tiết từng báo cáo (Giờ | Khu vực | Người gửi | Nội dung)</table>
<h2>🔵 Hệ Chữa cháy</h2>
<h2>🟢 Hệ Thông gió</h2>
<h2>🟡 Hệ Điện</h2>
<h2>📊 Tổng kết ngày</h2>
  <table>Summary 4 hệ (Số báo cáo | Khu vực | Trạng thái)</table>
  <callout>Vấn đề / Ghi chú</callout>
```
