# work-management-service Python API index

Generated from KSML; regenerate when the model changes. Use the canonical names
below, not Python member names or SQL columns, in Assist locations.

Run `cargo teaql --input MODEL TARGET` with the evaluated KSML file or directory.
Entity Query Assist lists fields; field Query Assist gives filters, projections,
ordering, aggregates and relation loading. Write Assist covers creation, changes,
soft deletion and transactions. Listed APIs remain subject to context authorization.

| Entity | Query entry | Query target | Write target |
| --- | --- | --- | --- |
| `work_space` | `Q.work_spaces()` / `Q.work_spaces_minimal()` | `python-assist-query/work_space` | `python-assist-write/work_space` |
| `work_account` | `Q.work_accounts()` / `Q.work_accounts_minimal()` | `python-assist-query/work_account` | `python-assist-write/work_account` |
| `work_project` | `Q.work_projects()` / `Q.work_projects_minimal()` | `python-assist-query/work_project` | `python-assist-write/work_project` |
| `project_membership` | `Q.project_memberships()` / `Q.project_memberships_minimal()` | `python-assist-query/project_membership` | `python-assist-write/project_membership` |
| `project_section` | `Q.project_sections()` / `Q.project_sections_minimal()` | `python-assist-query/project_section` | `python-assist-write/project_section` |
| `work_task` | `Q.work_tasks()` / `Q.work_tasks_minimal()` | `python-assist-query/work_task` | `python-assist-write/work_task` |
| `project_field` | `Q.project_fields()` / `Q.project_fields_minimal()` | `python-assist-query/project_field` | `python-assist-write/project_field` |
| `field_option` | `Q.field_options()` / `Q.field_options_minimal()` | `python-assist-query/field_option` | `python-assist-write/field_option` |
| `task_field_choice` | `Q.task_field_choices()` / `Q.task_field_choices_minimal()` | `python-assist-query/task_field_choice` | `python-assist-write/task_field_choice` |
| `work_subtask` | `Q.work_subtasks()` / `Q.work_subtasks_minimal()` | `python-assist-query/work_subtask` | `python-assist-write/work_subtask` |
| `task_comment` | `Q.task_comments()` / `Q.task_comments_minimal()` | `python-assist-query/task_comment` | `python-assist-write/task_comment` |
| `task_dependency` | `Q.task_dependencies()` / `Q.task_dependencies_minimal()` | `python-assist-query/task_dependency` | `python-assist-write/task_dependency` |
| `task_placement` | `Q.task_placements()` / `Q.task_placements_minimal()` | `python-assist-query/task_placement` | `python-assist-write/task_placement` |
| `recurrence_link` | `Q.recurrence_links()` / `Q.recurrence_links_minimal()` | `python-assist-query/recurrence_link` | `python-assist-write/recurrence_link` |
| `task_event` | `Q.task_events()` / `Q.task_events_minimal()` | `python-assist-query/task_event` | `python-assist-write/task_event` |
| `task_participant` | `Q.task_participants()` / `Q.task_participants_minimal()` | `python-assist-query/task_participant` | `python-assist-write/task_participant` |
| `deleted_task_viewer` | `Q.deleted_task_viewers()` / `Q.deleted_task_viewers_minimal()` | `python-assist-query/deleted_task_viewer` | `python-assist-write/deleted_task_viewer` |
| `task_blueprint` | `Q.task_blueprints()` / `Q.task_blueprints_minimal()` | `python-assist-query/task_blueprint` | `python-assist-write/task_blueprint` |
| `blueprint_choice` | `Q.blueprint_choices()` / `Q.blueprint_choices_minimal()` | `python-assist-query/blueprint_choice` | `python-assist-write/blueprint_choice` |
| `blueprint_subtask` | `Q.blueprint_subtasks()` / `Q.blueprint_subtasks_minimal()` | `python-assist-query/blueprint_subtask` | `python-assist-write/blueprint_subtask` |
| `inbox_notice` | `Q.inbox_notices()` / `Q.inbox_notices_minimal()` | `python-assist-query/inbox_notice` | `python-assist-write/inbox_notice` |

The `_minimal()` entries start with identity/version only; select fields before reading them.
Use each exact Q entry above rather than guessing a plural.

## `work_space`

Request source: [requests/work_space_request.py](requests/work_space_request.py).
`?` marks nullable fields. Examples below show one capability; request field Assist for the full API.

| Field / relation | Type | Filter / select example | Field Assist target |
| --- | --- | --- | --- |
| `id` | `id` | `with_id_is(value)` | `python-assist-query/work_space.id` |
| `workspace_name` | `string` | `with_workspace_name_is(value)` | `python-assist-query/work_space.workspace_name` |
| `version` | `version` | `with_version_is(value)` | `python-assist-query/work_space.version` |
| `work_account_list` (reverse) | `work_account[]` | `select_work_account_list()` | `python-assist-query/work_space.work_account_list` |
| `work_project_list` (reverse) | `work_project[]` | `select_work_project_list()` | `python-assist-query/work_space.work_project_list` |
| `project_membership_list` (reverse) | `project_membership[]` | `select_project_membership_list()` | `python-assist-query/work_space.project_membership_list` |
| `project_section_list` (reverse) | `project_section[]` | `select_project_section_list()` | `python-assist-query/work_space.project_section_list` |
| `work_task_list` (reverse) | `work_task[]` | `select_work_task_list()` | `python-assist-query/work_space.work_task_list` |
| `project_field_list` (reverse) | `project_field[]` | `select_project_field_list()` | `python-assist-query/work_space.project_field_list` |
| `field_option_list` (reverse) | `field_option[]` | `select_field_option_list()` | `python-assist-query/work_space.field_option_list` |
| `task_field_choice_list` (reverse) | `task_field_choice[]` | `select_task_field_choice_list()` | `python-assist-query/work_space.task_field_choice_list` |
| `work_subtask_list` (reverse) | `work_subtask[]` | `select_work_subtask_list()` | `python-assist-query/work_space.work_subtask_list` |
| `task_comment_list` (reverse) | `task_comment[]` | `select_task_comment_list()` | `python-assist-query/work_space.task_comment_list` |
| `task_dependency_list` (reverse) | `task_dependency[]` | `select_task_dependency_list()` | `python-assist-query/work_space.task_dependency_list` |
| `task_placement_list` (reverse) | `task_placement[]` | `select_task_placement_list()` | `python-assist-query/work_space.task_placement_list` |
| `recurrence_link_list` (reverse) | `recurrence_link[]` | `select_recurrence_link_list()` | `python-assist-query/work_space.recurrence_link_list` |
| `task_event_list` (reverse) | `task_event[]` | `select_task_event_list()` | `python-assist-query/work_space.task_event_list` |
| `task_participant_list` (reverse) | `task_participant[]` | `select_task_participant_list()` | `python-assist-query/work_space.task_participant_list` |
| `deleted_task_viewer_list` (reverse) | `deleted_task_viewer[]` | `select_deleted_task_viewer_list()` | `python-assist-query/work_space.deleted_task_viewer_list` |
| `task_blueprint_list` (reverse) | `task_blueprint[]` | `select_task_blueprint_list()` | `python-assist-query/work_space.task_blueprint_list` |
| `blueprint_choice_list` (reverse) | `blueprint_choice[]` | `select_blueprint_choice_list()` | `python-assist-query/work_space.blueprint_choice_list` |
| `blueprint_subtask_list` (reverse) | `blueprint_subtask[]` | `select_blueprint_subtask_list()` | `python-assist-query/work_space.blueprint_subtask_list` |
| `inbox_notice_list` (reverse) | `inbox_notice[]` | `select_inbox_notice_list()` | `python-assist-query/work_space.inbox_notice_list` |

## `work_account`

Request source: [requests/work_account_request.py](requests/work_account_request.py).
`?` marks nullable fields. Examples below show one capability; request field Assist for the full API.

| Field / relation | Type | Filter / select example | Field Assist target |
| --- | --- | --- | --- |
| `id` | `id` | `whose_id_is(value)` | `python-assist-query/work_account.id` |
| `work_space` | `work_space` | `filter_by_work_space(id)` | `python-assist-query/work_account.work_space` |
| `display_name` | `string` | `whose_display_name_is(value)` | `python-assist-query/work_account.display_name` |
| `email_address` | `string` | `whose_email_address_is(value)` | `python-assist-query/work_account.email_address` |
| `password_hash` | `string` | `whose_password_hash_is(value)` | `python-assist-query/work_account.password_hash` |
| `version` | `version` | `whose_version_is(value)` | `python-assist-query/work_account.version` |
| `work_project_list` (reverse) | `work_project[]` | `select_work_project_list()` | `python-assist-query/work_account.work_project_list` |
| `project_membership_list` (reverse) | `project_membership[]` | `select_project_membership_list()` | `python-assist-query/work_account.project_membership_list` |
| `work_task_list_as_created_by` (reverse) | `work_task[]` | `select_work_task_list_as_created_by()` | `python-assist-query/work_account.work_task_list_as_created_by` |
| `work_task_list_as_assignee` (reverse) | `work_task[]` | `select_work_task_list_as_assignee()` | `python-assist-query/work_account.work_task_list_as_assignee` |
| `work_subtask_list` (reverse) | `work_subtask[]` | `select_work_subtask_list()` | `python-assist-query/work_account.work_subtask_list` |
| `task_comment_list` (reverse) | `task_comment[]` | `select_task_comment_list()` | `python-assist-query/work_account.task_comment_list` |
| `task_event_list` (reverse) | `task_event[]` | `select_task_event_list()` | `python-assist-query/work_account.task_event_list` |
| `task_participant_list` (reverse) | `task_participant[]` | `select_task_participant_list()` | `python-assist-query/work_account.task_participant_list` |
| `deleted_task_viewer_list` (reverse) | `deleted_task_viewer[]` | `select_deleted_task_viewer_list()` | `python-assist-query/work_account.deleted_task_viewer_list` |
| `task_blueprint_list` (reverse) | `task_blueprint[]` | `select_task_blueprint_list()` | `python-assist-query/work_account.task_blueprint_list` |
| `blueprint_subtask_list` (reverse) | `blueprint_subtask[]` | `select_blueprint_subtask_list()` | `python-assist-query/work_account.blueprint_subtask_list` |
| `inbox_notice_list` (reverse) | `inbox_notice[]` | `select_inbox_notice_list()` | `python-assist-query/work_account.inbox_notice_list` |

## `work_project`

Request source: [requests/work_project_request.py](requests/work_project_request.py).
`?` marks nullable fields. Examples below show one capability; request field Assist for the full API.

| Field / relation | Type | Filter / select example | Field Assist target |
| --- | --- | --- | --- |
| `id` | `id` | `with_id_is(value)` | `python-assist-query/work_project.id` |
| `work_space` | `work_space` | `filter_by_work_space(id)` | `python-assist-query/work_project.work_space` |
| `owner_account` | `work_account` | `filter_by_owner_account(id)` | `python-assist-query/work_project.owner_account` |
| `project_name` | `string` | `with_project_name_is(value)` | `python-assist-query/work_project.project_name` |
| `shift_dates` | `bool?` | `which_are_shift_dates()` / `which_are_not_shift_dates()` | `python-assist-query/work_project.shift_dates` |
| `version` | `version` | `with_version_is(value)` | `python-assist-query/work_project.version` |
| `project_membership_list` (reverse) | `project_membership[]` | `select_project_membership_list()` | `python-assist-query/work_project.project_membership_list` |
| `project_section_list` (reverse) | `project_section[]` | `select_project_section_list()` | `python-assist-query/work_project.project_section_list` |
| `work_task_list` (reverse) | `work_task[]` | `select_work_task_list()` | `python-assist-query/work_project.work_task_list` |
| `project_field_list` (reverse) | `project_field[]` | `select_project_field_list()` | `python-assist-query/work_project.project_field_list` |
| `task_placement_list` (reverse) | `task_placement[]` | `select_task_placement_list()` | `python-assist-query/work_project.task_placement_list` |
| `task_event_list` (reverse) | `task_event[]` | `select_task_event_list()` | `python-assist-query/work_project.task_event_list` |
| `task_blueprint_list` (reverse) | `task_blueprint[]` | `select_task_blueprint_list()` | `python-assist-query/work_project.task_blueprint_list` |

## `project_membership`

Request source: [requests/project_membership_request.py](requests/project_membership_request.py).
`?` marks nullable fields. Examples below show one capability; request field Assist for the full API.

| Field / relation | Type | Filter / select example | Field Assist target |
| --- | --- | --- | --- |
| `id` | `id` | `with_id_is(value)` | `python-assist-query/project_membership.id` |
| `work_space` | `work_space` | `filter_by_work_space(id)` | `python-assist-query/project_membership.work_space` |
| `project` | `work_project` | `filter_by_project(id)` | `python-assist-query/project_membership.project` |
| `member_account` | `work_account` | `filter_by_member_account(id)` | `python-assist-query/project_membership.member_account` |
| `access_role` | `string?` | `with_access_role_is(value)` | `python-assist-query/project_membership.access_role` |
| `version` | `version` | `with_version_is(value)` | `python-assist-query/project_membership.version` |


## `project_section`

Request source: [requests/project_section_request.py](requests/project_section_request.py).
`?` marks nullable fields. Examples below show one capability; request field Assist for the full API.

| Field / relation | Type | Filter / select example | Field Assist target |
| --- | --- | --- | --- |
| `id` | `id` | `with_id_is(value)` | `python-assist-query/project_section.id` |
| `work_space` | `work_space` | `filter_by_work_space(id)` | `python-assist-query/project_section.work_space` |
| `project` | `work_project` | `filter_by_project(id)` | `python-assist-query/project_section.project` |
| `section_name` | `string` | `with_section_name_is(value)` | `python-assist-query/project_section.section_name` |
| `section_order` | `integer?` | `with_section_order_is(value)` | `python-assist-query/project_section.section_order` |
| `default_section` | `bool` | `which_are_default_section()` / `which_are_not_default_section()` | `python-assist-query/project_section.default_section` |
| `version` | `version` | `with_version_is(value)` | `python-assist-query/project_section.version` |
| `work_task_list` (reverse) | `work_task[]` | `select_work_task_list()` | `python-assist-query/project_section.work_task_list` |
| `task_placement_list` (reverse) | `task_placement[]` | `select_task_placement_list()` | `python-assist-query/project_section.task_placement_list` |

## `work_task`

Request source: [requests/work_task_request.py](requests/work_task_request.py).
`?` marks nullable fields. Examples below show one capability; request field Assist for the full API.

| Field / relation | Type | Filter / select example | Field Assist target |
| --- | --- | --- | --- |
| `id` | `id` | `with_id_is(value)` | `python-assist-query/work_task.id` |
| `work_space` | `work_space` | `filter_by_work_space(id)` | `python-assist-query/work_task.work_space` |
| `project` | `work_project` | `filter_by_project(id)` | `python-assist-query/work_task.project` |
| `section` | `project_section` | `filter_by_section(id)` | `python-assist-query/work_task.section` |
| `deleted_epoch` | `integer?` | `with_deleted_epoch_is(value)` | `python-assist-query/work_task.deleted_epoch` |
| `approval` | `bool?` | `which_are_approval()` / `which_are_not_approval()` | `python-assist-query/work_task.approval` |
| `decision` | `string?` | `with_decision_is(value)` | `python-assist-query/work_task.decision` |
| `repeat_period` | `string?` | `with_repeat_period_is(value)` | `python-assist-query/work_task.repeat_period` |
| `created_by` | `work_account?` | `filter_by_created_by(id)` | `python-assist-query/work_task.created_by` |
| `primary_detached` | `bool?` | `which_are_primary_detached()` / `which_are_not_primary_detached()` | `python-assist-query/work_task.primary_detached` |
| `task_order` | `integer?` | `with_task_order_is(value)` | `python-assist-query/work_task.task_order` |
| `task_title` | `string` | `with_task_title_is(value)` | `python-assist-query/work_task.task_title` |
| `description` | `string?` | `with_description_is(value)` | `python-assist-query/work_task.description` |
| `assignee` | `work_account?` | `filter_by_assignee(id)` | `python-assist-query/work_task.assignee` |
| `start_date` | `date?` | `with_start_date_is(value)` | `python-assist-query/work_task.start_date` |
| `due_date` | `date?` | `with_due_date_is(value)` | `python-assist-query/work_task.due_date` |
| `completed` | `bool` | `which_are_completed()` / `which_are_not_completed()` | `python-assist-query/work_task.completed` |
| `version` | `version` | `with_version_is(value)` | `python-assist-query/work_task.version` |
| `task_field_choice_list` (reverse) | `task_field_choice[]` | `select_task_field_choice_list()` | `python-assist-query/work_task.task_field_choice_list` |
| `work_subtask_list` (reverse) | `work_subtask[]` | `select_work_subtask_list()` | `python-assist-query/work_task.work_subtask_list` |
| `task_comment_list` (reverse) | `task_comment[]` | `select_task_comment_list()` | `python-assist-query/work_task.task_comment_list` |
| `task_dependency_list_as_dependent` (reverse) | `task_dependency[]` | `select_task_dependency_list_as_dependent()` | `python-assist-query/work_task.task_dependency_list_as_dependent` |
| `task_dependency_list_as_blocker` (reverse) | `task_dependency[]` | `select_task_dependency_list_as_blocker()` | `python-assist-query/work_task.task_dependency_list_as_blocker` |
| `task_placement_list` (reverse) | `task_placement[]` | `select_task_placement_list()` | `python-assist-query/work_task.task_placement_list` |
| `recurrence_link_list_as_source_task` (reverse) | `recurrence_link[]` | `select_recurrence_link_list_as_source_task()` | `python-assist-query/work_task.recurrence_link_list_as_source_task` |
| `recurrence_link_list_as_next_task` (reverse) | `recurrence_link[]` | `select_recurrence_link_list_as_next_task()` | `python-assist-query/work_task.recurrence_link_list_as_next_task` |
| `task_event_list_as_task` (reverse) | `task_event[]` | `select_task_event_list_as_task()` | `python-assist-query/work_task.task_event_list_as_task` |
| `task_event_list_as_related_task` (reverse) | `task_event[]` | `select_task_event_list_as_related_task()` | `python-assist-query/work_task.task_event_list_as_related_task` |
| `task_participant_list` (reverse) | `task_participant[]` | `select_task_participant_list()` | `python-assist-query/work_task.task_participant_list` |
| `deleted_task_viewer_list` (reverse) | `deleted_task_viewer[]` | `select_deleted_task_viewer_list()` | `python-assist-query/work_task.deleted_task_viewer_list` |
| `inbox_notice_list` (reverse) | `inbox_notice[]` | `select_inbox_notice_list()` | `python-assist-query/work_task.inbox_notice_list` |

## `project_field`

Request source: [requests/project_field_request.py](requests/project_field_request.py).
`?` marks nullable fields. Examples below show one capability; request field Assist for the full API.

| Field / relation | Type | Filter / select example | Field Assist target |
| --- | --- | --- | --- |
| `id` | `id` | `with_id_is(value)` | `python-assist-query/project_field.id` |
| `work_space` | `work_space` | `filter_by_work_space(id)` | `python-assist-query/project_field.work_space` |
| `project` | `work_project` | `filter_by_project(id)` | `python-assist-query/project_field.project` |
| `field_name` | `string` | `with_field_name_is(value)` | `python-assist-query/project_field.field_name` |
| `version` | `version` | `with_version_is(value)` | `python-assist-query/project_field.version` |
| `field_option_list` (reverse) | `field_option[]` | `select_field_option_list()` | `python-assist-query/project_field.field_option_list` |
| `task_field_choice_list` (reverse) | `task_field_choice[]` | `select_task_field_choice_list()` | `python-assist-query/project_field.task_field_choice_list` |
| `blueprint_choice_list` (reverse) | `blueprint_choice[]` | `select_blueprint_choice_list()` | `python-assist-query/project_field.blueprint_choice_list` |

## `field_option`

Request source: [requests/field_option_request.py](requests/field_option_request.py).
`?` marks nullable fields. Examples below show one capability; request field Assist for the full API.

| Field / relation | Type | Filter / select example | Field Assist target |
| --- | --- | --- | --- |
| `id` | `id` | `with_id_is(value)` | `python-assist-query/field_option.id` |
| `work_space` | `work_space` | `filter_by_work_space(id)` | `python-assist-query/field_option.work_space` |
| `field` | `project_field` | `filter_by_field(id)` | `python-assist-query/field_option.field` |
| `option_name` | `string` | `with_option_name_is(value)` | `python-assist-query/field_option.option_name` |
| `option_order` | `integer` | `with_option_order_is(value)` | `python-assist-query/field_option.option_order` |
| `version` | `version` | `with_version_is(value)` | `python-assist-query/field_option.version` |
| `task_field_choice_list` (reverse) | `task_field_choice[]` | `select_task_field_choice_list()` | `python-assist-query/field_option.task_field_choice_list` |
| `blueprint_choice_list` (reverse) | `blueprint_choice[]` | `select_blueprint_choice_list()` | `python-assist-query/field_option.blueprint_choice_list` |

## `task_field_choice`

Request source: [requests/task_field_choice_request.py](requests/task_field_choice_request.py).
`?` marks nullable fields. Examples below show one capability; request field Assist for the full API.

| Field / relation | Type | Filter / select example | Field Assist target |
| --- | --- | --- | --- |
| `id` | `id` | `with_id_is(value)` | `python-assist-query/task_field_choice.id` |
| `work_space` | `work_space` | `filter_by_work_space(id)` | `python-assist-query/task_field_choice.work_space` |
| `task` | `work_task` | `filter_by_task(id)` | `python-assist-query/task_field_choice.task` |
| `field` | `project_field` | `filter_by_field(id)` | `python-assist-query/task_field_choice.field` |
| `selected_option` | `field_option` | `filter_by_selected_option(id)` | `python-assist-query/task_field_choice.selected_option` |
| `version` | `version` | `with_version_is(value)` | `python-assist-query/task_field_choice.version` |


## `work_subtask`

Request source: [requests/work_subtask_request.py](requests/work_subtask_request.py).
`?` marks nullable fields. Examples below show one capability; request field Assist for the full API.

| Field / relation | Type | Filter / select example | Field Assist target |
| --- | --- | --- | --- |
| `id` | `id` | `with_id_is(value)` | `python-assist-query/work_subtask.id` |
| `work_space` | `work_space` | `filter_by_work_space(id)` | `python-assist-query/work_subtask.work_space` |
| `task` | `work_task` | `filter_by_task(id)` | `python-assist-query/work_subtask.task` |
| `subtask_title` | `string` | `with_subtask_title_is(value)` | `python-assist-query/work_subtask.subtask_title` |
| `assignee` | `work_account?` | `filter_by_assignee(id)` | `python-assist-query/work_subtask.assignee` |
| `due_date` | `date?` | `with_due_date_is(value)` | `python-assist-query/work_subtask.due_date` |
| `completed` | `bool` | `which_are_completed()` / `which_are_not_completed()` | `python-assist-query/work_subtask.completed` |
| `version` | `version` | `with_version_is(value)` | `python-assist-query/work_subtask.version` |


## `task_comment`

Request source: [requests/task_comment_request.py](requests/task_comment_request.py).
`?` marks nullable fields. Examples below show one capability; request field Assist for the full API.

| Field / relation | Type | Filter / select example | Field Assist target |
| --- | --- | --- | --- |
| `id` | `id` | `with_id_is(value)` | `python-assist-query/task_comment.id` |
| `work_space` | `work_space` | `filter_by_work_space(id)` | `python-assist-query/task_comment.work_space` |
| `task` | `work_task` | `filter_by_task(id)` | `python-assist-query/task_comment.task` |
| `author` | `work_account` | `filter_by_author(id)` | `python-assist-query/task_comment.author` |
| `comment_text` | `string` | `with_comment_text_is(value)` | `python-assist-query/task_comment.comment_text` |
| `edited` | `bool` | `which_are_edited()` / `which_are_not_edited()` | `python-assist-query/task_comment.edited` |
| `create_time` | `createTime` | `with_create_time_is(value)` | `python-assist-query/task_comment.create_time` |
| `version` | `version` | `with_version_is(value)` | `python-assist-query/task_comment.version` |


## `task_dependency`

Request source: [requests/task_dependency_request.py](requests/task_dependency_request.py).
`?` marks nullable fields. Examples below show one capability; request field Assist for the full API.

| Field / relation | Type | Filter / select example | Field Assist target |
| --- | --- | --- | --- |
| `id` | `id` | `with_id_is(value)` | `python-assist-query/task_dependency.id` |
| `work_space` | `work_space` | `filter_by_work_space(id)` | `python-assist-query/task_dependency.work_space` |
| `dependent` | `work_task` | `filter_by_dependent(id)` | `python-assist-query/task_dependency.dependent` |
| `blocker` | `work_task` | `filter_by_blocker(id)` | `python-assist-query/task_dependency.blocker` |
| `version` | `version` | `with_version_is(value)` | `python-assist-query/task_dependency.version` |


## `task_placement`

Request source: [requests/task_placement_request.py](requests/task_placement_request.py).
`?` marks nullable fields. Examples below show one capability; request field Assist for the full API.

| Field / relation | Type | Filter / select example | Field Assist target |
| --- | --- | --- | --- |
| `id` | `id` | `with_id_is(value)` | `python-assist-query/task_placement.id` |
| `work_space` | `work_space` | `filter_by_work_space(id)` | `python-assist-query/task_placement.work_space` |
| `task` | `work_task` | `filter_by_task(id)` | `python-assist-query/task_placement.task` |
| `project` | `work_project` | `filter_by_project(id)` | `python-assist-query/task_placement.project` |
| `section` | `project_section` | `filter_by_section(id)` | `python-assist-query/task_placement.section` |
| `placement_order` | `integer` | `with_placement_order_is(value)` | `python-assist-query/task_placement.placement_order` |
| `version` | `version` | `with_version_is(value)` | `python-assist-query/task_placement.version` |


## `recurrence_link`

Request source: [requests/recurrence_link_request.py](requests/recurrence_link_request.py).
`?` marks nullable fields. Examples below show one capability; request field Assist for the full API.

| Field / relation | Type | Filter / select example | Field Assist target |
| --- | --- | --- | --- |
| `id` | `id` | `with_id_is(value)` | `python-assist-query/recurrence_link.id` |
| `work_space` | `work_space` | `filter_by_work_space(id)` | `python-assist-query/recurrence_link.work_space` |
| `source_task` | `work_task` | `filter_by_source_task(id)` | `python-assist-query/recurrence_link.source_task` |
| `next_task` | `work_task` | `filter_by_next_task(id)` | `python-assist-query/recurrence_link.next_task` |
| `version` | `version` | `with_version_is(value)` | `python-assist-query/recurrence_link.version` |


## `task_event`

Request source: [requests/task_event_request.py](requests/task_event_request.py).
`?` marks nullable fields. Examples below show one capability; request field Assist for the full API.

| Field / relation | Type | Filter / select example | Field Assist target |
| --- | --- | --- | --- |
| `id` | `id` | `with_id_is(value)` | `python-assist-query/task_event.id` |
| `work_space` | `work_space` | `filter_by_work_space(id)` | `python-assist-query/task_event.work_space` |
| `task` | `work_task` | `filter_by_task(id)` | `python-assist-query/task_event.task` |
| `actor` | `work_account` | `filter_by_actor(id)` | `python-assist-query/task_event.actor` |
| `scope_project` | `work_project?` | `filter_by_scope_project(id)` | `python-assist-query/task_event.scope_project` |
| `related_task` | `work_task?` | `filter_by_related_task(id)` | `python-assist-query/task_event.related_task` |
| `event_kind` | `string` | `with_event_kind_is(value)` | `python-assist-query/task_event.event_kind` |
| `field_label` | `string` | `with_field_label_is(value)` | `python-assist-query/task_event.field_label` |
| `old_value` | `string?` | `with_old_value_is(value)` | `python-assist-query/task_event.old_value` |
| `new_value` | `string?` | `with_new_value_is(value)` | `python-assist-query/task_event.new_value` |
| `event_time` | `createTime` | `with_event_time_is(value)` | `python-assist-query/task_event.event_time` |
| `version` | `version` | `with_version_is(value)` | `python-assist-query/task_event.version` |
| `inbox_notice_list` (reverse) | `inbox_notice[]` | `select_inbox_notice_list()` | `python-assist-query/task_event.inbox_notice_list` |

## `task_participant`

Request source: [requests/task_participant_request.py](requests/task_participant_request.py).
`?` marks nullable fields. Examples below show one capability; request field Assist for the full API.

| Field / relation | Type | Filter / select example | Field Assist target |
| --- | --- | --- | --- |
| `id` | `id` | `with_id_is(value)` | `python-assist-query/task_participant.id` |
| `work_space` | `work_space` | `filter_by_work_space(id)` | `python-assist-query/task_participant.work_space` |
| `task` | `work_task` | `filter_by_task(id)` | `python-assist-query/task_participant.task` |
| `participant` | `work_account` | `filter_by_participant(id)` | `python-assist-query/task_participant.participant` |
| `version` | `version` | `with_version_is(value)` | `python-assist-query/task_participant.version` |


## `deleted_task_viewer`

Request source: [requests/deleted_task_viewer_request.py](requests/deleted_task_viewer_request.py).
`?` marks nullable fields. Examples below show one capability; request field Assist for the full API.

| Field / relation | Type | Filter / select example | Field Assist target |
| --- | --- | --- | --- |
| `id` | `id` | `with_id_is(value)` | `python-assist-query/deleted_task_viewer.id` |
| `work_space` | `work_space` | `filter_by_work_space(id)` | `python-assist-query/deleted_task_viewer.work_space` |
| `task` | `work_task` | `filter_by_task(id)` | `python-assist-query/deleted_task_viewer.task` |
| `viewer` | `work_account` | `filter_by_viewer(id)` | `python-assist-query/deleted_task_viewer.viewer` |
| `version` | `version` | `with_version_is(value)` | `python-assist-query/deleted_task_viewer.version` |


## `task_blueprint`

Request source: [requests/task_blueprint_request.py](requests/task_blueprint_request.py).
`?` marks nullable fields. Examples below show one capability; request field Assist for the full API.

| Field / relation | Type | Filter / select example | Field Assist target |
| --- | --- | --- | --- |
| `id` | `id` | `with_id_is(value)` | `python-assist-query/task_blueprint.id` |
| `work_space` | `work_space` | `filter_by_work_space(id)` | `python-assist-query/task_blueprint.work_space` |
| `project` | `work_project` | `filter_by_project(id)` | `python-assist-query/task_blueprint.project` |
| `template_name` | `string` | `with_template_name_is(value)` | `python-assist-query/task_blueprint.template_name` |
| `initial_title` | `string` | `with_initial_title_is(value)` | `python-assist-query/task_blueprint.initial_title` |
| `initial_description` | `string?` | `with_initial_description_is(value)` | `python-assist-query/task_blueprint.initial_description` |
| `assignee` | `work_account?` | `filter_by_assignee(id)` | `python-assist-query/task_blueprint.assignee` |
| `due_offset` | `integer?` | `with_due_offset_is(value)` | `python-assist-query/task_blueprint.due_offset` |
| `repeat_period` | `string` | `with_repeat_period_is(value)` | `python-assist-query/task_blueprint.repeat_period` |
| `approval` | `bool` | `which_are_approval()` / `which_are_not_approval()` | `python-assist-query/task_blueprint.approval` |
| `version` | `version` | `with_version_is(value)` | `python-assist-query/task_blueprint.version` |
| `blueprint_choice_list` (reverse) | `blueprint_choice[]` | `select_blueprint_choice_list()` | `python-assist-query/task_blueprint.blueprint_choice_list` |
| `blueprint_subtask_list` (reverse) | `blueprint_subtask[]` | `select_blueprint_subtask_list()` | `python-assist-query/task_blueprint.blueprint_subtask_list` |

## `blueprint_choice`

Request source: [requests/blueprint_choice_request.py](requests/blueprint_choice_request.py).
`?` marks nullable fields. Examples below show one capability; request field Assist for the full API.

| Field / relation | Type | Filter / select example | Field Assist target |
| --- | --- | --- | --- |
| `id` | `id` | `with_id_is(value)` | `python-assist-query/blueprint_choice.id` |
| `work_space` | `work_space` | `filter_by_work_space(id)` | `python-assist-query/blueprint_choice.work_space` |
| `blueprint` | `task_blueprint` | `filter_by_blueprint(id)` | `python-assist-query/blueprint_choice.blueprint` |
| `field` | `project_field` | `filter_by_field(id)` | `python-assist-query/blueprint_choice.field` |
| `selected_option` | `field_option` | `filter_by_selected_option(id)` | `python-assist-query/blueprint_choice.selected_option` |
| `version` | `version` | `with_version_is(value)` | `python-assist-query/blueprint_choice.version` |


## `blueprint_subtask`

Request source: [requests/blueprint_subtask_request.py](requests/blueprint_subtask_request.py).
`?` marks nullable fields. Examples below show one capability; request field Assist for the full API.

| Field / relation | Type | Filter / select example | Field Assist target |
| --- | --- | --- | --- |
| `id` | `id` | `with_id_is(value)` | `python-assist-query/blueprint_subtask.id` |
| `work_space` | `work_space` | `filter_by_work_space(id)` | `python-assist-query/blueprint_subtask.work_space` |
| `blueprint` | `task_blueprint` | `filter_by_blueprint(id)` | `python-assist-query/blueprint_subtask.blueprint` |
| `subtask_title` | `string` | `with_subtask_title_is(value)` | `python-assist-query/blueprint_subtask.subtask_title` |
| `assignee` | `work_account?` | `filter_by_assignee(id)` | `python-assist-query/blueprint_subtask.assignee` |
| `due_offset` | `integer?` | `with_due_offset_is(value)` | `python-assist-query/blueprint_subtask.due_offset` |
| `version` | `version` | `with_version_is(value)` | `python-assist-query/blueprint_subtask.version` |


## `inbox_notice`

Request source: [requests/inbox_notice_request.py](requests/inbox_notice_request.py).
`?` marks nullable fields. Examples below show one capability; request field Assist for the full API.

| Field / relation | Type | Filter / select example | Field Assist target |
| --- | --- | --- | --- |
| `id` | `id` | `with_id_is(value)` | `python-assist-query/inbox_notice.id` |
| `work_space` | `work_space` | `filter_by_work_space(id)` | `python-assist-query/inbox_notice.work_space` |
| `task` | `work_task` | `filter_by_task(id)` | `python-assist-query/inbox_notice.task` |
| `recipient` | `work_account` | `filter_by_recipient(id)` | `python-assist-query/inbox_notice.recipient` |
| `event` | `task_event` | `filter_by_event(id)` | `python-assist-query/inbox_notice.event` |
| `read_flag` | `bool` | `which_are_read_flag()` / `which_are_not_read_flag()` | `python-assist-query/inbox_notice.read_flag` |
| `version` | `version` | `with_version_is(value)` | `python-assist-query/inbox_notice.version` |
