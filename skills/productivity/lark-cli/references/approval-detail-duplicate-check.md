# Checking Approval Details for Duplicates & Verifying Amounts

When the user asks to review an approval's line items for duplicates or errors, use this workflow.

## Step 1 — Fetch the approval instance

Follow `references/approval-lookup-workflow.md` to find the `instance_code` by `serial_number`, then call `approval instances get`.

## Step 2 — Parse the fieldList ("Chi tiết") rows

`data.form` is a JSON string → `json.loads`. Find the widget with `"type": "fieldList"`. Each entry in its `"value"` array is a detail row with keys like: `Nội dung`, `Đơn vị`, `Số lượng`, `Đơn giá`, `Thành tiền`, `Ngày`, `Hóa đơn`, `Ghi chú`.

### Verification checks

1. **Qty × Price = Total**: For every row, check `Số lượng × Đơn giá == Thành tiền`. Report any mismatches.
2. **Duplicate names**: Group rows by normalized name (`.strip().lower()`). Flag groups with ≥2 entries.
3. **Classify duplicates**:
   - **Same name, same amount, same person** → high likelihood of accidental duplicate entry.
   - **Same name, different amounts** → likely different purchases, just same description (e.g. "mua dầu" at different quantities/prices). Still worth flagging but lower concern.

## Step 3 — Download & analyze the xlsx attachment (if present)

The approval often has an `.xlsx` attachment with richer data than the form's fieldList. The xlsx has proper column headers, real dates (not all the same), an explicit **Hóa đơn** column (E), and a **Ghi chú** column (G).

```python
import subprocess, json, os
env = os.environ.copy()
env["PATH"] = "/root/.nvm/versions/node/v24.13.0/bin:" + env.get("PATH", "")

# Get the attachment URLs from the form's "Tệp đính kèm" widget
# Download the .xlsx URL
import requests
r = requests.get(xlsx_url, timeout=30)
with open("/tmp/approval.xlsx", "wb") as f:
    f.write(r.content)
```

Then read with openpyxl (use system Python if venv has numpy issues):

```bash
/usr/bin/python3 -c "
import openpyxl
wb = openpyxl.load_workbook('/tmp/approval.xlsx', data_only=True, read_only=True)
ws = wb[wb.sheetnames[0]]
for row in ws.iter_rows(min_row=10, max_row=68, min_col=1, max_col=7, values_only=True):
    a,b,c,d,e,f,g = (list(row) + [None]*7)[:7]
    # process...
"
```

### Key xlsx columns (row 8 = header, data starts row 10)

| Col | Header | Content |
|-----|--------|---------|
| A | Stt | Sequence number |
| B | Nội dung chuyển tiền | Description |
| C | Ngày tháng | Actual date (datetime) — **more granular than form** |
| D | Số tiền (VNĐ) | Amount |
| E | Hóa đơn | Invoice reference — **form may not have this** |
| F | Người đề xuất | Requester |
| G | Ghi chú | Notes — may contain "Mua ngoài không có hóa đơn" etc. |

The xlsx dates are the **real purchase dates** (each different), while the form's `Ngày` field may all show the same submission date. This distinction is critical for determining whether same-name items are truly duplicates or separate purchases on different days.

## Step 4 — Cross-reference findings

Compare form fieldList data with xlsx data:
- If the xlsx shows **different dates** for items with the same name/amount → they are separate purchases, not duplicates.
- If the xlsx shows **same date, same amount, same description** → likely a genuine duplicate entry error.
- Check the **Hóa đơn column** (E) in xlsx: items marked "Mua ngoài không có hóa đơn" in Ghi chú (G) or with empty E column have no invoice — flag for the user.
