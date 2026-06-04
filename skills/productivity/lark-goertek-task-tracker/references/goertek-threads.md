# GOERTEK Threads & KTX-Báo cáo Details

## 1. Thread Scanning Procedure in Large External Groups

Since external groups restrict search APIs and generic `execute_code` python scripts are blocked/restricted in some configurations, we can use a bash paging loop with `lark-cli` and `python3 -c` parser to scan and extract all `thread_id` values from message pages:

```bash
# Loop through the message pages (descending order) and extract all thread_id mappings
page_token=""
for i in $(seq 1 40); do
  if [ -z "$page_token" ]; then
    result=$(lark-cli im +chat-messages-list --chat-id <chat_id> --as user --page-size 50 --sort desc --format json 2>&1)
  else
    result=$(lark-cli im +chat-messages-list --chat-id <chat_id> --as user --page-size 50 --sort desc --format json --page-token "$page_token" 2>&1)
  fi
  
  echo "$result" | python3 -c "
import sys, json
raw = sys.stdin.read()
idx = raw.index('{')
data = json.loads(raw[idx:])
msgs = data['data']['messages']
for m in msgs:
    tid = m.get('thread_id', '')
    if tid:
        print(f'THREAD|{tid}|{m[\"message_id\"]}|{m[\"create_time\"]}|{m.get(\"sender\",{}).get(\"id\",\"\")}|{m.get(\"content\",\"\")[:120]}')
pt = data['data'].get('page_token','')
hm = data['data'].get('has_more', False)
print(f'META|has_more={hm}|page_token={pt}')
"
  
  # Ensure the page_token variable gets the full length (128+ chars)
  page_token=$(echo "$result" | python3 -c "
import sys, json
raw = sys.stdin.read()
idx = raw.index('{')
data = json.loads(raw[idx:])
print(data['data'].get('page_token',''))
")
  
  has_more=$(echo "$result" | python3 -c "
import sys, json
raw = sys.stdin.read()
idx = raw.index('{')
data = json.loads(raw[idx:])
print(data['data'].get('has_more',''))
")
  
  if [ "$has_more" != "True" ] && [ "$has_more" != "true" ]; then
    break
  fi
done
```

### ⚠️ Pitfall: Page Token Truncation in Bash
Lark API page tokens are long strings (e.g., 128 characters or more, e.g. `4cXSlmN7uFAnWWU5yfIGMJjamdL...`). When printing in pipeline commands, ensure no string cutting or truncation happens (like `head` or terminal width truncation), otherwise subsequent API calls will fail with `invalid page_token` API error code `230001`.

---

## 2. KTX-Báo cáo Thread Details

- **Thread ID**: `omt_196c1eaf68cf1981`
- **Created**: 17/05/2026 by **TA Mẫn Văn Hà**
- **Purpose**: A dedicated thread in `GOERTEK_BÁO CÁO CÔNG VIỆC` (`oc_c999ede161bd4f500eb83c8dfaf92dd0`) to collect all progress photos, pipe layings, sleeve placement and inspection drawings for the Dormitory (nhà KTX) work without cluttering the main channel.
- **Key participants**: TA Mẫn Văn Hà (Manager), TA Nguyễn Sinh Hùng (Supervision), Phùng Xuân Quang (QA/QC), Lê An Thụy (Báo cháy), Đào Văn Đạt (Báo cháy/Bảo dưỡng), Nguyễn Văn Phúc (Đội Toản), TL Xuân Đạt (Bảo dưỡng).
- **Color Coding Rule**:
  - Báo cháy (Fire alarm): **Đỏ (Red)**
  - Loa (PA speaker): **Xanh (Blue/Green)**
  - Exit sự cố (Emergency exit/light): **Vàng (Yellow)**
- **Zones & Scope**:
  - Zone 1: Floor 1-3 (Trục 1-9/L-P)
  - Zone 4: Floor 2
  - Zone 5: Floor 2
