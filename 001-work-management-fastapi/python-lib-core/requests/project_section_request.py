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
from models.project_section import ProjectSection
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

class ProjectSectionRequest:
    def __init__(self, minimal=False):
        self.query = SelectQuery("ProjectSection")
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
        return ExecutableProjectSectionRequest(self)

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
        self.query.project("id", "work_space", "project", "section_name", "section_order", "default_section", "version")
        return self

    def select_id(self):
        self.query.project("id")
        return self



    def select_section_name(self):
        self.query.project("section_name")
        return self

    def select_section_order(self):
        self.query.project("section_order")
        return self

    def select_default_section(self):
        self.query.project("default_section")
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

    def with_section_name_containing(self, val: str):
        self.query.and_filter(contain("section_name", val))
        return self

    def with_section_name_not_containing(self, val: str):
        self.query.and_filter(not_contain("section_name", val))
        return self

    def with_section_name_starting_with(self, val: str):
        self.query.and_filter(begin_with("section_name", val))
        return self

    def with_section_name_not_starting_with(self, val: str):
        self.query.and_filter(not_begin_with("section_name", val))
        return self

    def with_section_name_ending_with(self, val: str):
        self.query.and_filter(end_with("section_name", val))
        return self

    def with_section_name_not_ending_with(self, val: str):
        self.query.and_filter(not_end_with("section_name", val))
        return self

    def with_section_name_sounding_like(self, val: str):
        self.query.and_filter(sound_like("section_name", val))
        return self

    def with_section_name_is(self, val: str):
        self.query.and_filter(eq("section_name", val))
        return self
    def with_section_name_is_not(self, val):
        self.query.and_filter(ne("section_name", val))
        return self

    def with_section_name_in(self, *vals):
        _set_arguments("with_section_name_in", vals)
        if not vals:
            self.query.and_filter(is_null(column("id")))
            return self
        self.query.and_filter(in_list("section_name", list(vals)))
        return self

    def with_section_name_not_in(self, *vals):
        _set_arguments("with_section_name_not_in", vals)
        if not vals:
            return self
        self.query.and_filter(not_in_list("section_name", list(vals)))
        return self

    def with_section_name_greater_than(self, val):
        self.query.and_filter(gt("section_name", val))
        return self

    def with_section_name_greater_than_or_equal_to(self, val):
        self.query.and_filter(gte("section_name", val))
        return self

    def with_section_name_less_than(self, val):
        self.query.and_filter(lt("section_name", val))
        return self

    def with_section_name_less_than_or_equal_to(self, val):
        self.query.and_filter(lte("section_name", val))
        return self

    def with_section_name_between(self, lower, upper):
        self.query.and_filter(between(column("section_name"), value(lower), value(upper)))
        return self

    def with_section_name_is_known(self):
        self.query.and_filter(is_not_null(column("section_name")))
        return self

    def with_section_name_is_unknown(self):
        self.query.and_filter(is_null(column("section_name")))
        return self

    def with_section_order_is(self, val):
        self.query.and_filter(eq("section_order", val))
        return self

    def with_section_order_is_not(self, val):
        self.query.and_filter(ne("section_order", val))
        return self

    def with_section_order_in(self, *vals):
        _set_arguments("with_section_order_in", vals)
        if not vals:
            self.query.and_filter(is_null(column("id")))
            return self
        self.query.and_filter(in_list("section_order", list(vals)))
        return self

    def with_section_order_not_in(self, *vals):
        _set_arguments("with_section_order_not_in", vals)
        if not vals:
            return self
        self.query.and_filter(not_in_list("section_order", list(vals)))
        return self

    def with_section_order_greater_than(self, val):
        self.query.and_filter(gt("section_order", val))
        return self

    def with_section_order_greater_than_or_equal_to(self, val):
        self.query.and_filter(gte("section_order", val))
        return self

    def with_section_order_less_than(self, val):
        self.query.and_filter(lt("section_order", val))
        return self

    def with_section_order_less_than_or_equal_to(self, val):
        self.query.and_filter(lte("section_order", val))
        return self

    def with_section_order_between(self, lower, upper):
        self.query.and_filter(between(column("section_order"), value(lower), value(upper)))
        return self

    def with_section_order_is_known(self):
        self.query.and_filter(is_not_null(column("section_order")))
        return self

    def with_section_order_is_unknown(self):
        self.query.and_filter(is_null(column("section_order")))
        return self

    def which_are_default_section(self):
        self.query.and_filter(eq("default_section", True))
        return self

    def which_are_not_default_section(self):
        self.query.and_filter(eq("default_section", False))
        return self
    def with_default_section_is_not(self, val):
        self.query.and_filter(ne("default_section", val))
        return self

    def with_default_section_in(self, *vals):
        _set_arguments("with_default_section_in", vals)
        if not vals:
            self.query.and_filter(is_null(column("id")))
            return self
        self.query.and_filter(in_list("default_section", list(vals)))
        return self

    def with_default_section_not_in(self, *vals):
        _set_arguments("with_default_section_not_in", vals)
        if not vals:
            return self
        self.query.and_filter(not_in_list("default_section", list(vals)))
        return self

    def with_default_section_greater_than(self, val):
        self.query.and_filter(gt("default_section", val))
        return self

    def with_default_section_greater_than_or_equal_to(self, val):
        self.query.and_filter(gte("default_section", val))
        return self

    def with_default_section_less_than(self, val):
        self.query.and_filter(lt("default_section", val))
        return self

    def with_default_section_less_than_or_equal_to(self, val):
        self.query.and_filter(lte("default_section", val))
        return self

    def with_default_section_between(self, lower, upper):
        self.query.and_filter(between(column("default_section"), value(lower), value(upper)))
        return self

    def with_default_section_is_known(self):
        self.query.and_filter(is_not_null(column("default_section")))
        return self

    def with_default_section_is_unknown(self):
        self.query.and_filter(is_null(column("default_section")))
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



    def order_by_section_name_ascending(self):
        self.query.order_by("section_name", "asc")
        return self

    def order_by_section_name_descending(self):
        self.query.order_by("section_name", "desc")
        return self

    def order_by_section_order_ascending(self):
        self.query.order_by("section_order", "asc")
        return self

    def order_by_section_order_descending(self):
        self.query.order_by("section_order", "desc")
        return self

    def order_by_default_section_ascending(self):
        self.query.order_by("default_section", "asc")
        return self

    def order_by_default_section_descending(self):
        self.query.order_by("default_section", "desc")
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

    def min_section_order(self):
        return self.min_section_order_as("minOfSectionOrder")

    def min_section_order_as(self, ret_name: str):
        self.query.min("section_order", ret_name)
        return self
    def max_section_order(self):
        return self.max_section_order_as("maxOfSectionOrder")

    def max_section_order_as(self, ret_name: str):
        self.query.max("section_order", ret_name)
        return self
    def sum_section_order(self):
        return self.sum_section_order_as("sumOfSectionOrder")

    def sum_section_order_as(self, ret_name: str):
        self.query.sum("section_order", ret_name)
        return self
    def avg_section_order(self):
        return self.avg_section_order_as("avgOfSectionOrder")

    def avg_section_order_as(self, ret_name: str):
        self.query.avg("section_order", ret_name)
        return self
    def standardDeviation_section_order(self):
        return self.standardDeviation_section_order_as("standardDeviationOfSectionOrder")

    def standardDeviation_section_order_as(self, ret_name: str):
        self.query.standardDeviation("section_order", ret_name)
        return self
    def squareRootOfPopulationStandardDeviation_section_order(self):
        return self.squareRootOfPopulationStandardDeviation_section_order_as("squareRootOfPopulationStandardDeviationOfSectionOrder")

    def squareRootOfPopulationStandardDeviation_section_order_as(self, ret_name: str):
        self.query.squareRootOfPopulationStandardDeviation("section_order", ret_name)
        return self
    def sampleVariance_section_order(self):
        return self.sampleVariance_section_order_as("sampleVarianceOfSectionOrder")

    def sampleVariance_section_order_as(self, ret_name: str):
        self.query.sampleVariance("section_order", ret_name)
        return self
    def samplePopulationVariance_section_order(self):
        return self.samplePopulationVariance_section_order_as("samplePopulationVarianceOfSectionOrder")

    def samplePopulationVariance_section_order_as(self, ret_name: str):
        self.query.samplePopulationVariance("section_order", ret_name)
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
    def group_by_section_name(self):
        self.query.group_by("section_name")
        return self

    def group_by_section_name_as(self, ret_name: str):
        self.query.group_by("section_name")
        return self
    def group_by_section_order(self):
        self.query.group_by("section_order")
        return self

    def group_by_section_order_as(self, ret_name: str):
        self.query.group_by("section_order")
        return self
    def group_by_default_section(self):
        self.query.group_by("default_section")
        return self

    def group_by_default_section_as(self, ret_name: str):
        self.query.group_by("default_section")
        return self
    def group_by_version(self):
        self.query.group_by("version")
        return self

    def group_by_version_as(self, ret_name: str):
        self.query.group_by("version")
        return self
    def select_work_task_list(self):
        from requests.work_task_request import WorkTaskRequest
        return self.select_work_task_list_with(WorkTaskRequest())

    def select_work_task_list_with(self, child_request):
        self.query.relation_query("work_task_list", child_request.query)
        return self
    def select_task_placement_list(self):
        from requests.task_placement_request import TaskPlacementRequest
        return self.select_task_placement_list_with(TaskPlacementRequest())

    def select_task_placement_list_with(self, child_request):
        self.query.relation_query("task_placement_list", child_request.query)
        return self
    def have_work_tasks(self):
        from requests.work_task_request import WorkTaskRequest
        return self.with_work_task_list_matching(WorkTaskRequest())

    def have_no_work_tasks(self):
        from requests.work_task_request import WorkTaskRequest
        return self.without_work_task_list_matching(WorkTaskRequest())

    def with_work_task_list_matching(self, child_request):
        child_request.query.projection = ["section"]
        self.query.and_filter(in_subquery(column("id"), "WorkTask", child_request.query))
        return self

    def without_work_task_list_matching(self, child_request):
        child_request.query.projection = ["section"]
        self.query.and_filter(not_in_subquery(column("id"), "WorkTask", child_request.query))
        return self
    def have_task_placements(self):
        from requests.task_placement_request import TaskPlacementRequest
        return self.with_task_placement_list_matching(TaskPlacementRequest())

    def have_no_task_placements(self):
        from requests.task_placement_request import TaskPlacementRequest
        return self.without_task_placement_list_matching(TaskPlacementRequest())

    def with_task_placement_list_matching(self, child_request):
        child_request.query.projection = ["section"]
        self.query.and_filter(in_subquery(column("id"), "TaskPlacement", child_request.query))
        return self

    def without_task_placement_list_matching(self, child_request):
        child_request.query.projection = ["section"]
        self.query.and_filter(not_in_subquery(column("id"), "TaskPlacement", child_request.query))
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
    def facet_by_work_space_as(self, name: str, request: QuerySelection,
                                      include_all_facets: bool = True):
        self.query.facet_by(name, "work_space", request.query, include_all_facets)
        return self

    def facet_by_project_as(self, name: str, request: QuerySelection,
                                      include_all_facets: bool = True):
        self.query.facet_by(name, "project", request.query, include_all_facets)
        return self


class ExecutableProjectSectionRequest:
    def __init__(self, request):
        self._request = request

    def comment(self, c: str):
        self._request.comment(c)
        return self

    def new_entity(self, context) -> ProjectSection:
        request = self._request
        if not request._comment or not request._comment.strip() or not request._purpose or not request._purpose.strip():
            raise ValueError("Security audit failure: non-empty comment() and purpose() are required before new_entity()")
        entity = context.initialize_entity("ProjectSection", ProjectSection._teaql_construct())
        if not isinstance(entity, ProjectSection):
            raise TypeError("entity initializer returned an incompatible ProjectSection")
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

    async def execute_for_list(self, context) -> SmartList[ProjectSection]:
        result = await self.execute_for_result(context)
        query_root = EntityRoot()
        return SmartList(
            (ProjectSection._teaql_construct(_entity_root=query_root, **row) for row in result.rows),
            facets=result.facets)

    async def execute_for_page(self, context, offset: int, limit: int) -> TeaQLPage[ProjectSection]:
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
        data = SmartList(ProjectSection._teaql_construct(_entity_root=query_root, **row) for row in row_result.rows)
        return TeaQLPage(data=data, total_count=total_count, offset=offset, limit=limit)

    async def execute_for_one(self, context):
        request = deepcopy(self._request)
        request.limit(1)
        entities = await ExecutableProjectSectionRequest(request).execute_for_list(context)
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
                yield ProjectSection._teaql_construct(_entity_root=query_root, **row)
