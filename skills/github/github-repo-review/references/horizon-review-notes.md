# Horizon (Thysrael/Horizon) — Review Notes

**Date:** 2026-05-31
**Repo:** https://github.com/Thysrael/Horizon
**Verdict:** Safe to use, well-structured project

## What It Does
AI-powered news radar — self-hosted aggregator that fetches from HN, RSS, Reddit, Telegram, Twitter/X, GitHub, OpenBB → deduplicates → AI scores 0-10 → enriches with web context → generates bilingual (EN/CN) daily briefings → delivers via GitHub Pages, email, webhooks (Feishu/Lark, Slack, Discord), or MCP server.

## Key Security Findings

### Safe Patterns
- Telegram scraper uses **public web preview** (`t.me/s/{channel}`) parsed with BeautifulSoup — no Telegram Bot Token or API account needed. Very safe approach.
- Webhook service has built-in **sensitive header masking** (regex on authorization/token/secret/key/password headers) before logging.
- All API keys read from env vars via `config.api_key_env`, never hardcoded.
- AI client factory pattern supports multiple providers cleanly (Anthropic, OpenAI, Gemini, Azure, DeepSeek, Ollama, etc.).
- Docker uses `python:3.11-slim`, no root-user issues in compose.
- Proper SECURITY.md with responsible disclosure policy.

### Risks to Note
1. **GitHub Pages public by default** — if user configures private/internal sources, summaries become publicly accessible. Mitigation: disable GitHub Pages delivery, use webhook-to-Lark only.
2. **Indirect Prompt Injection** — content from scraped articles is fed directly into LLM prompts for scoring. A malicious article could contain hidden instructions. Impact: minimal (only affects scoring/summary quality, not system security).
3. **API cost** — no built-in budget caps; every item scored by LLM. Mitigation: set provider-level budget caps, configure strict source filtering before AI scoring.
4. **SMTP/IMAP for newsletter** — requires email credentials. Mitigation: use a dedicated email account, not primary business email.

## Tech Stack
- Python 3.11+, managed with `uv`
- httpx (async HTTP), feedparser, beautifulsoup4
- anthropic, openai, google-genai SDKs
- pydantic for models, mcp for Model Context Protocol server
- hatchling build system
- Docker + docker-compose

## Code Quality
- Clean modular architecture: scrapers/, ai/, services/, setup/, storage/, mcp/
- Each scraper is a separate class inheriting from BaseScraper
- Orchestrator pattern with clear pipeline stages
- Well-documented README (EN + CN), configuration guide, scoring guide
