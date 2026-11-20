"""Personal, permission-checked trash with a durable deletion audience and expiry."""
import asyncio
from contextlib import asynccontextmanager
import logging
from teaql.runtime import BusinessOperation
from .work_data import *
from . import placements,activity,auth_model
from .services.temporal import business_time

VIEWER="deleted_task_viewer"
RETENTION=30*86400


def stamp(ctx):
    moment=business_time(ctx)
    return int(moment.timestamp())


def expired(ctx,task):
    deleted=val(TASK,task,"deleted_epoch")
    return deleted is not None and stamp(ctx)-deleted>=RETENTION


async def audience(ctx,task):
    result={val(TASK,task,"created_by"),val(TASK,task,"assignee")}
    result.update(val(activity.PARTICIPANT,p,"participant") for p in await find(ctx,activity.PARTICIPANT,task=task.id))
    result.update(val("task_comment",c,"author") for c in await find(ctx,"task_comment",task=task.id))
    result.discard(None)
    return result


async def restorable(ctx,actor,task):
    homes=await placements.all_for(ctx,task)
    if not homes: return True
    return any([await role(ctx,actor,e.project)=="full" for e in homes])


async def lookup(ctx,actor,tid):
    task=await db.read_one(ctx,TASK,tid)
    if task is None or not is_trashed(task) or expired(ctx,task):
        raise HTTPException(404,"Deleted task not found")
    if not await find(ctx,VIEWER,task=tid,viewer=actor.id): raise HTTPException(404,"Deleted task not found")
    return task


async def purge(ctx,task):
    tid=task.id
    # Explicitly retire all references, including both directions of task relationships.
    retired=set()
    for name,spec in db.ENTITIES.items():
        if name==TASK: continue
        for field in spec["fields"]:
            if field["target"]!=TASK: continue
            for row in await find(ctx,name,**{field["name"]:tid}):
                key=(name,row.id)
                if key not in retired:
                    await row.mark_for_deletion().audit_as("Permanently remove deleted task data").save(ctx)
                    retired.add(key)
    await task.mark_for_deletion().audit_as("Permanently delete task").save(ctx)


def register(action):
    @action("task-trash")
    async def delete(ctx,actor,tid,data):
        task=await get(ctx,TASK,tid)
        if await task_role(ctx,actor,task)!="full": raise HTTPException(403,"Full access is required to delete")
        places=await placements.visible(ctx,actor,task)
        for uid in await audience(ctx,task):
            user=await get(ctx,ACCOUNT,uid)
            if await task_role(ctx,user,task):
                await create(ctx,VIEWER,task,{"viewer":user},"Capture personal deleted-task visibility")
        await edit(ctx,TASK,task,{"deleted_epoch":stamp(ctx)},"Move task to Deleted")
        return {"location":project_path(places[0].project) if places else "/"}

    @action("task-restore")
    async def restore(ctx,actor,tid,data):
        task=await lookup(ctx,actor,tid)
        if not await restorable(ctx,actor,task): raise HTTPException(403,"Full access is required to restore")
        await edit(ctx,TASK,task,{"deleted_epoch":None},"Restore deleted task")
        for viewer in await find(ctx,VIEWER,task=tid): await remove(ctx, VIEWER, viewer, "Clear deletion audience after restore")
        return {"location":task_path(tid)}

    @action("task-purge")
    async def permanently_delete(ctx,actor,tid,data):
        task=await lookup(ctx,actor,tid)
        if not await restorable(ctx,actor,task): raise HTTPException(403,"Full access is required to permanently delete")
        await purge(ctx,task)
        return {"location":"/deleted"}


async def listing(ctx,actor):
    result=[]
    for row in await find(ctx,VIEWER,viewer=actor.id):
        task=await db.read_one(ctx,TASK,val(VIEWER,row,"task"))
        if task and is_trashed(task) and not expired(ctx,task):
            result.append({"id":task.id,"title":val(TASK,task,"task_title"),"canRestore":await restorable(ctx,actor,task),
                           "deleted":val(TASK,task,"deleted_epoch")})
    return sorted(result,key=lambda r:-r["deleted"])


def install_expiry(app):
    from . import main
    original=app.router.lifespan_context
    async def handler(ctx,inputs):
        task=await db.read_one(ctx,TASK,inputs["tid"])
        if task and expired(ctx,task): await purge(ctx,task)
        return {"id":inputs["tid"]}
    async def prepare_expiry(ctx, inputs):
        return {}

    async def verify_expiry(ctx, inputs, before, result):
        task = await db.read_one(ctx, TASK, result["id"])
        return task is None or not expired(ctx, task)

    op=BusinessOperation(name="ExpireTask",version="1",root_type="WorkSpace",parameters={"tid":int},
        authorize=lambda ctx,p:ctx.get_resource("expiry_worker") is True,prepare=prepare_expiry,
        handler=handler,validate=verify_expiry)
    async def sweep():
        while True:
            try:
                ctx=auth_model.bind_context(main.sqlite_context(app.state.data_service))
                ctx.insert_resource("expiry_worker",True)
                query=QUERIES[TASK]().with_deleted_epoch_less_than_or_equal_to(stamp(ctx)-RETENTION)
                for item in await rows(ctx,query,"Find expired deleted tasks"):
                    await op.execute(ctx,key=f"expiry-{item.id}-{val(TASK,item,'deleted_epoch')}",parameters={"tid":item.id},comment="Enforce deleted task retention")
            except Exception:
                logging.getLogger(__name__).exception("Deleted task expiry failed")
            await asyncio.sleep(60)
    @asynccontextmanager
    async def lifespan(application):
        async with original(application):
            worker=asyncio.create_task(sweep())
            try: yield
            finally:
                worker.cancel()
                try: await worker
                except asyncio.CancelledError: pass
    app.router.lifespan_context=lifespan
