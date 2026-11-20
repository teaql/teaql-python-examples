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
from models.task_blueprint import TaskBlueprint
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

class TaskBlueprintRequest:
    def __init__(self, minimal=False):
        self.query = SelectQuery("TaskBlueprint")
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
        return ExecutableTaskBlueprintRequest(self)

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
        self.query.project("id", "work_space", "project", "template_name", "initial_title", "initial_description", "assignee", "due_offset", "repeat_period", "approval", "version")
        return self

    def select_id(self):
        self.query.project("id")
        return self



    def select_template_name(self):
        self.query.project("template_name")
        return self

    def select_initial_title(self):
        self.query.project("initial_title")
        return self

    def select_initial_description(self):
        self.query.project("initial_description")
        return self


    def select_due_offset(self):
        self.query.project("due_offset")
        return self

    def select_repeat_period(self):
        self.query.project("repeat_period")
        return self

    def select_approval(self):
        self.query.project("approval")
        return self

    def select_version(self):
        self.query.project("version")
        return self

    def select_work_space_with(self, child_request):
        self.query.project("work_space")
        self.query.relation_query("work_space", child_request.query)
        return self
    def select_project_with(self, child_request):
        self.query.project("project")
        self.query.relation_query("project", child_request.query)
        return self
    def select_assignee_with(self, child_request):
        self.query.project("assignee")
        self.query.relation_query("assignee", child_request.query)
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
    def with_project_matching(self, child_request):
        child_request.query.projection = ["id"]
        self.query.and_filter(in_subquery(column("project"), "WorkProject", child_request.query))
        return self

    def without_project_matching(self, child_request):
        child_request.query.projection = ["id"]
        self.query.and_filter(not_in_subquery(column("project"), "WorkProject", child_request.query))
        return self

    def have_project(self):
        self.query.and_filter(is_not_null(column("project")))
        return self

    def have_no_project(self):
        self.query.and_filter(is_null(column("project")))
        return self
    def with_assignee_matching(self, child_request):
        child_request.query.projection = ["id"]
        self.query.and_filter(in_subquery(column("assignee"), "WorkAccount", child_request.query))
        return self

    def without_assignee_matching(self, child_request):
        child_request.query.projection = ["id"]
        self.query.and_filter(not_in_subquery(column("assignee"), "WorkAccount", child_request.query))
        return self

    def have_assignee(self):
        self.query.and_filter(is_not_null(column("assignee")))
        return self

    def have_no_assignee(self):
        self.query.and_filter(is_null(column("assignee")))
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

    def filter_by_work_space(self, val):
        self.query.and_filter(eq("work_space", val))
        return self

    def filter_by_project(self, val):
        self.query.and_filter(eq("project", val))
        return self

    def with_template_name_containing(self, val: str):
        self.query.and_filter(contain("template_name", val))
        return self

    def with_template_name_not_containing(self, val: str):
        self.query.and_filter(not_contain("template_name", val))
        return self

    def with_template_name_starting_with(self, val: str):
        self.query.and_filter(begin_with("template_name", val))
        return self

    def with_template_name_not_starting_with(self, val: str):
        self.query.and_filter(not_begin_with("template_name", val))
        return self

    def with_template_name_ending_with(self, val: str):
        self.query.and_filter(end_with("template_name", val))
        return self

    def with_template_name_not_ending_with(self, val: str):
        self.query.and_filter(not_end_with("template_name", val))
        return self

    def with_template_name_sounding_like(self, val: str):
        self.query.and_filter(sound_like("template_name", val))
        return self

    def with_template_name_is(self, val: str):
        self.query.and_filter(eq("template_name", val))
        return self
    def with_template_name_is_not(self, val):
        self.query.and_filter(ne("template_name", val))
        return self

    def with_template_name_in(self, *vals):
        _set_arguments("with_template_name_in", vals)
        if not vals:
            self.query.and_filter(is_null(column("id")))
            return self
        self.query.and_filter(in_list("template_name", list(vals)))
        return self

    def with_template_name_not_in(self, *vals):
        _set_arguments("with_template_name_not_in", vals)
        if not vals:
            return self
        self.query.and_filter(not_in_list("template_name", list(vals)))
        return self

    def with_template_name_greater_than(self, val):
        self.query.and_filter(gt("template_name", val))
        return self

    def with_template_name_greater_than_or_equal_to(self, val):
        self.query.and_filter(gte("template_name", val))
        return self

    def with_template_name_less_than(self, val):
        self.query.and_filter(lt("template_name", val))
        return self

    def with_template_name_less_than_or_equal_to(self, val):
        self.query.and_filter(lte("template_name", val))
        return self

    def with_template_name_between(self, lower, upper):
        self.query.and_filter(between(column("template_name"), value(lower), value(upper)))
        return self

    def with_template_name_is_known(self):
        self.query.and_filter(is_not_null(column("template_name")))
        return self

    def with_template_name_is_unknown(self):
        self.query.and_filter(is_null(column("template_name")))
        return self

    def with_initial_title_containing(self, val: str):
        self.query.and_filter(contain("initial_title", val))
        return self

    def with_initial_title_not_containing(self, val: str):
        self.query.and_filter(not_contain("initial_title", val))
        return self

    def with_initial_title_starting_with(self, val: str):
        self.query.and_filter(begin_with("initial_title", val))
        return self

    def with_initial_title_not_starting_with(self, val: str):
        self.query.and_filter(not_begin_with("initial_title", val))
        return self

    def with_initial_title_ending_with(self, val: str):
        self.query.and_filter(end_with("initial_title", val))
        return self

    def with_initial_title_not_ending_with(self, val: str):
        self.query.and_filter(not_end_with("initial_title", val))
        return self

    def with_initial_title_sounding_like(self, val: str):
        self.query.and_filter(sound_like("initial_title", val))
        return self

    def with_initial_title_is(self, val: str):
        self.query.and_filter(eq("initial_title", val))
        return self
    def with_initial_title_is_not(self, val):
        self.query.and_filter(ne("initial_title", val))
        return self

    def with_initial_title_in(self, *vals):
        _set_arguments("with_initial_title_in", vals)
        if not vals:
            self.query.and_filter(is_null(column("id")))
            return self
        self.query.and_filter(in_list("initial_title", list(vals)))
        return self

    def with_initial_title_not_in(self, *vals):
        _set_arguments("with_initial_title_not_in", vals)
        if not vals:
            return self
        self.query.and_filter(not_in_list("initial_title", list(vals)))
        return self

    def with_initial_title_greater_than(self, val):
        self.query.and_filter(gt("initial_title", val))
        return self

    def with_initial_title_greater_than_or_equal_to(self, val):
        self.query.and_filter(gte("initial_title", val))
        return self

    def with_initial_title_less_than(self, val):
        self.query.and_filter(lt("initial_title", val))
        return self

    def with_initial_title_less_than_or_equal_to(self, val):
        self.query.and_filter(lte("initial_title", val))
        return self

    def with_initial_title_between(self, lower, upper):
        self.query.and_filter(between(column("initial_title"), value(lower), value(upper)))
        return self

    def with_initial_title_is_known(self):
        self.query.and_filter(is_not_null(column("initial_title")))
        return self

    def with_initial_title_is_unknown(self):
        self.query.and_filter(is_null(column("initial_title")))
        return self

    def with_initial_description_containing(self, val: str):
        self.query.and_filter(contain("initial_description", val))
        return self

    def with_initial_description_not_containing(self, val: str):
        self.query.and_filter(not_contain("initial_description", val))
        return self

    def with_initial_description_starting_with(self, val: str):
        self.query.and_filter(begin_with("initial_description", val))
        return self

    def with_initial_description_not_starting_with(self, val: str):
        self.query.and_filter(not_begin_with("initial_description", val))
        return self

    def with_initial_description_ending_with(self, val: str):
        self.query.and_filter(end_with("initial_description", val))
        return self

    def with_initial_description_not_ending_with(self, val: str):
        self.query.and_filter(not_end_with("initial_description", val))
        return self

    def with_initial_description_sounding_like(self, val: str):
        self.query.and_filter(sound_like("initial_description", val))
        return self

    def with_initial_description_is(self, val: str):
        self.query.and_filter(eq("initial_description", val))
        return self
    def with_initial_description_is_not(self, val):
        self.query.and_filter(ne("initial_description", val))
        return self

    def with_initial_description_in(self, *vals):
        _set_arguments("with_initial_description_in", vals)
        if not vals:
            self.query.and_filter(is_null(column("id")))
            return self
        self.query.and_filter(in_list("initial_description", list(vals)))
        return self

    def with_initial_description_not_in(self, *vals):
        _set_arguments("with_initial_description_not_in", vals)
        if not vals:
            return self
        self.query.and_filter(not_in_list("initial_description", list(vals)))
        return self

    def with_initial_description_greater_than(self, val):
        self.query.and_filter(gt("initial_description", val))
        return self

    def with_initial_description_greater_than_or_equal_to(self, val):
        self.query.and_filter(gte("initial_description", val))
        return self

    def with_initial_description_less_than(self, val):
        self.query.and_filter(lt("initial_description", val))
        return self

    def with_initial_description_less_than_or_equal_to(self, val):
        self.query.and_filter(lte("initial_description", val))
        return self

    def with_initial_description_between(self, lower, upper):
        self.query.and_filter(between(column("initial_description"), value(lower), value(upper)))
        return self

    def with_initial_description_is_known(self):
        self.query.and_filter(is_not_null(column("initial_description")))
        return self

    def with_initial_description_is_unknown(self):
        self.query.and_filter(is_null(column("initial_description")))
        return self

    def filter_by_assignee(self, val):
        self.query.and_filter(eq("assignee", val))
        return self

    def with_due_offset_is(self, val):
        self.query.and_filter(eq("due_offset", val))
        return self

    def with_due_offset_is_not(self, val):
        self.query.and_filter(ne("due_offset", val))
        return self

    def with_due_offset_in(self, *vals):
        _set_arguments("with_due_offset_in", vals)
        if not vals:
            self.query.and_filter(is_null(column("id")))
            return self
        self.query.and_filter(in_list("due_offset", list(vals)))
        return self

    def with_due_offset_not_in(self, *vals):
        _set_arguments("with_due_offset_not_in", vals)
        if not vals:
            return self
        self.query.and_filter(not_in_list("due_offset", list(vals)))
        return self

    def with_due_offset_greater_than(self, val):
        self.query.and_filter(gt("due_offset", val))
        return self

    def with_due_offset_greater_than_or_equal_to(self, val):
        self.query.and_filter(gte("due_offset", val))
        return self

    def with_due_offset_less_than(self, val):
        self.query.and_filter(lt("due_offset", val))
        return self

    def with_due_offset_less_than_or_equal_to(self, val):
        self.query.and_filter(lte("due_offset", val))
        return self

    def with_due_offset_between(self, lower, upper):
        self.query.and_filter(between(column("due_offset"), value(lower), value(upper)))
        return self

    def with_due_offset_is_known(self):
        self.query.and_filter(is_not_null(column("due_offset")))
        return self

    def with_due_offset_is_unknown(self):
        self.query.and_filter(is_null(column("due_offset")))
        return self

    def with_repeat_period_containing(self, val: str):
        self.query.and_filter(contain("repeat_period", val))
        return self

    def with_repeat_period_not_containing(self, val: str):
        self.query.and_filter(not_contain("repeat_period", val))
        return self

    def with_repeat_period_starting_with(self, val: str):
        self.query.and_filter(begin_with("repeat_period", val))
        return self

    def with_repeat_period_not_starting_with(self, val: str):
        self.query.and_filter(not_begin_with("repeat_period", val))
        return self

    def with_repeat_period_ending_with(self, val: str):
        self.query.and_filter(end_with("repeat_period", val))
        return self

    def with_repeat_period_not_ending_with(self, val: str):
        self.query.and_filter(not_end_with("repeat_period", val))
        return self

    def with_repeat_period_sounding_like(self, val: str):
        self.query.and_filter(sound_like("repeat_period", val))
        return self

    def with_repeat_period_is(self, val: str):
        self.query.and_filter(eq("repeat_period", val))
        return self
    def with_repeat_period_is_not(self, val):
        self.query.and_filter(ne("repeat_period", val))
        return self

    def with_repeat_period_in(self, *vals):
        _set_arguments("with_repeat_period_in", vals)
        if not vals:
            self.query.and_filter(is_null(column("id")))
            return self
        self.query.and_filter(in_list("repeat_period", list(vals)))
        return self

    def with_repeat_period_not_in(self, *vals):
        _set_arguments("with_repeat_period_not_in", vals)
        if not vals:
            return self
        self.query.and_filter(not_in_list("repeat_period", list(vals)))
        return self

    def with_repeat_period_greater_than(self, val):
        self.query.and_filter(gt("repeat_period", val))
        return self

    def with_repeat_period_greater_than_or_equal_to(self, val):
        self.query.and_filter(gte("repeat_period", val))
        return self

    def with_repeat_period_less_than(self, val):
        self.query.and_filter(lt("repeat_period", val))
        return self

    def with_repeat_period_less_than_or_equal_to(self, val):
        self.query.and_filter(lte("repeat_period", val))
        return self

    def with_repeat_period_between(self, lower, upper):
        self.query.and_filter(between(column("repeat_period"), value(lower), value(upper)))
        return self

    def with_repeat_period_is_known(self):
        self.query.and_filter(is_not_null(column("repeat_period")))
        return self

    def with_repeat_period_is_unknown(self):
        self.query.and_filter(is_null(column("repeat_period")))
        return self

    def which_are_approval(self):
        self.query.and_filter(eq("approval", True))
        return self

    def which_are_not_approval(self):
        self.query.and_filter(eq("approval", False))
        return self
    def with_approval_is_not(self, val):
        self.query.and_filter(ne("approval", val))
        return self

    def with_approval_in(self, *vals):
        _set_arguments("with_approval_in", vals)
        if not vals:
            self.query.and_filter(is_null(column("id")))
            return self
        self.query.and_filter(in_list("approval", list(vals)))
        return self

    def with_approval_not_in(self, *vals):
        _set_arguments("with_approval_not_in", vals)
        if not vals:
            return self
        self.query.and_filter(not_in_list("approval", list(vals)))
        return self

    def with_approval_greater_than(self, val):
        self.query.and_filter(gt("approval", val))
        return self

    def with_approval_greater_than_or_equal_to(self, val):
        self.query.and_filter(gte("approval", val))
        return self

    def with_approval_less_than(self, val):
        self.query.and_filter(lt("approval", val))
        return self

    def with_approval_less_than_or_equal_to(self, val):
        self.query.and_filter(lte("approval", val))
        return self

    def with_approval_between(self, lower, upper):
        self.query.and_filter(between(column("approval"), value(lower), value(upper)))
        return self

    def with_approval_is_known(self):
        self.query.and_filter(is_not_null(column("approval")))
        return self

    def with_approval_is_unknown(self):
        self.query.and_filter(is_null(column("approval")))
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



    def order_by_template_name_ascending(self):
        self.query.order_by("template_name", "asc")
        return self

    def order_by_template_name_descending(self):
        self.query.order_by("template_name", "desc")
        return self

    def order_by_initial_title_ascending(self):
        self.query.order_by("initial_title", "asc")
        return self

    def order_by_initial_title_descending(self):
        self.query.order_by("initial_title", "desc")
        return self

    def order_by_initial_description_ascending(self):
        self.query.order_by("initial_description", "asc")
        return self

    def order_by_initial_description_descending(self):
        self.query.order_by("initial_description", "desc")
        return self


    def order_by_due_offset_ascending(self):
        self.query.order_by("due_offset", "asc")
        return self

    def order_by_due_offset_descending(self):
        self.query.order_by("due_offset", "desc")
        return self

    def order_by_repeat_period_ascending(self):
        self.query.order_by("repeat_period", "asc")
        return self

    def order_by_repeat_period_descending(self):
        self.query.order_by("repeat_period", "desc")
        return self

    def order_by_approval_ascending(self):
        self.query.order_by("approval", "asc")
        return self

    def order_by_approval_descending(self):
        self.query.order_by("approval", "desc")
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

    def min_due_offset(self):
        return self.min_due_offset_as("minOfDueOffset")

    def min_due_offset_as(self, ret_name: str):
        self.query.min("due_offset", ret_name)
        return self
    def max_due_offset(self):
        return self.max_due_offset_as("maxOfDueOffset")

    def max_due_offset_as(self, ret_name: str):
        self.query.max("due_offset", ret_name)
        return self
    def sum_due_offset(self):
        return self.sum_due_offset_as("sumOfDueOffset")

    def sum_due_offset_as(self, ret_name: str):
        self.query.sum("due_offset", ret_name)
        return self
    def avg_due_offset(self):
        return self.avg_due_offset_as("avgOfDueOffset")

    def avg_due_offset_as(self, ret_name: str):
        self.query.avg("due_offset", ret_name)
        return self
    def standardDeviation_due_offset(self):
        return self.standardDeviation_due_offset_as("standardDeviationOfDueOffset")

    def standardDeviation_due_offset_as(self, ret_name: str):
        self.query.standardDeviation("due_offset", ret_name)
        return self
    def squareRootOfPopulationStandardDeviation_due_offset(self):
        return self.squareRootOfPopulationStandardDeviation_due_offset_as("squareRootOfPopulationStandardDeviationOfDueOffset")

    def squareRootOfPopulationStandardDeviation_due_offset_as(self, ret_name: str):
        self.query.squareRootOfPopulationStandardDeviation("due_offset", ret_name)
        return self
    def sampleVariance_due_offset(self):
        return self.sampleVariance_due_offset_as("sampleVarianceOfDueOffset")

    def sampleVariance_due_offset_as(self, ret_name: str):
        self.query.sampleVariance("due_offset", ret_name)
        return self
    def samplePopulationVariance_due_offset(self):
        return self.samplePopulationVariance_due_offset_as("samplePopulationVarianceOfDueOffset")

    def samplePopulationVariance_due_offset_as(self, ret_name: str):
        self.query.samplePopulationVariance("due_offset", ret_name)
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
    def group_by_project(self):
        self.query.group_by("project")
        return self

    def group_by_project_as(self, ret_name: str):
        self.query.group_by("project")
        return self
    def group_by_template_name(self):
        self.query.group_by("template_name")
        return self

    def group_by_template_name_as(self, ret_name: str):
        self.query.group_by("template_name")
        return self
    def group_by_initial_title(self):
        self.query.group_by("initial_title")
        return self

    def group_by_initial_title_as(self, ret_name: str):
        self.query.group_by("initial_title")
        return self
    def group_by_initial_description(self):
        self.query.group_by("initial_description")
        return self

    def group_by_initial_description_as(self, ret_name: str):
        self.query.group_by("initial_description")
        return self
    def group_by_assignee(self):
        self.query.group_by("assignee")
        return self

    def group_by_assignee_as(self, ret_name: str):
        self.query.group_by("assignee")
        return self
    def group_by_due_offset(self):
        self.query.group_by("due_offset")
        return self

    def group_by_due_offset_as(self, ret_name: str):
        self.query.group_by("due_offset")
        return self
    def group_by_repeat_period(self):
        self.query.group_by("repeat_period")
        return self

    def group_by_repeat_period_as(self, ret_name: str):
        self.query.group_by("repeat_period")
        return self
    def group_by_approval(self):
        self.query.group_by("approval")
        return self

    def group_by_approval_as(self, ret_name: str):
        self.query.group_by("approval")
        return self
    def group_by_version(self):
        self.query.group_by("version")
        return self

    def group_by_version_as(self, ret_name: str):
        self.query.group_by("version")
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
    def have_blueprint_choices(self):
        from requests.blueprint_choice_request import BlueprintChoiceRequest
        return self.with_blueprint_choice_list_matching(BlueprintChoiceRequest())

    def have_no_blueprint_choices(self):
        from requests.blueprint_choice_request import BlueprintChoiceRequest
        return self.without_blueprint_choice_list_matching(BlueprintChoiceRequest())

    def with_blueprint_choice_list_matching(self, child_request):
        child_request.query.projection = ["blueprint"]
        self.query.and_filter(in_subquery(column("id"), "BlueprintChoice", child_request.query))
        return self

    def without_blueprint_choice_list_matching(self, child_request):
        child_request.query.projection = ["blueprint"]
        self.query.and_filter(not_in_subquery(column("id"), "BlueprintChoice", child_request.query))
        return self
    def have_blueprint_subtasks(self):
        from requests.blueprint_subtask_request import BlueprintSubtaskRequest
        return self.with_blueprint_subtask_list_matching(BlueprintSubtaskRequest())

    def have_no_blueprint_subtasks(self):
        from requests.blueprint_subtask_request import BlueprintSubtaskRequest
        return self.without_blueprint_subtask_list_matching(BlueprintSubtaskRequest())

    def with_blueprint_subtask_list_matching(self, child_request):
        child_request.query.projection = ["blueprint"]
        self.query.and_filter(in_subquery(column("id"), "BlueprintSubtask", child_request.query))
        return self

    def without_blueprint_subtask_list_matching(self, child_request):
        child_request.query.projection = ["blueprint"]
        self.query.and_filter(not_in_subquery(column("id"), "BlueprintSubtask", child_request.query))
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
    def facet_by_work_space_as(self, name: str, request: QuerySelection,
                                      include_all_facets: bool = True):
        self.query.facet_by(name, "work_space", request.query, include_all_facets)
        return self

    def facet_by_project_as(self, name: str, request: QuerySelection,
                                      include_all_facets: bool = True):
        self.query.facet_by(name, "project", request.query, include_all_facets)
        return self

    def facet_by_assignee_as(self, name: str, request: QuerySelection,
                                      include_all_facets: bool = True):
        self.query.facet_by(name, "assignee", request.query, include_all_facets)
        return self


class ExecutableTaskBlueprintRequest:
    def __init__(self, request):
        self._request = request

    def comment(self, c: str):
        self._request.comment(c)
        return self

    def new_entity(self, context) -> TaskBlueprint:
        request = self._request
        if not request._comment or not request._comment.strip() or not request._purpose or not request._purpose.strip():
            raise ValueError("Security audit failure: non-empty comment() and purpose() are required before new_entity()")
        entity = context.initialize_entity("TaskBlueprint", TaskBlueprint._teaql_construct())
        if not isinstance(entity, TaskBlueprint):
            raise TypeError("entity initializer returned an incompatible TaskBlueprint")
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

    async def execute_for_list(self, context) -> SmartList[TaskBlueprint]:
        result = await self.execute_for_result(context)
        query_root = EntityRoot()
        return SmartList(
            (TaskBlueprint._teaql_construct(_entity_root=query_root, **row) for row in result.rows),
            facets=result.facets)

    async def execute_for_page(self, context, offset: int, limit: int) -> TeaQLPage[TaskBlueprint]:
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
        data = SmartList(TaskBlueprint._teaql_construct(_entity_root=query_root, **row) for row in row_result.rows)
        return TeaQLPage(data=data, total_count=total_count, offset=offset, limit=limit)

    async def execute_for_one(self, context):
        request = deepcopy(self._request)
        request.limit(1)
        entities = await ExecutableTaskBlueprintRequest(request).execute_for_list(context)
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
                yield TaskBlueprint._teaql_construct(_entity_root=query_root, **row)
