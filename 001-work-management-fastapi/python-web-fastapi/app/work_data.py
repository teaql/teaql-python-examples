"""Trusted project data access shared by policies and application commands."""
from fastapi import HTTPException
from . import feature_commands as db
from .feature_bindings import BY_IDS, FILTERS, MATCHERS, QUERIES, UPDATERS

PROJECT = "work_project"
TASK = "work_task"
ACCOUNT = "work_account"
MEMBER = "project_membership"
SECTION = "project_section"


def val(name, row, field):
    return db.identifier(db.value(name, row, field))


def is_trashed(task):
    return val(TASK, task, "deleted_epoch") is not None


async def rows(ctx, query, why):
    page_size = 512
    query.order_by_id_ascending().limit(page_size)
    result = []
    while True:
        page = await (query.offset(len(result)).comment(why).purpose("Serve the workspace workflow")
                      .execute_for_list(ctx))
        result.extend(page)
        if len(page) < page_size:
            return result


async def get(ctx, name, ident):
    row = await db.read_one(ctx, name, ident)
    if row is None or name==TASK and is_trashed(row):
        raise HTTPException(404, "Record not found")
    return row


async def find(ctx, name, **where):
    query = QUERIES[name]()
    for key, value in where.items():
        query = FILTERS[name][key](query, value)
    return await rows(ctx, query, "Read related " + name)


async def create(ctx, name, parent, values, reason):
    row = await db.prepare(ctx, name, parent, values)
    await row.audit_as(reason).save(ctx)
    from .activity import track
    await track(ctx,name,row,"add",values,{},reason)
    return row


async def edit(ctx, name, row, values, reason):
    before={key:val(name,row,key) for key in values}
    for key, value in values.items():
        UPDATERS[name][key](row, value)
    if values:
        await row.audit_as(reason).save(ctx)
        from .activity import track
        await track(ctx,name,row,"edit",values,before,reason)
    return row


async def remove(ctx, name, row, reason):
    from .activity import track
    await track(ctx, name, row, "remove", {}, {}, reason)
    await row.mark_for_deletion().audit_as(reason).save(ctx)


async def member_rows(ctx, actor):
    return await find(ctx, MEMBER, member_account=actor.id)


async def project_ids(ctx, actor):
    return [val(MEMBER, row, "project") for row in await member_rows(ctx, actor)]


async def role(ctx, actor, project_id):
    links = await find(ctx, MEMBER, project=project_id, member_account=actor.id)
    if not links: return None
    return val(MEMBER,links[0],"access_role") or "full"


async def task_role(ctx, actor, task):
    if is_trashed(task): return None
    from .placements import all_for,can_open_orphan
    places=await all_for(ctx,task)
    if not places:
        return "full" if await can_open_orphan(ctx,actor,task) else None
    roles=[await role(ctx,actor,p.project) for p in places]
    if "full" in roles: return "full"
    if "comment" in roles: return "comment"
    return "assignee" if val(TASK,task,"assignee")==actor.id else None


async def project_scope(ctx, actor, action, query, parent):
    return BY_IDS[PROJECT](query, await project_ids(ctx, actor))


async def project_action(ctx, actor, action, entity, parent):
    if action in ("list", "create"): return True
    return action == "read" and entity is not None and bool(await role(ctx, actor, entity.id))


async def task_scope(ctx, actor, action, query, parent):
    from .placements import in_scope
    if parent is not None:
        ids=[e.task.id for e in await in_scope(ctx,"project",parent.id)]
    else:
        ids=set()
        for pid in await project_ids(ctx,actor):
            ids.update(e.task.id for e in await in_scope(ctx,"project",pid))
        for key in ("assignee","created_by"):
            ids.update(t.id for t in await find(ctx,TASK,**{key:actor.id}))
        ids.update(val("task_participant",c,"task") for c in await find(ctx,"task_participant",participant=actor.id))
        ids.update(val("task_comment",c,"task") for c in await find(ctx,"task_comment",author=actor.id))
    return BY_IDS[TASK](query, sorted(ids))


async def task_action(ctx, actor, action, entity, parent):
    if entity is None:
        access = await role(ctx, actor, parent.id) if parent else None
        return bool(access) if action == "list" else action == "create" and access == "full"
    access = await task_role(ctx, actor, entity)
    return bool(access) if action == "read" else action in ("update", "delete") and access == "full"


def task_path(task_id):
    return "/crud/work_task/" + str(task_id)


def project_path(project_id):
    return "/crud/work_project/" + str(project_id)


async def require_project(ctx, actor, project_id, *, write=False):
    access = await role(ctx, actor, project_id)
    if not access: raise HTTPException(404, "Project not found")
    if write and access != "full": raise HTTPException(403, "Full membership is required")
    return await get(ctx, PROJECT, project_id)




async def by_ids(ctx, name, ids):
    """Read a known set with bounded parameter counts and return it indexed by id."""
    ordered = sorted(set(ids))
    result = {}
    for offset in range(0, len(ordered), 400):
        query = BY_IDS[name](QUERIES[name](), ordered[offset:offset + 400])
        result.update((item.id, item) for item in await rows(ctx, query, "Read selected " + name))
    return result


async def visible_task_set(ctx, actor, tasks, projects):
    """Resolve the same read rules as task_role for a batch in a single request."""
    active = {t.id: t for t in tasks if not is_trashed(t)}
    if not active:
        return set()

    from .placements import PLACEMENT
    homes = {tid: set() if val(TASK, task, "primary_detached") else {val(TASK, task, "project")}
             for tid, task in active.items()}
    ids = list(active)
    for offset in range(0, len(ids), 400):
        tasks_query = BY_IDS[TASK](QUERIES[TASK](), ids[offset:offset + 400])
        links = MATCHERS[PLACEMENT]["task"](QUERIES[PLACEMENT](), tasks_query)
        for link in await rows(ctx, links, "Resolve project placements for visible tasks"):
            homes[val(PLACEMENT, link, "task")].add(val(PLACEMENT, link, "project"))

    visible = {tid for tid, t in active.items()
               if homes[tid] & projects or val(TASK, t, "assignee") == actor.id
               or (not homes[tid] and val(TASK, t, "created_by") == actor.id)}
    orphans = {tid for tid in active if tid not in visible and not homes[tid]}
    if orphans:
        for entity, person_field in (("task_participant", "participant"), ("task_comment", "author")):
            participants = await find(ctx, entity, **{person_field: actor.id})
            visible.update(orphans & {val(entity, row, "task") for row in participants})
    return visible
