from teaql.core.mutation import InsertCommand, UpdateCommand, DeleteCommand, MutationRequest
from teaql.core.value import Value
from teaql.runtime import CheckException, CheckResult, EntityKey, EntityRoot, ObjectLocation
import itertools
from models.work_space import WorkSpace
from models.work_project import WorkProject


class ProjectSection:
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
        raise TypeError("Entity constructors are internal; use Q.project_sections().comment('what').purpose('why').new_entity(context)")

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
        if "section_name" in kwargs and "sectionName" not in kwargs:
            kwargs["sectionName"] = kwargs.pop("section_name")
        if "section_order" in kwargs and "sectionOrder" not in kwargs:
            kwargs["sectionOrder"] = kwargs.pop("section_order")
        if "default_section" in kwargs and "defaultSection" not in kwargs:
            kwargs["defaultSection"] = kwargs.pop("default_section")
        if "version" in kwargs and "version" not in kwargs:
            kwargs["version"] = kwargs.pop("version")
        self._action = "Update" if kwargs.get("id") else "Create"
        self._comment = None
        self._loaded_fields = set(kwargs.keys())
        object.__setattr__(self, "id", kwargs.get("id"))

        object.__setattr__(self, "workSpace", kwargs.get("workSpace"))

        object.__setattr__(self, "project", kwargs.get("project"))

        object.__setattr__(self, "sectionName", kwargs.get("sectionName"))

        object.__setattr__(self, "sectionOrder", kwargs.get("sectionOrder"))

        object.__setattr__(self, "defaultSection", kwargs.get("defaultSection"))

        object.__setattr__(self, "version", kwargs.get("version"))

        if isinstance(self.workSpace, dict):
            object.__setattr__(self, "workSpace", WorkSpace._teaql_construct(**self.workSpace))
        if isinstance(self.project, dict):
            object.__setattr__(self, "project", WorkProject._teaql_construct(**self.project))
        self._work_task_list = kwargs.get("work_task_list", [])
        if "work_task_list" in kwargs or kwargs.get("id") is None:
            self._loaded_fields.add("work_task_list")
        self._task_placement_list = kwargs.get("task_placement_list", [])
        if "task_placement_list" in kwargs or kwargs.get("id") is None:
            self._loaded_fields.add("task_placement_list")
        if self._work_task_list:
            from models.work_task import WorkTask
            self._work_task_list = [
                item if isinstance(item, WorkTask) else WorkTask._teaql_construct(**item)
                for item in self._work_task_list
            ]
        if self._task_placement_list:
            from models.task_placement import TaskPlacement
            self._task_placement_list = [
                item if isinstance(item, TaskPlacement) else TaskPlacement._teaql_construct(**item)
                for item in self._task_placement_list
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
        return EntityKey("ProjectSection", self._ledger_id)

    def _teaql_attach_root(self, root):
        if self._entity_root is not root:
            root.merge_from(self._entity_root)
            self._entity_root = root
        for child in self._work_task_list:
            child._teaql_attach_root(root)
        for child in self._task_placement_list:
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
            object.__setattr__(self, "id", int(await allocator("ProjectSection")))
            self._loaded_fields.add("id")
            self._ledger_id = self.id
            new_key = self._teaql_entity_key()
            self._entity_root.rekey(old_key, new_key)
            self._entity_root.set(new_key, "id", Value.I64(self.id))
        for child in self._work_task_list:
            child._teaql_attach_root(self._entity_root)
            await child._teaql_reserve_graph_ids(context, visited)
        for child in self._task_placement_list:
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

        if "sectionName" in self._loaded_fields:
            payload["section_name"] = Value.Text(self.sectionName)

        if "sectionOrder" in self._loaded_fields:
            payload["section_order"] = Value.I64(self.sectionOrder)

        if "defaultSection" in self._loaded_fields:
            payload["default_section"] = Value.Bool(self.defaultSection)

        if "version" in self._loaded_fields:
            payload["version"] = Value.I64(self.version)

        action = self._action
        if action == "Update":
            ledger = dict(self._entity_root.current_change_set().changes()).get(self._teaql_entity_key(), {})
            payload = {field: value for field, value in ledger.items() if field not in ("id", "version")}
        if action == "Create":
            cmd = InsertCommand("ProjectSection", payload)
        elif action == "Update":
            cmd = UpdateCommand("ProjectSection", Value.from_any(getattr(self, "id", None)), getattr(self, "version", None))
            for key, value in payload.items():
                if key not in ("id", "version"): cmd.value(key, value)
        else:
            cmd = DeleteCommand("ProjectSection", Value.from_any(getattr(self, "id", None)), getattr(self, "version", None))
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
            if "sectionName" not in self._loaded_fields:
                raise CheckException([CheckResult("invalid_type", ObjectLocation().property("section_name"), message="Mutation requires a fully loaded entity")])
            if "sectionOrder" not in self._loaded_fields:
                raise CheckException([CheckResult("invalid_type", ObjectLocation().property("section_order"), message="Mutation requires a fully loaded entity")])
            if "defaultSection" not in self._loaded_fields:
                raise CheckException([CheckResult("invalid_type", ObjectLocation().property("default_section"), message="Mutation requires a fully loaded entity")])
            if "version" not in self._loaded_fields:
                raise CheckException([CheckResult("invalid_type", ObjectLocation().property("version"), message="Mutation requires a fully loaded entity")])
        _action, cmd = self._teaql_build_command()
        try:
            context.preflight_mutation(cmd)
        finally:
            for field, value in getattr(cmd, "values", {}).items():
                if field not in ("id", "version"):
                    self._entity_root.set(self._teaql_entity_key(), field, value)
        for index, child in enumerate(self._work_task_list):
            child._teaql_attach_root(self._entity_root)
            child.update_section(self)
            child.audit_as(self._comment)
            try:
                child._teaql_preflight_graph(context, graph)
            except CheckException as error:
                prefix = ObjectLocation().property("work_task_list").index(index)
                raise CheckException([
                    CheckResult(v.rule_id, v.location.prefixed_by(prefix), v.input_value, v.system_value, v.message)
                    for v in error.violations
                ]) from error
        for index, child in enumerate(self._task_placement_list):
            child._teaql_attach_root(self._entity_root)
            child.update_section(self)
            child.audit_as(self._comment)
            try:
                child._teaql_preflight_graph(context, graph)
            except CheckException as error:
                prefix = ObjectLocation().property("task_placement_list").index(index)
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
                "Mutation provider did not return authoritative persisted state for ProjectSection"
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
        if "section_name" in persisted:
            object.__setattr__(self, "sectionName", persisted["section_name"])
            self._loaded_fields.add("sectionName")
        elif "sectionName" in persisted:
            object.__setattr__(self, "sectionName", persisted["sectionName"])
            self._loaded_fields.add("sectionName")
        if "section_order" in persisted:
            object.__setattr__(self, "sectionOrder", persisted["section_order"])
            self._loaded_fields.add("sectionOrder")
        elif "sectionOrder" in persisted:
            object.__setattr__(self, "sectionOrder", persisted["sectionOrder"])
            self._loaded_fields.add("sectionOrder")
        if "default_section" in persisted:
            object.__setattr__(self, "defaultSection", persisted["default_section"])
            self._loaded_fields.add("defaultSection")
        elif "defaultSection" in persisted:
            object.__setattr__(self, "defaultSection", persisted["defaultSection"])
            self._loaded_fields.add("defaultSection")
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
        cascade_relations.append(("work_task_list", self._work_task_list, "update_section"))
        cascade_relations.append(("task_placement_list", self._task_placement_list, "update_section"))
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

    def update_section_name(self, value):
        object.__setattr__(self, "sectionName", value)
        self._loaded_fields.add("sectionName")
        self._entity_root.set(self._teaql_entity_key(), "section_name", Value.from_any(value))
        return self

    def update_section_order(self, value):
        object.__setattr__(self, "sectionOrder", value)
        self._loaded_fields.add("sectionOrder")
        self._entity_root.set(self._teaql_entity_key(), "section_order", Value.from_any(value))
        return self

    def update_default_section(self, value):
        object.__setattr__(self, "defaultSection", value)
        self._loaded_fields.add("defaultSection")
        self._entity_root.set(self._teaql_entity_key(), "default_section", Value.from_any(value))
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

    def work_task_list(self) -> list:
        self._loaded_fields.add("work_task_list")
        return self._work_task_list

    def task_placement_list(self) -> list:
        self._loaded_fields.add("task_placement_list")
        return self._task_placement_list
