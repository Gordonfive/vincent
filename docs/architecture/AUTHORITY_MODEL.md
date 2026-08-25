# Authority Model

| Subject | May decide | Must not decide alone |
|---|---|---|
| Owner | Product direction, priorities, security, production, Project DNA, major architecture | — |
| ChatGPT | Task decomposition, explicit worker assignment, review recommendations, routine coordination | Production/destructive actions or Project DNA changes without owner approval |
| Coordinator | Dispatch, leases, health, capability matching when assignment is absent | Product priority, architecture, or silent reassignment against explicit instruction |
| Worker | Bounded engineering choices, implementation, validation, reporting | Production actions, authority expansion, force-push, unrelated repository changes |
| Git | Durable work, tasks, decisions, reports, configuration, provenance | High-frequency heartbeat or live process state |

Conversation is not command. Workers act only on authenticated durable tasks.

Worker completion, review approval, integration, and production deployment are separate states and authorities.

