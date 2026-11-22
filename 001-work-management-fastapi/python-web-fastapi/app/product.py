"""Application-owned, same-origin JSON workflows mounted before generic CRUD routes."""
import json
import secrets
from fastapi import APIRouter, Depends, HTTPException, Request
from teaql.runtime import BusinessOperationError
from . import sections, custom_fields, discussion, dependencies, placements, recurrence, activity, approvals, trash, templates, inbox
from .auth import Identity, current_identity
from .web_transport import browser_shell, json_fields, private_response
from .feature_web import record_form_data, collection_data
from .services.transactions import command, execute
from . import auth_model, observability, upgrade
from .work_data import *

router = APIRouter(dependencies=[Depends(private_response)])
who = Depends(current_identity)
ACTIONS = {}


def action(name, *fields):
    def register(handler):
        ACTIONS[name] = (set(fields), handler)
        return handler
    return register


async def authorize(ctx, inputs):
    return ctx.user_identifier() == str(inputs["actor_id"]) and inputs["action"] in ACTIONS


async def prepare(ctx, inputs):
    return {}


async def handle(ctx, inputs):
    actor = await auth_model.account_by_id(ctx, inputs["actor_id"])
    if actor is None: raise HTTPException(401, "Sign in first")
    _, handler = ACTIONS[inputs["action"]]
    return await handler(ctx, actor, inputs["target_id"], json.loads(inputs["payload"]))


async def validate(ctx, inputs, before, result):
    return isinstance(result, dict) and "location" in result


operation = command(name="WorkspaceChange", version="1", root_type="WorkSpace",
                    parameters={"actor_id": int, "action": str, "target_id": int, "payload": str},
                    authorize=authorize, prepare=prepare, handler=handle, validate=validate)


async def change(request, identity, name, target_id, payload=None):
    if name not in ACTIONS: raise HTTPException(404, "Action not found")
    allowed, _ = ACTIONS[name]
    values = await json_fields(request, allowed) if payload is None else payload
    key = request.headers.get("Idempotency-Key", "")
    if not key and name in ("task-edit","task-trash"): key=secrets.token_urlsafe(24)
    if not 1 <= len(key) <= 200: raise HTTPException(400, "A command key is required")
    try:
        with observability.observe_business_step(identity.context, name):
            return await execute(
                operation,
                identity.context,
                key=key,
                parameters={
                    "actor_id": identity.actor.id,
                    "action": name,
                    "target_id": target_id,
                    "payload": json.dumps(values, sort_keys=True),
                },
                comment="Apply workspace change " + name,
            )
    except BusinessOperationError as error:
        if isinstance(error.__cause__, HTTPException): raise error.__cause__
        if isinstance(error.__cause__, (ValueError, KeyError, TypeError)):
            raise HTTPException(400, "Invalid input: " + str(error.__cause__)) from error
        raise


@router.post("/api/change/{name}/{target_id}")
async def change_route(name: str, target_id: int, request: Request, identity: Identity = who):
    return await change(request, identity, name, target_id)


@action("member-add", "account")
async def add_member(ctx, actor, project_id, values):
    project = await require_project(ctx, actor, project_id, write=True)
    person = await get(ctx, ACCOUNT, int(values["account"]))
    if not await find(ctx, MEMBER, project=project.id, member_account=person.id):
        await create(ctx, MEMBER, project, {"member_account":person,"access_role":"full"}, "Add a project member")
    return {"location": project_path(project.id)}


@action("member-remove", "account")
async def remove_member(ctx, actor, project_id, values):
    project = await require_project(ctx, actor, project_id, write=True)
    if int(values["account"])==val(PROJECT,project,"owner_account"): raise HTTPException(400,"The project owner keeps full access")
    members = await find(ctx, MEMBER, project=project_id, member_account=int(values["account"]))
    for link in members: await remove(ctx, MEMBER, link, "Remove a project member")
    await templates.member_removed(ctx,project_id,int(values["account"]))
    return {"location": project_path(project.id) if int(values["account"]) != actor.id else "/"}


@action("member-role","account","role")
async def set_role(ctx,actor,project_id,values):
    project=await require_project(ctx,actor,project_id,write=True)
    uid=int(values["account"])
    if uid in (actor.id,val(PROJECT,project,"owner_account")): raise HTTPException(403,"Change another member's role; the owner keeps full access")
    new=values["role"]
    if new not in ("full","comment"): raise HTTPException(400,"Choose full or comment-only access")
    links=await find(ctx,MEMBER,project=project.id,member_account=uid)
    if not links: raise HTTPException(404,"Member not found")
    await edit(ctx,MEMBER,links[0],{"access_role":new},"Change project member access")
    return {"location":project_path(project.id)}


async def project_payload(ctx, actor, project):
    memberships = await find(ctx, MEMBER, project=project.id)
    members = {val(MEMBER,row,"member_account"):(val(MEMBER,row,"access_role") or "full") for row in memberships}
    access=await role(ctx,actor,project.id)
    query=QUERIES[ACCOUNT]() if access=="full" else BY_IDS[ACCOUNT](QUERIES[ACCOUNT](),list(members))
    accounts = await rows(ctx, query, "List workspace accounts for membership management")
    def person(row):
        return {"id":row.id, "name":val(ACCOUNT,row,"display_name"),"email":val(ACCOUNT,row,"email_address")}
    layout=await sections.layout(ctx,actor,project)
    fields=await custom_fields.definitions(ctx,project.id)
    option_labels = {o["id"]: f["name"] + ": " + o["name"] for f in fields for o in f["options"]}
    task_values = {}
    if option_labels:
        local_fields = FILTERS[custom_fields.FIELD]["project"](QUERIES[custom_fields.FIELD](), project.id)
        choices = MATCHERS[custom_fields.CHOICE]["field"](QUERIES[custom_fields.CHOICE](), local_fields)
        for value in await rows(ctx, choices, "Read dropdown values for this project's board"):
            label = option_labels.get(val(custom_fields.CHOICE, value, "selected_option"))
            if label is not None:
                task_values.setdefault(val(custom_fields.CHOICE, value, "task"), []).append(label)
    for section in layout:
        for task in section["tasks"]:
            task["values"] = task_values.get(task["id"], [])
    return {"id":project.id, "templates":await templates.detail(ctx,project),"shiftDates":bool(val(PROJECT,project,"shift_dates")), "fields":fields, "sections":layout, "members":[{**person(row),"role":members[row.id],"owner":row.id==val(PROJECT,project,"owner_account"),"me":row.id==actor.id} for row in accounts if row.id in members],
            "candidates":[person(row) for row in accounts if row.id not in members],
            "access":access}


@router.get("/api/crud/work_project/{project_id:int}")
async def project_detail(project_id: int, identity: Identity = who):
    ctx, actor = identity.context, identity.actor
    project = await require_project(ctx, actor, project_id)
    writable=await role(ctx,actor,project_id)=="full"
    return {"kind":"record","title":val(PROJECT,project,"project_name"),
            "form":await record_form_data(PROJECT,identity,entity=project),
            "collections":[{"label":"Task","create":f"/crud/work_task/{project_id}/new" if writable else None}],
            "project":await project_payload(ctx,actor,project)}


TASK_FIELDS = db.ENTITIES[TASK]["editable"]


@action("task-edit", *TASK_FIELDS, "custom_fields", "context_project", "repeat_period")
async def edit_task(ctx, actor, ident, values):
    task = await get(ctx, TASK, ident)
    access = await task_role(ctx, actor, task)
    if not access: raise HTTPException(404, "Task not found")
    selected=int(values.pop("context_project",0) or 0)
    if access != "full" and (access != "assignee" or set(values) - {"completed"}):
        raise HTTPException(403, "Only completion can be changed by a former member assigned this task")
    visible=await placements.visible(ctx,actor,task)
    if selected and selected not in [p.project for p in visible]:
        if "custom_fields" in values: raise HTTPException(403,"Project write access required")
        selected=0
    project=await get(ctx,PROJECT,selected or visible[0].project) if selected or visible else None
    if "custom_fields" in values:
        if not project or await role(ctx,actor,project.id)!="full": raise HTTPException(403,"Project write access required")
        await custom_fields.apply_values(ctx,task,project,values.pop("custom_fields"))
    repeat=values.pop("repeat_period",val(TASK,task,"repeat_period") or "none")
    merged = db.parse_values(TASK, values, task)
    recurrence.validate_period(repeat, merged["due_date"])
    updates = {key:merged[key] for key in values}
    updates = await db.resolve_references(ctx,actor,TASK,updates,project,task)
    if repeat != (val(TASK,task,"repeat_period") or "none"): updates["repeat_period"]=repeat
    approvals.configure_edit(task,updates)
    was_done=bool(val(TASK,task,"completed"))
    old_due = val(TASK,task,"due_date")
    if updates.get("completed") and not val(TASK,task,"completed") and await dependencies.open_blockers(ctx,ident):
        raise HTTPException(409,"Cannot complete a task while a blocker is open")
    await edit(ctx,TASK,task,updates,"Save edited task fields")
    if "due_date" in updates and old_due != updates["due_date"]:
        await dependencies.propagate(ctx,task)
    if updates.get("completed") and not was_done: await recurrence.next_occurrence(ctx,actor,task)
    return {"location":task_path(ident)+(f"?project={selected}" if selected else "")}


@router.get("/api/crud/work_task/{project_id:int}/new")
async def new_task(project_id: int, identity: Identity = who):
    project = await require_project(identity.context, identity.actor, project_id, write=True)
    form = await record_form_data(TASK, identity, parent=project)
    recurrence.add_control(None, form, "full")
    return {"kind": "record", "title": "Create Task", "form": form, "collections": []}


@router.post("/crud/work_task/{ident:int}")
async def legacy_task_write(ident: int, identity: Identity = who):
    raise HTTPException(415, "Submit task edits as JSON to /api/crud/work_task/" + str(ident))


@router.post("/api/crud/work_task/{ident:int}")
async def save_task(ident: int, request: Request, identity: Identity = who):
    return await change(request, identity, "task-edit", ident)


@router.get("/api/crud/work_task/{ident:int}")
async def task_detail(ident: int, project: int | None = None, identity: Identity = who):
    ctx, actor = identity.context, identity.actor
    task = await get(ctx,TASK,ident)
    access = await task_role(ctx,actor,task)
    if not access: raise HTTPException(404,"Task not found")
    visible=await placements.visible(ctx,actor,task)
    if project not in [p.project for p in visible]: project=None
    selected=project or (visible[0].project if visible else None)
    project=await get(ctx,PROJECT,selected) if selected else None
    form=await record_form_data(TASK,identity,entity=task,parent=project)
    if access == "assignee":
        form["action"] = task_path(ident)
        for field in form["fields"]: field["readonly"] = field["name"] != "completed"
    assignee = val(TASK,task,"assignee")
    if assignee:
        person = await get(ctx,ACCOUNT,assignee)
        field = next(f for f in form["fields"] if f["name"]=="assignee")
        if all(option["id"]!=str(assignee) for option in field["options"]):
            field["options"].append({"id":str(assignee),"label":val(ACCOUNT,person,"display_name")})
    if val(TASK,task,"approval"):
        for field in form["fields"]:
            if field["name"]=="completed": field["readonly"]=True
    recurrence.add_control(task,form,access)
    if project: await custom_fields.add_to_form(ctx,task,project,form,await role(ctx,actor,selected))
    return {"kind":"record","title":val(TASK,task,"task_title"),"form":form,"collections":[],
            "task":{"id":ident,"occurrences":await recurrence.links(ctx,actor,task),"decision":approvals.label(task),"canDecide":access=="full" or val(TASK,task,"assignee")==actor.id,"access":access,"history":await activity.detail(ctx,actor,task),**await discussion.detail(ctx,actor,task),**await dependencies.detail(ctx,actor,task),**await placements.detail(ctx,actor,task,selected)}}


@router.post("/crud/work_task/{ident:int}/delete")
async def legacy_delete(ident: int, identity: Identity = who):
    raise HTTPException(415,"Use the JSON delete endpoint")


@router.post("/api/crud/work_task/{ident:int}/delete")
async def delete_task(ident: int, request: Request, identity: Identity = who):
    return await change(request,identity,"task-trash",ident)


@router.get("/api/deleted")
async def deleted(identity: Identity = who):
    return {"kind":"deleted","title":"Deleted tasks","items":await trash.listing(identity.context,identity.actor)}


@router.get("/api/inbox")
async def notifications(identity: Identity = who):
    items=await inbox.listing(identity.context,identity.actor)
    return {"kind":"inbox","title":"Inbox","items":items,"unread":sum(not n["read"] for n in items)}


@router.get("/inbox")
@router.get("/deleted")
@router.get("/my-tasks")
@router.get("/crud/work_project/{ident:int}")
@router.get("/crud/work_task/{ident:int}")
async def shell(request: Request):
    from fastapi.responses import HTMLResponse
    shell=browser_shell(request)
    selected=request.query_params.get("project")
    if shell and selected and selected.isdecimal():
        url="/api"+request.url.path
        return HTMLResponse(shell.body.decode().replace('"'+url+'"','"'+url+'?project='+str(int(selected))+'"'),
                            headers={"Cache-Control":"no-store","Vary":"Accept"})
    return shell or {"detail":"Open the page in a browser or use /api"}


@router.get("/api/my-tasks")
async def assigned_tasks(identity: Identity = who):
    ctx, actor = identity.context, identity.actor
    items = []
    for task in await find(ctx,TASK,assignee=actor.id):
        if not await task_role(ctx,actor,task): continue
        projects=[await get(ctx,PROJECT,p.project) for p in await placements.visible(ctx,actor,task)]
        items.append({"href":task_path(task.id),"label":val(TASK,task,"task_title"),
                      "project":", ".join(val(PROJECT,p,"project_name") for p in projects),"due":val(TASK,task,"due_date")})
    return {"kind":"tasks","title":"My Tasks","items":items}


sections.register(action)
custom_fields.register(action)
discussion.register(action)
dependencies.register(action)
placements.register(action)
approvals.register(action)
trash.register(action)
templates.register(action)
inbox.register(action)


def install(app):
    """Register the application routes before the generated generic CRUD routes."""
    if getattr(app.state, "work_management_installed", False):
        return
    observability.install(app)
    upgrade.install(app)
    trash.install_expiry(app)
    app.router.routes[0:0] = router.routes
    app.state.work_management_installed = True
