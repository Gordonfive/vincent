# Project Start Here

## Read in order

1. `project-dna/PROJECT_DNA.md`
2. `architecture/AUTHORITY_MODEL.md`
3. `architecture/SYSTEM_ARCHITECTURE.md`
4. `security/THREAT_AND_CREDENTIAL_MODEL.md`
5. `protocols/WORKER_PROTOCOL_V1.md`
6. `protocols/SCHEMAS_V1.md`
7. `operations/RECOVERY_MODEL.md`
8. `decisions/ADR-0001-CODEX-EXEC.md`
9. `decisions/ADR-0002-APPLIANCE-ACCOUNTS-AND-CONSOLE.md`
10. `CONTINUATION_HANDOFF.md`
11. `ROADMAP.md`

## Current state

- Phase: Workstream 2 Vincent ISO physical testing and appliance hardening
- Active ISO branch: `workstream/iso-self-test-console`
- Running workers: none
- Coordinator: not implemented
- Production authority: none
- Public repository: `Gordonfive/vincent`
- Private fleet control: `Gordonfive/mission-control`
- Migration: complete enough for accepted Workstream 2 ISO testing; legacy repositories remain preserved
- Current installer policy: no human login account, no owner username/password, root locked before first boot, manual disk selection and final destructive confirmation only
- Local console policy: tty1 persistent Vincent dashboard; tty2 optional non-root Codex console as locked `mission-control` service account
- Runtime source: exact ISO-pinned commit fetched from public Vincent Git; embedded archive is recovery/evidence only
- Next gate: validate the exact current ISO branch tip, rebuild/inspect, then repeat physical installation until the unattended appliance reaches READY

## Durable-state locations

- Intent: `project-dna/`
- Architecture and authority: `architecture/`
- Decisions: `decisions/`
- Schemas and state machines: `protocols/`
- Security: `security/`
- Recovery and operations: `operations/`
- Original specification: `specification/`
- Implementation order and gates: `ROADMAP.md`
- Current continuation state: `CONTINUATION_HANDOFF.md`
