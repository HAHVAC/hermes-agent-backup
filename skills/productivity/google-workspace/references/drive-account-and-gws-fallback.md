# Drive account and gws fallback notes

Use this when a Google Drive URL cannot be downloaded with `gdown` or direct API lookup returns `File not found`.

## Symptoms

- `gdown` says it cannot retrieve the public link.
- Direct browser/download URL redirects to Google sign-in.
- Drive API `files().get(fileId=...)` returns 404 `File not found` even though the user can see the link.
- `gws` CLI may fail on this host with `GLIBC_2.39 not found`.

## Working approach

1. Do not assume the Slack/Gmail label equals the OAuth account. For Boss's Hermes, the Google Workspace token used by gws/Google API can be `pcccthanglong.tlc@gmail.com`.
2. Bypass broken `gws` by importing the skill's Python API wrapper:

```python
import sys
sys.path.insert(0, '/root/.hermes/skills/productivity/google-workspace/scripts')
import google_api
svc = google_api.build_service('drive', 'v3')
```

3. Try exact metadata/download:

```python
meta = svc.files().get(fileId=file_id, fields='id,name,mimeType,size', supportsAllDrives=True).execute()
```

4. If exact ID fails but user insists the account should have access, search by distinctive text/filename:

```python
res = svc.files().list(
    q="fullText contains 'nghiệm thu phòng cháy' and fullText contains 'thanh toán'",
    fields='files(id,name,mimeType,webViewLink,owners(emailAddress),modifiedTime,size)',
    pageSize=20,
    supportsAllDrives=True,
    includeItemsFromAllDrives=True,
).execute()
```

5. Download candidates with `MediaIoBaseDownload` for binary Office/PDF files.

## Pitfalls

- `drive.file` OAuth scope may only expose files the app created/opened, so broad Drive search can be incomplete. If ID lookup and text search fail, ask the user to share the file explicitly with the OAuth account or make it link-viewable.
- Google Drive `fullText` search may find related/duplicate files but not the exact linked ID. Report the file name, owner, and ID you actually read.
