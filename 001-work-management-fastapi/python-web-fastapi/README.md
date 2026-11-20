# work-management-service FastAPI workspace

This application loads its generated Python bindings from the sibling `python-lib-core/`. Run the documented commands from this application directory.

The browser UI is React + TypeScript in `frontend/main.tsx`. Start `PYTHONPATH=../python-lib-core python3 app.py`;
the workspace includes its local JS bundle. React reads JSON from `GET /api/` and
`/api` plus the page path, and posts JSON to the form action. Create requests
send the form's commandKey in the Idempotency-Key header. Keep policy checks and
transactions on the server. For component changes, run `npm ci` and `npm run build`
inside `frontend/`. For styling alone, edit workspace-root `theme.css`.

Self registration with `web_auth_account` is closed by default. Enable it explicitly with root `web_auth_registration="self_service"` only when required.

## Runnable API references and common helpers

`SERVICE_INDEX.md` lists the always-generated common services and up to two
model-bound entity examples. Use them as runnable references and consult object/field
Query or Write Assist for exact fields, signatures and constraints. Prefer existing
time, identity and transaction helpers when they fit; adapt examples in application-owned
code for business rules, preserving trusted context, authorization, reference scopes
and transaction boundaries. Verify the affected business flow.
`python -m app.service_smoke` checks common components using a disposable database,
a fixed context-owned clock and an explicit test identity/policy; also test actual entity operations.
The examples register no HTTP routes. Missing identity or application service policy
denies data access before a query. Authentication alone grants no business permission.
Use `app.services.identity.service_context` as a FastAPI dependency and configure
`app.state.workspace_service_policy` in trusted application code. Policies separately
provide query scope, action permission and reference candidate scope.
`app/services/temporal.py` fixes ISO date/instant conversion and preserves model
nullability; omitted updates remain unchanged. `transactions.py` uses the native
BusinessOperation and its supplied callback context. `errors.py` returns safe public
errors. Application routes explicitly map request fields and response DTOs.

`CAPABILITIES.json` contains field_contracts from KSML. `app.services.contracts.field_input`
distinguishes omission (UNSET), explicit clear (None) and application defaults.
Use the same contract for form requirements and server input validation; repair KSML when
the business permits empty values that the model forbids. `create_pair.py`, when present,
shows creation of a parent and referenced child in one BusinessOperation. Application
callbacks supply values, authorization and validation; no business initialization is implicit.

Module paths in CAPABILITIES.json are relative to its directory. Keep the original
manifest with the generated modules and the root app.py launcher. The CLI verifies
the workspace during installation. The download archive is optional. If you need a
copy, use `--keep-zip` to retain the target-named ZIP.

## Generated capabilities in this workspace

- Authentication: enabled.
- Optional owner-based resource example: disabled.
- Model-declared CRUD, policy and candidate hooks: enabled.
- `CAPABILITIES.json` records the generated entity/field/relation coverage and actual workspace modules.
  The domain API catalog is in `API_INDEX.md`.

Actual generated workspace Python modules:

- `app.py`
- `app/__init__.py`
- `app/application.py`
- `app/auth.py`
- `app/auth_model.py`
- `app/auth_smoke.py`
- `app/feature_bindings.py`
- `app/feature_commands.py`
- `app/feature_policy.py`
- `app/feature_web.py`
- `app/main.py`
- `app/persistence_smoke.py`
- `app/service_examples/__init__.py`
- `app/service_examples/atomic_pair.py`
- `app/service_examples/work_project.py`
- `app/service_examples/work_subtask.py`
- `app/service_smoke.py`
- `app/services/__init__.py`
- `app/services/_usage.py`
- `app/services/contracts.py`
- `app/services/errors.py`
- `app/services/identity.py`
- `app/services/inputs.py`
- `app/services/temporal.py`
- `app/services/transactions.py`
- `app/web_transport.py`
- `models/__init__.py`
- `requests/__init__.py`

`app/feature_*` and the editable `app/application.py` are included.
Register the model-named hooks before startup.
Prepare a compatible Python environment as described in the [example setup](../README.md#run-from-a-python-environment).
Start with `PYTHONPATH=../python-lib-core python3 app.py`. Authentication and its FastAPI dependencies
are generated independently of business ownership. Run `python -m app.auth_smoke`
to check registration, case-insensitive login, session restart and audit masking.
Custom navigation can reuse `app.auth.logout_form()`, which submits POST `/logout`.
Authentication routes are GET `/` (sign in or application home), GET `/signup`,
POST `/signup`, POST `/login` and POST `/logout`.
Business pages use the canonical model entity: `/crud/ENTITY/ID`.
The signed-in home links to enabled top-level entities; details link to declared
children. Each entity requires its own policy. No extra owner/resource entity is needed.
FastAPI initializes its SQLite schema and generated domain root at startup.
Run `python -m app.persistence_smoke` to initialize a disposable database and
read the generated root from a second process with initialization disabled.
`app/persistence_smoke.py` also shows the exact generated root query for this
model. Reuse `sqlite_context(data_service)` when composing a request context.

## Troubleshooting

Run focused tests for each change, then recheck existing flows. Inspect the exact
failure and server log before repeating the same failed test.

For streaming endpoints, test against a running server with a total deadline.
Close the stream after the expected event; an ordinary HTTP read can wait for
a long-lived stream to finish.

Use Assist with the original evaluated KSML for exact API names. Request field
help only for the field being used. If an operation is unavailable, report
`MISSING_ASSIST` with its entity, action and field.
Set filters use positional values: `..._in(value1, value2)` or `..._in(*values)`.
For scalar fields, a collection passed as one value raises TypeError at the call
site. A dict/list remains a valid single value for a JSON field.

## Write operations and transactions

### Choose the KSML CRUD configuration

`app.auth` exports `current_identity`, `current_actor`, and `current_context` for
FastAPI `Depends(...)`. Identity and trusted context are cached per request.
| Mode | Where to configure it | What the generated form supplies |
| --- | --- | --- |
| Entity CRUD with `python-web-fastapi` | Root `web_auth_account`; entity `_web_crud_fields` and `_web_authorization` | The entity's allow-listed editable fields. The parent and application creation hook can supply other required values. |
| Legacy owner example with `python-web-fastapi-crud` | Root `web_crud_resource="resource_entity,name_field,owner_relation"`, `web_crud_label="Record"` and `web_crud_account="account_entity,name_field,email_field,password_hash_field"` (or `web_auth_account`) | One editable name. The handler supplies the owner, root and runtime fields; other fields must be optional by design. |

Authentication uses one account with a direct relation to the sole domain root.
List its selected name, email and password hash in `_audit_mask_fields`.
Set `web_auth_registration="self_service"` to opt into self-signup with
`web_auth_account`. Only the legacy example requires the selected resource to
have a writable owner relation to the account.

Use one form configuration per entity. Other entities can use entity CRUD
alongside a separate legacy owner example. To migrate the legacy resource to
entity CRUD, remove root `web_crud_resource` and `web_crud_label`, move the
account configuration to `web_auth_account`, and remove `web_crud_account`.
Keep the domain fields and their requiredness. On that entity list user inputs
in `_web_crud_fields`, declare its `_web_authorization`, and use
`_web_create_handler` for values supplied by business rules. Re-evaluate and
generate `python-web-fastapi`.

The following table describes available opt-in contracts, not a claim that they
are enabled. Check the capability status and actual modules above.

Containment, authorization and reference choices are separate contracts:

| Entity metadata | Meaning |
| --- | --- |
| `_web_container="relation"` | Navigation/list containment and server-bound parent relation; grants no permission |
| `_web_authorization="policy_name"` | Required application policy, with independent query scope and action checks |
| `_web_candidates='{"reference":"query_name"}'` | Application query for each editable reference; validates submitted IDs against the same query |
| `_web_crud_fields="title,notes,approved"` | Explicit form/edit field allowlist, at most 16 fields |
| `_web_title="title"` | Record display field |
| `_web_multiline="notes"` | Explicit multiline text controls; nullability does not select a widget |
| `_web_date_order="begins_on,ends_on"` | Date comparison in generated CRUD commands, before mutation |
| `_web_defaults='{"approved":false}'` | Static editable-field defaults |
| `_web_group="reference"` | Presentation grouping, independent of reference selection |
| `_web_group_query="query_name"` | Query for reference group labels, including empty groups |
| `_web_create_handler="command_name"` | Application-owned creation/default/validation callbacks, executed in the generated transaction |

The CRUD adapter renders plain HTML lists, details and forms from these contracts.
Register the named hooks, start `PYTHONPATH=../python-lib-core python3 app.py`, and exercise the default pages
with a disposable database. Verify creation, refresh, updates and deletion for
the actions the policy grants. For a style-only pass, add `theme.css` at the
workspace root. The generated authentication and CRUD pages load it from
`/teaql-theme.css`; they work without the file. The generator does not emit or
overwrite it. The stylesheet is public, so it should contain presentation rules
only. Repeat the same browser flow after styling.

Retired `_web_parent`, `_web_actor_fields`, `_web_single_refs` and
`_web_create_children` are rejected with migration guidance. No rule substitutes
the current actor or a unique candidate for an explicit business choice.
Zero, one and multiple candidates use the same query contract; a required blank
reference is rejected even when exactly one candidate exists.

After enabling these contracts and regenerating, register the model-named hooks
in editable `app/application.py`, or point
`TEAQL_APPLICATION_MODULE` to your application module with `configure(registry)`.
The generated default module contains no business decisions. Missing registrations
fail closed with entity, field and hook names before serving requests.

```python
def configure(registry):
    registry.policy("policy_name", scope=query_scope, allows=action_permission)
    registry.candidates("query_name", target="target_entity", query=candidate_query)
    registry.creation("command_name", handler=create_business_records,
                      defaults=creation_defaults, validate=check_result, version="1")
```

Callback signatures:

- `scope(context, actor, action, query, parent)` returns the declared generated Request.
- `allows(context, actor, action, entity, parent)` returns True to authorize.

| Operation | Callback arguments | Application decision |
| --- | --- | --- |
| Show a collection | `allows(ctx, actor, "list", None, parent)` | May the actor enter this collection? On the home page parent is None. A denied decision hides the whole section. |
| Show its create button | `allows(ctx, actor, "create", None, parent)` | May the actor create here, including the first record in an empty collection? |
| Select visible rows | `scope(ctx, actor, "read", query, parent)` | Return the generated request restricted by the business visibility rule. An empty scope yields an empty collection. |
| Show each selected row | `allows(ctx, actor, "read", row, parent)` | Check the actual row. Only allowed rows appear. |
| Open, update or delete by ID | `scope` for the requested action, then `allows` on the fetched entity | Enforce record access on direct requests too. |

In a nested collection the parent is the actual container. Decide collection
entry and creation using the actor and this context. Reserve checks that need
a particular record for record actions. Keep each application's grants explicit.
For browser testing, setting `TEAQL_HOME_POLICY_TRACE=1` logs the entity,
policy, callback and denied action for hidden homepage entries. Match the
page's opaque `data-teaql-home-trace` value to its server log entry.
- Candidate queries receive `(context, actor, parent, current)` and return a
  generated Request of the registered target. They may return zero or many rows.
- Creation `defaults(context, actor, parent, submitted)` returns editable defaults.
  Explicit submitted values take precedence; it is optional.
- Creation `handler(context, actor, parent, values)` receives validated business
  input and returns a JSON result with the created record's `id`.
- Creation `validate(context, actor, parent, result)` must return True to commit.

Callbacks can be sync or async. Query scopes and action permissions are both
required. Container access is never inherited as child authorization. Public
parents can have private children, and child permissions may differ from parents.
The standalone basic CRUD example retains its legacy owner behavior only when
these capabilities are not enabled.

The generated `app/feature_bindings.py` provides exact `QUERIES`, `BY_ID`, `BY_IDS`, `FILTERS`,
`MATCHERS` and `UPDATERS`. `feature_commands.py` provides mechanics and audited
saves. Its `prepare(context, entity_name, parent, trusted_values)` helper binds
only the domain root and declared container; applications supply business values
such as owners explicitly. It never creates default children.

The generated creation operation wraps application callbacks in a `BusinessOperation`
with trusted actor provenance, stable idempotency key, schema/hook version and one
transaction. Use only the callback context for all participating queries and saves.
All persisted entity types, fields and relationships belong in KSML. Application
callbacks decide which instances to create and how to authorize/select/default
their values; they do not define a separate persistence schema.
Arbitrary business commands can also use the runtime's
BusinessOperation directly; they are not encoded as web initialization metadata.

The current web adapter targets Python/FastAPI with SQLite and the verified
BusinessOperation runtime. Policies, candidate semantics and application invariants
remain application-owned. Domain constraints needed on every persistence path
must also be enforced in the domain/runtime layer, beyond these CRUD callbacks.

Use `cargo teaql --input MODEL python-assist-write/ENTITY` for creation, updates
and soft deletion. The former create/update/delete Assist targets are replaced
by this single entry. Its preparation helper changes an unsaved or fully loaded
entity without committing it.

Save a prepared entity graph once with `await entity.audit_as(reason).save(context)`.
The runtime commits that graph atomically. Separate saves remain independent,
even with the same UserContext. For a business command spanning separate graphs,
the write Assist shows `BusinessOperation` registration and execution. Use only
the context supplied to its handler for participating saves, and validate a real
late-write failure rolls back all business rows. Keep schema initialization in
startup and return success only after the transaction completes.

Repair model-derived failures in KSML and regenerate the affected Python
artifacts. Before implementing a new feature, check its persistent entity,
field and relationship coverage against KSML and `CAPABILITIES.json`. Fill model
gaps and regenerate first. Do not add business tables or handwritten SQL as a
replacement for missing generated APIs; report a concrete capability gap if it
remains after generation. Keep application-owned routes and UI in separate modules and preserve
them during regeneration. Reuse generated persistence, descriptors and runtime
bindings. Initialize database, audit, actor and authorization resources in
`trusted_context()` from server-side state. Queries require non-empty purpose
and comment; writes require a non-empty audit reason.