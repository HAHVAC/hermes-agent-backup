---
name: anygen-skills-install
description: Install and configure the complete AnyGen skill suite for Hermes / OpenClaw agent. Install all 9 AnyGen generation skills in one go.
---

# AnyGen Skills Installation Skill

This skill installs, configures and authenticates the complete AnyGen AI skill suite for Hermes Agent.

## Steps

1.  Clone the official repository into Hermes skills directory:
    ```bash
    mkdir -p ~/.hermes/skills/ && rm -rf ~/.hermes/skills/anygen
    git clone https://github.com/AnyGenIO/anygen-skills.git ~/.hermes/skills/anygen
    ```

2.  Install AnyGen global CLI:
    ```bash
    npm install -g @anygen/cli
    ```

3.  Authenticate:
    ```bash
    anygen auth login --no-wait
    ```
    Send the generated auth URL to the user to complete browser login via Google.
    No manual API key copy is needed when using this flow.

4.  Verify installation:
    ```bash
    anygen --version
    ```

## Installed skills:
- slide-generator
- doc-generator
- diagram-generator
- data-analysis
- deep-research
- financial-research
- image-generator
- storybook-generator
- website-generator

## Notes
✅ All skills become automatically available to Hermes after restart
✅ Uses server-side generation at anygen.io
✅ Works on headless VPS environments
