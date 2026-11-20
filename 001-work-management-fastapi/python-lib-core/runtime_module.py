import asyncio
from datetime import datetime, timezone
from teaql.runtime import CheckResult, ContextEntityRef, JsonFieldNamingProfile, ObjectLocation, RuntimeModule, create_wire_entity_metadata
from teaql.core.meta import EntityDescriptor, PropertyDescriptor, RelationDescriptor
from teaql.core.value import DataType
from Q import Q
from teaql.core.value import Value
try:
    from teaql.core.graph import GraphNode
except ImportError:
    class GraphNode:
        def __init__(self, entity):
            self.entity, self.fields = entity, {}
        def set(self, field, value):
            self.fields[field] = value
            return self
from models.work_space import WorkSpace
from models.work_account import WorkAccount
from models.work_project import WorkProject
from models.project_membership import ProjectMembership
from models.project_section import ProjectSection
from models.work_task import WorkTask
from models.project_field import ProjectField
from models.field_option import FieldOption
from models.task_field_choice import TaskFieldChoice
from models.work_subtask import WorkSubtask
from models.task_comment import TaskComment
from models.task_dependency import TaskDependency
from models.task_placement import TaskPlacement
from models.recurrence_link import RecurrenceLink
from models.task_event import TaskEvent
from models.task_participant import TaskParticipant
from models.deleted_task_viewer import DeletedTaskViewer
from models.task_blueprint import TaskBlueprint
from models.blueprint_choice import BlueprintChoice
from models.blueprint_subtask import BlueprintSubtask
from models.inbox_notice import InboxNotice

def _teaql_is_null(value):
    return value.is_null() if hasattr(value, "is_null") else value is None

def _teaql_raw(value):
    return value.val if hasattr(value, "val") else value

def _teaql_entity_id(value):
    value = _teaql_raw(value)
    if hasattr(value, "id"):
        return value.id
    if isinstance(value, dict):
        return value.get("id")
    return value

class _WorkSpaceChecker:
    def check_and_fix(self, context, record, location, results):
        operation = context.get_resource("fix_operation")
        now = context.get_resource("fix_time")
        if (operation == "insert" and "workspace_name" not in record) or ("workspace_name" in record and _teaql_is_null(record["workspace_name"])):
            results.append(CheckResult("required", ObjectLocation().property("workspace_name")))
        if "workspace_name" in record and _teaql_raw(record["workspace_name"]) is not None and len(_teaql_raw(record["workspace_name"])) > 100:
            results.append(CheckResult("max_length", ObjectLocation().property("workspace_name"), _teaql_raw(record["workspace_name"]), 100))



class _WorkAccountChecker:
    def check_and_fix(self, context, record, location, results):
        operation = context.get_resource("fix_operation")
        now = context.get_resource("fix_time")
        if (operation == "insert" and "work_space" not in record) or ("work_space" in record and _teaql_is_null(record["work_space"])):
            results.append(CheckResult("required", ObjectLocation().property("work_space")))

        if (operation == "insert" and "display_name" not in record) or ("display_name" in record and _teaql_is_null(record["display_name"])):
            results.append(CheckResult("required", ObjectLocation().property("display_name")))
        if "display_name" in record and _teaql_raw(record["display_name"]) is not None and len(_teaql_raw(record["display_name"])) > 100:
            results.append(CheckResult("max_length", ObjectLocation().property("display_name"), _teaql_raw(record["display_name"]), 100))

        if (operation == "insert" and "email_address" not in record) or ("email_address" in record and _teaql_is_null(record["email_address"])):
            results.append(CheckResult("required", ObjectLocation().property("email_address")))
        if "email_address" in record and _teaql_raw(record["email_address"]) is not None and len(_teaql_raw(record["email_address"])) > 100:
            results.append(CheckResult("max_length", ObjectLocation().property("email_address"), _teaql_raw(record["email_address"]), 100))

        if (operation == "insert" and "password_hash" not in record) or ("password_hash" in record and _teaql_is_null(record["password_hash"])):
            results.append(CheckResult("required", ObjectLocation().property("password_hash")))
        if "password_hash" in record and _teaql_raw(record["password_hash"]) is not None and len(_teaql_raw(record["password_hash"])) > 100:
            results.append(CheckResult("max_length", ObjectLocation().property("password_hash"), _teaql_raw(record["password_hash"]), 100))



class _WorkProjectChecker:
    def check_and_fix(self, context, record, location, results):
        operation = context.get_resource("fix_operation")
        now = context.get_resource("fix_time")
        if (operation == "insert" and "work_space" not in record) or ("work_space" in record and _teaql_is_null(record["work_space"])):
            results.append(CheckResult("required", ObjectLocation().property("work_space")))

        if (operation == "insert" and "owner_account" not in record) or ("owner_account" in record and _teaql_is_null(record["owner_account"])):
            results.append(CheckResult("required", ObjectLocation().property("owner_account")))

        if (operation == "insert" and "project_name" not in record) or ("project_name" in record and _teaql_is_null(record["project_name"])):
            results.append(CheckResult("required", ObjectLocation().property("project_name")))
        if "project_name" in record and _teaql_raw(record["project_name"]) is not None and len(_teaql_raw(record["project_name"])) > 100:
            results.append(CheckResult("max_length", ObjectLocation().property("project_name"), _teaql_raw(record["project_name"]), 100))




class _ProjectMembershipChecker:
    def check_and_fix(self, context, record, location, results):
        operation = context.get_resource("fix_operation")
        now = context.get_resource("fix_time")
        if (operation == "insert" and "work_space" not in record) or ("work_space" in record and _teaql_is_null(record["work_space"])):
            results.append(CheckResult("required", ObjectLocation().property("work_space")))

        if (operation == "insert" and "project" not in record) or ("project" in record and _teaql_is_null(record["project"])):
            results.append(CheckResult("required", ObjectLocation().property("project")))

        if (operation == "insert" and "member_account" not in record) or ("member_account" in record and _teaql_is_null(record["member_account"])):
            results.append(CheckResult("required", ObjectLocation().property("member_account")))

        if "access_role" in record and _teaql_raw(record["access_role"]) is not None and len(_teaql_raw(record["access_role"])) > 100:
            results.append(CheckResult("max_length", ObjectLocation().property("access_role"), _teaql_raw(record["access_role"]), 100))



class _ProjectSectionChecker:
    def check_and_fix(self, context, record, location, results):
        operation = context.get_resource("fix_operation")
        now = context.get_resource("fix_time")
        if (operation == "insert" and "work_space" not in record) or ("work_space" in record and _teaql_is_null(record["work_space"])):
            results.append(CheckResult("required", ObjectLocation().property("work_space")))

        if (operation == "insert" and "project" not in record) or ("project" in record and _teaql_is_null(record["project"])):
            results.append(CheckResult("required", ObjectLocation().property("project")))

        if (operation == "insert" and "section_name" not in record) or ("section_name" in record and _teaql_is_null(record["section_name"])):
            results.append(CheckResult("required", ObjectLocation().property("section_name")))
        if "section_name" in record and _teaql_raw(record["section_name"]) is not None and len(_teaql_raw(record["section_name"])) > 100:
            results.append(CheckResult("max_length", ObjectLocation().property("section_name"), _teaql_raw(record["section_name"]), 100))


        if (operation == "insert" and "default_section" not in record) or ("default_section" in record and _teaql_is_null(record["default_section"])):
            results.append(CheckResult("required", ObjectLocation().property("default_section")))



class _WorkTaskChecker:
    def check_and_fix(self, context, record, location, results):
        operation = context.get_resource("fix_operation")
        now = context.get_resource("fix_time")
        if (operation == "insert" and "work_space" not in record) or ("work_space" in record and _teaql_is_null(record["work_space"])):
            results.append(CheckResult("required", ObjectLocation().property("work_space")))

        if (operation == "insert" and "project" not in record) or ("project" in record and _teaql_is_null(record["project"])):
            results.append(CheckResult("required", ObjectLocation().property("project")))

        if (operation == "insert" and "section" not in record) or ("section" in record and _teaql_is_null(record["section"])):
            results.append(CheckResult("required", ObjectLocation().property("section")))



        if "decision" in record and _teaql_raw(record["decision"]) is not None and len(_teaql_raw(record["decision"])) > 100:
            results.append(CheckResult("max_length", ObjectLocation().property("decision"), _teaql_raw(record["decision"]), 100))

        if "repeat_period" in record and _teaql_raw(record["repeat_period"]) is not None and len(_teaql_raw(record["repeat_period"])) > 100:
            results.append(CheckResult("max_length", ObjectLocation().property("repeat_period"), _teaql_raw(record["repeat_period"]), 100))




        if (operation == "insert" and "task_title" not in record) or ("task_title" in record and _teaql_is_null(record["task_title"])):
            results.append(CheckResult("required", ObjectLocation().property("task_title")))
        if "task_title" in record and _teaql_raw(record["task_title"]) is not None and len(_teaql_raw(record["task_title"])) > 100:
            results.append(CheckResult("max_length", ObjectLocation().property("task_title"), _teaql_raw(record["task_title"]), 100))

        if "description" in record and _teaql_raw(record["description"]) is not None and len(_teaql_raw(record["description"])) > 100:
            results.append(CheckResult("max_length", ObjectLocation().property("description"), _teaql_raw(record["description"]), 100))




        if (operation == "insert" and "completed" not in record) or ("completed" in record and _teaql_is_null(record["completed"])):
            results.append(CheckResult("required", ObjectLocation().property("completed")))



class _ProjectFieldChecker:
    def check_and_fix(self, context, record, location, results):
        operation = context.get_resource("fix_operation")
        now = context.get_resource("fix_time")
        if (operation == "insert" and "work_space" not in record) or ("work_space" in record and _teaql_is_null(record["work_space"])):
            results.append(CheckResult("required", ObjectLocation().property("work_space")))

        if (operation == "insert" and "project" not in record) or ("project" in record and _teaql_is_null(record["project"])):
            results.append(CheckResult("required", ObjectLocation().property("project")))

        if (operation == "insert" and "field_name" not in record) or ("field_name" in record and _teaql_is_null(record["field_name"])):
            results.append(CheckResult("required", ObjectLocation().property("field_name")))
        if "field_name" in record and _teaql_raw(record["field_name"]) is not None and len(_teaql_raw(record["field_name"])) > 100:
            results.append(CheckResult("max_length", ObjectLocation().property("field_name"), _teaql_raw(record["field_name"]), 100))



class _FieldOptionChecker:
    def check_and_fix(self, context, record, location, results):
        operation = context.get_resource("fix_operation")
        now = context.get_resource("fix_time")
        if (operation == "insert" and "work_space" not in record) or ("work_space" in record and _teaql_is_null(record["work_space"])):
            results.append(CheckResult("required", ObjectLocation().property("work_space")))

        if (operation == "insert" and "field" not in record) or ("field" in record and _teaql_is_null(record["field"])):
            results.append(CheckResult("required", ObjectLocation().property("field")))

        if (operation == "insert" and "option_name" not in record) or ("option_name" in record and _teaql_is_null(record["option_name"])):
            results.append(CheckResult("required", ObjectLocation().property("option_name")))
        if "option_name" in record and _teaql_raw(record["option_name"]) is not None and len(_teaql_raw(record["option_name"])) > 100:
            results.append(CheckResult("max_length", ObjectLocation().property("option_name"), _teaql_raw(record["option_name"]), 100))

        if (operation == "insert" and "option_order" not in record) or ("option_order" in record and _teaql_is_null(record["option_order"])):
            results.append(CheckResult("required", ObjectLocation().property("option_order")))



class _TaskFieldChoiceChecker:
    def check_and_fix(self, context, record, location, results):
        operation = context.get_resource("fix_operation")
        now = context.get_resource("fix_time")
        if (operation == "insert" and "work_space" not in record) or ("work_space" in record and _teaql_is_null(record["work_space"])):
            results.append(CheckResult("required", ObjectLocation().property("work_space")))

        if (operation == "insert" and "task" not in record) or ("task" in record and _teaql_is_null(record["task"])):
            results.append(CheckResult("required", ObjectLocation().property("task")))

        if (operation == "insert" and "field" not in record) or ("field" in record and _teaql_is_null(record["field"])):
            results.append(CheckResult("required", ObjectLocation().property("field")))

        if (operation == "insert" and "selected_option" not in record) or ("selected_option" in record and _teaql_is_null(record["selected_option"])):
            results.append(CheckResult("required", ObjectLocation().property("selected_option")))



class _WorkSubtaskChecker:
    def check_and_fix(self, context, record, location, results):
        operation = context.get_resource("fix_operation")
        now = context.get_resource("fix_time")
        if (operation == "insert" and "work_space" not in record) or ("work_space" in record and _teaql_is_null(record["work_space"])):
            results.append(CheckResult("required", ObjectLocation().property("work_space")))

        if (operation == "insert" and "task" not in record) or ("task" in record and _teaql_is_null(record["task"])):
            results.append(CheckResult("required", ObjectLocation().property("task")))

        if (operation == "insert" and "subtask_title" not in record) or ("subtask_title" in record and _teaql_is_null(record["subtask_title"])):
            results.append(CheckResult("required", ObjectLocation().property("subtask_title")))
        if "subtask_title" in record and _teaql_raw(record["subtask_title"]) is not None and len(_teaql_raw(record["subtask_title"])) > 100:
            results.append(CheckResult("max_length", ObjectLocation().property("subtask_title"), _teaql_raw(record["subtask_title"]), 100))



        if (operation == "insert" and "completed" not in record) or ("completed" in record and _teaql_is_null(record["completed"])):
            results.append(CheckResult("required", ObjectLocation().property("completed")))



class _TaskCommentChecker:
    def check_and_fix(self, context, record, location, results):
        operation = context.get_resource("fix_operation")
        now = context.get_resource("fix_time")
        if operation == "insert" and ("create_time" not in record or _teaql_is_null(record["create_time"])):
            record["create_time"] = Value.from_any(now)
            context.record_fix_evidence("TaskComment", "create_time", "clock", "graphClock")


        if (operation == "insert" and "work_space" not in record) or ("work_space" in record and _teaql_is_null(record["work_space"])):
            results.append(CheckResult("required", ObjectLocation().property("work_space")))

        if (operation == "insert" and "task" not in record) or ("task" in record and _teaql_is_null(record["task"])):
            results.append(CheckResult("required", ObjectLocation().property("task")))

        if (operation == "insert" and "author" not in record) or ("author" in record and _teaql_is_null(record["author"])):
            results.append(CheckResult("required", ObjectLocation().property("author")))

        if (operation == "insert" and "comment_text" not in record) or ("comment_text" in record and _teaql_is_null(record["comment_text"])):
            results.append(CheckResult("required", ObjectLocation().property("comment_text")))
        if "comment_text" in record and _teaql_raw(record["comment_text"]) is not None and len(_teaql_raw(record["comment_text"])) > 100:
            results.append(CheckResult("max_length", ObjectLocation().property("comment_text"), _teaql_raw(record["comment_text"]), 100))

        if (operation == "insert" and "edited" not in record) or ("edited" in record and _teaql_is_null(record["edited"])):
            results.append(CheckResult("required", ObjectLocation().property("edited")))

        if (operation == "insert" and "create_time" not in record) or ("create_time" in record and _teaql_is_null(record["create_time"])):
            results.append(CheckResult("required", ObjectLocation().property("create_time")))



class _TaskDependencyChecker:
    def check_and_fix(self, context, record, location, results):
        operation = context.get_resource("fix_operation")
        now = context.get_resource("fix_time")
        if (operation == "insert" and "work_space" not in record) or ("work_space" in record and _teaql_is_null(record["work_space"])):
            results.append(CheckResult("required", ObjectLocation().property("work_space")))

        if (operation == "insert" and "dependent" not in record) or ("dependent" in record and _teaql_is_null(record["dependent"])):
            results.append(CheckResult("required", ObjectLocation().property("dependent")))

        if (operation == "insert" and "blocker" not in record) or ("blocker" in record and _teaql_is_null(record["blocker"])):
            results.append(CheckResult("required", ObjectLocation().property("blocker")))



class _TaskPlacementChecker:
    def check_and_fix(self, context, record, location, results):
        operation = context.get_resource("fix_operation")
        now = context.get_resource("fix_time")
        if (operation == "insert" and "work_space" not in record) or ("work_space" in record and _teaql_is_null(record["work_space"])):
            results.append(CheckResult("required", ObjectLocation().property("work_space")))

        if (operation == "insert" and "task" not in record) or ("task" in record and _teaql_is_null(record["task"])):
            results.append(CheckResult("required", ObjectLocation().property("task")))

        if (operation == "insert" and "project" not in record) or ("project" in record and _teaql_is_null(record["project"])):
            results.append(CheckResult("required", ObjectLocation().property("project")))

        if (operation == "insert" and "section" not in record) or ("section" in record and _teaql_is_null(record["section"])):
            results.append(CheckResult("required", ObjectLocation().property("section")))

        if (operation == "insert" and "placement_order" not in record) or ("placement_order" in record and _teaql_is_null(record["placement_order"])):
            results.append(CheckResult("required", ObjectLocation().property("placement_order")))



class _RecurrenceLinkChecker:
    def check_and_fix(self, context, record, location, results):
        operation = context.get_resource("fix_operation")
        now = context.get_resource("fix_time")
        if (operation == "insert" and "work_space" not in record) or ("work_space" in record and _teaql_is_null(record["work_space"])):
            results.append(CheckResult("required", ObjectLocation().property("work_space")))

        if (operation == "insert" and "source_task" not in record) or ("source_task" in record and _teaql_is_null(record["source_task"])):
            results.append(CheckResult("required", ObjectLocation().property("source_task")))

        if (operation == "insert" and "next_task" not in record) or ("next_task" in record and _teaql_is_null(record["next_task"])):
            results.append(CheckResult("required", ObjectLocation().property("next_task")))



class _TaskEventChecker:
    def check_and_fix(self, context, record, location, results):
        operation = context.get_resource("fix_operation")
        now = context.get_resource("fix_time")
        if operation == "insert" and ("event_time" not in record or _teaql_is_null(record["event_time"])):
            record["event_time"] = Value.from_any(now)
            context.record_fix_evidence("TaskEvent", "event_time", "clock", "graphClock")


        if (operation == "insert" and "work_space" not in record) or ("work_space" in record and _teaql_is_null(record["work_space"])):
            results.append(CheckResult("required", ObjectLocation().property("work_space")))

        if (operation == "insert" and "task" not in record) or ("task" in record and _teaql_is_null(record["task"])):
            results.append(CheckResult("required", ObjectLocation().property("task")))

        if (operation == "insert" and "actor" not in record) or ("actor" in record and _teaql_is_null(record["actor"])):
            results.append(CheckResult("required", ObjectLocation().property("actor")))



        if (operation == "insert" and "event_kind" not in record) or ("event_kind" in record and _teaql_is_null(record["event_kind"])):
            results.append(CheckResult("required", ObjectLocation().property("event_kind")))
        if "event_kind" in record and _teaql_raw(record["event_kind"]) is not None and len(_teaql_raw(record["event_kind"])) > 100:
            results.append(CheckResult("max_length", ObjectLocation().property("event_kind"), _teaql_raw(record["event_kind"]), 100))

        if (operation == "insert" and "field_label" not in record) or ("field_label" in record and _teaql_is_null(record["field_label"])):
            results.append(CheckResult("required", ObjectLocation().property("field_label")))
        if "field_label" in record and _teaql_raw(record["field_label"]) is not None and len(_teaql_raw(record["field_label"])) > 100:
            results.append(CheckResult("max_length", ObjectLocation().property("field_label"), _teaql_raw(record["field_label"]), 100))

        if "old_value" in record and _teaql_raw(record["old_value"]) is not None and len(_teaql_raw(record["old_value"])) > 100:
            results.append(CheckResult("max_length", ObjectLocation().property("old_value"), _teaql_raw(record["old_value"]), 100))

        if "new_value" in record and _teaql_raw(record["new_value"]) is not None and len(_teaql_raw(record["new_value"])) > 100:
            results.append(CheckResult("max_length", ObjectLocation().property("new_value"), _teaql_raw(record["new_value"]), 100))

        if (operation == "insert" and "event_time" not in record) or ("event_time" in record and _teaql_is_null(record["event_time"])):
            results.append(CheckResult("required", ObjectLocation().property("event_time")))



class _TaskParticipantChecker:
    def check_and_fix(self, context, record, location, results):
        operation = context.get_resource("fix_operation")
        now = context.get_resource("fix_time")
        if (operation == "insert" and "work_space" not in record) or ("work_space" in record and _teaql_is_null(record["work_space"])):
            results.append(CheckResult("required", ObjectLocation().property("work_space")))

        if (operation == "insert" and "task" not in record) or ("task" in record and _teaql_is_null(record["task"])):
            results.append(CheckResult("required", ObjectLocation().property("task")))

        if (operation == "insert" and "participant" not in record) or ("participant" in record and _teaql_is_null(record["participant"])):
            results.append(CheckResult("required", ObjectLocation().property("participant")))



class _DeletedTaskViewerChecker:
    def check_and_fix(self, context, record, location, results):
        operation = context.get_resource("fix_operation")
        now = context.get_resource("fix_time")
        if (operation == "insert" and "work_space" not in record) or ("work_space" in record and _teaql_is_null(record["work_space"])):
            results.append(CheckResult("required", ObjectLocation().property("work_space")))

        if (operation == "insert" and "task" not in record) or ("task" in record and _teaql_is_null(record["task"])):
            results.append(CheckResult("required", ObjectLocation().property("task")))

        if (operation == "insert" and "viewer" not in record) or ("viewer" in record and _teaql_is_null(record["viewer"])):
            results.append(CheckResult("required", ObjectLocation().property("viewer")))



class _TaskBlueprintChecker:
    def check_and_fix(self, context, record, location, results):
        operation = context.get_resource("fix_operation")
        now = context.get_resource("fix_time")
        if (operation == "insert" and "work_space" not in record) or ("work_space" in record and _teaql_is_null(record["work_space"])):
            results.append(CheckResult("required", ObjectLocation().property("work_space")))

        if (operation == "insert" and "project" not in record) or ("project" in record and _teaql_is_null(record["project"])):
            results.append(CheckResult("required", ObjectLocation().property("project")))

        if (operation == "insert" and "template_name" not in record) or ("template_name" in record and _teaql_is_null(record["template_name"])):
            results.append(CheckResult("required", ObjectLocation().property("template_name")))
        if "template_name" in record and _teaql_raw(record["template_name"]) is not None and len(_teaql_raw(record["template_name"])) > 100:
            results.append(CheckResult("max_length", ObjectLocation().property("template_name"), _teaql_raw(record["template_name"]), 100))

        if (operation == "insert" and "initial_title" not in record) or ("initial_title" in record and _teaql_is_null(record["initial_title"])):
            results.append(CheckResult("required", ObjectLocation().property("initial_title")))
        if "initial_title" in record and _teaql_raw(record["initial_title"]) is not None and len(_teaql_raw(record["initial_title"])) > 100:
            results.append(CheckResult("max_length", ObjectLocation().property("initial_title"), _teaql_raw(record["initial_title"]), 100))

        if "initial_description" in record and _teaql_raw(record["initial_description"]) is not None and len(_teaql_raw(record["initial_description"])) > 100:
            results.append(CheckResult("max_length", ObjectLocation().property("initial_description"), _teaql_raw(record["initial_description"]), 100))



        if (operation == "insert" and "repeat_period" not in record) or ("repeat_period" in record and _teaql_is_null(record["repeat_period"])):
            results.append(CheckResult("required", ObjectLocation().property("repeat_period")))
        if "repeat_period" in record and _teaql_raw(record["repeat_period"]) is not None and len(_teaql_raw(record["repeat_period"])) > 100:
            results.append(CheckResult("max_length", ObjectLocation().property("repeat_period"), _teaql_raw(record["repeat_period"]), 100))

        if (operation == "insert" and "approval" not in record) or ("approval" in record and _teaql_is_null(record["approval"])):
            results.append(CheckResult("required", ObjectLocation().property("approval")))



class _BlueprintChoiceChecker:
    def check_and_fix(self, context, record, location, results):
        operation = context.get_resource("fix_operation")
        now = context.get_resource("fix_time")
        if (operation == "insert" and "work_space" not in record) or ("work_space" in record and _teaql_is_null(record["work_space"])):
            results.append(CheckResult("required", ObjectLocation().property("work_space")))

        if (operation == "insert" and "blueprint" not in record) or ("blueprint" in record and _teaql_is_null(record["blueprint"])):
            results.append(CheckResult("required", ObjectLocation().property("blueprint")))

        if (operation == "insert" and "field" not in record) or ("field" in record and _teaql_is_null(record["field"])):
            results.append(CheckResult("required", ObjectLocation().property("field")))

        if (operation == "insert" and "selected_option" not in record) or ("selected_option" in record and _teaql_is_null(record["selected_option"])):
            results.append(CheckResult("required", ObjectLocation().property("selected_option")))



class _BlueprintSubtaskChecker:
    def check_and_fix(self, context, record, location, results):
        operation = context.get_resource("fix_operation")
        now = context.get_resource("fix_time")
        if (operation == "insert" and "work_space" not in record) or ("work_space" in record and _teaql_is_null(record["work_space"])):
            results.append(CheckResult("required", ObjectLocation().property("work_space")))

        if (operation == "insert" and "blueprint" not in record) or ("blueprint" in record and _teaql_is_null(record["blueprint"])):
            results.append(CheckResult("required", ObjectLocation().property("blueprint")))

        if (operation == "insert" and "subtask_title" not in record) or ("subtask_title" in record and _teaql_is_null(record["subtask_title"])):
            results.append(CheckResult("required", ObjectLocation().property("subtask_title")))
        if "subtask_title" in record and _teaql_raw(record["subtask_title"]) is not None and len(_teaql_raw(record["subtask_title"])) > 100:
            results.append(CheckResult("max_length", ObjectLocation().property("subtask_title"), _teaql_raw(record["subtask_title"]), 100))





class _InboxNoticeChecker:
    def check_and_fix(self, context, record, location, results):
        operation = context.get_resource("fix_operation")
        now = context.get_resource("fix_time")
        if (operation == "insert" and "work_space" not in record) or ("work_space" in record and _teaql_is_null(record["work_space"])):
            results.append(CheckResult("required", ObjectLocation().property("work_space")))

        if (operation == "insert" and "task" not in record) or ("task" in record and _teaql_is_null(record["task"])):
            results.append(CheckResult("required", ObjectLocation().property("task")))

        if (operation == "insert" and "recipient" not in record) or ("recipient" in record and _teaql_is_null(record["recipient"])):
            results.append(CheckResult("required", ObjectLocation().property("recipient")))

        if (operation == "insert" and "event" not in record) or ("event" in record and _teaql_is_null(record["event"])):
            results.append(CheckResult("required", ObjectLocation().property("event")))

        if (operation == "insert" and "read_flag" not in record) or ("read_flag" in record and _teaql_is_null(record["read_flag"])):
            results.append(CheckResult("required", ObjectLocation().property("read_flag")))



_WorkSpace_DESCRIPTOR = (EntityDescriptor("WorkSpace")
    .audit_mask_fields([])
    .table_name("work_space_data").property(PropertyDescriptor("id", DataType.I64).column_name("id").log_policy("plain").is_id().required()).property(PropertyDescriptor("workspace_name", DataType.Text).column_name("workspace_name").log_policy("plain").required()).property(PropertyDescriptor("version", DataType.I64).column_name("version").log_policy("plain").is_version().required()).relation(RelationDescriptor("work_account_list", "WorkAccount").local("id").foreign("work_space").many()).relation(RelationDescriptor("work_project_list", "WorkProject").local("id").foreign("work_space").many()).relation(RelationDescriptor("project_membership_list", "ProjectMembership").local("id").foreign("work_space").many()).relation(RelationDescriptor("project_section_list", "ProjectSection").local("id").foreign("work_space").many()).relation(RelationDescriptor("work_task_list", "WorkTask").local("id").foreign("work_space").many()).relation(RelationDescriptor("project_field_list", "ProjectField").local("id").foreign("work_space").many()).relation(RelationDescriptor("field_option_list", "FieldOption").local("id").foreign("work_space").many()).relation(RelationDescriptor("task_field_choice_list", "TaskFieldChoice").local("id").foreign("work_space").many()).relation(RelationDescriptor("work_subtask_list", "WorkSubtask").local("id").foreign("work_space").many()).relation(RelationDescriptor("task_comment_list", "TaskComment").local("id").foreign("work_space").many()).relation(RelationDescriptor("task_dependency_list", "TaskDependency").local("id").foreign("work_space").many()).relation(RelationDescriptor("task_placement_list", "TaskPlacement").local("id").foreign("work_space").many()).relation(RelationDescriptor("recurrence_link_list", "RecurrenceLink").local("id").foreign("work_space").many()).relation(RelationDescriptor("task_event_list", "TaskEvent").local("id").foreign("work_space").many()).relation(RelationDescriptor("task_participant_list", "TaskParticipant").local("id").foreign("work_space").many()).relation(RelationDescriptor("deleted_task_viewer_list", "DeletedTaskViewer").local("id").foreign("work_space").many()).relation(RelationDescriptor("task_blueprint_list", "TaskBlueprint").local("id").foreign("work_space").many()).relation(RelationDescriptor("blueprint_choice_list", "BlueprintChoice").local("id").foreign("work_space").many()).relation(RelationDescriptor("blueprint_subtask_list", "BlueprintSubtask").local("id").foreign("work_space").many()).relation(RelationDescriptor("inbox_notice_list", "InboxNotice").local("id").foreign("work_space").many())
)

_WorkAccount_DESCRIPTOR = (EntityDescriptor("WorkAccount")
    .audit_mask_fields(["display_name", "email_address", "password_hash"])
    .table_name("work_account_data").property(PropertyDescriptor("id", DataType.I64).column_name("id").log_policy("plain").is_id().required()).property(PropertyDescriptor("work_space", DataType.I64).column_name("work_space").log_policy("plain").required()).property(PropertyDescriptor("display_name", DataType.Text).column_name("display_name").log_policy("plain").required()).property(PropertyDescriptor("email_address", DataType.Text).column_name("email_address").log_policy("plain").required()).property(PropertyDescriptor("password_hash", DataType.Text).column_name("password_hash").log_policy("plain").required()).property(PropertyDescriptor("version", DataType.I64).column_name("version").log_policy("plain").is_version().required()).relation(RelationDescriptor("work_space", "WorkSpace").local("work_space").foreign("id")).relation(RelationDescriptor("work_project_list", "WorkProject").local("id").foreign("owner_account").many()).relation(RelationDescriptor("project_membership_list", "ProjectMembership").local("id").foreign("member_account").many()).relation(RelationDescriptor("work_task_list_as_created_by", "WorkTask").local("id").foreign("created_by").many()).relation(RelationDescriptor("work_task_list_as_assignee", "WorkTask").local("id").foreign("assignee").many()).relation(RelationDescriptor("work_subtask_list", "WorkSubtask").local("id").foreign("assignee").many()).relation(RelationDescriptor("task_comment_list", "TaskComment").local("id").foreign("author").many()).relation(RelationDescriptor("task_event_list", "TaskEvent").local("id").foreign("actor").many()).relation(RelationDescriptor("task_participant_list", "TaskParticipant").local("id").foreign("participant").many()).relation(RelationDescriptor("deleted_task_viewer_list", "DeletedTaskViewer").local("id").foreign("viewer").many()).relation(RelationDescriptor("task_blueprint_list", "TaskBlueprint").local("id").foreign("assignee").many()).relation(RelationDescriptor("blueprint_subtask_list", "BlueprintSubtask").local("id").foreign("assignee").many()).relation(RelationDescriptor("inbox_notice_list", "InboxNotice").local("id").foreign("recipient").many())
)

_WorkProject_DESCRIPTOR = (EntityDescriptor("WorkProject")
    .audit_mask_fields([])
    .table_name("work_project_data").property(PropertyDescriptor("id", DataType.I64).column_name("id").log_policy("plain").is_id().required()).property(PropertyDescriptor("work_space", DataType.I64).column_name("work_space").log_policy("plain").required()).property(PropertyDescriptor("owner_account", DataType.I64).column_name("owner_account").log_policy("plain").required()).property(PropertyDescriptor("project_name", DataType.Text).column_name("project_name").log_policy("plain").required()).property(PropertyDescriptor("shift_dates", DataType.Bool).column_name("shift_dates").log_policy("plain")).property(PropertyDescriptor("version", DataType.I64).column_name("version").log_policy("plain").is_version().required()).relation(RelationDescriptor("work_space", "WorkSpace").local("work_space").foreign("id")).relation(RelationDescriptor("owner_account", "WorkAccount").local("owner_account").foreign("id")).relation(RelationDescriptor("project_membership_list", "ProjectMembership").local("id").foreign("project").many()).relation(RelationDescriptor("project_section_list", "ProjectSection").local("id").foreign("project").many()).relation(RelationDescriptor("work_task_list", "WorkTask").local("id").foreign("project").many()).relation(RelationDescriptor("project_field_list", "ProjectField").local("id").foreign("project").many()).relation(RelationDescriptor("task_placement_list", "TaskPlacement").local("id").foreign("project").many()).relation(RelationDescriptor("task_event_list", "TaskEvent").local("id").foreign("scope_project").many()).relation(RelationDescriptor("task_blueprint_list", "TaskBlueprint").local("id").foreign("project").many())
)

_ProjectMembership_DESCRIPTOR = (EntityDescriptor("ProjectMembership")
    .audit_mask_fields([])
    .table_name("project_membership_data").property(PropertyDescriptor("id", DataType.I64).column_name("id").log_policy("plain").is_id().required()).property(PropertyDescriptor("work_space", DataType.I64).column_name("work_space").log_policy("plain").required()).property(PropertyDescriptor("project", DataType.I64).column_name("project").log_policy("plain").required()).property(PropertyDescriptor("member_account", DataType.I64).column_name("member_account").log_policy("plain").required()).property(PropertyDescriptor("access_role", DataType.Text).column_name("access_role").log_policy("plain")).property(PropertyDescriptor("version", DataType.I64).column_name("version").log_policy("plain").is_version().required()).relation(RelationDescriptor("work_space", "WorkSpace").local("work_space").foreign("id")).relation(RelationDescriptor("project", "WorkProject").local("project").foreign("id")).relation(RelationDescriptor("member_account", "WorkAccount").local("member_account").foreign("id"))
)

_ProjectSection_DESCRIPTOR = (EntityDescriptor("ProjectSection")
    .audit_mask_fields([])
    .table_name("project_section_data").property(PropertyDescriptor("id", DataType.I64).column_name("id").log_policy("plain").is_id().required()).property(PropertyDescriptor("work_space", DataType.I64).column_name("work_space").log_policy("plain").required()).property(PropertyDescriptor("project", DataType.I64).column_name("project").log_policy("plain").required()).property(PropertyDescriptor("section_name", DataType.Text).column_name("section_name").log_policy("plain").required()).property(PropertyDescriptor("section_order", DataType.I64).column_name("section_order").log_policy("plain")).property(PropertyDescriptor("default_section", DataType.Bool).column_name("default_section").log_policy("plain").required()).property(PropertyDescriptor("version", DataType.I64).column_name("version").log_policy("plain").is_version().required()).relation(RelationDescriptor("work_space", "WorkSpace").local("work_space").foreign("id")).relation(RelationDescriptor("project", "WorkProject").local("project").foreign("id")).relation(RelationDescriptor("work_task_list", "WorkTask").local("id").foreign("section").many()).relation(RelationDescriptor("task_placement_list", "TaskPlacement").local("id").foreign("section").many())
)

_WorkTask_DESCRIPTOR = (EntityDescriptor("WorkTask")
    .audit_mask_fields([])
    .table_name("work_task_data").property(PropertyDescriptor("id", DataType.I64).column_name("id").log_policy("plain").is_id().required()).property(PropertyDescriptor("work_space", DataType.I64).column_name("work_space").log_policy("plain").required()).property(PropertyDescriptor("project", DataType.I64).column_name("project").log_policy("plain").required()).property(PropertyDescriptor("section", DataType.I64).column_name("section").log_policy("plain").required()).property(PropertyDescriptor("deleted_epoch", DataType.I64).column_name("deleted_epoch").log_policy("plain")).property(PropertyDescriptor("approval", DataType.Bool).column_name("approval").log_policy("plain")).property(PropertyDescriptor("decision", DataType.Text).column_name("decision").log_policy("plain")).property(PropertyDescriptor("repeat_period", DataType.Text).column_name("repeat_period").log_policy("plain")).property(PropertyDescriptor("created_by", DataType.I64).column_name("created_by").log_policy("plain")).property(PropertyDescriptor("primary_detached", DataType.Bool).column_name("primary_detached").log_policy("plain")).property(PropertyDescriptor("task_order", DataType.I64).column_name("task_order").log_policy("plain")).property(PropertyDescriptor("task_title", DataType.Text).column_name("task_title").log_policy("plain").required()).property(PropertyDescriptor("description", DataType.Text).column_name("description").log_policy("plain")).property(PropertyDescriptor("assignee", DataType.I64).column_name("assignee").log_policy("plain")).property(PropertyDescriptor("start_date", DataType.Date).column_name("start_date").log_policy("plain")).property(PropertyDescriptor("due_date", DataType.Date).column_name("due_date").log_policy("plain")).property(PropertyDescriptor("completed", DataType.Bool).column_name("completed").log_policy("plain").required()).property(PropertyDescriptor("version", DataType.I64).column_name("version").log_policy("plain").is_version().required()).relation(RelationDescriptor("work_space", "WorkSpace").local("work_space").foreign("id")).relation(RelationDescriptor("project", "WorkProject").local("project").foreign("id")).relation(RelationDescriptor("section", "ProjectSection").local("section").foreign("id")).relation(RelationDescriptor("created_by", "WorkAccount").local("created_by").foreign("id")).relation(RelationDescriptor("assignee", "WorkAccount").local("assignee").foreign("id")).relation(RelationDescriptor("task_field_choice_list", "TaskFieldChoice").local("id").foreign("task").many()).relation(RelationDescriptor("work_subtask_list", "WorkSubtask").local("id").foreign("task").many()).relation(RelationDescriptor("task_comment_list", "TaskComment").local("id").foreign("task").many()).relation(RelationDescriptor("task_dependency_list_as_dependent", "TaskDependency").local("id").foreign("dependent").many()).relation(RelationDescriptor("task_dependency_list_as_blocker", "TaskDependency").local("id").foreign("blocker").many()).relation(RelationDescriptor("task_placement_list", "TaskPlacement").local("id").foreign("task").many()).relation(RelationDescriptor("recurrence_link_list_as_source_task", "RecurrenceLink").local("id").foreign("source_task").many()).relation(RelationDescriptor("recurrence_link_list_as_next_task", "RecurrenceLink").local("id").foreign("next_task").many()).relation(RelationDescriptor("task_event_list_as_task", "TaskEvent").local("id").foreign("task").many()).relation(RelationDescriptor("task_event_list_as_related_task", "TaskEvent").local("id").foreign("related_task").many()).relation(RelationDescriptor("task_participant_list", "TaskParticipant").local("id").foreign("task").many()).relation(RelationDescriptor("deleted_task_viewer_list", "DeletedTaskViewer").local("id").foreign("task").many()).relation(RelationDescriptor("inbox_notice_list", "InboxNotice").local("id").foreign("task").many())
)

_ProjectField_DESCRIPTOR = (EntityDescriptor("ProjectField")
    .audit_mask_fields([])
    .table_name("project_field_data").property(PropertyDescriptor("id", DataType.I64).column_name("id").log_policy("plain").is_id().required()).property(PropertyDescriptor("work_space", DataType.I64).column_name("work_space").log_policy("plain").required()).property(PropertyDescriptor("project", DataType.I64).column_name("project").log_policy("plain").required()).property(PropertyDescriptor("field_name", DataType.Text).column_name("field_name").log_policy("plain").required()).property(PropertyDescriptor("version", DataType.I64).column_name("version").log_policy("plain").is_version().required()).relation(RelationDescriptor("work_space", "WorkSpace").local("work_space").foreign("id")).relation(RelationDescriptor("project", "WorkProject").local("project").foreign("id")).relation(RelationDescriptor("field_option_list", "FieldOption").local("id").foreign("field").many()).relation(RelationDescriptor("task_field_choice_list", "TaskFieldChoice").local("id").foreign("field").many()).relation(RelationDescriptor("blueprint_choice_list", "BlueprintChoice").local("id").foreign("field").many())
)

_FieldOption_DESCRIPTOR = (EntityDescriptor("FieldOption")
    .audit_mask_fields([])
    .table_name("field_option_data").property(PropertyDescriptor("id", DataType.I64).column_name("id").log_policy("plain").is_id().required()).property(PropertyDescriptor("work_space", DataType.I64).column_name("work_space").log_policy("plain").required()).property(PropertyDescriptor("field", DataType.I64).column_name("field").log_policy("plain").required()).property(PropertyDescriptor("option_name", DataType.Text).column_name("option_name").log_policy("plain").required()).property(PropertyDescriptor("option_order", DataType.I64).column_name("option_order").log_policy("plain").required()).property(PropertyDescriptor("version", DataType.I64).column_name("version").log_policy("plain").is_version().required()).relation(RelationDescriptor("work_space", "WorkSpace").local("work_space").foreign("id")).relation(RelationDescriptor("field", "ProjectField").local("field").foreign("id")).relation(RelationDescriptor("task_field_choice_list", "TaskFieldChoice").local("id").foreign("selected_option").many()).relation(RelationDescriptor("blueprint_choice_list", "BlueprintChoice").local("id").foreign("selected_option").many())
)

_TaskFieldChoice_DESCRIPTOR = (EntityDescriptor("TaskFieldChoice")
    .audit_mask_fields([])
    .table_name("task_field_choice_data").property(PropertyDescriptor("id", DataType.I64).column_name("id").log_policy("plain").is_id().required()).property(PropertyDescriptor("work_space", DataType.I64).column_name("work_space").log_policy("plain").required()).property(PropertyDescriptor("task", DataType.I64).column_name("task").log_policy("plain").required()).property(PropertyDescriptor("field", DataType.I64).column_name("field").log_policy("plain").required()).property(PropertyDescriptor("selected_option", DataType.I64).column_name("selected_option").log_policy("plain").required()).property(PropertyDescriptor("version", DataType.I64).column_name("version").log_policy("plain").is_version().required()).relation(RelationDescriptor("work_space", "WorkSpace").local("work_space").foreign("id")).relation(RelationDescriptor("task", "WorkTask").local("task").foreign("id")).relation(RelationDescriptor("field", "ProjectField").local("field").foreign("id")).relation(RelationDescriptor("selected_option", "FieldOption").local("selected_option").foreign("id"))
)

_WorkSubtask_DESCRIPTOR = (EntityDescriptor("WorkSubtask")
    .audit_mask_fields([])
    .table_name("work_subtask_data").property(PropertyDescriptor("id", DataType.I64).column_name("id").log_policy("plain").is_id().required()).property(PropertyDescriptor("work_space", DataType.I64).column_name("work_space").log_policy("plain").required()).property(PropertyDescriptor("task", DataType.I64).column_name("task").log_policy("plain").required()).property(PropertyDescriptor("subtask_title", DataType.Text).column_name("subtask_title").log_policy("plain").required()).property(PropertyDescriptor("assignee", DataType.I64).column_name("assignee").log_policy("plain")).property(PropertyDescriptor("due_date", DataType.Date).column_name("due_date").log_policy("plain")).property(PropertyDescriptor("completed", DataType.Bool).column_name("completed").log_policy("plain").required()).property(PropertyDescriptor("version", DataType.I64).column_name("version").log_policy("plain").is_version().required()).relation(RelationDescriptor("work_space", "WorkSpace").local("work_space").foreign("id")).relation(RelationDescriptor("task", "WorkTask").local("task").foreign("id")).relation(RelationDescriptor("assignee", "WorkAccount").local("assignee").foreign("id"))
)

_TaskComment_DESCRIPTOR = (EntityDescriptor("TaskComment")
    .audit_mask_fields([])
    .table_name("task_comment_data").property(PropertyDescriptor("id", DataType.I64).column_name("id").log_policy("plain").is_id().required()).property(PropertyDescriptor("work_space", DataType.I64).column_name("work_space").log_policy("plain").required()).property(PropertyDescriptor("task", DataType.I64).column_name("task").log_policy("plain").required()).property(PropertyDescriptor("author", DataType.I64).column_name("author").log_policy("plain").required()).property(PropertyDescriptor("comment_text", DataType.Text).column_name("comment_text").log_policy("plain").required()).property(PropertyDescriptor("edited", DataType.Bool).column_name("edited").log_policy("plain").required()).property(PropertyDescriptor("create_time", DataType.Timestamp).column_name("create_time").log_policy("plain").required()).property(PropertyDescriptor("version", DataType.I64).column_name("version").log_policy("plain").is_version().required()).relation(RelationDescriptor("work_space", "WorkSpace").local("work_space").foreign("id")).relation(RelationDescriptor("task", "WorkTask").local("task").foreign("id")).relation(RelationDescriptor("author", "WorkAccount").local("author").foreign("id"))
)

_TaskDependency_DESCRIPTOR = (EntityDescriptor("TaskDependency")
    .audit_mask_fields([])
    .table_name("task_dependency_data").property(PropertyDescriptor("id", DataType.I64).column_name("id").log_policy("plain").is_id().required()).property(PropertyDescriptor("work_space", DataType.I64).column_name("work_space").log_policy("plain").required()).property(PropertyDescriptor("dependent", DataType.I64).column_name("dependent").log_policy("plain").required()).property(PropertyDescriptor("blocker", DataType.I64).column_name("blocker").log_policy("plain").required()).property(PropertyDescriptor("version", DataType.I64).column_name("version").log_policy("plain").is_version().required()).relation(RelationDescriptor("work_space", "WorkSpace").local("work_space").foreign("id")).relation(RelationDescriptor("dependent", "WorkTask").local("dependent").foreign("id")).relation(RelationDescriptor("blocker", "WorkTask").local("blocker").foreign("id"))
)

_TaskPlacement_DESCRIPTOR = (EntityDescriptor("TaskPlacement")
    .audit_mask_fields([])
    .table_name("task_placement_data").property(PropertyDescriptor("id", DataType.I64).column_name("id").log_policy("plain").is_id().required()).property(PropertyDescriptor("work_space", DataType.I64).column_name("work_space").log_policy("plain").required()).property(PropertyDescriptor("task", DataType.I64).column_name("task").log_policy("plain").required()).property(PropertyDescriptor("project", DataType.I64).column_name("project").log_policy("plain").required()).property(PropertyDescriptor("section", DataType.I64).column_name("section").log_policy("plain").required()).property(PropertyDescriptor("placement_order", DataType.I64).column_name("placement_order").log_policy("plain").required()).property(PropertyDescriptor("version", DataType.I64).column_name("version").log_policy("plain").is_version().required()).relation(RelationDescriptor("work_space", "WorkSpace").local("work_space").foreign("id")).relation(RelationDescriptor("task", "WorkTask").local("task").foreign("id")).relation(RelationDescriptor("project", "WorkProject").local("project").foreign("id")).relation(RelationDescriptor("section", "ProjectSection").local("section").foreign("id"))
)

_RecurrenceLink_DESCRIPTOR = (EntityDescriptor("RecurrenceLink")
    .audit_mask_fields([])
    .table_name("recurrence_link_data").property(PropertyDescriptor("id", DataType.I64).column_name("id").log_policy("plain").is_id().required()).property(PropertyDescriptor("work_space", DataType.I64).column_name("work_space").log_policy("plain").required()).property(PropertyDescriptor("source_task", DataType.I64).column_name("source_task").log_policy("plain").required()).property(PropertyDescriptor("next_task", DataType.I64).column_name("next_task").log_policy("plain").required()).property(PropertyDescriptor("version", DataType.I64).column_name("version").log_policy("plain").is_version().required()).relation(RelationDescriptor("work_space", "WorkSpace").local("work_space").foreign("id")).relation(RelationDescriptor("source_task", "WorkTask").local("source_task").foreign("id")).relation(RelationDescriptor("next_task", "WorkTask").local("next_task").foreign("id"))
)

_TaskEvent_DESCRIPTOR = (EntityDescriptor("TaskEvent")
    .audit_mask_fields([])
    .table_name("task_event_data").property(PropertyDescriptor("id", DataType.I64).column_name("id").log_policy("plain").is_id().required()).property(PropertyDescriptor("work_space", DataType.I64).column_name("work_space").log_policy("plain").required()).property(PropertyDescriptor("task", DataType.I64).column_name("task").log_policy("plain").required()).property(PropertyDescriptor("actor", DataType.I64).column_name("actor").log_policy("plain").required()).property(PropertyDescriptor("scope_project", DataType.I64).column_name("scope_project").log_policy("plain")).property(PropertyDescriptor("related_task", DataType.I64).column_name("related_task").log_policy("plain")).property(PropertyDescriptor("event_kind", DataType.Text).column_name("event_kind").log_policy("plain").required()).property(PropertyDescriptor("field_label", DataType.Text).column_name("field_label").log_policy("plain").required()).property(PropertyDescriptor("old_value", DataType.Text).column_name("old_value").log_policy("plain")).property(PropertyDescriptor("new_value", DataType.Text).column_name("new_value").log_policy("plain")).property(PropertyDescriptor("event_time", DataType.Timestamp).column_name("event_time").log_policy("plain").required()).property(PropertyDescriptor("version", DataType.I64).column_name("version").log_policy("plain").is_version().required()).relation(RelationDescriptor("work_space", "WorkSpace").local("work_space").foreign("id")).relation(RelationDescriptor("task", "WorkTask").local("task").foreign("id")).relation(RelationDescriptor("actor", "WorkAccount").local("actor").foreign("id")).relation(RelationDescriptor("scope_project", "WorkProject").local("scope_project").foreign("id")).relation(RelationDescriptor("related_task", "WorkTask").local("related_task").foreign("id")).relation(RelationDescriptor("inbox_notice_list", "InboxNotice").local("id").foreign("event").many())
)

_TaskParticipant_DESCRIPTOR = (EntityDescriptor("TaskParticipant")
    .audit_mask_fields([])
    .table_name("task_participant_data").property(PropertyDescriptor("id", DataType.I64).column_name("id").log_policy("plain").is_id().required()).property(PropertyDescriptor("work_space", DataType.I64).column_name("work_space").log_policy("plain").required()).property(PropertyDescriptor("task", DataType.I64).column_name("task").log_policy("plain").required()).property(PropertyDescriptor("participant", DataType.I64).column_name("participant").log_policy("plain").required()).property(PropertyDescriptor("version", DataType.I64).column_name("version").log_policy("plain").is_version().required()).relation(RelationDescriptor("work_space", "WorkSpace").local("work_space").foreign("id")).relation(RelationDescriptor("task", "WorkTask").local("task").foreign("id")).relation(RelationDescriptor("participant", "WorkAccount").local("participant").foreign("id"))
)

_DeletedTaskViewer_DESCRIPTOR = (EntityDescriptor("DeletedTaskViewer")
    .audit_mask_fields([])
    .table_name("deleted_task_viewer_data").property(PropertyDescriptor("id", DataType.I64).column_name("id").log_policy("plain").is_id().required()).property(PropertyDescriptor("work_space", DataType.I64).column_name("work_space").log_policy("plain").required()).property(PropertyDescriptor("task", DataType.I64).column_name("task").log_policy("plain").required()).property(PropertyDescriptor("viewer", DataType.I64).column_name("viewer").log_policy("plain").required()).property(PropertyDescriptor("version", DataType.I64).column_name("version").log_policy("plain").is_version().required()).relation(RelationDescriptor("work_space", "WorkSpace").local("work_space").foreign("id")).relation(RelationDescriptor("task", "WorkTask").local("task").foreign("id")).relation(RelationDescriptor("viewer", "WorkAccount").local("viewer").foreign("id"))
)

_TaskBlueprint_DESCRIPTOR = (EntityDescriptor("TaskBlueprint")
    .audit_mask_fields([])
    .table_name("task_blueprint_data").property(PropertyDescriptor("id", DataType.I64).column_name("id").log_policy("plain").is_id().required()).property(PropertyDescriptor("work_space", DataType.I64).column_name("work_space").log_policy("plain").required()).property(PropertyDescriptor("project", DataType.I64).column_name("project").log_policy("plain").required()).property(PropertyDescriptor("template_name", DataType.Text).column_name("template_name").log_policy("plain").required()).property(PropertyDescriptor("initial_title", DataType.Text).column_name("initial_title").log_policy("plain").required()).property(PropertyDescriptor("initial_description", DataType.Text).column_name("initial_description").log_policy("plain")).property(PropertyDescriptor("assignee", DataType.I64).column_name("assignee").log_policy("plain")).property(PropertyDescriptor("due_offset", DataType.I64).column_name("due_offset").log_policy("plain")).property(PropertyDescriptor("repeat_period", DataType.Text).column_name("repeat_period").log_policy("plain").required()).property(PropertyDescriptor("approval", DataType.Bool).column_name("approval").log_policy("plain").required()).property(PropertyDescriptor("version", DataType.I64).column_name("version").log_policy("plain").is_version().required()).relation(RelationDescriptor("work_space", "WorkSpace").local("work_space").foreign("id")).relation(RelationDescriptor("project", "WorkProject").local("project").foreign("id")).relation(RelationDescriptor("assignee", "WorkAccount").local("assignee").foreign("id")).relation(RelationDescriptor("blueprint_choice_list", "BlueprintChoice").local("id").foreign("blueprint").many()).relation(RelationDescriptor("blueprint_subtask_list", "BlueprintSubtask").local("id").foreign("blueprint").many())
)

_BlueprintChoice_DESCRIPTOR = (EntityDescriptor("BlueprintChoice")
    .audit_mask_fields([])
    .table_name("blueprint_choice_data").property(PropertyDescriptor("id", DataType.I64).column_name("id").log_policy("plain").is_id().required()).property(PropertyDescriptor("work_space", DataType.I64).column_name("work_space").log_policy("plain").required()).property(PropertyDescriptor("blueprint", DataType.I64).column_name("blueprint").log_policy("plain").required()).property(PropertyDescriptor("field", DataType.I64).column_name("field").log_policy("plain").required()).property(PropertyDescriptor("selected_option", DataType.I64).column_name("selected_option").log_policy("plain").required()).property(PropertyDescriptor("version", DataType.I64).column_name("version").log_policy("plain").is_version().required()).relation(RelationDescriptor("work_space", "WorkSpace").local("work_space").foreign("id")).relation(RelationDescriptor("blueprint", "TaskBlueprint").local("blueprint").foreign("id")).relation(RelationDescriptor("field", "ProjectField").local("field").foreign("id")).relation(RelationDescriptor("selected_option", "FieldOption").local("selected_option").foreign("id"))
)

_BlueprintSubtask_DESCRIPTOR = (EntityDescriptor("BlueprintSubtask")
    .audit_mask_fields([])
    .table_name("blueprint_subtask_data").property(PropertyDescriptor("id", DataType.I64).column_name("id").log_policy("plain").is_id().required()).property(PropertyDescriptor("work_space", DataType.I64).column_name("work_space").log_policy("plain").required()).property(PropertyDescriptor("blueprint", DataType.I64).column_name("blueprint").log_policy("plain").required()).property(PropertyDescriptor("subtask_title", DataType.Text).column_name("subtask_title").log_policy("plain").required()).property(PropertyDescriptor("assignee", DataType.I64).column_name("assignee").log_policy("plain")).property(PropertyDescriptor("due_offset", DataType.I64).column_name("due_offset").log_policy("plain")).property(PropertyDescriptor("version", DataType.I64).column_name("version").log_policy("plain").is_version().required()).relation(RelationDescriptor("work_space", "WorkSpace").local("work_space").foreign("id")).relation(RelationDescriptor("blueprint", "TaskBlueprint").local("blueprint").foreign("id")).relation(RelationDescriptor("assignee", "WorkAccount").local("assignee").foreign("id"))
)

_InboxNotice_DESCRIPTOR = (EntityDescriptor("InboxNotice")
    .audit_mask_fields([])
    .table_name("inbox_notice_data").property(PropertyDescriptor("id", DataType.I64).column_name("id").log_policy("plain").is_id().required()).property(PropertyDescriptor("work_space", DataType.I64).column_name("work_space").log_policy("plain").required()).property(PropertyDescriptor("task", DataType.I64).column_name("task").log_policy("plain").required()).property(PropertyDescriptor("recipient", DataType.I64).column_name("recipient").log_policy("plain").required()).property(PropertyDescriptor("event", DataType.I64).column_name("event").log_policy("plain").required()).property(PropertyDescriptor("read_flag", DataType.Bool).column_name("read_flag").log_policy("plain").required()).property(PropertyDescriptor("version", DataType.I64).column_name("version").log_policy("plain").is_version().required()).relation(RelationDescriptor("work_space", "WorkSpace").local("work_space").foreign("id")).relation(RelationDescriptor("task", "WorkTask").local("task").foreign("id")).relation(RelationDescriptor("recipient", "WorkAccount").local("recipient").foreign("id")).relation(RelationDescriptor("event", "TaskEvent").local("event").foreign("id"))
)

async def _ensure_generated_bootstrap_once(context):
    previous_actor = context.user_identifier() if hasattr(context, 'user_identifier') else None
    previous_category = context.get_resource('bootstrapCategory')
    if hasattr(context, 'set_user_identifier'):
        context.set_user_identifier('teaql-generated-bootstrap')
    context.insert_resource('bootstrapCategory', 'runtime-bootstrap')
    try:
        work_space_1 = await (Q.work_spaces().with_id_is(1).comment('what: locate generated bootstrap entity').purpose('why: idempotent runtime bootstrap').execute_for_one(context))
        if work_space_1 is None:
            work_space_1 = WorkSpace._teaql_new_with_fixed_id(1)
            work_space_1.update_workspace_name("Shared workspace")
            try:
                await work_space_1.audit_as('create model root WorkSpace(1)').save(context)
            except Exception as _teaql_create_error:
                for _teaql_attempt in range(5):
                    work_space_1 = await (Q.work_spaces().with_id_is(1).comment('what: recover concurrent bootstrap').purpose('why: make generated bootstrap idempotent').execute_for_one(context))
                    if work_space_1 is not None:
                        break
                    if _teaql_attempt < 4:
                        await asyncio.sleep((_teaql_attempt + 1) * 0.01)
                if work_space_1 is None:
                    raise _teaql_create_error
        context.with_active_root(ContextEntityRef("WorkSpace", 1))
    finally:
        if hasattr(context, 'set_user_identifier'):
            context.set_user_identifier(previous_actor)
        context.insert_resource('bootstrapCategory', previous_category)

async def _ensure_generated_bootstrap(context):
    for _teaql_attempt in range(5):
        try:
            await _ensure_generated_bootstrap_once(context)
            return
        except Exception:
            if _teaql_attempt == 4:
                raise
            await asyncio.sleep((_teaql_attempt + 1) * 0.01)


# Passive generated manifest. Call ensure_schema() separately and explicitly.
GENERATED_RUNTIME_MODULE = (RuntimeModule().entity(WorkSpace)
    .schema_entity(_WorkSpace_DESCRIPTOR)
    .checker("WorkSpace", _WorkSpaceChecker())
    .wire_metadata("WorkSpace", create_wire_entity_metadata("WorkSpace", ["id", "workspace_name", "version"], JsonFieldNamingProfile.CAMEL_CASE, {"id": ["id"], "workspace_name": ["workspace_name"], "version": ["version"]})).entity(WorkAccount)
    .schema_entity(_WorkAccount_DESCRIPTOR)
    .checker("WorkAccount", _WorkAccountChecker())
    .wire_metadata("WorkAccount", create_wire_entity_metadata("WorkAccount", ["id", "work_space", "display_name", "email_address", "password_hash", "version"], JsonFieldNamingProfile.CAMEL_CASE, {"id": ["id"], "work_space": ["work_space"], "display_name": ["display_name"], "email_address": ["email_address"], "password_hash": ["password_hash"], "version": ["version"]})).entity(WorkProject)
    .schema_entity(_WorkProject_DESCRIPTOR)
    .checker("WorkProject", _WorkProjectChecker())
    .wire_metadata("WorkProject", create_wire_entity_metadata("WorkProject", ["id", "work_space", "owner_account", "project_name", "shift_dates", "version"], JsonFieldNamingProfile.CAMEL_CASE, {"id": ["id"], "work_space": ["work_space"], "owner_account": ["owner_account"], "project_name": ["project_name"], "shift_dates": ["shift_dates"], "version": ["version"]})).entity(ProjectMembership)
    .schema_entity(_ProjectMembership_DESCRIPTOR)
    .checker("ProjectMembership", _ProjectMembershipChecker())
    .wire_metadata("ProjectMembership", create_wire_entity_metadata("ProjectMembership", ["id", "work_space", "project", "member_account", "access_role", "version"], JsonFieldNamingProfile.CAMEL_CASE, {"id": ["id"], "work_space": ["work_space"], "project": ["project"], "member_account": ["member_account"], "access_role": ["access_role"], "version": ["version"]})).entity(ProjectSection)
    .schema_entity(_ProjectSection_DESCRIPTOR)
    .checker("ProjectSection", _ProjectSectionChecker())
    .wire_metadata("ProjectSection", create_wire_entity_metadata("ProjectSection", ["id", "work_space", "project", "section_name", "section_order", "default_section", "version"], JsonFieldNamingProfile.CAMEL_CASE, {"id": ["id"], "work_space": ["work_space"], "project": ["project"], "section_name": ["section_name"], "section_order": ["section_order"], "default_section": ["default_section"], "version": ["version"]})).entity(WorkTask)
    .schema_entity(_WorkTask_DESCRIPTOR)
    .checker("WorkTask", _WorkTaskChecker())
    .wire_metadata("WorkTask", create_wire_entity_metadata("WorkTask", ["id", "work_space", "project", "section", "deleted_epoch", "approval", "decision", "repeat_period", "created_by", "primary_detached", "task_order", "task_title", "description", "assignee", "start_date", "due_date", "completed", "version"], JsonFieldNamingProfile.CAMEL_CASE, {"id": ["id"], "work_space": ["work_space"], "project": ["project"], "section": ["section"], "deleted_epoch": ["deleted_epoch"], "approval": ["approval"], "decision": ["decision"], "repeat_period": ["repeat_period"], "created_by": ["created_by"], "primary_detached": ["primary_detached"], "task_order": ["task_order"], "task_title": ["task_title"], "description": ["description"], "assignee": ["assignee"], "start_date": ["start_date"], "due_date": ["due_date"], "completed": ["completed"], "version": ["version"]})).entity(ProjectField)
    .schema_entity(_ProjectField_DESCRIPTOR)
    .checker("ProjectField", _ProjectFieldChecker())
    .wire_metadata("ProjectField", create_wire_entity_metadata("ProjectField", ["id", "work_space", "project", "field_name", "version"], JsonFieldNamingProfile.CAMEL_CASE, {"id": ["id"], "work_space": ["work_space"], "project": ["project"], "field_name": ["field_name"], "version": ["version"]})).entity(FieldOption)
    .schema_entity(_FieldOption_DESCRIPTOR)
    .checker("FieldOption", _FieldOptionChecker())
    .wire_metadata("FieldOption", create_wire_entity_metadata("FieldOption", ["id", "work_space", "field", "option_name", "option_order", "version"], JsonFieldNamingProfile.CAMEL_CASE, {"id": ["id"], "work_space": ["work_space"], "field": ["field"], "option_name": ["option_name"], "option_order": ["option_order"], "version": ["version"]})).entity(TaskFieldChoice)
    .schema_entity(_TaskFieldChoice_DESCRIPTOR)
    .checker("TaskFieldChoice", _TaskFieldChoiceChecker())
    .wire_metadata("TaskFieldChoice", create_wire_entity_metadata("TaskFieldChoice", ["id", "work_space", "task", "field", "selected_option", "version"], JsonFieldNamingProfile.CAMEL_CASE, {"id": ["id"], "work_space": ["work_space"], "task": ["task"], "field": ["field"], "selected_option": ["selected_option"], "version": ["version"]})).entity(WorkSubtask)
    .schema_entity(_WorkSubtask_DESCRIPTOR)
    .checker("WorkSubtask", _WorkSubtaskChecker())
    .wire_metadata("WorkSubtask", create_wire_entity_metadata("WorkSubtask", ["id", "work_space", "task", "subtask_title", "assignee", "due_date", "completed", "version"], JsonFieldNamingProfile.CAMEL_CASE, {"id": ["id"], "work_space": ["work_space"], "task": ["task"], "subtask_title": ["subtask_title"], "assignee": ["assignee"], "due_date": ["due_date"], "completed": ["completed"], "version": ["version"]})).entity(TaskComment)
    .schema_entity(_TaskComment_DESCRIPTOR)
    .checker("TaskComment", _TaskCommentChecker())
    .wire_metadata("TaskComment", create_wire_entity_metadata("TaskComment", ["id", "work_space", "task", "author", "comment_text", "edited", "create_time", "version"], JsonFieldNamingProfile.CAMEL_CASE, {"id": ["id"], "work_space": ["work_space"], "task": ["task"], "author": ["author"], "comment_text": ["comment_text"], "edited": ["edited"], "create_time": ["create_time"], "version": ["version"]})).entity(TaskDependency)
    .schema_entity(_TaskDependency_DESCRIPTOR)
    .checker("TaskDependency", _TaskDependencyChecker())
    .wire_metadata("TaskDependency", create_wire_entity_metadata("TaskDependency", ["id", "work_space", "dependent", "blocker", "version"], JsonFieldNamingProfile.CAMEL_CASE, {"id": ["id"], "work_space": ["work_space"], "dependent": ["dependent"], "blocker": ["blocker"], "version": ["version"]})).entity(TaskPlacement)
    .schema_entity(_TaskPlacement_DESCRIPTOR)
    .checker("TaskPlacement", _TaskPlacementChecker())
    .wire_metadata("TaskPlacement", create_wire_entity_metadata("TaskPlacement", ["id", "work_space", "task", "project", "section", "placement_order", "version"], JsonFieldNamingProfile.CAMEL_CASE, {"id": ["id"], "work_space": ["work_space"], "task": ["task"], "project": ["project"], "section": ["section"], "placement_order": ["placement_order"], "version": ["version"]})).entity(RecurrenceLink)
    .schema_entity(_RecurrenceLink_DESCRIPTOR)
    .checker("RecurrenceLink", _RecurrenceLinkChecker())
    .wire_metadata("RecurrenceLink", create_wire_entity_metadata("RecurrenceLink", ["id", "work_space", "source_task", "next_task", "version"], JsonFieldNamingProfile.CAMEL_CASE, {"id": ["id"], "work_space": ["work_space"], "source_task": ["source_task"], "next_task": ["next_task"], "version": ["version"]})).entity(TaskEvent)
    .schema_entity(_TaskEvent_DESCRIPTOR)
    .checker("TaskEvent", _TaskEventChecker())
    .wire_metadata("TaskEvent", create_wire_entity_metadata("TaskEvent", ["id", "work_space", "task", "actor", "scope_project", "related_task", "event_kind", "field_label", "old_value", "new_value", "event_time", "version"], JsonFieldNamingProfile.CAMEL_CASE, {"id": ["id"], "work_space": ["work_space"], "task": ["task"], "actor": ["actor"], "scope_project": ["scope_project"], "related_task": ["related_task"], "event_kind": ["event_kind"], "field_label": ["field_label"], "old_value": ["old_value"], "new_value": ["new_value"], "event_time": ["event_time"], "version": ["version"]})).entity(TaskParticipant)
    .schema_entity(_TaskParticipant_DESCRIPTOR)
    .checker("TaskParticipant", _TaskParticipantChecker())
    .wire_metadata("TaskParticipant", create_wire_entity_metadata("TaskParticipant", ["id", "work_space", "task", "participant", "version"], JsonFieldNamingProfile.CAMEL_CASE, {"id": ["id"], "work_space": ["work_space"], "task": ["task"], "participant": ["participant"], "version": ["version"]})).entity(DeletedTaskViewer)
    .schema_entity(_DeletedTaskViewer_DESCRIPTOR)
    .checker("DeletedTaskViewer", _DeletedTaskViewerChecker())
    .wire_metadata("DeletedTaskViewer", create_wire_entity_metadata("DeletedTaskViewer", ["id", "work_space", "task", "viewer", "version"], JsonFieldNamingProfile.CAMEL_CASE, {"id": ["id"], "work_space": ["work_space"], "task": ["task"], "viewer": ["viewer"], "version": ["version"]})).entity(TaskBlueprint)
    .schema_entity(_TaskBlueprint_DESCRIPTOR)
    .checker("TaskBlueprint", _TaskBlueprintChecker())
    .wire_metadata("TaskBlueprint", create_wire_entity_metadata("TaskBlueprint", ["id", "work_space", "project", "template_name", "initial_title", "initial_description", "assignee", "due_offset", "repeat_period", "approval", "version"], JsonFieldNamingProfile.CAMEL_CASE, {"id": ["id"], "work_space": ["work_space"], "project": ["project"], "template_name": ["template_name"], "initial_title": ["initial_title"], "initial_description": ["initial_description"], "assignee": ["assignee"], "due_offset": ["due_offset"], "repeat_period": ["repeat_period"], "approval": ["approval"], "version": ["version"]})).entity(BlueprintChoice)
    .schema_entity(_BlueprintChoice_DESCRIPTOR)
    .checker("BlueprintChoice", _BlueprintChoiceChecker())
    .wire_metadata("BlueprintChoice", create_wire_entity_metadata("BlueprintChoice", ["id", "work_space", "blueprint", "field", "selected_option", "version"], JsonFieldNamingProfile.CAMEL_CASE, {"id": ["id"], "work_space": ["work_space"], "blueprint": ["blueprint"], "field": ["field"], "selected_option": ["selected_option"], "version": ["version"]})).entity(BlueprintSubtask)
    .schema_entity(_BlueprintSubtask_DESCRIPTOR)
    .checker("BlueprintSubtask", _BlueprintSubtaskChecker())
    .wire_metadata("BlueprintSubtask", create_wire_entity_metadata("BlueprintSubtask", ["id", "work_space", "blueprint", "subtask_title", "assignee", "due_offset", "version"], JsonFieldNamingProfile.CAMEL_CASE, {"id": ["id"], "work_space": ["work_space"], "blueprint": ["blueprint"], "subtask_title": ["subtask_title"], "assignee": ["assignee"], "due_offset": ["due_offset"], "version": ["version"]})).entity(InboxNotice)
    .schema_entity(_InboxNotice_DESCRIPTOR)
    .checker("InboxNotice", _InboxNoticeChecker())
    .wire_metadata("InboxNotice", create_wire_entity_metadata("InboxNotice", ["id", "work_space", "task", "recipient", "event", "read_flag", "version"], JsonFieldNamingProfile.CAMEL_CASE, {"id": ["id"], "work_space": ["work_space"], "task": ["task"], "recipient": ["recipient"], "event": ["event"], "read_flag": ["read_flag"], "version": ["version"]}))
    .generated_bootstrap(_ensure_generated_bootstrap)
)