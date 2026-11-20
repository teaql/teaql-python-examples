"""Model-bound internal service example. No routes; missing actor/policy denies access."""
from Q import Q
from app.services.temporal import UNSET
from app.services.inputs import normalize
from app.services.contracts import field_input
from app.services.identity import policy_for, authorize, scoped_query, reference_query
from app.services.errors import ServiceError, NotFound, VersionConflict, AccessDenied


class WorkSubtaskService:
    entity_name = "work_subtask"

    @staticmethod
    def _values(raw, create):
        values = {}
        item = field_input("work_subtask", "work_space", raw.get("work_space", UNSET), operation="create" if create else "update")
        if item is not UNSET: values["work_space"] = item
        item = field_input("work_subtask", "task", raw.get("task", UNSET), operation="create" if create else "update")
        if item is not UNSET: values["task"] = item
        item = field_input("work_subtask", "subtask_title", raw.get("subtask_title", UNSET), operation="create" if create else "update")
        if item is not UNSET: values["subtask_title"] = item
        item = field_input("work_subtask", "assignee", raw.get("assignee", UNSET), operation="create" if create else "update")
        if item is not UNSET: values["assignee"] = item
        item = field_input("work_subtask", "due_date", raw.get("due_date", UNSET), operation="create" if create else "update")
        if item is not UNSET: values["due_date"] = item
        item = field_input("work_subtask", "completed", raw.get("completed", UNSET), operation="create" if create else "update")
        if item is not UNSET: values["completed"] = item
        return values

    @staticmethod
    async def _references(context, values, current=None):
        if "work_space" in values and values["work_space"] is not None:
            query = await reference_query(context, "work_subtask", "work_space", Q.work_spaces_minimal(), current)
            selected = await (query.with_id_is(values["work_space"]).comment("Validate the work_space reference")
                              .purpose("Enforce the application's candidate scope").execute_for_one(context))
            if selected is None: raise ServiceError("work_space is not an allowed reference")
            values["work_space"] = selected

        if "task" in values and values["task"] is not None:
            query = await reference_query(context, "work_subtask", "task", Q.work_tasks_minimal(), current)
            selected = await (query.with_id_is(values["task"]).comment("Validate the task reference")
                              .purpose("Enforce the application's candidate scope").execute_for_one(context))
            if selected is None: raise ServiceError("task is not an allowed reference")
            values["task"] = selected


        if "assignee" in values and values["assignee"] is not None:
            query = await reference_query(context, "work_subtask", "assignee", Q.work_accounts_minimal(), current)
            selected = await (query.whose_id_is(values["assignee"]).comment("Validate the assignee reference")
                              .purpose("Enforce the application's candidate scope").execute_for_one(context))
            if selected is None: raise ServiceError("assignee is not an allowed reference")
            values["assignee"] = selected



        return values

    @staticmethod
    async def _load(context, identifier, action):
        query = await scoped_query(context, "work_subtask", action, Q.work_subtasks())
        identifier = normalize(identifier, field="id", kind="reference")
        record = await (query.with_id_is(identifier).comment("Load work_subtask for an authorized action")
                        .purpose("Execute a policy-scoped service operation").execute_for_one(context))
        if record is None: raise NotFound("work_subtask was not found in the permitted scope")
        return record

    @staticmethod
    async def get(context, identifier):
        record = await WorkSubtaskService._load(context, identifier, "read")
        await authorize(context, "work_subtask", "read", record)
        return record

    @staticmethod
    async def list(context, *, offset=0, limit=100):
        await authorize(context, "work_subtask", "list")
        offset = normalize(offset, field="offset", kind="integer")
        limit = normalize(limit, field="limit", kind="integer")
        if not (offset >= 0 and limit in range(1, 1001)): raise ServiceError("Invalid page bounds")
        query = await scoped_query(context, "work_subtask", "list", Q.work_subtasks())
        rows = await (query.order_by_id_ascending().offset(offset).limit(limit)
                      .comment("Read a policy-scoped page of work_subtask")
                      .purpose("List authorized service records").execute_for_list(context))
        visible = []
        for record in rows:
            try: await authorize(context, "work_subtask", "read", record)
            except AccessDenied: continue
            visible.append(record)
        return visible

    @staticmethod
    async def create(context, *, audit_reason,
        value_work_space=UNSET,value_task=UNSET,value_subtask_title=UNSET,value_assignee=UNSET,value_due_date=UNSET,value_completed=UNSET,    ):
        policy_for(context)
        if not isinstance(audit_reason, str) or not audit_reason.strip(): raise ServiceError("An audit reason is required")
        values = WorkSubtaskService._values({"work_space": value_work_space, "task": value_task, "subtask_title": value_subtask_title, "assignee": value_assignee, "due_date": value_due_date, "completed": value_completed}, True)
        await authorize(context, "work_subtask", "create", changes=values)
        values = await WorkSubtaskService._references(context, values)
        record = (Q.work_subtasks().comment("Initialize work_subtask through its generated factory")
                  .purpose("Prepare an authorized service creation").new_entity(context))
        if "work_space" in values: record.update_work_space(values["work_space"])
        if "task" in values: record.update_task(values["task"])
        if "subtask_title" in values: record.update_subtask_title(values["subtask_title"])
        if "assignee" in values: record.update_assignee(values["assignee"])
        if "due_date" in values: record.update_due_date(values["due_date"])
        if "completed" in values: record.update_completed(values["completed"])
        await record.audit_as(audit_reason).save(context)
        return record

    @staticmethod
    async def update(context, identifier, *, expected_version, audit_reason,
        value_work_space=UNSET,value_task=UNSET,value_subtask_title=UNSET,value_assignee=UNSET,value_due_date=UNSET,value_completed=UNSET,    ):
        record = await WorkSubtaskService._load(context, identifier, "update")
        if not isinstance(audit_reason, str) or not audit_reason.strip(): raise ServiceError("An audit reason is required")
        values = WorkSubtaskService._values({"work_space": value_work_space, "task": value_task, "subtask_title": value_subtask_title, "assignee": value_assignee, "due_date": value_due_date, "completed": value_completed}, False)
        await authorize(context, "work_subtask", "update", record, values)
        version = normalize(expected_version, field="expected_version", kind="integer")
        if record.version != version: raise VersionConflict("Reload the record before applying a stale edit")
        values = await WorkSubtaskService._references(context, values, record)
        if "work_space" in values: record.update_work_space(values["work_space"])
        if "task" in values: record.update_task(values["task"])
        if "subtask_title" in values: record.update_subtask_title(values["subtask_title"])
        if "assignee" in values: record.update_assignee(values["assignee"])
        if "due_date" in values: record.update_due_date(values["due_date"])
        if "completed" in values: record.update_completed(values["completed"])
        await record.audit_as(audit_reason).save(context)
        return record

    @staticmethod
    async def delete(context, identifier, *, expected_version, audit_reason):
        record = await WorkSubtaskService._load(context, identifier, "delete")
        await authorize(context, "work_subtask", "delete", record)
        version = normalize(expected_version, field="expected_version", kind="integer")
        if record.version != version: raise VersionConflict("Reload the record before deleting a stale version")
        if not isinstance(audit_reason, str) or not audit_reason.strip(): raise ServiceError("An audit reason is required")
        await record.mark_for_deletion().audit_as(audit_reason).save(context)