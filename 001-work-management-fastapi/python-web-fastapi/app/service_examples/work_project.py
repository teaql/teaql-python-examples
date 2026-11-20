"""Model-bound internal service example. No routes; missing actor/policy denies access."""
from Q import Q
from app.services.temporal import UNSET
from app.services.inputs import normalize
from app.services.contracts import field_input
from app.services.identity import policy_for, authorize, scoped_query, reference_query
from app.services.errors import ServiceError, NotFound, VersionConflict, AccessDenied


class WorkProjectService:
    entity_name = "work_project"

    @staticmethod
    def _values(raw, create):
        values = {}
        item = field_input("work_project", "work_space", raw.get("work_space", UNSET), operation="create" if create else "update")
        if item is not UNSET: values["work_space"] = item
        item = field_input("work_project", "owner_account", raw.get("owner_account", UNSET), operation="create" if create else "update")
        if item is not UNSET: values["owner_account"] = item
        item = field_input("work_project", "project_name", raw.get("project_name", UNSET), operation="create" if create else "update")
        if item is not UNSET: values["project_name"] = item
        item = field_input("work_project", "shift_dates", raw.get("shift_dates", UNSET), operation="create" if create else "update")
        if item is not UNSET: values["shift_dates"] = item
        return values

    @staticmethod
    async def _references(context, values, current=None):
        if "work_space" in values and values["work_space"] is not None:
            query = await reference_query(context, "work_project", "work_space", Q.work_spaces_minimal(), current)
            selected = await (query.with_id_is(values["work_space"]).comment("Validate the work_space reference")
                              .purpose("Enforce the application's candidate scope").execute_for_one(context))
            if selected is None: raise ServiceError("work_space is not an allowed reference")
            values["work_space"] = selected

        if "owner_account" in values and values["owner_account"] is not None:
            query = await reference_query(context, "work_project", "owner_account", Q.work_accounts_minimal(), current)
            selected = await (query.whose_id_is(values["owner_account"]).comment("Validate the owner_account reference")
                              .purpose("Enforce the application's candidate scope").execute_for_one(context))
            if selected is None: raise ServiceError("owner_account is not an allowed reference")
            values["owner_account"] = selected



        return values

    @staticmethod
    async def _load(context, identifier, action):
        query = await scoped_query(context, "work_project", action, Q.work_projects())
        identifier = normalize(identifier, field="id", kind="reference")
        record = await (query.with_id_is(identifier).comment("Load work_project for an authorized action")
                        .purpose("Execute a policy-scoped service operation").execute_for_one(context))
        if record is None: raise NotFound("work_project was not found in the permitted scope")
        return record

    @staticmethod
    async def get(context, identifier):
        record = await WorkProjectService._load(context, identifier, "read")
        await authorize(context, "work_project", "read", record)
        return record

    @staticmethod
    async def list(context, *, offset=0, limit=100):
        await authorize(context, "work_project", "list")
        offset = normalize(offset, field="offset", kind="integer")
        limit = normalize(limit, field="limit", kind="integer")
        if not (offset >= 0 and limit in range(1, 1001)): raise ServiceError("Invalid page bounds")
        query = await scoped_query(context, "work_project", "list", Q.work_projects())
        rows = await (query.order_by_id_ascending().offset(offset).limit(limit)
                      .comment("Read a policy-scoped page of work_project")
                      .purpose("List authorized service records").execute_for_list(context))
        visible = []
        for record in rows:
            try: await authorize(context, "work_project", "read", record)
            except AccessDenied: continue
            visible.append(record)
        return visible

    @staticmethod
    async def create(context, *, audit_reason,
        value_work_space=UNSET,value_owner_account=UNSET,value_project_name=UNSET,value_shift_dates=UNSET,    ):
        policy_for(context)
        if not isinstance(audit_reason, str) or not audit_reason.strip(): raise ServiceError("An audit reason is required")
        values = WorkProjectService._values({"work_space": value_work_space, "owner_account": value_owner_account, "project_name": value_project_name, "shift_dates": value_shift_dates}, True)
        await authorize(context, "work_project", "create", changes=values)
        values = await WorkProjectService._references(context, values)
        record = (Q.work_projects().comment("Initialize work_project through its generated factory")
                  .purpose("Prepare an authorized service creation").new_entity(context))
        if "work_space" in values: record.update_work_space(values["work_space"])
        if "owner_account" in values: record.update_owner_account(values["owner_account"])
        if "project_name" in values: record.update_project_name(values["project_name"])
        if "shift_dates" in values: record.update_shift_dates(values["shift_dates"])
        await record.audit_as(audit_reason).save(context)
        return record

    @staticmethod
    async def update(context, identifier, *, expected_version, audit_reason,
        value_work_space=UNSET,value_owner_account=UNSET,value_project_name=UNSET,value_shift_dates=UNSET,    ):
        record = await WorkProjectService._load(context, identifier, "update")
        if not isinstance(audit_reason, str) or not audit_reason.strip(): raise ServiceError("An audit reason is required")
        values = WorkProjectService._values({"work_space": value_work_space, "owner_account": value_owner_account, "project_name": value_project_name, "shift_dates": value_shift_dates}, False)
        await authorize(context, "work_project", "update", record, values)
        version = normalize(expected_version, field="expected_version", kind="integer")
        if record.version != version: raise VersionConflict("Reload the record before applying a stale edit")
        values = await WorkProjectService._references(context, values, record)
        if "work_space" in values: record.update_work_space(values["work_space"])
        if "owner_account" in values: record.update_owner_account(values["owner_account"])
        if "project_name" in values: record.update_project_name(values["project_name"])
        if "shift_dates" in values: record.update_shift_dates(values["shift_dates"])
        await record.audit_as(audit_reason).save(context)
        return record

    @staticmethod
    async def delete(context, identifier, *, expected_version, audit_reason):
        record = await WorkProjectService._load(context, identifier, "delete")
        await authorize(context, "work_project", "delete", record)
        version = normalize(expected_version, field="expected_version", kind="integer")
        if record.version != version: raise VersionConflict("Reload the record before deleting a stale version")
        if not isinstance(audit_reason, str) or not audit_reason.strip(): raise ServiceError("An audit reason is required")
        await record.mark_for_deletion().audit_as(audit_reason).save(context)