from teaql.core.mutation import InsertCommand, UpdateCommand, DeleteCommand, MutationRequest
from teaql.core.value import Value
from teaql.runtime import CheckException, CheckResult, EntityKey, EntityRoot, ObjectLocation
import itertools
from models.work_space import WorkSpace
from models.work_project import WorkProject
from models.work_account import WorkAccount


class TaskBlueprint:
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
        raise TypeError("Entity constructors are internal; use Q.task_blueprints().comment('what').purpose('why').new_entity(context)")

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
        if "template_name" in kwargs and "templateName" not in kwargs:
            kwargs["templateName"] = kwargs.pop("template_name")
        if "initial_title" in kwargs and "initialTitle" not in kwargs:
            kwargs["initialTitle"] = kwargs.pop("initial_title")
        if "initial_description" in kwargs and "initialDescription" not in kwargs:
            kwargs["initialDescription"] = kwargs.pop("initial_description")
        if "assignee" in kwargs and "assignee" not in kwargs:
            kwargs["assignee"] = kwargs.pop("assignee")
        if "due_offset" in kwargs and "dueOffset" not in kwargs:
            kwargs["dueOffset"] = kwargs.pop("due_offset")
        if "repeat_period" in kwargs and "repeatPeriod" not in kwargs:
            kwargs["repeatPeriod"] = kwargs.pop("repeat_period")
        if "approval" in kwargs and "approval" not in kwargs:
            kwargs["approval"] = kwargs.pop("approval")
        if "version" in kwargs and "version" not in kwargs:
            kwargs["version"] = kwargs.pop("version")
        self._action = "Update" if kwargs.get("id") else "Create"
        self._comment = None
        self._loaded_fields = set(kwargs.keys())
        object.__setattr__(self, "id", kwargs.get("id"))

        object.__setattr__(self, "workSpace", kwargs.get("workSpace"))

        object.__setattr__(self, "project", kwargs.get("project"))

        object.__setattr__(self, "templateName", kwargs.get("templateName"))

        object.__setattr__(self, "initialTitle", kwargs.get("initialTitle"))

        object.__setattr__(self, "initialDescription", kwargs.get("initialDescription"))

        object.__setattr__(self, "assignee", kwargs.get("assignee"))

        object.__setattr__(self, "dueOffset", kwargs.get("dueOffset"))

        object.__setattr__(self, "repeatPeriod", kwargs.get("repeatPeriod"))

        object.__setattr__(self, "approval", kwargs.get("approval"))

        object.__setattr__(self, "version", kwargs.get("version"))

        if isinstance(self.workSpace, dict):
            object.__setattr__(self, "workSpace", WorkSpace._teaql_construct(**self.workSpace))
        if isinstance(self.project, dict):
            object.__setattr__(self, "project", WorkProject._teaql_construct(**self.project))
        if isinstance(self.assignee, dict):
            object.__setattr__(self, "assignee", WorkAccount._teaql_construct(**self.assignee))
        self._blueprint_choice_list = kwargs.get("blueprint_choice_list", [])
        if "blueprint_choice_list" in kwargs or kwargs.get("id") is None:
            self._loaded_fields.add("blueprint_choice_list")
        self._blueprint_subtask_list = kwargs.get("blueprint_subtask_list", [])
        if "blueprint_subtask_list" in kwargs or kwargs.get("id") is None:
            self._loaded_fields.add("blueprint_subtask_list")
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
        self._ledger_id = getattr(self, "id", None)
        if self._ledger_id is None:
            self._ledger_id = -next(self._teaql_temporary_ids)
        key = self._teaql_entity_key()
        if self._action == "Create":
            self._entity_root.mark_as_new(key)
        elif getattr(self, "version", None) is not None:
            self._entity_root.set_original_version(key, int(self.version))

    def _teaql_entity_key(self):
        return EntityKey("TaskBlueprint", self._ledger_id)

    def _teaql_attach_root(self, root):
        if self._entity_root is not root:
            root.merge_from(self._entity_root)
            self._entity_root = root
        for child in self._blueprint_choice_list:
            child._teaql_attach_root(root)
        for child in self._blueprint_subtask_list:
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
            object.__setattr__(self, "id", int(await allocator("TaskBlueprint")))
            self._loaded_fields.add("id")
            self._ledger_id = self.id
            new_key = self._teaql_entity_key()
            self._entity_root.rekey(old_key, new_key)
            self._entity_root.set(new_key, "id", Value.I64(self.id))
        for child in self._blueprint_choice_list:
            child._teaql_attach_root(self._entity_root)
            await child._teaql_reserve_graph_ids(context, visited)
        for child in self._blueprint_subtask_list:
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

        if "templateName" in self._loaded_fields:
            payload["template_name"] = Value.Text(self.templateName)

        if "initialTitle" in self._loaded_fields:
            payload["initial_title"] = Value.Text(self.initialTitle)

        if "initialDescription" in self._loaded_fields:
            payload["initial_description"] = Value.Text(self.initialDescription)

        if "assignee" in self._loaded_fields:
            reference = self.assignee
            reference_id = getattr(reference, "id", reference)
            payload["assignee"] = (Value.Object(reference)
                if reference is not None and hasattr(reference, "id") and reference_id is None
                else Value.I64(reference_id))

        if "dueOffset" in self._loaded_fields:
            payload["due_offset"] = Value.I64(self.dueOffset)

        if "repeatPeriod" in self._loaded_fields:
            payload["repeat_period"] = Value.Text(self.repeatPeriod)

        if "approval" in self._loaded_fields:
            payload["approval"] = Value.Bool(self.approval)

        if "version" in self._loaded_fields:
            payload["version"] = Value.I64(self.version)

        action = self._action
        if action == "Update":
            ledger = dict(self._entity_root.current_change_set().changes()).get(self._teaql_entity_key(), {})
            payload = {field: value for field, value in ledger.items() if field not in ("id", "version")}
        if action == "Create":
            cmd = InsertCommand("TaskBlueprint", payload)
        elif action == "Update":
            cmd = UpdateCommand("TaskBlueprint", Value.from_any(getattr(self, "id", None)), getattr(self, "version", None))
            for key, value in payload.items():
                if key not in ("id", "version"): cmd.value(key, value)
        else:
            cmd = DeleteCommand("TaskBlueprint", Value.from_any(getattr(self, "id", None)), getattr(self, "version", None))
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
            if "templateName" not in self._loaded_fields:
                raise CheckException([CheckResult("invalid_type", ObjectLocation().property("template_name"), message="Mutation requires a fully loaded entity")])
            if "initialTitle" not in self._loaded_fields:
                raise CheckException([CheckResult("invalid_type", ObjectLocation().property("initial_title"), message="Mutation requires a fully loaded entity")])
            if "initialDescription" not in self._loaded_fields:
                raise CheckException([CheckResult("invalid_type", ObjectLocation().property("initial_description"), message="Mutation requires a fully loaded entity")])
            if "assignee" not in self._loaded_fields:
                raise CheckException([CheckResult("invalid_type", ObjectLocation().property("assignee"), message="Mutation requires a fully loaded entity")])
            if "dueOffset" not in self._loaded_fields:
                raise CheckException([CheckResult("invalid_type", ObjectLocation().property("due_offset"), message="Mutation requires a fully loaded entity")])
            if "repeatPeriod" not in self._loaded_fields:
                raise CheckException([CheckResult("invalid_type", ObjectLocation().property("repeat_period"), message="Mutation requires a fully loaded entity")])
            if "approval" not in self._loaded_fields:
                raise CheckException([CheckResult("invalid_type", ObjectLocation().property("approval"), message="Mutation requires a fully loaded entity")])
            if "version" not in self._loaded_fields:
                raise CheckException([CheckResult("invalid_type", ObjectLocation().property("version"), message="Mutation requires a fully loaded entity")])
        _action, cmd = self._teaql_build_command()
        try:
            context.preflight_mutation(cmd)
        finally:
            for field, value in getattr(cmd, "values", {}).items():
                if field not in ("id", "version"):
                    self._entity_root.set(self._teaql_entity_key(), field, value)
        for index, child in enumerate(self._blueprint_choice_list):
            child._teaql_attach_root(self._entity_root)
            child.update_blueprint(self)
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
            child.update_blueprint(self)
            child.audit_as(self._comment)
            try:
                child._teaql_preflight_graph(context, graph)
            except CheckException as error:
                prefix = ObjectLocation().property("blueprint_subtask_list").index(index)
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
                "Mutation provider did not return authoritative persisted state for TaskBlueprint"
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
        if "template_name" in persisted:
            object.__setattr__(self, "templateName", persisted["template_name"])
            self._loaded_fields.add("templateName")
        elif "templateName" in persisted:
            object.__setattr__(self, "templateName", persisted["templateName"])
            self._loaded_fields.add("templateName")
        if "initial_title" in persisted:
            object.__setattr__(self, "initialTitle", persisted["initial_title"])
            self._loaded_fields.add("initialTitle")
        elif "initialTitle" in persisted:
            object.__setattr__(self, "initialTitle", persisted["initialTitle"])
            self._loaded_fields.add("initialTitle")
        if "initial_description" in persisted:
            object.__setattr__(self, "initialDescription", persisted["initial_description"])
            self._loaded_fields.add("initialDescription")
        elif "initialDescription" in persisted:
            object.__setattr__(self, "initialDescription", persisted["initialDescription"])
            self._loaded_fields.add("initialDescription")
        if "assignee" in persisted:
            object.__setattr__(self, "assignee", persisted["assignee"])
            self._loaded_fields.add("assignee")
        elif "assignee" in persisted:
            object.__setattr__(self, "assignee", persisted["assignee"])
            self._loaded_fields.add("assignee")
        if "due_offset" in persisted:
            object.__setattr__(self, "dueOffset", persisted["due_offset"])
            self._loaded_fields.add("dueOffset")
        elif "dueOffset" in persisted:
            object.__setattr__(self, "dueOffset", persisted["dueOffset"])
            self._loaded_fields.add("dueOffset")
        if "repeat_period" in persisted:
            object.__setattr__(self, "repeatPeriod", persisted["repeat_period"])
            self._loaded_fields.add("repeatPeriod")
        elif "repeatPeriod" in persisted:
            object.__setattr__(self, "repeatPeriod", persisted["repeatPeriod"])
            self._loaded_fields.add("repeatPeriod")
        if "approval" in persisted:
            object.__setattr__(self, "approval", persisted["approval"])
            self._loaded_fields.add("approval")
        elif "approval" in persisted:
            object.__setattr__(self, "approval", persisted["approval"])
            self._loaded_fields.add("approval")
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
        cascade_relations.append(("blueprint_choice_list", self._blueprint_choice_list, "update_blueprint"))
        cascade_relations.append(("blueprint_subtask_list", self._blueprint_subtask_list, "update_blueprint"))
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

    def update_template_name(self, value):
        object.__setattr__(self, "templateName", value)
        self._loaded_fields.add("templateName")
        self._entity_root.set(self._teaql_entity_key(), "template_name", Value.from_any(value))
        return self

    def update_initial_title(self, value):
        object.__setattr__(self, "initialTitle", value)
        self._loaded_fields.add("initialTitle")
        self._entity_root.set(self._teaql_entity_key(), "initial_title", Value.from_any(value))
        return self

    def update_initial_description(self, value):
        object.__setattr__(self, "initialDescription", value)
        self._loaded_fields.add("initialDescription")
        self._entity_root.set(self._teaql_entity_key(), "initial_description", Value.from_any(value))
        return self

    def update_due_offset(self, value):
        object.__setattr__(self, "dueOffset", value)
        self._loaded_fields.add("dueOffset")
        self._entity_root.set(self._teaql_entity_key(), "due_offset", Value.from_any(value))
        return self

    def update_repeat_period(self, value):
        object.__setattr__(self, "repeatPeriod", value)
        self._loaded_fields.add("repeatPeriod")
        self._entity_root.set(self._teaql_entity_key(), "repeat_period", Value.from_any(value))
        return self

    def update_approval(self, value):
        object.__setattr__(self, "approval", value)
        self._loaded_fields.add("approval")
        self._entity_root.set(self._teaql_entity_key(), "approval", Value.from_any(value))
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


    def update_assignee(self, value):
        object.__setattr__(self, "assignee", getattr(value, "id", value) if value else None)
        self._loaded_fields.add("assignee")
        self._entity_root.set(self._teaql_entity_key(), "assignee", Value.from_any(self.assignee))
        return self

    def blueprint_choice_list(self) -> list:
        self._loaded_fields.add("blueprint_choice_list")
        return self._blueprint_choice_list

    def blueprint_subtask_list(self) -> list:
        self._loaded_fields.add("blueprint_subtask_list")
        return self._blueprint_subtask_list
