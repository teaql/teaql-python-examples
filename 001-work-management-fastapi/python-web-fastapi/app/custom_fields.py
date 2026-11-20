"""Project-scoped dropdown definitions and task values."""
import json
from .work_data import *
from .sections import title, ordered, place

FIELD = "project_field"
OPTION = "field_option"
CHOICE = "task_field_choice"


async def options(ctx, fid):
    return ordered(OPTION,"option_order",await find(ctx,OPTION,field=fid))


async def definitions(ctx,pid):
    result=[]
    for field in await find(ctx,FIELD,project=pid):
        result.append({"id":field.id,"name":val(FIELD,field,"field_name"),
                       "options":[{"id":o.id,"name":val(OPTION,o,"option_name")} for o in await options(ctx,field.id)]})
    return result


async def values_for(ctx,tid):
    return {val(CHOICE,c,"field"):val(CHOICE,c,"selected_option") for c in await find(ctx,CHOICE,task=tid)}


async def apply_values(ctx,task,project,encoded):
    try: values=json.loads(encoded)
    except (ValueError,TypeError) as e: raise HTTPException(400,"Invalid field values") from e
    if not isinstance(values,dict): raise HTTPException(400,"Expected field values")
    for field_key,raw in values.items():
        field=await get(ctx,FIELD,int(field_key))
        if val(FIELD,field,"project")!=project.id: raise HTTPException(400,"Field belongs to another project")
        existing=await find(ctx,CHOICE,task=task.id,field=field.id)
        if raw in (None,""):
            for c in existing: await remove(ctx, CHOICE, c, "Clear task field value")
            continue
        option=await get(ctx,OPTION,int(raw))
        if val(OPTION,option,"field")!=field.id: raise HTTPException(400,"Choose an option from this field")
        if existing: await edit(ctx,CHOICE,existing[0],{"selected_option":option},"Change task dropdown value")
        else: await create(ctx,CHOICE,task,{"field":field,"selected_option":option},"Set task dropdown value")


async def add_to_form(ctx,task,project,form,access):
    selected=await values_for(ctx,task.id)
    for f in await definitions(ctx,project.id):
        form["fields"].append({"name":"choice_"+str(f["id"]),"label":f["name"],"kind":"reference","required":False,
              "readonly":access!="full","value":str(selected[f["id"]]) if f["id"] in selected else "",
              "options":[{"id":str(o["id"]),"label":o["name"]} for o in f["options"]]})


def register(action):
    @action("field-add","name","options")
    async def add(ctx,actor,pid,data):
        project=await require_project(ctx,actor,pid,write=True)
        field=await create(ctx,FIELD,project,{"field_name":title(data["name"])},"Create project dropdown")
        names=[title(x) for x in str(data.get("options","")).split(",") if x.strip()]
        for i,name in enumerate(dict.fromkeys(names)):
            await create(ctx,OPTION,field,{"option_name":name,"option_order":i},"Create dropdown option")
        return {"location":project_path(pid)}

    @action("option-add","name")
    async def add_option(ctx,actor,fid,data):
        field=await get(ctx,FIELD,fid)
        pid=val(FIELD,field,"project")
        await require_project(ctx,actor,pid,write=True)
        existing=await options(ctx,fid)
        at=max((val(OPTION,r,"option_order") for r in existing),default=-1)+1
        await create(ctx,OPTION,field,{"option_name":title(data["name"]),"option_order":at},"Add dropdown option")
        return {"location":project_path(pid)}

    @action("option-edit","name","position")
    async def edit_option(ctx,actor,oid,data):
        option=await get(ctx,OPTION,oid)
        field=await get(ctx,FIELD,val(OPTION,option,"field"))
        pid=val(FIELD,field,"project")
        await require_project(ctx,actor,pid,write=True)
        if "name" in data: await edit(ctx,OPTION,option,{"option_name":title(data["name"])},"Rename dropdown option")
        if "position" in data: await place(ctx,OPTION,"option_order",option,await options(ctx,field.id),int(data["position"]))
        return {"location":project_path(pid)}

    @action("option-delete")
    async def delete_option(ctx,actor,oid,data):
        option=await get(ctx,OPTION,oid)
        field=await get(ctx,FIELD,val(OPTION,option,"field"))
        pid=val(FIELD,field,"project")
        await require_project(ctx,actor,pid,write=True)
        for c in await find(ctx,CHOICE,selected_option=oid):
            task=await db.read_one(ctx,TASK,val(CHOICE,c,"task"))
            if task and is_trashed(task):
                await c.mark_for_deletion().audit_as("Clear removed option on archived task").save(ctx)
            else: await remove(ctx, CHOICE, c, "Clear deleted dropdown option")
        for item in await find(ctx,"blueprint_choice",selected_option=oid): await remove(ctx, "blueprint_choice", item, "Clear deleted template option")
        await remove(ctx, OPTION, option, "Delete dropdown option")
        return {"location":project_path(pid)}
