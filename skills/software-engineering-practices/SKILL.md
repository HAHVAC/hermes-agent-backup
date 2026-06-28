---
name: software-engineering-practices
description: Core methodologies for software development including plan formulation, test-driven development (TDD), systematic debugging, code review prep, spike investigations, container execution, and subagent delegation.
category: software-development
---

# Software Engineering Practices

This skill outlines our standardized methodologies for plan formulation, execution, testing, debugging, and task delegation.

---

## 1. Planning and Task Decomposition (`plan`, `writing-plans`)

Before starting any feature implementation or refactor, document your plan:
1. **Formulate**: Break down the task into sequential, bite-sized checklist items.
2. **File Creation**: Write plans to `.hermes/plans/<name>.md`.
3. **Verify**: Ensure boundaries, paths, and API changes are clearly defined.

Refer to `references/plan.md` and `references/writing-plans.md` for specific formatting structures.

---

## 2. Test-Driven Development (TDD) (`test-driven-development`)

Enforce the **RED-GREEN-REFACTOR** workflow:
1. **RED**: Write a failing unit or integration test before implementing the logic. Verify the failure.
2. **GREEN**: Write the minimal amount of code to make the test pass.
3. **REFACTOR**: Clean up code structure, paths, and comments while keeping tests green.

Read guidelines on establishing test boundaries in `references/test-driven-development.md`.

---

## 3. Systematic Debugging (`systematic-debugging`)

Adhere to the **4-Phase Debugging Protocol**:
- **Phase 1: Understand & Reproduce**: Do not modify code. Create a reproducible test case and gather logs.
- **Phase 2: Formulate Hypothesis**: Identify the exact root cause.
- **Phase 3: Implement & Verify**: Apply targeted patches.
- **Phase 4: Document**: Review changes to prevent regressions.

Read `references/systematic-debugging.md` for step-by-step instructions.

---

## 4. Subagent-Driven Development (`subagent-driven-development`)

For large, complex, or multi-step tasks:
- **Delegation**: Spawn child agents with isolated terminal spaces using the `delegate_task` tool.
- **Spec Review**: Confirm expectations before launching tasks.
- **Quality Gates**: Conduct verification passes on output code.

Check the following references:
- `references/subagent-driven-development.md`
- `references/context-budget-discipline.md` (budgeting prompt context)
- `references/gates-taxonomy.md` (defining exit gates)

---

## 5. Spike Investigations & Prototyping (`spike`)

For exploratory coding and validating third-party integrations:
- Write throwaway prototype files in `spikes/`.
- Validate logic without introducing clutter to production code.

Read execution steps in `references/spike.md`.

---

## 6. Remote Debugging & Tooling (`python-debugpy`, `node-inspect-debugger`, `debugging-hermes-tui-commands`)

- **Python Debugging**: Configure `debugpy` to connect pdb REPL or IDEs via DAP. See `references/python-debugpy.md`.
- **Node.js Debugging**: Run with `--inspect` and interact with Chrome DevTools Protocol. See `references/node-inspect-debugger.md`.
- **TUI Debugging**: Troubleshoot Hermes TUI slash commands and UI bindings. See `references/debugging-hermes-tui-commands.md`.

---

## 7. Skill Authoring (`hermes-agent-skill-authoring`, `import-openclaw-skill`)

Rules for writing `SKILL.md` documents and importing skills from official hubs:
- Document trigger phrases, YAML frontmatter, checklists, code snippets, and common pitfalls.
- Read authoring constraints in `references/hermes-agent-skill-authoring.md` and imports in `references/import-openclaw-skill.md`.

---

## 8. Container & Service Supervision (`hermes-s6-container-supervision`)

Modify or extend container services supervised by `s6-overlay`. Read `references/hermes-s6-container-supervision.md`.
