"""Explicit local smoke: disposable database, fixed clock, no HTTP routes or default grants."""
import asyncio
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from Q import Q
from runtime_module import GENERATED_RUNTIME_MODULE
from teaql.provider.sqlite import create_sqlite_service
from teaql.runtime import UserContext, ContextEntityRef
from teaql.runtime.business_clock import FixedBusinessClock
from .services import identity, temporal, transactions
from .services.errors import AuthenticationRequired, AccessDenied


async def exercise(folder):
    service = create_sqlite_service(str(folder / "smoke.sqlite3"))
    context = UserContext.new().install(GENERATED_RUNTIME_MODULE)
    context.insert_resource("dataService", service)
    context.with_active_root(ContextEntityRef("WorkSpace", 1))
    context.with_business_clock(FixedBusinessClock(datetime(2030, 6, 10, 12, 0, tzinfo=timezone.utc)))
    try:
        await identity.scoped_query(context, "work_space", "read", Q.work_spaces())
    except AuthenticationRequired: pass
    else: raise AssertionError("Missing actor was accepted")
    context.set_user_identifier("smoke")
    identity.bind_actor(context, SimpleNamespace(id="smoke"))
    try:
        await identity.scoped_query(context, "work_space", "read", Q.work_spaces())
    except AccessDenied: pass
    else: raise AssertionError("Missing policy was accepted")

    class SmokePolicy:
        # This policy is local to this explicit smoke and its temporary database.
        def scope(self, context, actor, entity, action, query):
            if entity != "work_space" or action != "read": raise AccessDenied("Smoke scope refused")
            return query.with_id_is(1)
        def allows(self, context, actor, entity, action, current, changes):
            return entity == "work_space" and action == "read" and actor.id == "smoke"
    identity.install_policy(context, SmokePolicy())
    await context.ensure_schema()
    await service.ensure_business_operation_schema()
    query = await identity.scoped_query(context, "work_space", "read", Q.work_spaces())
    row = await query.comment("Read the smoke root").purpose("Verify actual generated API usage").execute_for_one(context)
    await identity.authorize(context, "work_space", "read", row)
    assert row.id == 1
    assert str(temporal.business_date(context)) == "2030-06-10"
    assert temporal.date_value("2030-06-10", field="day").isoformat() == "2030-06-10"
    assert temporal.date_value(None, field="day", nullable=True) is None

    async def allow(ctx, inputs): return identity.actor(ctx).id == "smoke"
    async def before(ctx, inputs): return {}
    async def handler(ctx, inputs): return {"day": str(temporal.business_date(ctx))}
    async def valid(ctx, inputs, before, result): return result["day"] == "2030-06-10"
    operation = transactions.command(name="WorkspaceServiceSmoke", version="1", root_type="WorkSpace",
        parameters={"probe": str}, authorize=allow, prepare=before, handler=handler, validate=valid)
    first = await transactions.execute(operation, context, key="smoke", parameters={"probe": "local"}, comment="Verify command API")
    repeated = await transactions.execute(operation, context, key="smoke", parameters={"probe": "local"}, comment="Verify replay")
    assert first == repeated
    print("PASS workspace services: default denial, scoped query, fixed clock, nullable date, native command and replay")


if __name__ == "__main__":
    with TemporaryDirectory(prefix="teaql-service-smoke-") as folder:
        asyncio.run(exercise(Path(folder)))