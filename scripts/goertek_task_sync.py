#!/usr/bin/env python3
"""
GOERTEK - Quét tin nhắn giao việc từ nhóm Lark (chỉ từ các TA được chỉ định),
chỉ lấy tin có nội dung giao việc + deadline,
tổng hợp báo cáo hằng ngày gửi cho Boss qua Lark.

Nhóm: GOERTEK_TRAO ĐỔI CÔNG VIỆC (oc_c00846108437ef7596beaec09dfccbed)
Sheet: GOERTEK - Theo dõi giao việc (WmeUsSghGhoYH8tAMqcleIMIgJf)
"""

import json
import re
import subprocess
import sys
from datetime import datetime, timezone, timedelta

# ── Config ────────────────────────────────────────────────────────────────────
CHAT_ID      = "oc_c00846108437ef7596beaec09dfccbed"
SHEET_TOKEN  = "WmeUsSghGhoYH8tAMqcleIMIgJf"
SHEET_ID     = "a5ae30"
SHEET_URL    = "https://pccctruongan.sg.larksuite.com/sheets/WmeUsSghGhoYH8tAMqcleIMIgJf"
LARK_CLI     = "lark-cli"
TZ_VN        = timezone(timedelta(hours=7))

# Chỉ lấy tin nhắn từ các thành viên này
ALLOWED_SENDERS = [
    "TA Mẫn Văn Hà",
    "TA Trần Sơn Trung",
    "TA Nguyễn Ngọc Duy",
    "TA-Nguyễn Quang Long",
]

# Từ khoá nhận diện tin nhắn giao việc
TASK_KEYWORDS = [
    "làm", "thực hiện", "chuẩn bị", "gửi", "nộp", "kiểm tra", "xử lý",
    "hoàn thành", "dứt điểm", "khắc phục", "liên hệ", "báo cáo",
    "yêu cầu", "cần", "nhớ", "lưu ý", "deadline", "trước ngày",
    "hạn", "tuần", "tháng", "ngày", "anh em", "ae"
]

# ── Helpers ───────────────────────────────────────────────────────────────────
def run(cmd: list) -> dict:
    result = subprocess.run(cmd, capture_output=True, text=True)
    try:
        return json.loads(result.stdout)
    except Exception:
        return {"ok": False, "error": result.stderr or result.stdout}


def lark(*args) -> dict:
    return run([LARK_CLI] + list(args))


def is_from_allowed_sender(msg: dict) -> bool:
    """Kiểm tra người gửi có trong danh sách cho phép không."""
    sender_name = msg.get("sender", {}).get("name", "").strip()
    for allowed in ALLOWED_SENDERS:
        # So khớp linh hoạt: bỏ dấu phân cách, so sánh không phân biệt khoảng trắng
        if allowed.replace(" ", "").replace("-", "").lower() in \
           sender_name.replace(" ", "").replace("-", "").lower():
            return True
    return False


def is_task_message(msg: dict) -> bool:
    """Tin nhắn có nội dung giao việc."""
    if msg.get("msg_type") not in ("text", "post"):
        return False
    content = msg.get("content", "").lower()
    return any(kw in content for kw in TASK_KEYWORDS)


def has_deadline(text: str) -> bool:
    """Kiểm tra tin nhắn có chứa deadline/hạn không."""
    patterns = [
        r"deadline",
        r"hạn\s*(?:hoàn\s*thành|chót|cuối)?",
        r"trước\s+ngày",
        r"hoàn\s*thành\s*(?:trước|ngày|vào)",
        r"nộp\s*(?:trước|ngày|vào)",
        r"gửi\s*(?:trước|ngày|vào)",
        r"\d{1,2}[./]\d{1,2}(?:[./]\d{2,4})?",
    ]
    for pat in patterns:
        if re.search(pat, text, re.IGNORECASE):
            return True
    return False


def extract_deadline(text: str) -> str:
    patterns = [
        r"trước ngày\s+(\d{1,2}[./]\d{1,2}(?:[./]\d{2,4})?)",
        r"deadline[:\s]+(\d{1,2}[./]\d{1,2}(?:[./]\d{2,4})?)",
        r"hạn[:\s]+(\d{1,2}[./]\d{1,2}(?:[./]\d{2,4})?)",
        r"(\d{1,2}[./]\d{1,2}[./]\d{2,4})",
        r"(\d{1,2}/\d{1,2})",
    ]
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            return m.group(1)
    return ""


def get_existing_message_ids() -> set:
    result = lark("sheets", "+read",
                  "--url", SHEET_URL,
                  "--sheet-id", SHEET_ID,
                  "--range", "I2:I")
    rows = result.get("data", {}).get("values", []) or []
    return {str(r[0]).strip() for r in rows if r and str(r[0]).strip()}


def get_current_row_count() -> int:
    result = lark("sheets", "+read",
                  "--url", SHEET_URL,
                  "--sheet-id", SHEET_ID,
                  "--range", "A2:A")
    rows = result.get("data", {}).get("values", []) or []
    return sum(1 for r in rows if r and str(r[0]).strip())


def append_rows(rows: list) -> dict:
    return lark("sheets", "+append",
                "--url", SHEET_URL,
                "--sheet-id", SHEET_ID,
                "--values", json.dumps(rows))


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    now_vn = datetime.now(TZ_VN)
    start_of_day = now_vn.replace(hour=7, minute=0, second=0, microsecond=0)
    start_iso = start_of_day.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    end_iso   = now_vn.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    print(f"[{now_vn.strftime('%H:%M %d/%m/%Y')}] Quét tin nhắn từ {start_of_day.strftime('%H:%M')} → {now_vn.strftime('%H:%M')}")

    # 1. Lấy tin nhắn trong ngày
    resp = lark("im", "+chat-messages-list",
                "--chat-id", CHAT_ID,
                "--start", start_iso,
                "--end", end_iso,
                "--sort", "asc",
                "--page-size", "50")

    if not resp.get("ok"):
        print(f"[LỖI] Không lấy được tin nhắn: {resp}")
        sys.exit(1)

    messages = resp.get("data", {}).get("messages", [])
    print(f"  → Tổng tin nhắn: {len(messages)}")

    # 2. Lọc: chỉ từ sender được phép + nội dung giao việc + có deadline
    filtered = []
    for m in messages:
        if not is_from_allowed_sender(m):
            continue
        if not is_task_message(m):
            continue
        if not has_deadline(m.get("content", "")):
            continue
        filtered.append(m)

    print(f"  → Tin nhắn giao việc (có deadline, từ TA chỉ định): {len(filtered)}")

    if not filtered:
        print("\n📋 BÁO CÁO GIAO VIỆC GOERTEK — " + now_vn.strftime("%d/%m/%Y"))
        print("Hôm nay không có công việc mới từ các TA.")
        print(f"\n📊 Sheet đầy đủ: {SHEET_URL}")
        return

    # 3. Loại trùng với sheet
    existing_ids = get_existing_message_ids()
    new_msgs = [m for m in filtered if m.get("message_id") not in existing_ids]
    print(f"  → Việc mới cần thêm: {len(new_msgs)}")

    # 4. Ghi vào sheet (các việc mới)
    if new_msgs:
        current_count = get_current_row_count()
        rows_to_append = []

        for i, msg in enumerate(new_msgs, start=1):
            stt         = current_count + i
            content     = msg.get("content", "")
            sender_name = msg.get("sender", {}).get("name", "")
            mentions    = msg.get("mentions", [])
            assignees   = ", ".join(m["name"] for m in mentions) if mentions else ""
            create_time = msg.get("create_time", "")
            deadline    = extract_deadline(content)
            message_id  = msg.get("message_id", "")

            rows_to_append.append([
                stt,
                content,
                sender_name,
                assignees,
                deadline,
                "Chưa làm",
                "",
                create_time,
                message_id,
            ])

        result = append_rows(rows_to_append)
        if not result.get("ok"):
            print(f"[LỖI] Ghi sheet thất bại: {result}")
            sys.exit(1)
        print(f"  ✅ Đã ghi {len(rows_to_append)} việc vào sheet")
    else:
        rows_to_append = []

    # 5. Tổng hợp báo cáo hằng ngày (tất cả filtered, không chỉ mới)
    print(f"\n{'='*58}")
    print(f"📋 BÁO CÁO GIAO VIỆC GOERTEK — {now_vn.strftime('%d/%m/%Y')}")
    print(f"{'='*58}")
    print(f"⏰ Cập nhật lúc: {now_vn.strftime('%H:%M')} (GMT+7)")
    print(f"📥 Nhóm: GOERTEK_TRAO ĐỔI CÔNG VIỆC")
    print(f"👥 Nguồn: {', '.join(ALLOWED_SENDERS)}")
    print(f"🆕 Việc mới hôm nay: {len(new_msgs)}")
    print(f"📝 Tổng việc trong ngày: {len(filtered)}")
    print()

    # Nhóm theo người giao
    by_sender = {}
    for msg in filtered:
        sender = msg.get("sender", {}).get("name", "Không rõ")
        if sender not in by_sender:
            by_sender[sender] = []
        by_sender[sender].append(msg)

    for sender, msgs in by_sender.items():
        print(f"  👤 {sender} ({len(msgs)} việc)")
        for j, m in enumerate(msgs, 1):
            content = m.get("content", "")
            mentions = m.get("mentions", [])
            assignees = ", ".join(mention["name"] for mention in mentions) if mentions else ""
            deadline = extract_deadline(content)
            create_time = m.get("create_time", "")

            print(f"    [{j}] 📌 {content[:120]}")
            if assignees:
                print(f"         👥 Người thực hiện: {assignees}")
            if deadline:
                print(f"         📅 Hạn: {deadline}")
            print(f"         🕐 Nhắn lúc: {create_time}")
            print()

    print(f"📊 Sheet đầy đủ: {SHEET_URL}")
    print(f"{'='*58}")


if __name__ == "__main__":
    main()
