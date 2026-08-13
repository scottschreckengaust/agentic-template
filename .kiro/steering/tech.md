---
inclusion: always
---

# Technology & Constraints

## Current State

This is an unscaffolded template. There is:
- No application code
- No build system
- No lockfile
- No CI job that runs tests

Do not invent commands (`make test`, `npm test`, etc.) — none exist yet.

## Agent Tools Configured

- Claude (`.claude/`)
- Codex (`.codex/`)
- Cursor (`.cursor/`)
- Gemini (`.gemini/`, `.github/gemini.yml`)
- OpenCode (`.opencode/`)
- Kiro (`.kiro/`)

## When Scaffolding

When a toolchain is added:
- Commit the lockfile and formatter/linter config (no editor-only settings).
- Document canonical commands in `README.md` and update `AGENTS.md`.
- Use `src/`, `tests/`, `docs/`, `assets/`.
- Mirror source paths in the test tree (`src/auth/session.*` -> `tests/auth/session_test.*`).
- Put slow or service-dependent tests under `tests/integration/`.

## Formatting

- Two spaces for YAML, JSON, and Markdown lists.
- Otherwise defer to the language formatter.
