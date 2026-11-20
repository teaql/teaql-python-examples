"""One task with project-local placement, ordering and field values."""
from dataclasses import dataclass
from .work_data import *

PLACEMENT="task_placement"


@dataclass(frozen=True)
class Placement:
    task: object
    project: int
    section: int
    position: int
    link: object = None


def primary(task):
    return Placement(task,val(TASK,task,"project"),val(TASK,task,"section"),val(TASK,task,"task_order") or 0)


def secondary(task,link):
    return Placement(task,val(PLACEMENT,link,"project"),val(PLACEMENT,link,"section"),
                     val(PLACEMENT,link,"placement_order"),link)


async def all_for(ctx,task):
    result=[] if val(TASK,task,"primary_detached") else [primary(task)]
    for link in await find(ctx,PLACEMENT,task=task.id):
        result.append(secondary(task,link))
    return result


async def in_scope(ctx,field,ident,*,include_deleted=False):
    result=[primary(task) for task in await find(ctx,TASK,**{field:ident}) if not val(TASK,task,"primary_detached")]
    for link in await find(ctx,PLACEMENT,**{field:ident}):
        task=await db.read_one(ctx,TASK,val(PLACEMENT,link,"task"))
        if task: result.append(secondary(task,link))
    return sorted((e for e in result if include_deleted or not is_trashed(e.task)),key=lambda e:(e.position,e.task.id))


async def save(ctx,entry,section,index):
    if entry.section==section.id and entry.position==index: return
    if entry.link:
        await edit(ctx,PLACEMENT,entry.link,{"section":section,"placement_order":index},"Move project-local task placement")
    else:
        await edit(ctx,TASK,entry.task,{"section":section,"task_order":index},"Move task in its project")


async def move(ctx,actor,tid,sid,index):
    section=await get(ctx,SECTION,sid)
    pid=val(SECTION,section,"project")
    await require_project(ctx,actor,pid,write=True)
    task=await get(ctx,TASK,tid)
    entry=next((e for e in await all_for(ctx,task) if e.project==pid),None)
    if not entry: raise HTTPException(400,"Task has no placement in that project")
    sequence=[e for e in await in_scope(ctx,"section",sid) if e.task.id!=tid]
    sequence.insert(max(0,min(len(sequence),index)),entry)
    for i,item in enumerate(sequence): await save(ctx,item,section,i)
    return pid


async def add(ctx,task,project):
    if any(e.project==project.id for e in await all_for(ctx,task)): return
    from .sections import sections
    groups=await sections(ctx,project.id)
    if not groups: raise HTTPException(409,"Project has no section")
    section=groups[0]
    sequence=await in_scope(ctx,"section",section.id)
    index=max((e.position for e in sequence),default=-1)+1
    if val(TASK,task,"project")==project.id:
        await edit(ctx,TASK,task,{"primary_detached":False,"section":section,"task_order":index},"Restore project placement")
    else:
        await create(ctx,PLACEMENT,task,{"project":project,"section":section,"placement_order":index},"Add task to another project")


async def visible(ctx,actor,task):
    ids=set(await project_ids(ctx,actor))
    return [e for e in await all_for(ctx,task) if e.project in ids]


async def can_open_orphan(ctx,actor,task):
    if actor.id in (val(TASK,task,"created_by"), val(TASK,task,"assignee")): return True
    return bool(await find(ctx,"task_participant",task=task.id,participant=actor.id) or await find(ctx,"task_comment",task=task.id,author=actor.id))


async def detail(ctx,actor,task,selected):
    places=await visible(ctx,actor,task)
    own_ids={p.project for p in places}
    projects=await rows(ctx,await project_scope(ctx,actor,"read",QUERIES[PROJECT](),None),"Visible projects")
    can_edit=await task_role(ctx,actor,task)=="full"
    result={"projects":[],"candidates":[],"selected":selected}
    for p in projects:
        item={"id":p.id,"name":val(PROJECT,p,"project_name"),"access":await role(ctx,actor,p.id)}
        if p.id in own_ids: result["projects"].append(item)
        elif can_edit and item["access"]=="full": result["candidates"].append(item)
    return result


def register(action):
    @action("project-link","project")
    async def attach(ctx,actor,tid,data):
        from .discussion import require_task
        task=await require_task(ctx,actor,tid,{"full"})
        project=await require_project(ctx,actor,int(data["project"]),write=True)
        await add(ctx,task,project)
        return {"location":task_path(tid)}

    @action("project-unlink","project")
    async def detach(ctx,actor,tid,data):
        from .custom_fields import CHOICE,FIELD
        project=await require_project(ctx,actor,int(data["project"]),write=True)
        task=await get(ctx,TASK,tid)
        entry=next((e for e in await all_for(ctx,task) if e.project==project.id),None)
        if not entry: raise HTTPException(404,"Placement not found")
        for f in await find(ctx,FIELD,project=project.id):
            for c in await find(ctx,CHOICE,task=tid,field=f.id): await remove(ctx, CHOICE, c, "Clear project-local task field")
        if entry.link: await remove(ctx, PLACEMENT, entry.link, "Remove project placement")
        else: await edit(ctx,TASK,task,{"primary_detached":True},"Detach primary project placement")
        return {"location":task_path(tid) if await task_role(ctx,actor,task) else project_path(project.id)}
