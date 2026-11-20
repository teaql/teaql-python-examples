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
from models.work_account import WorkAccount
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

class WorkAccountRequest:
    def __init__(self, minimal=False):
        self.query = SelectQuery("WorkAccount")
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
        return ExecutableWorkAccountRequest(self)

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
        self.query.project("id", "work_space", "display_name", "email_address", "password_hash", "version")
        return self

    def select_id(self):
        self.query.project("id")
        return self


    def select_display_name(self):
        self.query.project("display_name")
        return self

    def select_email_address(self):
        self.query.project("email_address")
        return self

    def select_password_hash(self):
        self.query.project("password_hash")
        return self

    def select_version(self):
        self.query.project("version")
        return self

    def select_work_space_with(self, child_request):
        self.query.project("work_space")
        self.query.relation_query("work_space", child_request.query)
        return self
    def with_work_space_matching(self, child_request):
        child_request.query.projection = ["id"]
        self.query.and_filter(in_subquery(column("work_space"), "WorkSpace", child_request.query))
        return self

    def without_work_space_matching(self, child_request):
        child_request.query.projection = ["id"]
        self.query.and_filter(not_in_subquery(column("work_space"), "WorkSpace", child_request.query))
        return self

    def have_work_space(self):
        self.query.and_filter(is_not_null(column("work_space")))
        return self

    def have_no_work_space(self):
        self.query.and_filter(is_null(column("work_space")))
        return self

    def whose_id_is(self, val):
        if isinstance(val, (list, tuple, set, frozenset, dict)):
            raise TypeError("whose_id_is expects one scalar ID; use whose_id_in(*values) for a collection")
        self.query.and_filter(eq("id", val))
        return self

    def whose_id_is_not(self, val):
        if isinstance(val, (list, tuple, set, frozenset, dict)):
            raise TypeError("whose_id_is_not expects one scalar ID; use whose_id_not_in(*values) for a collection")
        self.query.and_filter(ne("id", val))
        return self

    def whose_id_in(self, *vals):
        _set_arguments("whose_id_in", vals)
        if not vals:
            self.query.and_filter(is_null(column("id")))
            return self
        self.query.and_filter(in_list("id", list(vals)))
        return self

    def whose_id_not_in(self, *vals):
        _set_arguments("whose_id_not_in", vals)
        if not vals:
            return self
        self.query.and_filter(not_in_list("id", list(vals)))
        return self

    def whose_id_greater_than(self, val):
        self.query.and_filter(gt("id", val))
        return self

    def whose_id_greater_than_or_equal_to(self, val):
        self.query.and_filter(gte("id", val))
        return self

    def whose_id_less_than(self, val):
        self.query.and_filter(lt("id", val))
        return self

    def whose_id_less_than_or_equal_to(self, val):
        self.query.and_filter(lte("id", val))
        return self

    def whose_id_between(self, lower, upper):
        self.query.and_filter(between(column("id"), value(lower), value(upper)))
        return self

    def whose_id_is_known(self):
        self.query.and_filter(is_not_null(column("id")))
        return self

    def whose_id_is_unknown(self):
        self.query.and_filter(is_null(column("id")))
        return self

    def filter_by_work_space(self, val):
        self.query.and_filter(eq("work_space", val))
        return self

    def whose_display_name_contains(self, val: str):
        self.query.and_filter(contain("display_name", val))
        return self

    def whose_display_name_not_containing(self, val: str):
        self.query.and_filter(not_contain("display_name", val))
        return self

    def whose_display_name_starting_with(self, val: str):
        self.query.and_filter(begin_with("display_name", val))
        return self

    def whose_display_name_not_starting_with(self, val: str):
        self.query.and_filter(not_begin_with("display_name", val))
        return self

    def whose_display_name_ending_with(self, val: str):
        self.query.and_filter(end_with("display_name", val))
        return self

    def whose_display_name_not_ending_with(self, val: str):
        self.query.and_filter(not_end_with("display_name", val))
        return self

    def whose_display_name_sounding_like(self, val: str):
        self.query.and_filter(sound_like("display_name", val))
        return self

    def whose_display_name_is(self, val: str):
        self.query.and_filter(eq("display_name", val))
        return self
    def whose_display_name_is_not(self, val):
        self.query.and_filter(ne("display_name", val))
        return self

    def whose_display_name_in(self, *vals):
        _set_arguments("whose_display_name_in", vals)
        if not vals:
            self.query.and_filter(is_null(column("id")))
            return self
        self.query.and_filter(in_list("display_name", list(vals)))
        return self

    def whose_display_name_not_in(self, *vals):
        _set_arguments("whose_display_name_not_in", vals)
        if not vals:
            return self
        self.query.and_filter(not_in_list("display_name", list(vals)))
        return self

    def whose_display_name_greater_than(self, val):
        self.query.and_filter(gt("display_name", val))
        return self

    def whose_display_name_greater_than_or_equal_to(self, val):
        self.query.and_filter(gte("display_name", val))
        return self

    def whose_display_name_less_than(self, val):
        self.query.and_filter(lt("display_name", val))
        return self

    def whose_display_name_less_than_or_equal_to(self, val):
        self.query.and_filter(lte("display_name", val))
        return self

    def whose_display_name_between(self, lower, upper):
        self.query.and_filter(between(column("display_name"), value(lower), value(upper)))
        return self

    def whose_display_name_is_known(self):
        self.query.and_filter(is_not_null(column("display_name")))
        return self

    def whose_display_name_is_unknown(self):
        self.query.and_filter(is_null(column("display_name")))
        return self

    def whose_email_address_contains(self, val: str):
        self.query.and_filter(contain("email_address", val))
        return self

    def whose_email_address_not_containing(self, val: str):
        self.query.and_filter(not_contain("email_address", val))
        return self

    def whose_email_address_starting_with(self, val: str):
        self.query.and_filter(begin_with("email_address", val))
        return self

    def whose_email_address_not_starting_with(self, val: str):
        self.query.and_filter(not_begin_with("email_address", val))
        return self

    def whose_email_address_ending_with(self, val: str):
        self.query.and_filter(end_with("email_address", val))
        return self

    def whose_email_address_not_ending_with(self, val: str):
        self.query.and_filter(not_end_with("email_address", val))
        return self

    def whose_email_address_sounding_like(self, val: str):
        self.query.and_filter(sound_like("email_address", val))
        return self

    def whose_email_address_is(self, val: str):
        self.query.and_filter(eq("email_address", val))
        return self
    def whose_email_address_is_not(self, val):
        self.query.and_filter(ne("email_address", val))
        return self

    def whose_email_address_in(self, *vals):
        _set_arguments("whose_email_address_in", vals)
        if not vals:
            self.query.and_filter(is_null(column("id")))
            return self
        self.query.and_filter(in_list("email_address", list(vals)))
        return self

    def whose_email_address_not_in(self, *vals):
        _set_arguments("whose_email_address_not_in", vals)
        if not vals:
            return self
        self.query.and_filter(not_in_list("email_address", list(vals)))
        return self

    def whose_email_address_greater_than(self, val):
        self.query.and_filter(gt("email_address", val))
        return self

    def whose_email_address_greater_than_or_equal_to(self, val):
        self.query.and_filter(gte("email_address", val))
        return self

    def whose_email_address_less_than(self, val):
        self.query.and_filter(lt("email_address", val))
        return self

    def whose_email_address_less_than_or_equal_to(self, val):
        self.query.and_filter(lte("email_address", val))
        return self

    def whose_email_address_between(self, lower, upper):
        self.query.and_filter(between(column("email_address"), value(lower), value(upper)))
        return self

    def whose_email_address_is_known(self):
        self.query.and_filter(is_not_null(column("email_address")))
        return self

    def whose_email_address_is_unknown(self):
        self.query.and_filter(is_null(column("email_address")))
        return self

    def whose_password_hash_contains(self, val: str):
        self.query.and_filter(contain("password_hash", val))
        return self

    def whose_password_hash_not_containing(self, val: str):
        self.query.and_filter(not_contain("password_hash", val))
        return self

    def whose_password_hash_starting_with(self, val: str):
        self.query.and_filter(begin_with("password_hash", val))
        return self

    def whose_password_hash_not_starting_with(self, val: str):
        self.query.and_filter(not_begin_with("password_hash", val))
        return self

    def whose_password_hash_ending_with(self, val: str):
        self.query.and_filter(end_with("password_hash", val))
        return self

    def whose_password_hash_not_ending_with(self, val: str):
        self.query.and_filter(not_end_with("password_hash", val))
        return self

    def whose_password_hash_sounding_like(self, val: str):
        self.query.and_filter(sound_like("password_hash", val))
        return self

    def whose_password_hash_is(self, val: str):
        self.query.and_filter(eq("password_hash", val))
        return self
    def whose_password_hash_is_not(self, val):
        self.query.and_filter(ne("password_hash", val))
        return self

    def whose_password_hash_in(self, *vals):
        _set_arguments("whose_password_hash_in", vals)
        if not vals:
            self.query.and_filter(is_null(column("id")))
            return self
        self.query.and_filter(in_list("password_hash", list(vals)))
        return self

    def whose_password_hash_not_in(self, *vals):
        _set_arguments("whose_password_hash_not_in", vals)
        if not vals:
            return self
        self.query.and_filter(not_in_list("password_hash", list(vals)))
        return self

    def whose_password_hash_greater_than(self, val):
        self.query.and_filter(gt("password_hash", val))
        return self

    def whose_password_hash_greater_than_or_equal_to(self, val):
        self.query.and_filter(gte("password_hash", val))
        return self

    def whose_password_hash_less_than(self, val):
        self.query.and_filter(lt("password_hash", val))
        return self

    def whose_password_hash_less_than_or_equal_to(self, val):
        self.query.and_filter(lte("password_hash", val))
        return self

    def whose_password_hash_between(self, lower, upper):
        self.query.and_filter(between(column("password_hash"), value(lower), value(upper)))
        return self

    def whose_password_hash_is_known(self):
        self.query.and_filter(is_not_null(column("password_hash")))
        return self

    def whose_password_hash_is_unknown(self):
        self.query.and_filter(is_null(column("password_hash")))
        return self

    def whose_version_is(self, val):
        self.query.and_filter(eq("version", val))
        return self

    def whose_version_is_not(self, val):
        self.query.and_filter(ne("version", val))
        return self

    def whose_version_in(self, *vals):
        _set_arguments("whose_version_in", vals)
        if not vals:
            self.query.and_filter(is_null(column("id")))
            return self
        self.query.and_filter(in_list("version", list(vals)))
        return self

    def whose_version_not_in(self, *vals):
        _set_arguments("whose_version_not_in", vals)
        if not vals:
            return self
        self.query.and_filter(not_in_list("version", list(vals)))
        return self

    def whose_version_greater_than(self, val):
        self.query.and_filter(gt("version", val))
        return self

    def whose_version_greater_than_or_equal_to(self, val):
        self.query.and_filter(gte("version", val))
        return self

    def whose_version_less_than(self, val):
        self.query.and_filter(lt("version", val))
        return self

    def whose_version_less_than_or_equal_to(self, val):
        self.query.and_filter(lte("version", val))
        return self

    def whose_version_between(self, lower, upper):
        self.query.and_filter(between(column("version"), value(lower), value(upper)))
        return self

    def whose_version_is_known(self):
        self.query.and_filter(is_not_null(column("version")))
        return self

    def whose_version_is_unknown(self):
        self.query.and_filter(is_null(column("version")))
        return self

    def order_by_id_ascending(self):
        self.query.order_by("id", "asc")
        return self

    def order_by_id_descending(self):
        self.query.order_by("id", "desc")
        return self


    def order_by_display_name_ascending(self):
        self.query.order_by("display_name", "asc")
        return self

    def order_by_display_name_descending(self):
        self.query.order_by("display_name", "desc")
        return self

    def order_by_email_address_ascending(self):
        self.query.order_by("email_address", "asc")
        return self

    def order_by_email_address_descending(self):
        self.query.order_by("email_address", "desc")
        return self

    def order_by_password_hash_ascending(self):
        self.query.order_by("password_hash", "asc")
        return self

    def order_by_password_hash_descending(self):
        self.query.order_by("password_hash", "desc")
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
    def group_by_work_space(self):
        self.query.group_by("work_space")
        return self

    def group_by_work_space_as(self, ret_name: str):
        self.query.group_by("work_space")
        return self
    def group_by_display_name(self):
        self.query.group_by("display_name")
        return self

    def group_by_display_name_as(self, ret_name: str):
        self.query.group_by("display_name")
        return self
    def group_by_email_address(self):
        self.query.group_by("email_address")
        return self

    def group_by_email_address_as(self, ret_name: str):
        self.query.group_by("email_address")
        return self
    def group_by_password_hash(self):
        self.query.group_by("password_hash")
        return self

    def group_by_password_hash_as(self, ret_name: str):
        self.query.group_by("password_hash")
        return self
    def group_by_version(self):
        self.query.group_by("version")
        return self

    def group_by_version_as(self, ret_name: str):
        self.query.group_by("version")
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
    def select_work_task_list_as_created_by(self):
        from requests.work_task_request import WorkTaskRequest
        return self.select_work_task_list_as_created_by_with(WorkTaskRequest())

    def select_work_task_list_as_created_by_with(self, child_request):
        self.query.relation_query("work_task_list_as_created_by", child_request.query)
        return self
    def select_work_task_list_as_assignee(self):
        from requests.work_task_request import WorkTaskRequest
        return self.select_work_task_list_as_assignee_with(WorkTaskRequest())

    def select_work_task_list_as_assignee_with(self, child_request):
        self.query.relation_query("work_task_list_as_assignee", child_request.query)
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
    def have_work_projects(self):
        from requests.work_project_request import WorkProjectRequest
        return self.with_work_project_list_matching(WorkProjectRequest())

    def have_no_work_projects(self):
        from requests.work_project_request import WorkProjectRequest
        return self.without_work_project_list_matching(WorkProjectRequest())

    def with_work_project_list_matching(self, child_request):
        child_request.query.projection = ["owner_account"]
        self.query.and_filter(in_subquery(column("id"), "WorkProject", child_request.query))
        return self

    def without_work_project_list_matching(self, child_request):
        child_request.query.projection = ["owner_account"]
        self.query.and_filter(not_in_subquery(column("id"), "WorkProject", child_request.query))
        return self
    def have_project_memberships(self):
        from requests.project_membership_request import ProjectMembershipRequest
        return self.with_project_membership_list_matching(ProjectMembershipRequest())

    def have_no_project_memberships(self):
        from requests.project_membership_request import ProjectMembershipRequest
        return self.without_project_membership_list_matching(ProjectMembershipRequest())

    def with_project_membership_list_matching(self, child_request):
        child_request.query.projection = ["member_account"]
        self.query.and_filter(in_subquery(column("id"), "ProjectMembership", child_request.query))
        return self

    def without_project_membership_list_matching(self, child_request):
        child_request.query.projection = ["member_account"]
        self.query.and_filter(not_in_subquery(column("id"), "ProjectMembership", child_request.query))
        return self
    def have_work_tasks_as_created_by(self):
        from requests.work_task_request import WorkTaskRequest
        return self.with_work_task_list_as_created_by_matching(WorkTaskRequest())

    def have_no_work_tasks_as_created_by(self):
        from requests.work_task_request import WorkTaskRequest
        return self.without_work_task_list_as_created_by_matching(WorkTaskRequest())

    def with_work_task_list_as_created_by_matching(self, child_request):
        child_request.query.projection = ["created_by"]
        self.query.and_filter(in_subquery(column("id"), "WorkTask", child_request.query))
        return self

    def without_work_task_list_as_created_by_matching(self, child_request):
        child_request.query.projection = ["created_by"]
        self.query.and_filter(not_in_subquery(column("id"), "WorkTask", child_request.query))
        return self
    def have_work_tasks_as_assignee(self):
        from requests.work_task_request import WorkTaskRequest
        return self.with_work_task_list_as_assignee_matching(WorkTaskRequest())

    def have_no_work_tasks_as_assignee(self):
        from requests.work_task_request import WorkTaskRequest
        return self.without_work_task_list_as_assignee_matching(WorkTaskRequest())

    def with_work_task_list_as_assignee_matching(self, child_request):
        child_request.query.projection = ["assignee"]
        self.query.and_filter(in_subquery(column("id"), "WorkTask", child_request.query))
        return self

    def without_work_task_list_as_assignee_matching(self, child_request):
        child_request.query.projection = ["assignee"]
        self.query.and_filter(not_in_subquery(column("id"), "WorkTask", child_request.query))
        return self
    def have_work_subtasks(self):
        from requests.work_subtask_request import WorkSubtaskRequest
        return self.with_work_subtask_list_matching(WorkSubtaskRequest())

    def have_no_work_subtasks(self):
        from requests.work_subtask_request import WorkSubtaskRequest
        return self.without_work_subtask_list_matching(WorkSubtaskRequest())

    def with_work_subtask_list_matching(self, child_request):
        child_request.query.projection = ["assignee"]
        self.query.and_filter(in_subquery(column("id"), "WorkSubtask", child_request.query))
        return self

    def without_work_subtask_list_matching(self, child_request):
        child_request.query.projection = ["assignee"]
        self.query.and_filter(not_in_subquery(column("id"), "WorkSubtask", child_request.query))
        return self
    def have_task_comments(self):
        from requests.task_comment_request import TaskCommentRequest
        return self.with_task_comment_list_matching(TaskCommentRequest())

    def have_no_task_comments(self):
        from requests.task_comment_request import TaskCommentRequest
        return self.without_task_comment_list_matching(TaskCommentRequest())

    def with_task_comment_list_matching(self, child_request):
        child_request.query.projection = ["author"]
        self.query.and_filter(in_subquery(column("id"), "TaskComment", child_request.query))
        return self

    def without_task_comment_list_matching(self, child_request):
        child_request.query.projection = ["author"]
        self.query.and_filter(not_in_subquery(column("id"), "TaskComment", child_request.query))
        return self
    def have_task_events(self):
        from requests.task_event_request import TaskEventRequest
        return self.with_task_event_list_matching(TaskEventRequest())

    def have_no_task_events(self):
        from requests.task_event_request import TaskEventRequest
        return self.without_task_event_list_matching(TaskEventRequest())

    def with_task_event_list_matching(self, child_request):
        child_request.query.projection = ["actor"]
        self.query.and_filter(in_subquery(column("id"), "TaskEvent", child_request.query))
        return self

    def without_task_event_list_matching(self, child_request):
        child_request.query.projection = ["actor"]
        self.query.and_filter(not_in_subquery(column("id"), "TaskEvent", child_request.query))
        return self
    def have_task_participants(self):
        from requests.task_participant_request import TaskParticipantRequest
        return self.with_task_participant_list_matching(TaskParticipantRequest())

    def have_no_task_participants(self):
        from requests.task_participant_request import TaskParticipantRequest
        return self.without_task_participant_list_matching(TaskParticipantRequest())

    def with_task_participant_list_matching(self, child_request):
        child_request.query.projection = ["participant"]
        self.query.and_filter(in_subquery(column("id"), "TaskParticipant", child_request.query))
        return self

    def without_task_participant_list_matching(self, child_request):
        child_request.query.projection = ["participant"]
        self.query.and_filter(not_in_subquery(column("id"), "TaskParticipant", child_request.query))
        return self
    def have_deleted_task_viewers(self):
        from requests.deleted_task_viewer_request import DeletedTaskViewerRequest
        return self.with_deleted_task_viewer_list_matching(DeletedTaskViewerRequest())

    def have_no_deleted_task_viewers(self):
        from requests.deleted_task_viewer_request import DeletedTaskViewerRequest
        return self.without_deleted_task_viewer_list_matching(DeletedTaskViewerRequest())

    def with_deleted_task_viewer_list_matching(self, child_request):
        child_request.query.projection = ["viewer"]
        self.query.and_filter(in_subquery(column("id"), "DeletedTaskViewer", child_request.query))
        return self

    def without_deleted_task_viewer_list_matching(self, child_request):
        child_request.query.projection = ["viewer"]
        self.query.and_filter(not_in_subquery(column("id"), "DeletedTaskViewer", child_request.query))
        return self
    def have_task_blueprints(self):
        from requests.task_blueprint_request import TaskBlueprintRequest
        return self.with_task_blueprint_list_matching(TaskBlueprintRequest())

    def have_no_task_blueprints(self):
        from requests.task_blueprint_request import TaskBlueprintRequest
        return self.without_task_blueprint_list_matching(TaskBlueprintRequest())

    def with_task_blueprint_list_matching(self, child_request):
        child_request.query.projection = ["assignee"]
        self.query.and_filter(in_subquery(column("id"), "TaskBlueprint", child_request.query))
        return self

    def without_task_blueprint_list_matching(self, child_request):
        child_request.query.projection = ["assignee"]
        self.query.and_filter(not_in_subquery(column("id"), "TaskBlueprint", child_request.query))
        return self
    def have_blueprint_subtasks(self):
        from requests.blueprint_subtask_request import BlueprintSubtaskRequest
        return self.with_blueprint_subtask_list_matching(BlueprintSubtaskRequest())

    def have_no_blueprint_subtasks(self):
        from requests.blueprint_subtask_request import BlueprintSubtaskRequest
        return self.without_blueprint_subtask_list_matching(BlueprintSubtaskRequest())

    def with_blueprint_subtask_list_matching(self, child_request):
        child_request.query.projection = ["assignee"]
        self.query.and_filter(in_subquery(column("id"), "BlueprintSubtask", child_request.query))
        return self

    def without_blueprint_subtask_list_matching(self, child_request):
        child_request.query.projection = ["assignee"]
        self.query.and_filter(not_in_subquery(column("id"), "BlueprintSubtask", child_request.query))
        return self
    def have_inbox_notices(self):
        from requests.inbox_notice_request import InboxNoticeRequest
        return self.with_inbox_notice_list_matching(InboxNoticeRequest())

    def have_no_inbox_notices(self):
        from requests.inbox_notice_request import InboxNoticeRequest
        return self.without_inbox_notice_list_matching(InboxNoticeRequest())

    def with_inbox_notice_list_matching(self, child_request):
        child_request.query.projection = ["recipient"]
        self.query.and_filter(in_subquery(column("id"), "InboxNotice", child_request.query))
        return self

    def without_inbox_notice_list_matching(self, child_request):
        child_request.query.projection = ["recipient"]
        self.query.and_filter(not_in_subquery(column("id"), "InboxNotice", child_request.query))
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


    def count_work_tasks_as_created_by(self):
        return self.count_work_tasks_as_created_by_as("count_work_tasks_as_created_by")

    def count_work_tasks_as_created_by_as(self, alias: str):
        from requests.work_task_request import WorkTaskRequest
        return self.count_work_tasks_as_created_by_with(alias, WorkTaskRequest())

    def count_work_tasks_as_created_by_with(self, alias: str, child_request):
        child_request.query.count_field("id", alias)
        self.query.relation_aggregates.append(
            RelationAggregate("work_task_list_as_created_by", alias, child_request.query, True)
        )
        return self

    def min_deleted_epoch_of_work_tasks_as_created_by(self):
        from requests.work_task_request import WorkTaskRequest
        return self.min_deleted_epoch_of_work_tasks_as_created_by_as(
            "min_deleted_epoch_of_work_tasks_as_created_by", WorkTaskRequest())

    def min_deleted_epoch_of_work_tasks_as_created_by_as(self, alias: str, child_request):
        child_request.query.min("deleted_epoch", "min_deleted_epoch")
        self.query.relation_aggregates.append(
            RelationAggregate("work_task_list_as_created_by", alias, child_request.query, True)
        )
        return self
    def max_deleted_epoch_of_work_tasks_as_created_by(self):
        from requests.work_task_request import WorkTaskRequest
        return self.max_deleted_epoch_of_work_tasks_as_created_by_as(
            "max_deleted_epoch_of_work_tasks_as_created_by", WorkTaskRequest())

    def max_deleted_epoch_of_work_tasks_as_created_by_as(self, alias: str, child_request):
        child_request.query.max("deleted_epoch", "max_deleted_epoch")
        self.query.relation_aggregates.append(
            RelationAggregate("work_task_list_as_created_by", alias, child_request.query, True)
        )
        return self
    def sum_deleted_epoch_of_work_tasks_as_created_by(self):
        from requests.work_task_request import WorkTaskRequest
        return self.sum_deleted_epoch_of_work_tasks_as_created_by_as(
            "sum_deleted_epoch_of_work_tasks_as_created_by", WorkTaskRequest())

    def sum_deleted_epoch_of_work_tasks_as_created_by_as(self, alias: str, child_request):
        child_request.query.sum("deleted_epoch", "sum_deleted_epoch")
        self.query.relation_aggregates.append(
            RelationAggregate("work_task_list_as_created_by", alias, child_request.query, True)
        )
        return self
    def avg_deleted_epoch_of_work_tasks_as_created_by(self):
        from requests.work_task_request import WorkTaskRequest
        return self.avg_deleted_epoch_of_work_tasks_as_created_by_as(
            "avg_deleted_epoch_of_work_tasks_as_created_by", WorkTaskRequest())

    def avg_deleted_epoch_of_work_tasks_as_created_by_as(self, alias: str, child_request):
        child_request.query.avg("deleted_epoch", "avg_deleted_epoch")
        self.query.relation_aggregates.append(
            RelationAggregate("work_task_list_as_created_by", alias, child_request.query, True)
        )
        return self
    def standardDeviation_deleted_epoch_of_work_tasks_as_created_by(self):
        from requests.work_task_request import WorkTaskRequest
        return self.standardDeviation_deleted_epoch_of_work_tasks_as_created_by_as(
            "standardDeviation_deleted_epoch_of_work_tasks_as_created_by", WorkTaskRequest())

    def standardDeviation_deleted_epoch_of_work_tasks_as_created_by_as(self, alias: str, child_request):
        child_request.query.standardDeviation("deleted_epoch", "standardDeviation_deleted_epoch")
        self.query.relation_aggregates.append(
            RelationAggregate("work_task_list_as_created_by", alias, child_request.query, True)
        )
        return self
    def squareRootOfPopulationStandardDeviation_deleted_epoch_of_work_tasks_as_created_by(self):
        from requests.work_task_request import WorkTaskRequest
        return self.squareRootOfPopulationStandardDeviation_deleted_epoch_of_work_tasks_as_created_by_as(
            "squareRootOfPopulationStandardDeviation_deleted_epoch_of_work_tasks_as_created_by", WorkTaskRequest())

    def squareRootOfPopulationStandardDeviation_deleted_epoch_of_work_tasks_as_created_by_as(self, alias: str, child_request):
        child_request.query.squareRootOfPopulationStandardDeviation("deleted_epoch", "squareRootOfPopulationStandardDeviation_deleted_epoch")
        self.query.relation_aggregates.append(
            RelationAggregate("work_task_list_as_created_by", alias, child_request.query, True)
        )
        return self
    def sampleVariance_deleted_epoch_of_work_tasks_as_created_by(self):
        from requests.work_task_request import WorkTaskRequest
        return self.sampleVariance_deleted_epoch_of_work_tasks_as_created_by_as(
            "sampleVariance_deleted_epoch_of_work_tasks_as_created_by", WorkTaskRequest())

    def sampleVariance_deleted_epoch_of_work_tasks_as_created_by_as(self, alias: str, child_request):
        child_request.query.sampleVariance("deleted_epoch", "sampleVariance_deleted_epoch")
        self.query.relation_aggregates.append(
            RelationAggregate("work_task_list_as_created_by", alias, child_request.query, True)
        )
        return self
    def samplePopulationVariance_deleted_epoch_of_work_tasks_as_created_by(self):
        from requests.work_task_request import WorkTaskRequest
        return self.samplePopulationVariance_deleted_epoch_of_work_tasks_as_created_by_as(
            "samplePopulationVariance_deleted_epoch_of_work_tasks_as_created_by", WorkTaskRequest())

    def samplePopulationVariance_deleted_epoch_of_work_tasks_as_created_by_as(self, alias: str, child_request):
        child_request.query.samplePopulationVariance("deleted_epoch", "samplePopulationVariance_deleted_epoch")
        self.query.relation_aggregates.append(
            RelationAggregate("work_task_list_as_created_by", alias, child_request.query, True)
        )
        return self
    def min_task_order_of_work_tasks_as_created_by(self):
        from requests.work_task_request import WorkTaskRequest
        return self.min_task_order_of_work_tasks_as_created_by_as(
            "min_task_order_of_work_tasks_as_created_by", WorkTaskRequest())

    def min_task_order_of_work_tasks_as_created_by_as(self, alias: str, child_request):
        child_request.query.min("task_order", "min_task_order")
        self.query.relation_aggregates.append(
            RelationAggregate("work_task_list_as_created_by", alias, child_request.query, True)
        )
        return self
    def max_task_order_of_work_tasks_as_created_by(self):
        from requests.work_task_request import WorkTaskRequest
        return self.max_task_order_of_work_tasks_as_created_by_as(
            "max_task_order_of_work_tasks_as_created_by", WorkTaskRequest())

    def max_task_order_of_work_tasks_as_created_by_as(self, alias: str, child_request):
        child_request.query.max("task_order", "max_task_order")
        self.query.relation_aggregates.append(
            RelationAggregate("work_task_list_as_created_by", alias, child_request.query, True)
        )
        return self
    def sum_task_order_of_work_tasks_as_created_by(self):
        from requests.work_task_request import WorkTaskRequest
        return self.sum_task_order_of_work_tasks_as_created_by_as(
            "sum_task_order_of_work_tasks_as_created_by", WorkTaskRequest())

    def sum_task_order_of_work_tasks_as_created_by_as(self, alias: str, child_request):
        child_request.query.sum("task_order", "sum_task_order")
        self.query.relation_aggregates.append(
            RelationAggregate("work_task_list_as_created_by", alias, child_request.query, True)
        )
        return self
    def avg_task_order_of_work_tasks_as_created_by(self):
        from requests.work_task_request import WorkTaskRequest
        return self.avg_task_order_of_work_tasks_as_created_by_as(
            "avg_task_order_of_work_tasks_as_created_by", WorkTaskRequest())

    def avg_task_order_of_work_tasks_as_created_by_as(self, alias: str, child_request):
        child_request.query.avg("task_order", "avg_task_order")
        self.query.relation_aggregates.append(
            RelationAggregate("work_task_list_as_created_by", alias, child_request.query, True)
        )
        return self
    def standardDeviation_task_order_of_work_tasks_as_created_by(self):
        from requests.work_task_request import WorkTaskRequest
        return self.standardDeviation_task_order_of_work_tasks_as_created_by_as(
            "standardDeviation_task_order_of_work_tasks_as_created_by", WorkTaskRequest())

    def standardDeviation_task_order_of_work_tasks_as_created_by_as(self, alias: str, child_request):
        child_request.query.standardDeviation("task_order", "standardDeviation_task_order")
        self.query.relation_aggregates.append(
            RelationAggregate("work_task_list_as_created_by", alias, child_request.query, True)
        )
        return self
    def squareRootOfPopulationStandardDeviation_task_order_of_work_tasks_as_created_by(self):
        from requests.work_task_request import WorkTaskRequest
        return self.squareRootOfPopulationStandardDeviation_task_order_of_work_tasks_as_created_by_as(
            "squareRootOfPopulationStandardDeviation_task_order_of_work_tasks_as_created_by", WorkTaskRequest())

    def squareRootOfPopulationStandardDeviation_task_order_of_work_tasks_as_created_by_as(self, alias: str, child_request):
        child_request.query.squareRootOfPopulationStandardDeviation("task_order", "squareRootOfPopulationStandardDeviation_task_order")
        self.query.relation_aggregates.append(
            RelationAggregate("work_task_list_as_created_by", alias, child_request.query, True)
        )
        return self
    def sampleVariance_task_order_of_work_tasks_as_created_by(self):
        from requests.work_task_request import WorkTaskRequest
        return self.sampleVariance_task_order_of_work_tasks_as_created_by_as(
            "sampleVariance_task_order_of_work_tasks_as_created_by", WorkTaskRequest())

    def sampleVariance_task_order_of_work_tasks_as_created_by_as(self, alias: str, child_request):
        child_request.query.sampleVariance("task_order", "sampleVariance_task_order")
        self.query.relation_aggregates.append(
            RelationAggregate("work_task_list_as_created_by", alias, child_request.query, True)
        )
        return self
    def samplePopulationVariance_task_order_of_work_tasks_as_created_by(self):
        from requests.work_task_request import WorkTaskRequest
        return self.samplePopulationVariance_task_order_of_work_tasks_as_created_by_as(
            "samplePopulationVariance_task_order_of_work_tasks_as_created_by", WorkTaskRequest())

    def samplePopulationVariance_task_order_of_work_tasks_as_created_by_as(self, alias: str, child_request):
        child_request.query.samplePopulationVariance("task_order", "samplePopulationVariance_task_order")
        self.query.relation_aggregates.append(
            RelationAggregate("work_task_list_as_created_by", alias, child_request.query, True)
        )
        return self
    def count_work_tasks_as_assignee(self):
        return self.count_work_tasks_as_assignee_as("count_work_tasks_as_assignee")

    def count_work_tasks_as_assignee_as(self, alias: str):
        from requests.work_task_request import WorkTaskRequest
        return self.count_work_tasks_as_assignee_with(alias, WorkTaskRequest())

    def count_work_tasks_as_assignee_with(self, alias: str, child_request):
        child_request.query.count_field("id", alias)
        self.query.relation_aggregates.append(
            RelationAggregate("work_task_list_as_assignee", alias, child_request.query, True)
        )
        return self

    def min_deleted_epoch_of_work_tasks_as_assignee(self):
        from requests.work_task_request import WorkTaskRequest
        return self.min_deleted_epoch_of_work_tasks_as_assignee_as(
            "min_deleted_epoch_of_work_tasks_as_assignee", WorkTaskRequest())

    def min_deleted_epoch_of_work_tasks_as_assignee_as(self, alias: str, child_request):
        child_request.query.min("deleted_epoch", "min_deleted_epoch")
        self.query.relation_aggregates.append(
            RelationAggregate("work_task_list_as_assignee", alias, child_request.query, True)
        )
        return self
    def max_deleted_epoch_of_work_tasks_as_assignee(self):
        from requests.work_task_request import WorkTaskRequest
        return self.max_deleted_epoch_of_work_tasks_as_assignee_as(
            "max_deleted_epoch_of_work_tasks_as_assignee", WorkTaskRequest())

    def max_deleted_epoch_of_work_tasks_as_assignee_as(self, alias: str, child_request):
        child_request.query.max("deleted_epoch", "max_deleted_epoch")
        self.query.relation_aggregates.append(
            RelationAggregate("work_task_list_as_assignee", alias, child_request.query, True)
        )
        return self
    def sum_deleted_epoch_of_work_tasks_as_assignee(self):
        from requests.work_task_request import WorkTaskRequest
        return self.sum_deleted_epoch_of_work_tasks_as_assignee_as(
            "sum_deleted_epoch_of_work_tasks_as_assignee", WorkTaskRequest())

    def sum_deleted_epoch_of_work_tasks_as_assignee_as(self, alias: str, child_request):
        child_request.query.sum("deleted_epoch", "sum_deleted_epoch")
        self.query.relation_aggregates.append(
            RelationAggregate("work_task_list_as_assignee", alias, child_request.query, True)
        )
        return self
    def avg_deleted_epoch_of_work_tasks_as_assignee(self):
        from requests.work_task_request import WorkTaskRequest
        return self.avg_deleted_epoch_of_work_tasks_as_assignee_as(
            "avg_deleted_epoch_of_work_tasks_as_assignee", WorkTaskRequest())

    def avg_deleted_epoch_of_work_tasks_as_assignee_as(self, alias: str, child_request):
        child_request.query.avg("deleted_epoch", "avg_deleted_epoch")
        self.query.relation_aggregates.append(
            RelationAggregate("work_task_list_as_assignee", alias, child_request.query, True)
        )
        return self
    def standardDeviation_deleted_epoch_of_work_tasks_as_assignee(self):
        from requests.work_task_request import WorkTaskRequest
        return self.standardDeviation_deleted_epoch_of_work_tasks_as_assignee_as(
            "standardDeviation_deleted_epoch_of_work_tasks_as_assignee", WorkTaskRequest())

    def standardDeviation_deleted_epoch_of_work_tasks_as_assignee_as(self, alias: str, child_request):
        child_request.query.standardDeviation("deleted_epoch", "standardDeviation_deleted_epoch")
        self.query.relation_aggregates.append(
            RelationAggregate("work_task_list_as_assignee", alias, child_request.query, True)
        )
        return self
    def squareRootOfPopulationStandardDeviation_deleted_epoch_of_work_tasks_as_assignee(self):
        from requests.work_task_request import WorkTaskRequest
        return self.squareRootOfPopulationStandardDeviation_deleted_epoch_of_work_tasks_as_assignee_as(
            "squareRootOfPopulationStandardDeviation_deleted_epoch_of_work_tasks_as_assignee", WorkTaskRequest())

    def squareRootOfPopulationStandardDeviation_deleted_epoch_of_work_tasks_as_assignee_as(self, alias: str, child_request):
        child_request.query.squareRootOfPopulationStandardDeviation("deleted_epoch", "squareRootOfPopulationStandardDeviation_deleted_epoch")
        self.query.relation_aggregates.append(
            RelationAggregate("work_task_list_as_assignee", alias, child_request.query, True)
        )
        return self
    def sampleVariance_deleted_epoch_of_work_tasks_as_assignee(self):
        from requests.work_task_request import WorkTaskRequest
        return self.sampleVariance_deleted_epoch_of_work_tasks_as_assignee_as(
            "sampleVariance_deleted_epoch_of_work_tasks_as_assignee", WorkTaskRequest())

    def sampleVariance_deleted_epoch_of_work_tasks_as_assignee_as(self, alias: str, child_request):
        child_request.query.sampleVariance("deleted_epoch", "sampleVariance_deleted_epoch")
        self.query.relation_aggregates.append(
            RelationAggregate("work_task_list_as_assignee", alias, child_request.query, True)
        )
        return self
    def samplePopulationVariance_deleted_epoch_of_work_tasks_as_assignee(self):
        from requests.work_task_request import WorkTaskRequest
        return self.samplePopulationVariance_deleted_epoch_of_work_tasks_as_assignee_as(
            "samplePopulationVariance_deleted_epoch_of_work_tasks_as_assignee", WorkTaskRequest())

    def samplePopulationVariance_deleted_epoch_of_work_tasks_as_assignee_as(self, alias: str, child_request):
        child_request.query.samplePopulationVariance("deleted_epoch", "samplePopulationVariance_deleted_epoch")
        self.query.relation_aggregates.append(
            RelationAggregate("work_task_list_as_assignee", alias, child_request.query, True)
        )
        return self
    def min_task_order_of_work_tasks_as_assignee(self):
        from requests.work_task_request import WorkTaskRequest
        return self.min_task_order_of_work_tasks_as_assignee_as(
            "min_task_order_of_work_tasks_as_assignee", WorkTaskRequest())

    def min_task_order_of_work_tasks_as_assignee_as(self, alias: str, child_request):
        child_request.query.min("task_order", "min_task_order")
        self.query.relation_aggregates.append(
            RelationAggregate("work_task_list_as_assignee", alias, child_request.query, True)
        )
        return self
    def max_task_order_of_work_tasks_as_assignee(self):
        from requests.work_task_request import WorkTaskRequest
        return self.max_task_order_of_work_tasks_as_assignee_as(
            "max_task_order_of_work_tasks_as_assignee", WorkTaskRequest())

    def max_task_order_of_work_tasks_as_assignee_as(self, alias: str, child_request):
        child_request.query.max("task_order", "max_task_order")
        self.query.relation_aggregates.append(
            RelationAggregate("work_task_list_as_assignee", alias, child_request.query, True)
        )
        return self
    def sum_task_order_of_work_tasks_as_assignee(self):
        from requests.work_task_request import WorkTaskRequest
        return self.sum_task_order_of_work_tasks_as_assignee_as(
            "sum_task_order_of_work_tasks_as_assignee", WorkTaskRequest())

    def sum_task_order_of_work_tasks_as_assignee_as(self, alias: str, child_request):
        child_request.query.sum("task_order", "sum_task_order")
        self.query.relation_aggregates.append(
            RelationAggregate("work_task_list_as_assignee", alias, child_request.query, True)
        )
        return self
    def avg_task_order_of_work_tasks_as_assignee(self):
        from requests.work_task_request import WorkTaskRequest
        return self.avg_task_order_of_work_tasks_as_assignee_as(
            "avg_task_order_of_work_tasks_as_assignee", WorkTaskRequest())

    def avg_task_order_of_work_tasks_as_assignee_as(self, alias: str, child_request):
        child_request.query.avg("task_order", "avg_task_order")
        self.query.relation_aggregates.append(
            RelationAggregate("work_task_list_as_assignee", alias, child_request.query, True)
        )
        return self
    def standardDeviation_task_order_of_work_tasks_as_assignee(self):
        from requests.work_task_request import WorkTaskRequest
        return self.standardDeviation_task_order_of_work_tasks_as_assignee_as(
            "standardDeviation_task_order_of_work_tasks_as_assignee", WorkTaskRequest())

    def standardDeviation_task_order_of_work_tasks_as_assignee_as(self, alias: str, child_request):
        child_request.query.standardDeviation("task_order", "standardDeviation_task_order")
        self.query.relation_aggregates.append(
            RelationAggregate("work_task_list_as_assignee", alias, child_request.query, True)
        )
        return self
    def squareRootOfPopulationStandardDeviation_task_order_of_work_tasks_as_assignee(self):
        from requests.work_task_request import WorkTaskRequest
        return self.squareRootOfPopulationStandardDeviation_task_order_of_work_tasks_as_assignee_as(
            "squareRootOfPopulationStandardDeviation_task_order_of_work_tasks_as_assignee", WorkTaskRequest())

    def squareRootOfPopulationStandardDeviation_task_order_of_work_tasks_as_assignee_as(self, alias: str, child_request):
        child_request.query.squareRootOfPopulationStandardDeviation("task_order", "squareRootOfPopulationStandardDeviation_task_order")
        self.query.relation_aggregates.append(
            RelationAggregate("work_task_list_as_assignee", alias, child_request.query, True)
        )
        return self
    def sampleVariance_task_order_of_work_tasks_as_assignee(self):
        from requests.work_task_request import WorkTaskRequest
        return self.sampleVariance_task_order_of_work_tasks_as_assignee_as(
            "sampleVariance_task_order_of_work_tasks_as_assignee", WorkTaskRequest())

    def sampleVariance_task_order_of_work_tasks_as_assignee_as(self, alias: str, child_request):
        child_request.query.sampleVariance("task_order", "sampleVariance_task_order")
        self.query.relation_aggregates.append(
            RelationAggregate("work_task_list_as_assignee", alias, child_request.query, True)
        )
        return self
    def samplePopulationVariance_task_order_of_work_tasks_as_assignee(self):
        from requests.work_task_request import WorkTaskRequest
        return self.samplePopulationVariance_task_order_of_work_tasks_as_assignee_as(
            "samplePopulationVariance_task_order_of_work_tasks_as_assignee", WorkTaskRequest())

    def samplePopulationVariance_task_order_of_work_tasks_as_assignee_as(self, alias: str, child_request):
        child_request.query.samplePopulationVariance("task_order", "samplePopulationVariance_task_order")
        self.query.relation_aggregates.append(
            RelationAggregate("work_task_list_as_assignee", alias, child_request.query, True)
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


    def facet_by_work_space_as(self, name: str, request: QuerySelection,
                                      include_all_facets: bool = True):
        self.query.facet_by(name, "work_space", request.query, include_all_facets)
        return self


class ExecutableWorkAccountRequest:
    def __init__(self, request):
        self._request = request

    def comment(self, c: str):
        self._request.comment(c)
        return self

    def new_entity(self, context) -> WorkAccount:
        request = self._request
        if not request._comment or not request._comment.strip() or not request._purpose or not request._purpose.strip():
            raise ValueError("Security audit failure: non-empty comment() and purpose() are required before new_entity()")
        entity = context.initialize_entity("WorkAccount", WorkAccount._teaql_construct())
        if not isinstance(entity, WorkAccount):
            raise TypeError("entity initializer returned an incompatible WorkAccount")
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

    async def execute_for_list(self, context) -> SmartList[WorkAccount]:
        result = await self.execute_for_result(context)
        query_root = EntityRoot()
        return SmartList(
            (WorkAccount._teaql_construct(_entity_root=query_root, **row) for row in result.rows),
            facets=result.facets)

    async def execute_for_page(self, context, offset: int, limit: int) -> TeaQLPage[WorkAccount]:
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
        data = SmartList(WorkAccount._teaql_construct(_entity_root=query_root, **row) for row in row_result.rows)
        return TeaQLPage(data=data, total_count=total_count, offset=offset, limit=limit)

    async def execute_for_one(self, context):
        request = deepcopy(self._request)
        request.limit(1)
        entities = await ExecutableWorkAccountRequest(request).execute_for_list(context)
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
                yield WorkAccount._teaql_construct(_entity_root=query_root, **row)
