"""Verify generated SQLite startup and a durable domain-root write."""
import asyncio
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory

from teaql.provider.sqlite import create_sqlite_service

from Q import Q
from .main import app, sqlite_context


async def read_root(data_service):
    context = sqlite_context(data_service)
    root = await (Q.work_spaces()
                  .with_id_is(1)
                  .comment("Load the domain root created during startup")
                  .purpose("Verify durable generated SQLite initialization")
                  .execute_for_one(context))
    if root is None:
        raise RuntimeError("The generated domain root did not persist")


async def write_then_check():
    async with app.router.lifespan_context(app):
        # ensure_schema() performs the generated, audited root bootstrap.
        await read_root(app.state.data_service)


def persistence_smoke():
    with TemporaryDirectory(prefix="teaql-fastapi-smoke-") as directory:
        database = Path(directory) / "fresh.sqlite3"
        env = {**os.environ, "TEAQL_DATABASE_CONNECTION_STRING": str(database)}
        for step in ("write", "read"):
            subprocess.run([sys.executable, "-m", "app.persistence_smoke", step], env=env, check=True)
    print("PASS SQLite startup, audited bootstrap, and readback from a new process")


if __name__ == "__main__":
    if sys.argv[1:] == ["write"]:
        asyncio.run(write_then_check())
    elif sys.argv[1:] == ["read"]:
        # Skip initialization in the second process to prove persistence.
        asyncio.run(read_root(create_sqlite_service(os.environ["TEAQL_DATABASE_CONNECTION_STRING"])))
    elif not sys.argv[1:]:
        persistence_smoke()
    else:
        raise SystemExit("Usage: python -m app.persistence_smoke")