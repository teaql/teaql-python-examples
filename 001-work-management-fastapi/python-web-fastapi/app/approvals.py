"""An approval decision sets completion and uses the same blocker and recurrence rules."""
from .work_data import *
from .discussion import require_task
from . import dependencies, recurrence

DECISIONS={"approved":"Approved","rejected":"Rejected","changes":"Changes requested"}


def label(task):
    return DECISIONS.get(val(TASK,task,"decision"),"Pending approval") if val(TASK,task,"approval") else None


def configure_edit(task,updates):
    before=bool(val(TASK,task,"approval"))
    approval=bool(updates.get("approval",before))
    if approval and updates.get("completed")!=None and bool(updates["completed"])!=bool(val(TASK,task,"completed")):
        raise HTTPException(400,"Use an approval decision to change completion")
    if approval!=before:
        updates.update(decision=None,completed=False)


def register(action):
    @action("approval-decision","decision")
    async def decide(ctx,actor,tid,data):
        task=await require_task(ctx,actor,tid)
        access=await task_role(ctx,actor,task)
        if access!="full" and val(TASK,task,"assignee")!=actor.id: raise HTTPException(403,"Only an editor or the assignee can decide")
        if not val(TASK,task,"approval"): raise HTTPException(400,"This task is not an approval")
        decision=data["decision"]
        if decision not in DECISIONS: raise HTTPException(400,"Choose an approval decision")
        finished=decision in ("approved","rejected")
        if finished and await dependencies.open_blockers(ctx,tid): raise HTTPException(409,"Resolve blockers before deciding")
        was_done=val(TASK,task,"completed")
        await edit(ctx,TASK,task,{"decision":decision,"completed":finished},"Record approval decision")
        if finished and not was_done: await recurrence.next_occurrence(ctx,actor,task)
        return {"location":task_path(tid)}
