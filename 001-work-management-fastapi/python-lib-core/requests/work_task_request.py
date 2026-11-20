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
from models.work_task import WorkTask
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

class WorkTaskRequest:
    def __init__(self, minimal=False):
        self.query = SelectQuery("WorkTask")
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
        return ExecutableWorkTaskRequest(self)

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
        self.query.project("id", "work_space", "project", "section", "deleted_epoch", "approval", "decision", "repeat_period", "created_by", "primary_detached", "task_order", "task_title", "description", "assignee", "start_date", "due_date", "completed", "version")
        return self

    def select_id(self):
        self.query.project("id")
        return self




    def select_deleted_epoch(self):
        self.query.project("deleted_epoch")
        return self

    def select_approval(self):
        self.query.project("approval")
        return self

    def select_decision(self):
        self.query.project("decision")
        return self

    def select_repeat_period(self):
        self.query.project("repeat_period")
        return self


    def select_primary_detached(self):
        self.query.project("primary_detached")
        return self

    def select_task_order(self):
        self.query.project("task_order")
        return self

    def select_task_title(self):
        self.query.project("task_title")
        return self

    def select_description(self):
        self.query.project("description")
        return self


    def select_start_date(self):
        self.query.project("start_date")
        return self

    def select_due_date(self):
        self.query.project("due_date")
        return self

    def select_completed(self):
        self.query.project("completed")
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
    def select_section_with(self, child_request):
        self.query.project("section")
        self.query.relation_query("section", child_request.query)
        return self
    def select_created_by_with(self, child_request):
        self.query.project("created_by")
        self.query.relation_query("created_by", child_request.query)
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
    def with_section_matching(self, child_request):
        child_request.query.projection = ["id"]
        self.query.and_filter(in_subquery(column("section"), "ProjectSection", child_request.query))
        return self

    def without_section_matching(self, child_request):
        child_request.query.projection = ["id"]
        self.query.and_filter(not_in_subquery(column("section"), "ProjectSection", child_request.query))
        return self

    def have_section(self):
        self.query.and_filter(is_not_null(column("section")))
        return self

    def have_no_section(self):
        self.query.and_filter(is_null(column("section")))
        return self
    def with_created_by_matching(self, child_request):
        child_request.query.projection = ["id"]
        self.query.and_filter(in_subquery(column("created_by"), "WorkAccount", child_request.query))
        return self

    def without_created_by_matching(self, child_request):
        child_request.query.projection = ["id"]
        self.query.and_filter(not_in_subquery(column("created_by"), "WorkAccount", child_request.query))
        return self

    def have_created_by(self):
        self.query.and_filter(is_not_null(column("created_by")))
        return self

    def have_no_created_by(self):
        self.query.and_filter(is_null(column("created_by")))
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

    def filter_by_section(self, val):
        self.query.and_filter(eq("section", val))
        return self

    def with_deleted_epoch_is(self, val):
        self.query.and_filter(eq("deleted_epoch", val))
        return self

    def with_deleted_epoch_is_not(self, val):
        self.query.and_filter(ne("deleted_epoch", val))
        return self

    def with_deleted_epoch_in(self, *vals):
        _set_arguments("with_deleted_epoch_in", vals)
        if not vals:
            self.query.and_filter(is_null(column("id")))
            return self
        self.query.and_filter(in_list("deleted_epoch", list(vals)))
        return self

    def with_deleted_epoch_not_in(self, *vals):
        _set_arguments("with_deleted_epoch_not_in", vals)
        if not vals:
            return self
        self.query.and_filter(not_in_list("deleted_epoch", list(vals)))
        return self

    def with_deleted_epoch_greater_than(self, val):
        self.query.and_filter(gt("deleted_epoch", val))
        return self

    def with_deleted_epoch_greater_than_or_equal_to(self, val):
        self.query.and_filter(gte("deleted_epoch", val))
        return self

    def with_deleted_epoch_less_than(self, val):
        self.query.and_filter(lt("deleted_epoch", val))
        return self

    def with_deleted_epoch_less_than_or_equal_to(self, val):
        self.query.and_filter(lte("deleted_epoch", val))
        return self

    def with_deleted_epoch_between(self, lower, upper):
        self.query.and_filter(between(column("deleted_epoch"), value(lower), value(upper)))
        return self

    def with_deleted_epoch_is_known(self):
        self.query.and_filter(is_not_null(column("deleted_epoch")))
        return self

    def with_deleted_epoch_is_unknown(self):
        self.query.and_filter(is_null(column("deleted_epoch")))
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

    def with_decision_containing(self, val: str):
        self.query.and_filter(contain("decision", val))
        return self

    def with_decision_not_containing(self, val: str):
        self.query.and_filter(not_contain("decision", val))
        return self

    def with_decision_starting_with(self, val: str):
        self.query.and_filter(begin_with("decision", val))
        return self

    def with_decision_not_starting_with(self, val: str):
        self.query.and_filter(not_begin_with("decision", val))
        return self

    def with_decision_ending_with(self, val: str):
        self.query.and_filter(end_with("decision", val))
        return self

    def with_decision_not_ending_with(self, val: str):
        self.query.and_filter(not_end_with("decision", val))
        return self

    def with_decision_sounding_like(self, val: str):
        self.query.and_filter(sound_like("decision", val))
        return self

    def with_decision_is(self, val: str):
        self.query.and_filter(eq("decision", val))
        return self
    def with_decision_is_not(self, val):
        self.query.and_filter(ne("decision", val))
        return self

    def with_decision_in(self, *vals):
        _set_arguments("with_decision_in", vals)
        if not vals:
            self.query.and_filter(is_null(column("id")))
            return self
        self.query.and_filter(in_list("decision", list(vals)))
        return self

    def with_decision_not_in(self, *vals):
        _set_arguments("with_decision_not_in", vals)
        if not vals:
            return self
        self.query.and_filter(not_in_list("decision", list(vals)))
        return self

    def with_decision_greater_than(self, val):
        self.query.and_filter(gt("decision", val))
        return self

    def with_decision_greater_than_or_equal_to(self, val):
        self.query.and_filter(gte("decision", val))
        return self

    def with_decision_less_than(self, val):
        self.query.and_filter(lt("decision", val))
        return self

    def with_decision_less_than_or_equal_to(self, val):
        self.query.and_filter(lte("decision", val))
        return self

    def with_decision_between(self, lower, upper):
        self.query.and_filter(between(column("decision"), value(lower), value(upper)))
        return self

    def with_decision_is_known(self):
        self.query.and_filter(is_not_null(column("decision")))
        return self

    def with_decision_is_unknown(self):
        self.query.and_filter(is_null(column("decision")))
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

    def filter_by_created_by(self, val):
        self.query.and_filter(eq("created_by", val))
        return self

    def which_are_primary_detached(self):
        self.query.and_filter(eq("primary_detached", True))
        return self

    def which_are_not_primary_detached(self):
        self.query.and_filter(eq("primary_detached", False))
        return self
    def with_primary_detached_is_not(self, val):
        self.query.and_filter(ne("primary_detached", val))
        return self

    def with_primary_detached_in(self, *vals):
        _set_arguments("with_primary_detached_in", vals)
        if not vals:
            self.query.and_filter(is_null(column("id")))
            return self
        self.query.and_filter(in_list("primary_detached", list(vals)))
        return self

    def with_primary_detached_not_in(self, *vals):
        _set_arguments("with_primary_detached_not_in", vals)
        if not vals:
            return self
        self.query.and_filter(not_in_list("primary_detached", list(vals)))
        return self

    def with_primary_detached_greater_than(self, val):
        self.query.and_filter(gt("primary_detached", val))
        return self

    def with_primary_detached_greater_than_or_equal_to(self, val):
        self.query.and_filter(gte("primary_detached", val))
        return self

    def with_primary_detached_less_than(self, val):
        self.query.and_filter(lt("primary_detached", val))
        return self

    def with_primary_detached_less_than_or_equal_to(self, val):
        self.query.and_filter(lte("primary_detached", val))
        return self

    def with_primary_detached_between(self, lower, upper):
        self.query.and_filter(between(column("primary_detached"), value(lower), value(upper)))
        return self

    def with_primary_detached_is_known(self):
        self.query.and_filter(is_not_null(column("primary_detached")))
        return self

    def with_primary_detached_is_unknown(self):
        self.query.and_filter(is_null(column("primary_detached")))
        return self

    def with_task_order_is(self, val):
        self.query.and_filter(eq("task_order", val))
        return self

    def with_task_order_is_not(self, val):
        self.query.and_filter(ne("task_order", val))
        return self

    def with_task_order_in(self, *vals):
        _set_arguments("with_task_order_in", vals)
        if not vals:
            self.query.and_filter(is_null(column("id")))
            return self
        self.query.and_filter(in_list("task_order", list(vals)))
        return self

    def with_task_order_not_in(self, *vals):
        _set_arguments("with_task_order_not_in", vals)
        if not vals:
            return self
        self.query.and_filter(not_in_list("task_order", list(vals)))
        return self

    def with_task_order_greater_than(self, val):
        self.query.and_filter(gt("task_order", val))
        return self

    def with_task_order_greater_than_or_equal_to(self, val):
        self.query.and_filter(gte("task_order", val))
        return self

    def with_task_order_less_than(self, val):
        self.query.and_filter(lt("task_order", val))
        return self

    def with_task_order_less_than_or_equal_to(self, val):
        self.query.and_filter(lte("task_order", val))
        return self

    def with_task_order_between(self, lower, upper):
        self.query.and_filter(between(column("task_order"), value(lower), value(upper)))
        return self

    def with_task_order_is_known(self):
        self.query.and_filter(is_not_null(column("task_order")))
        return self

    def with_task_order_is_unknown(self):
        self.query.and_filter(is_null(column("task_order")))
        return self

    def with_task_title_containing(self, val: str):
        self.query.and_filter(contain("task_title", val))
        return self

    def with_task_title_not_containing(self, val: str):
        self.query.and_filter(not_contain("task_title", val))
        return self

    def with_task_title_starting_with(self, val: str):
        self.query.and_filter(begin_with("task_title", val))
        return self

    def with_task_title_not_starting_with(self, val: str):
        self.query.and_filter(not_begin_with("task_title", val))
        return self

    def with_task_title_ending_with(self, val: str):
        self.query.and_filter(end_with("task_title", val))
        return self

    def with_task_title_not_ending_with(self, val: str):
        self.query.and_filter(not_end_with("task_title", val))
        return self

    def with_task_title_sounding_like(self, val: str):
        self.query.and_filter(sound_like("task_title", val))
        return self

    def with_task_title_is(self, val: str):
        self.query.and_filter(eq("task_title", val))
        return self
    def with_task_title_is_not(self, val):
        self.query.and_filter(ne("task_title", val))
        return self

    def with_task_title_in(self, *vals):
        _set_arguments("with_task_title_in", vals)
        if not vals:
            self.query.and_filter(is_null(column("id")))
            return self
        self.query.and_filter(in_list("task_title", list(vals)))
        return self

    def with_task_title_not_in(self, *vals):
        _set_arguments("with_task_title_not_in", vals)
        if not vals:
            return self
        self.query.and_filter(not_in_list("task_title", list(vals)))
        return self

    def with_task_title_greater_than(self, val):
        self.query.and_filter(gt("task_title", val))
        return self

    def with_task_title_greater_than_or_equal_to(self, val):
        self.query.and_filter(gte("task_title", val))
        return self

    def with_task_title_less_than(self, val):
        self.query.and_filter(lt("task_title", val))
        return self

    def with_task_title_less_than_or_equal_to(self, val):
        self.query.and_filter(lte("task_title", val))
        return self

    def with_task_title_between(self, lower, upper):
        self.query.and_filter(between(column("task_title"), value(lower), value(upper)))
        return self

    def with_task_title_is_known(self):
        self.query.and_filter(is_not_null(column("task_title")))
        return self

    def with_task_title_is_unknown(self):
        self.query.and_filter(is_null(column("task_title")))
        return self

    def with_description_containing(self, val: str):
        self.query.and_filter(contain("description", val))
        return self

    def with_description_not_containing(self, val: str):
        self.query.and_filter(not_contain("description", val))
        return self

    def with_description_starting_with(self, val: str):
        self.query.and_filter(begin_with("description", val))
        return self

    def with_description_not_starting_with(self, val: str):
        self.query.and_filter(not_begin_with("description", val))
        return self

    def with_description_ending_with(self, val: str):
        self.query.and_filter(end_with("description", val))
        return self

    def with_description_not_ending_with(self, val: str):
        self.query.and_filter(not_end_with("description", val))
        return self

    def with_description_sounding_like(self, val: str):
        self.query.and_filter(sound_like("description", val))
        return self

    def with_description_is(self, val: str):
        self.query.and_filter(eq("description", val))
        return self
    def with_description_is_not(self, val):
        self.query.and_filter(ne("description", val))
        return self

    def with_description_in(self, *vals):
        _set_arguments("with_description_in", vals)
        if not vals:
            self.query.and_filter(is_null(column("id")))
            return self
        self.query.and_filter(in_list("description", list(vals)))
        return self

    def with_description_not_in(self, *vals):
        _set_arguments("with_description_not_in", vals)
        if not vals:
            return self
        self.query.and_filter(not_in_list("description", list(vals)))
        return self

    def with_description_greater_than(self, val):
        self.query.and_filter(gt("description", val))
        return self

    def with_description_greater_than_or_equal_to(self, val):
        self.query.and_filter(gte("description", val))
        return self

    def with_description_less_than(self, val):
        self.query.and_filter(lt("description", val))
        return self

    def with_description_less_than_or_equal_to(self, val):
        self.query.and_filter(lte("description", val))
        return self

    def with_description_between(self, lower, upper):
        self.query.and_filter(between(column("description"), value(lower), value(upper)))
        return self

    def with_description_is_known(self):
        self.query.and_filter(is_not_null(column("description")))
        return self

    def with_description_is_unknown(self):
        self.query.and_filter(is_null(column("description")))
        return self

    def filter_by_assignee(self, val):
        self.query.and_filter(eq("assignee", val))
        return self

    def with_start_date_is(self, val):
        self.query.and_filter(eq("start_date", val))
        return self

    def with_start_date_is_not(self, val):
        self.query.and_filter(ne("start_date", val))
        return self

    def with_start_date_in(self, *vals):
        _set_arguments("with_start_date_in", vals)
        if not vals:
            self.query.and_filter(is_null(column("id")))
            return self
        self.query.and_filter(in_list("start_date", list(vals)))
        return self

    def with_start_date_not_in(self, *vals):
        _set_arguments("with_start_date_not_in", vals)
        if not vals:
            return self
        self.query.and_filter(not_in_list("start_date", list(vals)))
        return self

    def with_start_date_greater_than(self, val):
        self.query.and_filter(gt("start_date", val))
        return self

    def with_start_date_greater_than_or_equal_to(self, val):
        self.query.and_filter(gte("start_date", val))
        return self

    def with_start_date_less_than(self, val):
        self.query.and_filter(lt("start_date", val))
        return self

    def with_start_date_less_than_or_equal_to(self, val):
        self.query.and_filter(lte("start_date", val))
        return self

    def with_start_date_between(self, lower, upper):
        self.query.and_filter(between(column("start_date"), value(lower), value(upper)))
        return self

    def with_start_date_is_known(self):
        self.query.and_filter(is_not_null(column("start_date")))
        return self

    def with_start_date_is_unknown(self):
        self.query.and_filter(is_null(column("start_date")))
        return self

    def with_due_date_is(self, val):
        self.query.and_filter(eq("due_date", val))
        return self

    def with_due_date_is_not(self, val):
        self.query.and_filter(ne("due_date", val))
        return self

    def with_due_date_in(self, *vals):
        _set_arguments("with_due_date_in", vals)
        if not vals:
            self.query.and_filter(is_null(column("id")))
            return self
        self.query.and_filter(in_list("due_date", list(vals)))
        return self

    def with_due_date_not_in(self, *vals):
        _set_arguments("with_due_date_not_in", vals)
        if not vals:
            return self
        self.query.and_filter(not_in_list("due_date", list(vals)))
        return self

    def with_due_date_greater_than(self, val):
        self.query.and_filter(gt("due_date", val))
        return self

    def with_due_date_greater_than_or_equal_to(self, val):
        self.query.and_filter(gte("due_date", val))
        return self

    def with_due_date_less_than(self, val):
        self.query.and_filter(lt("due_date", val))
        return self

    def with_due_date_less_than_or_equal_to(self, val):
        self.query.and_filter(lte("due_date", val))
        return self

    def with_due_date_between(self, lower, upper):
        self.query.and_filter(between(column("due_date"), value(lower), value(upper)))
        return self

    def with_due_date_is_known(self):
        self.query.and_filter(is_not_null(column("due_date")))
        return self

    def with_due_date_is_unknown(self):
        self.query.and_filter(is_null(column("due_date")))
        return self

    def which_are_completed(self):
        self.query.and_filter(eq("completed", True))
        return self

    def which_are_not_completed(self):
        self.query.and_filter(eq("completed", False))
        return self
    def with_completed_is_not(self, val):
        self.query.and_filter(ne("completed", val))
        return self

    def with_completed_in(self, *vals):
        _set_arguments("with_completed_in", vals)
        if not vals:
            self.query.and_filter(is_null(column("id")))
            return self
        self.query.and_filter(in_list("completed", list(vals)))
        return self

    def with_completed_not_in(self, *vals):
        _set_arguments("with_completed_not_in", vals)
        if not vals:
            return self
        self.query.and_filter(not_in_list("completed", list(vals)))
        return self

    def with_completed_greater_than(self, val):
        self.query.and_filter(gt("completed", val))
        return self

    def with_completed_greater_than_or_equal_to(self, val):
        self.query.and_filter(gte("completed", val))
        return self

    def with_completed_less_than(self, val):
        self.query.and_filter(lt("completed", val))
        return self

    def with_completed_less_than_or_equal_to(self, val):
        self.query.and_filter(lte("completed", val))
        return self

    def with_completed_between(self, lower, upper):
        self.query.and_filter(between(column("completed"), value(lower), value(upper)))
        return self

    def with_completed_is_known(self):
        self.query.and_filter(is_not_null(column("completed")))
        return self

    def with_completed_is_unknown(self):
        self.query.and_filter(is_null(column("completed")))
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




    def order_by_deleted_epoch_ascending(self):
        self.query.order_by("deleted_epoch", "asc")
        return self

    def order_by_deleted_epoch_descending(self):
        self.query.order_by("deleted_epoch", "desc")
        return self

    def order_by_approval_ascending(self):
        self.query.order_by("approval", "asc")
        return self

    def order_by_approval_descending(self):
        self.query.order_by("approval", "desc")
        return self

    def order_by_decision_ascending(self):
        self.query.order_by("decision", "asc")
        return self

    def order_by_decision_descending(self):
        self.query.order_by("decision", "desc")
        return self

    def order_by_repeat_period_ascending(self):
        self.query.order_by("repeat_period", "asc")
        return self

    def order_by_repeat_period_descending(self):
        self.query.order_by("repeat_period", "desc")
        return self


    def order_by_primary_detached_ascending(self):
        self.query.order_by("primary_detached", "asc")
        return self

    def order_by_primary_detached_descending(self):
        self.query.order_by("primary_detached", "desc")
        return self

    def order_by_task_order_ascending(self):
        self.query.order_by("task_order", "asc")
        return self

    def order_by_task_order_descending(self):
        self.query.order_by("task_order", "desc")
        return self

    def order_by_task_title_ascending(self):
        self.query.order_by("task_title", "asc")
        return self

    def order_by_task_title_descending(self):
        self.query.order_by("task_title", "desc")
        return self

    def order_by_description_ascending(self):
        self.query.order_by("description", "asc")
        return self

    def order_by_description_descending(self):
        self.query.order_by("description", "desc")
        return self


    def order_by_start_date_ascending(self):
        self.query.order_by("start_date", "asc")
        return self

    def order_by_start_date_descending(self):
        self.query.order_by("start_date", "desc")
        return self

    def order_by_due_date_ascending(self):
        self.query.order_by("due_date", "asc")
        return self

    def order_by_due_date_descending(self):
        self.query.order_by("due_date", "desc")
        return self

    def order_by_completed_ascending(self):
        self.query.order_by("completed", "asc")
        return self

    def order_by_completed_descending(self):
        self.query.order_by("completed", "desc")
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

    def min_deleted_epoch(self):
        return self.min_deleted_epoch_as("minOfDeletedEpoch")

    def min_deleted_epoch_as(self, ret_name: str):
        self.query.min("deleted_epoch", ret_name)
        return self
    def max_deleted_epoch(self):
        return self.max_deleted_epoch_as("maxOfDeletedEpoch")

    def max_deleted_epoch_as(self, ret_name: str):
        self.query.max("deleted_epoch", ret_name)
        return self
    def sum_deleted_epoch(self):
        return self.sum_deleted_epoch_as("sumOfDeletedEpoch")

    def sum_deleted_epoch_as(self, ret_name: str):
        self.query.sum("deleted_epoch", ret_name)
        return self
    def avg_deleted_epoch(self):
        return self.avg_deleted_epoch_as("avgOfDeletedEpoch")

    def avg_deleted_epoch_as(self, ret_name: str):
        self.query.avg("deleted_epoch", ret_name)
        return self
    def standardDeviation_deleted_epoch(self):
        return self.standardDeviation_deleted_epoch_as("standardDeviationOfDeletedEpoch")

    def standardDeviation_deleted_epoch_as(self, ret_name: str):
        self.query.standardDeviation("deleted_epoch", ret_name)
        return self
    def squareRootOfPopulationStandardDeviation_deleted_epoch(self):
        return self.squareRootOfPopulationStandardDeviation_deleted_epoch_as("squareRootOfPopulationStandardDeviationOfDeletedEpoch")

    def squareRootOfPopulationStandardDeviation_deleted_epoch_as(self, ret_name: str):
        self.query.squareRootOfPopulationStandardDeviation("deleted_epoch", ret_name)
        return self
    def sampleVariance_deleted_epoch(self):
        return self.sampleVariance_deleted_epoch_as("sampleVarianceOfDeletedEpoch")

    def sampleVariance_deleted_epoch_as(self, ret_name: str):
        self.query.sampleVariance("deleted_epoch", ret_name)
        return self
    def samplePopulationVariance_deleted_epoch(self):
        return self.samplePopulationVariance_deleted_epoch_as("samplePopulationVarianceOfDeletedEpoch")

    def samplePopulationVariance_deleted_epoch_as(self, ret_name: str):
        self.query.samplePopulationVariance("deleted_epoch", ret_name)
        return self
    def min_task_order(self):
        return self.min_task_order_as("minOfTaskOrder")

    def min_task_order_as(self, ret_name: str):
        self.query.min("task_order", ret_name)
        return self
    def max_task_order(self):
        return self.max_task_order_as("maxOfTaskOrder")

    def max_task_order_as(self, ret_name: str):
        self.query.max("task_order", ret_name)
        return self
    def sum_task_order(self):
        return self.sum_task_order_as("sumOfTaskOrder")

    def sum_task_order_as(self, ret_name: str):
        self.query.sum("task_order", ret_name)
        return self
    def avg_task_order(self):
        return self.avg_task_order_as("avgOfTaskOrder")

    def avg_task_order_as(self, ret_name: str):
        self.query.avg("task_order", ret_name)
        return self
    def standardDeviation_task_order(self):
        return self.standardDeviation_task_order_as("standardDeviationOfTaskOrder")

    def standardDeviation_task_order_as(self, ret_name: str):
        self.query.standardDeviation("task_order", ret_name)
        return self
    def squareRootOfPopulationStandardDeviation_task_order(self):
        return self.squareRootOfPopulationStandardDeviation_task_order_as("squareRootOfPopulationStandardDeviationOfTaskOrder")

    def squareRootOfPopulationStandardDeviation_task_order_as(self, ret_name: str):
        self.query.squareRootOfPopulationStandardDeviation("task_order", ret_name)
        return self
    def sampleVariance_task_order(self):
        return self.sampleVariance_task_order_as("sampleVarianceOfTaskOrder")

    def sampleVariance_task_order_as(self, ret_name: str):
        self.query.sampleVariance("task_order", ret_name)
        return self
    def samplePopulationVariance_task_order(self):
        return self.samplePopulationVariance_task_order_as("samplePopulationVarianceOfTaskOrder")

    def samplePopulationVariance_task_order_as(self, ret_name: str):
        self.query.samplePopulationVariance("task_order", ret_name)
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
    def group_by_section(self):
        self.query.group_by("section")
        return self

    def group_by_section_as(self, ret_name: str):
        self.query.group_by("section")
        return self
    def group_by_deleted_epoch(self):
        self.query.group_by("deleted_epoch")
        return self

    def group_by_deleted_epoch_as(self, ret_name: str):
        self.query.group_by("deleted_epoch")
        return self
    def group_by_approval(self):
        self.query.group_by("approval")
        return self

    def group_by_approval_as(self, ret_name: str):
        self.query.group_by("approval")
        return self
    def group_by_decision(self):
        self.query.group_by("decision")
        return self

    def group_by_decision_as(self, ret_name: str):
        self.query.group_by("decision")
        return self
    def group_by_repeat_period(self):
        self.query.group_by("repeat_period")
        return self

    def group_by_repeat_period_as(self, ret_name: str):
        self.query.group_by("repeat_period")
        return self
    def group_by_created_by(self):
        self.query.group_by("created_by")
        return self

    def group_by_created_by_as(self, ret_name: str):
        self.query.group_by("created_by")
        return self
    def group_by_primary_detached(self):
        self.query.group_by("primary_detached")
        return self

    def group_by_primary_detached_as(self, ret_name: str):
        self.query.group_by("primary_detached")
        return self
    def group_by_task_order(self):
        self.query.group_by("task_order")
        return self

    def group_by_task_order_as(self, ret_name: str):
        self.query.group_by("task_order")
        return self
    def group_by_task_title(self):
        self.query.group_by("task_title")
        return self

    def group_by_task_title_as(self, ret_name: str):
        self.query.group_by("task_title")
        return self
    def group_by_description(self):
        self.query.group_by("description")
        return self

    def group_by_description_as(self, ret_name: str):
        self.query.group_by("description")
        return self
    def group_by_assignee(self):
        self.query.group_by("assignee")
        return self

    def group_by_assignee_as(self, ret_name: str):
        self.query.group_by("assignee")
        return self
    def group_by_start_date(self):
        self.query.group_by("start_date")
        return self

    def group_by_start_date_as(self, ret_name: str):
        self.query.group_by("start_date")
        return self
    def group_by_due_date(self):
        self.query.group_by("due_date")
        return self

    def group_by_due_date_as(self, ret_name: str):
        self.query.group_by("due_date")
        return self
    def group_by_completed(self):
        self.query.group_by("completed")
        return self

    def group_by_completed_as(self, ret_name: str):
        self.query.group_by("completed")
        return self
    def group_by_version(self):
        self.query.group_by("version")
        return self

    def group_by_version_as(self, ret_name: str):
        self.query.group_by("version")
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
    def select_task_dependency_list_as_dependent(self):
        from requests.task_dependency_request import TaskDependencyRequest
        return self.select_task_dependency_list_as_dependent_with(TaskDependencyRequest())

    def select_task_dependency_list_as_dependent_with(self, child_request):
        self.query.relation_query("task_dependency_list_as_dependent", child_request.query)
        return self
    def select_task_dependency_list_as_blocker(self):
        from requests.task_dependency_request import TaskDependencyRequest
        return self.select_task_dependency_list_as_blocker_with(TaskDependencyRequest())

    def select_task_dependency_list_as_blocker_with(self, child_request):
        self.query.relation_query("task_dependency_list_as_blocker", child_request.query)
        return self
    def select_task_placement_list(self):
        from requests.task_placement_request import TaskPlacementRequest
        return self.select_task_placement_list_with(TaskPlacementRequest())

    def select_task_placement_list_with(self, child_request):
        self.query.relation_query("task_placement_list", child_request.query)
        return self
    def select_recurrence_link_list_as_source_task(self):
        from requests.recurrence_link_request import RecurrenceLinkRequest
        return self.select_recurrence_link_list_as_source_task_with(RecurrenceLinkRequest())

    def select_recurrence_link_list_as_source_task_with(self, child_request):
        self.query.relation_query("recurrence_link_list_as_source_task", child_request.query)
        return self
    def select_recurrence_link_list_as_next_task(self):
        from requests.recurrence_link_request import RecurrenceLinkRequest
        return self.select_recurrence_link_list_as_next_task_with(RecurrenceLinkRequest())

    def select_recurrence_link_list_as_next_task_with(self, child_request):
        self.query.relation_query("recurrence_link_list_as_next_task", child_request.query)
        return self
    def select_task_event_list_as_task(self):
        from requests.task_event_request import TaskEventRequest
        return self.select_task_event_list_as_task_with(TaskEventRequest())

    def select_task_event_list_as_task_with(self, child_request):
        self.query.relation_query("task_event_list_as_task", child_request.query)
        return self
    def select_task_event_list_as_related_task(self):
        from requests.task_event_request import TaskEventRequest
        return self.select_task_event_list_as_related_task_with(TaskEventRequest())

    def select_task_event_list_as_related_task_with(self, child_request):
        self.query.relation_query("task_event_list_as_related_task", child_request.query)
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
    def select_inbox_notice_list(self):
        from requests.inbox_notice_request import InboxNoticeRequest
        return self.select_inbox_notice_list_with(InboxNoticeRequest())

    def select_inbox_notice_list_with(self, child_request):
        self.query.relation_query("inbox_notice_list", child_request.query)
        return self
    def have_task_field_choices(self):
        from requests.task_field_choice_request import TaskFieldChoiceRequest
        return self.with_task_field_choice_list_matching(TaskFieldChoiceRequest())

    def have_no_task_field_choices(self):
        from requests.task_field_choice_request import TaskFieldChoiceRequest
        return self.without_task_field_choice_list_matching(TaskFieldChoiceRequest())

    def with_task_field_choice_list_matching(self, child_request):
        child_request.query.projection = ["task"]
        self.query.and_filter(in_subquery(column("id"), "TaskFieldChoice", child_request.query))
        return self

    def without_task_field_choice_list_matching(self, child_request):
        child_request.query.projection = ["task"]
        self.query.and_filter(not_in_subquery(column("id"), "TaskFieldChoice", child_request.query))
        return self
    def have_work_subtasks(self):
        from requests.work_subtask_request import WorkSubtaskRequest
        return self.with_work_subtask_list_matching(WorkSubtaskRequest())

    def have_no_work_subtasks(self):
        from requests.work_subtask_request import WorkSubtaskRequest
        return self.without_work_subtask_list_matching(WorkSubtaskRequest())

    def with_work_subtask_list_matching(self, child_request):
        child_request.query.projection = ["task"]
        self.query.and_filter(in_subquery(column("id"), "WorkSubtask", child_request.query))
        return self

    def without_work_subtask_list_matching(self, child_request):
        child_request.query.projection = ["task"]
        self.query.and_filter(not_in_subquery(column("id"), "WorkSubtask", child_request.query))
        return self
    def have_task_comments(self):
        from requests.task_comment_request import TaskCommentRequest
        return self.with_task_comment_list_matching(TaskCommentRequest())

    def have_no_task_comments(self):
        from requests.task_comment_request import TaskCommentRequest
        return self.without_task_comment_list_matching(TaskCommentRequest())

    def with_task_comment_list_matching(self, child_request):
        child_request.query.projection = ["task"]
        self.query.and_filter(in_subquery(column("id"), "TaskComment", child_request.query))
        return self

    def without_task_comment_list_matching(self, child_request):
        child_request.query.projection = ["task"]
        self.query.and_filter(not_in_subquery(column("id"), "TaskComment", child_request.query))
        return self
    def have_task_dependencies_as_dependent(self):
        from requests.task_dependency_request import TaskDependencyRequest
        return self.with_task_dependency_list_as_dependent_matching(TaskDependencyRequest())

    def have_no_task_dependencies_as_dependent(self):
        from requests.task_dependency_request import TaskDependencyRequest
        return self.without_task_dependency_list_as_dependent_matching(TaskDependencyRequest())

    def with_task_dependency_list_as_dependent_matching(self, child_request):
        child_request.query.projection = ["dependent"]
        self.query.and_filter(in_subquery(column("id"), "TaskDependency", child_request.query))
        return self

    def without_task_dependency_list_as_dependent_matching(self, child_request):
        child_request.query.projection = ["dependent"]
        self.query.and_filter(not_in_subquery(column("id"), "TaskDependency", child_request.query))
        return self
    def have_task_dependencies_as_blocker(self):
        from requests.task_dependency_request import TaskDependencyRequest
        return self.with_task_dependency_list_as_blocker_matching(TaskDependencyRequest())

    def have_no_task_dependencies_as_blocker(self):
        from requests.task_dependency_request import TaskDependencyRequest
        return self.without_task_dependency_list_as_blocker_matching(TaskDependencyRequest())

    def with_task_dependency_list_as_blocker_matching(self, child_request):
        child_request.query.projection = ["blocker"]
        self.query.and_filter(in_subquery(column("id"), "TaskDependency", child_request.query))
        return self

    def without_task_dependency_list_as_blocker_matching(self, child_request):
        child_request.query.projection = ["blocker"]
        self.query.and_filter(not_in_subquery(column("id"), "TaskDependency", child_request.query))
        return self
    def have_task_placements(self):
        from requests.task_placement_request import TaskPlacementRequest
        return self.with_task_placement_list_matching(TaskPlacementRequest())

    def have_no_task_placements(self):
        from requests.task_placement_request import TaskPlacementRequest
        return self.without_task_placement_list_matching(TaskPlacementRequest())

    def with_task_placement_list_matching(self, child_request):
        child_request.query.projection = ["task"]
        self.query.and_filter(in_subquery(column("id"), "TaskPlacement", child_request.query))
        return self

    def without_task_placement_list_matching(self, child_request):
        child_request.query.projection = ["task"]
        self.query.and_filter(not_in_subquery(column("id"), "TaskPlacement", child_request.query))
        return self
    def have_recurrence_links_as_source_task(self):
        from requests.recurrence_link_request import RecurrenceLinkRequest
        return self.with_recurrence_link_list_as_source_task_matching(RecurrenceLinkRequest())

    def have_no_recurrence_links_as_source_task(self):
        from requests.recurrence_link_request import RecurrenceLinkRequest
        return self.without_recurrence_link_list_as_source_task_matching(RecurrenceLinkRequest())

    def with_recurrence_link_list_as_source_task_matching(self, child_request):
        child_request.query.projection = ["source_task"]
        self.query.and_filter(in_subquery(column("id"), "RecurrenceLink", child_request.query))
        return self

    def without_recurrence_link_list_as_source_task_matching(self, child_request):
        child_request.query.projection = ["source_task"]
        self.query.and_filter(not_in_subquery(column("id"), "RecurrenceLink", child_request.query))
        return self
    def have_recurrence_links_as_next_task(self):
        from requests.recurrence_link_request import RecurrenceLinkRequest
        return self.with_recurrence_link_list_as_next_task_matching(RecurrenceLinkRequest())

    def have_no_recurrence_links_as_next_task(self):
        from requests.recurrence_link_request import RecurrenceLinkRequest
        return self.without_recurrence_link_list_as_next_task_matching(RecurrenceLinkRequest())

    def with_recurrence_link_list_as_next_task_matching(self, child_request):
        child_request.query.projection = ["next_task"]
        self.query.and_filter(in_subquery(column("id"), "RecurrenceLink", child_request.query))
        return self

    def without_recurrence_link_list_as_next_task_matching(self, child_request):
        child_request.query.projection = ["next_task"]
        self.query.and_filter(not_in_subquery(column("id"), "RecurrenceLink", child_request.query))
        return self
    def have_task_events_as_task(self):
        from requests.task_event_request import TaskEventRequest
        return self.with_task_event_list_as_task_matching(TaskEventRequest())

    def have_no_task_events_as_task(self):
        from requests.task_event_request import TaskEventRequest
        return self.without_task_event_list_as_task_matching(TaskEventRequest())

    def with_task_event_list_as_task_matching(self, child_request):
        child_request.query.projection = ["task"]
        self.query.and_filter(in_subquery(column("id"), "TaskEvent", child_request.query))
        return self

    def without_task_event_list_as_task_matching(self, child_request):
        child_request.query.projection = ["task"]
        self.query.and_filter(not_in_subquery(column("id"), "TaskEvent", child_request.query))
        return self
    def have_task_events_as_related_task(self):
        from requests.task_event_request import TaskEventRequest
        return self.with_task_event_list_as_related_task_matching(TaskEventRequest())

    def have_no_task_events_as_related_task(self):
        from requests.task_event_request import TaskEventRequest
        return self.without_task_event_list_as_related_task_matching(TaskEventRequest())

    def with_task_event_list_as_related_task_matching(self, child_request):
        child_request.query.projection = ["related_task"]
        self.query.and_filter(in_subquery(column("id"), "TaskEvent", child_request.query))
        return self

    def without_task_event_list_as_related_task_matching(self, child_request):
        child_request.query.projection = ["related_task"]
        self.query.and_filter(not_in_subquery(column("id"), "TaskEvent", child_request.query))
        return self
    def have_task_participants(self):
        from requests.task_participant_request import TaskParticipantRequest
        return self.with_task_participant_list_matching(TaskParticipantRequest())

    def have_no_task_participants(self):
        from requests.task_participant_request import TaskParticipantRequest
        return self.without_task_participant_list_matching(TaskParticipantRequest())

    def with_task_participant_list_matching(self, child_request):
        child_request.query.projection = ["task"]
        self.query.and_filter(in_subquery(column("id"), "TaskParticipant", child_request.query))
        return self

    def without_task_participant_list_matching(self, child_request):
        child_request.query.projection = ["task"]
        self.query.and_filter(not_in_subquery(column("id"), "TaskParticipant", child_request.query))
        return self
    def have_deleted_task_viewers(self):
        from requests.deleted_task_viewer_request import DeletedTaskViewerRequest
        return self.with_deleted_task_viewer_list_matching(DeletedTaskViewerRequest())

    def have_no_deleted_task_viewers(self):
        from requests.deleted_task_viewer_request import DeletedTaskViewerRequest
        return self.without_deleted_task_viewer_list_matching(DeletedTaskViewerRequest())

    def with_deleted_task_viewer_list_matching(self, child_request):
        child_request.query.projection = ["task"]
        self.query.and_filter(in_subquery(column("id"), "DeletedTaskViewer", child_request.query))
        return self

    def without_deleted_task_viewer_list_matching(self, child_request):
        child_request.query.projection = ["task"]
        self.query.and_filter(not_in_subquery(column("id"), "DeletedTaskViewer", child_request.query))
        return self
    def have_inbox_notices(self):
        from requests.inbox_notice_request import InboxNoticeRequest
        return self.with_inbox_notice_list_matching(InboxNoticeRequest())

    def have_no_inbox_notices(self):
        from requests.inbox_notice_request import InboxNoticeRequest
        return self.without_inbox_notice_list_matching(InboxNoticeRequest())

    def with_inbox_notice_list_matching(self, child_request):
        child_request.query.projection = ["task"]
        self.query.and_filter(in_subquery(column("id"), "InboxNotice", child_request.query))
        return self

    def without_inbox_notice_list_matching(self, child_request):
        child_request.query.projection = ["task"]
        self.query.and_filter(not_in_subquery(column("id"), "InboxNotice", child_request.query))
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


    def count_task_dependencies_as_dependent(self):
        return self.count_task_dependencies_as_dependent_as("count_task_dependencies_as_dependent")

    def count_task_dependencies_as_dependent_as(self, alias: str):
        from requests.task_dependency_request import TaskDependencyRequest
        return self.count_task_dependencies_as_dependent_with(alias, TaskDependencyRequest())

    def count_task_dependencies_as_dependent_with(self, alias: str, child_request):
        child_request.query.count_field("id", alias)
        self.query.relation_aggregates.append(
            RelationAggregate("task_dependency_list_as_dependent", alias, child_request.query, True)
        )
        return self


    def count_task_dependencies_as_blocker(self):
        return self.count_task_dependencies_as_blocker_as("count_task_dependencies_as_blocker")

    def count_task_dependencies_as_blocker_as(self, alias: str):
        from requests.task_dependency_request import TaskDependencyRequest
        return self.count_task_dependencies_as_blocker_with(alias, TaskDependencyRequest())

    def count_task_dependencies_as_blocker_with(self, alias: str, child_request):
        child_request.query.count_field("id", alias)
        self.query.relation_aggregates.append(
            RelationAggregate("task_dependency_list_as_blocker", alias, child_request.query, True)
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
    def count_recurrence_links_as_source_task(self):
        return self.count_recurrence_links_as_source_task_as("count_recurrence_links_as_source_task")

    def count_recurrence_links_as_source_task_as(self, alias: str):
        from requests.recurrence_link_request import RecurrenceLinkRequest
        return self.count_recurrence_links_as_source_task_with(alias, RecurrenceLinkRequest())

    def count_recurrence_links_as_source_task_with(self, alias: str, child_request):
        child_request.query.count_field("id", alias)
        self.query.relation_aggregates.append(
            RelationAggregate("recurrence_link_list_as_source_task", alias, child_request.query, True)
        )
        return self


    def count_recurrence_links_as_next_task(self):
        return self.count_recurrence_links_as_next_task_as("count_recurrence_links_as_next_task")

    def count_recurrence_links_as_next_task_as(self, alias: str):
        from requests.recurrence_link_request import RecurrenceLinkRequest
        return self.count_recurrence_links_as_next_task_with(alias, RecurrenceLinkRequest())

    def count_recurrence_links_as_next_task_with(self, alias: str, child_request):
        child_request.query.count_field("id", alias)
        self.query.relation_aggregates.append(
            RelationAggregate("recurrence_link_list_as_next_task", alias, child_request.query, True)
        )
        return self


    def count_task_events_as_task(self):
        return self.count_task_events_as_task_as("count_task_events_as_task")

    def count_task_events_as_task_as(self, alias: str):
        from requests.task_event_request import TaskEventRequest
        return self.count_task_events_as_task_with(alias, TaskEventRequest())

    def count_task_events_as_task_with(self, alias: str, child_request):
        child_request.query.count_field("id", alias)
        self.query.relation_aggregates.append(
            RelationAggregate("task_event_list_as_task", alias, child_request.query, True)
        )
        return self


    def count_task_events_as_related_task(self):
        return self.count_task_events_as_related_task_as("count_task_events_as_related_task")

    def count_task_events_as_related_task_as(self, alias: str):
        from requests.task_event_request import TaskEventRequest
        return self.count_task_events_as_related_task_with(alias, TaskEventRequest())

    def count_task_events_as_related_task_with(self, alias: str, child_request):
        child_request.query.count_field("id", alias)
        self.query.relation_aggregates.append(
            RelationAggregate("task_event_list_as_related_task", alias, child_request.query, True)
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

    def facet_by_project_as(self, name: str, request: QuerySelection,
                                      include_all_facets: bool = True):
        self.query.facet_by(name, "project", request.query, include_all_facets)
        return self

    def facet_by_section_as(self, name: str, request: QuerySelection,
                                      include_all_facets: bool = True):
        self.query.facet_by(name, "section", request.query, include_all_facets)
        return self

    def facet_by_created_by_as(self, name: str, request: QuerySelection,
                                      include_all_facets: bool = True):
        self.query.facet_by(name, "created_by", request.query, include_all_facets)
        return self

    def facet_by_assignee_as(self, name: str, request: QuerySelection,
                                      include_all_facets: bool = True):
        self.query.facet_by(name, "assignee", request.query, include_all_facets)
        return self


class ExecutableWorkTaskRequest:
    def __init__(self, request):
        self._request = request

    def comment(self, c: str):
        self._request.comment(c)
        return self

    def new_entity(self, context) -> WorkTask:
        request = self._request
        if not request._comment or not request._comment.strip() or not request._purpose or not request._purpose.strip():
            raise ValueError("Security audit failure: non-empty comment() and purpose() are required before new_entity()")
        entity = context.initialize_entity("WorkTask", WorkTask._teaql_construct())
        if not isinstance(entity, WorkTask):
            raise TypeError("entity initializer returned an incompatible WorkTask")
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

    async def execute_for_list(self, context) -> SmartList[WorkTask]:
        result = await self.execute_for_result(context)
        query_root = EntityRoot()
        return SmartList(
            (WorkTask._teaql_construct(_entity_root=query_root, **row) for row in result.rows),
            facets=result.facets)

    async def execute_for_page(self, context, offset: int, limit: int) -> TeaQLPage[WorkTask]:
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
        data = SmartList(WorkTask._teaql_construct(_entity_root=query_root, **row) for row in row_result.rows)
        return TeaQLPage(data=data, total_count=total_count, offset=offset, limit=limit)

    async def execute_for_one(self, context):
        request = deepcopy(self._request)
        request.limit(1)
        entities = await ExecutableWorkTaskRequest(request).execute_for_list(context)
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
                yield WorkTask._teaql_construct(_entity_root=query_root, **row)
