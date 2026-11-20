"""Acyclic task dependencies and forward-only date propagation."""
from collections import deque
from datetime import date, timedelta
from .work_data import *
from .discussion import require_task

EDGE="task_dependency"


async def open_blockers(ctx,tid):
    result=[]
    for edge in await find(ctx,EDGE,dependent=tid):
        task=await db.read_one(ctx,TASK,val(EDGE,edge,"blocker"))
        if task and not is_trashed(task) and not val(TASK,task,"completed"): result.append(task)
    return result


async def sharing(ctx,task):
    from .placements import all_for
    return {p.project for p in await all_for(ctx,task)}


async def shift_enabled(ctx,left,right):
    for pid in (await sharing(ctx,left)) & (await sharing(ctx,right)):
        project=await get(ctx,PROJECT,pid)
        if val(PROJECT,project,"shift_dates"): return True
    return False


def calendar(value):
    return date.fromisoformat(str(value)) if value else None


async def propagate(ctx,changed):
    queue=deque([changed.id])
    while queue:
        blocker=await get(ctx,TASK,queue.popleft())
        for edge in await find(ctx,EDGE,blocker=blocker.id):
            dependent=await db.read_one(ctx,TASK,val(EDGE,edge,"dependent"))
            if not dependent or is_trashed(dependent): continue
            start=calendar(val(TASK,dependent,"start_date"))
            end=calendar(val(TASK,dependent,"due_date"))
            if not start or not end or not await shift_enabled(ctx,blocker,dependent): continue
            dates=[]
            for other in await find(ctx,EDGE,dependent=dependent.id):
                upstream=await db.read_one(ctx,TASK,val(EDGE,other,"blocker"))
                if not upstream or is_trashed(upstream): continue
                day=calendar(val(TASK,upstream,"due_date"))
                if day and await shift_enabled(ctx,upstream,dependent): dates.append(day)
            if dates and max(dates)>=start:
                new_start=max(dates)+timedelta(days=1)
                await edit(ctx,TASK,dependent,{"start_date":new_start,"due_date":new_start+(end-start)},"Shift dependent task dates")
                queue.append(dependent.id)


async def reaches(ctx,start,wanted):
    pending=[start]
    seen=set()
    while pending:
        tid=pending.pop()
        if tid==wanted: return True
        if tid in seen: continue
        seen.add(tid)
        pending.extend(val(EDGE,e,"blocker") for e in await find(ctx,EDGE,dependent=tid))
    return False


async def detail(ctx,actor,task):
    payload={"blockers":[],"blocking":[],"dependencyCandidates":[]}
    for field,other,key in [("dependent","blocker","blockers"),("blocker","dependent","blocking")]:
        for edge in await find(ctx,EDGE,**{field:task.id}):
            row=await db.read_one(ctx,TASK,val(EDGE,edge,other))
            if row and await task_role(ctx,actor,row):
                payload[key].append({"id":row.id,"title":val(TASK,row,"task_title"),"edge":edge.id})
    if await task_role(ctx,actor,task)=="full":
        query=await task_scope(ctx,actor,"read",QUERIES[TASK](),None)
        existing={b["id"] for b in payload["blockers"]}
        candidates = await rows(ctx, query, "Find visible dependency candidates")
        visible = await visible_task_set(ctx, actor, candidates, set(await project_ids(ctx, actor)))
        payload["dependencyCandidates"] = [{"id": item.id, "title": val(TASK, item, "task_title")}
            for item in candidates if item.id != task.id and item.id not in existing and item.id in visible]
    return payload


def register(action):
    @action("dependency-add","blocker")
    async def add(ctx,actor,tid,data):
        task=await require_task(ctx,actor,tid,{"full"})
        blocker=await require_task(ctx,actor,int(data["blocker"]))
        if await reaches(ctx,blocker.id,tid): raise HTTPException(400,"This dependency would create a loop")
        if not await find(ctx,EDGE,dependent=tid,blocker=blocker.id):
            await create(ctx,EDGE,task,{"blocker":blocker},"Link blocking task")
        return {"location":task_path(tid)}

    @action("dependency-remove")
    async def delete(ctx,actor,eid,data):
        edge=await get(ctx,EDGE,eid)
        task=await require_task(ctx,actor,val(EDGE,edge,"dependent"),{"full"})
        await require_task(ctx,actor,val(EDGE,edge,"blocker"))
        await remove(ctx, EDGE, edge, "Unlink blocking task")
        return {"location":task_path(task.id)}

    @action("shift-setting","enabled")
    async def setting(ctx,actor,pid,data):
        project=await require_project(ctx,actor,pid,write=True)
        enabled=db.parse_field({"kind":"boolean","nullable":False,"label":"Shift dates"},data["enabled"])
        await edit(ctx,PROJECT,project,{"shift_dates":enabled},"Configure dependent date shifting")
        return {"location":project_path(pid)}
