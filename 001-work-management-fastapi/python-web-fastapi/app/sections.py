"""Ordering for the List and Board. Each move and section deletion runs in one command."""
from .work_data import *
from . import placements


def ordered(name, field, records):
    return sorted(records, key=lambda r: (val(name,r,field) if val(name,r,field) is not None else r.id,r.id))


async def sections(ctx, project_id):
    return ordered(SECTION,"section_order",await find(ctx,SECTION,project=project_id))


async def tasks_in(ctx, section_id):
    return ordered(TASK,"task_order",await find(ctx,TASK,section=section_id))


async def place(ctx, entity, key, row, sequence, index):
    sequence = [other for other in sequence if other.id != row.id]
    sequence.insert(max(0,min(len(sequence),index)),row)
    for position, other in enumerate(sequence):
        if val(entity,other,key) != position:
            await edit(ctx,entity,other,{key:position},"Order " + entity)


def title(value):
    if not isinstance(value,str) or not 1 <= len(value.strip()) <= 200:
        raise HTTPException(400,"Enter a name of 1–200 characters")
    return value.strip()


async def layout(ctx, actor, project):
    contents = []
    accounts = {}
    for section in await sections(ctx,project.id):
        tasks=[]
        for entry in await placements.in_scope(ctx,"section",section.id):
            row=entry.task
            uid = val(TASK,row,"assignee")
            if uid and uid not in accounts:
                account=await get(ctx,ACCOUNT,uid)
                accounts[uid]=val(ACCOUNT,account,"display_name")
            from .approvals import label
            tasks.append({"decision":label(row),"id":row.id,"href":task_path(row.id)+(f"?project={project.id}" if entry.link else ""),"title":val(TASK,row,"task_title"),"done":val(TASK,row,"completed"),
                          "assignee":accounts.get(uid),"due":val(TASK,row,"due_date")})
        contents.append({"id":section.id,"name":val(SECTION,section,"section_name"),"tasks":tasks})
    return contents


def register(action):
    @action("section-add","name")
    async def add(ctx,actor,pid,data):
        project=await require_project(ctx,actor,pid,write=True)
        current=await sections(ctx,pid)
        position=max((val(SECTION,s,"section_order") or 0 for s in current),default=-1)+1
        await create(ctx,SECTION,project,{"section_name":title(data["name"]),"section_order":position,
                                       "default_section":not current},"Create a project section")
        return {"location":project_path(pid)}

    @action("section-edit","name","position")
    async def update(ctx,actor,sid,data):
        section=await get(ctx,SECTION,sid)
        pid=val(SECTION,section,"project")
        await require_project(ctx,actor,pid,write=True)
        if "name" in data: await edit(ctx,SECTION,section,{"section_name":title(data["name"])},"Rename section")
        if "position" in data: await place(ctx,SECTION,"section_order",section,await sections(ctx,pid),int(data["position"]))
        return {"location":project_path(pid)}

    @action("section-delete")
    async def delete(ctx,actor,sid,data):
        section=await get(ctx,SECTION,sid)
        pid=val(SECTION,section,"project")
        project=await require_project(ctx,actor,pid,write=True)
        remaining=[s for s in await sections(ctx,pid) if s.id!=sid]
        if not remaining:
            target=await create(ctx,SECTION,project,{"section_name":"Tasks","section_order":0,"default_section":True},"Replace last project section")
        else:
            target=remaining[0]
            if val(SECTION,section,"default_section"):
                await edit(ctx,SECTION,target,{"default_section":True},"Choose the new default section")
        seq=await placements.in_scope(ctx,"section",target.id)
        offset=max((entry.position for entry in seq),default=-1)+1
        for i,entry in enumerate(await placements.in_scope(ctx,"section",sid,include_deleted=True)):
            await placements.save(ctx,entry,target,offset+i)
        await remove(ctx, SECTION, section, "Delete project section")
        return {"location":project_path(pid)}

    @action("task-move","section","position")
    async def move(ctx,actor,tid,data):
        pid=await placements.move(ctx,actor,tid,int(data["section"]),int(data.get("position",10000)))
        return {"location":project_path(pid)}
