"""Create a single independent occurrence on the completion transition."""
from calendar import monthrange
from datetime import timedelta
from .work_data import *
from . import placements,custom_fields,discussion
from .dependencies import calendar

PERIODS={"none":"Does not repeat","daily":"Daily","weekly":"Weekly","monthly":"Monthly"}


def add_control(task, form, access):
    field = next(f for f in form["fields"] if f["name"] == "repeat_period")
    field.update(kind="reference", label="Repeat", required=True,
                 value=(val(TASK, task, "repeat_period") if task else None) or "none",
                 readonly=access != "full", options=[{"id": k, "label": v} for k, v in PERIODS.items()])


def validate_period(period, due):
    if period not in PERIODS:
        raise ValueError("Choose a daily, weekly, monthly or non-repeating schedule")
    if period != "none" and not due:
        raise ValueError("A repeating task needs a due date")


async def links(ctx, actor, task):
    result = []
    for source, target, label in (("source_task", "next_task", "Next occurrence"),
                                  ("next_task", "source_task", "Previous occurrence")):
        for link in await find(ctx, "recurrence_link", **{source: task.id}):
            occurrence = await db.read_one(ctx, TASK, val("recurrence_link", link, target))
            if occurrence is not None and await task_role(ctx, actor, occurrence):
                result.append({"label": label, "href": task_path(occurrence.id),
                               "due": val(TASK, occurrence, "due_date")})
    return result


def advance(day,period):
    if period=="daily": return day+timedelta(days=1)
    if period=="weekly": return day+timedelta(days=7)
    year,month=(day.year+1,1) if day.month==12 else (day.year,day.month+1)
    return day.replace(year=year,month=month,day=min(day.day,monthrange(year,month)[1]))


async def next_occurrence(ctx,actor,task):
    period=val(TASK,task,"repeat_period") or "none"
    if period=="none" or await find(ctx,"recurrence_link",source_task=task.id): return None
    due=calendar(val(TASK,task,"due_date"))
    if not due: raise HTTPException(400,"A repeating task needs a due date")
    start=calendar(val(TASK,task,"start_date"))
    new_due=advance(due,period)
    project=await get(ctx,PROJECT,val(TASK,task,"project"))
    base_section=await db.read_one(ctx,SECTION,val(TASK,task,"section"))
    if not base_section:
        from .sections import sections
        base_section=(await sections(ctx,project.id))[0]
    person=val(TASK,task,"assignee")
    base_items=await placements.in_scope(ctx,"section",base_section.id)
    position=max((p.position for p in base_items),default=-1)+1
    values={"approval":bool(val(TASK,task,"approval")),"decision":None,"section":base_section,"task_order":position,"created_by":actor,"repeat_period":period,
            "primary_detached":bool(val(TASK,task,"primary_detached")),"task_title":val(TASK,task,"task_title"),
            "description":val(TASK,task,"description"),"completed":False,
            "assignee":await get(ctx,ACCOUNT,person) if person else None,"due_date":new_due,
            "start_date":new_due-(due-start) if start else None}
    new=await create(ctx,TASK,project,values,"Create next recurring task")
    for entry in await placements.all_for(ctx,task):
        if not entry.link: continue
        local=await get(ctx,PROJECT,entry.project)
        group=await get(ctx,SECTION,entry.section)
        order=max((p.position for p in await placements.in_scope(ctx,"section",group.id)),default=-1)+1
        await create(ctx,placements.PLACEMENT,new,{"project":local,"section":group,"placement_order":order},"Copy recurring project placement")
    for choice in await find(ctx,custom_fields.CHOICE,task=task.id):
        field=await get(ctx,custom_fields.FIELD,val(custom_fields.CHOICE,choice,"field"))
        option=await get(ctx,custom_fields.OPTION,val(custom_fields.CHOICE,choice,"selected_option"))
        await create(ctx,custom_fields.CHOICE,new,{"field":field,"selected_option":option},"Copy recurring task field")
    for sub in await find(ctx,discussion.SUBTASK,task=task.id):
        uid=val(discussion.SUBTASK,sub,"assignee")
        await create(ctx,discussion.SUBTASK,new,{"subtask_title":val(discussion.SUBTASK,sub,"subtask_title"),
            "due_date":val(discussion.SUBTASK,sub,"due_date"),"completed":False,
            "assignee":await get(ctx,ACCOUNT,uid) if uid else None},"Copy unchecked recurring subtask")
    await create(ctx,"recurrence_link",task,{"next_task":new},"Link the next occurrence")
    return new
