class TeaQLNotLoadedError(RuntimeError):
    def __init__(self, root, access_path, break_point):
        self.root = root
        self.access_path = access_path
        self.break_point = break_point
        super().__init__(
            f"TeaQLNotLoadedError: root={root} access_path={access_path} "
            f"break_point={break_point} suggested_fix=select_{break_point}(...)"
        )


class ValueExpression:
    def __init__(self, value=None, error=None):
        self._value = value
        self._error = error

    def eval(self):
        if self._error is not None:
            raise self._error
        return self._value

    def or_if_null(self, fallback):
        value = self.eval()
        return fallback if value is None else value


class EntityExpression:
    def __init__(self, value, root=None, path="", error=None):
        self._value = value
        self._root = root or f"{type(value).__name__ if value is not None else 'Entity'}(null)"
        self._path = path
        self._error = error

    def eval(self):
        if self._error is not None:
            raise self._error
        return self._value

    def _path_for(self, field):
        return f"{self._path}.{field}" if self._path else field

    def _not_loaded(self, field):
        path = self._path_for(field)
        return TeaQLNotLoadedError(self._root, path, field)

    def _scalar(self, field, relation_id=False):
        if self._error is not None:
            return ValueExpression(error=self._error)
        if self._value is None:
            return ValueExpression(None)
        if field not in getattr(self._value, "_loaded_fields", set()):
            return ValueExpression(error=self._not_loaded(field))
        value = getattr(self._value, field)
        if relation_id and value is not None and not isinstance(value, (int, str)):
            value = getattr(value, "id", None)
        return ValueExpression(value)

    def _relation(self, field, expression_type):
        path = self._path_for(field)
        if self._error is not None:
            return expression_type(None, self._root, path, self._error)
        if self._value is None:
            return expression_type(None, self._root, path)
        if field not in getattr(self._value, "_loaded_fields", set()):
            return expression_type(None, self._root, path, self._not_loaded(field))
        value = getattr(self._value, field)
        if value is not None and isinstance(value, (int, str)):
            return expression_type(None, self._root, path, self._not_loaded(field))
        return expression_type(value, self._root, path)


class ListExpression:
    def __init__(self, values, root, path, item_expression, error=None):
        self._values = values
        self._root = root
        self._path = path
        self._item_expression = item_expression
        self._error = error

    def size(self):
        return ValueExpression(error=self._error) if self._error else ValueExpression(len(self._values))

    def first(self):
        return self.get(0)

    def get(self, index):
        path = f"{self._path}.get({index})"
        if self._error is not None:
            return self._item_expression(None, self._root, path, self._error)
        value = self._values[index] if 0 <= index < len(self._values) else None
        return self._item_expression(value, self._root, path)


class WorkSpaceExpression(EntityExpression):
    def id(self):
        return self._scalar("id")
    def workspace_name(self):
        return self._scalar("workspaceName")
    def version(self):
        return self._scalar("version")
    def work_account_list(self):
        path = self._path_for("work_account_list")
        if self._error is not None:
            return ListExpression([], self._root, path, WorkAccountExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, WorkAccountExpression)
        if "work_account_list" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, WorkAccountExpression, self._not_loaded("work_account_list"))
        return ListExpression(getattr(self._value, "_work_account_list"), self._root, path, WorkAccountExpression)
    def work_project_list(self):
        path = self._path_for("work_project_list")
        if self._error is not None:
            return ListExpression([], self._root, path, WorkProjectExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, WorkProjectExpression)
        if "work_project_list" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, WorkProjectExpression, self._not_loaded("work_project_list"))
        return ListExpression(getattr(self._value, "_work_project_list"), self._root, path, WorkProjectExpression)
    def project_membership_list(self):
        path = self._path_for("project_membership_list")
        if self._error is not None:
            return ListExpression([], self._root, path, ProjectMembershipExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, ProjectMembershipExpression)
        if "project_membership_list" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, ProjectMembershipExpression, self._not_loaded("project_membership_list"))
        return ListExpression(getattr(self._value, "_project_membership_list"), self._root, path, ProjectMembershipExpression)
    def project_section_list(self):
        path = self._path_for("project_section_list")
        if self._error is not None:
            return ListExpression([], self._root, path, ProjectSectionExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, ProjectSectionExpression)
        if "project_section_list" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, ProjectSectionExpression, self._not_loaded("project_section_list"))
        return ListExpression(getattr(self._value, "_project_section_list"), self._root, path, ProjectSectionExpression)
    def work_task_list(self):
        path = self._path_for("work_task_list")
        if self._error is not None:
            return ListExpression([], self._root, path, WorkTaskExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, WorkTaskExpression)
        if "work_task_list" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, WorkTaskExpression, self._not_loaded("work_task_list"))
        return ListExpression(getattr(self._value, "_work_task_list"), self._root, path, WorkTaskExpression)
    def project_field_list(self):
        path = self._path_for("project_field_list")
        if self._error is not None:
            return ListExpression([], self._root, path, ProjectFieldExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, ProjectFieldExpression)
        if "project_field_list" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, ProjectFieldExpression, self._not_loaded("project_field_list"))
        return ListExpression(getattr(self._value, "_project_field_list"), self._root, path, ProjectFieldExpression)
    def field_option_list(self):
        path = self._path_for("field_option_list")
        if self._error is not None:
            return ListExpression([], self._root, path, FieldOptionExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, FieldOptionExpression)
        if "field_option_list" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, FieldOptionExpression, self._not_loaded("field_option_list"))
        return ListExpression(getattr(self._value, "_field_option_list"), self._root, path, FieldOptionExpression)
    def task_field_choice_list(self):
        path = self._path_for("task_field_choice_list")
        if self._error is not None:
            return ListExpression([], self._root, path, TaskFieldChoiceExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, TaskFieldChoiceExpression)
        if "task_field_choice_list" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, TaskFieldChoiceExpression, self._not_loaded("task_field_choice_list"))
        return ListExpression(getattr(self._value, "_task_field_choice_list"), self._root, path, TaskFieldChoiceExpression)
    def work_subtask_list(self):
        path = self._path_for("work_subtask_list")
        if self._error is not None:
            return ListExpression([], self._root, path, WorkSubtaskExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, WorkSubtaskExpression)
        if "work_subtask_list" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, WorkSubtaskExpression, self._not_loaded("work_subtask_list"))
        return ListExpression(getattr(self._value, "_work_subtask_list"), self._root, path, WorkSubtaskExpression)
    def task_comment_list(self):
        path = self._path_for("task_comment_list")
        if self._error is not None:
            return ListExpression([], self._root, path, TaskCommentExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, TaskCommentExpression)
        if "task_comment_list" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, TaskCommentExpression, self._not_loaded("task_comment_list"))
        return ListExpression(getattr(self._value, "_task_comment_list"), self._root, path, TaskCommentExpression)
    def task_dependency_list(self):
        path = self._path_for("task_dependency_list")
        if self._error is not None:
            return ListExpression([], self._root, path, TaskDependencyExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, TaskDependencyExpression)
        if "task_dependency_list" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, TaskDependencyExpression, self._not_loaded("task_dependency_list"))
        return ListExpression(getattr(self._value, "_task_dependency_list"), self._root, path, TaskDependencyExpression)
    def task_placement_list(self):
        path = self._path_for("task_placement_list")
        if self._error is not None:
            return ListExpression([], self._root, path, TaskPlacementExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, TaskPlacementExpression)
        if "task_placement_list" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, TaskPlacementExpression, self._not_loaded("task_placement_list"))
        return ListExpression(getattr(self._value, "_task_placement_list"), self._root, path, TaskPlacementExpression)
    def recurrence_link_list(self):
        path = self._path_for("recurrence_link_list")
        if self._error is not None:
            return ListExpression([], self._root, path, RecurrenceLinkExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, RecurrenceLinkExpression)
        if "recurrence_link_list" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, RecurrenceLinkExpression, self._not_loaded("recurrence_link_list"))
        return ListExpression(getattr(self._value, "_recurrence_link_list"), self._root, path, RecurrenceLinkExpression)
    def task_event_list(self):
        path = self._path_for("task_event_list")
        if self._error is not None:
            return ListExpression([], self._root, path, TaskEventExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, TaskEventExpression)
        if "task_event_list" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, TaskEventExpression, self._not_loaded("task_event_list"))
        return ListExpression(getattr(self._value, "_task_event_list"), self._root, path, TaskEventExpression)
    def task_participant_list(self):
        path = self._path_for("task_participant_list")
        if self._error is not None:
            return ListExpression([], self._root, path, TaskParticipantExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, TaskParticipantExpression)
        if "task_participant_list" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, TaskParticipantExpression, self._not_loaded("task_participant_list"))
        return ListExpression(getattr(self._value, "_task_participant_list"), self._root, path, TaskParticipantExpression)
    def deleted_task_viewer_list(self):
        path = self._path_for("deleted_task_viewer_list")
        if self._error is not None:
            return ListExpression([], self._root, path, DeletedTaskViewerExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, DeletedTaskViewerExpression)
        if "deleted_task_viewer_list" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, DeletedTaskViewerExpression, self._not_loaded("deleted_task_viewer_list"))
        return ListExpression(getattr(self._value, "_deleted_task_viewer_list"), self._root, path, DeletedTaskViewerExpression)
    def task_blueprint_list(self):
        path = self._path_for("task_blueprint_list")
        if self._error is not None:
            return ListExpression([], self._root, path, TaskBlueprintExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, TaskBlueprintExpression)
        if "task_blueprint_list" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, TaskBlueprintExpression, self._not_loaded("task_blueprint_list"))
        return ListExpression(getattr(self._value, "_task_blueprint_list"), self._root, path, TaskBlueprintExpression)
    def blueprint_choice_list(self):
        path = self._path_for("blueprint_choice_list")
        if self._error is not None:
            return ListExpression([], self._root, path, BlueprintChoiceExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, BlueprintChoiceExpression)
        if "blueprint_choice_list" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, BlueprintChoiceExpression, self._not_loaded("blueprint_choice_list"))
        return ListExpression(getattr(self._value, "_blueprint_choice_list"), self._root, path, BlueprintChoiceExpression)
    def blueprint_subtask_list(self):
        path = self._path_for("blueprint_subtask_list")
        if self._error is not None:
            return ListExpression([], self._root, path, BlueprintSubtaskExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, BlueprintSubtaskExpression)
        if "blueprint_subtask_list" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, BlueprintSubtaskExpression, self._not_loaded("blueprint_subtask_list"))
        return ListExpression(getattr(self._value, "_blueprint_subtask_list"), self._root, path, BlueprintSubtaskExpression)
    def inbox_notice_list(self):
        path = self._path_for("inbox_notice_list")
        if self._error is not None:
            return ListExpression([], self._root, path, InboxNoticeExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, InboxNoticeExpression)
        if "inbox_notice_list" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, InboxNoticeExpression, self._not_loaded("inbox_notice_list"))
        return ListExpression(getattr(self._value, "_inbox_notice_list"), self._root, path, InboxNoticeExpression)
    pass

class WorkAccountExpression(EntityExpression):
    def id(self):
        return self._scalar("id")
    def display_name(self):
        return self._scalar("displayName")
    def email_address(self):
        return self._scalar("emailAddress")
    def password_hash(self):
        return self._scalar("passwordHash")
    def version(self):
        return self._scalar("version")
    def work_space_id(self):
        return self._scalar("workSpace", relation_id=True)

    def work_space(self):
        return self._relation("workSpace", WorkSpaceExpression)
    def work_project_list(self):
        path = self._path_for("work_project_list")
        if self._error is not None:
            return ListExpression([], self._root, path, WorkProjectExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, WorkProjectExpression)
        if "work_project_list" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, WorkProjectExpression, self._not_loaded("work_project_list"))
        return ListExpression(getattr(self._value, "_work_project_list"), self._root, path, WorkProjectExpression)
    def project_membership_list(self):
        path = self._path_for("project_membership_list")
        if self._error is not None:
            return ListExpression([], self._root, path, ProjectMembershipExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, ProjectMembershipExpression)
        if "project_membership_list" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, ProjectMembershipExpression, self._not_loaded("project_membership_list"))
        return ListExpression(getattr(self._value, "_project_membership_list"), self._root, path, ProjectMembershipExpression)
    def work_task_list_as_created_by(self):
        path = self._path_for("work_task_list_as_created_by")
        if self._error is not None:
            return ListExpression([], self._root, path, WorkTaskExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, WorkTaskExpression)
        if "work_task_list_as_created_by" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, WorkTaskExpression, self._not_loaded("work_task_list_as_created_by"))
        return ListExpression(getattr(self._value, "_work_task_list_as_created_by"), self._root, path, WorkTaskExpression)
    def work_task_list_as_assignee(self):
        path = self._path_for("work_task_list_as_assignee")
        if self._error is not None:
            return ListExpression([], self._root, path, WorkTaskExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, WorkTaskExpression)
        if "work_task_list_as_assignee" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, WorkTaskExpression, self._not_loaded("work_task_list_as_assignee"))
        return ListExpression(getattr(self._value, "_work_task_list_as_assignee"), self._root, path, WorkTaskExpression)
    def work_subtask_list(self):
        path = self._path_for("work_subtask_list")
        if self._error is not None:
            return ListExpression([], self._root, path, WorkSubtaskExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, WorkSubtaskExpression)
        if "work_subtask_list" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, WorkSubtaskExpression, self._not_loaded("work_subtask_list"))
        return ListExpression(getattr(self._value, "_work_subtask_list"), self._root, path, WorkSubtaskExpression)
    def task_comment_list(self):
        path = self._path_for("task_comment_list")
        if self._error is not None:
            return ListExpression([], self._root, path, TaskCommentExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, TaskCommentExpression)
        if "task_comment_list" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, TaskCommentExpression, self._not_loaded("task_comment_list"))
        return ListExpression(getattr(self._value, "_task_comment_list"), self._root, path, TaskCommentExpression)
    def task_event_list(self):
        path = self._path_for("task_event_list")
        if self._error is not None:
            return ListExpression([], self._root, path, TaskEventExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, TaskEventExpression)
        if "task_event_list" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, TaskEventExpression, self._not_loaded("task_event_list"))
        return ListExpression(getattr(self._value, "_task_event_list"), self._root, path, TaskEventExpression)
    def task_participant_list(self):
        path = self._path_for("task_participant_list")
        if self._error is not None:
            return ListExpression([], self._root, path, TaskParticipantExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, TaskParticipantExpression)
        if "task_participant_list" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, TaskParticipantExpression, self._not_loaded("task_participant_list"))
        return ListExpression(getattr(self._value, "_task_participant_list"), self._root, path, TaskParticipantExpression)
    def deleted_task_viewer_list(self):
        path = self._path_for("deleted_task_viewer_list")
        if self._error is not None:
            return ListExpression([], self._root, path, DeletedTaskViewerExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, DeletedTaskViewerExpression)
        if "deleted_task_viewer_list" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, DeletedTaskViewerExpression, self._not_loaded("deleted_task_viewer_list"))
        return ListExpression(getattr(self._value, "_deleted_task_viewer_list"), self._root, path, DeletedTaskViewerExpression)
    def task_blueprint_list(self):
        path = self._path_for("task_blueprint_list")
        if self._error is not None:
            return ListExpression([], self._root, path, TaskBlueprintExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, TaskBlueprintExpression)
        if "task_blueprint_list" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, TaskBlueprintExpression, self._not_loaded("task_blueprint_list"))
        return ListExpression(getattr(self._value, "_task_blueprint_list"), self._root, path, TaskBlueprintExpression)
    def blueprint_subtask_list(self):
        path = self._path_for("blueprint_subtask_list")
        if self._error is not None:
            return ListExpression([], self._root, path, BlueprintSubtaskExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, BlueprintSubtaskExpression)
        if "blueprint_subtask_list" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, BlueprintSubtaskExpression, self._not_loaded("blueprint_subtask_list"))
        return ListExpression(getattr(self._value, "_blueprint_subtask_list"), self._root, path, BlueprintSubtaskExpression)
    def inbox_notice_list(self):
        path = self._path_for("inbox_notice_list")
        if self._error is not None:
            return ListExpression([], self._root, path, InboxNoticeExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, InboxNoticeExpression)
        if "inbox_notice_list" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, InboxNoticeExpression, self._not_loaded("inbox_notice_list"))
        return ListExpression(getattr(self._value, "_inbox_notice_list"), self._root, path, InboxNoticeExpression)
    pass

class WorkProjectExpression(EntityExpression):
    def id(self):
        return self._scalar("id")
    def project_name(self):
        return self._scalar("projectName")
    def shift_dates(self):
        return self._scalar("shiftDates")
    def version(self):
        return self._scalar("version")
    def work_space_id(self):
        return self._scalar("workSpace", relation_id=True)

    def work_space(self):
        return self._relation("workSpace", WorkSpaceExpression)
    def owner_account_id(self):
        return self._scalar("ownerAccount", relation_id=True)

    def owner_account(self):
        return self._relation("ownerAccount", WorkAccountExpression)
    def project_membership_list(self):
        path = self._path_for("project_membership_list")
        if self._error is not None:
            return ListExpression([], self._root, path, ProjectMembershipExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, ProjectMembershipExpression)
        if "project_membership_list" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, ProjectMembershipExpression, self._not_loaded("project_membership_list"))
        return ListExpression(getattr(self._value, "_project_membership_list"), self._root, path, ProjectMembershipExpression)
    def project_section_list(self):
        path = self._path_for("project_section_list")
        if self._error is not None:
            return ListExpression([], self._root, path, ProjectSectionExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, ProjectSectionExpression)
        if "project_section_list" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, ProjectSectionExpression, self._not_loaded("project_section_list"))
        return ListExpression(getattr(self._value, "_project_section_list"), self._root, path, ProjectSectionExpression)
    def work_task_list(self):
        path = self._path_for("work_task_list")
        if self._error is not None:
            return ListExpression([], self._root, path, WorkTaskExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, WorkTaskExpression)
        if "work_task_list" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, WorkTaskExpression, self._not_loaded("work_task_list"))
        return ListExpression(getattr(self._value, "_work_task_list"), self._root, path, WorkTaskExpression)
    def project_field_list(self):
        path = self._path_for("project_field_list")
        if self._error is not None:
            return ListExpression([], self._root, path, ProjectFieldExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, ProjectFieldExpression)
        if "project_field_list" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, ProjectFieldExpression, self._not_loaded("project_field_list"))
        return ListExpression(getattr(self._value, "_project_field_list"), self._root, path, ProjectFieldExpression)
    def task_placement_list(self):
        path = self._path_for("task_placement_list")
        if self._error is not None:
            return ListExpression([], self._root, path, TaskPlacementExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, TaskPlacementExpression)
        if "task_placement_list" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, TaskPlacementExpression, self._not_loaded("task_placement_list"))
        return ListExpression(getattr(self._value, "_task_placement_list"), self._root, path, TaskPlacementExpression)
    def task_event_list(self):
        path = self._path_for("task_event_list")
        if self._error is not None:
            return ListExpression([], self._root, path, TaskEventExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, TaskEventExpression)
        if "task_event_list" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, TaskEventExpression, self._not_loaded("task_event_list"))
        return ListExpression(getattr(self._value, "_task_event_list"), self._root, path, TaskEventExpression)
    def task_blueprint_list(self):
        path = self._path_for("task_blueprint_list")
        if self._error is not None:
            return ListExpression([], self._root, path, TaskBlueprintExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, TaskBlueprintExpression)
        if "task_blueprint_list" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, TaskBlueprintExpression, self._not_loaded("task_blueprint_list"))
        return ListExpression(getattr(self._value, "_task_blueprint_list"), self._root, path, TaskBlueprintExpression)
    pass

class ProjectMembershipExpression(EntityExpression):
    def id(self):
        return self._scalar("id")
    def access_role(self):
        return self._scalar("accessRole")
    def version(self):
        return self._scalar("version")
    def work_space_id(self):
        return self._scalar("workSpace", relation_id=True)

    def work_space(self):
        return self._relation("workSpace", WorkSpaceExpression)
    def project_id(self):
        return self._scalar("project", relation_id=True)

    def project(self):
        return self._relation("project", WorkProjectExpression)
    def member_account_id(self):
        return self._scalar("memberAccount", relation_id=True)

    def member_account(self):
        return self._relation("memberAccount", WorkAccountExpression)
    pass

class ProjectSectionExpression(EntityExpression):
    def id(self):
        return self._scalar("id")
    def section_name(self):
        return self._scalar("sectionName")
    def section_order(self):
        return self._scalar("sectionOrder")
    def default_section(self):
        return self._scalar("defaultSection")
    def version(self):
        return self._scalar("version")
    def work_space_id(self):
        return self._scalar("workSpace", relation_id=True)

    def work_space(self):
        return self._relation("workSpace", WorkSpaceExpression)
    def project_id(self):
        return self._scalar("project", relation_id=True)

    def project(self):
        return self._relation("project", WorkProjectExpression)
    def work_task_list(self):
        path = self._path_for("work_task_list")
        if self._error is not None:
            return ListExpression([], self._root, path, WorkTaskExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, WorkTaskExpression)
        if "work_task_list" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, WorkTaskExpression, self._not_loaded("work_task_list"))
        return ListExpression(getattr(self._value, "_work_task_list"), self._root, path, WorkTaskExpression)
    def task_placement_list(self):
        path = self._path_for("task_placement_list")
        if self._error is not None:
            return ListExpression([], self._root, path, TaskPlacementExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, TaskPlacementExpression)
        if "task_placement_list" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, TaskPlacementExpression, self._not_loaded("task_placement_list"))
        return ListExpression(getattr(self._value, "_task_placement_list"), self._root, path, TaskPlacementExpression)
    pass

class WorkTaskExpression(EntityExpression):
    def id(self):
        return self._scalar("id")
    def deleted_epoch(self):
        return self._scalar("deletedEpoch")
    def approval(self):
        return self._scalar("approval")
    def decision(self):
        return self._scalar("decision")
    def repeat_period(self):
        return self._scalar("repeatPeriod")
    def primary_detached(self):
        return self._scalar("primaryDetached")
    def task_order(self):
        return self._scalar("taskOrder")
    def task_title(self):
        return self._scalar("taskTitle")
    def description(self):
        return self._scalar("description")
    def start_date(self):
        return self._scalar("startDate")
    def due_date(self):
        return self._scalar("dueDate")
    def completed(self):
        return self._scalar("completed")
    def version(self):
        return self._scalar("version")
    def work_space_id(self):
        return self._scalar("workSpace", relation_id=True)

    def work_space(self):
        return self._relation("workSpace", WorkSpaceExpression)
    def project_id(self):
        return self._scalar("project", relation_id=True)

    def project(self):
        return self._relation("project", WorkProjectExpression)
    def section_id(self):
        return self._scalar("section", relation_id=True)

    def section(self):
        return self._relation("section", ProjectSectionExpression)
    def created_by_id(self):
        return self._scalar("createdBy", relation_id=True)

    def created_by(self):
        return self._relation("createdBy", WorkAccountExpression)
    def assignee_id(self):
        return self._scalar("assignee", relation_id=True)

    def assignee(self):
        return self._relation("assignee", WorkAccountExpression)
    def task_field_choice_list(self):
        path = self._path_for("task_field_choice_list")
        if self._error is not None:
            return ListExpression([], self._root, path, TaskFieldChoiceExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, TaskFieldChoiceExpression)
        if "task_field_choice_list" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, TaskFieldChoiceExpression, self._not_loaded("task_field_choice_list"))
        return ListExpression(getattr(self._value, "_task_field_choice_list"), self._root, path, TaskFieldChoiceExpression)
    def work_subtask_list(self):
        path = self._path_for("work_subtask_list")
        if self._error is not None:
            return ListExpression([], self._root, path, WorkSubtaskExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, WorkSubtaskExpression)
        if "work_subtask_list" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, WorkSubtaskExpression, self._not_loaded("work_subtask_list"))
        return ListExpression(getattr(self._value, "_work_subtask_list"), self._root, path, WorkSubtaskExpression)
    def task_comment_list(self):
        path = self._path_for("task_comment_list")
        if self._error is not None:
            return ListExpression([], self._root, path, TaskCommentExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, TaskCommentExpression)
        if "task_comment_list" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, TaskCommentExpression, self._not_loaded("task_comment_list"))
        return ListExpression(getattr(self._value, "_task_comment_list"), self._root, path, TaskCommentExpression)
    def task_dependency_list_as_dependent(self):
        path = self._path_for("task_dependency_list_as_dependent")
        if self._error is not None:
            return ListExpression([], self._root, path, TaskDependencyExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, TaskDependencyExpression)
        if "task_dependency_list_as_dependent" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, TaskDependencyExpression, self._not_loaded("task_dependency_list_as_dependent"))
        return ListExpression(getattr(self._value, "_task_dependency_list_as_dependent"), self._root, path, TaskDependencyExpression)
    def task_dependency_list_as_blocker(self):
        path = self._path_for("task_dependency_list_as_blocker")
        if self._error is not None:
            return ListExpression([], self._root, path, TaskDependencyExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, TaskDependencyExpression)
        if "task_dependency_list_as_blocker" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, TaskDependencyExpression, self._not_loaded("task_dependency_list_as_blocker"))
        return ListExpression(getattr(self._value, "_task_dependency_list_as_blocker"), self._root, path, TaskDependencyExpression)
    def task_placement_list(self):
        path = self._path_for("task_placement_list")
        if self._error is not None:
            return ListExpression([], self._root, path, TaskPlacementExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, TaskPlacementExpression)
        if "task_placement_list" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, TaskPlacementExpression, self._not_loaded("task_placement_list"))
        return ListExpression(getattr(self._value, "_task_placement_list"), self._root, path, TaskPlacementExpression)
    def recurrence_link_list_as_source_task(self):
        path = self._path_for("recurrence_link_list_as_source_task")
        if self._error is not None:
            return ListExpression([], self._root, path, RecurrenceLinkExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, RecurrenceLinkExpression)
        if "recurrence_link_list_as_source_task" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, RecurrenceLinkExpression, self._not_loaded("recurrence_link_list_as_source_task"))
        return ListExpression(getattr(self._value, "_recurrence_link_list_as_source_task"), self._root, path, RecurrenceLinkExpression)
    def recurrence_link_list_as_next_task(self):
        path = self._path_for("recurrence_link_list_as_next_task")
        if self._error is not None:
            return ListExpression([], self._root, path, RecurrenceLinkExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, RecurrenceLinkExpression)
        if "recurrence_link_list_as_next_task" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, RecurrenceLinkExpression, self._not_loaded("recurrence_link_list_as_next_task"))
        return ListExpression(getattr(self._value, "_recurrence_link_list_as_next_task"), self._root, path, RecurrenceLinkExpression)
    def task_event_list_as_task(self):
        path = self._path_for("task_event_list_as_task")
        if self._error is not None:
            return ListExpression([], self._root, path, TaskEventExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, TaskEventExpression)
        if "task_event_list_as_task" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, TaskEventExpression, self._not_loaded("task_event_list_as_task"))
        return ListExpression(getattr(self._value, "_task_event_list_as_task"), self._root, path, TaskEventExpression)
    def task_event_list_as_related_task(self):
        path = self._path_for("task_event_list_as_related_task")
        if self._error is not None:
            return ListExpression([], self._root, path, TaskEventExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, TaskEventExpression)
        if "task_event_list_as_related_task" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, TaskEventExpression, self._not_loaded("task_event_list_as_related_task"))
        return ListExpression(getattr(self._value, "_task_event_list_as_related_task"), self._root, path, TaskEventExpression)
    def task_participant_list(self):
        path = self._path_for("task_participant_list")
        if self._error is not None:
            return ListExpression([], self._root, path, TaskParticipantExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, TaskParticipantExpression)
        if "task_participant_list" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, TaskParticipantExpression, self._not_loaded("task_participant_list"))
        return ListExpression(getattr(self._value, "_task_participant_list"), self._root, path, TaskParticipantExpression)
    def deleted_task_viewer_list(self):
        path = self._path_for("deleted_task_viewer_list")
        if self._error is not None:
            return ListExpression([], self._root, path, DeletedTaskViewerExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, DeletedTaskViewerExpression)
        if "deleted_task_viewer_list" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, DeletedTaskViewerExpression, self._not_loaded("deleted_task_viewer_list"))
        return ListExpression(getattr(self._value, "_deleted_task_viewer_list"), self._root, path, DeletedTaskViewerExpression)
    def inbox_notice_list(self):
        path = self._path_for("inbox_notice_list")
        if self._error is not None:
            return ListExpression([], self._root, path, InboxNoticeExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, InboxNoticeExpression)
        if "inbox_notice_list" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, InboxNoticeExpression, self._not_loaded("inbox_notice_list"))
        return ListExpression(getattr(self._value, "_inbox_notice_list"), self._root, path, InboxNoticeExpression)
    pass

class ProjectFieldExpression(EntityExpression):
    def id(self):
        return self._scalar("id")
    def field_name(self):
        return self._scalar("fieldName")
    def version(self):
        return self._scalar("version")
    def work_space_id(self):
        return self._scalar("workSpace", relation_id=True)

    def work_space(self):
        return self._relation("workSpace", WorkSpaceExpression)
    def project_id(self):
        return self._scalar("project", relation_id=True)

    def project(self):
        return self._relation("project", WorkProjectExpression)
    def field_option_list(self):
        path = self._path_for("field_option_list")
        if self._error is not None:
            return ListExpression([], self._root, path, FieldOptionExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, FieldOptionExpression)
        if "field_option_list" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, FieldOptionExpression, self._not_loaded("field_option_list"))
        return ListExpression(getattr(self._value, "_field_option_list"), self._root, path, FieldOptionExpression)
    def task_field_choice_list(self):
        path = self._path_for("task_field_choice_list")
        if self._error is not None:
            return ListExpression([], self._root, path, TaskFieldChoiceExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, TaskFieldChoiceExpression)
        if "task_field_choice_list" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, TaskFieldChoiceExpression, self._not_loaded("task_field_choice_list"))
        return ListExpression(getattr(self._value, "_task_field_choice_list"), self._root, path, TaskFieldChoiceExpression)
    def blueprint_choice_list(self):
        path = self._path_for("blueprint_choice_list")
        if self._error is not None:
            return ListExpression([], self._root, path, BlueprintChoiceExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, BlueprintChoiceExpression)
        if "blueprint_choice_list" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, BlueprintChoiceExpression, self._not_loaded("blueprint_choice_list"))
        return ListExpression(getattr(self._value, "_blueprint_choice_list"), self._root, path, BlueprintChoiceExpression)
    pass

class FieldOptionExpression(EntityExpression):
    def id(self):
        return self._scalar("id")
    def option_name(self):
        return self._scalar("optionName")
    def option_order(self):
        return self._scalar("optionOrder")
    def version(self):
        return self._scalar("version")
    def work_space_id(self):
        return self._scalar("workSpace", relation_id=True)

    def work_space(self):
        return self._relation("workSpace", WorkSpaceExpression)
    def field_id(self):
        return self._scalar("field", relation_id=True)

    def field(self):
        return self._relation("field", ProjectFieldExpression)
    def task_field_choice_list(self):
        path = self._path_for("task_field_choice_list")
        if self._error is not None:
            return ListExpression([], self._root, path, TaskFieldChoiceExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, TaskFieldChoiceExpression)
        if "task_field_choice_list" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, TaskFieldChoiceExpression, self._not_loaded("task_field_choice_list"))
        return ListExpression(getattr(self._value, "_task_field_choice_list"), self._root, path, TaskFieldChoiceExpression)
    def blueprint_choice_list(self):
        path = self._path_for("blueprint_choice_list")
        if self._error is not None:
            return ListExpression([], self._root, path, BlueprintChoiceExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, BlueprintChoiceExpression)
        if "blueprint_choice_list" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, BlueprintChoiceExpression, self._not_loaded("blueprint_choice_list"))
        return ListExpression(getattr(self._value, "_blueprint_choice_list"), self._root, path, BlueprintChoiceExpression)
    pass

class TaskFieldChoiceExpression(EntityExpression):
    def id(self):
        return self._scalar("id")
    def version(self):
        return self._scalar("version")
    def work_space_id(self):
        return self._scalar("workSpace", relation_id=True)

    def work_space(self):
        return self._relation("workSpace", WorkSpaceExpression)
    def task_id(self):
        return self._scalar("task", relation_id=True)

    def task(self):
        return self._relation("task", WorkTaskExpression)
    def field_id(self):
        return self._scalar("field", relation_id=True)

    def field(self):
        return self._relation("field", ProjectFieldExpression)
    def selected_option_id(self):
        return self._scalar("selectedOption", relation_id=True)

    def selected_option(self):
        return self._relation("selectedOption", FieldOptionExpression)
    pass

class WorkSubtaskExpression(EntityExpression):
    def id(self):
        return self._scalar("id")
    def subtask_title(self):
        return self._scalar("subtaskTitle")
    def due_date(self):
        return self._scalar("dueDate")
    def completed(self):
        return self._scalar("completed")
    def version(self):
        return self._scalar("version")
    def work_space_id(self):
        return self._scalar("workSpace", relation_id=True)

    def work_space(self):
        return self._relation("workSpace", WorkSpaceExpression)
    def task_id(self):
        return self._scalar("task", relation_id=True)

    def task(self):
        return self._relation("task", WorkTaskExpression)
    def assignee_id(self):
        return self._scalar("assignee", relation_id=True)

    def assignee(self):
        return self._relation("assignee", WorkAccountExpression)
    pass

class TaskCommentExpression(EntityExpression):
    def id(self):
        return self._scalar("id")
    def comment_text(self):
        return self._scalar("commentText")
    def edited(self):
        return self._scalar("edited")
    def create_time(self):
        return self._scalar("createTime")
    def version(self):
        return self._scalar("version")
    def work_space_id(self):
        return self._scalar("workSpace", relation_id=True)

    def work_space(self):
        return self._relation("workSpace", WorkSpaceExpression)
    def task_id(self):
        return self._scalar("task", relation_id=True)

    def task(self):
        return self._relation("task", WorkTaskExpression)
    def author_id(self):
        return self._scalar("author", relation_id=True)

    def author(self):
        return self._relation("author", WorkAccountExpression)
    pass

class TaskDependencyExpression(EntityExpression):
    def id(self):
        return self._scalar("id")
    def version(self):
        return self._scalar("version")
    def work_space_id(self):
        return self._scalar("workSpace", relation_id=True)

    def work_space(self):
        return self._relation("workSpace", WorkSpaceExpression)
    def dependent_id(self):
        return self._scalar("dependent", relation_id=True)

    def dependent(self):
        return self._relation("dependent", WorkTaskExpression)
    def blocker_id(self):
        return self._scalar("blocker", relation_id=True)

    def blocker(self):
        return self._relation("blocker", WorkTaskExpression)
    pass

class TaskPlacementExpression(EntityExpression):
    def id(self):
        return self._scalar("id")
    def placement_order(self):
        return self._scalar("placementOrder")
    def version(self):
        return self._scalar("version")
    def work_space_id(self):
        return self._scalar("workSpace", relation_id=True)

    def work_space(self):
        return self._relation("workSpace", WorkSpaceExpression)
    def task_id(self):
        return self._scalar("task", relation_id=True)

    def task(self):
        return self._relation("task", WorkTaskExpression)
    def project_id(self):
        return self._scalar("project", relation_id=True)

    def project(self):
        return self._relation("project", WorkProjectExpression)
    def section_id(self):
        return self._scalar("section", relation_id=True)

    def section(self):
        return self._relation("section", ProjectSectionExpression)
    pass

class RecurrenceLinkExpression(EntityExpression):
    def id(self):
        return self._scalar("id")
    def version(self):
        return self._scalar("version")
    def work_space_id(self):
        return self._scalar("workSpace", relation_id=True)

    def work_space(self):
        return self._relation("workSpace", WorkSpaceExpression)
    def source_task_id(self):
        return self._scalar("sourceTask", relation_id=True)

    def source_task(self):
        return self._relation("sourceTask", WorkTaskExpression)
    def next_task_id(self):
        return self._scalar("nextTask", relation_id=True)

    def next_task(self):
        return self._relation("nextTask", WorkTaskExpression)
    pass

class TaskEventExpression(EntityExpression):
    def id(self):
        return self._scalar("id")
    def event_kind(self):
        return self._scalar("eventKind")
    def field_label(self):
        return self._scalar("fieldLabel")
    def old_value(self):
        return self._scalar("oldValue")
    def new_value(self):
        return self._scalar("newValue")
    def event_time(self):
        return self._scalar("eventTime")
    def version(self):
        return self._scalar("version")
    def work_space_id(self):
        return self._scalar("workSpace", relation_id=True)

    def work_space(self):
        return self._relation("workSpace", WorkSpaceExpression)
    def task_id(self):
        return self._scalar("task", relation_id=True)

    def task(self):
        return self._relation("task", WorkTaskExpression)
    def actor_id(self):
        return self._scalar("actor", relation_id=True)

    def actor(self):
        return self._relation("actor", WorkAccountExpression)
    def scope_project_id(self):
        return self._scalar("scopeProject", relation_id=True)

    def scope_project(self):
        return self._relation("scopeProject", WorkProjectExpression)
    def related_task_id(self):
        return self._scalar("relatedTask", relation_id=True)

    def related_task(self):
        return self._relation("relatedTask", WorkTaskExpression)
    def inbox_notice_list(self):
        path = self._path_for("inbox_notice_list")
        if self._error is not None:
            return ListExpression([], self._root, path, InboxNoticeExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, InboxNoticeExpression)
        if "inbox_notice_list" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, InboxNoticeExpression, self._not_loaded("inbox_notice_list"))
        return ListExpression(getattr(self._value, "_inbox_notice_list"), self._root, path, InboxNoticeExpression)
    pass

class TaskParticipantExpression(EntityExpression):
    def id(self):
        return self._scalar("id")
    def version(self):
        return self._scalar("version")
    def work_space_id(self):
        return self._scalar("workSpace", relation_id=True)

    def work_space(self):
        return self._relation("workSpace", WorkSpaceExpression)
    def task_id(self):
        return self._scalar("task", relation_id=True)

    def task(self):
        return self._relation("task", WorkTaskExpression)
    def participant_id(self):
        return self._scalar("participant", relation_id=True)

    def participant(self):
        return self._relation("participant", WorkAccountExpression)
    pass

class DeletedTaskViewerExpression(EntityExpression):
    def id(self):
        return self._scalar("id")
    def version(self):
        return self._scalar("version")
    def work_space_id(self):
        return self._scalar("workSpace", relation_id=True)

    def work_space(self):
        return self._relation("workSpace", WorkSpaceExpression)
    def task_id(self):
        return self._scalar("task", relation_id=True)

    def task(self):
        return self._relation("task", WorkTaskExpression)
    def viewer_id(self):
        return self._scalar("viewer", relation_id=True)

    def viewer(self):
        return self._relation("viewer", WorkAccountExpression)
    pass

class TaskBlueprintExpression(EntityExpression):
    def id(self):
        return self._scalar("id")
    def template_name(self):
        return self._scalar("templateName")
    def initial_title(self):
        return self._scalar("initialTitle")
    def initial_description(self):
        return self._scalar("initialDescription")
    def due_offset(self):
        return self._scalar("dueOffset")
    def repeat_period(self):
        return self._scalar("repeatPeriod")
    def approval(self):
        return self._scalar("approval")
    def version(self):
        return self._scalar("version")
    def work_space_id(self):
        return self._scalar("workSpace", relation_id=True)

    def work_space(self):
        return self._relation("workSpace", WorkSpaceExpression)
    def project_id(self):
        return self._scalar("project", relation_id=True)

    def project(self):
        return self._relation("project", WorkProjectExpression)
    def assignee_id(self):
        return self._scalar("assignee", relation_id=True)

    def assignee(self):
        return self._relation("assignee", WorkAccountExpression)
    def blueprint_choice_list(self):
        path = self._path_for("blueprint_choice_list")
        if self._error is not None:
            return ListExpression([], self._root, path, BlueprintChoiceExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, BlueprintChoiceExpression)
        if "blueprint_choice_list" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, BlueprintChoiceExpression, self._not_loaded("blueprint_choice_list"))
        return ListExpression(getattr(self._value, "_blueprint_choice_list"), self._root, path, BlueprintChoiceExpression)
    def blueprint_subtask_list(self):
        path = self._path_for("blueprint_subtask_list")
        if self._error is not None:
            return ListExpression([], self._root, path, BlueprintSubtaskExpression, self._error)
        if self._value is None:
            return ListExpression([], self._root, path, BlueprintSubtaskExpression)
        if "blueprint_subtask_list" not in getattr(self._value, "_loaded_fields", set()):
            return ListExpression([], self._root, path, BlueprintSubtaskExpression, self._not_loaded("blueprint_subtask_list"))
        return ListExpression(getattr(self._value, "_blueprint_subtask_list"), self._root, path, BlueprintSubtaskExpression)
    pass

class BlueprintChoiceExpression(EntityExpression):
    def id(self):
        return self._scalar("id")
    def version(self):
        return self._scalar("version")
    def work_space_id(self):
        return self._scalar("workSpace", relation_id=True)

    def work_space(self):
        return self._relation("workSpace", WorkSpaceExpression)
    def blueprint_id(self):
        return self._scalar("blueprint", relation_id=True)

    def blueprint(self):
        return self._relation("blueprint", TaskBlueprintExpression)
    def field_id(self):
        return self._scalar("field", relation_id=True)

    def field(self):
        return self._relation("field", ProjectFieldExpression)
    def selected_option_id(self):
        return self._scalar("selectedOption", relation_id=True)

    def selected_option(self):
        return self._relation("selectedOption", FieldOptionExpression)
    pass

class BlueprintSubtaskExpression(EntityExpression):
    def id(self):
        return self._scalar("id")
    def subtask_title(self):
        return self._scalar("subtaskTitle")
    def due_offset(self):
        return self._scalar("dueOffset")
    def version(self):
        return self._scalar("version")
    def work_space_id(self):
        return self._scalar("workSpace", relation_id=True)

    def work_space(self):
        return self._relation("workSpace", WorkSpaceExpression)
    def blueprint_id(self):
        return self._scalar("blueprint", relation_id=True)

    def blueprint(self):
        return self._relation("blueprint", TaskBlueprintExpression)
    def assignee_id(self):
        return self._scalar("assignee", relation_id=True)

    def assignee(self):
        return self._relation("assignee", WorkAccountExpression)
    pass

class InboxNoticeExpression(EntityExpression):
    def id(self):
        return self._scalar("id")
    def read_flag(self):
        return self._scalar("readFlag")
    def version(self):
        return self._scalar("version")
    def work_space_id(self):
        return self._scalar("workSpace", relation_id=True)

    def work_space(self):
        return self._relation("workSpace", WorkSpaceExpression)
    def task_id(self):
        return self._scalar("task", relation_id=True)

    def task(self):
        return self._relation("task", WorkTaskExpression)
    def recipient_id(self):
        return self._scalar("recipient", relation_id=True)

    def recipient(self):
        return self._relation("recipient", WorkAccountExpression)
    def event_id(self):
        return self._scalar("event", relation_id=True)

    def event(self):
        return self._relation("event", TaskEventExpression)
    pass

class E:
    @staticmethod
    def work_space(value):
        entity_id = getattr(value, "id", None)
        return WorkSpaceExpression(value, "WorkSpace(id={})".format(entity_id))
    @staticmethod
    def work_account(value):
        entity_id = getattr(value, "id", None)
        return WorkAccountExpression(value, "WorkAccount(id={})".format(entity_id))
    @staticmethod
    def work_project(value):
        entity_id = getattr(value, "id", None)
        return WorkProjectExpression(value, "WorkProject(id={})".format(entity_id))
    @staticmethod
    def project_membership(value):
        entity_id = getattr(value, "id", None)
        return ProjectMembershipExpression(value, "ProjectMembership(id={})".format(entity_id))
    @staticmethod
    def project_section(value):
        entity_id = getattr(value, "id", None)
        return ProjectSectionExpression(value, "ProjectSection(id={})".format(entity_id))
    @staticmethod
    def work_task(value):
        entity_id = getattr(value, "id", None)
        return WorkTaskExpression(value, "WorkTask(id={})".format(entity_id))
    @staticmethod
    def project_field(value):
        entity_id = getattr(value, "id", None)
        return ProjectFieldExpression(value, "ProjectField(id={})".format(entity_id))
    @staticmethod
    def field_option(value):
        entity_id = getattr(value, "id", None)
        return FieldOptionExpression(value, "FieldOption(id={})".format(entity_id))
    @staticmethod
    def task_field_choice(value):
        entity_id = getattr(value, "id", None)
        return TaskFieldChoiceExpression(value, "TaskFieldChoice(id={})".format(entity_id))
    @staticmethod
    def work_subtask(value):
        entity_id = getattr(value, "id", None)
        return WorkSubtaskExpression(value, "WorkSubtask(id={})".format(entity_id))
    @staticmethod
    def task_comment(value):
        entity_id = getattr(value, "id", None)
        return TaskCommentExpression(value, "TaskComment(id={})".format(entity_id))
    @staticmethod
    def task_dependency(value):
        entity_id = getattr(value, "id", None)
        return TaskDependencyExpression(value, "TaskDependency(id={})".format(entity_id))
    @staticmethod
    def task_placement(value):
        entity_id = getattr(value, "id", None)
        return TaskPlacementExpression(value, "TaskPlacement(id={})".format(entity_id))
    @staticmethod
    def recurrence_link(value):
        entity_id = getattr(value, "id", None)
        return RecurrenceLinkExpression(value, "RecurrenceLink(id={})".format(entity_id))
    @staticmethod
    def task_event(value):
        entity_id = getattr(value, "id", None)
        return TaskEventExpression(value, "TaskEvent(id={})".format(entity_id))
    @staticmethod
    def task_participant(value):
        entity_id = getattr(value, "id", None)
        return TaskParticipantExpression(value, "TaskParticipant(id={})".format(entity_id))
    @staticmethod
    def deleted_task_viewer(value):
        entity_id = getattr(value, "id", None)
        return DeletedTaskViewerExpression(value, "DeletedTaskViewer(id={})".format(entity_id))
    @staticmethod
    def task_blueprint(value):
        entity_id = getattr(value, "id", None)
        return TaskBlueprintExpression(value, "TaskBlueprint(id={})".format(entity_id))
    @staticmethod
    def blueprint_choice(value):
        entity_id = getattr(value, "id", None)
        return BlueprintChoiceExpression(value, "BlueprintChoice(id={})".format(entity_id))
    @staticmethod
    def blueprint_subtask(value):
        entity_id = getattr(value, "id", None)
        return BlueprintSubtaskExpression(value, "BlueprintSubtask(id={})".format(entity_id))
    @staticmethod
    def inbox_notice(value):
        entity_id = getattr(value, "id", None)
        return InboxNoticeExpression(value, "InboxNotice(id={})".format(entity_id))
    pass