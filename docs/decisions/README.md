# Architecture Decision Records

Use ADRs for consequential choices that affect architecture, security boundaries, persistent interfaces, installer behavior, compatibility, or long-term maintenance.

`../DECISIONS.md` is the concise decision index/register. Detailed decisions live here as `ADR-NNNN-SHORT-TITLE.md`.

## ADR format

```markdown
# ADR-NNNN: Title

- Status: Proposed | Accepted | Superseded | Rejected
- Decision date: YYYY-MM-DDTHH:MM:SS±HH:MM
- Supersedes: ADR-NNNN (optional)
- Superseded by: ADR-NNNN (optional)

## Context

What problem or constraint requires a decision?

## Decision

What was decided?

## Alternatives considered

What meaningful alternatives were considered and why were they not selected?

## Consequences

What becomes easier, harder, required, or prohibited because of this decision?

## Validation / follow-up

What implementation, testing, migration, or documentation work is required?
```

## Rules

- Record decisions, not meeting transcripts or task status.
- Prefer explicit supersession over relying only on timestamps.
- Do not rewrite accepted ADR history to make later decisions look original; supersede it.
- Remove obsolete implementation after compatibility/history requirements are satisfied; Git history is sufficient archival provenance.
