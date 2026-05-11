#!/usr/bin/env python3
"""
Daily Email Report - pcccthanglong.tlc@gmail.com
Outputs raw structured data for AI to translate and format.

Attachment handling:
- Lists attachment filenames and MIME types only (no download/upload).
"""

import base64
import importlib.util
import json
import os
import subprocess
import sys
from datetime import datetime, timezone, timedelta

GAPI = "/root/.hermes/skills/productivity/google-workspace/scripts/google_api.py"
GWS_BIN = "/root/.local/bin/gws"
TZ_VN = timezone(timedelta(hours=7))

API_ENV = {
    "PATH": "/usr/bin:/bin:/root/.local/bin",
    "HERMES_GWS_BIN": GWS_BIN,
    "HOME": "/root",
    "HERMES_HOME": "/root/.hermes",
}


def load_google_api_module():
    spec = importlib.util.spec_from_file_location("hermes_google_api", GAPI)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build_service(api, version):
    mod = load_google_api_module()
    return mod.build_service(api, version)


def run_gmail(query, max_results=50):
    result = subprocess.run(
        [sys.executable, GAPI, "gmail", "search", query, "--max", str(max_results)],
        capture_output=True,
        text=True,
        env=API_ENV,
    )
    try:
        data = json.loads(result.stdout)
        return data if isinstance(data, list) else []
    except Exception:
        return []


def get_full_message(service, msg_id):
    try:
        return service.users().messages().get(userId="me", id=msg_id, format="full").execute()
    except Exception:
        return {}


def decode_body_data(data):
    if not data:
        return ""
    try:
        return base64.urlsafe_b64decode(data.encode("utf-8")).decode("utf-8", errors="replace")
    except Exception:
        return ""


def walk_parts(part):
    if not part:
        return
    yield part
    for child in part.get("parts", []) or []:
        yield from walk_parts(child)


def extract_message_body(full_msg):
    payload = full_msg.get("payload", {})
    html_fallback = ""
    for part in walk_parts(payload):
        mime = part.get("mimeType", "")
        data = part.get("body", {}).get("data", "")
        if mime == "text/plain" and data:
            return decode_body_data(data)
        if mime == "text/html" and data and not html_fallback:
            html_fallback = decode_body_data(data)
    return html_fallback


def list_attachments(full_msg):
    """List attachment filenames only — no download/upload."""
    attachments = []
    for part in walk_parts(full_msg.get("payload", {})):
        filename = part.get("filename") or ""
        body = part.get("body", {}) or {}
        if not filename:
            continue
        attachments.append({
            "filename": filename,
            "mime_type": part.get("mimeType", ""),
            "size_bytes": body.get("size", 0),
        })
    return attachments


def clean_body(text, max_len=1000):
    """Extract meaningful content, remove signatures/footers."""
    if not text:
        return ""
    lines = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        low = line.lower()
        if any(marker in low for marker in [
            "unsubscribe", "click here", "view in browser", "privacy policy",
            "©", "copyright", "all rights reserved", "sent from my", "get outlook",
            "________________________________", "---", "___",
            "https://", "http://", "www.",
        ]):
            continue
        lines.append(line)

    text = "\n".join(lines)
    if len(text) > max_len:
        text = text[:max_len] + "..."
    return text.strip()


def format_date(date_str):
    try:
        from email.utils import parsedate_to_datetime
        dt = parsedate_to_datetime(date_str)
        dt_vn = dt.astimezone(TZ_VN)
        days_vn = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"]
        day_name = days_vn[dt_vn.weekday()]
        return f"{day_name}, {dt_vn.strftime('%d/%m/%Y %H:%M')}"
    except Exception:
        return date_str


def build_email_item(msg, full_msg, direction):
    body = extract_message_body(full_msg) or msg.get("snippet", "")
    item = {
        "subject": msg.get("subject", "(Không có tiêu đề)"),
        "date": format_date(msg.get("date", "")),
        "body": clean_body(body),
        "attachments": list_attachments(full_msg),
    }
    if direction == "inbox":
        item["from"] = msg.get("from", "N/A")
        item["to"] = msg.get("to", "N/A")
    else:
        item["to"] = msg.get("to", "N/A")
    return item


def main():
    now = datetime.now(TZ_VN)
    report_date = now.strftime("%d/%m/%Y")
    report_day = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"][now.weekday()]

    inbox = run_gmail("in:inbox newer_than:1d", max_results=30)
    sent = run_gmail("in:sent newer_than:1d", max_results=30)

    gmail_service = build_service("gmail", "v1")

    out = {
        "meta": {
            "account": "pcccthanglong.tlc@gmail.com",
            "date": report_date,
            "day": report_day,
            "time": now.strftime("%H:%M"),
            "inbox_count": len(inbox),
            "sent_count": len(sent),
        },
        "inbox": [],
        "sent": [],
    }

    for msg in inbox:
        full = get_full_message(gmail_service, msg.get("id", ""))
        out["inbox"].append(build_email_item(msg, full, "inbox"))

    for msg in sent:
        full = get_full_message(gmail_service, msg.get("id", ""))
        out["sent"].append(build_email_item(msg, full, "sent"))

    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
