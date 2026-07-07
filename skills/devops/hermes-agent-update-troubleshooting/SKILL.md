---
name: hermes-agent-update-troubleshooting
description: "Sửa lỗi và xử lý các tình huống phát sinh khi chạy lệnh cập nhật hoặc nâng cấp Hermes Agent (hermes update)."
version: 1.0.0
author: Doremon
metadata:
  hermes:
    tags: [hermes, update, upgrade, troubleshooting, package-lock, git]
---

# Hướng Dẫn Sửa Lỗi Cập Nhật Hermes Agent (hermes update)

Tài liệu này ghi lại các bài học kinh nghiệm và phương pháp giải quyết các sự cố phát sinh khi chạy cập nhật hoặc nâng cấp phiên bản cho Hermes Agent (`hermes update`).

## Lỗi Xung Đột Git Làm Trượt Cập Nhật (Dirty Working Directory)

### Hiện tượng
Khi chạy `hermes update`, lệnh có thể báo lỗi hoặc không thể kéo code mới về do thư mục làm việc của Git không sạch (dirty), ví dụ có file `package-lock.json` hoặc các file sinh ra trong quá trình cài đặt bị thay đổi cục bộ.

### Cách xử lý
1. Di chuyển vào thư mục cài đặt gốc của Hermes Agent (mặc định là `~/.hermes/hermes-agent`).
2. Khôi phục lại trạng thái sạch cho các file bị thay đổi cục bộ bằng Git:
   ```bash
   git -C ~/.hermes/hermes-agent restore package-lock.json
   # Hoặc khôi phục toàn bộ working tree nếu không có thay đổi quan trọng tự tạo
   git -C ~/.hermes/hermes-agent reset --hard HEAD
   ```
3. Chạy lại lệnh cập nhật:
   ```bash
   hermes update
   ```

## Lỗi Timeout Khi Cập Nhật (Command Timed Out)

### Hiện tượng
Lệnh `hermes update` thực hiện việc cài đặt lại rất nhiều thư viện Python và Node.js phụ thuộc (dependencies). Quá trình biên dịch và tải xuống có thể vượt quá giới hạn timeout mặc định của CLI (thường là 60 giây), dẫn đến thông báo `[Command timed out after 60s]`.

### Cách xử lý & Xác minh
Mặc dù CLI báo timeout, tiến trình cài đặt thực tế dưới nền (background process) thường vẫn tiếp tục chạy và hoàn thành sau đó một vài giây.

Để xác minh xem quá trình cập nhật đã thực sự thành công hay chưa, hãy chạy:
```bash
hermes --version
```
Nếu kết quả trả về đúng phiên bản mới nhất và báo `Up to date` thì quá trình nâng cấp đã hoàn tất thành công dưới nền. Nếu chưa, hãy chạy lại lệnh cài đặt thủ công trong môi trường ảo:
```bash
cd ~/.hermes/hermes-agent
# Kích hoạt venv và cài đặt lại thủ công bằng uv
.venv/bin/pip install -e .
```
