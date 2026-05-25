---
name: linux-system-cleanup
description: >
  Dọn dẹp disk và tài nguyên hệ thống Linux: /tmp, pip cache, Docker, git objects,
  log cũ, email attachments, audio cache, state snapshots. Dùng khi disk usage >80%
  hoặc user hỏi "dọn dẹp hệ thống", "giải phóng disk", "clean up server".
triggers:
  - "dọn dẹp hệ thống"
  - "giải phóng disk"
  - "clean up server"
  - "disk full"
  - "disk usage cao"
  - "free up space"
  - "xóa file rác"
tags: [linux, disk, cleanup, devops, maintenance]
---

# Linux System Cleanup

## Khi nào dùng skill này
- Disk usage ≥ 80% (`df -h /` báo)
- User yêu cầu "dọn dẹp hệ thống", "giải phóng dung lượng"
- Sau upgrade/update lớn còn sót snapshot cũ
- Server chạy lâu chưa dọn /tmp, log, cache

---

## Quy trình chuẩn (thực hiện theo thứ tự)

### Bước 1 — Khảo sát trước khi làm

```bash
# Tổng quan disk
df -h /

# Những thư mục lớn trong /tmp
du -sh /tmp/* 2>/dev/null | sort -rh | head -20

# Những thư mục lớn trong ~/.hermes
du -sh ~/.hermes/*/ 2>/dev/null | sort -rh | head -15

# Docker
docker system df 2>/dev/null || true

# Pip cache
pip cache info 2>/dev/null
```

**Luôn đo dung lượng TRƯỚC và SAU mỗi bước** để báo cáo kết quả rõ ràng.

---

### Bước 2 — Xử lý theo ưu tiên

#### 🔴 Ưu tiên cao (an toàn, lợi nhiều)

**2a. Dọn /tmp**
```bash
# Xem trước, xác nhận
du -sh /tmp/ && ls /tmp/

# Xóa thư mục cụ thể (KHÔNG xóa toàn bộ /tmp — có thể có socket/pipe đang dùng)
rm -rf /tmp/easy-vibe /tmp/camoufox-* /tmp/node-compile-cache \
       /tmp/skills* /tmp/lark_* /tmp/*_pages \
       /tmp/openclaw* /tmp/gws_* /tmp/pccc_research \
       /tmp/agent-skills /tmp/knowledge-work-plugins \
       /tmp/lark_download* /tmp/jiti /tmp/hermes-agent
```
> ⚠️ **Pitfall:** Không `rm -rf /tmp/*` — socket file của X11/systemd/dbus nằm trong /tmp.
> Xóa từng thư mục rõ tên là an toàn nhất.

**2b. Pip cache**
```bash
pip cache purge
```

**2c. Hermes state-snapshots cũ**
```bash
# Xem bản nào có
ls -lh ~/.hermes/state-snapshots/

# Xóa bản cũ nhất, GIỮ bản mới nhất
rm -rf ~/.hermes/state-snapshots/<tên-snapshot-cũ>
```

---

#### 🟡 Ưu tiên trung bình

**2d. Docker — KIỂM TRA TRƯỚC**
```bash
docker ps -a          # Xem container nào đang chạy
docker images         # Xem image nào đang dùng
```
- Nếu image không có container nào active: `docker image prune -a`
- **KHÔNG** xóa image của container đang chạy (vd: n8n, nginx)
- Volumes: kiểm tra kỹ trước khi `docker volume prune`

**2e. Hermes email_attachments cũ**
```bash
# Xem thư mục nào >30 ngày
find ~/.hermes/email_attachments/ -maxdepth 1 -type d -mtime +30

# Xóa
rm -rf ~/.hermes/email_attachments/YYYY-MM-DD/
```

**2f. audio_cache TTS cũ**
```bash
# Xóa file cũ hơn 7 ngày
find ~/.hermes/audio_cache/ -type f -mtime +7 -delete
```

---

#### 🟢 Ưu tiên thấp

**2g. Git GC nén repo lớn**
```bash
cd /path/to/repo
du -sh .git

# Chạy với timeout ngắn — repo lớn có thể timeout 2 phút
git gc --prune=now 2>&1 | tail -5
```
> ⚠️ **Pitfall:** `git gc --aggressive` trên repo >200MB thường timeout >120s trong terminal foreground.
> Dùng `git gc --prune=now` (không `--aggressive`) hoặc chạy background với `notify_on_complete=true`.

**2h. npm/node cache**
```bash
npm cache clean --force 2>/dev/null || true
```

---

### Bước 3 — Verify & báo cáo

```bash
df -h /
```

Báo cáo dạng bảng:
| Mục | Giải phóng |
|-----|-----------|
| /tmp | X GB |
| pip cache | X MB |
| ... | ... |
| **Tổng** | **X GB** |

Disk **trước**: XX% → Disk **sau**: XX%

---

## Pitfalls quan trọng

1. **Không xóa Docker image đang dùng bởi container active** — check `docker ps -a` trước.
2. **Không `rm -rf /tmp/*`** — xóa từng thư mục tên rõ ràng.
3. **git gc --aggressive timeout** trên repo lớn — dùng `--prune=now` hoặc background process.
4. **state-snapshots** — luôn giữ ít nhất 1 bản mới nhất trước khi xóa.
5. **Docker volumes** — `docker volume prune` có thể xóa data persistent; cần kiểm tra kỹ từng volume.

---

## Baseline Hermes trên server này (`/root/.hermes`)

Các thư mục hay tích lũy nhiều nhất (thứ tự ưu tiên dọn):

| Thư mục | Mô tả | Dọn được |
|---------|-------|----------|
| `state-snapshots/` | Bản backup pre-update | Giữ 1 bản mới nhất |
| `email_attachments/` | Attachment email cũ | >30 ngày |
| `sessions/` | JSON session cũ | Archive nếu cần |
| `audio_cache/` | File TTS mp3/ogg | >7 ngày |
| `migration/` | File migration cũ | Sau khi migrate xong |
| `logs/` | Log file | Rotate nếu >100MB |

---

## References
- `references/cleanup-session-2026-05-25.md` — kết quả session dọn dẹp thực tế, giải phóng ~3GB
