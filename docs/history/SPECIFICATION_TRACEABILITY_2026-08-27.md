# Historical Specification Traceability — 2026-08-27

**Purpose:** one-time migration evidence for retiring the historical 260-section specification. This file is not a second product specification and is not normative.

Current authority is `docs/PRODUCT.md`, `docs/REQUIREMENTS.md`, accepted ADRs, current architecture/operations, the Vincent product roadmap, Mission Control canonical documentation, and active GitHub issues/PRs.

Every historical section has an explicit disposition below. After review/integration proves no useful intent or requirement was lost, `docs/specification/` is removed from the active tree and Git history remains the archive.

| Section | Disposition | Canonical destination / reason |
|---:|---|---|
| 1 | Migrated | docs/PRODUCT.md; VIN-REQ-0001..0005 |
| 2 | Migrated | docs/PRODUCT.md guiding principles; VIN-REQ-0003,0004 |
| 3 | Migrated | VIN-REQ-0008..0010 |
| 4 | Migrated | VIN-REQ-0007 |
| 5 | Migrated with correction | VIN-REQ-0011..0020; ADR-0003/0004/0005/0006 (forced disk automation superseded) |
| 6 | Migrated | VIN-REQ-0021 |
| 7 | Migrated | VIN-REQ-0022..0024 |
| 8 | Superseded | Repository already established as Gordonfive/vincent; old codex-worker-platform name retired |
| 9 | Migrated | VIN-REQ-0005,0009; project/control-source boundary |
| 10 | Migrated / evolved | VIN-REQ-0031..0034; Mission Control owns fleet dispatch/leases |
| 11 | Migrated | VIN-REQ-0031,0032,0059 |
| 12 | Migrated | VIN-REQ-0034 |
| 13 | Migrated / generalized | VIN-REQ-0028,0046..0049; ADR-0011 |
| 14 | Moved | Mission Control PRODUCT/REQUIREMENTS; Vincent remains headless/standalone |
| 15 | Moved / narrowed | Mission Control program coordination; durable authority is Git/project/control objects, not chat |
| 16 | Moved | Mission Control phone-first product requirements |
| 17 | Moved | Mission Control notification/event backlog/requirements |
| 18 | Migrated / moved | VIN-REQ-0008,0031; Mission Control multi-worker coordination |
| 19 | Moved to project scope | Project-specific environment policy; VIN-REQ-0006,0029 |
| 20 | Migrated | VIN-REQ-0030; CONTRIBUTING.md trunk/PR policy; project integration authority |
| 21 | Migrated | docs/PRODUCT.md lifecycle; VIN-REQ-0002,0005,0028,0038 |
| 22 | Migrated | VIN-REQ-0025,0026; authority model |
| 23 | Migrated | VIN-REQ-0004,0058 |
| 24 | Migrated / moved | VIN-REQ-0054,0055; Mission Control fleet observability |
| 25 | Superseded as phase instruction | Current PRODUCT/REQUIREMENTS/ADRs/roadmaps replace Phase 0 directive |
| 26 | Superseded as phase instruction | Current STATUS and V1_WORKER_ACCEPTANCE replace old Phase 1 sequencing |
| 27 | Superseded as phase instruction | VIN-REQ-0011..0020 and current installer roadmap/acceptance |
| 28 | Superseded as phase instruction | Program roadmap / Mission Control multi-worker milestones |
| 29 | Moved | Mission Control program roadmap / phone-first requirements |
| 30 | Moved | Mission Control product roadmap |
| 31 | Moved | Mission Control operations/automation backlog |
| 32 | Migrated | docs/PRODUCT.md non-goals |
| 33 | Migrated | docs/PRODUCT.md guiding principles; docs/ARCHITECTURE.md |
| 34 | Migrated | VIN-REQ-0061; docs/README.md |
| 35 | Migrated then terminology retired | docs/PRODUCT.md + docs/REQUIREMENTS.md; Project DNA name retired |
| 36 | Migrated | docs/architecture/AUTHORITY_MODEL.md; product/control-plane authority requirements |
| 37 | Moved | Mission Control control/assignment architecture |
| 38 | Migrated | VIN-REQ-0037,0038 |
| 39 | Migrated / generalized | VIN-REQ-0037; provider-specific capacity handling |
| 40 | Migrated | VIN-REQ-0009 |
| 41 | Migrated | VIN-REQ-0010 |
| 42 | Migrated | VIN-REQ-0038,0041 |
| 43 | Migrated | VIN-REQ-0030 |
| 44 | Migrated | VIN-REQ-0023,0063 |
| 45 | Migrated / moved | VIN-REQ-0021,0022,0051; Mission Control enrollment/trust |
| 46 | Migrated | VIN-REQ-0018,0025 |
| 47 | Migrated | VIN-REQ-0026 |
| 48 | Migrated | VIN-REQ-0001,0006 |
| 49 | Moved / migrated | Mission Control capability/role model; VIN-REQ-0009 |
| 50 | Migrated / moved | VIN-REQ-0021; human-readable fleet naming belongs to Mission Control policy |
| 51 | Migrated | VIN-REQ-0055 |
| 52 | Migrated | VIN-REQ-0027 |
| 53 | Migrated | VIN-REQ-0042..0044; ADR-0007/0008 |
| 54 | Migrated | VIN-REQ-0020,0060; SemVer policy |
| 55 | Migrated | VIN-REQ-0057,0058 |
| 56 | Migrated | VIN-REQ-0033,0035,0057 |
| 57 | Migrated | VIN-REQ-0036 |
| 58 | Migrated | VIN-REQ-0035 |
| 59 | Migrated | VIN-REQ-0056 |
| 60 | Migrated | VIN-REQ-0058; V1_WORKER_ACCEPTANCE |
| 61 | Migrated / corrected | docs/PRODUCT.md + VIN-REQ-0002,0054; standalone READY replaces enrollment-required-by-default |
| 62 | Moved | Mission Control web UI/product architecture |
| 63 | Moved | Mission Control service/event-driven architecture |
| 64 | Moved | Mission Control worker-pool/scheduling requirements |
| 65 | Migrated | VIN-REQ-0004,0058 |
| 66 | Migrated / moved | docs/PRODUCT.md boundary; Mission Control owns control-plane product |
| 67 | Migrated | docs/PRODUCT.md success criteria; V1_WORKER_ACCEPTANCE and program roadmap |
| 68 | Superseded | Historical first-agent execution directive; current AGENTS.md/docs/README.md |
| 69 | Superseded | Repository already exists as Gordonfive/vincent; current repository structure/documentation index |
| 70 | Migrated then terminology retired | docs/PRODUCT.md + REQUIREMENTS.md; Project DNA retired |
| 71 | Migrated / generalized | VIN-REQ-0046..0049; provider-specific interfaces verified by adapters |
| 72 | Migrated | VIN-REQ-0032,0059; docs/protocols |
| 73 | Migrated / moved | VIN-REQ-0031; Mission Control leases/claiming |
| 74 | Migrated / moved | VIN-REQ-0021,0051; Mission Control trust/enrollment |
| 75 | Migrated | VIN-REQ-0022,0023; provider/Git auth implementation issues |
| 76 | Migrated | VIN-REQ-0027,0028 |
| 77 | Migrated | VIN-REQ-0029 |
| 78 | Migrated | VIN-REQ-0003,0004,0038; architecture durable/local/ephemeral state |
| 79 | Migrated | VIN-REQ-0038; recovery runbook |
| 80 | Migrated | VIN-REQ-0038; recovery runbook |
| 81 | Migrated / generalized | VIN-REQ-0037,0038 |
| 82 | Migrated / generalized | VIN-REQ-0037 |
| 83 | Migrated | VIN-REQ-0030 |
| 84 | Migrated | authority model; project integration policy |
| 85 | Migrated | VIN-REQ-0033 |
| 86 | Migrated | VIN-REQ-0034 |
| 87 | Migrated | VIN-REQ-0034,0036 |
| 88 | Moved | Mission Control approval/decision requirements |
| 89 | Moved | Mission Control event/notification requirements |
| 90 | Moved | Mission Control liveness/heartbeat requirements |
| 91 | Migrated / moved | Vincent architecture durable-vs-ephemeral boundary; Mission Control operational state |
| 92 | Superseded | Current canonical documentation set replaces Phase 0 package gate |
| 93 | Superseded | Architecture acceptance represented by current requirements/ADRs and PR review |
| 94 | Migrated | VIN-REQ-0059 |
| 95 | Moved to STATUS/test evidence | Current physical hardware roles in docs/STATUS.md |
| 96 | Migrated | VIN-REQ-0018 |
| 97 | Migrated with correction | VIN-REQ-0011..0018; ADR-0003/0004 |
| 98 | Superseded | Fixed disk-layout requirement removed; operator selects layout under ADR-0003 |
| 99 | Migrated | VIN-REQ-0007,0017,0027,0042 |
| 100 | Migrated | VIN-REQ-0006,0042 |
| 101 | Migrated | VIN-REQ-0006,0042 |
| 102 | Migrated / generalized | VIN-REQ-0047..0049 |
| 103 | Migrated | VIN-REQ-0021 |
| 104 | Moved / migrated | Mission Control enrollment approval; VIN-REQ-0051 |
| 105 | Migrated | VIN-REQ-0022,0030 |
| 106 | Migrated | VIN-REQ-0028 |
| 107 | Migrated | VIN-REQ-0033..0035,0057; V1_WORKER_ACCEPTANCE |
| 108 | Migrated | VIN-REQ-0057,0058; V1_WORKER_ACCEPTANCE |
| 109 | Migrated | VIN-REQ-0037,0038 |
| 110 | Migrated / generalized | VIN-REQ-0037,0038 |
| 111 | Migrated | VIN-REQ-0038 |
| 112 | Migrated | VIN-REQ-0038,0058 |
| 113 | Migrated | VIN-REQ-0038,0041 |
| 114 | Migrated | VIN-REQ-0030 |
| 115 | Migrated | VIN-REQ-0029 |
| 116 | Migrated | VIN-REQ-0032,0038 |
| 117 | Migrated | VIN-REQ-0032 |
| 118 | Migrated / moved | VIN-REQ-0034,0036; Mission Control approvals |
| 119 | Migrated / generalized | VIN-REQ-0037 |
| 120 | Migrated | VIN-REQ-0058; V1_WORKER_ACCEPTANCE |
| 121 | Migrated | VIN-REQ-0009 |
| 122 | Migrated / moved | VIN-REQ-0009; Mission Control capability scheduling |
| 123 | Migrated | VIN-REQ-0011,0012 |
| 124 | Migrated | VIN-REQ-0011,0019 |
| 125 | Migrated | VIN-REQ-0016,0023 |
| 126 | Migrated | VIN-REQ-0057 |
| 127 | Migrated | docs/PRODUCT.md automation principle; VIN-REQ-0056 |
| 128 | Migrated | VIN-REQ-0054 |
| 129 | Migrated | VIN-REQ-0055,0062 |
| 130 | Migrated | VIN-REQ-0057; V1_WORKER_ACCEPTANCE |
| 131 | Moved to STATUS/program test plan | Physical second-worker role is temporary program state |
| 132 | Migrated / moved | VIN-REQ-0057; Mission Control multi-worker program milestone |
| 133 | Migrated / moved | VIN-REQ-0022,0051; Mission Control revocation |
| 134 | Migrated | VIN-REQ-0008,0009 |
| 135 | Moved | Mission Control multi-worker coordination/program acceptance |
| 136 | Migrated / moved | VIN-REQ-0031; Mission Control leases/claim arbitration |
| 137 | Moved | Mission Control explicit assignment policy |
| 138 | Migrated / moved | VIN-REQ-0009; Mission Control capability matching |
| 139 | Migrated | VIN-REQ-0030 |
| 140 | Migrated | VIN-REQ-0006,0029 |
| 141 | Moved to project authority | VIN-REQ-0006; project owns development-data authority |
| 142 | Moved to project authority | VIN-REQ-0006; sanitized fixtures are project-specific |
| 143 | Migrated | VIN-REQ-0004,0006 |
| 144 | Migrated | VIN-REQ-0057; program roadmap owns cross-worker gate |
| 145 | Moved | Mission Control control-plane product roadmap |
| 146 | Moved | Mission Control early Git-backed control strategy |
| 147 | Moved | Mission Control integration/API boundary |
| 148 | Moved | Mission Control PRODUCT/REQUIREMENTS/architecture/program roadmap |
| 149 | Moved | Mission Control PRODUCT/REQUIREMENTS/architecture/program roadmap |
| 150 | Moved | Mission Control PRODUCT/REQUIREMENTS/architecture/program roadmap |
| 151 | Moved | Mission Control PRODUCT/REQUIREMENTS/architecture/program roadmap |
| 152 | Moved | Mission Control PRODUCT/REQUIREMENTS/architecture/program roadmap |
| 153 | Moved | Mission Control PRODUCT/REQUIREMENTS/architecture/program roadmap |
| 154 | Moved | Mission Control PRODUCT/REQUIREMENTS/architecture/program roadmap |
| 155 | Moved | Mission Control PRODUCT/REQUIREMENTS/architecture/program roadmap |
| 156 | Moved | Mission Control PRODUCT/REQUIREMENTS/architecture/program roadmap |
| 157 | Moved | Mission Control PRODUCT/REQUIREMENTS/architecture/program roadmap |
| 158 | Moved | Mission Control PRODUCT/REQUIREMENTS/architecture/program roadmap |
| 159 | Moved | Mission Control PRODUCT/REQUIREMENTS/architecture/program roadmap |
| 160 | Moved | Mission Control PRODUCT/REQUIREMENTS/architecture/program roadmap |
| 161 | Moved | Mission Control PRODUCT/REQUIREMENTS/architecture/program roadmap |
| 162 | Moved | Mission Control PRODUCT/REQUIREMENTS/architecture/program roadmap |
| 163 | Moved | Mission Control PRODUCT/REQUIREMENTS/architecture/program roadmap |
| 164 | Moved | Mission Control PRODUCT/REQUIREMENTS/architecture/program roadmap |
| 165 | Moved | Mission Control PRODUCT/REQUIREMENTS/architecture/program roadmap |
| 166 | Moved | Mission Control PRODUCT/REQUIREMENTS/architecture/program roadmap |
| 167 | Moved | Mission Control PRODUCT/REQUIREMENTS/architecture/program roadmap |
| 168 | Moved | Mission Control PRODUCT/REQUIREMENTS/architecture/program roadmap |
| 169 | Moved | Mission Control PRODUCT/REQUIREMENTS/architecture/program roadmap |
| 170 | Moved | Mission Control PRODUCT/REQUIREMENTS/architecture/program roadmap |
| 171 | Moved | Mission Control PRODUCT/REQUIREMENTS/architecture/program roadmap |
| 172 | Moved | Mission Control PRODUCT/REQUIREMENTS/architecture/program roadmap |
| 173 | Moved | Mission Control PRODUCT/REQUIREMENTS/architecture/program roadmap |
| 174 | Moved | Mission Control PRODUCT/REQUIREMENTS/architecture/program roadmap |
| 175 | Moved | Mission Control PRODUCT/REQUIREMENTS/architecture/program roadmap |
| 176 | Moved | Mission Control PRODUCT/REQUIREMENTS/architecture/program roadmap |
| 177 | Migrated / moved | Mission Control capacity policy + VIN-REQ-0037 |
| 178 | Moved | Mission Control PRODUCT/REQUIREMENTS/architecture/program roadmap |
| 179 | Migrated / moved | VIN-REQ-0042/0038 + Mission Control draining policy |
| 180 | Migrated / moved | VIN-REQ-0038 + Mission Control draining policy |
| 181 | Migrated / moved | VIN-REQ-0004/0058 + Mission Control replacement policy |
| 182 | Migrated / moved | VIN-REQ-0022/0058 + Mission Control retirement history |
| 183 | Moved | Mission Control PRODUCT/REQUIREMENTS/architecture/program roadmap |
| 184 | Moved | Mission Control PRODUCT/REQUIREMENTS/architecture/program roadmap |
| 185 | Moved | Mission Control PRODUCT/REQUIREMENTS/architecture/program roadmap |
| 186 | Moved | Mission Control PRODUCT/REQUIREMENTS/architecture/program roadmap |
| 187 | Moved | Mission Control PRODUCT/REQUIREMENTS/architecture/program roadmap |
| 188 | Moved | Mission Control PRODUCT/REQUIREMENTS/architecture/program roadmap |
| 189 | Moved | Mission Control PRODUCT/REQUIREMENTS/architecture/program roadmap |
| 190 | Moved | Mission Control PRODUCT/REQUIREMENTS/architecture/program roadmap |
| 191 | Moved | Mission Control PRODUCT/REQUIREMENTS/architecture/program roadmap |
| 192 | Moved | Mission Control PRODUCT/REQUIREMENTS/architecture/program roadmap |
| 193 | Moved | Mission Control PRODUCT/REQUIREMENTS/architecture/program roadmap |
| 194 | Moved | Mission Control PRODUCT/REQUIREMENTS/architecture/program roadmap |
| 195 | Migrated / moved | VIN-REQ-0028; Mission Control scheduling distinguishes AI-required vs deterministic local work |
| 196 | Migrated | VIN-REQ-0028,0061; provider context supplied from canonical project docs/task |
| 197 | Migrated | VIN-REQ-0061; AGENTS.md |
| 198 | Moved | Mission Control integration/review/self-development/test requirements |
| 199 | Moved | Mission Control integration/review/self-development/test requirements |
| 200 | Moved | Mission Control integration/review/self-development/test requirements |
| 201 | Moved | Mission Control integration/review/self-development/test requirements |
| 202 | Moved | Mission Control integration/review/self-development/test requirements |
| 203 | Moved | Mission Control integration/review/self-development/test requirements |
| 204 | Moved | Mission Control integration/review/self-development/test requirements |
| 205 | Moved | Mission Control integration/review/self-development/test requirements |
| 206 | Moved | Mission Control integration/review/self-development/test requirements |
| 207 | Moved | Mission Control integration/review/self-development/test requirements |
| 208 | Moved | Mission Control integration/review/self-development/test requirements |
| 209 | Moved | Mission Control integration/review/self-development/test requirements |
| 210 | Moved | Mission Control integration/review/self-development/test requirements |
| 211 | Migrated / moved | Vincent security requirements/SECURITY.md and Mission Control threat model |
| 212 | Migrated | Authority model; VIN-REQ-0025 |
| 213 | Migrated | VIN-REQ-0024 |
| 214 | Migrated / moved | VIN-REQ-0022; Mission Control credential lifecycle |
| 215 | Migrated / moved | VIN-REQ-0022,0051; Mission Control emergency revocation |
| 216 | Migrated | VIN-REQ-0023,0063; CI secret scanning |
| 217 | Migrated | VIN-REQ-0025,0026 |
| 218 | Moved | Mission Control/deployment backlog; not a Vincent 1.0 requirement |
| 219 | Migrated / moved | VIN-REQ-0060; Mission Control has independent release process |
| 220 | Migrated / moved | VIN-REQ-0044; Mission Control fleet update policy |
| 221 | Migrated | VIN-REQ-0042..0044 |
| 222 | Migrated | VIN-REQ-0004,0042 |
| 223 | Migrated | VIN-REQ-0008 |
| 224 | Migrated | VIN-REQ-0041,0052 |
| 225 | Migrated | VIN-REQ-0038 |
| 226 | Migrated | VIN-REQ-0054 |
| 227 | Migrated | VIN-REQ-0010 |
| 228 | Migrated | VIN-REQ-0009,0010 |
| 229 | Migrated | VIN-REQ-0010 |
| 230 | Migrated | VIN-REQ-0003,0004; full-system worker backups are non-authoritative |
| 231 | Migrated | VIN-REQ-0058 |
| 232 | Migrated | VIN-REQ-0011,0012 |
| 233 | Migrated | VIN-REQ-0061; docs/README.md start order |
| 234 | Migrated / superseded form | docs/README.md is canonical index; PROJECT_START_HERE retired |
| 235 | Moved | Mission Control docs/README.md canonical start order |
| 236 | Migrated | VIN-REQ-0061; documentation lifecycle rules |
| 237 | Migrated | VIN-REQ-0061; documentation CI validation |
| 238 | Migrated | docs/PRODUCT.md complexity/proven-components principles |
| 239 | Superseded | Current Vincent product roadmap + Mission Control program roadmap replace historical implementation order |
| 240 | Moved | Mission Control PROGRAM_ROADMAP.md cross-product milestones |
| 241 | Migrated / moved | Vincent ROADMAP.md product-only; Mission Control owns program roadmap |
| 242 | Migrated | CONTRIBUTING.md bounded PR/work policy; Mission Control task requirements |
| 243 | Migrated | docs/PRODUCT.md correctness-before-utilization |
| 244 | Migrated | docs/PRODUCT.md proven-components principle |
| 245 | Migrated / moved | docs/PRODUCT.md; Mission Control self-hosted architecture avoids unnecessary cloud dependence |
| 246 | Migrated | VIN-REQ-0007; docs/PRODUCT.md |
| 247 | Migrated | VIN-REQ-0063; MPL-2.0 public product boundary |
| 248 | Migrated / moved | VIN-REQ-0063; Mission Control public-app/private-state split |
| 249 | Resolved | Vincent MPL-2.0; Mission Control AGPLv3 |
| 250 | Moved | Mission Control PRODUCT/REQUIREMENTS/program roadmap |
| 251 | Moved | Mission Control REQUIREMENTS/ROADMAP defines its independent 1.0 |
| 252 | Moved | Mission Control PRODUCT.md non-goals |
| 253 | Moved | Mission Control emergency-stop requirement |
| 254 | Moved | Mission Control global-pause requirement |
| 255 | Migrated / moved | docs/PRODUCT.md human-judgment principle; Mission Control approval policy |
| 256 | Migrated / terminology corrected | PRODUCT/REQUIREMENTS replace Project DNA; Mission Control restores fleet operation |
| 257 | Superseded | Historical first-agent directive; current AGENTS.md/docs/README.md/trunk workflow |
| 258 | Superseded | Current PR template/status/evidence conventions replace first-agent report |
| 259 | Superseded | Current ADR/requirements/PR review process replaces initial Phase 0 review |
| 260 | Migrated / superseded | Incremental design-test-break-recover principle retained; one-time build directive retired |
