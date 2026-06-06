---
name: chuyen-file-sang-md
description: Chuyển đổi các tài liệu (PDF, Word, Excel, PowerPoint, v.v.) sang định dạng Markdown sạch đẹp bằng công cụ markitdown của Microsoft và bộ lọc làm sạch định dạng tiếng Việt.
version: 1.0.0
triggers:
  - "chuyển file sang md"
  - "chuyen file sang md"
  - "chuyen-file-sang-md"
  - "chuyển tài liệu sang md"
  - "dịch file sang md"
tools:
  - terminal
  - file
---

# Chuyển File Sang Markdown (chuyen-file-sang-md)

Skill này hỗ trợ chuyển đổi bất kỳ tài liệu nào sang định dạng Markdown tối ưu hóa cho LLM sử dụng thư viện `markitdown` của Microsoft cùng với các bộ lọc tối ưu hóa tiếng Việt.

## Quy Trình Thực Hiện (Pipeline)

```
File Đầu Vào → Tải Về Tạm Thời → Chuyển Đổi (CLI chuyen-file-sang-md) → Gửi File Cho Anh
```

### Bước 1: Xác Định Nguồn File Đầu Vào
- **Google Drive**: Sử dụng công cụ `gdown` để tải về `/tmp/mc_input_file`.
- **URL Trực Tiếp**: Dùng `curl -sL -o /tmp/mc_input_file "<URL>"` để tải về.
- **File Cục Bộ**: Sử dụng trực tiếp đường dẫn file có sẵn trên máy.
- **File Đính Kèm Chat**: Sử dụng đường dẫn file được gateway cung cấp.

### Bước 2: Thực Thi Chuyển Đổi
Chạy công cụ CLI `/usr/local/bin/chuyen-file-sang-md` đã được cài đặt trên hệ thống:
```bash
chuyen-file-sang-md /path/to/input_file [optional_output_file.md]
```
*Lưu ý:* Lệnh này sử dụng môi trường Python ảo `/root/.hermes/hermes-agent/venv` có chứa `markitdown` và `numpy` tương thích.

### Bước 3: Định Dạng & Làm Sạch (Tự Động)
Lệnh CLI trên đã tích hợp bộ lọc nâng cao từ `format_md.py` để xử lý các lỗi đặc thù của tài liệu tiếng Việt sau khi chuyển đổi:
- Loại bỏ các dòng cảnh báo thư viện Python ở đầu.
- Xóa ký tự xuống trang (`\x0c`).
- Nối các dòng văn bản bị ngắt quãng do layout cột của PDF. **Lưu ý quan trọng:** Chỉ thực hiện việc nối đoạn văn bản (`join_paragraphs`) khi định dạng file gốc là PDF (nhằm tránh việc gộp nhầm cấu trúc dòng của danh sách `*`/`-` và bảng biểu `|` đối với các file khác như DOCX, HTML).
- Chuẩn hóa khoảng trắng dư thừa và giới hạn tối đa 2 dòng trống liên tiếp.
- Giữ nguyên cấu trúc Chương, Phần, Phụ lục và Bảng biểu.

### Bước 4: Gửi Kết Quả Cho Anh
- Lưu file đầu ra tại thư mục gốc của file đầu vào hoặc `/root/Downloads/markdown/`.
- Phản hồi ngắn gọn kết quả bao gồm: kích thước file, số dòng.
- Gửi file trực tiếp qua kênh chat dưới định dạng tệp đính kèm bằng cách dùng thẻ:
  `MEDIA:/path/to/output_file.md`

## ⚠️ Cạm bẫy & Lưu ý kỹ thuật (Pitfalls)
- **Xung đột NumPy trên phần cứng VM:** Thư viện `markitdown` phụ thuộc vào `magika` sử dụng `ONNX Runtime` và `NumPy`. Trên các VM có kiến trúc CPU cũ hơn hoặc không hỗ trợ X86_V2 baseline optimizations, phiên bản NumPy 2.x trở lên sẽ gây lỗi `RuntimeError: NumPy was built with baseline optimizations...`. Cần hạ cấp xuống `numpy<2.0.0` (ví dụ `numpy-1.26.4`) để chạy ổn định.
- **Lỗi `Namespace' object has no attribute 'no'` khi parse tham số:** Trong Python argparse, tham số `--no-format` sẽ tự động chuyển thành thuộc tính `args.no_format` thay vì `args.no-format`. Việc cố truy cập `args.no-format` trực tiếp sẽ bị lỗi cú pháp trừ.
- **Tránh gộp dòng tự động đối với định dạng không phải PDF:** Đối với DOCX, HTML, v.v., bố cục dòng vốn đã chuẩn nên không cần gọi `join_paragraphs`, nếu không sẽ phá hỏng định dạng danh sách và bảng biểu. Hãy chỉ định `source_type == "pdf"` trước khi thực hiện nối dòng.

## Ví Dụ Sử Dụng Trong Chat

Anh có thể yêu cầu:
- *"Chuyển file này sang md: /root/tailieu.pdf"*
- *"Tải link này và chuyển file sang md: https://example.com/proposal.docx"*
