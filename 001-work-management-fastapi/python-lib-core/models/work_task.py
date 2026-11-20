from teaql.core.mutation import InsertCommand, UpdateCommand, DeleteCommand, MutationRequest
from teaql.core.value import Value
from teaql.runtime import CheckException, CheckResult, EntityKey, EntityRoot, ObjectLocation
import itertools
from models.work_space import WorkSpace
from models.work_project import WorkProject
from models.project_section import ProjectSection
from models.work_account import WorkAccount
from models.work_account import WorkAccount


class WorkTask:
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
        raise TypeError("Entity constructors are internal; use Q.work_tasks().comment('what').purpose('why').new_entity(context)")

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
        if "project" in kwargs and "project" not in kwargs:
            kwargs["project"] = kwargs.pop("project")
        if "section" in kwargs and "section" not in kwargs:
            kwargs["section"] = kwargs.pop("section")
        if "deleted_epoch" in kwargs and "deletedEpoch" not in kwargs:
            kwargs["deletedEpoch"] = kwargs.pop("deleted_epoch")
        if "approval" in kwargs and "approval" not in kwargs:
            kwargs["approval"] = kwargs.pop("approval")
        if "decision" in kwargs and "decision" not in kwargs:
            kwargs["decision"] = kwargs.pop("decision")
        if "repeat_period" in kwargs and "repeatPeriod" not in kwargs:
            kwargs["repeatPeriod"] = kwargs.pop("repeat_period")
        if "created_by" in kwargs and "createdBy" not in kwargs:
            kwargs["createdBy"] = kwargs.pop("created_by")
        if "primary_detached" in kwargs and "primaryDetached" not in kwargs:
            kwargs["primaryDetached"] = kwargs.pop("primary_detached")
        if "task_order" in kwargs and "taskOrder" not in kwargs:
            kwargs["taskOrder"] = kwargs.pop("task_order")
        if "task_title" in kwargs and "taskTitle" not in kwargs:
            kwargs["taskTitle"] = kwargs.pop("task_title")
        if "description" in kwargs and "description" not in kwargs:
            kwargs["description"] = kwargs.pop("description")
        if "assignee" in kwargs and "assignee" not in kwargs:
            kwargs["assignee"] = kwargs.pop("assignee")
        if "start_date" in kwargs and "startDate" not in kwargs:
            kwargs["startDate"] = kwargs.pop("start_date")
        if "due_date" in kwargs and "dueDate" not in kwargs:
            kwargs["dueDate"] = kwargs.pop("due_date")
        if "completed" in kwargs and "completed" not in kwargs:
            kwargs["completed"] = kwargs.pop("completed")
        if "version" in kwargs and "version" not in kwargs:
            kwargs["version"] = kwargs.pop("version")
        self._action = "Update" if kwargs.get("id") else "Create"
        self._comment = None
        self._loaded_fields = set(kwargs.keys())
        object.__setattr__(self, "id", kwargs.get("id"))

        object.__setattr__(self, "workSpace", kwargs.get("workSpace"))

        object.__setattr__(self, "project", kwargs.get("project"))

        object.__setattr__(self, "section", kwargs.get("section"))

        object.__setattr__(self, "deletedEpoch", kwargs.get("deletedEpoch"))

        object.__setattr__(self, "approval", kwargs.get("approval"))

        object.__setattr__(self, "decision", kwargs.get("decision"))

        object.__setattr__(self, "repeatPeriod", kwargs.get("repeatPeriod"))

        object.__setattr__(self, "createdBy", kwargs.get("createdBy"))

        object.__setattr__(self, "primaryDetached", kwargs.get("primaryDetached"))

        object.__setattr__(self, "taskOrder", kwargs.get("taskOrder"))

        object.__setattr__(self, "taskTitle", kwargs.get("taskTitle"))

        object.__setattr__(self, "description", kwargs.get("description"))

        object.__setattr__(self, "assignee", kwargs.get("assignee"))

        object.__setattr__(self, "startDate", kwargs.get("startDate"))

        object.__setattr__(self, "dueDate", kwargs.get("dueDate"))

        object.__setattr__(self, "completed", kwargs.get("completed"))

        object.__setattr__(self, "version", kwargs.get("version"))

        if isinstance(self.workSpace, dict):
            object.__setattr__(self, "workSpace", WorkSpace._teaql_construct(**self.workSpace))
        if isinstance(self.project, dict):
            object.__setattr__(self, "project", WorkProject._teaql_construct(**self.project))
        if isinstance(self.section, dict):
            object.__setattr__(self, "section", ProjectSection._teaql_construct(**self.section))
        if isinstance(self.createdBy, dict):
            object.__setattr__(self, "createdBy", WorkAccount._teaql_construct(**self.createdBy))
        if isinstance(self.assignee, dict):
            object.__setattr__(self, "assignee", WorkAccount._teaql_construct(**self.assignee))
        self._task_field_choice_list = kwargs.get("task_field_choice_list", [])
        if "task_field_choice_list" in kwargs or kwargs.get("id") is None:
            self._loaded_fields.add("task_field_choice_list")
        self._work_subtask_list = kwargs.get("work_subtask_list", [])
        if "work_subtask_list" in kwargs or kwargs.get("id") is None:
            self._loaded_fields.add("work_subtask_list")
        self._task_comment_list = kwargs.get("task_comment_list", [])
        if "task_comment_list" in kwargs or kwargs.get("id") is None:
            self._loaded_fields.add("task_comment_list")
        self._task_dependency_list_as_dependent = kwargs.get("task_dependency_list_as_dependent", [])
        if "task_dependency_list_as_dependent" in kwargs or kwargs.get("id") is None:
            self._loaded_fields.add("task_dependency_list_as_dependent")
        self._task_dependency_list_as_blocker = kwargs.get("task_dependency_list_as_blocker", [])
        if "task_dependency_list_as_blocker" in kwargs or kwargs.get("id") is None:
            self._loaded_fields.add("task_dependency_list_as_blocker")
        self._task_placement_list = kwargs.get("task_placement_list", [])
        if "task_placement_list" in kwargs or kwargs.get("id") is None:
            self._loaded_fields.add("task_placement_list")
        self._recurrence_link_list_as_source_task = kwargs.get("recurrence_link_list_as_source_task", [])
        if "recurrence_link_list_as_source_task" in kwargs or kwargs.get("id") is None:
            self._loaded_fields.add("recurrence_link_list_as_source_task")
        self._recurrence_link_list_as_next_task = kwargs.get("recurrence_link_list_as_next_task", [])
        if "recurrence_link_list_as_next_task" in kwargs or kwargs.get("id") is None:
            self._loaded_fields.add("recurrence_link_list_as_next_task")
        self._task_event_list_as_task = kwargs.get("task_event_list_as_task", [])
        if "task_event_list_as_task" in kwargs or kwargs.get("id") is None:
            self._loaded_fields.add("task_event_list_as_task")
        self._task_event_list_as_related_task = kwargs.get("task_event_list_as_related_task", [])
        if "task_event_list_as_related_task" in kwargs or kwargs.get("id") is None:
            self._loaded_fields.add("task_event_list_as_related_task")
        self._task_participant_list = kwargs.get("task_participant_list", [])
        if "task_participant_list" in kwargs or kwargs.get("id") is None:
            self._loaded_fields.add("task_participant_list")
        self._deleted_task_viewer_list = kwargs.get("deleted_task_viewer_list", [])
        if "deleted_task_viewer_list" in kwargs or kwargs.get("id") is None:
            self._loaded_fields.add("deleted_task_viewer_list")
        self._inbox_notice_list = kwargs.get("inbox_notice_list", [])
        if "inbox_notice_list" in kwargs or kwargs.get("id") is None:
            self._loaded_fields.add("inbox_notice_list")
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
        if self._task_dependency_list_as_dependent:
            from models.task_dependency import TaskDependency
            self._task_dependency_list_as_dependent = [
                item if isinstance(item, TaskDependency) else TaskDependency._teaql_construct(**item)
                for item in self._task_dependency_list_as_dependent
            ]
        if self._task_dependency_list_as_blocker:
            from models.task_dependency import TaskDependency
            self._task_dependency_list_as_blocker = [
                item if isinstance(item, TaskDependency) else TaskDependency._teaql_construct(**item)
                for item in self._task_dependency_list_as_blocker
            ]
        if self._task_placement_list:
            from models.task_placement import TaskPlacement
            self._task_placement_list = [
                item if isinstance(item, TaskPlacement) else TaskPlacement._teaql_construct(**item)
                for item in self._task_placement_list
            ]
        if self._recurrence_link_list_as_source_task:
            from models.recurrence_link import RecurrenceLink
            self._recurrence_link_list_as_source_task = [
                item if isinstance(item, RecurrenceLink) else RecurrenceLink._teaql_construct(**item)
                for item in self._recurrence_link_list_as_source_task
            ]
        if self._recurrence_link_list_as_next_task:
            from models.recurrence_link import RecurrenceLink
            self._recurrence_link_list_as_next_task = [
                item if isinstance(item, RecurrenceLink) else RecurrenceLink._teaql_construct(**item)
                for item in self._recurrence_link_list_as_next_task
            ]
        if self._task_event_list_as_task:
            from models.task_event import TaskEvent
            self._task_event_list_as_task = [
                item if isinstance(item, TaskEvent) else TaskEvent._teaql_construct(**item)
                for item in self._task_event_list_as_task
            ]
        if self._task_event_list_as_related_task:
            from models.task_event import TaskEvent
            self._task_event_list_as_related_task = [
                item if isinstance(item, TaskEvent) else TaskEvent._teaql_construct(**item)
                for item in self._task_event_list_as_related_task
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
        return EntityKey("WorkTask", self._ledger_id)

    def _teaql_attach_root(self, root):
        if self._entity_root is not root:
            root.merge_from(self._entity_root)
            self._entity_root = root
        for child in self._task_field_choice_list:
            child._teaql_attach_root(root)
        for child in self._work_subtask_list:
            child._teaql_attach_root(root)
        for child in self._task_comment_list:
            child._teaql_attach_root(root)
        for child in self._task_dependency_list_as_dependent:
            child._teaql_attach_root(root)
        for child in self._task_dependency_list_as_blocker:
            child._teaql_attach_root(root)
        for child in self._task_placement_list:
            child._teaql_attach_root(root)
        for child in self._recurrence_link_list_as_source_task:
            child._teaql_attach_root(root)
        for child in self._recurrence_link_list_as_next_task:
            child._teaql_attach_root(root)
        for child in self._task_event_list_as_task:
            child._teaql_attach_root(root)
        for child in self._task_event_list_as_related_task:
            child._teaql_attach_root(root)
        for child in self._task_participant_list:
            child._teaql_attach_root(root)
        for child in self._deleted_task_viewer_list:
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
            object.__setattr__(self, "id", int(await allocator("WorkTask")))
            self._loaded_fields.add("id")
            self._ledger_id = self.id
            new_key = self._teaql_entity_key()
            self._entity_root.rekey(old_key, new_key)
            self._entity_root.set(new_key, "id", Value.I64(self.id))
        for child in self._task_field_choice_list:
            child._teaql_attach_root(self._entity_root)
            await child._teaql_reserve_graph_ids(context, visited)
        for child in self._work_subtask_list:
            child._teaql_attach_root(self._entity_root)
            await child._teaql_reserve_graph_ids(context, visited)
        for child in self._task_comment_list:
            child._teaql_attach_root(self._entity_root)
            await child._teaql_reserve_graph_ids(context, visited)
        for child in self._task_dependency_list_as_dependent:
            child._teaql_attach_root(self._entity_root)
            await child._teaql_reserve_graph_ids(context, visited)
        for child in self._task_dependency_list_as_blocker:
            child._teaql_attach_root(self._entity_root)
            await child._teaql_reserve_graph_ids(context, visited)
        for child in self._task_placement_list:
            child._teaql_attach_root(self._entity_root)
            await child._teaql_reserve_graph_ids(context, visited)
        for child in self._recurrence_link_list_as_source_task:
            child._teaql_attach_root(self._entity_root)
            await child._teaql_reserve_graph_ids(context, visited)
        for child in self._recurrence_link_list_as_next_task:
            child._teaql_attach_root(self._entity_root)
            await child._teaql_reserve_graph_ids(context, visited)
        for child in self._task_event_list_as_task:
            child._teaql_attach_root(self._entity_root)
            await child._teaql_reserve_graph_ids(context, visited)
        for child in self._task_event_list_as_related_task:
            child._teaql_attach_root(self._entity_root)
            await child._teaql_reserve_graph_ids(context, visited)
        for child in self._task_participant_list:
            child._teaql_attach_root(self._entity_root)
            await child._teaql_reserve_graph_ids(context, visited)
        for child in self._deleted_task_viewer_list:
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

        if "project" in self._loaded_fields:
            reference = self.project
            reference_id = getattr(reference, "id", reference)
            payload["project"] = (Value.Object(reference)
                if reference is not None and hasattr(reference, "id") and reference_id is None
                else Value.I64(reference_id))

        if "section" in self._loaded_fields:
            reference = self.section
            reference_id = getattr(reference, "id", reference)
            payload["section"] = (Value.Object(reference)
                if reference is not None and hasattr(reference, "id") and reference_id is None
                else Value.I64(reference_id))

        if "deletedEpoch" in self._loaded_fields:
            payload["deleted_epoch"] = Value.I64(self.deletedEpoch)

        if "approval" in self._loaded_fields:
            payload["approval"] = Value.Bool(self.approval)

        if "decision" in self._loaded_fields:
            payload["decision"] = Value.Text(self.decision)

        if "repeatPeriod" in self._loaded_fields:
            payload["repeat_period"] = Value.Text(self.repeatPeriod)

        if "createdBy" in self._loaded_fields:
            reference = self.createdBy
            reference_id = getattr(reference, "id", reference)
            payload["created_by"] = (Value.Object(reference)
                if reference is not None and hasattr(reference, "id") and reference_id is None
                else Value.I64(reference_id))

        if "primaryDetached" in self._loaded_fields:
            payload["primary_detached"] = Value.Bool(self.primaryDetached)

        if "taskOrder" in self._loaded_fields:
            payload["task_order"] = Value.I64(self.taskOrder)

        if "taskTitle" in self._loaded_fields:
            payload["task_title"] = Value.Text(self.taskTitle)

        if "description" in self._loaded_fields:
            payload["description"] = Value.Text(self.description)

        if "assignee" in self._loaded_fields:
            reference = self.assignee
            reference_id = getattr(reference, "id", reference)
            payload["assignee"] = (Value.Object(reference)
                if reference is not None and hasattr(reference, "id") and reference_id is None
                else Value.I64(reference_id))

        if "startDate" in self._loaded_fields:
            payload["start_date"] = Value.Date(self.startDate)

        if "dueDate" in self._loaded_fields:
            payload["due_date"] = Value.Date(self.dueDate)

        if "completed" in self._loaded_fields:
            payload["completed"] = Value.Bool(self.completed)

        if "version" in self._loaded_fields:
            payload["version"] = Value.I64(self.version)

        action = self._action
        if action == "Update":
            ledger = dict(self._entity_root.current_change_set().changes()).get(self._teaql_entity_key(), {})
            payload = {field: value for field, value in ledger.items() if field not in ("id", "version")}
        if action == "Create":
            cmd = InsertCommand("WorkTask", payload)
        elif action == "Update":
            cmd = UpdateCommand("WorkTask", Value.from_any(getattr(self, "id", None)), getattr(self, "version", None))
            for key, value in payload.items():
                if key not in ("id", "version"): cmd.value(key, value)
        else:
            cmd = DeleteCommand("WorkTask", Value.from_any(getattr(self, "id", None)), getattr(self, "version", None))
        return action, cmd

    def _teaql_preflight_graph(self, context, graph):
        if not self._comment or not self._comment.strip():
            raise Exception("Security audit failure: audit_as() must be called before save()")
        if self._action == "Update":
            if "id" not in self._loaded_fields:
                raise CheckException([CheckResult("invalid_type", ObjectLocation().property("id"), message="Mutation requires a fully loaded entity")])
            if "workSpace" not in self._loaded_fields:
                raise CheckException([CheckResult("invalid_type", ObjectLocation().property("work_space"), message="Mutation requires a fully loaded entity")])
            if "project" not in self._loaded_fields:
                raise CheckException([CheckResult("invalid_type", ObjectLocation().property("project"), message="Mutation requires a fully loaded entity")])
            if "section" not in self._loaded_fields:
                raise CheckException([CheckResult("invalid_type", ObjectLocation().property("section"), message="Mutation requires a fully loaded entity")])
            if "deletedEpoch" not in self._loaded_fields:
                raise CheckException([CheckResult("invalid_type", ObjectLocation().property("deleted_epoch"), message="Mutation requires a fully loaded entity")])
            if "approval" not in self._loaded_fields:
                raise CheckException([CheckResult("invalid_type", ObjectLocation().property("approval"), message="Mutation requires a fully loaded entity")])
            if "decision" not in self._loaded_fields:
                raise CheckException([CheckResult("invalid_type", ObjectLocation().property("decision"), message="Mutation requires a fully loaded entity")])
            if "repeatPeriod" not in self._loaded_fields:
                raise CheckException([CheckResult("invalid_type", ObjectLocation().property("repeat_period"), message="Mutation requires a fully loaded entity")])
            if "createdBy" not in self._loaded_fields:
                raise CheckException([CheckResult("invalid_type", ObjectLocation().property("created_by"), message="Mutation requires a fully loaded entity")])
            if "primaryDetached" not in self._loaded_fields:
                raise CheckException([CheckResult("invalid_type", ObjectLocation().property("primary_detached"), message="Mutation requires a fully loaded entity")])
            if "taskOrder" not in self._loaded_fields:
                raise CheckException([CheckResult("invalid_type", ObjectLocation().property("task_order"), message="Mutation requires a fully loaded entity")])
            if "taskTitle" not in self._loaded_fields:
                raise CheckException([CheckResult("invalid_type", ObjectLocation().property("task_title"), message="Mutation requires a fully loaded entity")])
            if "description" not in self._loaded_fields:
                raise CheckException([CheckResult("invalid_type", ObjectLocation().property("description"), message="Mutation requires a fully loaded entity")])
            if "assignee" not in self._loaded_fields:
                raise CheckException([CheckResult("invalid_type", ObjectLocation().property("assignee"), message="Mutation requires a fully loaded entity")])
            if "startDate" not in self._loaded_fields:
                raise CheckException([CheckResult("invalid_type", ObjectLocation().property("start_date"), message="Mutation requires a fully loaded entity")])
            if "dueDate" not in self._loaded_fields:
                raise CheckException([CheckResult("invalid_type", ObjectLocation().property("due_date"), message="Mutation requires a fully loaded entity")])
            if "completed" not in self._loaded_fields:
                raise CheckException([CheckResult("invalid_type", ObjectLocation().property("completed"), message="Mutation requires a fully loaded entity")])
            if "version" not in self._loaded_fields:
                raise CheckException([CheckResult("invalid_type", ObjectLocation().property("version"), message="Mutation requires a fully loaded entity")])
        _action, cmd = self._teaql_build_command()
        try:
            context.preflight_mutation(cmd)
        finally:
            for field, value in getattr(cmd, "values", {}).items():
                if field not in ("id", "version"):
                    self._entity_root.set(self._teaql_entity_key(), field, value)
        for index, child in enumerate(self._task_field_choice_list):
            child._teaql_attach_root(self._entity_root)
            child.update_task(self)
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
            child.update_task(self)
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
            child.update_task(self)
            child.audit_as(self._comment)
            try:
                child._teaql_preflight_graph(context, graph)
            except CheckException as error:
                prefix = ObjectLocation().property("task_comment_list").index(index)
                raise CheckException([
                    CheckResult(v.rule_id, v.location.prefixed_by(prefix), v.input_value, v.system_value, v.message)
                    for v in error.violations
                ]) from error
        for index, child in enumerate(self._task_dependency_list_as_dependent):
            child._teaql_attach_root(self._entity_root)
            child.update_dependent(self)
            child.audit_as(self._comment)
            try:
                child._teaql_preflight_graph(context, graph)
            except CheckException as error:
                prefix = ObjectLocation().property("task_dependency_list_as_dependent").index(index)
                raise CheckException([
                    CheckResult(v.rule_id, v.location.prefixed_by(prefix), v.input_value, v.system_value, v.message)
                    for v in error.violations
                ]) from error
        for index, child in enumerate(self._task_dependency_list_as_blocker):
            child._teaql_attach_root(self._entity_root)
            child.update_blocker(self)
            child.audit_as(self._comment)
            try:
                child._teaql_preflight_graph(context, graph)
            except CheckException as error:
                prefix = ObjectLocation().property("task_dependency_list_as_blocker").index(index)
                raise CheckException([
                    CheckResult(v.rule_id, v.location.prefixed_by(prefix), v.input_value, v.system_value, v.message)
                    for v in error.violations
                ]) from error
        for index, child in enumerate(self._task_placement_list):
            child._teaql_attach_root(self._entity_root)
            child.update_task(self)
            child.audit_as(self._comment)
            try:
                child._teaql_preflight_graph(context, graph)
            except CheckException as error:
                prefix = ObjectLocation().property("task_placement_list").index(index)
                raise CheckException([
                    CheckResult(v.rule_id, v.location.prefixed_by(prefix), v.input_value, v.system_value, v.message)
                    for v in error.violations
                ]) from error
        for index, child in enumerate(self._recurrence_link_list_as_source_task):
            child._teaql_attach_root(self._entity_root)
            child.update_source_task(self)
            child.audit_as(self._comment)
            try:
                child._teaql_preflight_graph(context, graph)
            except CheckException as error:
                prefix = ObjectLocation().property("recurrence_link_list_as_source_task").index(index)
                raise CheckException([
                    CheckResult(v.rule_id, v.location.prefixed_by(prefix), v.input_value, v.system_value, v.message)
                    for v in error.violations
                ]) from error
        for index, child in enumerate(self._recurrence_link_list_as_next_task):
            child._teaql_attach_root(self._entity_root)
            child.update_next_task(self)
            child.audit_as(self._comment)
            try:
                child._teaql_preflight_graph(context, graph)
            except CheckException as error:
                prefix = ObjectLocation().property("recurrence_link_list_as_next_task").index(index)
                raise CheckException([
                    CheckResult(v.rule_id, v.location.prefixed_by(prefix), v.input_value, v.system_value, v.message)
                    for v in error.violations
                ]) from error
        for index, child in enumerate(self._task_event_list_as_task):
            child._teaql_attach_root(self._entity_root)
            child.update_task(self)
            child.audit_as(self._comment)
            try:
                child._teaql_preflight_graph(context, graph)
            except CheckException as error:
                prefix = ObjectLocation().property("task_event_list_as_task").index(index)
                raise CheckException([
                    CheckResult(v.rule_id, v.location.prefixed_by(prefix), v.input_value, v.system_value, v.message)
                    for v in error.violations
                ]) from error
        for index, child in enumerate(self._task_event_list_as_related_task):
            child._teaql_attach_root(self._entity_root)
            child.update_related_task(self)
            child.audit_as(self._comment)
            try:
                child._teaql_preflight_graph(context, graph)
            except CheckException as error:
                prefix = ObjectLocation().property("task_event_list_as_related_task").index(index)
                raise CheckException([
                    CheckResult(v.rule_id, v.location.prefixed_by(prefix), v.input_value, v.system_value, v.message)
                    for v in error.violations
                ]) from error
        for index, child in enumerate(self._task_participant_list):
            child._teaql_attach_root(self._entity_root)
            child.update_task(self)
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
            child.update_task(self)
            child.audit_as(self._comment)
            try:
                child._teaql_preflight_graph(context, graph)
            except CheckException as error:
                prefix = ObjectLocation().property("deleted_task_viewer_list").index(index)
                raise CheckException([
                    CheckResult(v.rule_id, v.location.prefixed_by(prefix), v.input_value, v.system_value, v.message)
                    for v in error.violations
                ]) from error
        for index, child in enumerate(self._inbox_notice_list):
            child._teaql_attach_root(self._entity_root)
            child.update_task(self)
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
                "Mutation provider did not return authoritative persisted state for WorkTask"
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
        if "project" in persisted:
            object.__setattr__(self, "project", persisted["project"])
            self._loaded_fields.add("project")
        elif "project" in persisted:
            object.__setattr__(self, "project", persisted["project"])
            self._loaded_fields.add("project")
        if "section" in persisted:
            object.__setattr__(self, "section", persisted["section"])
            self._loaded_fields.add("section")
        elif "section" in persisted:
            object.__setattr__(self, "section", persisted["section"])
            self._loaded_fields.add("section")
        if "deleted_epoch" in persisted:
            object.__setattr__(self, "deletedEpoch", persisted["deleted_epoch"])
            self._loaded_fields.add("deletedEpoch")
        elif "deletedEpoch" in persisted:
            object.__setattr__(self, "deletedEpoch", persisted["deletedEpoch"])
            self._loaded_fields.add("deletedEpoch")
        if "approval" in persisted:
            object.__setattr__(self, "approval", persisted["approval"])
            self._loaded_fields.add("approval")
        elif "approval" in persisted:
            object.__setattr__(self, "approval", persisted["approval"])
            self._loaded_fields.add("approval")
        if "decision" in persisted:
            object.__setattr__(self, "decision", persisted["decision"])
            self._loaded_fields.add("decision")
        elif "decision" in persisted:
            object.__setattr__(self, "decision", persisted["decision"])
            self._loaded_fields.add("decision")
        if "repeat_period" in persisted:
            object.__setattr__(self, "repeatPeriod", persisted["repeat_period"])
            self._loaded_fields.add("repeatPeriod")
        elif "repeatPeriod" in persisted:
            object.__setattr__(self, "repeatPeriod", persisted["repeatPeriod"])
            self._loaded_fields.add("repeatPeriod")
        if "created_by" in persisted:
            object.__setattr__(self, "createdBy", persisted["created_by"])
            self._loaded_fields.add("createdBy")
        elif "createdBy" in persisted:
            object.__setattr__(self, "createdBy", persisted["createdBy"])
            self._loaded_fields.add("createdBy")
        if "primary_detached" in persisted:
            object.__setattr__(self, "primaryDetached", persisted["primary_detached"])
            self._loaded_fields.add("primaryDetached")
        elif "primaryDetached" in persisted:
            object.__setattr__(self, "primaryDetached", persisted["primaryDetached"])
            self._loaded_fields.add("primaryDetached")
        if "task_order" in persisted:
            object.__setattr__(self, "taskOrder", persisted["task_order"])
            self._loaded_fields.add("taskOrder")
        elif "taskOrder" in persisted:
            object.__setattr__(self, "taskOrder", persisted["taskOrder"])
            self._loaded_fields.add("taskOrder")
        if "task_title" in persisted:
            object.__setattr__(self, "taskTitle", persisted["task_title"])
            self._loaded_fields.add("taskTitle")
        elif "taskTitle" in persisted:
            object.__setattr__(self, "taskTitle", persisted["taskTitle"])
            self._loaded_fields.add("taskTitle")
        if "description" in persisted:
            object.__setattr__(self, "description", persisted["description"])
            self._loaded_fields.add("description")
        elif "description" in persisted:
            object.__setattr__(self, "description", persisted["description"])
            self._loaded_fields.add("description")
        if "assignee" in persisted:
            object.__setattr__(self, "assignee", persisted["assignee"])
            self._loaded_fields.add("assignee")
        elif "assignee" in persisted:
            object.__setattr__(self, "assignee", persisted["assignee"])
            self._loaded_fields.add("assignee")
        if "start_date" in persisted:
            object.__setattr__(self, "startDate", persisted["start_date"])
            self._loaded_fields.add("startDate")
        elif "startDate" in persisted:
            object.__setattr__(self, "startDate", persisted["startDate"])
            self._loaded_fields.add("startDate")
        if "due_date" in persisted:
            object.__setattr__(self, "dueDate", persisted["due_date"])
            self._loaded_fields.add("dueDate")
        elif "dueDate" in persisted:
            object.__setattr__(self, "dueDate", persisted["dueDate"])
            self._loaded_fields.add("dueDate")
        if "completed" in persisted:
            object.__setattr__(self, "completed", persisted["completed"])
            self._loaded_fields.add("completed")
        elif "completed" in persisted:
            object.__setattr__(self, "completed", persisted["completed"])
            self._loaded_fields.add("completed")
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
        cascade_relations.append(("task_field_choice_list", self._task_field_choice_list, "update_task"))
        cascade_relations.append(("work_subtask_list", self._work_subtask_list, "update_task"))
        cascade_relations.append(("task_comment_list", self._task_comment_list, "update_task"))
        cascade_relations.append(("task_dependency_list_as_dependent", self._task_dependency_list_as_dependent, "update_dependent"))
        cascade_relations.append(("task_dependency_list_as_blocker", self._task_dependency_list_as_blocker, "update_blocker"))
        cascade_relations.append(("task_placement_list", self._task_placement_list, "update_task"))
        cascade_relations.append(("recurrence_link_list_as_source_task", self._recurrence_link_list_as_source_task, "update_source_task"))
        cascade_relations.append(("recurrence_link_list_as_next_task", self._recurrence_link_list_as_next_task, "update_next_task"))
        cascade_relations.append(("task_event_list_as_task", self._task_event_list_as_task, "update_task"))
        cascade_relations.append(("task_event_list_as_related_task", self._task_event_list_as_related_task, "update_related_task"))
        cascade_relations.append(("task_participant_list", self._task_participant_list, "update_task"))
        cascade_relations.append(("deleted_task_viewer_list", self._deleted_task_viewer_list, "update_task"))
        cascade_relations.append(("inbox_notice_list", self._inbox_notice_list, "update_task"))
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

    def update_deleted_epoch(self, value):
        object.__setattr__(self, "deletedEpoch", value)
        self._loaded_fields.add("deletedEpoch")
        self._entity_root.set(self._teaql_entity_key(), "deleted_epoch", Value.from_any(value))
        return self

    def update_approval(self, value):
        object.__setattr__(self, "approval", value)
        self._loaded_fields.add("approval")
        self._entity_root.set(self._teaql_entity_key(), "approval", Value.from_any(value))
        return self

    def update_decision(self, value):
        object.__setattr__(self, "decision", value)
        self._loaded_fields.add("decision")
        self._entity_root.set(self._teaql_entity_key(), "decision", Value.from_any(value))
        return self

    def update_repeat_period(self, value):
        object.__setattr__(self, "repeatPeriod", value)
        self._loaded_fields.add("repeatPeriod")
        self._entity_root.set(self._teaql_entity_key(), "repeat_period", Value.from_any(value))
        return self

    def update_primary_detached(self, value):
        object.__setattr__(self, "primaryDetached", value)
        self._loaded_fields.add("primaryDetached")
        self._entity_root.set(self._teaql_entity_key(), "primary_detached", Value.from_any(value))
        return self

    def update_task_order(self, value):
        object.__setattr__(self, "taskOrder", value)
        self._loaded_fields.add("taskOrder")
        self._entity_root.set(self._teaql_entity_key(), "task_order", Value.from_any(value))
        return self

    def update_task_title(self, value):
        object.__setattr__(self, "taskTitle", value)
        self._loaded_fields.add("taskTitle")
        self._entity_root.set(self._teaql_entity_key(), "task_title", Value.from_any(value))
        return self

    def update_description(self, value):
        object.__setattr__(self, "description", value)
        self._loaded_fields.add("description")
        self._entity_root.set(self._teaql_entity_key(), "description", Value.from_any(value))
        return self

    def update_start_date(self, value):
        object.__setattr__(self, "startDate", value)
        self._loaded_fields.add("startDate")
        self._entity_root.set(self._teaql_entity_key(), "start_date", Value.from_any(value))
        return self

    def update_due_date(self, value):
        object.__setattr__(self, "dueDate", value)
        self._loaded_fields.add("dueDate")
        self._entity_root.set(self._teaql_entity_key(), "due_date", Value.from_any(value))
        return self

    def update_completed(self, value):
        object.__setattr__(self, "completed", value)
        self._loaded_fields.add("completed")
        self._entity_root.set(self._teaql_entity_key(), "completed", Value.from_any(value))
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


    def update_project(self, value):
        object.__setattr__(self, "project", getattr(value, "id", value) if value else None)
        self._loaded_fields.add("project")
        self._entity_root.set(self._teaql_entity_key(), "project", Value.from_any(self.project))
        return self


    def update_section(self, value):
        object.__setattr__(self, "section", getattr(value, "id", value) if value else None)
        self._loaded_fields.add("section")
        self._entity_root.set(self._teaql_entity_key(), "section", Value.from_any(self.section))
        return self


    def update_created_by(self, value):
        object.__setattr__(self, "createdBy", getattr(value, "id", value) if value else None)
        self._loaded_fields.add("createdBy")
        self._entity_root.set(self._teaql_entity_key(), "created_by", Value.from_any(self.createdBy))
        return self


    def update_assignee(self, value):
        object.__setattr__(self, "assignee", getattr(value, "id", value) if value else None)
        self._loaded_fields.add("assignee")
        self._entity_root.set(self._teaql_entity_key(), "assignee", Value.from_any(self.assignee))
        return self

    def task_field_choice_list(self) -> list:
        self._loaded_fields.add("task_field_choice_list")
        return self._task_field_choice_list

    def work_subtask_list(self) -> list:
        self._loaded_fields.add("work_subtask_list")
        return self._work_subtask_list

    def task_comment_list(self) -> list:
        self._loaded_fields.add("task_comment_list")
        return self._task_comment_list

    def task_dependency_list_as_dependent(self) -> list:
        self._loaded_fields.add("task_dependency_list_as_dependent")
        return self._task_dependency_list_as_dependent

    def task_dependency_list_as_blocker(self) -> list:
        self._loaded_fields.add("task_dependency_list_as_blocker")
        return self._task_dependency_list_as_blocker

    def task_placement_list(self) -> list:
        self._loaded_fields.add("task_placement_list")
        return self._task_placement_list

    def recurrence_link_list_as_source_task(self) -> list:
        self._loaded_fields.add("recurrence_link_list_as_source_task")
        return self._recurrence_link_list_as_source_task

    def recurrence_link_list_as_next_task(self) -> list:
        self._loaded_fields.add("recurrence_link_list_as_next_task")
        return self._recurrence_link_list_as_next_task

    def task_event_list_as_task(self) -> list:
        self._loaded_fields.add("task_event_list_as_task")
        return self._task_event_list_as_task

    def task_event_list_as_related_task(self) -> list:
        self._loaded_fields.add("task_event_list_as_related_task")
        return self._task_event_list_as_related_task

    def task_participant_list(self) -> list:
        self._loaded_fields.add("task_participant_list")
        return self._task_participant_list

    def deleted_task_viewer_list(self) -> list:
        self._loaded_fields.add("deleted_task_viewer_list")
        return self._deleted_task_viewer_list

    def inbox_notice_list(self) -> list:
        self._loaded_fields.add("inbox_notice_list")
        return self._inbox_notice_list
