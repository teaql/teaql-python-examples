from .work_data import *
from .sections import title
from .services.temporal import date_value

SUBTASK="work_subtask"
COMMENT="task_comment"


async def require_task(ctx,actor,tid,accesses=None):
    task=await get(ctx,TASK,tid)
    access=await task_role(ctx,actor,task)
    if not access: raise HTTPException(404,"Task not found")
    if accesses and access not in accesses: raise HTTPException(403,"Not allowed for this task")
    return task


def text(value):
    if not isinstance(value,str) or not 1<=len(value.strip())<=4000:
        raise HTTPException(400,"Enter a comment of 1–4000 characters")
    return value.strip()


async def task_people(ctx,actor,task):
    from .placements import visible, all_for
    if not await all_for(ctx,task):
        return {r.id for r in await rows(ctx,QUERIES[ACCOUNT](),"Workspace candidate accounts")}
    pids=[e.project for e in await visible(ctx,actor,task)]
    people=set()
    for pid in pids:
        for link in await find(ctx,MEMBER,project=pid): people.add(val(MEMBER,link,"member_account"))
    return people


async def detail(ctx,actor,task):
    comments=[]
    for row in sorted(await find(ctx,COMMENT,task=task.id),key=lambda c:c.id):
        person=await get(ctx,ACCOUNT,val(COMMENT,row,"author"))
        comments.append({"id":row.id,"body":val(COMMENT,row,"comment_text"),"author":val(ACCOUNT,person,"display_name"),
                         "mine":person.id==actor.id,"edited":val(COMMENT,row,"edited"),"date":val(COMMENT,row,"create_time")})
    subtasks=[]
    for row in await find(ctx,SUBTASK,task=task.id):
        uid=val(SUBTASK,row,"assignee")
        person=await get(ctx,ACCOUNT,uid) if uid else None
        subtasks.append({"id":row.id,"title":val(SUBTASK,row,"subtask_title"),"due":val(SUBTASK,row,"due_date"),
                         "done":val(SUBTASK,row,"completed"),"assignee":uid,"person":val(ACCOUNT,person,"display_name") if person else ""})
    people=[]
    if await task_role(ctx,actor,task)=="full":
        for uid in sorted(await task_people(ctx,actor,task)):
            person=await get(ctx,ACCOUNT,uid)
            people.append({"id":uid,"name":val(ACCOUNT,person,"display_name")})
    return {"comments":comments,"subtasks":subtasks,"people":people}


async def sub_values(ctx,actor,task,data):
    result={}
    if "title" in data: result["subtask_title"]=title(data["title"])
    if "due" in data: result["due_date"]=date_value(data["due"],field="Due date",nullable=True)
    if "done" in data: result["completed"]=db.parse_field({"kind":"boolean","nullable":False,"label":"Completed"},data["done"])
    if "assignee" in data:
        uid=int(data["assignee"]) if data["assignee"] else None
        if uid and uid not in await task_people(ctx,actor,task): raise HTTPException(400,"Choose a project member")
        result["assignee"]=await get(ctx,ACCOUNT,uid) if uid else None
    return result


def register(action):
    @action("subtask-add","title","assignee","due","done")
    async def add(ctx,actor,tid,data):
        task=await require_task(ctx,actor,tid,{"full"})
        values=await sub_values(ctx,actor,task,data)
        if "subtask_title" not in values: raise HTTPException(400,"Enter a task title")
        await create(ctx,SUBTASK,task,{"completed":False,**values},"Create a subtask")
        return {"location":task_path(tid)}

    @action("subtask-edit","title","assignee","due","done")
    async def update(ctx,actor,sid,data):
        sub=await get(ctx,SUBTASK,sid)
        task=await require_task(ctx,actor,val(SUBTASK,sub,"task"),{"full"})
        await edit(ctx,SUBTASK,sub,await sub_values(ctx,actor,task,data),"Change a subtask")
        return {"location":task_path(task.id)}

    @action("subtask-delete")
    async def delete(ctx,actor,sid,data):
        sub=await get(ctx,SUBTASK,sid)
        task=await require_task(ctx,actor,val(SUBTASK,sub,"task"),{"full"})
        await remove(ctx, SUBTASK, sub, "Delete a subtask")
        return {"location":task_path(task.id)}

    @action("comment-add","comment")
    async def post(ctx,actor,tid,data):
        task=await require_task(ctx,actor,tid)
        await create(ctx,COMMENT,task,{"author":actor,"comment_text":text(data["comment"]),"edited":False},"Post task comment")
        return {"location":task_path(tid)}

    async def own(ctx,actor,cid):
        row=await get(ctx,COMMENT,cid)
        task=await require_task(ctx,actor,val(COMMENT,row,"task"))
        if val(COMMENT,row,"author")!=actor.id: raise HTTPException(403,"Only the author can change this comment")
        return row,task

    @action("comment-edit","comment")
    async def correct(ctx,actor,cid,data):
        row,task=await own(ctx,actor,cid)
        await edit(ctx,COMMENT,row,{"comment_text":text(data["comment"]),"edited":True},"Edit own comment")
        return {"location":task_path(task.id)}

    @action("comment-delete")
    async def retract(ctx,actor,cid,data):
        row,task=await own(ctx,actor,cid)
        await remove(ctx, COMMENT, row, "Delete own comment")
        return {"location":task_path(task.id)}
