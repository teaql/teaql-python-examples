from teaql.core.mutation import InsertCommand, UpdateCommand, DeleteCommand, MutationRequest
from teaql.core.value import Value
from teaql.runtime import CheckException, CheckResult, EntityKey, EntityRoot, ObjectLocation
import itertools
from models.work_space import WorkSpace
from models.work_task import WorkTask
from models.work_account import WorkAccount
from models.work_project import WorkProject
from models.work_task import WorkTask


class TaskEvent:
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
        raise TypeError("Entity constructors are internal; use Q.task_events().comment('what').purpose('why').new_entity(context)")

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
        if "task" in kwargs and "task" not in kwargs:
            kwargs["task"] = kwargs.pop("task")
        if "actor" in kwargs and "actor" not in kwargs:
            kwargs["actor"] = kwargs.pop("actor")
        if "scope_project" in kwargs and "scopeProject" not in kwargs:
            kwargs["scopeProject"] = kwargs.pop("scope_project")
        if "related_task" in kwargs and "relatedTask" not in kwargs:
            kwargs["relatedTask"] = kwargs.pop("related_task")
        if "event_kind" in kwargs and "eventKind" not in kwargs:
            kwargs["eventKind"] = kwargs.pop("event_kind")
        if "field_label" in kwargs and "fieldLabel" not in kwargs:
            kwargs["fieldLabel"] = kwargs.pop("field_label")
        if "old_value" in kwargs and "oldValue" not in kwargs:
            kwargs["oldValue"] = kwargs.pop("old_value")
        if "new_value" in kwargs and "newValue" not in kwargs:
            kwargs["newValue"] = kwargs.pop("new_value")
        if "event_time" in kwargs and "eventTime" not in kwargs:
            kwargs["eventTime"] = kwargs.pop("event_time")
        if "version" in kwargs and "version" not in kwargs:
            kwargs["version"] = kwargs.pop("version")
        self._action = "Update" if kwargs.get("id") else "Create"
        self._comment = None
        self._loaded_fields = set(kwargs.keys())
        object.__setattr__(self, "id", kwargs.get("id"))

        object.__setattr__(self, "workSpace", kwargs.get("workSpace"))

        object.__setattr__(self, "task", kwargs.get("task"))

        object.__setattr__(self, "actor", kwargs.get("actor"))

        object.__setattr__(self, "scopeProject", kwargs.get("scopeProject"))

        object.__setattr__(self, "relatedTask", kwargs.get("relatedTask"))

        object.__setattr__(self, "eventKind", kwargs.get("eventKind"))

        object.__setattr__(self, "fieldLabel", kwargs.get("fieldLabel"))

        object.__setattr__(self, "oldValue", kwargs.get("oldValue"))

        object.__setattr__(self, "newValue", kwargs.get("newValue"))

        object.__setattr__(self, "eventTime", kwargs.get("eventTime"))

        object.__setattr__(self, "version", kwargs.get("version"))

        if isinstance(self.workSpace, dict):
            object.__setattr__(self, "workSpace", WorkSpace._teaql_construct(**self.workSpace))
        if isinstance(self.task, dict):
            object.__setattr__(self, "task", WorkTask._teaql_construct(**self.task))
        if isinstance(self.actor, dict):
            object.__setattr__(self, "actor", WorkAccount._teaql_construct(**self.actor))
        if isinstance(self.scopeProject, dict):
            object.__setattr__(self, "scopeProject", WorkProject._teaql_construct(**self.scopeProject))
        if isinstance(self.relatedTask, dict):
            object.__setattr__(self, "relatedTask", WorkTask._teaql_construct(**self.relatedTask))
        self._inbox_notice_list = kwargs.get("inbox_notice_list", [])
        if "inbox_notice_list" in kwargs or kwargs.get("id") is None:
            self._loaded_fields.add("inbox_notice_list")
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
        return EntityKey("TaskEvent", self._ledger_id)

    def _teaql_attach_root(self, root):
        if self._entity_root is not root:
            root.merge_from(self._entity_root)
            self._entity_root = root
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
            object.__setattr__(self, "id", int(await allocator("TaskEvent")))
            self._loaded_fields.add("id")
            self._ledger_id = self.id
            new_key = self._teaql_entity_key()
            self._entity_root.rekey(old_key, new_key)
            self._entity_root.set(new_key, "id", Value.I64(self.id))
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

        if "task" in self._loaded_fields:
            reference = self.task
            reference_id = getattr(reference, "id", reference)
            payload["task"] = (Value.Object(reference)
                if reference is not None and hasattr(reference, "id") and reference_id is None
                else Value.I64(reference_id))

        if "actor" in self._loaded_fields:
            reference = self.actor
            reference_id = getattr(reference, "id", reference)
            payload["actor"] = (Value.Object(reference)
                if reference is not None and hasattr(reference, "id") and reference_id is None
                else Value.I64(reference_id))

        if "scopeProject" in self._loaded_fields:
            reference = self.scopeProject
            reference_id = getattr(reference, "id", reference)
            payload["scope_project"] = (Value.Object(reference)
                if reference is not None and hasattr(reference, "id") and reference_id is None
                else Value.I64(reference_id))

        if "relatedTask" in self._loaded_fields:
            reference = self.relatedTask
            reference_id = getattr(reference, "id", reference)
            payload["related_task"] = (Value.Object(reference)
                if reference is not None and hasattr(reference, "id") and reference_id is None
                else Value.I64(reference_id))

        if "eventKind" in self._loaded_fields:
            payload["event_kind"] = Value.Text(self.eventKind)

        if "fieldLabel" in self._loaded_fields:
            payload["field_label"] = Value.Text(self.fieldLabel)

        if "oldValue" in self._loaded_fields:
            payload["old_value"] = Value.Text(self.oldValue)

        if "newValue" in self._loaded_fields:
            payload["new_value"] = Value.Text(self.newValue)

        if "eventTime" in self._loaded_fields:
            payload["event_time"] = Value.DateTime(self.eventTime)

        if "version" in self._loaded_fields:
            payload["version"] = Value.I64(self.version)

        action = self._action
        if action == "Update":
            ledger = dict(self._entity_root.current_change_set().changes()).get(self._teaql_entity_key(), {})
            payload = {field: value for field, value in ledger.items() if field not in ("id", "version")}
        if action == "Create":
            cmd = InsertCommand("TaskEvent", payload)
        elif action == "Update":
            cmd = UpdateCommand("TaskEvent", Value.from_any(getattr(self, "id", None)), getattr(self, "version", None))
            for key, value in payload.items():
                if key not in ("id", "version"): cmd.value(key, value)
        else:
            cmd = DeleteCommand("TaskEvent", Value.from_any(getattr(self, "id", None)), getattr(self, "version", None))
        return action, cmd

    def _teaql_preflight_graph(self, context, graph):
        if not self._comment or not self._comment.strip():
            raise Exception("Security audit failure: audit_as() must be called before save()")
        if self._action == "Update":
            if "id" not in self._loaded_fields:
                raise CheckException([CheckResult("invalid_type", ObjectLocation().property("id"), message="Mutation requires a fully loaded entity")])
            if "workSpace" not in self._loaded_fields:
                raise CheckException([CheckResult("invalid_type", ObjectLocation().property("work_space"), message="Mutation requires a fully loaded entity")])
            if "task" not in self._loaded_fields:
                raise CheckException([CheckResult("invalid_type", ObjectLocation().property("task"), message="Mutation requires a fully loaded entity")])
            if "actor" not in self._loaded_fields:
                raise CheckException([CheckResult("invalid_type", ObjectLocation().property("actor"), message="Mutation requires a fully loaded entity")])
            if "scopeProject" not in self._loaded_fields:
                raise CheckException([CheckResult("invalid_type", ObjectLocation().property("scope_project"), message="Mutation requires a fully loaded entity")])
            if "relatedTask" not in self._loaded_fields:
                raise CheckException([CheckResult("invalid_type", ObjectLocation().property("related_task"), message="Mutation requires a fully loaded entity")])
            if "eventKind" not in self._loaded_fields:
                raise CheckException([CheckResult("invalid_type", ObjectLocation().property("event_kind"), message="Mutation requires a fully loaded entity")])
            if "fieldLabel" not in self._loaded_fields:
                raise CheckException([CheckResult("invalid_type", ObjectLocation().property("field_label"), message="Mutation requires a fully loaded entity")])
            if "oldValue" not in self._loaded_fields:
                raise CheckException([CheckResult("invalid_type", ObjectLocation().property("old_value"), message="Mutation requires a fully loaded entity")])
            if "newValue" not in self._loaded_fields:
                raise CheckException([CheckResult("invalid_type", ObjectLocation().property("new_value"), message="Mutation requires a fully loaded entity")])
            if "eventTime" not in self._loaded_fields:
                raise CheckException([CheckResult("invalid_type", ObjectLocation().property("event_time"), message="Mutation requires a fully loaded entity")])
            if "version" not in self._loaded_fields:
                raise CheckException([CheckResult("invalid_type", ObjectLocation().property("version"), message="Mutation requires a fully loaded entity")])
        _action, cmd = self._teaql_build_command()
        try:
            context.preflight_mutation(cmd)
        finally:
            for field, value in getattr(cmd, "values", {}).items():
                if field not in ("id", "version"):
                    self._entity_root.set(self._teaql_entity_key(), field, value)
        for index, child in enumerate(self._inbox_notice_list):
            child._teaql_attach_root(self._entity_root)
            child.update_event(self)
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
                "Mutation provider did not return authoritative persisted state for TaskEvent"
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
        if "task" in persisted:
            object.__setattr__(self, "task", persisted["task"])
            self._loaded_fields.add("task")
        elif "task" in persisted:
            object.__setattr__(self, "task", persisted["task"])
            self._loaded_fields.add("task")
        if "actor" in persisted:
            object.__setattr__(self, "actor", persisted["actor"])
            self._loaded_fields.add("actor")
        elif "actor" in persisted:
            object.__setattr__(self, "actor", persisted["actor"])
            self._loaded_fields.add("actor")
        if "scope_project" in persisted:
            object.__setattr__(self, "scopeProject", persisted["scope_project"])
            self._loaded_fields.add("scopeProject")
        elif "scopeProject" in persisted:
            object.__setattr__(self, "scopeProject", persisted["scopeProject"])
            self._loaded_fields.add("scopeProject")
        if "related_task" in persisted:
            object.__setattr__(self, "relatedTask", persisted["related_task"])
            self._loaded_fields.add("relatedTask")
        elif "relatedTask" in persisted:
            object.__setattr__(self, "relatedTask", persisted["relatedTask"])
            self._loaded_fields.add("relatedTask")
        if "event_kind" in persisted:
            object.__setattr__(self, "eventKind", persisted["event_kind"])
            self._loaded_fields.add("eventKind")
        elif "eventKind" in persisted:
            object.__setattr__(self, "eventKind", persisted["eventKind"])
            self._loaded_fields.add("eventKind")
        if "field_label" in persisted:
            object.__setattr__(self, "fieldLabel", persisted["field_label"])
            self._loaded_fields.add("fieldLabel")
        elif "fieldLabel" in persisted:
            object.__setattr__(self, "fieldLabel", persisted["fieldLabel"])
            self._loaded_fields.add("fieldLabel")
        if "old_value" in persisted:
            object.__setattr__(self, "oldValue", persisted["old_value"])
            self._loaded_fields.add("oldValue")
        elif "oldValue" in persisted:
            object.__setattr__(self, "oldValue", persisted["oldValue"])
            self._loaded_fields.add("oldValue")
        if "new_value" in persisted:
            object.__setattr__(self, "newValue", persisted["new_value"])
            self._loaded_fields.add("newValue")
        elif "newValue" in persisted:
            object.__setattr__(self, "newValue", persisted["newValue"])
            self._loaded_fields.add("newValue")
        if "event_time" in persisted:
            object.__setattr__(self, "eventTime", persisted["event_time"])
            self._loaded_fields.add("eventTime")
        elif "eventTime" in persisted:
            object.__setattr__(self, "eventTime", persisted["eventTime"])
            self._loaded_fields.add("eventTime")
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
        cascade_relations.append(("inbox_notice_list", self._inbox_notice_list, "update_event"))
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

    def update_event_kind(self, value):
        object.__setattr__(self, "eventKind", value)
        self._loaded_fields.add("eventKind")
        self._entity_root.set(self._teaql_entity_key(), "event_kind", Value.from_any(value))
        return self

    def update_field_label(self, value):
        object.__setattr__(self, "fieldLabel", value)
        self._loaded_fields.add("fieldLabel")
        self._entity_root.set(self._teaql_entity_key(), "field_label", Value.from_any(value))
        return self

    def update_old_value(self, value):
        object.__setattr__(self, "oldValue", value)
        self._loaded_fields.add("oldValue")
        self._entity_root.set(self._teaql_entity_key(), "old_value", Value.from_any(value))
        return self

    def update_new_value(self, value):
        object.__setattr__(self, "newValue", value)
        self._loaded_fields.add("newValue")
        self._entity_root.set(self._teaql_entity_key(), "new_value", Value.from_any(value))
        return self

    def update_event_time(self, value):
        object.__setattr__(self, "eventTime", value)
        self._loaded_fields.add("eventTime")
        self._entity_root.set(self._teaql_entity_key(), "event_time", Value.from_any(value))
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


    def update_task(self, value):
        object.__setattr__(self, "task", getattr(value, "id", value) if value else None)
        self._loaded_fields.add("task")
        self._entity_root.set(self._teaql_entity_key(), "task", Value.from_any(self.task))
        return self


    def update_actor(self, value):
        object.__setattr__(self, "actor", getattr(value, "id", value) if value else None)
        self._loaded_fields.add("actor")
        self._entity_root.set(self._teaql_entity_key(), "actor", Value.from_any(self.actor))
        return self


    def update_scope_project(self, value):
        object.__setattr__(self, "scopeProject", getattr(value, "id", value) if value else None)
        self._loaded_fields.add("scopeProject")
        self._entity_root.set(self._teaql_entity_key(), "scope_project", Value.from_any(self.scopeProject))
        return self


    def update_related_task(self, value):
        object.__setattr__(self, "relatedTask", getattr(value, "id", value) if value else None)
        self._loaded_fields.add("relatedTask")
        self._entity_root.set(self._teaql_entity_key(), "related_task", Value.from_any(self.relatedTask))
        return self

    def inbox_notice_list(self) -> list:
        self._loaded_fields.add("inbox_notice_list")
        return self._inbox_notice_list
