# Lark Approval detail-line amount → Base number field

Use this when a Base record was synced from Lark Approval and needs the total of a repeated detail field (e.g. `Chi tiết -> Thành tiền`) written back to a Base number/currency field by `Request No.`.

## Working pattern

1. Read Base records with minimal projection and JSON output:

```bash
lark-cli base +record-list --as user \
  --base-token <base_token> --table-id <table_id> --limit 200 --format json \
  --field-id 'Request No.' --field-id 'SourceID' --field-id 'Số tiền thanh toán'
```

2. Decode `SourceID` to get the Approval `instance_code`:

```python
import base64
instance_code = base64.b64decode(source_id).decode().split(':')[1]
```

Observed shape: `<tenant_or_definition_id>:<INSTANCE_CODE>:<hash>:<version>`.

3. Fetch each Approval instance:

```bash
lark-cli approval instances get --as user \
  --params '{"instance_code":"<INSTANCE_CODE>","locale":"vi-VN","user_id_type":"open_id"}' \
  --format json
```

4. Parse `data.form` as JSON string. Find the item named `Chi tiết`; its `value` is a list of detail rows. For each row, find cell `name == "Thành tiền"` and sum numeric `value`.

5. Update Base one record at a time (different amount per record, so `+record-batch-update` is not appropriate because it applies one shared patch):

```bash
lark-cli base +record-upsert --as user \
  --base-token <base_token> --table-id <table_id> --record-id <record_id> \
  --json '{"Số tiền thanh toán":25266950}'
```

## Safety / verification

- Save a local extraction/update plan before writing, including `record_id`, `request_no`, old amount, new amount, `instance_code`, and detail row count.
- Do a `--dry-run` on one update to verify the PATCH URL/body.
- Write serially with ~0.5–1s delay between updates to avoid write conflicts.
- Verify by reading `Request No.` + target number field again and comparing all records to the extracted totals.

## Pitfalls

- `lark-cli base +record-list --format json` may return row-oriented data under `data.data`, with `data.fields` and `data.record_id_list`; do not assume `data.records`.
- `Request No.` may be rendered as Markdown link text; extract the bracket text (`[202605190001](...) -> 202605190001`) for matching/reporting.
- The Approval `form` field is itself a JSON-encoded string, not a parsed object.
- Number/currency Base fields should be written as JSON numbers, not strings with commas or `VND`.
- Use `--as user` for both Approval and Base resources; bot identity may not see personal/resource-scoped data or may fail writes.
