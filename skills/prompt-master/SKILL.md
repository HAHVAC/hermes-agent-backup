# Prompt-Master v1.6.0 — Comprehensive Reference Summary

> **Purpose:** Generates optimized, production-ready prompts for specific AI tools. Activates **only** when user explicitly asks to write, fix, improve, or adapt a prompt. Does NOT activate for general conversation, coding, or document writing.

---

## Identity & Core Rules

**Role:** Operate as a prompt engineer — extract intent, identify target tool, output a single paste-ready prompt with zero wasted tokens.

### Hard Rules (Never Violate)
- **Always confirm target tool** before writing — ask if ambiguous
- **Never add CoT** to reasoning-native models: `o3`, `o4-mini`, `DeepSeek-R1`, `Qwen3 thinking mode`
- **Max 3 clarifying questions** before producing a prompt
- **No padding** — no unrequested explanations, no framework names in output
- **High-risk techniques** (use only when explicitly requested + tool supports them):
  - Mixture of Experts, Tree of Thought, Graph of Thought, Universal Self-Consistency, Prompt Chaining

---

## Output Format

```
1. Single copyable prompt block (ready to paste)
2. 🎯 Target: [tool name], 💡 [One sentence — what was optimized and why]
3. [Optional: 1-2 line setup note, ONLY when genuinely needed]
```

- Copywriting/content prompts: include `[TONE]`, `[AUDIENCE]`, `[BRAND VOICE]`, `[PRODUCT NAME]` placeholders where relevant

---

## Intent Extraction (9 Dimensions — Silent)

| Dimension | What to Extract | Critical? |
|-----------|----------------|-----------|
| **Task** | Precise operation (not vague verbs) | Always |
| **Target tool** | Which AI system receives the prompt | Always |
| **Output format** | Shape, length, structure, filetype | Always |
| **Constraints** | MUST / MUST NOT, scope boundaries | If complex |
| **Input** | What user provides alongside prompt | If applicable |
| **Context** | Domain, project state, prior decisions | If session has history |
| **Audience** | Who reads output, technical level | If user-facing |
| **Success criteria** | Binary pass/fail where possible | If task is complex |
| **Examples** | Input/output pairs for pattern lock | If format-critical |

---

## Tool Routing Reference

### LLM Models

#### Claude (claude.ai / API / 4.x)
- Be **explicit and specific** — Claude 4.x follows instructions literally; missing context = narrow output
- XML tags for complex prompts: `<task>`, `<context>`, `<constraints>`, `<output>`
- **Opus 4.7:** front-load everything in one turn (intent + constraints + acceptance criteria + files)
- Add: *"Only make changes directly requested. Do not add features or refactor beyond what was asked."*
- Influence thinking depth: *"Think carefully before responding"* (more) / *"Prioritize responding quickly"* (less)
- **Do NOT** use fixed thinking budget instructions — Opus 4.7 uses adaptive thinking
- Use **Template M** for agentic/multi-step tasks

#### ChatGPT / GPT-5.x
- Start with smallest prompt that achieves goal — add structure only when needed
- Explicit output contract: format + length + definition of "done"
- Constrain verbosity: *"Respond in under 150 words. No preamble. No caveats."*
- GPT-5.x strengths: long-context synthesis, tone adherence

#### o3 / o4-mini (OpenAI Reasoning Models)
- **SHORT clean instructions ONLY**
- **NEVER add CoT, "think step by step", or reasoning scaffolding**
- Zero-shot first; few-shot only if strictly needed
- System prompts **under 200 words**

#### Gemini 2.x / 3 Pro
- Leverage large context window for document-heavy prompts
- Always add: *"Cite only sources you are certain of. If uncertain, say [uncertain]."*
- Use explicit format locks with labelled examples (prone to format drift)
- Grounded tasks: *"Base your response only on the provided context. Do not extrapolate."*

#### Qwen 2.5 (instruct)
- Strengths: instruction following, JSON output, structured data
- Clear system prompt with role definition
- Shorter focused prompts > long complex ones

#### Qwen3 (thinking mode)
- **Thinking mode** (`/think` or `enable_thinking=True`): treat like o3 — short, no CoT
- **Non-thinking mode**: treat like Qwen2.5 — full structure, explicit format, role assignment

#### Ollama (local)
- **Always ask which model is running first** (Llama3, Mistral, Qwen2.5, CodeLlama behave differently)
- System prompt is most impactful lever — include for Modelfile
- Temperature: `0.1` for coding/deterministic, `0.7–0.8` for creative
- For coding: CodeLlama or Qwen2.5-Coder preferred

#### Llama / Mistral / Open-weight LLMs
- Shorter prompts, flat structure — avoid deep nesting
- More explicit than Claude/GPT — instruction following is weaker
- Always include role in system prompt

#### DeepSeek-R1
- Reasoning-native — **no CoT**
- Add *"Output only the final answer, no reasoning."* to suppress `<think>` tags

#### MiniMax (M2.7 / M2.5)
- OpenAI-compatible API — GPT prompts transfer directly
- M2.7: 1M context window; M2.5-highspeed: 204K context, latency-optimized
- **Temperature must be 0–1 inclusive** (above 1 = failure)
- Supp

[... summary truncated for context management ...]