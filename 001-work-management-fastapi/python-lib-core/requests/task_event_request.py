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
from models.task_event import TaskEvent
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

class TaskEventRequest:
    def __init__(self, minimal=False):
        self.query = SelectQuery("TaskEvent")
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
        return ExecutableTaskEventRequest(self)

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
        self.query.project("id", "work_space", "task", "actor", "scope_project", "related_task", "event_kind", "field_label", "old_value", "new_value", "event_time", "version")
        return self

    def select_id(self):
        self.query.project("id")
        return self






    def select_event_kind(self):
        self.query.project("event_kind")
        return self

    def select_field_label(self):
        self.query.project("field_label")
        return self

    def select_old_value(self):
        self.query.project("old_value")
        return self

    def select_new_value(self):
        self.query.project("new_value")
        return self

    def select_event_time(self):
        self.query.project("event_time")
        return self

    def select_version(self):
        self.query.project("version")
        return self

    def select_work_space_with(self, child_request):
        self.query.project("work_space")
        self.query.relation_query("work_space", child_request.query)
        return self
    def select_task_with(self, child_request):
        self.query.project("task")
        self.query.relation_query("task", child_request.query)
        return self
    def select_actor_with(self, child_request):
        self.query.project("actor")
        self.query.relation_query("actor", child_request.query)
        return self
    def select_scope_project_with(self, child_request):
        self.query.project("scope_project")
        self.query.relation_query("scope_project", child_request.query)
        return self
    def select_related_task_with(self, child_request):
        self.query.project("related_task")
        self.query.relation_query("related_task", child_request.query)
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
    def with_task_matching(self, child_request):
        child_request.query.projection = ["id"]
        self.query.and_filter(in_subquery(column("task"), "WorkTask", child_request.query))
        return self

    def without_task_matching(self, child_request):
        child_request.query.projection = ["id"]
        self.query.and_filter(not_in_subquery(column("task"), "WorkTask", child_request.query))
        return self

    def have_task(self):
        self.query.and_filter(is_not_null(column("task")))
        return self

    def have_no_task(self):
        self.query.and_filter(is_null(column("task")))
        return self
    def with_actor_matching(self, child_request):
        child_request.query.projection = ["id"]
        self.query.and_filter(in_subquery(column("actor"), "WorkAccount", child_request.query))
        return self

    def without_actor_matching(self, child_request):
        child_request.query.projection = ["id"]
        self.query.and_filter(not_in_subquery(column("actor"), "WorkAccount", child_request.query))
        return self

    def have_actor(self):
        self.query.and_filter(is_not_null(column("actor")))
        return self

    def have_no_actor(self):
        self.query.and_filter(is_null(column("actor")))
        return self
    def with_scope_project_matching(self, child_request):
        child_request.query.projection = ["id"]
        self.query.and_filter(in_subquery(column("scope_project"), "WorkProject", child_request.query))
        return self

    def without_scope_project_matching(self, child_request):
        child_request.query.projection = ["id"]
        self.query.and_filter(not_in_subquery(column("scope_project"), "WorkProject", child_request.query))
        return self

    def have_scope_project(self):
        self.query.and_filter(is_not_null(column("scope_project")))
        return self

    def have_no_scope_project(self):
        self.query.and_filter(is_null(column("scope_project")))
        return self
    def with_related_task_matching(self, child_request):
        child_request.query.projection = ["id"]
        self.query.and_filter(in_subquery(column("related_task"), "WorkTask", child_request.query))
        return self

    def without_related_task_matching(self, child_request):
        child_request.query.projection = ["id"]
        self.query.and_filter(not_in_subquery(column("related_task"), "WorkTask", child_request.query))
        return self

    def have_related_task(self):
        self.query.and_filter(is_not_null(column("related_task")))
        return self

    def have_no_related_task(self):
        self.query.and_filter(is_null(column("related_task")))
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

    def filter_by_task(self, val):
        self.query.and_filter(eq("task", val))
        return self

    def filter_by_actor(self, val):
        self.query.and_filter(eq("actor", val))
        return self

    def filter_by_scope_project(self, val):
        self.query.and_filter(eq("scope_project", val))
        return self

    def filter_by_related_task(self, val):
        self.query.and_filter(eq("related_task", val))
        return self

    def with_event_kind_containing(self, val: str):
        self.query.and_filter(contain("event_kind", val))
        return self

    def with_event_kind_not_containing(self, val: str):
        self.query.and_filter(not_contain("event_kind", val))
        return self

    def with_event_kind_starting_with(self, val: str):
        self.query.and_filter(begin_with("event_kind", val))
        return self

    def with_event_kind_not_starting_with(self, val: str):
        self.query.and_filter(not_begin_with("event_kind", val))
        return self

    def with_event_kind_ending_with(self, val: str):
        self.query.and_filter(end_with("event_kind", val))
        return self

    def with_event_kind_not_ending_with(self, val: str):
        self.query.and_filter(not_end_with("event_kind", val))
        return self

    def with_event_kind_sounding_like(self, val: str):
        self.query.and_filter(sound_like("event_kind", val))
        return self

    def with_event_kind_is(self, val: str):
        self.query.and_filter(eq("event_kind", val))
        return self
    def with_event_kind_is_not(self, val):
        self.query.and_filter(ne("event_kind", val))
        return self

    def with_event_kind_in(self, *vals):
        _set_arguments("with_event_kind_in", vals)
        if not vals:
            self.query.and_filter(is_null(column("id")))
            return self
        self.query.and_filter(in_list("event_kind", list(vals)))
        return self

    def with_event_kind_not_in(self, *vals):
        _set_arguments("with_event_kind_not_in", vals)
        if not vals:
            return self
        self.query.and_filter(not_in_list("event_kind", list(vals)))
        return self

    def with_event_kind_greater_than(self, val):
        self.query.and_filter(gt("event_kind", val))
        return self

    def with_event_kind_greater_than_or_equal_to(self, val):
        self.query.and_filter(gte("event_kind", val))
        return self

    def with_event_kind_less_than(self, val):
        self.query.and_filter(lt("event_kind", val))
        return self

    def with_event_kind_less_than_or_equal_to(self, val):
        self.query.and_filter(lte("event_kind", val))
        return self

    def with_event_kind_between(self, lower, upper):
        self.query.and_filter(between(column("event_kind"), value(lower), value(upper)))
        return self

    def with_event_kind_is_known(self):
        self.query.and_filter(is_not_null(column("event_kind")))
        return self

    def with_event_kind_is_unknown(self):
        self.query.and_filter(is_null(column("event_kind")))
        return self

    def with_field_label_containing(self, val: str):
        self.query.and_filter(contain("field_label", val))
        return self

    def with_field_label_not_containing(self, val: str):
        self.query.and_filter(not_contain("field_label", val))
        return self

    def with_field_label_starting_with(self, val: str):
        self.query.and_filter(begin_with("field_label", val))
        return self

    def with_field_label_not_starting_with(self, val: str):
        self.query.and_filter(not_begin_with("field_label", val))
        return self

    def with_field_label_ending_with(self, val: str):
        self.query.and_filter(end_with("field_label", val))
        return self

    def with_field_label_not_ending_with(self, val: str):
        self.query.and_filter(not_end_with("field_label", val))
        return self

    def with_field_label_sounding_like(self, val: str):
        self.query.and_filter(sound_like("field_label", val))
        return self

    def with_field_label_is(self, val: str):
        self.query.and_filter(eq("field_label", val))
        return self
    def with_field_label_is_not(self, val):
        self.query.and_filter(ne("field_label", val))
        return self

    def with_field_label_in(self, *vals):
        _set_arguments("with_field_label_in", vals)
        if not vals:
            self.query.and_filter(is_null(column("id")))
            return self
        self.query.and_filter(in_list("field_label", list(vals)))
        return self

    def with_field_label_not_in(self, *vals):
        _set_arguments("with_field_label_not_in", vals)
        if not vals:
            return self
        self.query.and_filter(not_in_list("field_label", list(vals)))
        return self

    def with_field_label_greater_than(self, val):
        self.query.and_filter(gt("field_label", val))
        return self

    def with_field_label_greater_than_or_equal_to(self, val):
        self.query.and_filter(gte("field_label", val))
        return self

    def with_field_label_less_than(self, val):
        self.query.and_filter(lt("field_label", val))
        return self

    def with_field_label_less_than_or_equal_to(self, val):
        self.query.and_filter(lte("field_label", val))
        return self

    def with_field_label_between(self, lower, upper):
        self.query.and_filter(between(column("field_label"), value(lower), value(upper)))
        return self

    def with_field_label_is_known(self):
        self.query.and_filter(is_not_null(column("field_label")))
        return self

    def with_field_label_is_unknown(self):
        self.query.and_filter(is_null(column("field_label")))
        return self

    def with_old_value_containing(self, val: str):
        self.query.and_filter(contain("old_value", val))
        return self

    def with_old_value_not_containing(self, val: str):
        self.query.and_filter(not_contain("old_value", val))
        return self

    def with_old_value_starting_with(self, val: str):
        self.query.and_filter(begin_with("old_value", val))
        return self

    def with_old_value_not_starting_with(self, val: str):
        self.query.and_filter(not_begin_with("old_value", val))
        return self

    def with_old_value_ending_with(self, val: str):
        self.query.and_filter(end_with("old_value", val))
        return self

    def with_old_value_not_ending_with(self, val: str):
        self.query.and_filter(not_end_with("old_value", val))
        return self

    def with_old_value_sounding_like(self, val: str):
        self.query.and_filter(sound_like("old_value", val))
        return self

    def with_old_value_is(self, val: str):
        self.query.and_filter(eq("old_value", val))
        return self
    def with_old_value_is_not(self, val):
        self.query.and_filter(ne("old_value", val))
        return self

    def with_old_value_in(self, *vals):
        _set_arguments("with_old_value_in", vals)
        if not vals:
            self.query.and_filter(is_null(column("id")))
            return self
        self.query.and_filter(in_list("old_value", list(vals)))
        return self

    def with_old_value_not_in(self, *vals):
        _set_arguments("with_old_value_not_in", vals)
        if not vals:
            return self
        self.query.and_filter(not_in_list("old_value", list(vals)))
        return self

    def with_old_value_greater_than(self, val):
        self.query.and_filter(gt("old_value", val))
        return self

    def with_old_value_greater_than_or_equal_to(self, val):
        self.query.and_filter(gte("old_value", val))
        return self

    def with_old_value_less_than(self, val):
        self.query.and_filter(lt("old_value", val))
        return self

    def with_old_value_less_than_or_equal_to(self, val):
        self.query.and_filter(lte("old_value", val))
        return self

    def with_old_value_between(self, lower, upper):
        self.query.and_filter(between(column("old_value"), value(lower), value(upper)))
        return self

    def with_old_value_is_known(self):
        self.query.and_filter(is_not_null(column("old_value")))
        return self

    def with_old_value_is_unknown(self):
        self.query.and_filter(is_null(column("old_value")))
        return self

    def with_new_value_containing(self, val: str):
        self.query.and_filter(contain("new_value", val))
        return self

    def with_new_value_not_containing(self, val: str):
        self.query.and_filter(not_contain("new_value", val))
        return self

    def with_new_value_starting_with(self, val: str):
        self.query.and_filter(begin_with("new_value", val))
        return self

    def with_new_value_not_starting_with(self, val: str):
        self.query.and_filter(not_begin_with("new_value", val))
        return self

    def with_new_value_ending_with(self, val: str):
        self.query.and_filter(end_with("new_value", val))
        return self

    def with_new_value_not_ending_with(self, val: str):
        self.query.and_filter(not_end_with("new_value", val))
        return self

    def with_new_value_sounding_like(self, val: str):
        self.query.and_filter(sound_like("new_value", val))
        return self

    def with_new_value_is(self, val: str):
        self.query.and_filter(eq("new_value", val))
        return self
    def with_new_value_is_not(self, val):
        self.query.and_filter(ne("new_value", val))
        return self

    def with_new_value_in(self, *vals):
        _set_arguments("with_new_value_in", vals)
        if not vals:
            self.query.and_filter(is_null(column("id")))
            return self
        self.query.and_filter(in_list("new_value", list(vals)))
        return self

    def with_new_value_not_in(self, *vals):
        _set_arguments("with_new_value_not_in", vals)
        if not vals:
            return self
        self.query.and_filter(not_in_list("new_value", list(vals)))
        return self

    def with_new_value_greater_than(self, val):
        self.query.and_filter(gt("new_value", val))
        return self

    def with_new_value_greater_than_or_equal_to(self, val):
        self.query.and_filter(gte("new_value", val))
        return self

    def with_new_value_less_than(self, val):
        self.query.and_filter(lt("new_value", val))
        return self

    def with_new_value_less_than_or_equal_to(self, val):
        self.query.and_filter(lte("new_value", val))
        return self

    def with_new_value_between(self, lower, upper):
        self.query.and_filter(between(column("new_value"), value(lower), value(upper)))
        return self

    def with_new_value_is_known(self):
        self.query.and_filter(is_not_null(column("new_value")))
        return self

    def with_new_value_is_unknown(self):
        self.query.and_filter(is_null(column("new_value")))
        return self

    def with_event_time_is(self, val):
        self.query.and_filter(eq("event_time", val))
        return self

    def with_event_time_is_not(self, val):
        self.query.and_filter(ne("event_time", val))
        return self

    def with_event_time_in(self, *vals):
        _set_arguments("with_event_time_in", vals)
        if not vals:
            self.query.and_filter(is_null(column("id")))
            return self
        self.query.and_filter(in_list("event_time", list(vals)))
        return self

    def with_event_time_not_in(self, *vals):
        _set_arguments("with_event_time_not_in", vals)
        if not vals:
            return self
        self.query.and_filter(not_in_list("event_time", list(vals)))
        return self

    def with_event_time_greater_than(self, val):
        self.query.and_filter(gt("event_time", val))
        return self

    def with_event_time_greater_than_or_equal_to(self, val):
        self.query.and_filter(gte("event_time", val))
        return self

    def with_event_time_less_than(self, val):
        self.query.and_filter(lt("event_time", val))
        return self

    def with_event_time_less_than_or_equal_to(self, val):
        self.query.and_filter(lte("event_time", val))
        return self

    def with_event_time_between(self, lower, upper):
        self.query.and_filter(between(column("event_time"), value(lower), value(upper)))
        return self

    def with_event_time_is_known(self):
        self.query.and_filter(is_not_null(column("event_time")))
        return self

    def with_event_time_is_unknown(self):
        self.query.and_filter(is_null(column("event_time")))
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






    def order_by_event_kind_ascending(self):
        self.query.order_by("event_kind", "asc")
        return self

    def order_by_event_kind_descending(self):
        self.query.order_by("event_kind", "desc")
        return self

    def order_by_field_label_ascending(self):
        self.query.order_by("field_label", "asc")
        return self

    def order_by_field_label_descending(self):
        self.query.order_by("field_label", "desc")
        return self

    def order_by_old_value_ascending(self):
        self.query.order_by("old_value", "asc")
        return self

    def order_by_old_value_descending(self):
        self.query.order_by("old_value", "desc")
        return self

    def order_by_new_value_ascending(self):
        self.query.order_by("new_value", "asc")
        return self

    def order_by_new_value_descending(self):
        self.query.order_by("new_value", "desc")
        return self

    def order_by_event_time_ascending(self):
        self.query.order_by("event_time", "asc")
        return self

    def order_by_event_time_descending(self):
        self.query.order_by("event_time", "desc")
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
    def group_by_task(self):
        self.query.group_by("task")
        return self

    def group_by_task_as(self, ret_name: str):
        self.query.group_by("task")
        return self
    def group_by_actor(self):
        self.query.group_by("actor")
        return self

    def group_by_actor_as(self, ret_name: str):
        self.query.group_by("actor")
        return self
    def group_by_scope_project(self):
        self.query.group_by("scope_project")
        return self

    def group_by_scope_project_as(self, ret_name: str):
        self.query.group_by("scope_project")
        return self
    def group_by_related_task(self):
        self.query.group_by("related_task")
        return self

    def group_by_related_task_as(self, ret_name: str):
        self.query.group_by("related_task")
        return self
    def group_by_event_kind(self):
        self.query.group_by("event_kind")
        return self

    def group_by_event_kind_as(self, ret_name: str):
        self.query.group_by("event_kind")
        return self
    def group_by_field_label(self):
        self.query.group_by("field_label")
        return self

    def group_by_field_label_as(self, ret_name: str):
        self.query.group_by("field_label")
        return self
    def group_by_old_value(self):
        self.query.group_by("old_value")
        return self

    def group_by_old_value_as(self, ret_name: str):
        self.query.group_by("old_value")
        return self
    def group_by_new_value(self):
        self.query.group_by("new_value")
        return self

    def group_by_new_value_as(self, ret_name: str):
        self.query.group_by("new_value")
        return self
    def group_by_event_time(self):
        self.query.group_by("event_time")
        return self

    def group_by_event_time_as(self, ret_name: str):
        self.query.group_by("event_time")
        return self
    def group_by_version(self):
        self.query.group_by("version")
        return self

    def group_by_version_as(self, ret_name: str):
        self.query.group_by("version")
        return self
    def select_inbox_notice_list(self):
        from requests.inbox_notice_request import InboxNoticeRequest
        return self.select_inbox_notice_list_with(InboxNoticeRequest())

    def select_inbox_notice_list_with(self, child_request):
        self.query.relation_query("inbox_notice_list", child_request.query)
        return self
    def have_inbox_notices(self):
        from requests.inbox_notice_request import InboxNoticeRequest
        return self.with_inbox_notice_list_matching(InboxNoticeRequest())

    def have_no_inbox_notices(self):
        from requests.inbox_notice_request import InboxNoticeRequest
        return self.without_inbox_notice_list_matching(InboxNoticeRequest())

    def with_inbox_notice_list_matching(self, child_request):
        child_request.query.projection = ["event"]
        self.query.and_filter(in_subquery(column("id"), "InboxNotice", child_request.query))
        return self

    def without_inbox_notice_list_matching(self, child_request):
        child_request.query.projection = ["event"]
        self.query.and_filter(not_in_subquery(column("id"), "InboxNotice", child_request.query))
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

    def facet_by_task_as(self, name: str, request: QuerySelection,
                                      include_all_facets: bool = True):
        self.query.facet_by(name, "task", request.query, include_all_facets)
        return self

    def facet_by_actor_as(self, name: str, request: QuerySelection,
                                      include_all_facets: bool = True):
        self.query.facet_by(name, "actor", request.query, include_all_facets)
        return self

    def facet_by_scope_project_as(self, name: str, request: QuerySelection,
                                      include_all_facets: bool = True):
        self.query.facet_by(name, "scope_project", request.query, include_all_facets)
        return self

    def facet_by_related_task_as(self, name: str, request: QuerySelection,
                                      include_all_facets: bool = True):
        self.query.facet_by(name, "related_task", request.query, include_all_facets)
        return self


class ExecutableTaskEventRequest:
    def __init__(self, request):
        self._request = request

    def comment(self, c: str):
        self._request.comment(c)
        return self

    def new_entity(self, context) -> TaskEvent:
        request = self._request
        if not request._comment or not request._comment.strip() or not request._purpose or not request._purpose.strip():
            raise ValueError("Security audit failure: non-empty comment() and purpose() are required before new_entity()")
        entity = context.initialize_entity("TaskEvent", TaskEvent._teaql_construct())
        if not isinstance(entity, TaskEvent):
            raise TypeError("entity initializer returned an incompatible TaskEvent")
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

    async def execute_for_list(self, context) -> SmartList[TaskEvent]:
        result = await self.execute_for_result(context)
        query_root = EntityRoot()
        return SmartList(
            (TaskEvent._teaql_construct(_entity_root=query_root, **row) for row in result.rows),
            facets=result.facets)

    async def execute_for_page(self, context, offset: int, limit: int) -> TeaQLPage[TaskEvent]:
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
        data = SmartList(TaskEvent._teaql_construct(_entity_root=query_root, **row) for row in row_result.rows)
        return TeaQLPage(data=data, total_count=total_count, offset=offset, limit=limit)

    async def execute_for_one(self, context):
        request = deepcopy(self._request)
        request.limit(1)
        entities = await ExecutableTaskEventRequest(request).execute_for_list(context)
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
                yield TaskEvent._teaql_construct(_entity_root=query_root, **row)
