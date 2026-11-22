# Work management with TeaQL

A small team can create projects, manage access, move tasks through a board, and review changes in an inbox. The app also supports task dependencies, recurring work, approvals, templates, and a recycle bin.

```text
models/main.xml      KSML source model
python-lib-core/     Generated Python models, queries, and runtime module
python-web-fastapi/  FastAPI application and React frontend
observability/       OpenTelemetry Collector configuration
```

## Run with Docker Compose

From this directory, start FastAPI, the OpenTelemetry Collector, and OpenObserve.

```sh
docker compose up --build -d --wait
```

| Service | Address |
| --- | --- |
| Work management | [localhost:3000](http://127.0.0.1:3000/) |
| OpenObserve | [localhost:5080](http://127.0.0.1:5080/) |

Sign up in the work management app. For OpenObserve, use `root@teaql.local` and `TeaQL-Work-Local1!`. The example publishes both ports to loopback. You can set `TEAQL_APP_PORT`, `OPENOBSERVE_PORT`, `OPENOBSERVE_EMAIL`, and `OPENOBSERVE_PASSWORD` in a local `.env` file before first startup. OpenObserve initializes its root account when it first creates its data volume.

The app and OpenObserve each use a named volume. `docker compose down` stops the stack and keeps both volumes.

## Follow an operation

1. Open the browser developer tools and select **Network**. Create a project or task, then select the corresponding `POST /api/...` request. Copy `X-TeaQL-Trace-Id` from its response headers.
2. In OpenObserve, open **Traces**, select the `default` stream and filter on the Trace ID. The request appears with its route template and status. Expand it to see application steps such as `project.initialize` or `task.place`, and TeaQL query, graph save, and SQLite provider spans.
3. In **Logs**, select the `default` stream and query the same ID in **SQL Mode**. Allow a few seconds for batched export.

```sql
SELECT * FROM "default" WHERE trace_id = '<trace-id>'
```

The logs show operation outcomes and masked SQL. The request trace records the route template, method and status. TeaQL applies its field masking rules to SQL logs and redacts credentials. In **Metrics**, query `teaql_runtime_operation_count` and filter on `service_name="teaql-work-management"`.

The Docker build pins a public TeaQL development commit from [PR #75](https://github.com/teaql/teaql-python/pull/75) for `BusinessOperation` and standard telemetry.

## Run from a Python environment

Create a virtual environment and install the same application dependencies if you want to run without Docker.

```sh
python3 -m pip install -r requirements-docker.txt
cd python-web-fastapi
PYTHONPATH=../python-lib-core HOST=127.0.0.1 python3 app.py
```

The database defaults to `python-web-fastapi/app.sqlite3`. Set `DATABASE_PATH` to use another SQLite file.

## Work on the frontend

The compiled bundle is included. Rebuild it after changing the React source.

```sh
cd python-web-fastapi/frontend
npm ci
npm run build
```

See the [FastAPI workspace guide](python-web-fastapi/AGENTS.md) for the application entry point, generated modules, and sibling library configuration.
