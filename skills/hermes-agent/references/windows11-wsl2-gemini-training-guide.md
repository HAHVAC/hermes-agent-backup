# Windows 11 + WSL2 + Google Gemini training guide notes

Session learning from creating a Vietnamese `.docx` training manual for Hermes Agent installation.

## Recommended training-manual scope

For a Windows 11 internal training guide using the stable path, cover:

1. Open Windows Terminal / PowerShell as Administrator.
2. Install WSL2 Ubuntu:
   ```powershell
   wsl --install -d Ubuntu
   wsl -l -v
   ```
3. Create Ubuntu user/password, then update packages:
   ```bash
   sudo apt update && sudo apt upgrade -y
   sudo apt install -y curl git build-essential ca-certificates unzip
   ```
4. Install Hermes inside Ubuntu WSL2:
   ```bash
   curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
   source ~/.bashrc
   hermes --version
   hermes doctor
   ```
5. Create Google Gemini API key at `https://aistudio.google.com/app/apikey`.
6. Configure model through the wizard first:
   ```bash
   hermes setup
   hermes model
   ```
   If manual env setup is needed, use `hermes config env-path` and set `GOOGLE_API_KEY` or `GEMINI_API_KEY`.
7. Verify CLI before adding gateway/features:
   ```bash
   hermes chat -q "Xin chào, hãy trả lời ngắn gọn bằng tiếng Việt: Hermes đã hoạt động chưa?"
   hermes config
   hermes status --all
   hermes doctor
   ```
8. For practical use, configure tools/memory/TTS/security:
   ```bash
   hermes tools
   hermes config set memory.memory_enabled true
   hermes config set memory.user_profile_enabled true
   hermes config set tts.provider edge
   hermes config set tts.edge.voice vi-VN-NamMinhNeural
   hermes config set approvals.mode smart
   hermes config set security.redact_secrets true
   ```
9. Gateway level-3 flow: run `hermes gateway setup`, test foreground with `hermes gateway run`, set `/sethome` from the chat, then install/start/status.
   ```bash
   hermes gateway install
   hermes gateway start
   hermes gateway status
   ```
10. If WSL service dies when terminal closes, enable systemd:
    ```bash
    sudo tee /etc/wsl.conf >/dev/null <<EOF
    [boot]
    systemd=true
    EOF
    ```
    Then from Windows PowerShell:
    ```powershell
    wsl --shutdown
    ```
11. Add a cron test only after CLI and gateway are working:
    ```bash
    hermes cron list
    hermes cron status
    hermes cron create "every 1h"
    ```

## Training-manual emphasis

- For Windows users, WSL2 Ubuntu remains the more battle-tested path than native Windows.
- Always verify plain CLI chat before gateway/cron/tools.
- For Google Gemini, prefer wizard-based provider/model selection because provider/model names can change between Hermes releases.
- Never include real Gemini API keys, bot tokens, or Slack tokens in the `.docx`.
- Include a final checklist and troubleshooting table; this makes the guide usable for non-developer staff.
