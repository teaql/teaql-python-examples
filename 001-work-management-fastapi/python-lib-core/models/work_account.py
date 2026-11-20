from teaql.core.mutation import InsertCommand, UpdateCommand, DeleteCommand, MutationRequest
from teaql.core.value import Value
from teaql.runtime import CheckException, CheckResult, EntityKey, EntityRoot, ObjectLocation
import itertools
from models.work_space import WorkSpace


class WorkAccount:
    _teaql_temporary_ids = itertools.count(1)

    def __setattr__(self, name, value):
        if not name.startswith("_"):
            raise AttributeError("Entity fields are read-only; use the generated update_*() methods")
        object.__setattr__(self, name, value)

    def __delattr__(self, name):
        if not name.startswith("_"):
            raise AttributeError("Entity fields cannot be deleted; use the generated update_*() methods")
        object.__delattr__(self, name)

    @classmethod
    def refer(cls, entity_id):
        return cls._teaql_construct(id=entity_id)

    @classmethod
    def _teaql_new_with_fixed_id(cls, entity_id):
        """Generated bootstrap capability; application code must not call it."""
        return cls._teaql_construct(id=entity_id)._teaql_force_create()

    def _teaql_force_create(self):
        self._action = "Create"
        self._entity_root.mark_as_new(self._teaql_entity_key())
        return self

    def __init__(self, **kwargs):
        raise TypeError("Entity constructors are internal; use Q.work_accounts().comment('what').purpose('why').new_entity(context)")

    @classmethod
    def _teaql_construct(cls, **kwargs):
        """Internal construction for generated requests, hydration and bootstrap."""
        entity = object.__new__(cls)
        entity._teaql_initialize(**kwargs)
        return entity

    def _teaql_initialize(self, **kwargs):
        self._entity_root = kwargs.pop("_entity_root", None) or EntityRoot()
        if "id" in kwargs and "id" not in kwargs:
            kwargs["id"] = kwargs.pop("id")
        if "work_space" in kwargs and "workSpace" not in kwargs:
            kwargs["workSpace"] = kwargs.pop("work_space")
        if "display_name" in kwargs and "displayName" not in kwargs:
            kwargs["displayName"] = kwargs.pop("display_name")
        if "email_address" in kwargs and "emailAddress" not in kwargs:
            kwargs["emailAddress"] = kwargs.pop("email_address")
        if "password_hash" in kwargs and "passwordHash" not in kwargs:
            kwargs["passwordHash"] = kwargs.pop("password_hash")
        if "version" in kwargs and "version" not in kwargs:
            kwargs["version"] = kwargs.pop("version")
        self._action = "Update" if kwargs.get("id") else "Create"
        self._comment = None
        self._loaded_fields = set(kwargs.keys())
        object.__setattr__(self, "id", kwargs.get("id"))

        object.__setattr__(self, "workSpace", kwargs.get("workSpace"))

        object.__setattr__(self, "displayName", kwargs.get("displayName"))

        object.__setattr__(self, "emailAddress", kwargs.get("emailAddress"))

        object.__setattr__(self, "passwordHash", kwargs.get("passwordHash"))

        object.__setattr__(self, "version", kwargs.get("version"))

        if isinstance(self.workSpace, dict):
            object.__setattr__(self, "workSpace", WorkSpace._teaql_construct(**self.workSpace))
        self._work_project_list = kwargs.get("work_project_list", [])
        if "work_project_list" in kwargs or kwargs.get("id") is None:
            self._loaded_fields.add("work_project_list")
        self._project_membership_list = kwargs.get("project_membership_list", [])
        if "project_membership_list" in kwargs or kwargs.get("id") is None:
            self._loaded_fields.add("project_membership_list")
        self._work_task_list_as_created_by = kwargs.get("work_task_list_as_created_by", [])
        if "work_task_list_as_created_by" in kwargs or kwargs.get("id") is None:
            self._loaded_fields.add("work_task_list_as_created_by")
        self._work_task_list_as_assignee = kwargs.get("work_task_list_as_assignee", [])
        if "work_task_list_as_assignee" in kwargs or kwargs.get("id") is None:
            self._loaded_fields.add("work_task_list_as_assignee")
        self._work_subtask_list = kwargs.get("work_subtask_list", [])
        if "work_subtask_list" in kwargs or kwargs.get("id") is None:
            self._loaded_fields.add("work_subtask_list")
        self._task_comment_list = kwargs.get("task_comment_list", [])
        if "task_comment_list" in kwargs or kwargs.get("id") is None:
            self._loaded_fields.add("task_comment_list")
        self._task_event_list = kwargs.get("task_event_list", [])
        if "task_event_list" in kwargs or kwargs.get("id") is None:
            self._loaded_fields.add("task_event_list")
        self._task_participant_list = kwargs.get("task_participant_list", [])
        if "task_participant_list" in kwargs or kwargs.get("id") is None:
            self._loaded_fields.add("task_participant_list")
        self._deleted_task_viewer_list = kwargs.get("deleted_task_viewer_list", [])
        if "deleted_task_viewer_list" in kwargs or kwargs.get("id") is None:
            self._loaded_fields.add("deleted_task_viewer_list")
        self._task_blueprint_list = kwargs.get("task_blueprint_list", [])
        if "task_blueprint_list" in kwargs or kwargs.get("id") is None:
            self._loaded_fields.add("task_blueprint_list")
        self._blueprint_subtask_list = kwargs.get("blueprint_subtask_list", [])
        if "blueprint_subtask_list" in kwargs or kwargs.get("id") is None:
            self._loaded_fields.add("blueprint_subtask_list")
        self._inbox_notice_list = kwargs.get("inbox_notice_list", [])
        if "inbox_notice_list" in kwargs or kwargs.get("id") is None:
            self._loaded_fields.add("inbox_notice_list")
        if self._work_project_list:
            from models.work_project import WorkProject
            self._work_project_list = [
                item if isinstance(item, WorkProject) else WorkProject._teaql_construct(**item)
                for item in self._work_project_list
            ]
        if self._project_membership_list:
            from models.project_membership import ProjectMembership
            self._project_membership_list = [
                item if isinstance(item, ProjectMembership) else ProjectMembership._teaql_construct(**item)
                for item in self._project_membership_list
            ]
        if self._work_task_list_as_created_by:
            from models.work_task import WorkTask
            self._work_task_list_as_created_by = [
                item if isinstance(item, WorkTask) else WorkTask._teaql_construct(**item)
                for item in self._work_task_list_as_created_by
            ]
        if self._work_task_list_as_assignee:
            from models.work_task import WorkTask
            self._work_task_list_as_assignee = [
                item if isinstance(item, WorkTask) else WorkTask._teaql_construct(**item)
                for item in self._work_task_list_as_assignee
            ]
        if self._work_subtask_list:
            from models.work_subtask import WorkSubtask
            self._work_subtask_list = [
                item if isinstance(item, WorkSubtask) else WorkSubtask._teaql_construct(**item)
                for item in self._work_subtask_list
            ]
        if self._task_comment_list:
            from models.task_comment import TaskComment
            self._task_comment_list = [
                item if isinstance(item, TaskComment) else TaskComment._teaql_construct(**item)
                for item in self._task_comment_list
            ]
        if self._task_event_list:
            from models.task_event import TaskEvent
            self._task_event_list = [
                item if isinstance(item, TaskEvent) else TaskEvent._teaql_construct(**item)
                for item in self._task_event_list
            ]
        if self._task_participant_list:
            from models.task_participant import TaskParticipant
            self._task_participant_list = [
                item if isinstance(item, TaskParticipant) else TaskParticipant._teaql_construct(**item)
                for item in self._task_participant_list
            ]
        if self._deleted_task_viewer_list:
            from models.deleted_task_viewer import DeletedTaskViewer
            self._deleted_task_viewer_list = [
                item if isinstance(item, DeletedTaskViewer) else DeletedTaskViewer._teaql_construct(**item)
                for item in self._deleted_task_viewer_list
            ]
        if self._task_blueprint_list:
            from models.task_blueprint import TaskBlueprint
            self._task_blueprint_list = [
                item if isinstance(item, TaskBlueprint) else TaskBlueprint._teaql_construct(**item)
                for item in self._task_blueprint_list
            ]
        if self._blueprint_subtask_list:
            from models.blueprint_subtask import BlueprintSubtask
            self._blueprint_subtask_list = [
                item if isinstance(item, BlueprintSubtask) else BlueprintSubtask._teaql_construct(**item)
                for item in self._blueprint_subtask_list
            ]
        if self._inbox_notice_list:
            from models.inbox_notice import InboxNotice
            self._inbox_notice_list = [
                item if isinstance(item, InboxNotice) else InboxNotice._teaql_construct(**item)
                for item in self._inbox_notice_list
            ]
        self._ledger_id = getattr(self, "id", None)
        if self._ledger_id is None:
            self._ledger_id = -next(self._teaql_temporary_ids)
        key = self._teaql_entity_key()
        if self._action == "Create":
            self._entity_root.mark_as_new(key)
        elif getattr(self, "version", None) is not None:
            self._entity_root.set_original_version(key, int(self.version))

    def _teaql_entity_key(self):
        return EntityKey("WorkAccount", self._ledger_id)

    def _teaql_attach_root(self, root):
        if self._entity_root is not root:
            root.merge_from(self._entity_root)
            self._entity_root = root
        for child in self._work_project_list:
            child._teaql_attach_root(root)
        for child in self._project_membership_list:
            child._teaql_attach_root(root)
        for child in self._work_task_list_as_created_by:
            child._teaql_attach_root(root)
        for child in self._work_task_list_as_assignee:
            child._teaql_attach_root(root)
        for child in self._work_subtask_list:
            child._teaql_attach_root(root)
        for child in self._task_comment_list:
            child._teaql_attach_root(root)
        for child in self._task_event_list:
            child._teaql_attach_root(root)
        for child in self._task_participant_list:
            child._teaql_attach_root(root)
        for child in self._deleted_task_viewer_list:
            child._teaql_attach_root(root)
        for child in self._task_blueprint_list:
            child._teaql_attach_root(root)
        for child in self._blueprint_subtask_list:
            child._teaql_attach_root(root)
        for child in self._inbox_notice_list:
            child._teaql_attach_root(root)
        return self
    def mark_for_deletion(self):
        self._action = "Delete"
        self._entity_root.mark_as_deleted(self._teaql_entity_key())
        return self

    def audit_as(self, comment: str):
        if not isinstance(comment, str) or not comment.strip():
            raise ValueError("Security audit failure: audit_as() requires a non-empty reason")
        self._comment = comment
        return self

    async def save(self, context):
        # Reserve stable internal IDs before the transaction and before policy
        # review. A relation to a new parent must have the same identity in the
        # reviewed graph plan and in the commands eventually sent to SQL.
        await self._teaql_reserve_graph_ids(context, set())
        await self._teaql_ensure_business_ids(context)
        return await context.execute_graph_save(lambda graph: self._teaql_preflight_and_save(graph), comment=self._comment)

    async def _teaql_ensure_business_ids(self, context):
        if self._action != "Create":
            return

    async def _teaql_reserve_graph_ids(self, context, visited):
        object_identity = id(self)
        if object_identity in visited:
            return
        visited.add(object_identity)
        if self._action == "Create" and getattr(self, "id", None) is None:
            service = context.require_resource("dataService")
            allocator = getattr(service, "next_id", None)
            if not callable(allocator):
                raise RuntimeError(
                    "Configured dataService does not support stable ID reservation"
                )
            old_key = self._teaql_entity_key()
            object.__setattr__(self, "id", int(await allocator("WorkAccount")))
            self._loaded_fields.add("id")
            self._ledger_id = self.id
            new_key = self._teaql_entity_key()
            self._entity_root.rekey(old_key, new_key)
            self._entity_root.set(new_key, "id", Value.I64(self.id))
        for child in self._work_project_list:
            child._teaql_attach_root(self._entity_root)
            await child._teaql_reserve_graph_ids(context, visited)
        for child in self._project_membership_list:
            child._teaql_attach_root(self._entity_root)
            await child._teaql_reserve_graph_ids(context, visited)
        for child in self._work_task_list_as_created_by:
            child._teaql_attach_root(self._entity_root)
            await child._teaql_reserve_graph_ids(context, visited)
        for child in self._work_task_list_as_assignee:
            child._teaql_attach_root(self._entity_root)
            await child._teaql_reserve_graph_ids(context, visited)
        for child in self._work_subtask_list:
            child._teaql_attach_root(self._entity_root)
            await child._teaql_reserve_graph_ids(context, visited)
        for child in self._task_comment_list:
            child._teaql_attach_root(self._entity_root)
            await child._teaql_reserve_graph_ids(context, visited)
        for child in self._task_event_list:
            child._teaql_attach_root(self._entity_root)
            await child._teaql_reserve_graph_ids(context, visited)
        for child in self._task_participant_list:
            child._teaql_attach_root(self._entity_root)
            await child._teaql_reserve_graph_ids(context, visited)
        for child in self._deleted_task_viewer_list:
            child._teaql_attach_root(self._entity_root)
            await child._teaql_reserve_graph_ids(context, visited)
        for child in self._task_blueprint_list:
            child._teaql_attach_root(self._entity_root)
            await child._teaql_reserve_graph_ids(context, visited)
        for child in self._blueprint_subtask_list:
            child._teaql_attach_root(self._entity_root)
            await child._teaql_reserve_graph_ids(context, visited)
        for child in self._inbox_notice_list:
            child._teaql_attach_root(self._entity_root)
            await child._teaql_reserve_graph_ids(context, visited)

    async def _teaql_preflight_and_save(self, graph):
        context = graph.context
        self._teaql_preflight_graph(context, graph)
        return await self._teaql_save_within_graph(context, graph)

    def _teaql_build_command(self):
        payload = {}
        if "id" in self._loaded_fields:
            payload["id"] = Value.I64(self.id)

        if "workSpace" in self._loaded_fields:
            reference = self.workSpace
            reference_id = getattr(reference, "id", reference)
            payload["work_space"] = (Value.Object(reference)
                if reference is not None and hasattr(reference, "id") and reference_id is None
                else Value.I64(reference_id))

        if "displayName" in self._loaded_fields:
            payload["display_name"] = Value.Text(self.displayName)

        if "emailAddress" in self._loaded_fields:
            payload["email_address"] = Value.Text(self.emailAddress)

        if "passwordHash" in self._loaded_fields:
            payload["password_hash"] = Value.Text(self.passwordHash)

        if "version" in self._loaded_fields:
            payload["version"] = Value.I64(self.version)

        action = self._action
        if action == "Update":
            ledger = dict(self._entity_root.current_change_set().changes()).get(self._teaql_entity_key(), {})
            payload = {field: value for field, value in ledger.items() if field not in ("id", "version")}
        if action == "Create":
            cmd = InsertCommand("WorkAccount", payload)
        elif action == "Update":
            cmd = UpdateCommand("WorkAccount", Value.from_any(getattr(self, "id", None)), getattr(self, "version", None))
            for key, value in payload.items():
                if key not in ("id", "version"): cmd.value(key, value)
        else:
            cmd = DeleteCommand("WorkAccount", Value.from_any(getattr(self, "id", None)), getattr(self, "version", None))
        return action, cmd

    def _teaql_preflight_graph(self, context, graph):
        if not self._comment or not self._comment.strip():
            raise Exception("Security audit failure: audit_as() must be called before save()")
        if self._action == "Update":
            if "id" not in self._loaded_fields:
                raise CheckException([CheckResult("invalid_type", ObjectLocation().property("id"), message="Mutation requires a fully loaded entity")])
            if "workSpace" not in self._loaded_fields:
                raise CheckException([CheckResult("invalid_type", ObjectLocation().property("work_space"), message="Mutation requires a fully loaded entity")])
            if "displayName" not in self._loaded_fields:
                raise CheckException([CheckResult("invalid_type", ObjectLocation().property("display_name"), message="Mutation requires a fully loaded entity")])
            if "emailAddress" not in self._loaded_fields:
                raise CheckException([CheckResult("invalid_type", ObjectLocation().property("email_address"), message="Mutation requires a fully loaded entity")])
            if "passwordHash" not in self._loaded_fields:
                raise CheckException([CheckResult("invalid_type", ObjectLocation().property("password_hash"), message="Mutation requires a fully loaded entity")])
            if "version" not in self._loaded_fields:
                raise CheckException([CheckResult("invalid_type", ObjectLocation().property("version"), message="Mutation requires a fully loaded entity")])
        _action, cmd = self._teaql_build_command()
        try:
            context.preflight_mutation(cmd)
        finally:
            for field, value in getattr(cmd, "values", {}).items():
                if field not in ("id", "version"):
                    self._entity_root.set(self._teaql_entity_key(), field, value)
        for index, child in enumerate(self._work_project_list):
            child._teaql_attach_root(self._entity_root)
            child.update_owner_account(self)
            child.audit_as(self._comment)
            try:
                child._teaql_preflight_graph(context, graph)
            except CheckException as error:
                prefix = ObjectLocation().property("work_project_list").index(index)
                raise CheckException([
                    CheckResult(v.rule_id, v.location.prefixed_by(prefix), v.input_value, v.system_value, v.message)
                    for v in error.violations
                ]) from error
        for index, child in enumerate(self._project_membership_list):
            child._teaql_attach_root(self._entity_root)
            child.update_member_account(self)
            child.audit_as(self._comment)
            try:
                child._teaql_preflight_graph(context, graph)
            except CheckException as error:
                prefix = ObjectLocation().property("project_membership_list").index(index)
                raise CheckException([
                    CheckResult(v.rule_id, v.location.prefixed_by(prefix), v.input_value, v.system_value, v.message)
                    for v in error.violations
                ]) from error
        for index, child in enumerate(self._work_task_list_as_created_by):
            child._teaql_attach_root(self._entity_root)
            child.update_created_by(self)
            child.audit_as(self._comment)
            try:
                child._teaql_preflight_graph(context, graph)
            except CheckException as error:
                prefix = ObjectLocation().property("work_task_list_as_created_by").index(index)
                raise CheckException([
                    CheckResult(v.rule_id, v.location.prefixed_by(prefix), v.input_value, v.system_value, v.message)
                    for v in error.violations
                ]) from error
        for index, child in enumerate(self._work_task_list_as_assignee):
            child._teaql_attach_root(self._entity_root)
            child.update_assignee(self)
            child.audit_as(self._comment)
            try:
                child._teaql_preflight_graph(context, graph)
            except CheckException as error:
                prefix = ObjectLocation().property("work_task_list_as_assignee").index(index)
                raise CheckException([
                    CheckResult(v.rule_id, v.location.prefixed_by(prefix), v.input_value, v.system_value, v.message)
                    for v in error.violations
                ]) from error
        for index, child in enumerate(self._work_subtask_list):
            child._teaql_attach_root(self._entity_root)
            child.update_assignee(self)
            child.audit_as(self._comment)
            try:
                child._teaql_preflight_graph(context, graph)
            except CheckException as error:
                prefix = ObjectLocation().property("work_subtask_list").index(index)
                raise CheckException([
                    CheckResult(v.rule_id, v.location.prefixed_by(prefix), v.input_value, v.system_value, v.message)
                    for v in error.violations
                ]) from error
        for index, child in enumerate(self._task_comment_list):
            child._teaql_attach_root(self._entity_root)
            child.update_author(self)
            child.audit_as(self._comment)
            try:
                child._teaql_preflight_graph(context, graph)
            except CheckException as error:
                prefix = ObjectLocation().property("task_comment_list").index(index)
                raise CheckException([
                    CheckResult(v.rule_id, v.location.prefixed_by(prefix), v.input_value, v.system_value, v.message)
                    for v in error.violations
                ]) from error
        for index, child in enumerate(self._task_event_list):
            child._teaql_attach_root(self._entity_root)
            child.update_actor(self)
            child.audit_as(self._comment)
            try:
                child._teaql_preflight_graph(context, graph)
            except CheckException as error:
                prefix = ObjectLocation().property("task_event_list").index(index)
                raise CheckException([
                    CheckResult(v.rule_id, v.location.prefixed_by(prefix), v.input_value, v.system_value, v.message)
                    for v in error.violations
                ]) from error
        for index, child in enumerate(self._task_participant_list):
            child._teaql_attach_root(self._entity_root)
            child.update_participant(self)
            child.audit_as(self._comment)
            try:
                child._teaql_preflight_graph(context, graph)
            except CheckException as error:
                prefix = ObjectLocation().property("task_participant_list").index(index)
                raise CheckException([
                    CheckResult(v.rule_id, v.location.prefixed_by(prefix), v.input_value, v.system_value, v.message)
                    for v in error.violations
                ]) from error
        for index, child in enumerate(self._deleted_task_viewer_list):
            child._teaql_attach_root(self._entity_root)
            child.update_viewer(self)
            child.audit_as(self._comment)
            try:
                child._teaql_preflight_graph(context, graph)
            except CheckException as error:
                prefix = ObjectLocation().property("deleted_task_viewer_list").index(index)
                raise CheckException([
                    CheckResult(v.rule_id, v.location.prefixed_by(prefix), v.input_value, v.system_value, v.message)
                    for v in error.violations
                ]) from error
        for index, child in enumerate(self._task_blueprint_list):
            child._teaql_attach_root(self._entity_root)
            child.update_assignee(self)
            child.audit_as(self._comment)
            try:
                child._teaql_preflight_graph(context, graph)
            except CheckException as error:
                prefix = ObjectLocation().property("task_blueprint_list").index(index)
                raise CheckException([
                    CheckResult(v.rule_id, v.location.prefixed_by(prefix), v.input_value, v.system_value, v.message)
                    for v in error.violations
                ]) from error
        for index, child in enumerate(self._blueprint_subtask_list):
            child._teaql_attach_root(self._entity_root)
            child.update_assignee(self)
            child.audit_as(self._comment)
            try:
                child._teaql_preflight_graph(context, graph)
            except CheckException as error:
                prefix = ObjectLocation().property("blueprint_subtask_list").index(index)
                raise CheckException([
                    CheckResult(v.rule_id, v.location.prefixed_by(prefix), v.input_value, v.system_value, v.message)
                    for v in error.violations
                ]) from error
        for index, child in enumerate(self._inbox_notice_list):
            child._teaql_attach_root(self._entity_root)
            child.update_recipient(self)
            child.audit_as(self._comment)
            try:
                child._teaql_preflight_graph(context, graph)
            except CheckException as error:
                prefix = ObjectLocation().property("inbox_notice_list").index(index)
                raise CheckException([
                    CheckResult(v.rule_id, v.location.prefixed_by(prefix), v.input_value, v.system_value, v.message)
                    for v in error.violations
                ]) from error

    async def _teaql_save_within_graph(self, context, graph, parent_scope=None):
        if not self._comment or not self._comment.strip():
            raise Exception("Security audit failure: audit_as() must be called before save()")

        self._teaql_attach_root(self._entity_root)
        action, cmd = self._teaql_build_command()


        scope = graph.scope(self._teaql_entity_key(), parent_scope, self._comment)
        req = graph.request(cmd, scope, self._entity_root, self._teaql_entity_key())

        try:
            context.check_and_fix_mutation(cmd)
        finally:
            for field, value in getattr(cmd, "values", {}).items():
                if field not in ("id", "version"):
                    self._entity_root.set(self._teaql_entity_key(), field, value)
        context.mark_mutation_checked(cmd)
        service = context.require_resource("dataService")
        result = await service.mutate(context, req)
        persisted = result.persisted_record
        if persisted is None:
            raise RuntimeError(
                "Mutation provider did not return authoritative persisted state for WorkAccount"
            )
        rollback_payload = {field: getattr(self, field, None) for field in self._loaded_fields | {"id", "version"}}
        rollback_ledger_id = self._ledger_id
        rollback_action = self._action
        rollback_loaded_fields = set(self._loaded_fields)
        old_key = self._teaql_entity_key()
        if "id" in persisted:
            object.__setattr__(self, "id", persisted["id"])
            self._loaded_fields.add("id")
        elif "id" in persisted:
            object.__setattr__(self, "id", persisted["id"])
            self._loaded_fields.add("id")
        if "work_space" in persisted:
            object.__setattr__(self, "workSpace", persisted["work_space"])
            self._loaded_fields.add("workSpace")
        elif "workSpace" in persisted:
            object.__setattr__(self, "workSpace", persisted["workSpace"])
            self._loaded_fields.add("workSpace")
        if "display_name" in persisted:
            object.__setattr__(self, "displayName", persisted["display_name"])
            self._loaded_fields.add("displayName")
        elif "displayName" in persisted:
            object.__setattr__(self, "displayName", persisted["displayName"])
            self._loaded_fields.add("displayName")
        if "email_address" in persisted:
            object.__setattr__(self, "emailAddress", persisted["email_address"])
            self._loaded_fields.add("emailAddress")
        elif "emailAddress" in persisted:
            object.__setattr__(self, "emailAddress", persisted["emailAddress"])
            self._loaded_fields.add("emailAddress")
        if "password_hash" in persisted:
            object.__setattr__(self, "passwordHash", persisted["password_hash"])
            self._loaded_fields.add("passwordHash")
        elif "passwordHash" in persisted:
            object.__setattr__(self, "passwordHash", persisted["passwordHash"])
            self._loaded_fields.add("passwordHash")
        if "version" in persisted:
            object.__setattr__(self, "version", persisted["version"])
            self._loaded_fields.add("version")
        elif "version" in persisted:
            object.__setattr__(self, "version", persisted["version"])
            self._loaded_fields.add("version")
        self._ledger_id = getattr(self, "id", self._ledger_id)
        new_key = self._teaql_entity_key()
        if old_key != new_key:
            self._entity_root.rekey(old_key, new_key)
        def rollback_entity():
            for field, value in rollback_payload.items():
                object.__setattr__(self, field, value)
            self._ledger_id = rollback_ledger_id
            self._action = rollback_action
            self._loaded_fields = rollback_loaded_fields
            if old_key != new_key:
                self._entity_root.rekey(new_key, old_key)
        graph.after_rollback(rollback_entity)
        if action != "Delete":
            self._action = "Update"

        cascade_relations = []
        cascade_relations.append(("work_project_list", self._work_project_list, "update_owner_account"))
        cascade_relations.append(("project_membership_list", self._project_membership_list, "update_member_account"))
        cascade_relations.append(("work_task_list_as_created_by", self._work_task_list_as_created_by, "update_created_by"))
        cascade_relations.append(("work_task_list_as_assignee", self._work_task_list_as_assignee, "update_assignee"))
        cascade_relations.append(("work_subtask_list", self._work_subtask_list, "update_assignee"))
        cascade_relations.append(("task_comment_list", self._task_comment_list, "update_author"))
        cascade_relations.append(("task_event_list", self._task_event_list, "update_actor"))
        cascade_relations.append(("task_participant_list", self._task_participant_list, "update_participant"))
        cascade_relations.append(("deleted_task_viewer_list", self._deleted_task_viewer_list, "update_viewer"))
        cascade_relations.append(("task_blueprint_list", self._task_blueprint_list, "update_assignee"))
        cascade_relations.append(("blueprint_subtask_list", self._blueprint_subtask_list, "update_assignee"))
        cascade_relations.append(("inbox_notice_list", self._inbox_notice_list, "update_recipient"))
        if action != "Delete":
            for relation_name, children, updater in cascade_relations:
                for index, child in enumerate(children):
                    child._teaql_attach_root(self._entity_root)
                    getattr(child, updater)(self)
                    child.audit_as(self._comment)
                    try:
                        await child._teaql_save_within_graph(context, graph, scope)
                    except CheckException as error:
                        prefix = ObjectLocation().property(relation_name).index(index)
                        raise CheckException([
                            CheckResult(
                                violation.rule_id,
                                violation.location.prefixed_by(prefix),
                                violation.input_value,
                                violation.system_value,
                                violation.message,
                            )
                            for violation in error.violations
                        ]) from error
        def commit_entity():
            self._entity_root.clear_entity(new_key)
            if getattr(self, "version", None) is not None:
                self._entity_root.accept_committed_version(new_key, int(self.version))
        graph.after_commit(commit_entity)
        return self

    def update_id(self, value):
        object.__setattr__(self, "id", value)
        self._loaded_fields.add("id")
        self._entity_root.set(self._teaql_entity_key(), "id", Value.from_any(value))
        return self

    def update_display_name(self, value):
        object.__setattr__(self, "displayName", value)
        self._loaded_fields.add("displayName")
        self._entity_root.set(self._teaql_entity_key(), "display_name", Value.from_any(value))
        return self

    def update_email_address(self, value):
        object.__setattr__(self, "emailAddress", value)
        self._loaded_fields.add("emailAddress")
        self._entity_root.set(self._teaql_entity_key(), "email_address", Value.from_any(value))
        return self

    def update_password_hash(self, value):
        object.__setattr__(self, "passwordHash", value)
        self._loaded_fields.add("passwordHash")
        self._entity_root.set(self._teaql_entity_key(), "password_hash", Value.from_any(value))
        return self

    def update_version(self, value):
        object.__setattr__(self, "version", value)
        self._loaded_fields.add("version")
        self._entity_root.set(self._teaql_entity_key(), "version", Value.from_any(value))
        return self
    def update_work_space(self, value):
        object.__setattr__(self, "workSpace", getattr(value, "id", value) if value else None)
        self._loaded_fields.add("workSpace")
        self._entity_root.set(self._teaql_entity_key(), "work_space", Value.from_any(self.workSpace))
        return self

    def work_project_list(self) -> list:
        self._loaded_fields.add("work_project_list")
        return self._work_project_list

    def project_membership_list(self) -> list:
        self._loaded_fields.add("project_membership_list")
        return self._project_membership_list

    def work_task_list_as_created_by(self) -> list:
        self._loaded_fields.add("work_task_list_as_created_by")
        return self._work_task_list_as_created_by

    def work_task_list_as_assignee(self) -> list:
        self._loaded_fields.add("work_task_list_as_assignee")
        return self._work_task_list_as_assignee

    def work_subtask_list(self) -> list:
        self._loaded_fields.add("work_subtask_list")
        return self._work_subtask_list

    def task_comment_list(self) -> list:
        self._loaded_fields.add("task_comment_list")
        return self._task_comment_list

    def task_event_list(self) -> list:
        self._loaded_fields.add("task_event_list")
        return self._task_event_list

    def task_participant_list(self) -> list:
        self._loaded_fields.add("task_participant_list")
        return self._task_participant_list

    def deleted_task_viewer_list(self) -> list:
        self._loaded_fields.add("deleted_task_viewer_list")
        return self._deleted_task_viewer_list

    def task_blueprint_list(self) -> list:
        self._loaded_fields.add("task_blueprint_list")
        return self._task_blueprint_list

    def blueprint_subtask_list(self) -> list:
        self._loaded_fields.add("blueprint_subtask_list")
        return self._blueprint_subtask_list

    def inbox_notice_list(self) -> list:
        self._loaded_fields.add("inbox_notice_list")
        return self._inbox_notice_list
