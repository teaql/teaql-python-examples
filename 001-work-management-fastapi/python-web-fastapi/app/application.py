"""MVP business rules registered with the generated FastAPI CRUD adapter."""
from . import feature_commands as records
from .feature_bindings import BY_IDS, FILTERS, MATCHERS, QUERIES

PROJECT = "work_project"
TASK = "work_task"
ACCOUNT = "work_account"
MEMBERSHIP = "project_membership"
SECTION = "project_section"


from .work_data import find, project_scope, project_action, task_scope, task_action


async def project_accounts(context, actor, parent, current):
    from .placements import visible, all_for
    if current is not None and not await all_for(context,current):
        return QUERIES[ACCOUNT]()
    pids=[p.project for p in await visible(context,actor,current)] if current else [parent.id]
    accounts=set()
    for pid in pids:
        members=await find(context, MEMBERSHIP, project=pid)
        accounts.update(records.identifier(records.value(MEMBERSHIP,m,"member_account")) for m in members)
    return BY_IDS[ACCOUNT](QUERIES[ACCOUNT](),sorted(accounts))


def project_sections(context, actor, parent, current):
    return FILTERS[SECTION]["project"](QUERIES[SECTION](), parent.id)


async def initialize_project(context, actor, parent, values):
    project = await records.prepare(context, PROJECT, None, {**values, "owner_account": actor, "shift_dates": False})
    await project.audit_as("Create the project").save(context)
    membership = await records.prepare(context, MEMBERSHIP, project, {"member_account": actor, "access_role":"full"})
    await membership.audit_as("Enroll the project creator").save(context)
    section = await records.prepare(context, SECTION, project, {"section_name": "Tasks", "default_section": True, "section_order": 0})
    await section.audit_as("Create the project's default section").save(context)
    return {"id": project.id, "membership_id": membership.id, "section_id": section.id}


async def verify_project(context, actor, parent, result):
    membership = await records.read_one(context, MEMBERSHIP, result["membership_id"])
    section = await records.read_one(context, SECTION, result["section_id"])
    return (membership is not None
            and records.identifier(records.value(MEMBERSHIP, membership, "project")) == result["id"]
            and records.identifier(records.value(MEMBERSHIP, membership, "member_account")) == actor.id
            and section is not None
            and records.identifier(records.value(SECTION, section, "project")) == result["id"]
            and records.value(SECTION, section, "default_section") is True)


async def place_task(context, actor, parent, values):
    sections = await records.related(context, SECTION, "project", parent.id)
    defaults = [section for section in sections if records.value(SECTION, section, "default_section")]
    if len(defaults) != 1:
        raise ValueError("The project needs one explicitly designated default section")
    task = await create_in_section(context, actor, parent, defaults[0], values)
    if values.get("completed"):
        from .recurrence import next_occurrence
        await next_occurrence(context, actor, task)
    return {"id": task.id}


async def create_in_section(context,actor,parent,section,values):
    from .placements import in_scope
    from .recurrence import validate_period
    validate_period(values.get("repeat_period") or "none", values.get("due_date"))
    siblings=await in_scope(context,"section",section.id)
    position=max((e.position for e in siblings),default=-1)+1
    if values.get("approval") and values.get("completed"):
        raise ValueError("A new approval starts pending")
    task = await records.prepare(context, TASK, parent, {**values, "created_by":actor, "primary_detached":False, "section": section, "task_order": position})
    await task.audit_as("Create a task in a project section").save(context)
    from .activity import emit
    await emit(context,task,"work_task_add","Task created",None,values["task_title"])
    return task


def configure(registry):
    registry.policy("project_access", scope=project_scope, allows=project_action)
    registry.policy("task_access", scope=task_scope, allows=task_action)
    registry.candidates("project_accounts", target=ACCOUNT, query=project_accounts)
    registry.candidates("project_sections", target=SECTION, query=project_sections)
    registry.creation("initialize_project", handler=initialize_project, validate=verify_project, version="1")
    registry.creation("place_task", handler=place_task, version="1")

    # The generated server calls this hook after creating its FastAPI instance.
    from .feature_policy import REGISTRY

    if registry is REGISTRY:
        from . import main, product

        product.install(main.app)
