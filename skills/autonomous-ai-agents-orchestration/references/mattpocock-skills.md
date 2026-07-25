# mattpocock/skills Integration Reference

The `mattpocock/skills` repository (often used inside Claude Code or Codex) provides a structured, disciplined workflow for software engineering using AI agents, moving away from unstructured "vibe coding" toward structured engineering.

## Installation Methods

### 1. Developer Tool / Agent standard harness (skills.sh)
To add to Codex or another Agent-Skills-standard harness:
```bash
npx skills@latest add mattpocock/skills
```
Followed by executing the setup skill in your agent:
```
/setup-matt-pocock-skills
```
This utility configures the issue tracker target (e.g., GitHub, Linear, or local Markdown files), triage labels, and document directories.

### 2. Claude Code Plugin Marketplace
For native Claude Code usage, install the skills as a managed plugin:
```
/plugin marketplace add mattpocock/skills
/plugin install mattpocock-skills@mattpocock
```
Or via the shell:
```bash
claude plugin marketplace add mattpocock/skills
claude plugin install mattpocock-skills@mattpocock
```

---

## Core Workflows & Playbooks

The skills are split into user-invoked orchestrators and model-invoked primitives. Below is the main flow pattern from **Idea** to **Implementation**:

### 1. Phase 1: Clarification & Alignment (`/grill-with-docs` or `/grill-me`)
- **Primitive**: Driven by the `/grilling` skill.
- **Rules**: 
  - AI must interview the user *one question at a time* about decisions and architectural trade-offs. Asking multiple questions at once is forbidden.
  - Facts that can be looked up in the filesystem or workspace must be searched automatically by the agent, rather than asking the user.
  - **With Codebase**: `/grill-with-docs` updates or creates `CONTEXT.md` (a domain glossary) and ADRs (Architecture Decision Records) under `docs/adr/` inline as decisions crystallize.
  - **No Codebase**: `/grill-me` runs the interview statelessly without writing files.

### 2. Phase 2: Specification (`/to-spec`)
- Takes the context of the conversation and codebase to generate a Spec (PRD).
- Does NOT interview the user (just synthesizes).
- Outlines **User Stories** (exhaustive list), **Testing Decisions** (tested modules, seams, prior art), and **Implementation Decisions** (modified modules/interfaces, API contracts, schema changes).
- Avoids specific file paths or code snippets in the spec unless they represent concrete prototype decisions (e.g., a state machine reducer or schema shape).

### 3. Phase 3: Task Breakdown (`/to-tickets`)
- Splits the spec/plan into **Tracer Bullet** tickets (narrow vertical slices crossing schema, API, UI, and tests) rather than horizontal layers.
- Each ticket declares its **blocking edges** (what other tickets must finish first).
- Supports **Wide Refactors** (expand-contract pattern: expand first to keep CI green, migrate call sites in batches, then contract and delete the old form).
- Outputs local ticket files (`.scratch/<feature>/issues/NN-<slug>.md`) or pushes them directly to tracking systems like GitHub or Linear.

### 4. Phase 4: Build & Verify (`/implement` via `/tdd` and `/code-review`)
- Picks tickets from the frontier (unblocked tickets) and implements them.
- Drives **`/tdd`** (test-driven development with a red-green-refactor loop) for each slice.
- Concludes by driving **`/code-review`** (standards audit + spec checklist review).

### 5. Phase 5: Upkeep & Debugging
- **`/improve-codebase-architecture`**: Scans the repository for "shallow modules" (large interfaces, thin implementations), produces an HTML report (under `$TMPDIR/architecture-review-<timestamp>.html`) with Tailwind and Mermaid diagrams, opens it, and interviews the user on deepening opportunities.
- **`/diagnosing-bugs`**: A strict bug-hunting cycle. Requires building a fast, deterministic feedback loop (unit test, curl script, or headless browser) that reproduces the bug (goes Red) *before* hypothesizing or reading code.
