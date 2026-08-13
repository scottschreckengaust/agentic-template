---
inclusion: always
---

# Repository Structure

## Agent Config Layout

```
AGENTS.md              # Single source of truth for all agents
CLAUDE.md              # Points to AGENTS.md
GEMINI.md              # Points to AGENTS.md
.claude/               # Claude-specific config (placeholder)
.codex/                # Codex-specific config (placeholder)
.cursor/               # Cursor-specific config
.cursor/rules/         # Cursor rules (alwaysApply)
.gemini/               # Gemini-specific config (placeholder)
.github/gemini.yml     # GitHub Gemini integration
.gitignore             # Ignores per-developer settings
.kiro/                 # Kiro configuration
.opencode/             # OpenCode config (shared + gitignored overlay)
```

## Conventions

- `AGENTS.md` is the single source of truth. Never duplicate guidance into tool-specific files.
- Per-tool config directories are intentionally near-empty placeholders. Leave them empty unless a change is actually needed.
- Per-developer settings files are gitignored (e.g., `.claude/settings.local.json`, `.opencode/opencode.jsonc`).

## Workflow

- Work in a `git worktree`. Never commit directly on `main`.
- Pull `main` and rebase onto it before finishing work.
- Imperative commit subjects; Conventional Commit prefixes are acceptable.
- Never commit credentials or environment-specific secrets.
