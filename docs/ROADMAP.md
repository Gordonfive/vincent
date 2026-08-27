# Vincent Product Roadmap

This roadmap covers **Vincent only**. The private Mission Control program repository owns the overall Vincent + Mission Control program roadmap and cross-product milestones.

Normative product intent and requirements live in [`PRODUCT.md`](PRODUCT.md) and [`REQUIREMENTS.md`](REQUIREMENTS.md). Consequential design choices live in [`decisions/`](decisions/). Current implementation/physical-test state lives in [`STATUS.md`](STATUS.md). Unscheduled ideas belong in GitHub issues rather than a permanent planned-features document.

## Pre-1.0 development

Vincent uses Semantic Versioning. Pre-1.0 development releases use `0.x.y`. Installer build numbers are independent provenance identifiers and do not determine Vincent software versions.

Current pre-1.0 work is focused on proving the installer/worker foundation against the accepted 1.0 requirements rather than accumulating additional speculative features.

## Vincent 1.0.0

### Installer and first boot

- reproducible Debian 13 installer build from exact version-controlled inputs;
- unique monotonically increasing installer build provenance;
- no embedded permanent worker identity, private project/fleet configuration, or reusable credentials;
- normal interactive operator choice for network and storage/partitioning/final write;
- active installer media excluded from target disks without auto-selecting another disk;
- dedicated locked `vincent` runtime service identity with separately controlled privileged/recovery paths;
- first-boot self-test/status/diagnostics leading to standalone READY/unassigned state;
- installer/network diagnostic evidence sufficient to troubleshoot representative physical failures without exposing secrets.

### Runtime and networking

- systemd-managed Vincent runtime/supervisor and narrow privileged helpers;
- persistent worker identity, local health/status, structured logs and human-readable failures;
- wired/Wi-Fi discovery, protected Wi-Fi profiles, Ethernet preference and supported Wi-Fi recovery/failover;
- layered diagnostics for link/association, DHCP/addressing, routing, DNS, HTTP(S)/TLS, Debian package sources, Git/project access and AI-provider access;
- bounded workspace/environment preparation and resource-aware operation;
- safe Git synchronization, ownership/conflict detection and verified remote publication;
- structured task/result/validation handling with interruption/reboot recovery.

### Project connection and work proof

- operator-selected Git/project/control source for standalone V1 operation;
- project dependency/version constraints represented and respected during environment preparation/maintenance;
- bounded harmless real work performed in an isolated environment;
- independent validation executed and recorded;
- resulting Git/project artifacts and structured report published durably;
- failure/block states preserve useful work rather than silently discarding it.

### AI-provider foundation

- Codex supported as the initial AI provider through a provider boundary that does not permanently couple the core worker lifecycle to one vendor;
- provider-specific enrollment/authentication performed locally through the adapter using supported mechanisms;
- reusable provider credentials excluded from Git/task text/ordinary evidence;
- non-secret effective provider identity/scope/health surfaced where supported so unintended account/project use is detectable;
- architecture ready for later Gemini, Copilot, Ollama/local-model and custom-agent providers without redesigning worker identity/task/recovery semantics.

### Maintenance and software lifecycle

- Vincent maintains Debian, its own runtime/dependencies and representative development tooling while respecting project constraints;
- minimum safe in-place Vincent update path from the validated public release channel unless implementation would materially delay the core 1.0 acceptance gate;
- status/reporting clearly distinguishes immutable installer provenance from current Vincent software SemVer;
- clean reinstall remains a supported recovery path even though routine application updates do not require reimaging.

### 1.0 acceptance

Vincent 1.0.0 is not declared until the accepted requirements are backed by outcome-level evidence. At minimum:

- representative physical machines install reproducibly without undocumented repair;
- installer media cannot be selected as the target;
- storage/network choices remain operator-controlled;
- a fresh worker reaches standalone READY;
- runtime wired/Wi-Fi recovery and diagnostics are demonstrated;
- the dedicated `vincent` service identity/privilege boundary is demonstrated;
- one operator-selected project connection completes bounded work, validation and durable result publication;
- installer provenance and current Vincent version are reported separately;
- representative maintenance/update behavior works without requiring a fresh ISO for ordinary software changes;
- a clean repeat install proves reproducibility.

## Vincent 1.1.x

Planned lifecycle improvements after the 1.0 foundation:

- complete/strengthen trusted in-place update if only the minimum path ships in 1.0;
- implement ADR-0010 if accepted: compatible online installer fetches the current approved Vincent release while preserving validated bundled offline fallback;
- explicit installer-to-Vincent compatibility metadata;
- stronger application-update rollback/recovery;
- update channels/policies such as stable/testing, staged/canary adoption and maintenance windows;
- clearer maintenance/project-constraint reporting;
- reduce need to reimage installation media solely because Vincent application software advanced.

## Later Vincent product work

Later work is tracked as GitHub issues and promoted into this roadmap only when scheduled. Expected areas include:

- additional AI-provider adapters;
- stronger worker/provider capability discovery;
- improved local environment/profile management;
- additional supported Linux/base environments when real requirements justify them;
- stronger recovery/diagnostic automation;
- Vincent-side implementation of stable Mission Control protocols as the control-plane product matures.

## Permanent roadmap constraints

- `PRODUCT.md` and `REQUIREMENTS.md` define product intent/requirements; the roadmap does not override them.
- Human/operator approval remains required for destructive hardware actions, production actions, credential expansion and major product/architecture changes.
- Workers are replaceable and least-privileged, but productive hardware is not destroyed merely to demonstrate replaceability outside an explicit acceptance test.
- Public Vincent content never contains private fleet/project state or reusable secrets.
- Mission Control is optional for basic Vincent health/maintenance/update operation.
- Routine Vincent software updates do not rewrite immutable installer provenance.
- Complexity is added to solve demonstrated requirements, not to maximize the appearance of autonomy.
