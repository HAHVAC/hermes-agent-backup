# Cleanup Session — 2026-05-25

## Trạng thái ban đầu
- Disk: 34G/39G used (**87%**), còn 5.4GB
- RAM: 1.3G/3.8G used (OK)
- Swap: 545MB/4GB

## Các thư mục lớn phát hiện

### /tmp (~2.5GB)
```
807M  /tmp/easy-vibe
680M  /tmp/camoufox-4PHY6d
266M  /tmp/node-compile-cache
110M  /tmp/skills
 98M  /tmp/lark_minutes_media
 72M  /tmp/nq66_pages
 64M  /tmp/pccc3917_pages
 51M  /tmp/hermes-agent
 32M  /tmp/openclaw
 25M  /tmp/gws_install
 24M  /tmp/danhmuc_duan_hanoi_2026_2030.pdf
 20M  /tmp/pccc_research
 17M  /tmp/jiti
 15M  /tmp/openclaw-skills
 14M  /tmp/lark_download2
 13M  /tmp/gws-cli
```

### ~/.hermes
```
2.3G  hermes-agent/ (bao gồm .git 262MB, node_modules 69MB)
455M  state-snapshots/ (2 bản: 20260521, 20260508)
271M  sessions/
229M  email_attachments/ (2026-04-24 đến 2026-04-26)
 53M  migration/
 27M  audio_cache/
 18M  skills/
```

### Docker
- 2 images: `n8nio/n8n:latest` (1.18GB), `nginx:alpine` (62MB)
- 2 containers **đang chạy**: n8n + n8n-nginx → **GIỮ NGUYÊN**

## Kết quả dọn dẹp

| Mục | Dung lượng giải phóng |
|-----|----------------------|
| /tmp (nhiều thư mục) | ~2.35 GB |
| pip cache (67 files) | ~134 MB |
| state-snapshot 20260508 | ~206 MB |
| email_attachments (tháng 4-5/2026) | ~229 MB |
| audio_cache TTS cũ >7 ngày | ~27 MB |
| **Tổng** | **~2.95 GB** |

## Trạng thái sau
- Disk: 31G/39G used (**79%**), còn 8.3GB ✅

## Ghi chú kỹ thuật
- `git gc --aggressive` trên `.git` 262MB → **timeout 120s** — bỏ qua, không ảnh hưởng
- Docker images (1.24GB) giữ nguyên vì cả 2 container đang active
- state-snapshot `20260521-121618-pre-update` (249MB) giữ lại là bản mới nhất
