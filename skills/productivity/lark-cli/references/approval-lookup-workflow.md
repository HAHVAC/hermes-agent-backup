# Lark Approval Lookup Workflow

When a user provides an approval **serial_number** (e.g. `202605270007`) or a keyword (e.g. "xương trần giả"), you must find the corresponding `instance_code` (UUID) before calling `approval instances get`.

## Step 1 — Determine search scope

- **User's own approvals**: `approval instances initiated --as user` returns up to 50 instances the current user initiated. Check `serial_number` field and `summaries` for keyword match.
- **Others' approvals (where user is approver)**: `approval tasks query --as user --params '{"topic":"1","page_size":50}'` for pending, or `topic:"2"` for processed. Each task has `instance_code` and `summaries`.

## Step 2 — Search by keyword in summaries

```python
# Search across tasks for keyword match
for topic in ["1", "2"]:
    result = run("lark-cli approval tasks query --as user "
                 f"--params '{json.dumps({'topic': topic, 'page_size': 50})}' "
                 "--format json")
    for task in result["data"]["tasks"]:
        summaries = {s["key"]: s["value"] for s in task.get("summaries", [])}
        content = " ".join(summaries.values())
        if keyword.lower() in content.lower():
            print(f"Found! instance_code={task['instance_code']}")
```

## Step 3 — Get full detail

```bash
lark-cli approval instances get --as user \
  --params '{"instance_code":"<UUID>","locale":"vi-VN","user_id_type":"open_id"}' \
  --format json
```

The response `data.form` is a JSON-encoded string. Parse it twice (json.loads on the string, then iterate). Key fields:
- `serial_number` — the human-readable approval number
- `instance_code` — the UUID
- `status` — PENDING / APPROVED / REJECTED / CANCELED
- `form` — contains all form widgets including repeated detail sections
- Attachments are in the form under `Tệp đính kèm`

## Step 4 — Compare for duplicates

When checking if a cost/expense is duplicated:
1. Search both `topic=1` (pending) and `topic=2` (processed) for the same keyword
2. For each match, extract: `serial_number`, `Nội dung thanh toán`, `Thành tiền`, `Ngày thanh toán`, attachment URLs
3. Compare amounts, dates, and detail line items
4. Check if `serial_number` sequence makes sense (e.g. "lần 1" before "lần 2")

## Bulk serial-number lookup (when keyword search in summaries isn't enough)

`tasks query` does NOT return `serial_number` — it only returns `instance_code`, `summaries`, `title`, etc. When you need to find an approval by serial number or scan all serials for a pattern, you must iterate:

### Step 1 — Collect all instance_codes

```python
# Get pending (topic=1) and processed (topic=2) tasks
for topic in ["1", "2"]:
    result = run("lark-cli approval tasks query --as user "
                 f"--params '{json.dumps({'topic': topic, 'page_size': 50})}' "
                 "--page-all --format json")
    for task in result["data"]["tasks"]:
        codes.add(task["instance_code"])

# Also check initiated (user's own approvals)
result = run("lark-cli approval instances initiated --as user --format json")
for inst in result["data"]["instances"]:
    codes.add(inst["instance_code"])
```

### Step 2 — Batch `instances get` and check serial_number

```python
matches = []
for code in codes:
    result = run(["lark-cli", "approval", "instances", "get", "--as", "user",
                  "--params", json.dumps({"instance_code": code, "locale": "vi-VN",
                                          "user_id_type": "open_id"}),
                  "--format", "json"])
    data = json.loads(result.stdout)
    sn = data.get("data", {}).get("serial_number", "")
    if target_serial in sn:
        matches.append({"serial": sn, "instance_code": code, "data": data})
```

**Performance:** ~134 instances takes ~70s (0.5s each). Use `execute_code` for the loop so it runs as one tool call.

### Step 3 — Extract form fields for comparison

`data.form` is a JSON string → parse with `json.loads`. Key widgets for "Đề nghị thanh toán":

| Widget name | Type | Notes |
|---|---|---|
| `Nội dung thanh toán` | textarea | Main description |
| `Người nhận tiền` | input | Payee name |
| `Số tài khoản` | input | Bank account |
| `Ngày thanh toán` | date | ISO date string |
| `Chi tiết` | fieldList | Repeated rows, each with: Nội dung, Đơn vị, Số lượng, Đơn giá, Thành tiền, Ngày, Hóa đơn |
| `Tệp đính kèm` | attachmentV2 | Array of signed URLs |

### Duplicate detection heuristics

When comparing approvals for duplicates, check these dimensions:
1. **Same amount** (`Thành tiền` in detail rows) — strongest signal
2. **Same payee** (`Người nhận tiền`) + **same bank account** (`Số tài khoản`)
3. **Overlapping date ranges** — check both `Ngày thanh toán` and date ranges in `Nội dung thanh toán` / detail `Ngày`
4. **Same content keywords** — especially project name + team name
5. **Multiple approvals on same day** with same amount = likely duplicate draft

Typical pattern: user submits a draft, then submits again with a more detailed description (e.g., adding "từ DD/MM đến hết DD/MM"). The earlier one stays PENDING while the later one gets APPROVED.

## API limitations

- `GET /open-apis/approval/v4/instances` (list all) does NOT support user access token (error 99991668). Only `instances initiated` and `tasks query` work with user identity.
- `approval tasks query` requires `topic` parameter: `"1"` = pending (待办), `"2"` = already processed (已办).
- `tasks query` does NOT return `serial_number` — only `instance_code` + `summaries`. To find by serial, you must iterate `instances get`.
- Paginate with `page_token` if more than 50 results; use `--page-all` if supported.
- The `initiated` list may only return the logged-in user's approvals, not all approvals in the tenant.
