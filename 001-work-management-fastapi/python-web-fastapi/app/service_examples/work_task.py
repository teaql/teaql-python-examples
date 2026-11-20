"""Model-bound internal service example. No routes; missing actor/policy denies access."""
from Q import Q
from app.services.temporal import UNSET
from app.services.inputs import normalize
from app.services.contracts import field_input
from app.services.identity import policy_for, authorize, scoped_query, reference_query
from app.services.errors import ServiceError, NotFound, VersionConflict, AccessDenied


class WorkTaskService:
    entity_name = "work_task"

    @staticmethod
    def _values(raw, create):
        values = {}
        item = field_input("work_task", "work_space", raw.get("work_space", UNSET), operation="create" if create else "update")
        if item is not UNSET: values["work_space"] = item
        item = field_input("work_task", "project", raw.get("project", UNSET), operation="create" if create else "update")
        if item is not UNSET: values["project"] = item
        item = field_input("work_task", "section", raw.get("section", UNSET), operation="create" if create else "update")
        if item is not UNSET: values["section"] = item
        item = field_input("work_task", "task_order", raw.get("task_order", UNSET), operation="create" if create else "update")
        if item is not UNSET: values["task_order"] = item
        item = field_input("work_task", "task_title", raw.get("task_title", UNSET), operation="create" if create else "update")
        if item is not UNSET: values["task_title"] = item
        item = field_input("work_task", "description", raw.get("description", UNSET), operation="create" if create else "update")
        if item is not UNSET: values["description"] = item
        item = field_input("work_task", "assignee", raw.get("assignee", UNSET), operation="create" if create else "update")
        if item is not UNSET: values["assignee"] = item
        item = field_input("work_task", "start_date", raw.get("start_date", UNSET), operation="create" if create else "update")
        if item is not UNSET: values["start_date"] = item
        item = field_input("work_task", "due_date", raw.get("due_date", UNSET), operation="create" if create else "update")
        if item is not UNSET: values["due_date"] = item
        item = field_input("work_task", "completed", raw.get("completed", UNSET), operation="create" if create else "update")
        if item is not UNSET: values["completed"] = item
        return values

    @staticmethod
    async def _references(context, values, current=None):
        if "work_space" in values and values["work_space"] is not None:
            query = await reference_query(context, "work_task", "work_space", Q.work_spaces_minimal(), current)
            selected = await (query.with_id_is(values["work_space"]).comment("Validate the work_space reference")
                              .purpose("Enforce the application's candidate scope").execute_for_one(context))
            if selected is None: raise ServiceError("work_space is not an allowed reference")
            values["work_space"] = selected

        if "project" in values and values["project"] is not None:
            query = await reference_query(context, "work_task", "project", Q.work_projects_minimal(), current)
            selected = await (query.with_id_is(values["project"]).comment("Validate the project reference")
                              .purpose("Enforce the application's candidate scope").execute_for_one(context))
            if selected is None: raise ServiceError("project is not an allowed reference")
            values["project"] = selected

        if "section" in values and values["section"] is not None:
            query = await reference_query(context, "work_task", "section", Q.project_sections_minimal(), current)
            selected = await (query.with_id_is(values["section"]).comment("Validate the section reference")
                              .purpose("Enforce the application's candidate scope").execute_for_one(context))
            if selected is None: raise ServiceError("section is not an allowed reference")
            values["section"] = selected




        if "assignee" in values and values["assignee"] is not None:
            query = await reference_query(context, "work_task", "assignee", Q.work_accounts_minimal(), current)
            selected = await (query.whose_id_is(values["assignee"]).comment("Validate the assignee reference")
                              .purpose("Enforce the application's candidate scope").execute_for_one(context))
            if selected is None: raise ServiceError("assignee is not an allowed reference")
            values["assignee"] = selected




        return values

    @staticmethod
    async def _load(context, identifier, action):
        query = await scoped_query(context, "work_task", action, Q.work_tasks())
        identifier = normalize(identifier, field="id", kind="reference")
        record = await (query.with_id_is(identifier).comment("Load work_task for an authorized action")
                        .purpose("Execute a policy-scoped service operation").execute_for_one(context))
        if record is None: raise NotFound("work_task was not found in the permitted scope")
        return record

    @staticmethod
    async def get(context, identifier):
        record = await WorkTaskService._load(context, identifier, "read")
        await authorize(context, "work_task", "read", record)
        return record

    @staticmethod
    async def list(context, *, offset=0, limit=100):
        await authorize(context, "work_task", "list")
        offset = normalize(offset, field="offset", kind="integer")
        limit = normalize(limit, field="limit", kind="integer")
        if not (offset >= 0 and limit in range(1, 1001)): raise ServiceError("Invalid page bounds")
        query = await scoped_query(context, "work_task", "list", Q.work_tasks())
        rows = await (query.order_by_id_ascending().offset(offset).limit(limit)
                      .comment("Read a policy-scoped page of work_task")
                      .purpose("List authorized service records").execute_for_list(context))
        visible = []
        for record in rows:
            try: await authorize(context, "work_task", "read", record)
            except AccessDenied: continue
            visible.append(record)
        return visible

    @staticmethod
    async def create(context, *, audit_reason,
        value_work_space=UNSET,value_project=UNSET,value_section=UNSET,value_task_order=UNSET,value_task_title=UNSET,value_description=UNSET,value_assignee=UNSET,value_start_date=UNSET,value_due_date=UNSET,value_completed=UNSET,    ):
        policy_for(context)
        if not isinstance(audit_reason, str) or not audit_reason.strip(): raise ServiceError("An audit reason is required")
        values = WorkTaskService._values({"work_space": value_work_space, "project": value_project, "section": value_section, "task_order": value_task_order, "task_title": value_task_title, "description": value_description, "assignee": value_assignee, "start_date": value_start_date, "due_date": value_due_date, "completed": value_completed}, True)
        await authorize(context, "work_task", "create", changes=values)
        values = await WorkTaskService._references(context, values)
        record = (Q.work_tasks().comment("Initialize work_task through its generated factory")
                  .purpose("Prepare an authorized service creation").new_entity(context))
        if "work_space" in values: record.update_work_space(values["work_space"])
        if "project" in values: record.update_project(values["project"])
        if "section" in values: record.update_section(values["section"])
        if "task_order" in values: record.update_task_order(values["task_order"])
        if "task_title" in values: record.update_task_title(values["task_title"])
        if "description" in values: record.update_description(values["description"])
        if "assignee" in values: record.update_assignee(values["assignee"])
        if "start_date" in values: record.update_start_date(values["start_date"])
        if "due_date" in values: record.update_due_date(values["due_date"])
        if "completed" in values: record.update_completed(values["completed"])
        await record.audit_as(audit_reason).save(context)
        return record

    @staticmethod
    async def update(context, identifier, *, expected_version, audit_reason,
        value_work_space=UNSET,value_project=UNSET,value_section=UNSET,value_task_order=UNSET,value_task_title=UNSET,value_description=UNSET,value_assignee=UNSET,value_start_date=UNSET,value_due_date=UNSET,value_completed=UNSET,    ):
        record = await WorkTaskService._load(context, identifier, "update")
        if not isinstance(audit_reason, str) or not audit_reason.strip(): raise ServiceError("An audit reason is required")
        values = WorkTaskService._values({"work_space": value_work_space, "project": value_project, "section": value_section, "task_order": value_task_order, "task_title": value_task_title, "description": value_description, "assignee": value_assignee, "start_date": value_start_date, "due_date": value_due_date, "completed": value_completed}, False)
        await authorize(context, "work_task", "update", record, values)
        version = normalize(expected_version, field="expected_version", kind="integer")
        if record.version != version: raise VersionConflict("Reload the record before applying a stale edit")
        values = await WorkTaskService._references(context, values, record)
        if "work_space" in values: record.update_work_space(values["work_space"])
        if "project" in values: record.update_project(values["project"])
        if "section" in values: record.update_section(values["section"])
        if "task_order" in values: record.update_task_order(values["task_order"])
        if "task_title" in values: record.update_task_title(values["task_title"])
        if "description" in values: record.update_description(values["description"])
        if "assignee" in values: record.update_assignee(values["assignee"])
        if "start_date" in values: record.update_start_date(values["start_date"])
        if "due_date" in values: record.update_due_date(values["due_date"])
        if "completed" in values: record.update_completed(values["completed"])
        await record.audit_as(audit_reason).save(context)
        return record

    @staticmethod
    async def delete(context, identifier, *, expected_version, audit_reason):
        record = await WorkTaskService._load(context, identifier, "delete")
        await authorize(context, "work_task", "delete", record)
        version = normalize(expected_version, field="expected_version", kind="integer")
        if record.version != version: raise VersionConflict("Reload the record before deleting a stale version")
        if not isinstance(audit_reason, str) or not audit_reason.strip(): raise ServiceError("An audit reason is required")
        await record.mark_for_deletion().audit_as(audit_reason).save(context)