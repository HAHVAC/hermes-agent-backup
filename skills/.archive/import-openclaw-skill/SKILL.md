---
name: import-openclaw-skill
description: "Import official OpenClaw skills from anthropics/skills GitHub repository into Hermes Agent. Handles directory copying, path patching, dependency installation, and verification."
---

# When to use
When importing any official skill from https://github.com/anthropics/skills repository into Hermes Agent. This covers all 17 core official skills: docx, xlsx, pptx, pdf, etc.

# Standard import workflow

1. **Clone the official repo (sparse checkout)**
```bash
cd /tmp && rm -rf openclaw-skill-repo
mkdir openclaw-skill-repo && cd openclaw-skill-repo
git init
git remote add origin https://github.com/anthropics/skills.git
git config core.sparseCheckout true
echo "skills/${SKILL_NAME}/*" >> .git/info/sparse-checkout
git pull origin main --depth 1
```

2. **Copy full skill directory**
```bash
rm -rf ~/.hermes/skills/${SKILL_NAME}
cp -r /tmp/openclaw-skill-repo/skills/${SKILL_NAME} ~/.hermes/skills/${SKILL_NAME}
```

3. **Patch relative script paths (CRITICAL)**
All OpenClaw skills use relative `scripts/` paths. Replace **ALL** occurrences in SKILL.md:
- Find: `python scripts/`
- Replace: `python3 ~/.hermes/skills/${SKILL_NAME}/scripts/`

Also add this note at the top of Requirements section:
> **Hermes note**: Scripts are located at full path `~/.hermes/skills/${SKILL_NAME}/scripts/`. Always use absolute paths when calling scripts from this skill.

4. **Install required dependencies**
Check skill docs for required system packages:
- `xlsx`, `docx`, `pptx`, `pdf` require: `libreoffice`, `openpyxl`, `python-docx`, `python-pptx`, `pymupdf`

5. **Verify skill loads correctly**
```
skill_view(name="${SKILL_NAME}")
```
Confirm no missing files, readiness_status = available.

6. **Test the recalc/validate script**
Run the main utility script with --help to confirm it works.

## Common pitfalls
- ❌ Do not just copy SKILL.md alone — always copy the entire skill directory including all subfolders and scripts
- ❌ Do not leave relative script paths — they will fail when executed from other working directories
- ✅ Always use sparse checkout instead of full 1GB repo clone
