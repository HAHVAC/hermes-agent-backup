import json
import subprocess
import sys

BASE = 'QPzQbdDZLasm2vsqeFql0RPsgyg'
MASTER_TABLE = 'tblBCgxj19VHYKFE'
SUBMISSION_TABLE = 'tblMMHFizWL8q0a5'
SUBMISSION_NAME_FIELD_ID = 'fldHv7gAJC'
SUBMISSION_DATES_FIELD_ID = 'fldvJwefHq'
DATE_FIELDS = ['26/4', '27/4', '30/4', '1/5', '2/5', '3/5']


def run(cmd):
    proc = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    if proc.returncode != 0:
        raise RuntimeError(proc.stdout + proc.stderr)
    return json.loads(proc.stdout)


def main():
    master = run(f"lark-cli base +record-list --as user --base-token {BASE} --table-id {MASTER_TABLE} --limit 200")
    submissions = run(f"lark-cli base +record-list --as user --base-token {BASE} --table-id {SUBMISSION_TABLE} --limit 200")

    master_fields = master['data']['fields']
    master_records = {}
    for rid, row in zip(master['data']['record_id_list'], master['data']['data']):
        rowmap = dict(zip(master_fields, row))
        name_list = rowmap.get('Họ và tên')
        if isinstance(name_list, list) and name_list:
            master_records[name_list[0]] = {'record_id': rid, 'row': rowmap}

    sub_fields = submissions['data']['field_id_list']
    latest_by_name = {}
    for row in submissions['data']['data']:
        rowmap = dict(zip(sub_fields, row))
        name_list = rowmap.get(SUBMISSION_NAME_FIELD_ID)
        if isinstance(name_list, list) and name_list:
            latest_by_name[name_list[0]] = list(rowmap.get(SUBMISSION_DATES_FIELD_ID) or [])

    updated = []
    skipped = []
    for name, selected_dates in latest_by_name.items():
        if name not in master_records:
            skipped.append(name)
            continue
        current = master_records[name]['row']
        patch = {}
        changed = False
        for d in DATE_FIELDS:
            target = d in selected_dates
            if current.get(d) is not target:
                patch[d] = target
                changed = True
        if changed:
            payload = json.dumps(patch, ensure_ascii=False)
            rid = master_records[name]['record_id']
            run(f"lark-cli base +record-upsert --as user --base-token {BASE} --table-id {MASTER_TABLE} --record-id {rid} --json {json.dumps(payload, ensure_ascii=False)}")
            updated.append(name)

    print(json.dumps({
        'updated_count': len(updated),
        'updated_names': updated,
        'skipped_missing_master': skipped,
        'submission_records_seen': len(submissions['data']['record_id_list'])
    }, ensure_ascii=False))


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(json.dumps({'error': str(e)}, ensure_ascii=False))
        sys.exit(1)
