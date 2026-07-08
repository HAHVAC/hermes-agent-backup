# Nhật ký dọn dẹp hệ thống thực tế - 08/07/2026

## Bối cảnh và kết quả
- **Hệ thống**: Linux VPS chạy Docker (n8n, nginx)
- **Tình trạng ban đầu**: Ổ đĩa `/` sử dụng **87%** (chỉ còn trống 5.3 GB)
- **Hành động**:
  1. Quét dung lượng toàn bộ thư mục bằng lệnh `du` có kiểm soát thời gian (`timeout 10` hoặc `timeout 15`) để tránh bị timeout 60s trên server lớn.
  2. Thu dọn Journal logs hệ thống bằng lệnh: `journalctl --vacuum-size=200M` giải phóng **3.6 GB**.
  3. Xóa các cache package trong `/root/.cache/` bao gồm uv, pip, electron, node-gyp, gdown (giải phóng **0.58 GB**).
  4. Xóa các thư mục tạm được đặt tên rõ ràng trong `/tmp` như `skills-*`, `node-compile-cache`, `openclaw`, `xlsx-skill-repo`, v.v. (giải phóng **0.12 GB**).
  5. Kiểm tra Docker system, container đang hoạt động (`n8n`, `n8n-nginx`) và các volumes an toàn, không có tài nguyên thừa cần prune nguy hiểm.
- **Kết quả cuối cùng**: Ổ đĩa giảm xuống **76%** (còn trống **9.5 GB**), đưa hệ thống về trạng thái an toàn (<80%).

## Bài học và kỹ thuật rút ra
1. **Lệnh `du` trên thư mục root `/` hoặc thư mục lớn**: Luôn sử dụng tiền tố `timeout 10` hoặc `timeout 15` để tránh việc tiến trình đệ quy quá sâu gây treo terminal và timeout 60s của Agent.
2. **Hút log hệ thống an toàn**: `journalctl --vacuum-size=200M` là cách dọn dẹp cực kỳ hiệu quả đối với các hệ thống chạy docker lâu ngày tích lũy nhiều systemd journal logs.
3. **Phân biệt dữ liệu Docker**: Luôn đối chiếu `docker ps -a` trước khi chạy `docker system prune` hoặc `docker image prune` để đảm bảo không làm gián đoạn các dịch vụ quan trọng của Anh (như n8n đang hoạt động).
