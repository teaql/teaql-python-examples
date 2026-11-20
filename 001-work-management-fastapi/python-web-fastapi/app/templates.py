from datetime import timedelta
import json
from .work_data import *
from . import custom_fields,discussion,recurrence,sections
from .services.temporal import business_date

TEMPLATE="task_blueprint"
CHOICE="blueprint_choice"
SUB="blueprint_subtask"
INPUTS=("name","title","description","assignee","offset","repeat","approval","choices","subtasks")


def offset(text):
    if text in (None,""): return None
    n=int(text)
    if not 0<=n<=36500: raise HTTPException(400,"Choose a due offset between 0 and 36500 days")
    return n


async def account(ctx,pid,uid):
    if not uid: return None
    user=await get(ctx,ACCOUNT,int(uid))
    if not await role(ctx,user,pid): raise HTTPException(400,"Template assignee must be a project member")
    return user


async def detail(ctx,project):
    result=[]
    for entry in await find(ctx,TEMPLATE,project=project.id):
        choices={str(val(CHOICE,c,"field")):val(CHOICE,c,"selected_option") for c in await find(ctx,CHOICE,blueprint=entry.id)}
        subs=[{"title":val(SUB,s,"subtask_title"),"assignee":val(SUB,s,"assignee"),"offset":val(SUB,s,"due_offset")}
              for s in await find(ctx,SUB,blueprint=entry.id)]
        result.append({"id":entry.id,"name":val(TEMPLATE,entry,"template_name"),"title":val(TEMPLATE,entry,"initial_title"),
                       "description":val(TEMPLATE,entry,"initial_description"),"assignee":val(TEMPLATE,entry,"assignee"),
                       "offset":val(TEMPLATE,entry,"due_offset"),"repeat":val(TEMPLATE,entry,"repeat_period"),
                       "approval":val(TEMPLATE,entry,"approval"),"choices":choices,"subtasks":subs})
    return result


async def clear_children(ctx,template):
    for entity in (CHOICE,SUB):
        for child in await find(ctx,entity,blueprint=template.id): await remove(ctx, entity, child, "Replace template settings")


async def save(ctx,project,data,template=None):
    repeat=data.get("repeat","none")
    days=offset(data.get("offset"))
    if repeat not in recurrence.PERIODS or repeat!="none" and days is None: raise HTTPException(400,"A repeating template needs a due offset")
    description=data.get("description") or None
    if description is not None and (not isinstance(description,str) or len(description)>4000): raise HTTPException(400,"Invalid description")
    values={"template_name":sections.title(data["name"]),"initial_title":sections.title(data["title"]),
            "initial_description":description,"assignee":await account(ctx,project.id,data.get("assignee")),
            "due_offset":days,"repeat_period":repeat,"approval":db.parse_field({"kind":"boolean","nullable":False,"label":"Approval"},data.get("approval",False))}
    if template:
        await edit(ctx,TEMPLATE,template,values,"Edit project task template")
        await clear_children(ctx,template)
    else: template=await create(ctx,TEMPLATE,project,values,"Create project task template")
    choices=json.loads(data.get("choices","{}"))
    subs=json.loads(data.get("subtasks","[]"))
    if not isinstance(choices,dict) or not isinstance(subs,list): raise HTTPException(400,"Invalid template contents")
    for k,v in choices.items():
        if not v: continue
        field=await get(ctx,custom_fields.FIELD,int(k)); option=await get(ctx,custom_fields.OPTION,int(v))
        if val(custom_fields.FIELD,field,"project")!=project.id or val(custom_fields.OPTION,option,"field")!=field.id:
            raise HTTPException(400,"Select an option in this project field")
        await create(ctx,CHOICE,template,{"field":field,"selected_option":option},"Save template field")
    for sub in subs:
        if not isinstance(sub,dict): raise HTTPException(400,"Invalid template subtask")
        await create(ctx,SUB,template,{"subtask_title":sections.title(sub["title"]),"assignee":await account(ctx,project.id,sub.get("assignee")),
                                     "due_offset":offset(sub.get("offset"))},"Save template subtask")


def register(action):
    @action("template-create",*INPUTS)
    async def add(ctx,actor,pid,data):
        project=await require_project(ctx,actor,pid,write=True)
        await save(ctx,project,data)
        return {"location":project_path(pid)}

    async def owned(ctx,actor,bid):
        template=await get(ctx,TEMPLATE,bid)
        project=await require_project(ctx,actor,val(TEMPLATE,template,"project"),write=True)
        return template,project

    @action("template-update",*INPUTS)
    async def update(ctx,actor,bid,data):
        template,project=await owned(ctx,actor,bid)
        await save(ctx,project,data,template)
        return {"location":project_path(project.id)}

    @action("template-delete")
    async def delete(ctx,actor,bid,data):
        template,project=await owned(ctx,actor,bid)
        await clear_children(ctx,template)
        await remove(ctx, TEMPLATE, template, "Delete project task template")
        return {"location":project_path(project.id)}

    @action("template-use")
    async def use(ctx,actor,bid,data):
        from .application import create_in_section
        template,project=await owned(ctx,actor,bid)
        today=business_date(ctx)
        def due(days): return today+timedelta(days=days) if days is not None else None
        first=(await sections.sections(ctx,project.id))[0]
        values={"task_title":val(TEMPLATE,template,"initial_title"),"description":val(TEMPLATE,template,"initial_description"),
                "assignee":await account(ctx,project.id,val(TEMPLATE,template,"assignee")),"start_date":None,
                "due_date":due(val(TEMPLATE,template,"due_offset")),"approval":val(TEMPLATE,template,"approval"),
                "repeat_period":val(TEMPLATE,template,"repeat_period"),"completed":False}
        task=await create_in_section(ctx,actor,project,first,values)
        for choice in await find(ctx,CHOICE,blueprint=bid):
            field=await get(ctx,custom_fields.FIELD,val(CHOICE,choice,"field"))
            opt=await get(ctx,custom_fields.OPTION,val(CHOICE,choice,"selected_option"))
            await create(ctx,custom_fields.CHOICE,task,{"field":field,"selected_option":opt},"Initialize task field from template")
        for sub in await find(ctx,SUB,blueprint=bid):
            await create(ctx,discussion.SUBTASK,task,{"subtask_title":val(SUB,sub,"subtask_title"),"completed":False,
                         "assignee":await account(ctx,project.id,val(SUB,sub,"assignee")),"due_date":due(val(SUB,sub,"due_offset"))},
                         "Create a separate subtask from template")
        return {"location":task_path(task.id)}


async def member_removed(ctx,pid,uid):
    for template in await find(ctx,TEMPLATE,project=pid):
        if val(TEMPLATE,template,"assignee")==uid: await edit(ctx,TEMPLATE,template,{"assignee":None},"Unassign removed template member")
        for sub in await find(ctx,SUB,blueprint=template.id,assignee=uid):
            await edit(ctx,SUB,sub,{"assignee":None},"Unassign removed template subtask member")
