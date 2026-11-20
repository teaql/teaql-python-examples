"""Activity-backed notifications filtered again on each read."""
from .work_data import *
from . import activity

NOTICE="inbox_notice"


async def deliver(ctx,task,event,actor,extra):
    if val(activity.EVENT,event,"event_kind") in ("task_comment_edit","task_comment_remove"):
        return
    recipients={val(TASK,task,"created_by"),val(TASK,task,"assignee"),*extra}
    recipients.update(val(activity.PARTICIPANT,r,"participant") for r in await find(ctx,activity.PARTICIPANT,task=task.id))
    recipients.discard(None)
    recipients.discard(actor.id)
    for uid in recipients:
        person=await get(ctx,ACCOUNT,uid)
        notice=await db.prepare(ctx,NOTICE,task,{"event":event,"recipient":person,"read_flag":False})
        await notice.audit_as("Notify task follower").save(ctx)


async def visible_event(ctx,actor,notice):
    if val(NOTICE,notice,"recipient")!=actor.id: return None
    task=await db.read_one(ctx,TASK,val(NOTICE,notice,"task"))
    if task is None or not await task_role(ctx,actor,task): return None
    event=await db.read_one(ctx,activity.EVENT,val(NOTICE,notice,"event"))
    if event is None or not await activity.visible(ctx,actor,event): return None
    return task,event


async def listing(ctx, actor):
    notices = await find(ctx, NOTICE, recipient=actor.id)
    if not notices:
        return []
    events = await by_ids(ctx, activity.EVENT, (val(NOTICE, n, "event") for n in notices))
    task_ids = {val(NOTICE, n, "task") for n in notices}
    task_ids.update(val(activity.EVENT, e, "related_task") for e in events.values())
    task_ids.discard(None)
    tasks = await by_ids(ctx, TASK, task_ids)
    projects = set(await project_ids(ctx, actor))
    visible = await visible_task_set(ctx, actor, tasks.values(), projects)
    people = await by_ids(ctx, ACCOUNT, (val(activity.EVENT, e, "actor") for e in events.values()))
    result = []
    for notice in sorted(notices, key=lambda n: -n.id):
        tid = val(NOTICE, notice, "task")
        event = events.get(val(NOTICE, notice, "event"))
        if tid not in visible or event is None:
            continue
        project = val(activity.EVENT, event, "scope_project")
        related = val(activity.EVENT, event, "related_task")
        if (project and project not in projects) or (related and related not in visible):
            continue
        who = people[val(activity.EVENT, event, "actor")]
        result.append({"id": notice.id, "task": val(TASK, tasks[tid], "task_title"),
                       "read": val(NOTICE, notice, "read_flag"), "actor": val(ACCOUNT, who, "display_name"),
                       "label": val(activity.EVENT, event, "field_label"), "old": val(activity.EVENT, event, "old_value"),
                       "new": val(activity.EVENT, event, "new_value"), "at": val(activity.EVENT, event, "event_time")})
    return result


def register(action):
    @action("notice-read","state","open")
    async def read(ctx,actor,nid,data):
        notice=await get(ctx,NOTICE,nid)
        pair=await visible_event(ctx,actor,notice)
        if not pair: raise HTTPException(404,"Notification not found")
        state=db.parse_field({"kind":"boolean","nullable":False,"label":"Read"},data["state"])
        await edit(ctx,NOTICE,notice,{"read_flag":state},"Change personal notification state")
        return {"location":task_path(pair[0].id) if data.get("open") is True else "/inbox"}
