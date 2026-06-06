#!/usr/bin/env python3
"""
KTX Daily Report Generator (Updated version)
- Đọc tin nhắn từ thread KTX-Báo cáo (GOERTEK)
- Phân loại theo 4 hệ: Báo cháy, Chữa cháy, Thông gió, Điện
- Tải hình ảnh hiện trường kèm theo từ thread, đổi tên theo yyyy-mm-dd-noidung.png
- Upload các hình ảnh này vào 1 thư mục Lark Drive thay vì chèn trực tiếp vào Lark Doc
- Tổng hợp báo cáo hàng ngày vào Lark Doc chung:
  + Mỗi ngày chỉ cần mỗi hệ 1 dòng tóm tắt các hoạt động, không báo theo giờ.
  + Báo cáo quân số nếu có.
  + Dẫn link thư mục Drive chứa ảnh của ngày đó hoặc thư mục tổng.
"""

import sys
import os
import subprocess
import json
import re
import urllib.parse
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor

# Configurations
os.environ["PATH"] = "/root/.nvm/versions/node/v24.13.0/bin:" + os.environ.get("PATH", "")

# Constants
THREAD_ID = "omt_196c1eaf68cf1981"
CHAT_ID = "oc_c999ede161bd4f500eb83c8dfaf92dd0"
DOC_ID = "KD8Xd3KUjouzhzxq2xolyWAmgkI"
# Thư mục gốc chứa ảnh báo cáo KTX trên Lark Drive
DRIVE_FOLDER_TOKEN = "RgFvfLbrlllgSsdg7VzlZz59ggg"

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
    
    first_brace = output.find('{')
    last_brace = output.rfind('}')
    if first_brace != -1 and last_brace != -1:
        try:
            return json.loads(output[first_brace:last_brace+1])
        except json.JSONDecodeError as e:
            print(f"ERROR parsing lark-cli output: {e}", file=sys.stderr)
            print(f"Output: {output[:1000]}", file=sys.stderr)
            return None
    else:
        print(f"ERROR: No JSON block found in output", file=sys.stderr)
        print(f"Output: {output[:1000]}", file=sys.stderr)
        return None


def clean_filename(name):
    """Clean Vietnamese text to English lowercase words separated by hyphens (max 60 chars)."""
    name = name.lower()
    name = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', name)
    name = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', name)
    name = re.sub(r'[ìíịỉĩ]', 'i', name)
    name = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', name)
    name = re.sub(r'[ùúụủũưừứựửữ]', 'u', name)
    name = re.sub(r'[ỳýỵỷỹ]', 'y', name)
    name = re.sub(r'đ', 'd', name)
    name = re.sub(r'[^a-z0-9\s_\-]', '', name)
    name = re.sub(r'[\s_\-]+', '-', name).strip('-')
    return name[:60] if name else "hinh-anh"


def create_daily_folder(target_date):
    """Create a subfolder for the target date inside the KTX report images folder."""
    folder_name = f"Báo cáo KTX {target_date}"
    args = [
        "drive", "+create-folder",
        "--name", folder_name,
        "--folder-token", DRIVE_FOLDER_TOKEN,
        "--as", "user"
    ]
    print(f"  -> Creating Drive folder '{folder_name}'...")
    res = run_lark_cli(args)
    if res and res.get("ok"):
        folder_token = res["data"].get("folder_token")
        url = res["data"].get("url")
        print(f"  ✅ Created subfolder. Token: {folder_token}, URL: {url}")
        return folder_token, url
    else:
        print(f"  ❌ Failed to create subfolder, using root folder token instead. Error: {res}", file=sys.stderr)
        return DRIVE_FOLDER_TOKEN, None


def download_and_upload_image_to_drive(message_id, image_key, target_folder_token, new_name):
    """Download image from Lark message and upload it to specific Drive folder with a clean name."""
    temp_filename = f"temp_{message_id}_{image_key}.png"
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
    dl_res = run_lark_cli(dl_args)
    if not dl_res or not dl_res.get("ok"):
        print(f"  ❌ Failed to download image {image_key}", file=sys.stderr)
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
            
    # 2. Upload image to Lark Drive folder with new name
    upload_args = [
        "drive", "+upload",
        "--file", temp_filepath,
        "--name", f"{new_name}.png",
        "--folder-token", target_folder_token,
        "--as", "user"
    ]
    print(f"  -> Uploading to Drive: {new_name}.png ...")
    up_res = run_lark_cli(upload_args)
    
    # Clean up temp file
    if os.path.exists(actual_path):
        try: os.remove(actual_path)
        except: pass
        
    if up_res and up_res.get("ok"):
        print(f"  ✅ Uploaded image successfully: {new_name}.png")
        return True
    else:
        print(f"  ❌ Failed to upload image {image_key} to Drive: {up_res}", file=sys.stderr)
        return False


def get_thread_messages_with_images(target_date):
    """
    Get all messages from KTX thread for a specific date.
    Groups images with their corresponding preceding text messages.
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
                "images": []
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
                        "images": []
                    }
                    reports.append(current_report)
                    report_idx = len(reports) - 1
                
                images_to_process.append({
                    "msg_id": msg_id,
                    "image_key": img_key,
                    "report_idx": report_idx
                })

    return reports, images_to_process


def process_images_concurrently(images_to_process, reports, target_date, target_folder_token):
    """Concurrently downloads, renames and uploads images to Drive folder."""
    if not images_to_process:
        return 0

    print(f"  -> Renaming and uploading {len(images_to_process)} images concurrently...")
    
    # We will build image filenames like yyyy-mm-dd-noidung-index.png
    # Let's count how many images are under each report index to add sequence numbers
    report_img_counts = {}
    for idx, img_info in enumerate(images_to_process):
        r_idx = img_info["report_idx"]
        report_img_counts[r_idx] = report_img_counts.get(r_idx, 0) + 1
        img_info["seq"] = report_img_counts[r_idx]

    def process_single_image(img_info):
        r_idx = img_info["report_idx"]
        report = reports[r_idx]
        seq = img_info["seq"]
        
        # Determine descriptive name based on report content
        desc = report["content"]
        # Skip generic text placeholder
        if desc == "[Hình ảnh hiện trường]":
            desc = f"{report['sender']}-hinh-anh"
        
        clean_desc = clean_filename(desc)
        # Final name structure: yyyy-mm-dd-noidung-index (no accents)
        # e.g., 2026-06-06-tien-do-ong-am-1
        new_name = f"{target_date}-{clean_desc}"
        if report_img_counts[r_idx] > 1:
            new_name += f"-{seq}"
            
        success = download_and_upload_image_to_drive(
            img_info["msg_id"], 
            img_info["image_key"], 
            target_folder_token, 
            new_name
        )
        return success

    # Use ThreadPoolExecutor to upload concurrently
    # Rate limit from Lark API for image upload is strict: use max_workers=2 and add minor delay to prevent rate limiting.
    import time
    def process_single_image_with_delay(img_info):
        # Add a tiny delay between starts to prevent simultaneous burst
        time.sleep(1.0)
        return process_single_image(img_info)

    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(process_single_image_with_delay, images_to_process))
        
    uploaded_count = sum(1 for r in results if r)
    return uploaded_count


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


def extract_quansobuoc(content):
    """Extract worker count (quân số) if mentioned."""
    # Match pattern "quân số 12" or "12 người"
    qs_match = re.search(r'(?:qu\u00e2n s\u1ed1|quan so)(?:\s*:|\s+l\u00e0)?\s*(\d+)|(\d+)\s*(?:ng\u01b0\u1eddi|nh\u00e2n s\u1ef1)', content, re.IGNORECASE)
    if qs_match:
        val = qs_match.group(1) or qs_match.group(2)
        try:
            return int(val)
        except:
            pass
    return None


def generate_daily_xml(target_date, reports, folder_url):
    """
    Generate XML content for the daily report section.
    Requirements:
    - 1 row per system (no hourly log table).
    - Summarizes all reports of each system into that single row.
    - Reports total worker count (quân số) if available.
    - Embeds link to the Lark Drive folder containing photos.
    """
    date_display = datetime.strptime(target_date, "%Y-%m-%d").strftime("%d/%m/%Y")
    
    # 1. Group data and extract summaries
    systems = {
        "bao_chay": {"name": "🔴 Hệ Báo cháy", "reports": [], "zones": set(), "senders": set(), "text_summaries": [], "workers": 0},
        "chua_chay": {"name": "🔵 Hệ Chữa cháy", "reports": [], "zones": set(), "senders": set(), "text_summaries": [], "workers": 0},
        "thong_gio": {"name": "🟢 Hệ Thông gió", "reports": [], "zones": set(), "senders": set(), "text_summaries": [], "workers": 0},
        "dien": {"name": "🟡 Hệ Điện", "reports": [], "zones": set(), "senders": set(), "text_summaries": [], "workers": 0},
    }

    total_workers_found = 0
    
    for r in reports:
        sys_key = classify_system(r["content"])
        if sys_key not in systems:
            continue
            
        sys_data = systems[sys_key]
        sys_data["reports"].append(r)
        
        # Extract zone/floor
        zone, floor = extract_zone_floor(r["content"])
        loc = f"{zone} {floor}".strip()
        if loc:
            sys_data["zones"].add(loc)
            
        sys_data["senders"].add(r["sender"])
        
        # Clean text content to add to summary
        txt = r["content"].strip()
        # Avoid placeholder images text
        if txt and txt != "[Hình ảnh hiện trường]" and not txt.startswith("[Image:"):
            # Escape XML special chars
            txt_safe = txt.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            sys_data["text_summaries"].append(f"- {r['sender']}: {txt_safe}")
            
        # Extract workers
        workers = extract_quansobuoc(r["content"])
        if workers:
            sys_data["workers"] = max(sys_data["workers"], workers)

    # Calculate total workers
    total_workers_found = sum(s["workers"] for s in systems.values())

    # Build XML
    xml_parts = []
    xml_parts.append(f'<h1>📅 Báo cáo ngày {date_display}</h1>')

    # Add Callout for summary overview
    xml_parts.append('<callout emoji="📊" background-color="light-gray" border-color="light-blue">')
    if total_workers_found > 0:
        xml_parts.append(f'<p><b>Tổng quân số KTX:</b> {total_workers_found} người</p>')
    else:
        xml_parts.append('<p><b>Tổng quân số KTX:</b> Không ghi nhận báo cáo quân số cụ thể</p>')
        
    if folder_url:
        xml_parts.append(f'<p><b>Folder hình ảnh hiện trường:</b> <a href="{folder_url}">Xem trên Lark Drive</a></p>')
    else:
        xml_parts.append(f'<p><b>Folder hình ảnh hiện trường:</b> <a href="https://pccctruongan.sg.larksuite.com/drive/folder/{DRIVE_FOLDER_TOKEN}">Xem trên Lark Drive</a></p>')
    xml_parts.append('</callout>')

    # Table: 1 row per system
    xml_parts.append('<table>')
    # Column widths: System, Area, Details / Senders, Workers
    xml_parts.append('<colgroup><col span="1" width="180"/><col span="1" width="180"/><col span="1" width="360"/><col span="1" width="80"/></colgroup>')
    xml_parts.append('<thead><tr><th background-color="light-gray">Hệ thống</th><th background-color="light-gray">Khu vực</th><th background-color="light-gray">Nội dung báo cáo chi tiết</th><th background-color="light-gray">Quân số</th></tr></thead>')
    xml_parts.append('<tbody>')

    for sys_key, sys_data in systems.items():
        if sys_data["reports"]:
            area_str = ", ".join(sorted(sys_data["zones"])) if sys_data["zones"] else "Tại công trường"
            
            # Form detailed report list
            if sys_data["text_summaries"]:
                details_str = "<br/>".join(sys_data["text_summaries"])
            else:
                details_str = "Gửi hình ảnh hiện trường thi công."
                
            workers_str = str(sys_data["workers"]) if sys_data["workers"] > 0 else "Có"
            
            xml_parts.append(f'<tr><td><b>{sys_data["name"]}</b></td><td>{area_str}</td><td>{details_str}</td><td>{workers_str}</td></tr>')
        else:
            xml_parts.append(f'<tr><td>{sys_data["name"]}</td><td>—</td><td>Chưa có báo cáo.</td><td>—</td></tr>')

    xml_parts.append('</tbody></table>')
    xml_parts.append('<hr/>')

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
    print("\n[1/4] Fetching thread messages & image metadata...")
    reports, images_to_process = get_thread_messages_with_images(target_date)
    print(f"  Found {len(reports)} grouped report entries, {len(images_to_process)} images to download")

    # If no report found at all, skip writing to Doc (silent mode)
    if not reports and len(images_to_process) == 0:
        print("\nNo messages or images found for today. Exiting silently (Silent mode).")
        # Return [SILENT] token for cron job to identify and skip notification
        print("[SILENT]")
        sys.exit(0)

    # Step 2: Create subfolder for today's images
    print("\n[2/4] Creating Lark Drive subfolder...")
    folder_token, folder_url = create_daily_folder(target_date)

    # Step 3: Process and upload images to the folder
    uploaded_image_count = 0
    if images_to_process:
        print("\n[3/4] Downloading, renaming and uploading images to Drive folder...")
        uploaded_image_count = process_images_concurrently(images_to_process, reports, target_date, folder_token)
        print(f"  Successfully renamed & uploaded {uploaded_image_count}/{len(images_to_process)} images to Lark Drive")
    else:
        print("\n[3/4] No images to upload today.")

    # Step 4: Generate XML and append to Lark Doc
    print("\n[4/4] Generating report XML & Appending to Lark Doc...")
    xml_content = generate_daily_xml(target_date, reports, folder_url)

    # Save to temp file for debugging
    with open("/tmp/ktx_daily_report_latest.xml", "w") as f:
        f.write(xml_content)
    print(f"  XML saved to /tmp/ktx_daily_report_latest.xml ({len(xml_content)} bytes)")

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
        print(f"📊 Summary: {len(reports)} entries processed, {uploaded_image_count} images renamed & uploaded")
        if folder_url:
            print(f"📂 Drive Folder: {folder_url}")
    else:
        print(f"  ❌ Failed to append report: {append_result}")
        sys.exit(1)


if __name__ == "__main__":
    main()
