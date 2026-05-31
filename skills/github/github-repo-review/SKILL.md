---
name: github-repo-review
description: "Review an external GitHub repository: what it does, code quality, security posture, and suitability for adoption. Use when user asks to 'check this repo', 'review this project', 'is this repo safe', 'what does this project do', or shares a GitHub URL wanting analysis."
tags: [github, security-review, code-review, repo-analysis]
related_skills: [github-code-review, codebase-inspection]
---

# GitHub Repository Review

Analyze an external GitHub repository for purpose, architecture, code quality, security posture, and adoption suitability — without cloning it.

## When to Use

- User shares a GitHub URL and asks what it does
- User asks if a repo/library/tool is safe to use
- User wants to evaluate adopting an open-source project
- User asks to "check" or "review" a GitHub repo

## Review Pipeline

### Step 1: README & Metadata
```
web_extract → README.md (both rendered page and raw)
```
Capture: purpose, features, stars/forks, license, language breakdown, author profile.

### Step 2: File Tree
```
web_extract → https://api.github.com/repos/{owner}/{repo}/git/trees/main?recursive=1
```
Identify: entry points, core modules, config files, CI/CD workflows, test coverage, dependency manifests.

### Step 3: Key Source Files (read raw via raw.githubusercontent.com)
Priority order — read as many as relevant:
1. **Dependency manifest**: `pyproject.toml`, `package.json`, `Cargo.toml`, `go.mod` — check dependency count, known-vulnerable packages, unusual dependencies.
2. **Entry points**: `main.py`, `src/main.*`, `index.*` — check for obfuscation, data exfiltration, hardcoded secrets.
3. **Network code**: any file making HTTP requests — check what data is sent where.
4. **Security-sensitive**: `Dockerfile`, `docker-compose.yml`, CI workflows — check for privilege escalation, exposed secrets, unsafe defaults.
5. **Config handling**: `.env.example`, config templates — check how secrets are managed.
6. **SECURITY.md**: vulnerability reporting policy.

### Step 4: Author & Community Signals
- GitHub profile of maintainer (activity, other repos)
- Issue/PR responsiveness
- Release frequency and versioning discipline
- SECURITY.md or security policy presence

### Step 5: Synthesize Report (in Vietnamese for Anh)

Structure the report as:

```
## 1. Repo này dùng để làm gì?
(2-5 bullet points, plain language)

## 2. Kiến trúc & Cấu trúc code
(Module breakdown, key files, tech stack)

## 3. Đánh giá an toàn (Security)
### ✅ Điểm an toàn
### ⚠️ Rủi ro cần lưu ý
(For each risk: what it is, impact level, mitigation)

## 4. Khuyến nghị
(Should they use it? How to deploy safely? Next steps?)
```

## Key Security Checks

### Red Flags 🚩
- Obfuscated code, eval/exec on network data
- Hardcoded API keys, tokens, or credentials
- Dependencies from suspicious/unmaintained sources
- Data sent to unexpected external servers
- postinstall scripts that download binaries
- Docker running as root without need
- CI workflows with `pull_request_target` + checkout

### Green Flags ✅
- Clean dependency list with well-known packages
- Secrets via environment variables only
- Proper Dockerfile (non-root user, slim base)
- Active maintainer, responsive to issues
- Test suite present
- Security policy (SECURITY.md)
- License clearly stated

## Tool Usage Pattern

```
# README (rendered page for description, raw for full content)
web_extract(["https://github.com/{owner}/{repo}", "https://raw.githubusercontent.com/{owner}/{repo}/main/README.md"])

# File tree
web_extract(["https://api.github.com/repos/{owner}/{repo}/git/trees/main?recursive=1"])

# Source files (raw)
web_extract(["https://raw.githubusercontent.com/{owner}/{repo}/main/{path}"])

# Web search for security issues
web_search("{repo-name} security vulnerability")
```

## Pitfalls

1. **Branch may not be `main`**: Some repos use `master`. Check the default branch from the API response.
2. **Raw URLs return 404 for large files**: For files over ~1MB, use the GitHub web page instead.
3. **web_extract truncates large pages**: The tree API response for very large repos may be truncated. Check the `truncated` field.
4. **Don't clone just to review**: All analysis can be done via raw URLs and API. Save disk and time.
5. **Check for mirrors/forks**: The real upstream may be a different org. Look for "forked from" indicators.

## References

- `references/horizon-review-notes.md` — Concrete review example: Horizon news radar (security findings, safe patterns, risk analysis)
