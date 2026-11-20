"""Upgrade records created by the initial owner-only version of this application."""
from contextlib import asynccontextmanager

from teaql.runtime import BusinessOperation

from . import auth_model
from .work_data import ACCOUNT, PROJECT, TASK, QUERIES, db, get, val


async def backfill_creator(ctx, params):
    task = await db.read_one(ctx, TASK, params["task_id"])
    if task is not None and val(TASK, task, "created_by") is None:
        # In the MVP the project owner was the only person allowed to create its tasks.
        project = await get(ctx, PROJECT, val(TASK, task, "project"))
        owner = await get(ctx, ACCOUNT, val(PROJECT, project, "owner_account"))
        await task.update_created_by(owner).audit_as("Identify the creator of an owner-only MVP task").save(ctx)
    return {"id": params["task_id"]}


async def prepare_upgrade(ctx, params):
    return {}


async def verify_creator(ctx, params, before, result):
    task = await db.read_one(ctx, TASK, result["id"])
    return task is None or val(TASK, task, "created_by") is not None


restore_creator = BusinessOperation(
    name="BackfillOwnerOnlyTaskCreator", version="1", root_type="WorkSpace",
    parameters={"task_id": int}, authorize=lambda ctx, p: ctx.get_resource("legacy_upgrade") is True,
    prepare=prepare_upgrade, handler=backfill_creator, validate=verify_creator,
)


def install(app):
    from . import main

    original = app.router.lifespan_context

    @asynccontextmanager
    async def lifespan(application):
        async with original(application):
            ctx = auth_model.bind_context(main.sqlite_context(application.state.data_service))
            ctx.insert_resource("legacy_upgrade", True)
            while True:
                tasks = await (QUERIES[TASK]().have_no_created_by().limit(128)
                               .comment("Find owner-only MVP tasks without a creator")
                               .purpose("Upgrade persisted MVP tasks").execute_for_list(ctx))
                if not tasks:
                    break
                for task in tasks:
                    await restore_creator.execute(ctx, key=f"legacy-creator-{task.id}",
                        parameters={"task_id": task.id}, comment="Preserve MVP task ownership")
            yield

    app.router.lifespan_context = lifespan
