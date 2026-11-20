# Workspace services

Use these services as runnable TeaQL API references. Consult object/field Query or Write Assist for exact fields, signatures and constraints. Prefer existing time, identity and transaction helpers when they fit; adapt examples in application-owned code for business rules. Preserve trusted context, authorization, reference scopes and transaction boundaries, then verify the affected flow.

`python -m app.service_smoke` checks common components using a disposable database, an explicit test identity/policy and a fixed clock; also test actual entity operations. No example routes are registered.

- `app/services/temporal.py`: ISO whole-day dates, timezone-aware instants, and the existing context-owned business clock. UNSET preserves a field; None clears only a nullable field.
- `identity.py`: FastAPI `Depends(service_context)` obtains the trusted actor. Install an application policy on `app.state.workspace_service_policy`; no policy means denial before data access.
- `transactions.py`: native BusinessOperation; explicit authorize/prepare/handler/validate callbacks and stable retry keys. All participating queries/saves use the supplied callback context.
- `contracts.py`: `field_input(entity, field, raw=UNSET, operation="create"|"update", default=UNSET)` reads the generated field contract. Omitted updates preserve; explicit None clears only nullable fields. A default handles omission, never overrides an explicit clear. Use `field_contract(entity, field)` to render matching input constraints.
- `errors.py`: safe public errors; raw SQL/exception payloads are not returned.

Policies implement `scope(context, actor, entity, action, query)` and `allows(context, actor, entity, action, current, changes)`. A reference additionally needs `reference_scope(context, actor, entity, field, query, current)`. Return an unevaluated generated request. Containment, authorization and candidate scope remain independent.

## work_project

`from app.service_examples.work_project import WorkProjectService`

Methods: `get(context, id)`, `list(context, *, offset=0, limit=100)`, `create(context, *, audit_reason, value_FIELD=...)`, `update(context, id, *, expected_version, audit_reason, value_FIELD=...)`, `delete(context, id, *, expected_version, audit_reason)`. They require actor and policy bindings. References accept IDs, then load actual authorized entities through the separate candidate query.

| Field | Kind | Nullable |
|---|---|---|
| work_space | reference | false |
| owner_account | reference | false |
| project_name | text | false |
| shift_dates | boolean | true |

## work_subtask

`from app.service_examples.work_subtask import WorkSubtaskService`

Methods: `get(context, id)`, `list(context, *, offset=0, limit=100)`, `create(context, *, audit_reason, value_FIELD=...)`, `update(context, id, *, expected_version, audit_reason, value_FIELD=...)`, `delete(context, id, *, expected_version, audit_reason)`. They require actor and policy bindings. References accept IDs, then load actual authorized entities through the separate candidate query.

| Field | Kind | Nullable |
|---|---|---|
| work_space | reference | false |
| task | reference | false |
| subtask_title | text | false |
| assignee | reference | true |
| due_date | date | true |
| completed | boolean | false |

`atomic_pair.build(version=..., authorize=..., validate=...)` creates a two-entity command using those services. It has no default authorizer and no HTTP entrypoint. Business validation is application-owned.

Application routes explicitly map request fields and response DTOs; do not serialize entity __dict__. Authentication alone grants no data access. Optional `_web_*` contracts enable generated web CRUD independently; these internal services/examples are present without them. Use `app.auth.logout_form()` for POST logout when authentication is enabled.
