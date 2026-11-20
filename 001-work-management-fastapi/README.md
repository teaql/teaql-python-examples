# Work management with TeaQL

A small team can create projects, manage access, move tasks through a board, and review changes in an inbox. The app also supports task dependencies, recurring work, approvals, templates, and a recycle bin.

```text
models/main.xml      KSML source model
python-lib-core/     Generated Python models, queries, and runtime module
python-web-fastapi/  FastAPI application and React frontend
```

## Run from a Python environment

Use a Python environment with FastAPI, Uvicorn, aiosqlite, and a TeaQL development runtime that provides `BusinessOperation` and its SQLite transaction support. The public TeaQL 0.5.0 and 0.6.0 wheels do not provide that API. Check the runtime in your active environment before launching.

```sh
python3 -c 'from teaql.runtime import BusinessOperation, BusinessOperationError'
cd python-web-fastapi
PYTHONPATH=../python-lib-core HOST=127.0.0.1 python3 app.py
```

Open <http://127.0.0.1:3000/> and create an account. The database defaults to `python-web-fastapi/app.sqlite3`. Set `DATABASE_PATH` to use another SQLite file.

## Run with the local benchmark image

If you already have the `teaql-inventory-bench-atomic:0.5.0-20261115` image, run this from the example directory.

```sh
docker run --pull never --rm \
  --publish 127.0.0.1:3000:3000 \
  --mount "type=bind,source=$PWD,target=/example,readonly" \
  --mount type=volume,source=teaql-work-management-example,target=/data \
  --workdir /example/python-web-fastapi \
  --env PYTHONPATH=/example/python-lib-core:/opt/deps \
  --env PYTHONDONTWRITEBYTECODE=1 \
  --env DATABASE_PATH=/data/app.sqlite3 \
  teaql-inventory-bench-atomic:0.5.0-20261115 python3 app.py
```

## Work on the frontend

The compiled bundle is included. Rebuild it after changing the React source.

```sh
cd python-web-fastapi/frontend
npm ci
npm run build
```

See the [FastAPI workspace guide](python-web-fastapi/AGENTS.md) for the application entry point, generated modules, and the sibling library configuration.
