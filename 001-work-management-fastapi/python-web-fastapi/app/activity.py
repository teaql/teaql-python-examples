"""Task history shares the initiating command's transaction and trusted actor."""
from .work_data import *

EVENT="task_event"
PARTICIPANT="task_participant"
PARENTS={"work_subtask":"task","task_comment":"task","task_field_choice":"task",
         "task_dependency":"dependent","task_placement":"task","recurrence_link":"source_task"}
SKIP_FIELDS={"work_space","created_by","task","source_task","dependent","primary_detached"}
TITLES={ACCOUNT:"display_name",PROJECT:"project_name",SECTION:"section_name",TASK:"task_title",
        "project_field":"field_name","field_option":"option_name"}
DESCRIPTIONS={"work_subtask":"Subtask","task_comment":"Comment","task_dependency":"Dependency",
              "task_field_choice":"Field value","task_placement":"Project placement","recurrence_link":"Next occurrence"}


async def human(ctx,name,key,raw):
    if raw is None: return ""
    try: spec=db.field(name,key)
    except StopIteration: return str(raw)
    if spec["kind"]=="reference" and spec["target"] in TITLES:
        related=await db.read_one(ctx,spec["target"],db.identifier(raw))
        if related is not None: return str(val(spec["target"],related,TITLES[spec["target"]]))
    return str(db.identifier(raw))


async def emit(ctx,task,kind,label,old,new,*,project=None,related=None,extra=()):
    actor=await get(ctx,ACCOUNT,int(ctx.user_identifier()))
    event=await db.prepare(ctx,EVENT,task,{"actor":actor,"event_kind":kind,"field_label":label,
        "old_value":str(old) if old not in (None,"") else None,
        "new_value":str(new) if new not in (None,"") else None,
        "scope_project":await get(ctx,PROJECT,project) if project else None,
        "related_task":await get(ctx,TASK,related) if related else None})
    await event.audit_as("Append activity history").save(ctx)
    from .inbox import deliver
    await deliver(ctx,task,event,actor,extra)
    return event


async def track(ctx,name,row,mode,values,previous,reason):
    if name!=TASK and name not in PARENTS: return
    task=row if name==TASK else await db.read_one(ctx,TASK,val(name,row,PARENTS[name]))
    if task is None: return
    pid=None
    related=None
    if name=="task_placement": pid=val(name,row,"project")
    if name=="task_field_choice":
        field=await get(ctx,"project_field",val(name,row,"field"))
        pid=val("project_field",field,"project")
    if name=="task_dependency": related=val(name,row,"blocker")
    if name=="task_comment" and mode=="add":
        uid=val(name,row,"author")
        if not await find(ctx,PARTICIPANT,task=task.id,participant=uid):
            member=await db.prepare(ctx,PARTICIPANT,task,{"participant":await get(ctx,ACCOUNT,uid)})
            await member.audit_as("Remember a task discussion participant").save(ctx)
    if mode!="edit":
        display_key={TASK:"task_title","work_subtask":"subtask_title","task_comment":"comment_text",
                     "task_field_choice":"selected_option","task_dependency":"blocker","task_placement":"project",
                     "recurrence_link":"next_task"}[name]
        value=await human(ctx,name,display_key,val(name,row,display_key))
        label=reason if name==TASK else DESCRIPTIONS[name] + (" added" if mode=="add" else " removed")
        if name=="task_field_choice": label=val("project_field",field,"field_name")
        await emit(ctx,task,name+"_"+mode,label,value if mode=="remove" else None,value if mode=="add" else None,project=pid,related=related)
        if name=="task_dependency":
            blocker=await get(ctx,TASK,related)
            await emit(ctx,blocker,name+"_"+mode,"Blocks task",val(TASK,task,"task_title") if mode=="remove" else None,
                       val(TASK,task,"task_title") if mode=="add" else None,related=task.id)
        return
    for key,raw in values.items():
        new=db.identifier(raw)
        old=previous.get(key)
        if old==new: continue
        if key=="primary_detached" and name==TASK:
            await emit(ctx,task,"task_placement_edit","Project placement","Attached" if new else "Detached",
                       "Detached" if new else "Attached",project=val(TASK,task,"project"))
            continue
        if key in SKIP_FIELDS: continue
        scope=val(TASK,row,"project") if name==TASK and key in {"section","task_order"} else pid
        label=db.field(name,key)["label"]
        if name!=TASK: label=DESCRIPTIONS[name]+" · "+label
        if name=="task_field_choice": label=val("project_field",field,"field_name")
        await emit(ctx,task,name+"_edit",label,await human(ctx,name,key,old),await human(ctx,name,key,new),project=scope,related=related,
                   extra=(old,new) if name==TASK and key=="assignee" else ())


async def visible(ctx,actor,event):
    pid=val(EVENT,event,"scope_project")
    if pid and not await role(ctx,actor,pid): return False
    tid=val(EVENT,event,"related_task")
    if tid:
        other=await db.read_one(ctx,TASK,tid)
        if other is None or not await task_role(ctx,actor,other): return False
    return True


async def detail(ctx,actor,task):
    history=[]
    for event in sorted(await find(ctx,EVENT,task=task.id),key=lambda e:e.id):
        if not await visible(ctx,actor,event): continue
        user=await get(ctx,ACCOUNT,val(EVENT,event,"actor"))
        history.append({"id":event.id,"actor":val(ACCOUNT,user,"display_name"),"label":val(EVENT,event,"field_label"),
                        "old":val(EVENT,event,"old_value"),"new":val(EVENT,event,"new_value"),"at":val(EVENT,event,"event_time")})
    return history
