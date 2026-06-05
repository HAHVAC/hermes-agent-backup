#!/usr/bin/env python3
"""
KTX Daily Report Generator
- Đọc tin nhắn từ thread KTX-Báo cáo (GOERTEK)
- Phân loại theo 4 hệ: Báo cháy, Chữa cháy, Thông gió, Điện
- Tải hình ảnh hiện trường kèm theo từ thread, upload và chèn trực tiếp dưới nội dung text báo cáo (Phương án 1)
- Cập nhật vào Lark Doc chung
- Gửi preview cho Boss duyệt
"""

import sys
import os
import subprocess
import json
import re
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor

# Configurations
os.environ["PATH"] = "/root/.nvm/versions/node/v24.13.0/bin:" + os.environ.get("PATH", "")

# Constants
THREAD_ID = "omt_196c1eaf68cf1981"
CHAT_ID = "oc_c999ede161bd4f500eb83c8dfaf92dd0"
DOC_ID = "KD8Xd3KUjouzhzxq2xolyWAmgkI"

# Sender mapping (resolved from Lark)
SENDER_MAP = {
    "ou_dcae1fcf640febfba998addc9e77b579": "Nguyễn Văn Phúc",
    "ou_feb04970c3c442a8f7fdd61a2daa0f78": "Lê An Thụy",
    "ou_82b3294ee4ddff2abb7a94828e9397aa": "Đào Văn Đạt",
    "ou_49810a6bc1eec25883d0d0807b57bcfe": "TA Mẫn Văn Hà",
    "ou_3c2f50cddac87e6945fe5f8f751fed77": "TA Nguyễn Sinh Hùng",
    "ou_6601b14e9cc7b9af394e6f2ab44c4621": "Phùng Xuân Quang",
}

# Keywords for system classification
SYSTEM_KEYWORDS = {
    "bao_chay": ["báo cháy", "báo chày", "bc ", "báo động", "chuông báo", "khói", "nhiệt", "đầu báo", "đặt âm", "ống âm", "dải ống", "ống lồng", "đặt ống"],
    "chua_chay": ["chữa cháy", "chữu cháy", "bình chữa", "vòi chữa", "van", "hệ nước", "bơm", "hydrant", "sprinkler", "hose reel"],
    "thong_gio": ["thông gió", "thóng gió", "điều hòa", "điều hoà", "ống gió", "fan", "ahu", "fcu", "difuser", "diffuser", "cửa gió"],
    "dien": ["điện", "điện nhẹ", "cáp", "ống điện", "tủ điện", "máng cáp", "cable tray", "đèn", "chiếu sáng", "công tắc", "ổ cắm", "đi dây"],
}


def run_lark_cli(args):
    """Run lark-cli command and return parsed JSON output."""
    cmd = ["lark-cli"] + args + ["--format", "json"]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    output = result.stdout + result.stderr
    try:
        idx = output.index('{')
        return json.loads(output[idx:])
    except (ValueError, json.JSONDecodeError) as e:
        print(f"ERROR parsing lark-cli output: {e}", file=sys.stderr)
        print(f"Output: {output[:500]}", file=sys.stderr)
        return None


def download_and_upload_image(message_id, image_key):
    """Download an image from Lark message and upload it to Drive Media to get a file_token."""
    temp_filename = f"temp_{message_id}_{image_key}.png"
    # use relative path since lark-cli only allows relative paths for --output
    temp_filepath = temp_filename
    
    # 1. Download image from message
    dl_args = [
        "im", "+messages-resources-download",
        "--message-id", message_id,
        "--file-key", image_key,
        "--type", "image",
        "--output", temp_filepath,
        "--as", "user"
    ]
    print(f"  -> Downloading image {image_key} from message {message_id}...")
    dl_res = run_lark_cli(dl_args)
    if not dl_res or not dl_res.get("ok"):
        print(f"  ❌ Failed to download image {image_key}: {dl_res}", file=sys.stderr)
        if os.path.exists(temp_filepath):
            try: os.remove(temp_filepath)
            except: pass
        return None
        
    actual_path = dl_res["data"].get("saved_path")
    if not actual_path or not os.path.exists(actual_path):
        actual_path = temp_filepath
        if not os.path.exists(actual_path):
            print(f"  ❌ Downloaded file not found at {actual_path}", file=sys.stderr)
            return None
            
    # 2. Upload image to Lark Drive DocxMedia
    file_size = os.path.getsize(actual_path)
    upload_args = [
        "api", "POST", "/open-apis/drive/v1/medias/upload_all",
        "--file", f"file={temp_filepath}",
        "--data", json.dumps({
            "file_name": os.path.basename(actual_path),
            "parent_type": "docx_image",
            "parent_node": DOC_ID,
            "size": file_size
        }),
        "--as", "user"
    ]
    print(f"  -> Uploading image {image_key} to Lark Drive (size: {file_size} bytes)...")
    up_res = run_lark_cli(upload_args)
    
    # Clean up temp file
    if os.path.exists(actual_path):
        try: os.remove(actual_path)
        except: pass
        
    if up_res and up_res.get("code") == 0:
        file_token = up_res["data"].get("file_token")
        print(f"  ✅ Uploaded image. File token: {file_token}")
        return file_token
    else:
        print(f"  ❌ Failed to upload image {image_key}: {up_res}", file=sys.stderr)
        return None


def get_thread_messages_with_images(target_date):
    """
    Get all messages from KTX thread for a specific date.
    Groups images with their corresponding preceding text messages.
    Concurrently downloads and uploads images.
    """
    all_msgs = []
    page_token = ""

    while True:
        args = [
            "im", "+threads-messages-list",
            "--thread", THREAD_ID,
            "--as", "user",
            "--sort", "desc",
            "--page-size", "50",
        ]
        if page_token:
            args.extend(["--page-token", page_token])

        data = run_lark_cli(args)
        if not data or "data" not in data:
            break

        msgs = data["data"]["messages"]
        reached_old = False

        for m in msgs:
            ct = m.get("create_time", "")
            # Check if message is from target date
            if target_date in ct:
                all_msgs.append(m)
            elif ct < target_date:
                # Messages are sorted desc, so we've passed our target date
                reached_old = True

        has_more = data["data"].get("has_more", False)
        page_token = data["data"].get("page_token", "")

        if not has_more or reached_old:
            break

    # Process chronologically to group images under their text reports
    all_msgs.reverse()
    
    reports = []
    current_report = None
    images_to_process = []  # List of dict: {"msg_id": msg_id, "image_key": img_key, "report_idx": idx}
    
    for m in all_msgs:
        mtype = m.get("msg_type", "")
        sender_id = m.get("sender", {}).get("id", "")
        sender_name = SENDER_MAP.get(sender_id, sender_id[:12])
        ct = m.get("create_time", "")
        content = m.get("content", "")
        msg_id = m.get("message_id", "")
        thread_pos = m.get("thread_message_position", "")

        if mtype == "text":
            current_report = {
                "time": ct,
                "sender": sender_name,
                "sender_id": sender_id,
                "content": content,
                "msg_id": msg_id,
                "thread_pos": thread_pos,
                "image_tokens": []
            }
            reports.append(current_report)
        elif mtype == "image":
            img_match = re.search(r"\[Image:\s*(img_v3_[a-zA-Z0-9_\-]+)\]", content)
            if img_match:
                img_key = img_match.group(1)
                
                # Check if this image belongs to the active report (same sender)
                if current_report and current_report["sender_id"] == sender_id:
                    report_idx = reports.index(current_report)
                else:
                    # Orphan image or different sender: create a placeholder report
                    current_report = {
                        "time": ct,
                        "sender": sender_name,
                        "sender_id": sender_id,
                        "content": "[Hình ảnh hiện trường]",
                        "msg_id": msg_id,
                        "thread_pos": thread_pos,
                        "image_tokens": []
                    }
                    reports.append(current_report)
                    report_idx = len(reports) - 1
                
                images_to_process.append({
                    "msg_id": msg_id,
                    "image_key": img_key,
                    "report_idx": report_idx
                })

    all_image_count = len(images_to_process)
    
    # Concurrently download and upload all images using ThreadPoolExecutor
    if images_to_process:
        print(f"  -> Processing {all_image_count} images concurrently...")
        
        def process_single_image(img_info):
            file_token = download_and_upload_image(img_info["msg_id"], img_info["image_key"])
            return img_info["report_idx"], file_token

        # Use up to 8 threads to balance speed and api rate limits
        with ThreadPoolExecutor(max_workers=8) as executor:
            results = executor.map(process_single_image, images_to_process)
            
        for report_idx, file_token in results:
            if file_token:
                reports[report_idx]["image_tokens"].append(file_token)

    return reports, all_image_count


def classify_system(content):
    """Classify a message into one of the 4 systems based on keywords."""
    content_lower = content.lower()
    scores = {}
    for system, keywords in SYSTEM_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in content_lower)
        if score > 0:
            scores[system] = score

    if not scores:
        # Default to bao_chay if it mentions KTX construction work
        if any(w in content_lower for w in ["ống", "thi công", "hiện trường", "nghiệm thu", "tiến độ", "zone", "tầng", "sàn"]):
            return "bao_chay"
        return "other"

    return max(scores, key=scores.get)


def extract_zone_floor(content):
    """Extract zone and floor info from message content."""
    zone = ""
    floor = ""

    # Extract Zone
    zone_match = re.search(r'[Zz]one\s*(\d+)', content, re.IGNORECASE)
    if zone_match:
        zone = f"Zone {zone_match.group(1)}"

    # Extract floor
    floor_match = re.search(r'tầng\s*(\d+)', content, re.IGNORECASE)
    if floor_match:
        floor = f"Tầng {floor_match.group(1)}"

    # Extract "sàn"
    san_match = re.search(r'sàn\s*tầng\s*(\d+)', content, re.IGNORECASE)
    if san_match and not floor:
        floor = f"Sàn Tầng {san_match.group(1)}"

    return zone, floor


def generate_daily_xml(target_date, reports, image_count):
    """Generate XML content for the daily report section."""
    # Group messages by system
    systems = {
        "bao_chay": {"name": "🔴 Hệ Báo cháy", "emoji": "🔴", "reports": []},
        "chua_chay": {"name": "🔵 Hệ Chữa cháy", "emoji": "🔵", "reports": []},
        "thong_gio": {"name": "🟢 Hệ Thông gió", "emoji": "🟢", "reports": []},
        "dien": {"name": "🟡 Hệ Điện", "emoji": "🟡", "reports": []},
    }

    for r in reports:
        sys_key = classify_system(r["content"])
        zone, floor = extract_zone_floor(r["content"])
        if sys_key in systems:
            systems[sys_key]["reports"].append({
                **r,
                "zone": zone,
                "floor": floor,
            })

    # Build XML
    date_display = datetime.strptime(target_date, "%Y-%m-%d").strftime("%d/%m/%Y")
    xml_parts = []
    xml_parts.append(f'<h1>📅 Báo cáo ngày {date_display}</h1>')

    for sys_key, sys_data in systems.items():
        sys_reports = sys_data["reports"]
        xml_parts.append(f'<h2>{sys_data["name"]}</h2>')

        if not sys_reports:
            xml_parts.append(f'<callout emoji="ℹ️" background-color="light-gray"><p>Chưa có báo cáo trong ngày {date_display}.</p></callout>')
        else:
            # Sender summary
            sys_senders = set(r["sender"] for r in sys_reports)
            xml_parts.append(f'<callout emoji="ℹ️" background-color="light-gray">')
            xml_parts.append(f'<p>Người gửi: <b>{", ".join(sys_senders)}</b> | Số báo cáo: {len(sys_reports)}</p>')
            xml_parts.append(f'</callout>')

            # Table
            xml_parts.append('<table>')
            # Column widths: Time, Area, Sender, Content (including images if any)
            xml_parts.append('<colgroup><col span="1" width="80"/><col span="1" width="130"/><col span="1" width="130"/><col span="1" width="460"/></colgroup>')
            xml_parts.append('<thead><tr><th background-color="light-gray">Giờ</th><th background-color="light-gray">Khu vực</th><th background-color="light-gray">Người gửi</th><th background-color="light-gray">Nội dung</th></tr></thead>')
            xml_parts.append('<tbody>')
            for r in sys_reports:
                time_short = r["time"].split(" ")[1][:5] if " " in r["time"] else r["time"]
                area = f'{r["zone"]}, {r["floor"]}' if r["zone"] and r["floor"] else (r["zone"] or r["floor"] or "—")
                
                # Escape XML special chars in content
                content_safe = r["content"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                
                # Append images directly under the text inside the table cell (if images exist)
                # Form: <img src="TOKEN" width="120" /> or standard format for layout
                if r["image_tokens"]:
                    img_tags = ""
                    for token in r["image_tokens"]:
                        img_tags += f'<br/><img src="{token}" width="200" />'
                    content_cell = f'<p>{content_safe}{img_tags}</p>'
                else:
                    content_cell = f'<p>{content_safe}</p>'
                    
                xml_parts.append(f'<tr><td>{time_short}</td><td>{area}</td><td>{r["sender"]}</td><td>{content_cell}</td></tr>')
            xml_parts.append('</tbody></table>')

        xml_parts.append('<hr/>')

    # Summary table
    xml_parts.append(f'<h2>📊 Tổng kết ngày {date_display}</h2>')
    xml_parts.append('<table>')
    xml_parts.append('<colgroup><col span="1" width="180"/><col span="1" width="100"/><col span="1" width="120"/><col span="1" width="120"/></colgroup>')
    xml_parts.append('<thead><tr><th background-color="light-gray">Hệ thống</th><th background-color="light-gray">Số báo cáo</th><th background-color="light-gray">Khu vực</th><th background-color="light-gray">Trạng thái</th></tr></thead>')
    xml_parts.append('<tbody>')

    sys_labels = {
        "bao_chay": "🔴 Báo cháy",
        "chua_chay": "🔵 Chữa cháy",
        "thong_gio": "🟢 Thông gió",
        "dien": "🟡 Điện",
    }

    issues = []
    for sys_key, sys_data in systems.items():
        sys_reports = sys_data["reports"]
        zones = set(r["zone"] for r in sys_reports if r["zone"])
        if sys_reports:
            status = '<span text-color="green">Đang thi công</span>'
        else:
            status = "—"
            issues.append(sys_labels[sys_key])

        xml_parts.append(f'<tr><td>{sys_labels[sys_key]}</td><td>{len(sys_reports) or "—"}</td><td>{", ".join(sorted(zones)) or "—"}</td><td>{status}</td></tr>')

    xml_parts.append('</tbody></table>')

    if issues:
        xml_parts.append('<callout emoji="⚠️" background-color="light-yellow" border-color="yellow">')
        xml_parts.append(f'<p><b>Vấn đề / Ghi chú:</b> Chưa có báo cáo cho {", ".join(issues)} trong ngày.</p>')
        xml_parts.append('</callout>')

    return "\n".join(xml_parts)


def main():
    # Target date: can be passed as argument, default = today VN time
    if len(sys.argv) > 1:
        target_date = sys.argv[1]
        date_display = datetime.strptime(target_date, "%Y-%m-%d").strftime("%d/%m/%Y")
    else:
        vn_now = datetime.utcnow() + timedelta(hours=7)
        target_date = vn_now.strftime("%Y-%m-%d")
        date_display = vn_now.strftime("%d/%m/%Y")

    print(f"=== KTX Daily Report for {date_display} ===")
    print(f"Target date: {target_date}")

    # Step 1: Get messages and images from thread
    print("\n[1/3] Fetching thread messages & uploading images...")
    reports, image_count = get_thread_messages_with_images(target_date)
    print(f"  Found {len(reports)} grouped report entries, {image_count} total images downloaded & uploaded")

    # If no report found at all, skip writing to Doc (silent mode)
    if not reports and image_count == 0:
        print("\nNo messages or images found for today. Exiting silently (Silent mode).")
        # Return [SILENT] token for cron job to identify and skip notification
        print("[SILENT]")
        sys.exit(0)

    # Step 2: Generate XML
    print("\n[2/3] Generating report XML...")
    xml_content = generate_daily_xml(target_date, reports, image_count)

    # Save to temp file for debugging
    with open("/tmp/ktx_daily_report_latest.xml", "w") as f:
        f.write(xml_content)
    print(f"  XML saved to /tmp/ktx_daily_report_latest.xml ({len(xml_content)} bytes)")

    # Step 3: Append to Lark Doc
    print("\n[3/3] Appending to Lark Doc...")
    append_result = run_lark_cli([
        "docs", "+update", "--api-version", "v2",
        "--doc", DOC_ID,
        "--command", "append",
        "--content", xml_content,
    ])

    if append_result and append_result.get("ok"):
        print(f"  ✅ Report appended to doc successfully!")
        doc_url = f"https://pccctruongan.sg.larksuite.com/docx/{DOC_ID}"
        print(f"\n📝 Doc URL: {doc_url}")
        print(f"\n📅 Date: {date_display}")
        print(f"📊 Summary: {len(reports)} entries, {image_count} images")
        print(f"🔗 URL: {doc_url}")
    else:
        print(f"  ❌ Failed to append report: {append_result}")
        sys.exit(1)


if __name__ == "__main__":
    main()
