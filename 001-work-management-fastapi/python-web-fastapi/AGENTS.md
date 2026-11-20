# work-management-service FastAPI

## Workspace layout check

Before editing and after regeneration, verify the evaluated KSML in the project's
`models/` directory or at its declared model location. Verify that `AGENTS.md`
is in `python-web-fastapi/` directly under the project root, or in the explicitly configured
destination. Use that destination as the workspace root.

- Verify these paths in that directory: `CAPABILITIES.json`, `app.py`, `app/application.py`, `app/main.py`, `frontend/dist/app.js`, `frontend/main.tsx`, `pyproject.toml`.
- If the files landed in an extra nested directory, correct the generation destination and check again.
- Check `workspace_layout.entrypoint` and every path under `workspace_modules`
  in `CAPABILITIES.json` against this directory.
- Resolve `workspace_layout.library_directory` as `../python-lib-core/` and check its `library_modules`. Put that directory on `PYTHONPATH` before startup.
- The required `python-lib-core/` belongs directly under the project root alongside `models/` and `python-web-fastapi/`.

The browser UI is React + TypeScript in `frontend/main.tsx`. Start `PYTHONPATH=../python-lib-core python3 app.py`;
the workspace includes its local JS bundle. React reads JSON from `GET /api/` and
`/api` plus the page path, and posts JSON to the form action. Create requests
send the form's commandKey in the Idempotency-Key header. Keep policy checks and
transactions on the server. For component changes, run `npm ci` and `npm run build`
inside `frontend/`. For styling alone, edit workspace-root `theme.css`.

For business pages, generate `python-web-fastapi`. On the KSML root set
`web_auth_account="ENTITY,NAME,EMAIL,PASSWORD_HASH"` and opt into signup with
`web_auth_registration="self_service"`. On each CRUD entity set
`_web_crud_fields` and `_web_authorization`. Declare containment, reference
queries and creation hooks as needed. Root `web_crud_resource` selects
the legacy owner example for one entity. That entity's form uses its configured
name only. If it needs explicit form fields or application-supplied required
values, remove root `web_crud_resource` and `web_crud_label` and replace
`web_crud_account` with `web_auth_account`. Keep the entity's business fields
and rules. See README for both modes.

Evaluate, regenerate, then register the named rules. Start `PYTHONPATH=../python-lib-core python3 app.py`
and verify the plain browser flow before styling.
For homepage access, `allows(..., "list", None, None)` controls the collection
section. A separate `"create"` decision controls its button. A new user can
qualify for both with zero visible rows if the business rules allow it.
`scope(..., "read", query, parent)` restricts visible rows, then `allows`
checks each row for `"read"`. For nested collections check the supplied parent.
For read/update/delete check the actual record. When an entry is hidden, fix
the named policy in `app/application.py` and exercise the generated page again.
Use workspace-root `theme.css` for styling only.

Use `SERVICE_INDEX.md` and `app/service_examples/` as runnable TeaQL API references.
Consult object/field Query or Write Assist for exact fields, signatures and constraints.
Prefer existing time, identity and transaction helpers when they fit; adapt examples
in application-owned code for business rules. Preserve trusted context, authorization,
reference scopes and transaction boundaries. Verify the affected business flow.
`python -m app.service_smoke` checks common components; also test actual entity operations.
`CAPABILITIES.json` field_contracts and `app/services/contracts.py` define input nullability.
UNSET preserves an omitted update; None clears only nullable fields. Defaults handle omission.
These services/examples are generated without `_web_*`; they register no HTTP routes.
Data services require a trusted actor and an explicit application policy; missing policy denies access.

Current capabilities: authentication enabled;
owner example disabled;
model-declared CRUD/policy hooks enabled.
`CAPABILITIES.json` lists actual modules and generated entity/field coverage.
Register model-named policies, candidate queries and creation hooks in `app/application.py`
or set `TEAQL_APPLICATION_MODULE` to your module. Missing hooks fail closed.
First run `python -m app.auth_smoke`; fix failures before extending the app.
Start with `PYTHONPATH=../python-lib-core python3 app.py`. Authentication uses `app/auth_model.py`.
Use `Depends(current_identity)` from `app.auth` for authenticated actor and context.
React navigation signs out with POST `/api/logout` and a JSON object.
`app/feature_*` supplies CRUD and transactions; business rules stay in application hooks.

- Entity CRUD uses the canonical entity's `/crud/ENTITY/ID` links. CAPABILITIES
  lists its contracts and routes. Authorization is application-owned.
- Before each new feature, map its persisted entities, fields and relations to KSML
  and `CAPABILITIES.json`. Fill gaps in KSML, evaluate and regenerate before coding.
  Preserve application-owned code. Use generated APIs for business persistence;
  do not add business tables or SQL to replace missing model declarations.
- Before using a new API, find entities and fields in `API_INDEX.md`, then run
  `cargo teaql --input MODEL TARGET` with the evaluated KSML.
  Actions: `query`, `write`. For field filters, selection and sorting use
  `python-assist-query/ENTITY.FIELD`; the index gives exact targets and Q entries.
  Scalar set filters take `..._in(value)` or `..._in(*values)`, never a nested list.
  JSON fields allow a dict/list as one JSON value.
- Use one trusted `UserContext` per request; keep identity and permissions server-side.
  Allowlist request fields. Queries require non-empty purpose/comment; writes require audit_as(reason).
- One save is one graph transaction. For atomic multi-save commands use `BusinessOperation`;
  `app/services/transactions.py` and `app/service_examples/atomic_pair.py` (when present)
  demonstrate the boundary. Adapt them with `python-assist-write/ENTITY` for exact APIs.
- `create_pair.py` (when present) demonstrates multi-entity creation with application callbacks.
  Test a late write failure rolls back every participant, even when using your own implementation.
- After changes, run relevant tests and recheck existing flows. See `README.md` for setup.