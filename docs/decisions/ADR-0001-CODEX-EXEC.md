# ADR-0001: Use `codex exec` for the Initial Supervisor Interface

Status: Proposed for Phase 0 review

## Decision

Design the first supervisor around stable `codex exec` noninteractive execution with JSONL output and explicit session resumption. Do not automate terminal keystrokes. Keep the app server as a future evaluation because its current documented maturity is experimental.

## Required Phase 1 verification

- actual installed CLI version and help output;
- JSONL event shapes and session identifier;
- exit codes by failure class;
- resume behavior after interruption;
- sandbox and approval behavior;
- authentication expiry behavior;
- usage-limit signals.

