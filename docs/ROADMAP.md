# Implementation Roadmap

| Milestone | Outcome | Status | Gate evidence |
|---|---|---|---|
| M0 | Architecture accepted | Complete | Owner accepted commit `8ed265b05cb9549f2deed43ed8a4612150a496fe` |
| M1 | First autonomous worker | Deployment gate | 91 tests and wheel build pass; disposable-host proof remains |
| M2 | Recovery proven | Not started | Failure-injection matrix passes |
| M3 | Universal installer proven | Prototype implemented | Debian 13 ISO builder and guarded USB flasher pass repository tests; physical proof pending |
| M4 | Two-worker coordination proven | Not started | Heterogeneous workers and exclusive claiming pass |
| M5 | Phone-first control proven | Not started | Owner creates/changes tasks and decisions without SSH |
| M6 | Coordinator proven | Not started | Replaceable coordinator, heartbeats, leases, recovery |
| M7 | Multi-project operation proven | Not started | Independent project manifests/policies operate safely |
| M8 | Full Mission Control recovery proven | Not started | Destructive fleet/coordinator recovery completes real task |

## M1 implementation sequence

1. Implement the versioned protocol models and transition enforcement. **Complete.**
2. Prove exclusive ownership through an atomic claim-store contract. **Complete in memory and against a local bare Git remote.**
3. Implement the deterministic supervisor execution loop around a mock executor. **Complete.**
4. Add durable local state, restart reconciliation, and bounded retry classification. **Complete.**
5. Implement the task-specific atomic Git remote claim adapter and integration tests. **Adapter and local-remote race proof complete; hosted-remote proof pending.**
6. Add workspace preparation, independent validation, checkpoint, reporting, and publication. **Complete under isolated Git tests.**
7. Package a conventional Linux service and exercise a harmless disposable-worker task. **Repository implementation complete; physical-host proof pending.**

Hardware provisioning remains outside repository authority and requires separate owner authorization.
