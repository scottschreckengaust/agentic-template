---
inclusion: always
---

# Product Overview

This repository is an **agentic-template** — a cross-tool AI agent configuration template. It provides a consistent starting point for repositories that use multiple AI coding assistants (Claude, Gemini, Cursor, Codex, OpenCode, Kiro, etc.).

## Purpose

- Provide a unified, opinionated set of agent configuration files that work across tools.
- Establish shared conventions so every AI assistant behaves consistently in this repo.
- Serve as a scaffolding point — the first real change to this template is adding a toolchain.

## Target Users

Developers who use AI coding assistants and want a clean, portable starting configuration that works across multiple tools without duplicating guidance.

## Key Principles

- Single source of truth: `AGENTS.md` contains the canonical guidance; other tool configs point to it.
- No application code exists yet — this is purely configuration until scaffolded.
- Per-developer settings are gitignored; shared settings are committed.
