# Copilot instructions for GCC Compass

Use the project context documents in `ai-context-docs/` as working context:

- At the start of a task, read `Memory.md` and `Task.md`.
- Before product or architecture changes, read `PRD.md`, `Architecture.md`, and `Rules.md`.
- Before UI changes, also read `design.md` and check `.streamlit/config.toml`.
- When finishing a task, update `Task.md` and record durable decisions in `Memory.md`.

The context-document structure is adapted from the [AI Context Docs guide](https://github.com/RahulMirji/vibe-coding-context-kit/tree/main/ai-context-docs). Use that guide as a reference for maintaining project context; do not copy its generic templates over the project-specific documentation.

## Project guardrails

- Inspect the relevant code and data before editing; preserve the existing Streamlit and CSV-backed design unless a task requires otherwise.
- Treat bundled records as prototype data. Preserve Verified, Needs review, and Illustrative distinctions, and never imply comprehensive GCC coverage.
- Provider examples are illustrative; company entries needing review are leads, not confirmed claims.
- The Research Assistant is deterministic keyword routing, not a connected LLM or RAG system.
- City cost, talent, policy, and ecosystem values are qualitative signals, not audited benchmarks.
- Keep changes focused, avoid unnecessary dependencies, and verify changes with relevant checks.
- Never put secrets or credentials in tracked files.
