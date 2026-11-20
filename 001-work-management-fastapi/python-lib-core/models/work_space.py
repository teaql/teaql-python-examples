from teaql.core.mutation import InsertCommand, UpdateCommand, DeleteCommand, MutationRequest
from teaql.core.value import Value
from teaql.runtime import CheckException, CheckResult, EntityKey, EntityRoot, ObjectLocation
import itertools


class WorkSpace:
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
        raise TypeError("Entity constructors are internal; use Q.work_spaces().comment('what').purpose('why').new_entity(context)")

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
        if "workspace_name" in kwargs and "workspaceName" not in kwargs:
            kwargs["workspaceName"] = kwargs.pop("workspace_name")
        if "version" in kwargs and "version" not in kwargs:
            kwargs["version"] = kwargs.pop("version")
        self._action = "Update" if kwargs.get("id") else "Create"
        self._comment = None
        self._loaded_fields = set(kwargs.keys())
        object.__setattr__(self, "id", kwargs.get("id"))

        object.__setattr__(self, "workspaceName", kwargs.get("workspaceName"))

        object.__setattr__(self, "version", kwargs.get("version"))

        self._work_account_list = kwargs.get("work_account_list", [])
        if "work_account_list" in kwargs or kwargs.get("id") is None:
            self._loaded_fields.add("work_account_list")
        self._work_project_list = kwargs.get("work_project_list", [])
        if "work_project_list" in kwargs or kwargs.get("id") is None:
            self._loaded_fields.add("work_project_list")
        self._project_membership_list = kwargs.get("project_membership_list", [])
        if "project_membership_list" in kwargs or kwargs.get("id") is None:
            self._loaded_fields.add("project_membership_list")
        self._project_section_list = kwargs.get("project_section_list", [])
        if "project_section_list" in kwargs or kwargs.get("id") is None:
            self._loaded_fields.add("project_section_list")
        self._work_task_list = kwargs.get("work_task_list", [])
        if "work_task_list" in kwargs or kwargs.get("id") is None:
            self._loaded_fields.add("work_task_list")
        self._project_field_list = kwargs.get("project_field_list", [])
        if "project_field_list" in kwargs or kwargs.get("id") is None:
            self._loaded_fields.add("project_field_list")
        self._field_option_list = kwargs.get("field_option_list", [])
        if "field_option_list" in kwargs or kwargs.get("id") is None:
            self._loaded_fields.add("field_option_list")
        self._task_field_choice_list = kwargs.get("task_field_choice_list", [])
        if "task_field_choice_list" in kwargs or kwargs.get("id") is None:
            self._loaded_fields.add("task_field_choice_list")
        self._work_subtask_list = kwargs.get("work_subtask_list", [])
        if "work_subtask_list" in kwargs or kwargs.get("id") is None:
            self._loaded_fields.add("work_subtask_list")
        self._task_comment_list = kwargs.get("task_comment_list", [])
        if "task_comment_list" in kwargs or kwargs.get("id") is None:
            self._loaded_fields.add("task_comment_list")
        self._task_dependency_list = kwargs.get("task_dependency_list", [])
        if "task_dependency_list" in kwargs or kwargs.get("id") is None:
            self._loaded_fields.add("task_dependency_list")
        self._task_placement_list = kwargs.get("task_placement_list", [])
        if "task_placement_list" in kwargs or kwargs.get("id") is None:
            self._loaded_fields.add("task_placement_list")
        self._recurrence_link_list = kwargs.get("recurrence_link_list", [])
        if "recurrence_link_list" in kwargs or kwargs.get("id") is None:
            self._loaded_fields.add("recurrence_link_list")
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
        self._blueprint_choice_list = kwargs.get("blueprint_choice_list", [])
        if "blueprint_choice_list" in kwargs or kwargs.get("id") is None:
            self._loaded_fields.add("blueprint_choice_list")
        self._blueprint_subtask_list = kwargs.get("blueprint_subtask_list", [])
        if "blueprint_subtask_list" in kwargs or kwargs.get("id") is None:
            self._loaded_fields.add("blueprint_subtask_list")
        self._inbox_notice_list = kwargs.get("inbox_notice_list", [])
        if "inbox_notice_list" in kwargs or kwargs.get("id") is None:
            self._loaded_fields.add("inbox_notice_list")
        if self._work_account_list:
            from models.work_account import WorkAccount
            self._work_account_list = [
                item if isinstance(item, WorkAccount) else WorkAccount._teaql_construct(**item)
                for item in self._work_account_list
            ]
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
        if self._project_section_list:
            from models.project_section import ProjectSection
            self._project_section_list = [
                item if isinstance(item, ProjectSection) else ProjectSection._teaql_construct(**item)
                for item in self._project_section_list
            ]
        if self._work_task_list:
            from models.work_task import WorkTask
            self._work_task_list = [
                item if isinstance(item, WorkTask) else WorkTask._teaql_construct(**item)
                for item in self._work_task_list
            ]
        if self._project_field_list:
            from models.project_field import ProjectField
            self._project_field_list = [
                item if isinstance(item, ProjectField) else ProjectField._teaql_construct(**item)
                for item in self._project_field_list
            ]
        if self._field_option_list:
            from models.field_option import FieldOption
            self._field_option_list = [
                item if isinstance(item, FieldOption) else FieldOption._teaql_construct(**item)
                for item in self._field_option_list
            ]
        if self._task_field_choice_list:
            from models.task_field_choice import TaskFieldChoice
            self._task_field_choice_list = [
                item if isinstance(item, TaskFieldChoice) else TaskFieldChoice._teaql_construct(**item)
                for item in self._task_field_choice_list
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
        if self._task_dependency_list:
            from models.task_dependency import TaskDependency
            self._task_dependency_list = [
                item if isinstance(item, TaskDependency) else TaskDependency._teaql_construct(**item)
                for item in self._task_dependency_list
            ]
        if self._task_placement_list:
            from models.task_placement import TaskPlacement
            self._task_placement_list = [
                item if isinstance(item, TaskPlacement) else TaskPlacement._teaql_construct(**item)
                for item in self._task_placement_list
            ]
        if self._recurrence_link_list:
            from models.recurrence_link import RecurrenceLink
            self._recurrence_link_list = [
                item if isinstance(item, RecurrenceLink) else RecurrenceLink._teaql_construct(**item)
                for item in self._recurrence_link_list
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
        if self._blueprint_choice_list:
            from models.blueprint_choice import BlueprintChoice
            self._blueprint_choice_list = [
                item if isinstance(item, BlueprintChoice) else BlueprintChoice._teaql_construct(**item)
                for item in self._blueprint_choice_list
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
        return EntityKey("WorkSpace", self._ledger_id)

    def _teaql_attach_root(self, root):
        if self._entity_root is not root:
            root.merge_from(self._entity_root)
            self._entity_root = root
        for child in self._work_account_list:
            child._teaql_attach_root(root)
        for child in self._work_project_list:
            child._teaql_attach_root(root)
        for child in self._project_membership_list:
            child._teaql_attach_root(root)
        for child in self._project_section_list:
            child._teaql_attach_root(root)
        for child in self._work_task_list:
            child._teaql_attach_root(root)
        for child in self._project_field_list:
            child._teaql_attach_root(root)
        for child in self._field_option_list:
            child._teaql_attach_root(root)
        for child in self._task_field_choice_list:
            child._teaql_attach_root(root)
        for child in self._work_subtask_list:
            child._teaql_attach_root(root)
        for child in self._task_comment_list:
            child._teaql_attach_root(root)
        for child in self._task_dependency_list:
            child._teaql_attach_root(root)
        for child in self._task_placement_list:
            child._teaql_attach_root(root)
        for child in self._recurrence_link_list:
            child._teaql_attach_root(root)
        for child in self._task_event_list:
            child._teaql_attach_root(root)
        for child in self._task_participant_list:
            child._teaql_attach_root(root)
        for child in self._deleted_task_viewer_list:
            child._teaql_attach_root(root)
        for child in self._task_blueprint_list:
            child._teaql_attach_root(root)
        for child in self._blueprint_choice_list:
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
            object.__setattr__(self, "id", int(await allocator("WorkSpace")))
            self._loaded_fields.add("id")
            self._ledger_id = self.id
            new_key = self._teaql_entity_key()
            self._entity_root.rekey(old_key, new_key)
            self._entity_root.set(new_key, "id", Value.I64(self.id))
        for child in self._work_account_list:
            child._teaql_attach_root(self._entity_root)
            await child._teaql_reserve_graph_ids(context, visited)
        for child in self._work_project_list:
            child._teaql_attach_root(self._entity_root)
            await child._teaql_reserve_graph_ids(context, visited)
        for child in self._project_membership_list:
            child._teaql_attach_root(self._entity_root)
            await child._teaql_reserve_graph_ids(context, visited)
        for child in self._project_section_list:
            child._teaql_attach_root(self._entity_root)
            await child._teaql_reserve_graph_ids(context, visited)
        for child in self._work_task_list:
            child._teaql_attach_root(self._entity_root)
            await child._teaql_reserve_graph_ids(context, visited)
        for child in self._project_field_list:
            child._teaql_attach_root(self._entity_root)
            await child._teaql_reserve_graph_ids(context, visited)
        for child in self._field_option_list:
            child._teaql_attach_root(self._entity_root)
            await child._teaql_reserve_graph_ids(context, visited)
        for child in self._task_field_choice_list:
            child._teaql_attach_root(self._entity_root)
            await child._teaql_reserve_graph_ids(context, visited)
        for child in self._work_subtask_list:
            child._teaql_attach_root(self._entity_root)
            await child._teaql_reserve_graph_ids(context, visited)
        for child in self._task_comment_list:
            child._teaql_attach_root(self._entity_root)
            await child._teaql_reserve_graph_ids(context, visited)
        for child in self._task_dependency_list:
            child._teaql_attach_root(self._entity_root)
            await child._teaql_reserve_graph_ids(context, visited)
        for child in self._task_placement_list:
            child._teaql_attach_root(self._entity_root)
            await child._teaql_reserve_graph_ids(context, visited)
        for child in self._recurrence_link_list:
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
        for child in self._blueprint_choice_list:
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

        if "workspaceName" in self._loaded_fields:
            payload["workspace_name"] = Value.Text(self.workspaceName)

        if "version" in self._loaded_fields:
            payload["version"] = Value.I64(self.version)

        action = self._action
        if action == "Update":
            ledger = dict(self._entity_root.current_change_set().changes()).get(self._teaql_entity_key(), {})
            payload = {field: value for field, value in ledger.items() if field not in ("id", "version")}
        if action == "Create":
            cmd = InsertCommand("WorkSpace", payload)
        elif action == "Update":
            cmd = UpdateCommand("WorkSpace", Value.from_any(getattr(self, "id", None)), getattr(self, "version", None))
            for key, value in payload.items():
                if key not in ("id", "version"): cmd.value(key, value)
        else:
            cmd = DeleteCommand("WorkSpace", Value.from_any(getattr(self, "id", None)), getattr(self, "version", None))
        return action, cmd

    def _teaql_preflight_graph(self, context, graph):
        if not self._comment or not self._comment.strip():
            raise Exception("Security audit failure: audit_as() must be called before save()")
        if self._action == "Update":
            if "id" not in self._loaded_fields:
                raise CheckException([CheckResult("invalid_type", ObjectLocation().property("id"), message="Mutation requires a fully loaded entity")])
            if "workspaceName" not in self._loaded_fields:
                raise CheckException([CheckResult("invalid_type", ObjectLocation().property("workspace_name"), message="Mutation requires a fully loaded entity")])
            if "version" not in self._loaded_fields:
                raise CheckException([CheckResult("invalid_type", ObjectLocation().property("version"), message="Mutation requires a fully loaded entity")])
        _action, cmd = self._teaql_build_command()
        try:
            context.preflight_mutation(cmd)
        finally:
            for field, value in getattr(cmd, "values", {}).items():
                if field not in ("id", "version"):
                    self._entity_root.set(self._teaql_entity_key(), field, value)
        for index, child in enumerate(self._work_account_list):
            child._teaql_attach_root(self._entity_root)
            child.update_work_space(self)
            child.audit_as(self._comment)
            try:
                child._teaql_preflight_graph(context, graph)
            except CheckException as error:
                prefix = ObjectLocation().property("work_account_list").index(index)
                raise CheckException([
                    CheckResult(v.rule_id, v.location.prefixed_by(prefix), v.input_value, v.system_value, v.message)
                    for v in error.violations
                ]) from error
        for index, child in enumerate(self._work_project_list):
            child._teaql_attach_root(self._entity_root)
            child.update_work_space(self)
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
            child.update_work_space(self)
            child.audit_as(self._comment)
            try:
                child._teaql_preflight_graph(context, graph)
            except CheckException as error:
                prefix = ObjectLocation().property("project_membership_list").index(index)
                raise CheckException([
                    CheckResult(v.rule_id, v.location.prefixed_by(prefix), v.input_value, v.system_value, v.message)
                    for v in error.violations
                ]) from error
        for index, child in enumerate(self._project_section_list):
            child._teaql_attach_root(self._entity_root)
            child.update_work_space(self)
            child.audit_as(self._comment)
            try:
                child._teaql_preflight_graph(context, graph)
            except CheckException as error:
                prefix = ObjectLocation().property("project_section_list").index(index)
                raise CheckException([
                    CheckResult(v.rule_id, v.location.prefixed_by(prefix), v.input_value, v.system_value, v.message)
                    for v in error.violations
                ]) from error
        for index, child in enumerate(self._work_task_list):
            child._teaql_attach_root(self._entity_root)
            child.update_work_space(self)
            child.audit_as(self._comment)
            try:
                child._teaql_preflight_graph(context, graph)
            except CheckException as error:
                prefix = ObjectLocation().property("work_task_list").index(index)
                raise CheckException([
                    CheckResult(v.rule_id, v.location.prefixed_by(prefix), v.input_value, v.system_value, v.message)
                    for v in error.violations
                ]) from error
        for index, child in enumerate(self._project_field_list):
            child._teaql_attach_root(self._entity_root)
            child.update_work_space(self)
            child.audit_as(self._comment)
            try:
                child._teaql_preflight_graph(context, graph)
            except CheckException as error:
                prefix = ObjectLocation().property("project_field_list").index(index)
                raise CheckException([
                    CheckResult(v.rule_id, v.location.prefixed_by(prefix), v.input_value, v.system_value, v.message)
                    for v in error.violations
                ]) from error
        for index, child in enumerate(self._field_option_list):
            child._teaql_attach_root(self._entity_root)
            child.update_work_space(self)
            child.audit_as(self._comment)
            try:
                child._teaql_preflight_graph(context, graph)
            except CheckException as error:
                prefix = ObjectLocation().property("field_option_list").index(index)
                raise CheckException([
                    CheckResult(v.rule_id, v.location.prefixed_by(prefix), v.input_value, v.system_value, v.message)
                    for v in error.violations
                ]) from error
        for index, child in enumerate(self._task_field_choice_list):
            child._teaql_attach_root(self._entity_root)
            child.update_work_space(self)
            child.audit_as(self._comment)
            try:
                child._teaql_preflight_graph(context, graph)
            except CheckException as error:
                prefix = ObjectLocation().property("task_field_choice_list").index(index)
                raise CheckException([
                    CheckResult(v.rule_id, v.location.prefixed_by(prefix), v.input_value, v.system_value, v.message)
                    for v in error.violations
                ]) from error
        for index, child in enumerate(self._work_subtask_list):
            child._teaql_attach_root(self._entity_root)
            child.update_work_space(self)
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
            child.update_work_space(self)
            child.audit_as(self._comment)
            try:
                child._teaql_preflight_graph(context, graph)
            except CheckException as error:
                prefix = ObjectLocation().property("task_comment_list").index(index)
                raise CheckException([
                    CheckResult(v.rule_id, v.location.prefixed_by(prefix), v.input_value, v.system_value, v.message)
                    for v in error.violations
                ]) from error
        for index, child in enumerate(self._task_dependency_list):
            child._teaql_attach_root(self._entity_root)
            child.update_work_space(self)
            child.audit_as(self._comment)
            try:
                child._teaql_preflight_graph(context, graph)
            except CheckException as error:
                prefix = ObjectLocation().property("task_dependency_list").index(index)
                raise CheckException([
                    CheckResult(v.rule_id, v.location.prefixed_by(prefix), v.input_value, v.system_value, v.message)
                    for v in error.violations
                ]) from error
        for index, child in enumerate(self._task_placement_list):
            child._teaql_attach_root(self._entity_root)
            child.update_work_space(self)
            child.audit_as(self._comment)
            try:
                child._teaql_preflight_graph(context, graph)
            except CheckException as error:
                prefix = ObjectLocation().property("task_placement_list").index(index)
                raise CheckException([
                    CheckResult(v.rule_id, v.location.prefixed_by(prefix), v.input_value, v.system_value, v.message)
                    for v in error.violations
                ]) from error
        for index, child in enumerate(self._recurrence_link_list):
            child._teaql_attach_root(self._entity_root)
            child.update_work_space(self)
            child.audit_as(self._comment)
            try:
                child._teaql_preflight_graph(context, graph)
            except CheckException as error:
                prefix = ObjectLocation().property("recurrence_link_list").index(index)
                raise CheckException([
                    CheckResult(v.rule_id, v.location.prefixed_by(prefix), v.input_value, v.system_value, v.message)
                    for v in error.violations
                ]) from error
        for index, child in enumerate(self._task_event_list):
            child._teaql_attach_root(self._entity_root)
            child.update_work_space(self)
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
            child.update_work_space(self)
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
            child.update_work_space(self)
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
            child.update_work_space(self)
            child.audit_as(self._comment)
            try:
                child._teaql_preflight_graph(context, graph)
            except CheckException as error:
                prefix = ObjectLocation().property("task_blueprint_list").index(index)
                raise CheckException([
                    CheckResult(v.rule_id, v.location.prefixed_by(prefix), v.input_value, v.system_value, v.message)
                    for v in error.violations
                ]) from error
        for index, child in enumerate(self._blueprint_choice_list):
            child._teaql_attach_root(self._entity_root)
            child.update_work_space(self)
            child.audit_as(self._comment)
            try:
                child._teaql_preflight_graph(context, graph)
            except CheckException as error:
                prefix = ObjectLocation().property("blueprint_choice_list").index(index)
                raise CheckException([
                    CheckResult(v.rule_id, v.location.prefixed_by(prefix), v.input_value, v.system_value, v.message)
                    for v in error.violations
                ]) from error
        for index, child in enumerate(self._blueprint_subtask_list):
            child._teaql_attach_root(self._entity_root)
            child.update_work_space(self)
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
            child.update_work_space(self)
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
                "Mutation provider did not return authoritative persisted state for WorkSpace"
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
        if "workspace_name" in persisted:
            object.__setattr__(self, "workspaceName", persisted["workspace_name"])
            self._loaded_fields.add("workspaceName")
        elif "workspaceName" in persisted:
            object.__setattr__(self, "workspaceName", persisted["workspaceName"])
            self._loaded_fields.add("workspaceName")
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
        cascade_relations.append(("work_account_list", self._work_account_list, "update_work_space"))
        cascade_relations.append(("work_project_list", self._work_project_list, "update_work_space"))
        cascade_relations.append(("project_membership_list", self._project_membership_list, "update_work_space"))
        cascade_relations.append(("project_section_list", self._project_section_list, "update_work_space"))
        cascade_relations.append(("work_task_list", self._work_task_list, "update_work_space"))
        cascade_relations.append(("project_field_list", self._project_field_list, "update_work_space"))
        cascade_relations.append(("field_option_list", self._field_option_list, "update_work_space"))
        cascade_relations.append(("task_field_choice_list", self._task_field_choice_list, "update_work_space"))
        cascade_relations.append(("work_subtask_list", self._work_subtask_list, "update_work_space"))
        cascade_relations.append(("task_comment_list", self._task_comment_list, "update_work_space"))
        cascade_relations.append(("task_dependency_list", self._task_dependency_list, "update_work_space"))
        cascade_relations.append(("task_placement_list", self._task_placement_list, "update_work_space"))
        cascade_relations.append(("recurrence_link_list", self._recurrence_link_list, "update_work_space"))
        cascade_relations.append(("task_event_list", self._task_event_list, "update_work_space"))
        cascade_relations.append(("task_participant_list", self._task_participant_list, "update_work_space"))
        cascade_relations.append(("deleted_task_viewer_list", self._deleted_task_viewer_list, "update_work_space"))
        cascade_relations.append(("task_blueprint_list", self._task_blueprint_list, "update_work_space"))
        cascade_relations.append(("blueprint_choice_list", self._blueprint_choice_list, "update_work_space"))
        cascade_relations.append(("blueprint_subtask_list", self._blueprint_subtask_list, "update_work_space"))
        cascade_relations.append(("inbox_notice_list", self._inbox_notice_list, "update_work_space"))
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

    def update_workspace_name(self, value):
        object.__setattr__(self, "workspaceName", value)
        self._loaded_fields.add("workspaceName")
        self._entity_root.set(self._teaql_entity_key(), "workspace_name", Value.from_any(value))
        return self

    def update_version(self, value):
        object.__setattr__(self, "version", value)
        self._loaded_fields.add("version")
        self._entity_root.set(self._teaql_entity_key(), "version", Value.from_any(value))
        return self
    def work_account_list(self) -> list:
        self._loaded_fields.add("work_account_list")
        return self._work_account_list

    def work_project_list(self) -> list:
        self._loaded_fields.add("work_project_list")
        return self._work_project_list

    def project_membership_list(self) -> list:
        self._loaded_fields.add("project_membership_list")
        return self._project_membership_list

    def project_section_list(self) -> list:
        self._loaded_fields.add("project_section_list")
        return self._project_section_list

    def work_task_list(self) -> list:
        self._loaded_fields.add("work_task_list")
        return self._work_task_list

    def project_field_list(self) -> list:
        self._loaded_fields.add("project_field_list")
        return self._project_field_list

    def field_option_list(self) -> list:
        self._loaded_fields.add("field_option_list")
        return self._field_option_list

    def task_field_choice_list(self) -> list:
        self._loaded_fields.add("task_field_choice_list")
        return self._task_field_choice_list

    def work_subtask_list(self) -> list:
        self._loaded_fields.add("work_subtask_list")
        return self._work_subtask_list

    def task_comment_list(self) -> list:
        self._loaded_fields.add("task_comment_list")
        return self._task_comment_list

    def task_dependency_list(self) -> list:
        self._loaded_fields.add("task_dependency_list")
        return self._task_dependency_list

    def task_placement_list(self) -> list:
        self._loaded_fields.add("task_placement_list")
        return self._task_placement_list

    def recurrence_link_list(self) -> list:
        self._loaded_fields.add("recurrence_link_list")
        return self._recurrence_link_list

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

    def blueprint_choice_list(self) -> list:
        self._loaded_fields.add("blueprint_choice_list")
        return self._blueprint_choice_list

    def blueprint_subtask_list(self) -> list:
        self._loaded_fields.add("blueprint_subtask_list")
        return self._blueprint_subtask_list

    def inbox_notice_list(self) -> list:
        self._loaded_fields.add("inbox_notice_list")
        return self._inbox_notice_list
