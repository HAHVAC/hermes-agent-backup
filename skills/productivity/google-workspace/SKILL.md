---
name: google-workspace
description: Gmail, Calendar, Drive, Contacts, Sheets, and Docs integration for Hermes. Uses Hermes-managed OAuth2 setup, prefers the Google Workspace CLI (`gws`) when available for broader API coverage, and falls back to the Python client libraries otherwise.
version: 1.0.0
author: Nous Research
license: MIT
metadata:
  hermes:
    tags: [Google, Gmail, Calendar, Drive, Sheets, Docs, Contacts, Email, OAuth]
    homepage: https://github.com/NousResearch/hermes-agent
    related_skills: [himalaya]
---

# Google Workspace

Gmail, Calendar, Drive, Contacts, Sheets, and Docs — through Hermes-managed OAuth and a thin CLI wrapper. When `gws` is installed, the skill uses it as the execution backend for broader Google Workspace coverage; otherwise it falls back to the bundled Python client implementation.

## Google Sheets & IMPORTRANGE Troubleshooting / Common Formula Pitfalls

When users report formula errors (e.g. `#REF!`, `#VALUE!`, `#DIV/0!`, `#NAME?`, `#ERROR!`) in spreadsheets that read/write via the Sheets API, analyze the formula patterns for the following issues:

### 1. IMPORTRANGE Permission Linkage (`#REF!`)
- **Symptom**: On the user's browser, a cell containing `IMPORTRANGE` displays a `#REF!` error.
- **Cause**: Google Sheets requires explicit user confirmation to connect a target spreadsheet to a source spreadsheet, even if the user has access to both.
- **Fix**: The user must hover over or click the cell in a web browser and click the **"Allow access"** (Cho phép truy cập) button. The API cannot bypass this visual gate on a newly duplicated or connected sheet.

### 2. Logic Failures with `SEARCH` in `FILTER` (`#VALUE!`)
- **Symptom**: Using `SEARCH` inside a `FILTER` expression (e.g., `=FILTER(IMPORTRANGE(...); SEARCH("value"; IMPORTRANGE(...)))`) causes the entire range to show `#VALUE!` or sập.
- **Cause**: In Google Sheets, `SEARCH` returns a number when a substring is found, but returns a `#VALUE!` error if the substring is **not** found. A single `#VALUE!` error in the criteria array of `FILTER` breaks the entire filter function.
- **Fix**: Wrap `SEARCH` inside `ISNUMBER(...)` to coerce matches to `TRUE` and non-matches to `FALSE` (instead of error). Alternatively, use `REGEXMATCH(...)` which naturally returns boolean values without throwing errors on missing substrings.

*   *Standard fix:* `=FILTER(IMPORTRANGE(...); ISNUMBER(SEARCH("value"; IMPORTRANGE(...))))`
*   *Optimal fix:* `=FILTER(IMPORTRANGE(...); REGEXMATCH(IMPORTRANGE(...); "value"))`

### 3. IMPORTRANGE Size Limits & Lỗi `#ERROR!` (Result too large)
- **Symptom**: An `IMPORTRANGE` formula returns `#ERROR!` with the tooltip "Result too large" or fails due to size limit.
- **Cause**: Google Sheets has a payload limit of 10MB or ~175,000 cells per individual `IMPORTRANGE` call. Spanning too many columns/rows (e.g. `A1:AJ` over 4,500+ rows) triggers this.
- **Fix**: 
    1. **Vertical Splitting**: Divide the fetch range by rows using an array formula `{}` to stack results. E.g., `={IMPORTRANGE("id"; "Sheet!A1:AJ2500"); IMPORTRANGE("id"; "Sheet!A2501:AJ")}`. (Note: standard locales use `;` to stack vertically, while some European/Vietnamese locales with `;` as formula delimiter may require `\` or `,` for horizontal merging if stacking columns).
    2. **Column Pruning**: Reduce the columns requested if not all are needed (e.g., from `A:AJ` to `A:Z`).

### 4. FILTER Mismatched Range Sizes (`#N/A` or `#VALUE!`)
- **Symptom**: `FILTER` returns an error stating that the range sizes do not match, usually when using `IMPORTRANGE` for both the data array and the filter criteria.
- **Cause**: If the source sheet's row count changes, Google Sheets' asynchronous calculation might refresh the data `IMPORTRANGE` and the criteria `IMPORTRANGE` at different times, creating mismatched array heights.
- **Fix**: 
    1. **Single-pass QUERY (Best Practice)**: Instead of `FILTER` with multiple `IMPORTRANGE` calls, pull the entire block once via `QUERY` and filter using `ColX` references. 
       *   *Example:* `=QUERY(IMPORTRANGE("id"; "Data!A1:O"); "select Col1, Col2 where Col15 contains 'K01'")`
    2. **Hard-coded row bounds**: Force the `IMPORTRANGE` sizes to match by specifying fixed row ranges (e.g., `A1:V10000` and `O1:O10000`) so their shapes are guaranteed to be equal.

---

## References

- `references/gmail-search-syntax.md` — Gmail search operators (is:unread, from:, newer_than:, etc.)
- `references/drive-account-and-gws-fallback.md` — Drive download/search fallback when `gdown` fails, exact file ID is inaccessible, or `gws` is broken.

## Scripts

- `scripts/setup.py` — OAuth2 setup (run once to authorize)
- `scripts/google_api.py` — compatibility wrapper CLI. It prefers `gws` for operations when available, while preserving Hermes' existing JSON output contract.

## First-Time Setup

The setup is fully non-interactive — you drive it step by step so it works
on CLI, Telegram, Discord, or any platform.

Define a shorthand first:

```bash
GSETUP="python ${HERMES_HOME:-$HOME/.hermes}/skills/productivity/google-workspace/scripts/setup.py"
```

### Step 0: Check if already set up

```bash
$GSETUP --check
```

If it prints `AUTHENTICATED`, skip to Usage — setup is already done.

### Step 1: Triage — ask the user what they need

Before starting OAuth setup, ask the user TWO questions:

**Question 1: "What Google services do you need? Just email, or also
Calendar/Drive/Sheets/Docs?"**

- **Email only** → They don't need this skill at all. Use the `himalaya` skill
  instead — it works with a Gmail App Password (Settings → Security → App
  Passwords) and takes 2 minutes to set up. No Google Cloud project needed.
  Load the himalaya skill and follow its setup instructions.

- **Email + Calendar** → Continue with this skill, but use
  `--services email,calendar` during auth so the consent screen only asks for
  the scopes they actually need.

- **Calendar/Drive/Sheets/Docs only** → Continue with this skill and use a
  narrower `--services` set like `calendar,drive,sheets,docs`.

- **Full Workspace access** → Continue with this skill and use the default
  `all` service set.

**Question 2: "Does your Google account use Advanced Protection (hardware
security keys required to sign in)? If you're not sure, you probably don't
— it's something you would have explicitly enrolled in."**

- **No / Not sure** → Normal setup. Continue below.
- **Yes** → Their Workspace admin must add the OAuth client ID to the org's
  allowed apps list before Step 4 will work. Let them know upfront.

### Step 2: Create OAuth credentials (one-time, ~5 minutes)

Tell the user:

> You need a Google Cloud OAuth client. This is a one-time setup:
>
> 1. Create or select a project:
>    https://console.cloud.google.com/projectselector2/home/dashboard
> 2. Enable the required APIs from the API Library:
>    https://console.cloud.google.com/apis/library
>    Enable: Gmail API, Google Calendar API, Google Drive API,
>    Google Sheets API, Google Docs API, People API
> 3. Create the OAuth client here:
>    https://console.cloud.google.com/apis/credentials
>    Credentials → Create Credentials → OAuth 2.0 Client ID
> 4. Application type: "Desktop app" → Create
> 5. If the app is still in Testing, add the user's Google account as a test user here:
>    https://console.cloud.google.com/auth/audience
>    Audience → Test users → Add users
> 6. Download the JSON file and tell me the file path
>
> Important Hermes CLI note: if the file path starts with `/`, do NOT send only the bare path as its own message in the CLI, because it can be mistaken for a slash command. Send it in a sentence instead, like:
> `The JSON file path is: /home/user/Downloads/client_secret_....json`

Once they provide the path:

```bash
$GSETUP --client-secret /path/to/client_secret.json
```

If they paste the raw client ID / client secret values instead of a file path,
write a valid Desktop OAuth JSON file for them yourself, save it somewhere
explicit (for example `~/Downloads/hermes-google-client-secret.json`), then run
`--client-secret` against that file.

### Step 3: Get authorization URL

Run:

```bash
$GSETUP --auth-url
```

Current setup script does **not** accept `--services` or `--format`; it prints the OAuth URL directly and saves pending PKCE state locally.

Agent rules for this step:
- Send the printed URL to the user as a single line.
- Tell the user that the browser will likely fail on `http://localhost:1` after approval, and that this is expected.
- Tell them to copy the ENTIRE redirected URL from the browser address bar.
- If the user gets `Error 403: access_denied`, send them directly to `https://console.cloud.google.com/auth/audience` to add themselves as a test user.

### Step 4: Exchange the code

The user will paste back either a URL like `http://localhost:1/?code=4/0A...&scope=...`
or just the code string. Either works. The `--auth-url` step stores a temporary
pending OAuth session locally so `--auth-code` can complete the PKCE exchange
later, even on headless systems:

```bash
$GSETUP --auth-code "THE_URL_OR_CODE_THE_USER_PASTED"
```

If `--auth-code` fails because the code expired, was already used, or came from
an older browser tab, it now returns a fresh `fresh_auth_url`. In that case,
immediately send the new URL to the user and have them retry with the newest
browser redirect only.

### Step 5: Verify

```bash
$GSETUP --check
```

Should print `AUTHENTICATED`. Setup is complete — token refreshes automatically from now on.

### Notes

- Token is stored at `~/.hermes/google_token.json` and auto-refreshes.
- Pending OAuth session state/verifier are stored temporarily at `~/.hermes/google_oauth_pending.json` until exchange completes.
- If `gws` is installed, `google_api.py` points it at the same `~/.hermes/google_token.json` credentials file. Users do not need to run a separate `gws auth login` flow.
- To revoke: `$GSETUP --revoke`

## Usage

All commands go through the API script. Set `GAPI` as a shorthand:

```bash
GAPI="python ${HERMES_HOME:-$HOME/.hermes}/skills/productivity/google-workspace/scripts/google_api.py"
```

### Gmail

```bash
# Search (returns JSON array with id, from, subject, date, snippet)
$GAPI gmail search "is:unread" --max 10
$GAPI gmail search "from:boss@company.com newer_than:1d"
$GAPI gmail search "has:attachment filename:pdf newer_than:7d"

# Read full message (returns JSON with body text)
$GAPI gmail get MESSAGE_ID

# Send
$GAPI gmail send --to user@example.com --subject "Hello" --body "Message text"
$GAPI gmail send --to user@example.com --subject "Report" --body "<h1>Q4</h1><p>Details...</p>" --html
$GAPI gmail send --to user@example.com --subject "Hello" --from '"Research Agent" <user@example.com>' --body "Message text"

# Reply (automatically threads and sets In-Reply-To)
$GAPI gmail reply MESSAGE_ID --body "Thanks, that works for me."
$GAPI gmail reply MESSAGE_ID --from '"Support Bot" <user@example.com>' --body "Thanks"

# Labels
$GAPI gmail labels
$GAPI gmail modify MESSAGE_ID --add-labels LABEL_ID
$GAPI gmail modify MESSAGE_ID --remove-labels UNREAD
```

### Calendar

```bash
# List events (defaults to next 7 days)
$GAPI calendar list
$GAPI calendar list --start 2026-03-01T00:00:00Z --end 2026-03-07T23:59:59Z

# Create event (ISO 8601 with timezone required)
$GAPI calendar create --summary "Team Standup" --start 2026-03-01T10:00:00-06:00 --end 2026-03-01T10:30:00-06:00
$GAPI calendar create --summary "Lunch" --start 2026-03-01T12:00:00Z --end 2026-03-01T13:00:00Z --location "Cafe"
$GAPI calendar create --summary "Review" --start 2026-03-01T14:00:00Z --end 2026-03-01T15:00:00Z --attendees "alice@co.com,bob@co.com"

# Delete event
$GAPI calendar delete EVENT_ID
```

### Drive

```bash
$GAPI drive search "quarterly report" --max 10
$GAPI drive search "mimeType='application/pdf'" --raw-query --max 5
```

OAuth scope note: Drive integration now uses `https://www.googleapis.com/auth/drive.file` so automations can create/upload files they manage. Existing tokens that were authorized with `drive.readonly` must be re-authorized before Drive uploads will work.

⚠️ Drive access pitfall: `drive.file` cannot reliably read arbitrary files shared by link or files the app did not create/open, even if the signed-in user can see them in a browser. `files().get(fileId=...)` may return `404 File not found`. If the user provides a Google Drive public/"Anyone with the link" file URL, prefer direct unauthenticated download first:

```bash
FILE_ID="..."
python3 - <<'PY'
import requests, os
fid=os.environ['FILE_ID']
url=f'https://drive.google.com/uc?export=download&id={fid}'
r=requests.get(url, headers={'User-Agent':'Mozilla/5.0'}, allow_redirects=True, timeout=60)
print(r.status_code, r.headers.get('content-type'), len(r.content), r.url)
open('/tmp/drive_download.bin','wb').write(r.content)
PY
file /tmp/drive_download.bin
```

Only fall back to Drive API when the file is in the app-authorized scope. Do not substitute keyword-search results for the exact requested file ID unless the user explicitly approves; if exact ID is inaccessible, report that and ask for share/public access.

### Contacts

```bash
$GAPI contacts list --max 20
```

### Sheets

```bash
# Read
$GAPI sheets get SHEET_ID "Sheet1!A1:D10"

# If gws is installed but broken/incompatible, bypass it for read-only Sheets access:
python - <<'PY'
import sys, json
sys.path.insert(0, '/root/.hermes/skills/productivity/google-workspace/scripts')
import google_api
svc = google_api.build_service('sheets', 'v4')
res = svc.spreadsheets().values().get(
    spreadsheetId='SHEET_ID',
    range="'Sheet Name'!A:AH",
).execute()
print(json.dumps(res.get('values', []), ensure_ascii=False))
PY

# Write
$GAPI sheets update SHEET_ID "Sheet1!A1:B2" --values '[["Name","Score"],["Alice","95"]]'

# Append rows
$GAPI sheets append SHEET_ID "Sheet1!A:C" --values '[["new","row","data"]]'
```

### Docs

```bash
$GAPI docs get DOC_ID
```

## Output Format

All commands return JSON. Parse with `jq` or read directly. Key fields:

- **Gmail search**: `[{id, threadId, from, to, subject, date, snippet, labels}]`
- **Gmail get**: `{id, threadId, from, to, subject, date, labels, body}`
- **Gmail send/reply**: `{status: "sent", id, threadId}`
- **Calendar list**: `[{id, summary, start, end, location, description, htmlLink}]`
- **Calendar create**: `{status: "created", id, summary, htmlLink}`
- **Drive search**: `[{id, name, mimeType, modifiedTime, webViewLink}]`
- **Contacts list**: `[{name, emails: [...], phones: [...]}]`
- **Sheets get**: `[[cell, cell, ...], ...]`

## Rules

1. **Never send email or create/delete events without confirming with the user first.** Show the draft content and ask for approval.
2. **Check auth before first use** — run `setup.py --check`. If it fails, guide the user through setup.
3. **Use the Gmail search syntax reference** for complex queries — load it with `skill_view("google-workspace", file_path="references/gmail-search-syntax.md")`.
4. **Calendar times must include timezone** — always use ISO 8601 with offset (e.g., `2026-03-01T10:00:00-06:00`) or UTC (`Z`).
5. **Respect rate limits** — avoid rapid-fire sequential API calls. Batch reads when possible.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `NOT_AUTHENTICATED` | Run setup Steps 2-5 above |
| `REFRESH_FAILED` | Token revoked or expired — redo Steps 3-5 |
| `HttpError 403: Insufficient Permission` | Missing API scope — `$GSETUP --revoke` then redo Steps 3-5 |
| `HttpError 403: Access Not Configured` | API not enabled — user needs to enable it in Google Cloud Console |
| `ModuleNotFoundError` | Run `$GSETUP --install-deps` |
| `gws: /lib/.../libc.so.6: version GLIBC_2.39 not found` | Installed `gws` binary is incompatible with host glibc. Bypass `gws` and call Google Python client libraries directly, or set `HERMES_GWS_BIN` to a working binary; `google_api.py` currently exits on broken `gws` instead of falling back. For Sheets reads, import `google_api` and call `build_service('sheets','v4')` directly; see snippet below. |
| Drive link returns sign-in page / `gdown` cannot retrieve public link / Drive API `File not found` | Confirm which Google account owns/has access. On Boss's Hermes instance, Google Workspace/gws OAuth may be `pcccthanglong.tlc@gmail.com` even when the message sender/account label is `hahvac`; do not assume `hahvac@gmail.com` for Drive. Use Python API fallback and, if exact file ID is inaccessible, search Drive by distinctive text or filename. |
| Advanced Protection blocks auth | Workspace admin must allowlist the OAuth client ID |

## Revoking Access

```bash
$GSETUP --revoke
```
