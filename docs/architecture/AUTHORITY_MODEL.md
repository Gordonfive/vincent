# Authority Model

| Subject | May decide | Must not decide alone |
|---|---|---|
| Owner | Product direction, priorities, security, production, credential scope, destructive actions, major architecture | — |
| ChatGPT | Task decomposition, bounded assignment preparation, review recommendations, routine coordination | Production/destructive actions, credential expansion, or major architecture changes without owner authority |
| Project/control repository | Durable project requirements, task definitions, tests, reports, and project-specific constraints | Weaken Vincent/host security or grant authority outside its own approved scope |
| Optional coordinator | Dispatch, liveness, leases, capability matching, inventory, fleet reporting within approved policy | Product priority, architecture, silent authority expansion, or production approval |
| Vincent worker | Bounded engineering choices, implementation, validation, publication, reporting | Production actions, authority expansion, force-push, unrelated repository changes, or destructive hardware actions |
| Git | Durable source, requirements, decisions, reports, configuration, provenance | Live process state or secret storage |

Conversation alone is not durable task authority. Consequential instructions must be represented through an authenticated durable source or explicit operator action appropriate to the operation.

Task completion, review approval, integration, release, production deployment, and destructive action are separate states and authorities.
