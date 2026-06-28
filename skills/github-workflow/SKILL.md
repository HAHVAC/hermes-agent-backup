---
name: github-workflow
description: Complete GitHub operations and review workflow (auth, codebase inspection, repo setup, PR lifecycle, code reviews, and issue triage) using the gh CLI or git API curl fallbacks.
category: github
---

# GitHub Workflows & Repository Management

An all-in-one class-level skill for authentication, codebase inspection, repository setup, pull request lifecycles, automated testing/CI tracking, and structured issue triage.

## Table of Contents
1. [Authentication Setup (`github-auth`)](#1-authentication-setup)
2. [Codebase Inspection (`codebase-inspection`)](#2-codebase-inspection)
3. [Repository Management (`github-repo-management`)](#3-repository-management)
4. [Pull Request Lifecycle (`github-pr-workflow`)](#4-pull-request-lifecycle)
5. [Code Reviews (`github-code-review`)](#5-code-reviews)
6. [Repository & Codebase Architecture Reviews (`github-repo-review`)](#6-repository--codebase-architecture-reviews)
7. [Issue Management (`github-issues`)](#7-issue-management)

---

## 1. Authentication Setup

### HTTPS Token Configuration
Verify authentication or set up fallback:
```bash
if command -v gh &>/dev/null && gh auth status &>/dev/null; then
  echo "gh CLI authenticated."
else
  echo "Using GITHUB_TOKEN environment variable or credential helper."
fi
```
To configure git credential helper with a token:
```bash
git config --global credential.helper store
echo "https://USERNAME:YOUR_TOKEN@github.com" > ~/.git-credentials
```

For SSH configuration, add your key to agent and verify:
```bash
ssh -T git@github.com
```

Refer to `references/github-auth.md` for local key rotation, troubleshooting SSH, and scope requirements.

---

## 2. Codebase Inspection

Before modifying a new project, analyze its structure, languages, and volume to plan scope:
- Use `pygount` or similar directory scans.
- Run language distribution checks:
```bash
pygount --format=summary .
```
Identify lines of code (LOC), comments-to-code ratios, and potential layout anomalies.
Detailed guidelines on files and structures to inspect can be found in `references/codebase-inspection.md`.

---

## 3. Repository Management

Common commands for setting up, cloning, or managing repositories:
```bash
# Clone with submodules
git clone --recurse-submodules https://github.com/owner/repo.git

# Create a repo under an organization or user space
gh repo create owner/new-repo --public --confirm

# List remotes
git remote -v
```
To back up or migrate repositories, consult the backup workflow pattern in `references/github-repo-management.md` and the cheatsheet at `references/github-api-cheatsheet.md`.

---

## 4. Pull Request Lifecycle

The standard PR workflow follows a structured sequence:
1. **Branch**: `git checkout -b <type>/<description>`
2. **Commit**: Apply Conventional Commits rules (e.g. `feat: ...`, `fix: ...`). See `references/conventional-commits.md`.
3. **Push**: `git push -u origin HEAD`
4. **Create PR**:
   ```bash
   gh pr create --title "type(scope): description" --body-file .github/pull_request_template.md
   ```
5. **Monitor CI**: `gh pr checks --watch` (or query API for statuses). See `references/ci-troubleshooting.md`.

Refer to the complete manual and fallbacks at `references/github-pr-workflow.md`, and use PR body templates:
- `templates/pr-body-feature.md`
- `templates/pr-body-bugfix.md`

---

## 5. Code Reviews

Review pull requests using a checklist-driven approach:
- Analyze diffs: `gh pr diff <number>`
- Leave line-level comments:
  ```bash
  gh pr review <number> --comment -b "Review comment"
  ```
- Review security parameters (leaked secrets, query injection, unsafe dependencies).

Check `references/github-code-review.md` and use the review output form at `references/review-output-template.md`.

---

## 6. Repository & Codebase Architecture Reviews

For high-level project architectural assessments:
- Map folder dependency layouts.
- Check compliance with design principles (SOLID, hexagonal architecture, etc.).
- Inspect environment setup guides and config loading mechanisms.

Read `references/github-repo-review.md` and check notes on specific architectural reviews in `references/horizon-review-notes.md`.

---

## 7. Issue Management

Create and triage issues:
```bash
gh issue create --title "Bug description" --body "Steps to reproduce..." --label "bug"
```
Use templates to enforce structured submissions:
- `templates/bug-report.md`
- `templates/feature-request.md`

Consult `references/github-issues.md` for workflows on tracking milestones, assigning issues, and triaging priority levels.
