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

1. **Respect the requested mode before rewriting.**
   - If the user asks for verbatim TTS, preserve the pasted content as-is except for harmless part markers when splitting long audio.
   - If the user asks for a summary/briefing, prepare a spoken script, not a written report.
   - Use natural spoken language for summaries.
   - Expand symbols and code-ish names so TTS reads well.
   - Keep URLs/commands minimal unless explicitly needed.

2. **For Telegram auto-TTS from pasted articles/Facebook posts.**
   - If the user has configured a group/chat for auto-TTS, treat pasted long-form text as the trigger; do not ask again unless intent is ambiguous.
   - Boss's preferred mode for the Telegram group “Hermes Text To Speech”: lightly edit pasted Facebook/article/doc content for smoother spoken delivery without changing meaning beyond ~5%, split long content into multiple audio files, and use `vi-VN-NamMinhNeural` by default.
   - If Boss explicitly asks for verbatim/full original reading, preserve the original text as-is except for harmless section markers and TTS-friendly pronunciation fixes.
   - For content the user explicitly marks as not for reading, e.g. starts with “Không đọc:”, skip TTS.
   - Split on natural section boundaries and add only a short spoken marker such as “Phần 1 trong 3” so the user can follow multi-part audio. For long Vietnamese posts, 2–4 parts is often better than one very long audio file.

3. **Match both text language and TTS voice locale.**
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
- **Edge-TTS Vietnamese Voice Connection Issues & Workarounds:**
  When converting large texts in Vietnamese via `edge-tts` (or using the `vi-VN-NamMinhNeural`/`vi-VN-HoaiMyNeural` voices), Microsoft Edge TTS servers often throttle connections or return `TimeoutError` / `NoAudioReceived` for blocks exceeding a few hundred characters. 
  - *Workaround:* Clean all special characters (dashes, quotes, parentheses) first, replacing them with simple commas or spaces.
  - *Fallback:* If TimeoutErrors persist, split the text into micro-chunks (sentences/phrases under 100 characters or ~15 words) before sending to `edge-tts`. In case of repeated failures, fall back to OpenAI TTS API (e.g. `alloy`, `onyx` voices) or other configured local Vietnamese TTS APIs.
- **TTS reads English technical names awkwardly.** For spoken Vietnamese, rewrite names phonetically where useful, e.g. “mattpocock slash skills”, “context chấm em đi”, or explain once in Vietnamese.
- **Slack direct playback matters.** Use `MEDIA:` with an absolute path; do not only mention the path.
- **Avoid overlong audio.** For executive briefings, aim 2–5 minutes unless the user asks for full detail.

## Verification

- Confirm the output file exists and is non-empty if using shell commands.
- For Telegram, prefer returning each generated file as its own `MEDIA:/absolute/path` line; `.ogg` is acceptable for voice/audio delivery, while `.mp3` is safer if the user reports playback issues.
- If available, list voices with:

```bash
edge-tts --list-voices | grep 'vi-VN'
```
