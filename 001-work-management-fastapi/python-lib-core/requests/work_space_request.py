from teaql.core.query import RelationAggregate, SelectQuery
from teaql.core.list import SmartList, TeaQLPage
from teaql.runtime import EntityRoot, UserContext
from teaql.data_service import QueryRequest
from copy import deepcopy
from teaql.core.expr import (
    begin_with, between, column, contain, end_with, eq, gt, gte,
    in_list, in_subquery, is_not_null, is_null, lt, lte, ne, not_begin_with,
    not_contain, not_end_with, not_in_list, not_in_subquery, value,
    sound_like,
)
from models.work_space import WorkSpace
from typing import Protocol

def _set_arguments(method, values):
    for item in values:
        if isinstance(item, (list, tuple, set, frozenset, dict)):
            raise TypeError(f"{method} expects positional scalar values; use {method}(*values) to unpack a collection, or {method}(value) for one value")
    return values

def _data_service(context):
    if not isinstance(context, UserContext):
        raise TypeError("Query execution requires exactly one UserContext; pass execute_for_list(context) or execute_for_one(context)")
    if context.get_resource("dataService") is None:
        raise RuntimeError("UserContext is missing dataService; install the trusted service with context.insert_resource('dataService', service). FastAPI workspaces also expose sqlite_context(service). Inside BusinessOperation use its supplied callback context")
    return context.require_resource("dataService")

class QuerySelection(Protocol):
    query: SelectQuery

class WorkSpaceRequest:
    def __init__(self, minimal=False):
        self.query = SelectQuery("WorkSpace")
        self._purpose = None
        self._comment = None
        self.query.and_filter(gte("version", 1))
        if minimal:
            self.select_id()
            self.select_version()
        else:
            self.select_self_fields()

    def comment(self, c: str):
        self.query.comment(c)
        self._comment = c
        return self

    def purpose(self, p: str):
        self.query.purpose(p)
        self._purpose = p
        return ExecutableWorkSpaceRequest(self)

    def optimize_for_continuous_page_fetch(self):
        self.query.optimize_for_continuous_page_fetch()
        return self

    def optimize_for_continuous_page_fetch_with(self, namespace: str, ttl_seconds: int):
        self.query.optimize_for_continuous_page_fetch_with(namespace, ttl_seconds)
        return self

    def optimize_pagination_with_id_set(self):
        self.query.optimize_pagination_with_id_set()
        return self

    def optimize_pagination_with_id_set_config(self, namespace: str, ttl_seconds: int, max_ids: int):
        self.query.optimize_pagination_with_id_set_config(namespace, ttl_seconds, max_ids)
        return self

    def top_n_probe_parent_threshold(self, threshold: int):
        self.query.top_n_probe_parent_threshold(threshold)
        return self

    def limit(self, n: int):
        self.query.limit(n)
        return self

    def offset(self, n: int):
        self.query.offset(n)
        return self

    def with_deleted_rows(self):
        self.query.with_deleted_rows()
        return self

    def deleted_rows_only(self):
        self.query.deleted_rows_only()
        return self

    def select_self_fields(self):
        self.query.project("id", "workspace_name", "version")
        return self

    def select_id(self):
        self.query.project("id")
        return self

    def select_workspace_name(self):
        self.query.project("workspace_name")
        return self

    def select_version(self):
        self.query.project("version")
        return self


    def with_id_is(self, val):
        if isinstance(val, (list, tuple, set, frozenset, dict)):
            raise TypeError("with_id_is expects one scalar ID; use with_id_in(*values) for a collection")
        self.query.and_filter(eq("id", val))
        return self

    def with_id_is_not(self, val):
        if isinstance(val, (list, tuple, set, frozenset, dict)):
            raise TypeError("with_id_is_not expects one scalar ID; use with_id_not_in(*values) for a collection")
        self.query.and_filter(ne("id", val))
        return self

    def with_id_in(self, *vals):
        _set_arguments("with_id_in", vals)
        if not vals:
            self.query.and_filter(is_null(column("id")))
            return self
        self.query.and_filter(in_list("id", list(vals)))
        return self

    def with_id_not_in(self, *vals):
        _set_arguments("with_id_not_in", vals)
        if not vals:
            return self
        self.query.and_filter(not_in_list("id", list(vals)))
        return self

    def with_id_greater_than(self, val):
        self.query.and_filter(gt("id", val))
        return self

    def with_id_greater_than_or_equal_to(self, val):
        self.query.and_filter(gte("id", val))
        return self

    def with_id_less_than(self, val):
        self.query.and_filter(lt("id", val))
        return self

    def with_id_less_than_or_equal_to(self, val):
        self.query.and_filter(lte("id", val))
        return self

    def with_id_between(self, lower, upper):
        self.query.and_filter(between(column("id"), value(lower), value(upper)))
        return self

    def with_id_is_known(self):
        self.query.and_filter(is_not_null(column("id")))
        return self

    def with_id_is_unknown(self):
        self.query.and_filter(is_null(column("id")))
        return self

    def with_workspace_name_containing(self, val: str):
        self.query.and_filter(contain("workspace_name", val))
        return self

    def with_workspace_name_not_containing(self, val: str):
        self.query.and_filter(not_contain("workspace_name", val))
        return self

    def with_workspace_name_starting_with(self, val: str):
        self.query.and_filter(begin_with("workspace_name", val))
        return self

    def with_workspace_name_not_starting_with(self, val: str):
        self.query.and_filter(not_begin_with("workspace_name", val))
        return self

    def with_workspace_name_ending_with(self, val: str):
        self.query.and_filter(end_with("workspace_name", val))
        return self

    def with_workspace_name_not_ending_with(self, val: str):
        self.query.and_filter(not_end_with("workspace_name", val))
        return self

    def with_workspace_name_sounding_like(self, val: str):
        self.query.and_filter(sound_like("workspace_name", val))
        return self

    def with_workspace_name_is(self, val: str):
        self.query.and_filter(eq("workspace_name", val))
        return self
    def with_workspace_name_is_not(self, val):
        self.query.and_filter(ne("workspace_name", val))
        return self

    def with_workspace_name_in(self, *vals):
        _set_arguments("with_workspace_name_in", vals)
        if not vals:
            self.query.and_filter(is_null(column("id")))
            return self
        self.query.and_filter(in_list("workspace_name", list(vals)))
        return self

    def with_workspace_name_not_in(self, *vals):
        _set_arguments("with_workspace_name_not_in", vals)
        if not vals:
            return self
        self.query.and_filter(not_in_list("workspace_name", list(vals)))
        return self

    def with_workspace_name_greater_than(self, val):
        self.query.and_filter(gt("workspace_name", val))
        return self

    def with_workspace_name_greater_than_or_equal_to(self, val):
        self.query.and_filter(gte("workspace_name", val))
        return self

    def with_workspace_name_less_than(self, val):
        self.query.and_filter(lt("workspace_name", val))
        return self

    def with_workspace_name_less_than_or_equal_to(self, val):
        self.query.and_filter(lte("workspace_name", val))
        return self

    def with_workspace_name_between(self, lower, upper):
        self.query.and_filter(between(column("workspace_name"), value(lower), value(upper)))
        return self

    def with_workspace_name_is_known(self):
        self.query.and_filter(is_not_null(column("workspace_name")))
        return self

    def with_workspace_name_is_unknown(self):
        self.query.and_filter(is_null(column("workspace_name")))
        return self

    def with_version_is(self, val):
        self.query.and_filter(eq("version", val))
        return self

    def with_version_is_not(self, val):
        self.query.and_filter(ne("version", val))
        return self

    def with_version_in(self, *vals):
        _set_arguments("with_version_in", vals)
        if not vals:
            self.query.and_filter(is_null(column("id")))
            return self
        self.query.and_filter(in_list("version", list(vals)))
        return self

    def with_version_not_in(self, *vals):
        _set_arguments("with_version_not_in", vals)
        if not vals:
            return self
        self.query.and_filter(not_in_list("version", list(vals)))
        return self

    def with_version_greater_than(self, val):
        self.query.and_filter(gt("version", val))
        return self

    def with_version_greater_than_or_equal_to(self, val):
        self.query.and_filter(gte("version", val))
        return self

    def with_version_less_than(self, val):
        self.query.and_filter(lt("version", val))
        return self

    def with_version_less_than_or_equal_to(self, val):
        self.query.and_filter(lte("version", val))
        return self

    def with_version_between(self, lower, upper):
        self.query.and_filter(between(column("version"), value(lower), value(upper)))
        return self

    def with_version_is_known(self):
        self.query.and_filter(is_not_null(column("version")))
        return self

    def with_version_is_unknown(self):
        self.query.and_filter(is_null(column("version")))
        return self

    def order_by_id_ascending(self):
        self.query.order_by("id", "asc")
        return self

    def order_by_id_descending(self):
        self.query.order_by("id", "desc")
        return self

    def order_by_workspace_name_ascending(self):
        self.query.order_by("workspace_name", "asc")
        return self

    def order_by_workspace_name_descending(self):
        self.query.order_by("workspace_name", "desc")
        return self

    def order_by_version_ascending(self):
        self.query.order_by("version", "asc")
        return self

    def order_by_version_descending(self):
        self.query.order_by("version", "desc")
        return self


    def count(self):
        self.query.count_field("id", "count")
        return self

    def count_as(self, ret_name: str):
        self.query.count_field("id", ret_name)
        return self

    def group_by_id(self):
        self.query.group_by("id")
        return self

    def group_by_id_as(self, ret_name: str):
        self.query.group_by("id")
        return self
    def group_by_workspace_name(self):
        self.query.group_by("workspace_name")
        return self

    def group_by_workspace_name_as(self, ret_name: str):
        self.query.group_by("workspace_name")
        return self
    def group_by_version(self):
        self.query.group_by("version")
        return self

    def group_by_version_as(self, ret_name: str):
        self.query.group_by("version")
        return self
    def select_work_account_list(self):
        from requests.work_account_request import WorkAccountRequest
        return self.select_work_account_list_with(WorkAccountRequest())

    def select_work_account_list_with(self, child_request):
        self.query.relation_query("work_account_list", child_request.query)
        return self
    def select_work_project_list(self):
        from requests.work_project_request import WorkProjectRequest
        return self.select_work_project_list_with(WorkProjectRequest())

    def select_work_project_list_with(self, child_request):
        self.query.relation_query("work_project_list", child_request.query)
        return self
    def select_project_membership_list(self):
        from requests.project_membership_request import ProjectMembershipRequest
        return self.select_project_membership_list_with(ProjectMembershipRequest())

    def select_project_membership_list_with(self, child_request):
        self.query.relation_query("project_membership_list", child_request.query)
        return self
    def select_project_section_list(self):
        from requests.project_section_request import ProjectSectionRequest
        return self.select_project_section_list_with(ProjectSectionRequest())

    def select_project_section_list_with(self, child_request):
        self.query.relation_query("project_section_list", child_request.query)
        return self
    def select_work_task_list(self):
        from requests.work_task_request import WorkTaskRequest
        return self.select_work_task_list_with(WorkTaskRequest())

    def select_work_task_list_with(self, child_request):
        self.query.relation_query("work_task_list", child_request.query)
        return self
    def select_project_field_list(self):
        from requests.project_field_request import ProjectFieldRequest
        return self.select_project_field_list_with(ProjectFieldRequest())

    def select_project_field_list_with(self, child_request):
        self.query.relation_query("project_field_list", child_request.query)
        return self
    def select_field_option_list(self):
        from requests.field_option_request import FieldOptionRequest
        return self.select_field_option_list_with(FieldOptionRequest())

    def select_field_option_list_with(self, child_request):
        self.query.relation_query("field_option_list", child_request.query)
        return self
    def select_task_field_choice_list(self):
        from requests.task_field_choice_request import TaskFieldChoiceRequest
        return self.select_task_field_choice_list_with(TaskFieldChoiceRequest())

    def select_task_field_choice_list_with(self, child_request):
        self.query.relation_query("task_field_choice_list", child_request.query)
        return self
    def select_work_subtask_list(self):
        from requests.work_subtask_request import WorkSubtaskRequest
        return self.select_work_subtask_list_with(WorkSubtaskRequest())

    def select_work_subtask_list_with(self, child_request):
        self.query.relation_query("work_subtask_list", child_request.query)
        return self
    def select_task_comment_list(self):
        from requests.task_comment_request import TaskCommentRequest
        return self.select_task_comment_list_with(TaskCommentRequest())

    def select_task_comment_list_with(self, child_request):
        self.query.relation_query("task_comment_list", child_request.query)
        return self
    def select_task_dependency_list(self):
        from requests.task_dependency_request import TaskDependencyRequest
        return self.select_task_dependency_list_with(TaskDependencyRequest())

    def select_task_dependency_list_with(self, child_request):
        self.query.relation_query("task_dependency_list", child_request.query)
        return self
    def select_task_placement_list(self):
        from requests.task_placement_request import TaskPlacementRequest
        return self.select_task_placement_list_with(TaskPlacementRequest())

    def select_task_placement_list_with(self, child_request):
        self.query.relation_query("task_placement_list", child_request.query)
        return self
    def select_recurrence_link_list(self):
        from requests.recurrence_link_request import RecurrenceLinkRequest
        return self.select_recurrence_link_list_with(RecurrenceLinkRequest())

    def select_recurrence_link_list_with(self, child_request):
        self.query.relation_query("recurrence_link_list", child_request.query)
        return self
    def select_task_event_list(self):
        from requests.task_event_request import TaskEventRequest
        return self.select_task_event_list_with(TaskEventRequest())

    def select_task_event_list_with(self, child_request):
        self.query.relation_query("task_event_list", child_request.query)
        return self
    def select_task_participant_list(self):
        from requests.task_participant_request import TaskParticipantRequest
        return self.select_task_participant_list_with(TaskParticipantRequest())

    def select_task_participant_list_with(self, child_request):
        self.query.relation_query("task_participant_list", child_request.query)
        return self
    def select_deleted_task_viewer_list(self):
        from requests.deleted_task_viewer_request import DeletedTaskViewerRequest
        return self.select_deleted_task_viewer_list_with(DeletedTaskViewerRequest())

    def select_deleted_task_viewer_list_with(self, child_request):
        self.query.relation_query("deleted_task_viewer_list", child_request.query)
        return self
    def select_task_blueprint_list(self):
        from requests.task_blueprint_request import TaskBlueprintRequest
        return self.select_task_blueprint_list_with(TaskBlueprintRequest())

    def select_task_blueprint_list_with(self, child_request):
        self.query.relation_query("task_blueprint_list", child_request.query)
        return self
    def select_blueprint_choice_list(self):
        from requests.blueprint_choice_request import BlueprintChoiceRequest
        return self.select_blueprint_choice_list_with(BlueprintChoiceRequest())

    def select_blueprint_choice_list_with(self, child_request):
        self.query.relation_query("blueprint_choice_list", child_request.query)
        return self
    def select_blueprint_subtask_list(self):
        from requests.blueprint_subtask_request import BlueprintSubtaskRequest
        return self.select_blueprint_subtask_list_with(BlueprintSubtaskRequest())

    def select_blueprint_subtask_list_with(self, child_request):
        self.query.relation_query("blueprint_subtask_list", child_request.query)
        return self
    def select_inbox_notice_list(self):
        from requests.inbox_notice_request import InboxNoticeRequest
        return self.select_inbox_notice_list_with(InboxNoticeRequest())

    def select_inbox_notice_list_with(self, child_request):
        self.query.relation_query("inbox_notice_list", child_request.query)
        return self
    def have_work_accounts(self):
        from requests.work_account_request import WorkAccountRequest
        return self.with_work_account_list_matching(WorkAccountRequest())

    def have_no_work_accounts(self):
        from requests.work_account_request import WorkAccountRequest
        return self.without_work_account_list_matching(WorkAccountRequest())

    def with_work_account_list_matching(self, child_request):
        child_request.query.projection = ["work_space"]
        self.query.and_filter(in_subquery(column("id"), "WorkAccount", child_request.query))
        return self

    def without_work_account_list_matching(self, child_request):
        child_request.query.projection = ["work_space"]
        self.query.and_filter(not_in_subquery(column("id"), "WorkAccount", child_request.query))
        return self
    def have_work_projects(self):
        from requests.work_project_request import WorkProjectRequest
        return self.with_work_project_list_matching(WorkProjectRequest())

    def have_no_work_projects(self):
        from requests.work_project_request import WorkProjectRequest
        return self.without_work_project_list_matching(WorkProjectRequest())

    def with_work_project_list_matching(self, child_request):
        child_request.query.projection = ["work_space"]
        self.query.and_filter(in_subquery(column("id"), "WorkProject", child_request.query))
        return self

    def without_work_project_list_matching(self, child_request):
        child_request.query.projection = ["work_space"]
        self.query.and_filter(not_in_subquery(column("id"), "WorkProject", child_request.query))
        return self
    def have_project_memberships(self):
        from requests.project_membership_request import ProjectMembershipRequest
        return self.with_project_membership_list_matching(ProjectMembershipRequest())

    def have_no_project_memberships(self):
        from requests.project_membership_request import ProjectMembershipRequest
        return self.without_project_membership_list_matching(ProjectMembershipRequest())

    def with_project_membership_list_matching(self, child_request):
        child_request.query.projection = ["work_space"]
        self.query.and_filter(in_subquery(column("id"), "ProjectMembership", child_request.query))
        return self

    def without_project_membership_list_matching(self, child_request):
        child_request.query.projection = ["work_space"]
        self.query.and_filter(not_in_subquery(column("id"), "ProjectMembership", child_request.query))
        return self
    def have_project_sections(self):
        from requests.project_section_request import ProjectSectionRequest
        return self.with_project_section_list_matching(ProjectSectionRequest())

    def have_no_project_sections(self):
        from requests.project_section_request import ProjectSectionRequest
        return self.without_project_section_list_matching(ProjectSectionRequest())

    def with_project_section_list_matching(self, child_request):
        child_request.query.projection = ["work_space"]
        self.query.and_filter(in_subquery(column("id"), "ProjectSection", child_request.query))
        return self

    def without_project_section_list_matching(self, child_request):
        child_request.query.projection = ["work_space"]
        self.query.and_filter(not_in_subquery(column("id"), "ProjectSection", child_request.query))
        return self
    def have_work_tasks(self):
        from requests.work_task_request import WorkTaskRequest
        return self.with_work_task_list_matching(WorkTaskRequest())

    def have_no_work_tasks(self):
        from requests.work_task_request import WorkTaskRequest
        return self.without_work_task_list_matching(WorkTaskRequest())

    def with_work_task_list_matching(self, child_request):
        child_request.query.projection = ["work_space"]
        self.query.and_filter(in_subquery(column("id"), "WorkTask", child_request.query))
        return self

    def without_work_task_list_matching(self, child_request):
        child_request.query.projection = ["work_space"]
        self.query.and_filter(not_in_subquery(column("id"), "WorkTask", child_request.query))
        return self
    def have_project_fields(self):
        from requests.project_field_request import ProjectFieldRequest
        return self.with_project_field_list_matching(ProjectFieldRequest())

    def have_no_project_fields(self):
        from requests.project_field_request import ProjectFieldRequest
        return self.without_project_field_list_matching(ProjectFieldRequest())

    def with_project_field_list_matching(self, child_request):
        child_request.query.projection = ["work_space"]
        self.query.and_filter(in_subquery(column("id"), "ProjectField", child_request.query))
        return self

    def without_project_field_list_matching(self, child_request):
        child_request.query.projection = ["work_space"]
        self.query.and_filter(not_in_subquery(column("id"), "ProjectField", child_request.query))
        return self
    def have_field_options(self):
        from requests.field_option_request import FieldOptionRequest
        return self.with_field_option_list_matching(FieldOptionRequest())

    def have_no_field_options(self):
        from requests.field_option_request import FieldOptionRequest
        return self.without_field_option_list_matching(FieldOptionRequest())

    def with_field_option_list_matching(self, child_request):
        child_request.query.projection = ["work_space"]
        self.query.and_filter(in_subquery(column("id"), "FieldOption", child_request.query))
        return self

    def without_field_option_list_matching(self, child_request):
        child_request.query.projection = ["work_space"]
        self.query.and_filter(not_in_subquery(column("id"), "FieldOption", child_request.query))
        return self
    def have_task_field_choices(self):
        from requests.task_field_choice_request import TaskFieldChoiceRequest
        return self.with_task_field_choice_list_matching(TaskFieldChoiceRequest())

    def have_no_task_field_choices(self):
        from requests.task_field_choice_request import TaskFieldChoiceRequest
        return self.without_task_field_choice_list_matching(TaskFieldChoiceRequest())

    def with_task_field_choice_list_matching(self, child_request):
        child_request.query.projection = ["work_space"]
        self.query.and_filter(in_subquery(column("id"), "TaskFieldChoice", child_request.query))
        return self

    def without_task_field_choice_list_matching(self, child_request):
        child_request.query.projection = ["work_space"]
        self.query.and_filter(not_in_subquery(column("id"), "TaskFieldChoice", child_request.query))
        return self
    def have_work_subtasks(self):
        from requests.work_subtask_request import WorkSubtaskRequest
        return self.with_work_subtask_list_matching(WorkSubtaskRequest())

    def have_no_work_subtasks(self):
        from requests.work_subtask_request import WorkSubtaskRequest
        return self.without_work_subtask_list_matching(WorkSubtaskRequest())

    def with_work_subtask_list_matching(self, child_request):
        child_request.query.projection = ["work_space"]
        self.query.and_filter(in_subquery(column("id"), "WorkSubtask", child_request.query))
        return self

    def without_work_subtask_list_matching(self, child_request):
        child_request.query.projection = ["work_space"]
        self.query.and_filter(not_in_subquery(column("id"), "WorkSubtask", child_request.query))
        return self
    def have_task_comments(self):
        from requests.task_comment_request import TaskCommentRequest
        return self.with_task_comment_list_matching(TaskCommentRequest())

    def have_no_task_comments(self):
        from requests.task_comment_request import TaskCommentRequest
        return self.without_task_comment_list_matching(TaskCommentRequest())

    def with_task_comment_list_matching(self, child_request):
        child_request.query.projection = ["work_space"]
        self.query.and_filter(in_subquery(column("id"), "TaskComment", child_request.query))
        return self

    def without_task_comment_list_matching(self, child_request):
        child_request.query.projection = ["work_space"]
        self.query.and_filter(not_in_subquery(column("id"), "TaskComment", child_request.query))
        return self
    def have_task_dependencies(self):
        from requests.task_dependency_request import TaskDependencyRequest
        return self.with_task_dependency_list_matching(TaskDependencyRequest())

    def have_no_task_dependencies(self):
        from requests.task_dependency_request import TaskDependencyRequest
        return self.without_task_dependency_list_matching(TaskDependencyRequest())

    def with_task_dependency_list_matching(self, child_request):
        child_request.query.projection = ["work_space"]
        self.query.and_filter(in_subquery(column("id"), "TaskDependency", child_request.query))
        return self

    def without_task_dependency_list_matching(self, child_request):
        child_request.query.projection = ["work_space"]
        self.query.and_filter(not_in_subquery(column("id"), "TaskDependency", child_request.query))
        return self
    def have_task_placements(self):
        from requests.task_placement_request import TaskPlacementRequest
        return self.with_task_placement_list_matching(TaskPlacementRequest())

    def have_no_task_placements(self):
        from requests.task_placement_request import TaskPlacementRequest
        return self.without_task_placement_list_matching(TaskPlacementRequest())

    def with_task_placement_list_matching(self, child_request):
        child_request.query.projection = ["work_space"]
        self.query.and_filter(in_subquery(column("id"), "TaskPlacement", child_request.query))
        return self

    def without_task_placement_list_matching(self, child_request):
        child_request.query.projection = ["work_space"]
        self.query.and_filter(not_in_subquery(column("id"), "TaskPlacement", child_request.query))
        return self
    def have_recurrence_links(self):
        from requests.recurrence_link_request import RecurrenceLinkRequest
        return self.with_recurrence_link_list_matching(RecurrenceLinkRequest())

    def have_no_recurrence_links(self):
        from requests.recurrence_link_request import RecurrenceLinkRequest
        return self.without_recurrence_link_list_matching(RecurrenceLinkRequest())

    def with_recurrence_link_list_matching(self, child_request):
        child_request.query.projection = ["work_space"]
        self.query.and_filter(in_subquery(column("id"), "RecurrenceLink", child_request.query))
        return self

    def without_recurrence_link_list_matching(self, child_request):
        child_request.query.projection = ["work_space"]
        self.query.and_filter(not_in_subquery(column("id"), "RecurrenceLink", child_request.query))
        return self
    def have_task_events(self):
        from requests.task_event_request import TaskEventRequest
        return self.with_task_event_list_matching(TaskEventRequest())

    def have_no_task_events(self):
        from requests.task_event_request import TaskEventRequest
        return self.without_task_event_list_matching(TaskEventRequest())

    def with_task_event_list_matching(self, child_request):
        child_request.query.projection = ["work_space"]
        self.query.and_filter(in_subquery(column("id"), "TaskEvent", child_request.query))
        return self

    def without_task_event_list_matching(self, child_request):
        child_request.query.projection = ["work_space"]
        self.query.and_filter(not_in_subquery(column("id"), "TaskEvent", child_request.query))
        return self
    def have_task_participants(self):
        from requests.task_participant_request import TaskParticipantRequest
        return self.with_task_participant_list_matching(TaskParticipantRequest())

    def have_no_task_participants(self):
        from requests.task_participant_request import TaskParticipantRequest
        return self.without_task_participant_list_matching(TaskParticipantRequest())

    def with_task_participant_list_matching(self, child_request):
        child_request.query.projection = ["work_space"]
        self.query.and_filter(in_subquery(column("id"), "TaskParticipant", child_request.query))
        return self

    def without_task_participant_list_matching(self, child_request):
        child_request.query.projection = ["work_space"]
        self.query.and_filter(not_in_subquery(column("id"), "TaskParticipant", child_request.query))
        return self
    def have_deleted_task_viewers(self):
        from requests.deleted_task_viewer_request import DeletedTaskViewerRequest
        return self.with_deleted_task_viewer_list_matching(DeletedTaskViewerRequest())

    def have_no_deleted_task_viewers(self):
        from requests.deleted_task_viewer_request import DeletedTaskViewerRequest
        return self.without_deleted_task_viewer_list_matching(DeletedTaskViewerRequest())

    def with_deleted_task_viewer_list_matching(self, child_request):
        child_request.query.projection = ["work_space"]
        self.query.and_filter(in_subquery(column("id"), "DeletedTaskViewer", child_request.query))
        return self

    def without_deleted_task_viewer_list_matching(self, child_request):
        child_request.query.projection = ["work_space"]
        self.query.and_filter(not_in_subquery(column("id"), "DeletedTaskViewer", child_request.query))
        return self
    def have_task_blueprints(self):
        from requests.task_blueprint_request import TaskBlueprintRequest
        return self.with_task_blueprint_list_matching(TaskBlueprintRequest())

    def have_no_task_blueprints(self):
        from requests.task_blueprint_request import TaskBlueprintRequest
        return self.without_task_blueprint_list_matching(TaskBlueprintRequest())

    def with_task_blueprint_list_matching(self, child_request):
        child_request.query.projection = ["work_space"]
        self.query.and_filter(in_subquery(column("id"), "TaskBlueprint", child_request.query))
        return self

    def without_task_blueprint_list_matching(self, child_request):
        child_request.query.projection = ["work_space"]
        self.query.and_filter(not_in_subquery(column("id"), "TaskBlueprint", child_request.query))
        return self
    def have_blueprint_choices(self):
        from requests.blueprint_choice_request import BlueprintChoiceRequest
        return self.with_blueprint_choice_list_matching(BlueprintChoiceRequest())

    def have_no_blueprint_choices(self):
        from requests.blueprint_choice_request import BlueprintChoiceRequest
        return self.without_blueprint_choice_list_matching(BlueprintChoiceRequest())

    def with_blueprint_choice_list_matching(self, child_request):
        child_request.query.projection = ["work_space"]
        self.query.and_filter(in_subquery(column("id"), "BlueprintChoice", child_request.query))
        return self

    def without_blueprint_choice_list_matching(self, child_request):
        child_request.query.projection = ["work_space"]
        self.query.and_filter(not_in_subquery(column("id"), "BlueprintChoice", child_request.query))
        return self
    def have_blueprint_subtasks(self):
        from requests.blueprint_subtask_request import BlueprintSubtaskRequest
        return self.with_blueprint_subtask_list_matching(BlueprintSubtaskRequest())

    def have_no_blueprint_subtasks(self):
        from requests.blueprint_subtask_request import BlueprintSubtaskRequest
        return self.without_blueprint_subtask_list_matching(BlueprintSubtaskRequest())

    def with_blueprint_subtask_list_matching(self, child_request):
        child_request.query.projection = ["work_space"]
        self.query.and_filter(in_subquery(column("id"), "BlueprintSubtask", child_request.query))
        return self

    def without_blueprint_subtask_list_matching(self, child_request):
        child_request.query.projection = ["work_space"]
        self.query.and_filter(not_in_subquery(column("id"), "BlueprintSubtask", child_request.query))
        return self
    def have_inbox_notices(self):
        from requests.inbox_notice_request import InboxNoticeRequest
        return self.with_inbox_notice_list_matching(InboxNoticeRequest())

    def have_no_inbox_notices(self):
        from requests.inbox_notice_request import InboxNoticeRequest
        return self.without_inbox_notice_list_matching(InboxNoticeRequest())

    def with_inbox_notice_list_matching(self, child_request):
        child_request.query.projection = ["work_space"]
        self.query.and_filter(in_subquery(column("id"), "InboxNotice", child_request.query))
        return self

    def without_inbox_notice_list_matching(self, child_request):
        child_request.query.projection = ["work_space"]
        self.query.and_filter(not_in_subquery(column("id"), "InboxNotice", child_request.query))
        return self
    def count_work_accounts(self):
        return self.count_work_accounts_as("count_work_accounts")

    def count_work_accounts_as(self, alias: str):
        from requests.work_account_request import WorkAccountRequest
        return self.count_work_accounts_with(alias, WorkAccountRequest())

    def count_work_accounts_with(self, alias: str, child_request):
        child_request.query.count_field("id", alias)
        self.query.relation_aggregates.append(
            RelationAggregate("work_account_list", alias, child_request.query, True)
        )
        return self


    def count_work_projects(self):
        return self.count_work_projects_as("count_work_projects")

    def count_work_projects_as(self, alias: str):
        from requests.work_project_request import WorkProjectRequest
        return self.count_work_projects_with(alias, WorkProjectRequest())

    def count_work_projects_with(self, alias: str, child_request):
        child_request.query.count_field("id", alias)
        self.query.relation_aggregates.append(
            RelationAggregate("work_project_list", alias, child_request.query, True)
        )
        return self


    def count_project_memberships(self):
        return self.count_project_memberships_as("count_project_memberships")

    def count_project_memberships_as(self, alias: str):
        from requests.project_membership_request import ProjectMembershipRequest
        return self.count_project_memberships_with(alias, ProjectMembershipRequest())

    def count_project_memberships_with(self, alias: str, child_request):
        child_request.query.count_field("id", alias)
        self.query.relation_aggregates.append(
            RelationAggregate("project_membership_list", alias, child_request.query, True)
        )
        return self


    def count_project_sections(self):
        return self.count_project_sections_as("count_project_sections")

    def count_project_sections_as(self, alias: str):
        from requests.project_section_request import ProjectSectionRequest
        return self.count_project_sections_with(alias, ProjectSectionRequest())

    def count_project_sections_with(self, alias: str, child_request):
        child_request.query.count_field("id", alias)
        self.query.relation_aggregates.append(
            RelationAggregate("project_section_list", alias, child_request.query, True)
        )
        return self

    def min_section_order_of_project_sections(self):
        from requests.project_section_request import ProjectSectionRequest
        return self.min_section_order_of_project_sections_as(
            "min_section_order_of_project_sections", ProjectSectionRequest())

    def min_section_order_of_project_sections_as(self, alias: str, child_request):
        child_request.query.min("section_order", "min_section_order")
        self.query.relation_aggregates.append(
            RelationAggregate("project_section_list", alias, child_request.query, True)
        )
        return self
    def max_section_order_of_project_sections(self):
        from requests.project_section_request import ProjectSectionRequest
        return self.max_section_order_of_project_sections_as(
            "max_section_order_of_project_sections", ProjectSectionRequest())

    def max_section_order_of_project_sections_as(self, alias: str, child_request):
        child_request.query.max("section_order", "max_section_order")
        self.query.relation_aggregates.append(
            RelationAggregate("project_section_list", alias, child_request.query, True)
        )
        return self
    def sum_section_order_of_project_sections(self):
        from requests.project_section_request import ProjectSectionRequest
        return self.sum_section_order_of_project_sections_as(
            "sum_section_order_of_project_sections", ProjectSectionRequest())

    def sum_section_order_of_project_sections_as(self, alias: str, child_request):
        child_request.query.sum("section_order", "sum_section_order")
        self.query.relation_aggregates.append(
            RelationAggregate("project_section_list", alias, child_request.query, True)
        )
        return self
    def avg_section_order_of_project_sections(self):
        from requests.project_section_request import ProjectSectionRequest
        return self.avg_section_order_of_project_sections_as(
            "avg_section_order_of_project_sections", ProjectSectionRequest())

    def avg_section_order_of_project_sections_as(self, alias: str, child_request):
        child_request.query.avg("section_order", "avg_section_order")
        self.query.relation_aggregates.append(
            RelationAggregate("project_section_list", alias, child_request.query, True)
        )
        return self
    def standardDeviation_section_order_of_project_sections(self):
        from requests.project_section_request import ProjectSectionRequest
        return self.standardDeviation_section_order_of_project_sections_as(
            "standardDeviation_section_order_of_project_sections", ProjectSectionRequest())

    def standardDeviation_section_order_of_project_sections_as(self, alias: str, child_request):
        child_request.query.standardDeviation("section_order", "standardDeviation_section_order")
        self.query.relation_aggregates.append(
            RelationAggregate("project_section_list", alias, child_request.query, True)
        )
        return self
    def squareRootOfPopulationStandardDeviation_section_order_of_project_sections(self):
        from requests.project_section_request import ProjectSectionRequest
        return self.squareRootOfPopulationStandardDeviation_section_order_of_project_sections_as(
            "squareRootOfPopulationStandardDeviation_section_order_of_project_sections", ProjectSectionRequest())

    def squareRootOfPopulationStandardDeviation_section_order_of_project_sections_as(self, alias: str, child_request):
        child_request.query.squareRootOfPopulationStandardDeviation("section_order", "squareRootOfPopulationStandardDeviation_section_order")
        self.query.relation_aggregates.append(
            RelationAggregate("project_section_list", alias, child_request.query, True)
        )
        return self
    def sampleVariance_section_order_of_project_sections(self):
        from requests.project_section_request import ProjectSectionRequest
        return self.sampleVariance_section_order_of_project_sections_as(
            "sampleVariance_section_order_of_project_sections", ProjectSectionRequest())

    def sampleVariance_section_order_of_project_sections_as(self, alias: str, child_request):
        child_request.query.sampleVariance("section_order", "sampleVariance_section_order")
        self.query.relation_aggregates.append(
            RelationAggregate("project_section_list", alias, child_request.query, True)
        )
        return self
    def samplePopulationVariance_section_order_of_project_sections(self):
        from requests.project_section_request import ProjectSectionRequest
        return self.samplePopulationVariance_section_order_of_project_sections_as(
            "samplePopulationVariance_section_order_of_project_sections", ProjectSectionRequest())

    def samplePopulationVariance_section_order_of_project_sections_as(self, alias: str, child_request):
        child_request.query.samplePopulationVariance("section_order", "samplePopulationVariance_section_order")
        self.query.relation_aggregates.append(
            RelationAggregate("project_section_list", alias, child_request.query, True)
        )
        return self
    def count_work_tasks(self):
        return self.count_work_tasks_as("count_work_tasks")

    def count_work_tasks_as(self, alias: str):
        from requests.work_task_request import WorkTaskRequest
        return self.count_work_tasks_with(alias, WorkTaskRequest())

    def count_work_tasks_with(self, alias: str, child_request):
        child_request.query.count_field("id", alias)
        self.query.relation_aggregates.append(
            RelationAggregate("work_task_list", alias, child_request.query, True)
        )
        return self

    def min_deleted_epoch_of_work_tasks(self):
        from requests.work_task_request import WorkTaskRequest
        return self.min_deleted_epoch_of_work_tasks_as(
            "min_deleted_epoch_of_work_tasks", WorkTaskRequest())

    def min_deleted_epoch_of_work_tasks_as(self, alias: str, child_request):
        child_request.query.min("deleted_epoch", "min_deleted_epoch")
        self.query.relation_aggregates.append(
            RelationAggregate("work_task_list", alias, child_request.query, True)
        )
        return self
    def max_deleted_epoch_of_work_tasks(self):
        from requests.work_task_request import WorkTaskRequest
        return self.max_deleted_epoch_of_work_tasks_as(
            "max_deleted_epoch_of_work_tasks", WorkTaskRequest())

    def max_deleted_epoch_of_work_tasks_as(self, alias: str, child_request):
        child_request.query.max("deleted_epoch", "max_deleted_epoch")
        self.query.relation_aggregates.append(
            RelationAggregate("work_task_list", alias, child_request.query, True)
        )
        return self
    def sum_deleted_epoch_of_work_tasks(self):
        from requests.work_task_request import WorkTaskRequest
        return self.sum_deleted_epoch_of_work_tasks_as(
            "sum_deleted_epoch_of_work_tasks", WorkTaskRequest())

    def sum_deleted_epoch_of_work_tasks_as(self, alias: str, child_request):
        child_request.query.sum("deleted_epoch", "sum_deleted_epoch")
        self.query.relation_aggregates.append(
            RelationAggregate("work_task_list", alias, child_request.query, True)
        )
        return self
    def avg_deleted_epoch_of_work_tasks(self):
        from requests.work_task_request import WorkTaskRequest
        return self.avg_deleted_epoch_of_work_tasks_as(
            "avg_deleted_epoch_of_work_tasks", WorkTaskRequest())

    def avg_deleted_epoch_of_work_tasks_as(self, alias: str, child_request):
        child_request.query.avg("deleted_epoch", "avg_deleted_epoch")
        self.query.relation_aggregates.append(
            RelationAggregate("work_task_list", alias, child_request.query, True)
        )
        return self
    def standardDeviation_deleted_epoch_of_work_tasks(self):
        from requests.work_task_request import WorkTaskRequest
        return self.standardDeviation_deleted_epoch_of_work_tasks_as(
            "standardDeviation_deleted_epoch_of_work_tasks", WorkTaskRequest())

    def standardDeviation_deleted_epoch_of_work_tasks_as(self, alias: str, child_request):
        child_request.query.standardDeviation("deleted_epoch", "standardDeviation_deleted_epoch")
        self.query.relation_aggregates.append(
            RelationAggregate("work_task_list", alias, child_request.query, True)
        )
        return self
    def squareRootOfPopulationStandardDeviation_deleted_epoch_of_work_tasks(self):
        from requests.work_task_request import WorkTaskRequest
        return self.squareRootOfPopulationStandardDeviation_deleted_epoch_of_work_tasks_as(
            "squareRootOfPopulationStandardDeviation_deleted_epoch_of_work_tasks", WorkTaskRequest())

    def squareRootOfPopulationStandardDeviation_deleted_epoch_of_work_tasks_as(self, alias: str, child_request):
        child_request.query.squareRootOfPopulationStandardDeviation("deleted_epoch", "squareRootOfPopulationStandardDeviation_deleted_epoch")
        self.query.relation_aggregates.append(
            RelationAggregate("work_task_list", alias, child_request.query, True)
        )
        return self
    def sampleVariance_deleted_epoch_of_work_tasks(self):
        from requests.work_task_request import WorkTaskRequest
        return self.sampleVariance_deleted_epoch_of_work_tasks_as(
            "sampleVariance_deleted_epoch_of_work_tasks", WorkTaskRequest())

    def sampleVariance_deleted_epoch_of_work_tasks_as(self, alias: str, child_request):
        child_request.query.sampleVariance("deleted_epoch", "sampleVariance_deleted_epoch")
        self.query.relation_aggregates.append(
            RelationAggregate("work_task_list", alias, child_request.query, True)
        )
        return self
    def samplePopulationVariance_deleted_epoch_of_work_tasks(self):
        from requests.work_task_request import WorkTaskRequest
        return self.samplePopulationVariance_deleted_epoch_of_work_tasks_as(
            "samplePopulationVariance_deleted_epoch_of_work_tasks", WorkTaskRequest())

    def samplePopulationVariance_deleted_epoch_of_work_tasks_as(self, alias: str, child_request):
        child_request.query.samplePopulationVariance("deleted_epoch", "samplePopulationVariance_deleted_epoch")
        self.query.relation_aggregates.append(
            RelationAggregate("work_task_list", alias, child_request.query, True)
        )
        return self
    def min_task_order_of_work_tasks(self):
        from requests.work_task_request import WorkTaskRequest
        return self.min_task_order_of_work_tasks_as(
            "min_task_order_of_work_tasks", WorkTaskRequest())

    def min_task_order_of_work_tasks_as(self, alias: str, child_request):
        child_request.query.min("task_order", "min_task_order")
        self.query.relation_aggregates.append(
            RelationAggregate("work_task_list", alias, child_request.query, True)
        )
        return self
    def max_task_order_of_work_tasks(self):
        from requests.work_task_request import WorkTaskRequest
        return self.max_task_order_of_work_tasks_as(
            "max_task_order_of_work_tasks", WorkTaskRequest())

    def max_task_order_of_work_tasks_as(self, alias: str, child_request):
        child_request.query.max("task_order", "max_task_order")
        self.query.relation_aggregates.append(
            RelationAggregate("work_task_list", alias, child_request.query, True)
        )
        return self
    def sum_task_order_of_work_tasks(self):
        from requests.work_task_request import WorkTaskRequest
        return self.sum_task_order_of_work_tasks_as(
            "sum_task_order_of_work_tasks", WorkTaskRequest())

    def sum_task_order_of_work_tasks_as(self, alias: str, child_request):
        child_request.query.sum("task_order", "sum_task_order")
        self.query.relation_aggregates.append(
            RelationAggregate("work_task_list", alias, child_request.query, True)
        )
        return self
    def avg_task_order_of_work_tasks(self):
        from requests.work_task_request import WorkTaskRequest
        return self.avg_task_order_of_work_tasks_as(
            "avg_task_order_of_work_tasks", WorkTaskRequest())

    def avg_task_order_of_work_tasks_as(self, alias: str, child_request):
        child_request.query.avg("task_order", "avg_task_order")
        self.query.relation_aggregates.append(
            RelationAggregate("work_task_list", alias, child_request.query, True)
        )
        return self
    def standardDeviation_task_order_of_work_tasks(self):
        from requests.work_task_request import WorkTaskRequest
        return self.standardDeviation_task_order_of_work_tasks_as(
            "standardDeviation_task_order_of_work_tasks", WorkTaskRequest())

    def standardDeviation_task_order_of_work_tasks_as(self, alias: str, child_request):
        child_request.query.standardDeviation("task_order", "standardDeviation_task_order")
        self.query.relation_aggregates.append(
            RelationAggregate("work_task_list", alias, child_request.query, True)
        )
        return self
    def squareRootOfPopulationStandardDeviation_task_order_of_work_tasks(self):
        from requests.work_task_request import WorkTaskRequest
        return self.squareRootOfPopulationStandardDeviation_task_order_of_work_tasks_as(
            "squareRootOfPopulationStandardDeviation_task_order_of_work_tasks", WorkTaskRequest())

    def squareRootOfPopulationStandardDeviation_task_order_of_work_tasks_as(self, alias: str, child_request):
        child_request.query.squareRootOfPopulationStandardDeviation("task_order", "squareRootOfPopulationStandardDeviation_task_order")
        self.query.relation_aggregates.append(
            RelationAggregate("work_task_list", alias, child_request.query, True)
        )
        return self
    def sampleVariance_task_order_of_work_tasks(self):
        from requests.work_task_request import WorkTaskRequest
        return self.sampleVariance_task_order_of_work_tasks_as(
            "sampleVariance_task_order_of_work_tasks", WorkTaskRequest())

    def sampleVariance_task_order_of_work_tasks_as(self, alias: str, child_request):
        child_request.query.sampleVariance("task_order", "sampleVariance_task_order")
        self.query.relation_aggregates.append(
            RelationAggregate("work_task_list", alias, child_request.query, True)
        )
        return self
    def samplePopulationVariance_task_order_of_work_tasks(self):
        from requests.work_task_request import WorkTaskRequest
        return self.samplePopulationVariance_task_order_of_work_tasks_as(
            "samplePopulationVariance_task_order_of_work_tasks", WorkTaskRequest())

    def samplePopulationVariance_task_order_of_work_tasks_as(self, alias: str, child_request):
        child_request.query.samplePopulationVariance("task_order", "samplePopulationVariance_task_order")
        self.query.relation_aggregates.append(
            RelationAggregate("work_task_list", alias, child_request.query, True)
        )
        return self
    def count_project_fields(self):
        return self.count_project_fields_as("count_project_fields")

    def count_project_fields_as(self, alias: str):
        from requests.project_field_request import ProjectFieldRequest
        return self.count_project_fields_with(alias, ProjectFieldRequest())

    def count_project_fields_with(self, alias: str, child_request):
        child_request.query.count_field("id", alias)
        self.query.relation_aggregates.append(
            RelationAggregate("project_field_list", alias, child_request.query, True)
        )
        return self


    def count_field_options(self):
        return self.count_field_options_as("count_field_options")

    def count_field_options_as(self, alias: str):
        from requests.field_option_request import FieldOptionRequest
        return self.count_field_options_with(alias, FieldOptionRequest())

    def count_field_options_with(self, alias: str, child_request):
        child_request.query.count_field("id", alias)
        self.query.relation_aggregates.append(
            RelationAggregate("field_option_list", alias, child_request.query, True)
        )
        return self

    def min_option_order_of_field_options(self):
        from requests.field_option_request import FieldOptionRequest
        return self.min_option_order_of_field_options_as(
            "min_option_order_of_field_options", FieldOptionRequest())

    def min_option_order_of_field_options_as(self, alias: str, child_request):
        child_request.query.min("option_order", "min_option_order")
        self.query.relation_aggregates.append(
            RelationAggregate("field_option_list", alias, child_request.query, True)
        )
        return self
    def max_option_order_of_field_options(self):
        from requests.field_option_request import FieldOptionRequest
        return self.max_option_order_of_field_options_as(
            "max_option_order_of_field_options", FieldOptionRequest())

    def max_option_order_of_field_options_as(self, alias: str, child_request):
        child_request.query.max("option_order", "max_option_order")
        self.query.relation_aggregates.append(
            RelationAggregate("field_option_list", alias, child_request.query, True)
        )
        return self
    def sum_option_order_of_field_options(self):
        from requests.field_option_request import FieldOptionRequest
        return self.sum_option_order_of_field_options_as(
            "sum_option_order_of_field_options", FieldOptionRequest())

    def sum_option_order_of_field_options_as(self, alias: str, child_request):
        child_request.query.sum("option_order", "sum_option_order")
        self.query.relation_aggregates.append(
            RelationAggregate("field_option_list", alias, child_request.query, True)
        )
        return self
    def avg_option_order_of_field_options(self):
        from requests.field_option_request import FieldOptionRequest
        return self.avg_option_order_of_field_options_as(
            "avg_option_order_of_field_options", FieldOptionRequest())

    def avg_option_order_of_field_options_as(self, alias: str, child_request):
        child_request.query.avg("option_order", "avg_option_order")
        self.query.relation_aggregates.append(
            RelationAggregate("field_option_list", alias, child_request.query, True)
        )
        return self
    def standardDeviation_option_order_of_field_options(self):
        from requests.field_option_request import FieldOptionRequest
        return self.standardDeviation_option_order_of_field_options_as(
            "standardDeviation_option_order_of_field_options", FieldOptionRequest())

    def standardDeviation_option_order_of_field_options_as(self, alias: str, child_request):
        child_request.query.standardDeviation("option_order", "standardDeviation_option_order")
        self.query.relation_aggregates.append(
            RelationAggregate("field_option_list", alias, child_request.query, True)
        )
        return self
    def squareRootOfPopulationStandardDeviation_option_order_of_field_options(self):
        from requests.field_option_request import FieldOptionRequest
        return self.squareRootOfPopulationStandardDeviation_option_order_of_field_options_as(
            "squareRootOfPopulationStandardDeviation_option_order_of_field_options", FieldOptionRequest())

    def squareRootOfPopulationStandardDeviation_option_order_of_field_options_as(self, alias: str, child_request):
        child_request.query.squareRootOfPopulationStandardDeviation("option_order", "squareRootOfPopulationStandardDeviation_option_order")
        self.query.relation_aggregates.append(
            RelationAggregate("field_option_list", alias, child_request.query, True)
        )
        return self
    def sampleVariance_option_order_of_field_options(self):
        from requests.field_option_request import FieldOptionRequest
        return self.sampleVariance_option_order_of_field_options_as(
            "sampleVariance_option_order_of_field_options", FieldOptionRequest())

    def sampleVariance_option_order_of_field_options_as(self, alias: str, child_request):
        child_request.query.sampleVariance("option_order", "sampleVariance_option_order")
        self.query.relation_aggregates.append(
            RelationAggregate("field_option_list", alias, child_request.query, True)
        )
        return self
    def samplePopulationVariance_option_order_of_field_options(self):
        from requests.field_option_request import FieldOptionRequest
        return self.samplePopulationVariance_option_order_of_field_options_as(
            "samplePopulationVariance_option_order_of_field_options", FieldOptionRequest())

    def samplePopulationVariance_option_order_of_field_options_as(self, alias: str, child_request):
        child_request.query.samplePopulationVariance("option_order", "samplePopulationVariance_option_order")
        self.query.relation_aggregates.append(
            RelationAggregate("field_option_list", alias, child_request.query, True)
        )
        return self
    def count_task_field_choices(self):
        return self.count_task_field_choices_as("count_task_field_choices")

    def count_task_field_choices_as(self, alias: str):
        from requests.task_field_choice_request import TaskFieldChoiceRequest
        return self.count_task_field_choices_with(alias, TaskFieldChoiceRequest())

    def count_task_field_choices_with(self, alias: str, child_request):
        child_request.query.count_field("id", alias)
        self.query.relation_aggregates.append(
            RelationAggregate("task_field_choice_list", alias, child_request.query, True)
        )
        return self


    def count_work_subtasks(self):
        return self.count_work_subtasks_as("count_work_subtasks")

    def count_work_subtasks_as(self, alias: str):
        from requests.work_subtask_request import WorkSubtaskRequest
        return self.count_work_subtasks_with(alias, WorkSubtaskRequest())

    def count_work_subtasks_with(self, alias: str, child_request):
        child_request.query.count_field("id", alias)
        self.query.relation_aggregates.append(
            RelationAggregate("work_subtask_list", alias, child_request.query, True)
        )
        return self


    def count_task_comments(self):
        return self.count_task_comments_as("count_task_comments")

    def count_task_comments_as(self, alias: str):
        from requests.task_comment_request import TaskCommentRequest
        return self.count_task_comments_with(alias, TaskCommentRequest())

    def count_task_comments_with(self, alias: str, child_request):
        child_request.query.count_field("id", alias)
        self.query.relation_aggregates.append(
            RelationAggregate("task_comment_list", alias, child_request.query, True)
        )
        return self


    def count_task_dependencies(self):
        return self.count_task_dependencies_as("count_task_dependencies")

    def count_task_dependencies_as(self, alias: str):
        from requests.task_dependency_request import TaskDependencyRequest
        return self.count_task_dependencies_with(alias, TaskDependencyRequest())

    def count_task_dependencies_with(self, alias: str, child_request):
        child_request.query.count_field("id", alias)
        self.query.relation_aggregates.append(
            RelationAggregate("task_dependency_list", alias, child_request.query, True)
        )
        return self


    def count_task_placements(self):
        return self.count_task_placements_as("count_task_placements")

    def count_task_placements_as(self, alias: str):
        from requests.task_placement_request import TaskPlacementRequest
        return self.count_task_placements_with(alias, TaskPlacementRequest())

    def count_task_placements_with(self, alias: str, child_request):
        child_request.query.count_field("id", alias)
        self.query.relation_aggregates.append(
            RelationAggregate("task_placement_list", alias, child_request.query, True)
        )
        return self

    def min_placement_order_of_task_placements(self):
        from requests.task_placement_request import TaskPlacementRequest
        return self.min_placement_order_of_task_placements_as(
            "min_placement_order_of_task_placements", TaskPlacementRequest())

    def min_placement_order_of_task_placements_as(self, alias: str, child_request):
        child_request.query.min("placement_order", "min_placement_order")
        self.query.relation_aggregates.append(
            RelationAggregate("task_placement_list", alias, child_request.query, True)
        )
        return self
    def max_placement_order_of_task_placements(self):
        from requests.task_placement_request import TaskPlacementRequest
        return self.max_placement_order_of_task_placements_as(
            "max_placement_order_of_task_placements", TaskPlacementRequest())

    def max_placement_order_of_task_placements_as(self, alias: str, child_request):
        child_request.query.max("placement_order", "max_placement_order")
        self.query.relation_aggregates.append(
            RelationAggregate("task_placement_list", alias, child_request.query, True)
        )
        return self
    def sum_placement_order_of_task_placements(self):
        from requests.task_placement_request import TaskPlacementRequest
        return self.sum_placement_order_of_task_placements_as(
            "sum_placement_order_of_task_placements", TaskPlacementRequest())

    def sum_placement_order_of_task_placements_as(self, alias: str, child_request):
        child_request.query.sum("placement_order", "sum_placement_order")
        self.query.relation_aggregates.append(
            RelationAggregate("task_placement_list", alias, child_request.query, True)
        )
        return self
    def avg_placement_order_of_task_placements(self):
        from requests.task_placement_request import TaskPlacementRequest
        return self.avg_placement_order_of_task_placements_as(
            "avg_placement_order_of_task_placements", TaskPlacementRequest())

    def avg_placement_order_of_task_placements_as(self, alias: str, child_request):
        child_request.query.avg("placement_order", "avg_placement_order")
        self.query.relation_aggregates.append(
            RelationAggregate("task_placement_list", alias, child_request.query, True)
        )
        return self
    def standardDeviation_placement_order_of_task_placements(self):
        from requests.task_placement_request import TaskPlacementRequest
        return self.standardDeviation_placement_order_of_task_placements_as(
            "standardDeviation_placement_order_of_task_placements", TaskPlacementRequest())

    def standardDeviation_placement_order_of_task_placements_as(self, alias: str, child_request):
        child_request.query.standardDeviation("placement_order", "standardDeviation_placement_order")
        self.query.relation_aggregates.append(
            RelationAggregate("task_placement_list", alias, child_request.query, True)
        )
        return self
    def squareRootOfPopulationStandardDeviation_placement_order_of_task_placements(self):
        from requests.task_placement_request import TaskPlacementRequest
        return self.squareRootOfPopulationStandardDeviation_placement_order_of_task_placements_as(
            "squareRootOfPopulationStandardDeviation_placement_order_of_task_placements", TaskPlacementRequest())

    def squareRootOfPopulationStandardDeviation_placement_order_of_task_placements_as(self, alias: str, child_request):
        child_request.query.squareRootOfPopulationStandardDeviation("placement_order", "squareRootOfPopulationStandardDeviation_placement_order")
        self.query.relation_aggregates.append(
            RelationAggregate("task_placement_list", alias, child_request.query, True)
        )
        return self
    def sampleVariance_placement_order_of_task_placements(self):
        from requests.task_placement_request import TaskPlacementRequest
        return self.sampleVariance_placement_order_of_task_placements_as(
            "sampleVariance_placement_order_of_task_placements", TaskPlacementRequest())

    def sampleVariance_placement_order_of_task_placements_as(self, alias: str, child_request):
        child_request.query.sampleVariance("placement_order", "sampleVariance_placement_order")
        self.query.relation_aggregates.append(
            RelationAggregate("task_placement_list", alias, child_request.query, True)
        )
        return self
    def samplePopulationVariance_placement_order_of_task_placements(self):
        from requests.task_placement_request import TaskPlacementRequest
        return self.samplePopulationVariance_placement_order_of_task_placements_as(
            "samplePopulationVariance_placement_order_of_task_placements", TaskPlacementRequest())

    def samplePopulationVariance_placement_order_of_task_placements_as(self, alias: str, child_request):
        child_request.query.samplePopulationVariance("placement_order", "samplePopulationVariance_placement_order")
        self.query.relation_aggregates.append(
            RelationAggregate("task_placement_list", alias, child_request.query, True)
        )
        return self
    def count_recurrence_links(self):
        return self.count_recurrence_links_as("count_recurrence_links")

    def count_recurrence_links_as(self, alias: str):
        from requests.recurrence_link_request import RecurrenceLinkRequest
        return self.count_recurrence_links_with(alias, RecurrenceLinkRequest())

    def count_recurrence_links_with(self, alias: str, child_request):
        child_request.query.count_field("id", alias)
        self.query.relation_aggregates.append(
            RelationAggregate("recurrence_link_list", alias, child_request.query, True)
        )
        return self


    def count_task_events(self):
        return self.count_task_events_as("count_task_events")

    def count_task_events_as(self, alias: str):
        from requests.task_event_request import TaskEventRequest
        return self.count_task_events_with(alias, TaskEventRequest())

    def count_task_events_with(self, alias: str, child_request):
        child_request.query.count_field("id", alias)
        self.query.relation_aggregates.append(
            RelationAggregate("task_event_list", alias, child_request.query, True)
        )
        return self


    def count_task_participants(self):
        return self.count_task_participants_as("count_task_participants")

    def count_task_participants_as(self, alias: str):
        from requests.task_participant_request import TaskParticipantRequest
        return self.count_task_participants_with(alias, TaskParticipantRequest())

    def count_task_participants_with(self, alias: str, child_request):
        child_request.query.count_field("id", alias)
        self.query.relation_aggregates.append(
            RelationAggregate("task_participant_list", alias, child_request.query, True)
        )
        return self


    def count_deleted_task_viewers(self):
        return self.count_deleted_task_viewers_as("count_deleted_task_viewers")

    def count_deleted_task_viewers_as(self, alias: str):
        from requests.deleted_task_viewer_request import DeletedTaskViewerRequest
        return self.count_deleted_task_viewers_with(alias, DeletedTaskViewerRequest())

    def count_deleted_task_viewers_with(self, alias: str, child_request):
        child_request.query.count_field("id", alias)
        self.query.relation_aggregates.append(
            RelationAggregate("deleted_task_viewer_list", alias, child_request.query, True)
        )
        return self


    def count_task_blueprints(self):
        return self.count_task_blueprints_as("count_task_blueprints")

    def count_task_blueprints_as(self, alias: str):
        from requests.task_blueprint_request import TaskBlueprintRequest
        return self.count_task_blueprints_with(alias, TaskBlueprintRequest())

    def count_task_blueprints_with(self, alias: str, child_request):
        child_request.query.count_field("id", alias)
        self.query.relation_aggregates.append(
            RelationAggregate("task_blueprint_list", alias, child_request.query, True)
        )
        return self

    def min_due_offset_of_task_blueprints(self):
        from requests.task_blueprint_request import TaskBlueprintRequest
        return self.min_due_offset_of_task_blueprints_as(
            "min_due_offset_of_task_blueprints", TaskBlueprintRequest())

    def min_due_offset_of_task_blueprints_as(self, alias: str, child_request):
        child_request.query.min("due_offset", "min_due_offset")
        self.query.relation_aggregates.append(
            RelationAggregate("task_blueprint_list", alias, child_request.query, True)
        )
        return self
    def max_due_offset_of_task_blueprints(self):
        from requests.task_blueprint_request import TaskBlueprintRequest
        return self.max_due_offset_of_task_blueprints_as(
            "max_due_offset_of_task_blueprints", TaskBlueprintRequest())

    def max_due_offset_of_task_blueprints_as(self, alias: str, child_request):
        child_request.query.max("due_offset", "max_due_offset")
        self.query.relation_aggregates.append(
            RelationAggregate("task_blueprint_list", alias, child_request.query, True)
        )
        return self
    def sum_due_offset_of_task_blueprints(self):
        from requests.task_blueprint_request import TaskBlueprintRequest
        return self.sum_due_offset_of_task_blueprints_as(
            "sum_due_offset_of_task_blueprints", TaskBlueprintRequest())

    def sum_due_offset_of_task_blueprints_as(self, alias: str, child_request):
        child_request.query.sum("due_offset", "sum_due_offset")
        self.query.relation_aggregates.append(
            RelationAggregate("task_blueprint_list", alias, child_request.query, True)
        )
        return self
    def avg_due_offset_of_task_blueprints(self):
        from requests.task_blueprint_request import TaskBlueprintRequest
        return self.avg_due_offset_of_task_blueprints_as(
            "avg_due_offset_of_task_blueprints", TaskBlueprintRequest())

    def avg_due_offset_of_task_blueprints_as(self, alias: str, child_request):
        child_request.query.avg("due_offset", "avg_due_offset")
        self.query.relation_aggregates.append(
            RelationAggregate("task_blueprint_list", alias, child_request.query, True)
        )
        return self
    def standardDeviation_due_offset_of_task_blueprints(self):
        from requests.task_blueprint_request import TaskBlueprintRequest
        return self.standardDeviation_due_offset_of_task_blueprints_as(
            "standardDeviation_due_offset_of_task_blueprints", TaskBlueprintRequest())

    def standardDeviation_due_offset_of_task_blueprints_as(self, alias: str, child_request):
        child_request.query.standardDeviation("due_offset", "standardDeviation_due_offset")
        self.query.relation_aggregates.append(
            RelationAggregate("task_blueprint_list", alias, child_request.query, True)
        )
        return self
    def squareRootOfPopulationStandardDeviation_due_offset_of_task_blueprints(self):
        from requests.task_blueprint_request import TaskBlueprintRequest
        return self.squareRootOfPopulationStandardDeviation_due_offset_of_task_blueprints_as(
            "squareRootOfPopulationStandardDeviation_due_offset_of_task_blueprints", TaskBlueprintRequest())

    def squareRootOfPopulationStandardDeviation_due_offset_of_task_blueprints_as(self, alias: str, child_request):
        child_request.query.squareRootOfPopulationStandardDeviation("due_offset", "squareRootOfPopulationStandardDeviation_due_offset")
        self.query.relation_aggregates.append(
            RelationAggregate("task_blueprint_list", alias, child_request.query, True)
        )
        return self
    def sampleVariance_due_offset_of_task_blueprints(self):
        from requests.task_blueprint_request import TaskBlueprintRequest
        return self.sampleVariance_due_offset_of_task_blueprints_as(
            "sampleVariance_due_offset_of_task_blueprints", TaskBlueprintRequest())

    def sampleVariance_due_offset_of_task_blueprints_as(self, alias: str, child_request):
        child_request.query.sampleVariance("due_offset", "sampleVariance_due_offset")
        self.query.relation_aggregates.append(
            RelationAggregate("task_blueprint_list", alias, child_request.query, True)
        )
        return self
    def samplePopulationVariance_due_offset_of_task_blueprints(self):
        from requests.task_blueprint_request import TaskBlueprintRequest
        return self.samplePopulationVariance_due_offset_of_task_blueprints_as(
            "samplePopulationVariance_due_offset_of_task_blueprints", TaskBlueprintRequest())

    def samplePopulationVariance_due_offset_of_task_blueprints_as(self, alias: str, child_request):
        child_request.query.samplePopulationVariance("due_offset", "samplePopulationVariance_due_offset")
        self.query.relation_aggregates.append(
            RelationAggregate("task_blueprint_list", alias, child_request.query, True)
        )
        return self
    def count_blueprint_choices(self):
        return self.count_blueprint_choices_as("count_blueprint_choices")

    def count_blueprint_choices_as(self, alias: str):
        from requests.blueprint_choice_request import BlueprintChoiceRequest
        return self.count_blueprint_choices_with(alias, BlueprintChoiceRequest())

    def count_blueprint_choices_with(self, alias: str, child_request):
        child_request.query.count_field("id", alias)
        self.query.relation_aggregates.append(
            RelationAggregate("blueprint_choice_list", alias, child_request.query, True)
        )
        return self


    def count_blueprint_subtasks(self):
        return self.count_blueprint_subtasks_as("count_blueprint_subtasks")

    def count_blueprint_subtasks_as(self, alias: str):
        from requests.blueprint_subtask_request import BlueprintSubtaskRequest
        return self.count_blueprint_subtasks_with(alias, BlueprintSubtaskRequest())

    def count_blueprint_subtasks_with(self, alias: str, child_request):
        child_request.query.count_field("id", alias)
        self.query.relation_aggregates.append(
            RelationAggregate("blueprint_subtask_list", alias, child_request.query, True)
        )
        return self

    def min_due_offset_of_blueprint_subtasks(self):
        from requests.blueprint_subtask_request import BlueprintSubtaskRequest
        return self.min_due_offset_of_blueprint_subtasks_as(
            "min_due_offset_of_blueprint_subtasks", BlueprintSubtaskRequest())

    def min_due_offset_of_blueprint_subtasks_as(self, alias: str, child_request):
        child_request.query.min("due_offset", "min_due_offset")
        self.query.relation_aggregates.append(
            RelationAggregate("blueprint_subtask_list", alias, child_request.query, True)
        )
        return self
    def max_due_offset_of_blueprint_subtasks(self):
        from requests.blueprint_subtask_request import BlueprintSubtaskRequest
        return self.max_due_offset_of_blueprint_subtasks_as(
            "max_due_offset_of_blueprint_subtasks", BlueprintSubtaskRequest())

    def max_due_offset_of_blueprint_subtasks_as(self, alias: str, child_request):
        child_request.query.max("due_offset", "max_due_offset")
        self.query.relation_aggregates.append(
            RelationAggregate("blueprint_subtask_list", alias, child_request.query, True)
        )
        return self
    def sum_due_offset_of_blueprint_subtasks(self):
        from requests.blueprint_subtask_request import BlueprintSubtaskRequest
        return self.sum_due_offset_of_blueprint_subtasks_as(
            "sum_due_offset_of_blueprint_subtasks", BlueprintSubtaskRequest())

    def sum_due_offset_of_blueprint_subtasks_as(self, alias: str, child_request):
        child_request.query.sum("due_offset", "sum_due_offset")
        self.query.relation_aggregates.append(
            RelationAggregate("blueprint_subtask_list", alias, child_request.query, True)
        )
        return self
    def avg_due_offset_of_blueprint_subtasks(self):
        from requests.blueprint_subtask_request import BlueprintSubtaskRequest
        return self.avg_due_offset_of_blueprint_subtasks_as(
            "avg_due_offset_of_blueprint_subtasks", BlueprintSubtaskRequest())

    def avg_due_offset_of_blueprint_subtasks_as(self, alias: str, child_request):
        child_request.query.avg("due_offset", "avg_due_offset")
        self.query.relation_aggregates.append(
            RelationAggregate("blueprint_subtask_list", alias, child_request.query, True)
        )
        return self
    def standardDeviation_due_offset_of_blueprint_subtasks(self):
        from requests.blueprint_subtask_request import BlueprintSubtaskRequest
        return self.standardDeviation_due_offset_of_blueprint_subtasks_as(
            "standardDeviation_due_offset_of_blueprint_subtasks", BlueprintSubtaskRequest())

    def standardDeviation_due_offset_of_blueprint_subtasks_as(self, alias: str, child_request):
        child_request.query.standardDeviation("due_offset", "standardDeviation_due_offset")
        self.query.relation_aggregates.append(
            RelationAggregate("blueprint_subtask_list", alias, child_request.query, True)
        )
        return self
    def squareRootOfPopulationStandardDeviation_due_offset_of_blueprint_subtasks(self):
        from requests.blueprint_subtask_request import BlueprintSubtaskRequest
        return self.squareRootOfPopulationStandardDeviation_due_offset_of_blueprint_subtasks_as(
            "squareRootOfPopulationStandardDeviation_due_offset_of_blueprint_subtasks", BlueprintSubtaskRequest())

    def squareRootOfPopulationStandardDeviation_due_offset_of_blueprint_subtasks_as(self, alias: str, child_request):
        child_request.query.squareRootOfPopulationStandardDeviation("due_offset", "squareRootOfPopulationStandardDeviation_due_offset")
        self.query.relation_aggregates.append(
            RelationAggregate("blueprint_subtask_list", alias, child_request.query, True)
        )
        return self
    def sampleVariance_due_offset_of_blueprint_subtasks(self):
        from requests.blueprint_subtask_request import BlueprintSubtaskRequest
        return self.sampleVariance_due_offset_of_blueprint_subtasks_as(
            "sampleVariance_due_offset_of_blueprint_subtasks", BlueprintSubtaskRequest())

    def sampleVariance_due_offset_of_blueprint_subtasks_as(self, alias: str, child_request):
        child_request.query.sampleVariance("due_offset", "sampleVariance_due_offset")
        self.query.relation_aggregates.append(
            RelationAggregate("blueprint_subtask_list", alias, child_request.query, True)
        )
        return self
    def samplePopulationVariance_due_offset_of_blueprint_subtasks(self):
        from requests.blueprint_subtask_request import BlueprintSubtaskRequest
        return self.samplePopulationVariance_due_offset_of_blueprint_subtasks_as(
            "samplePopulationVariance_due_offset_of_blueprint_subtasks", BlueprintSubtaskRequest())

    def samplePopulationVariance_due_offset_of_blueprint_subtasks_as(self, alias: str, child_request):
        child_request.query.samplePopulationVariance("due_offset", "samplePopulationVariance_due_offset")
        self.query.relation_aggregates.append(
            RelationAggregate("blueprint_subtask_list", alias, child_request.query, True)
        )
        return self
    def count_inbox_notices(self):
        return self.count_inbox_notices_as("count_inbox_notices")

    def count_inbox_notices_as(self, alias: str):
        from requests.inbox_notice_request import InboxNoticeRequest
        return self.count_inbox_notices_with(alias, InboxNoticeRequest())

    def count_inbox_notices_with(self, alias: str, child_request):
        child_request.query.count_field("id", alias)
        self.query.relation_aggregates.append(
            RelationAggregate("inbox_notice_list", alias, child_request.query, True)
        )
        return self



class ExecutableWorkSpaceRequest:
    def __init__(self, request):
        self._request = request

    def comment(self, c: str):
        self._request.comment(c)
        return self

    def new_entity(self, context) -> WorkSpace:
        request = self._request
        if not request._comment or not request._comment.strip() or not request._purpose or not request._purpose.strip():
            raise ValueError("Security audit failure: non-empty comment() and purpose() are required before new_entity()")
        entity = context.initialize_entity("WorkSpace", WorkSpace._teaql_construct())
        if not isinstance(entity, WorkSpace):
            raise TypeError("entity initializer returned an incompatible WorkSpace")
        return entity

    async def execute_for_result(self, context):
        self = self._request
        if not self._purpose or not self._purpose.strip() or not self._comment or not self._comment.strip():
            raise Exception("Security audit failure: comment() and purpose() must be called before execute_for_rows()")
        service = _data_service(context)
        req = QueryRequest(context.prepare_query(self.query), _comment=self._comment, _purpose=self._purpose)
        return await service.query(context, req)

    async def execute_for_rows(self, context):
        return (await self.execute_for_result(context)).rows

    async def execute_for_list(self, context) -> SmartList[WorkSpace]:
        result = await self.execute_for_result(context)
        query_root = EntityRoot()
        return SmartList(
            (WorkSpace._teaql_construct(_entity_root=query_root, **row) for row in result.rows),
            facets=result.facets)

    async def execute_for_page(self, context, offset: int, limit: int) -> TeaQLPage[WorkSpace]:
        request = self._request
        if not request._purpose or not request._purpose.strip() or not request._comment or not request._comment.strip():
            raise ValueError("Security audit failure: comment() and purpose() must be called before execute_for_page()")
        query = deepcopy(request.query)
        query.offset(offset).limit(limit)
        authorized = context.prepare_query(query)
        service = _data_service(context)
        alias = "__teaql_total"
        if authorized.id_set_pagination is not None:
            row_result = await service.query(context, QueryRequest(authorized, _comment=request._comment, _purpose=request._purpose))
            retained_count, accuracy = context.id_set_count()
            if accuracy == "EXACT":
                total_count = retained_count
            else:
                count_result = await service.query(context, QueryRequest(authorized.for_exact_count(alias), _comment=request._comment, _purpose=request._purpose))
                if not count_result.rows or not isinstance(count_result.rows[0].get(alias), (int, float)):
                    raise RuntimeError("dataService did not return an exact page count")
                total_count = int(count_result.rows[0][alias])
        else:
            count_result = await service.query(context, QueryRequest(authorized.for_exact_count(alias), _comment=request._comment, _purpose=request._purpose))
            if not count_result.rows or not isinstance(count_result.rows[0].get(alias), (int, float)):
                raise RuntimeError("dataService did not return an exact page count")
            total_count = int(count_result.rows[0][alias])
            row_result = await service.query(context, QueryRequest(authorized, _comment=request._comment, _purpose=request._purpose))
        query_root = EntityRoot()
        data = SmartList(WorkSpace._teaql_construct(_entity_root=query_root, **row) for row in row_result.rows)
        return TeaQLPage(data=data, total_count=total_count, offset=offset, limit=limit)

    async def execute_for_one(self, context):
        request = deepcopy(self._request)
        request.limit(1)
        entities = await ExecutableWorkSpaceRequest(request).execute_for_list(context)
        return entities[0] if entities else None

    async def execute_for_stream(self, context, chunk_size: int = 1000):
        """Yield entity chunks lazily from the provider cursor."""
        request = self._request
        if not request._purpose or not request._purpose.strip() or not request._comment or not request._comment.strip():
            raise Exception("Security audit failure: comment() and purpose() must be called before execute_for_stream()")
        service = _data_service(context)
        if not hasattr(service, "query_stream"):
            raise RuntimeError("dataService does not implement query_stream")
        query_root = EntityRoot()
        async for chunk in service.query_stream(context, QueryRequest(context.prepare_query(request.query), _comment=request._comment, _purpose=request._purpose), chunk_size):
            for row in chunk.rows:
                yield WorkSpace._teaql_construct(_entity_root=query_root, **row)
