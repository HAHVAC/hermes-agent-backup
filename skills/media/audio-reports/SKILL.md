---
name: audio-reports
description: Create spoken audio summaries/reports for Slack or chat delivery using text-to-speech, with language-specific voices and direct media attachment output.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [audio, text-to-speech, reports, slack, vietnamese]
---

# Audio Reports

Use this skill when the user asks for a report, summary, briefing, or explanation as an audio file/voice note, especially for Slack delivery.

## What to do

1. **Prepare a spoken script, not a written report.**
   - Use natural spoken language.
   - Expand symbols and code-ish names so TTS reads well.
   - Keep URLs/commands minimal unless explicitly needed.

2. **Match both text language and TTS voice locale.**
   - Do not assume Vietnamese text will be spoken with a Vietnamese voice.
   - For Vietnamese audio, explicitly use a Vietnamese voice such as:
     - `vi-VN-HoaiMyNeural` (female)
     - `vi-VN-NamMinhNeural` (male)
   - If using a generic `text_to_speech` tool, verify it supports/selected the desired locale; if not, use `edge-tts` directly.

3. **Create a Slack-openable media file.**
   - Prefer `.mp3` for broad client compatibility.
   - `.ogg` voice-note style may work, but if the user complains about opening/playback, regenerate as `.mp3`.
   - Return the file with `MEDIA:/absolute/path/to/file` so Slack uploads it as an attachment.

4. **If the user says the language/voice is wrong, regenerate immediately.**
   - Apologize briefly.
   - State the concrete fix: explicit locale voice selected.
   - Do not re-explain the whole report in text unless asked.

## Known-good Vietnamese command

```bash
edge-tts \
  --voice vi-VN-HoaiMyNeural \
  --text "<Vietnamese spoken script>" \
  --write-media /root/.hermes/audio_cache/report_vi.mp3
```

Then reply:

```text
MEDIA:/root/.hermes/audio_cache/report_vi.mp3
```

## Pitfalls

- **Vietnamese text with English voice is still wrong.** The user may describe this as “ngôn ngữ vẫn là tiếng Anh”. Regenerate using `vi-VN-*` voice explicitly.
- **TTS reads English technical names awkwardly.** For spoken Vietnamese, rewrite names phonetically where useful, e.g. “mattpocock slash skills”, “context chấm em đi”, or explain once in Vietnamese.
- **Slack direct playback matters.** Use `MEDIA:` with an absolute path; do not only mention the path.
- **Avoid overlong audio.** For executive briefings, aim 2–5 minutes unless the user asks for full detail.

## Verification

- Confirm the output file exists and is non-empty if using shell commands.
- If available, list voices with:

```bash
edge-tts --list-voices | grep 'vi-VN'
```
