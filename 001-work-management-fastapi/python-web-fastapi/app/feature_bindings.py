"""Generated capability bindings; names and APIs come from KSML."""
import json
from Q import Q

SCHEMA = json.loads("{\"root_type\":\"WorkSpace\",\"primary\":\"\",\"account\":\"work_account\",\"owner\":\"\",\"account_name_member\":\"displayName\",\"entities\":{\"work_account\":{\"name\":\"work_account\",\"label\":\"Account\",\"primary\":false,\"enabled\":false,\"editable\":[],\"container\":\"\",\"authorization\":\"\",\"create_handler\":\"\",\"title\":\"display_name\",\"root\":\"work_space\",\"group\":\"\",\"group_query\":\"\",\"candidates\":{},\"multiline\":[],\"defaults\":{},\"date_orders\":[],\"fields\":[{\"name\":\"id\",\"member\":\"id\",\"label\":\"Id\",\"kind\":\"unsupported\",\"nullable\":false,\"managed\":true,\"context_root\":false,\"target\":\"\"},{\"name\":\"work_space\",\"member\":\"workSpace\",\"label\":\"Work Space\",\"kind\":\"reference\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"work_space\"},{\"name\":\"display_name\",\"member\":\"displayName\",\"label\":\"Display Name\",\"kind\":\"text\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"\"},{\"name\":\"email_address\",\"member\":\"emailAddress\",\"label\":\"Email Address\",\"kind\":\"text\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"\"},{\"name\":\"password_hash\",\"member\":\"passwordHash\",\"label\":\"Password Hash\",\"kind\":\"text\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"\"},{\"name\":\"version\",\"member\":\"version\",\"label\":\"Version\",\"kind\":\"unsupported\",\"nullable\":false,\"managed\":true,\"context_root\":false,\"target\":\"\"}],\"application_required\":[\"display_name\",\"email_address\",\"password_hash\"]},\"work_project\":{\"name\":\"work_project\",\"label\":\"Project\",\"primary\":false,\"enabled\":true,\"editable\":[\"project_name\"],\"container\":\"\",\"authorization\":\"project_access\",\"create_handler\":\"initialize_project\",\"title\":\"project_name\",\"root\":\"work_space\",\"group\":\"\",\"group_query\":\"\",\"candidates\":{},\"multiline\":[],\"defaults\":{},\"date_orders\":[],\"fields\":[{\"name\":\"id\",\"member\":\"id\",\"label\":\"Id\",\"kind\":\"unsupported\",\"nullable\":false,\"managed\":true,\"context_root\":false,\"target\":\"\"},{\"name\":\"work_space\",\"member\":\"workSpace\",\"label\":\"Work Space\",\"kind\":\"reference\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"work_space\"},{\"name\":\"owner_account\",\"member\":\"ownerAccount\",\"label\":\"Owner Account\",\"kind\":\"reference\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"work_account\"},{\"name\":\"project_name\",\"member\":\"projectName\",\"label\":\"Project Name\",\"kind\":\"text\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"\"},{\"name\":\"shift_dates\",\"member\":\"shiftDates\",\"label\":\"Shift Dates\",\"kind\":\"boolean\",\"nullable\":true,\"managed\":false,\"context_root\":false,\"target\":\"\"},{\"name\":\"version\",\"member\":\"version\",\"label\":\"Version\",\"kind\":\"unsupported\",\"nullable\":false,\"managed\":true,\"context_root\":false,\"target\":\"\"}],\"application_required\":[\"owner_account\"]},\"project_membership\":{\"name\":\"project_membership\",\"label\":\"Membership\",\"primary\":false,\"enabled\":false,\"editable\":[],\"container\":\"project\",\"authorization\":\"\",\"create_handler\":\"\",\"title\":\"access_role\",\"root\":\"work_space\",\"group\":\"\",\"group_query\":\"\",\"candidates\":{},\"multiline\":[],\"defaults\":{},\"date_orders\":[],\"fields\":[{\"name\":\"id\",\"member\":\"id\",\"label\":\"Id\",\"kind\":\"unsupported\",\"nullable\":false,\"managed\":true,\"context_root\":false,\"target\":\"\"},{\"name\":\"work_space\",\"member\":\"workSpace\",\"label\":\"Work Space\",\"kind\":\"reference\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"work_space\"},{\"name\":\"project\",\"member\":\"project\",\"label\":\"Project\",\"kind\":\"reference\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"work_project\"},{\"name\":\"member_account\",\"member\":\"memberAccount\",\"label\":\"Member Account\",\"kind\":\"reference\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"work_account\"},{\"name\":\"access_role\",\"member\":\"accessRole\",\"label\":\"Access Role\",\"kind\":\"text\",\"nullable\":true,\"managed\":false,\"context_root\":false,\"target\":\"\"},{\"name\":\"version\",\"member\":\"version\",\"label\":\"Version\",\"kind\":\"unsupported\",\"nullable\":false,\"managed\":true,\"context_root\":false,\"target\":\"\"}],\"application_required\":[\"member_account\"]},\"project_section\":{\"name\":\"project_section\",\"label\":\"Section\",\"primary\":false,\"enabled\":false,\"editable\":[],\"container\":\"project\",\"authorization\":\"\",\"create_handler\":\"\",\"title\":\"section_name\",\"root\":\"work_space\",\"group\":\"\",\"group_query\":\"\",\"candidates\":{},\"multiline\":[],\"defaults\":{},\"date_orders\":[],\"fields\":[{\"name\":\"id\",\"member\":\"id\",\"label\":\"Id\",\"kind\":\"unsupported\",\"nullable\":false,\"managed\":true,\"context_root\":false,\"target\":\"\"},{\"name\":\"work_space\",\"member\":\"workSpace\",\"label\":\"Work Space\",\"kind\":\"reference\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"work_space\"},{\"name\":\"project\",\"member\":\"project\",\"label\":\"Project\",\"kind\":\"reference\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"work_project\"},{\"name\":\"section_name\",\"member\":\"sectionName\",\"label\":\"Section Name\",\"kind\":\"text\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"\"},{\"name\":\"section_order\",\"member\":\"sectionOrder\",\"label\":\"Section Order\",\"kind\":\"number\",\"nullable\":true,\"managed\":false,\"context_root\":false,\"target\":\"\"},{\"name\":\"default_section\",\"member\":\"defaultSection\",\"label\":\"Default Section\",\"kind\":\"boolean\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"\"},{\"name\":\"version\",\"member\":\"version\",\"label\":\"Version\",\"kind\":\"unsupported\",\"nullable\":false,\"managed\":true,\"context_root\":false,\"target\":\"\"}],\"application_required\":[\"section_name\",\"default_section\"]},\"work_task\":{\"name\":\"work_task\",\"label\":\"Task\",\"primary\":false,\"enabled\":true,\"editable\":[\"task_title\",\"description\",\"assignee\",\"start_date\",\"due_date\",\"completed\",\"approval\",\"repeat_period\"],\"container\":\"project\",\"authorization\":\"task_access\",\"create_handler\":\"place_task\",\"title\":\"task_title\",\"root\":\"work_space\",\"group\":\"section\",\"group_query\":\"project_sections\",\"candidates\":{\"assignee\":\"project_accounts\"},\"multiline\":[\"description\"],\"defaults\":{\"completed\":false,\"repeat_period\":\"none\"},\"date_orders\":[[\"start_date\",\"due_date\"]],\"fields\":[{\"name\":\"id\",\"member\":\"id\",\"label\":\"Id\",\"kind\":\"unsupported\",\"nullable\":false,\"managed\":true,\"context_root\":false,\"target\":\"\"},{\"name\":\"work_space\",\"member\":\"workSpace\",\"label\":\"Work Space\",\"kind\":\"reference\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"work_space\"},{\"name\":\"project\",\"member\":\"project\",\"label\":\"Project\",\"kind\":\"reference\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"work_project\"},{\"name\":\"section\",\"member\":\"section\",\"label\":\"Section\",\"kind\":\"reference\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"project_section\"},{\"name\":\"deleted_epoch\",\"member\":\"deletedEpoch\",\"label\":\"Deleted Epoch\",\"kind\":\"number\",\"nullable\":true,\"managed\":false,\"context_root\":false,\"target\":\"\"},{\"name\":\"approval\",\"member\":\"approval\",\"label\":\"Approval\",\"kind\":\"boolean\",\"nullable\":true,\"managed\":false,\"context_root\":false,\"target\":\"\"},{\"name\":\"decision\",\"member\":\"decision\",\"label\":\"Decision\",\"kind\":\"text\",\"nullable\":true,\"managed\":false,\"context_root\":false,\"target\":\"\"},{\"name\":\"repeat_period\",\"member\":\"repeatPeriod\",\"label\":\"Repeat Period\",\"kind\":\"text\",\"nullable\":true,\"managed\":false,\"context_root\":false,\"target\":\"\"},{\"name\":\"created_by\",\"member\":\"createdBy\",\"label\":\"Created By\",\"kind\":\"reference\",\"nullable\":true,\"managed\":false,\"context_root\":false,\"target\":\"work_account\"},{\"name\":\"primary_detached\",\"member\":\"primaryDetached\",\"label\":\"Primary Detached\",\"kind\":\"boolean\",\"nullable\":true,\"managed\":false,\"context_root\":false,\"target\":\"\"},{\"name\":\"task_order\",\"member\":\"taskOrder\",\"label\":\"Task Order\",\"kind\":\"number\",\"nullable\":true,\"managed\":false,\"context_root\":false,\"target\":\"\"},{\"name\":\"task_title\",\"member\":\"taskTitle\",\"label\":\"Task Title\",\"kind\":\"text\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"\"},{\"name\":\"description\",\"member\":\"description\",\"label\":\"Description\",\"kind\":\"text\",\"nullable\":true,\"managed\":false,\"context_root\":false,\"target\":\"\"},{\"name\":\"assignee\",\"member\":\"assignee\",\"label\":\"Assignee\",\"kind\":\"reference\",\"nullable\":true,\"managed\":false,\"context_root\":false,\"target\":\"work_account\"},{\"name\":\"start_date\",\"member\":\"startDate\",\"label\":\"Start Date\",\"kind\":\"date\",\"nullable\":true,\"managed\":false,\"context_root\":false,\"target\":\"\"},{\"name\":\"due_date\",\"member\":\"dueDate\",\"label\":\"Due Date\",\"kind\":\"date\",\"nullable\":true,\"managed\":false,\"context_root\":false,\"target\":\"\"},{\"name\":\"completed\",\"member\":\"completed\",\"label\":\"Completed\",\"kind\":\"boolean\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"\"},{\"name\":\"version\",\"member\":\"version\",\"label\":\"Version\",\"kind\":\"unsupported\",\"nullable\":false,\"managed\":true,\"context_root\":false,\"target\":\"\"}],\"application_required\":[\"section\"]},\"project_field\":{\"name\":\"project_field\",\"label\":\"Project field\",\"primary\":false,\"enabled\":false,\"editable\":[],\"container\":\"project\",\"authorization\":\"\",\"create_handler\":\"\",\"title\":\"field_name\",\"root\":\"work_space\",\"group\":\"\",\"group_query\":\"\",\"candidates\":{},\"multiline\":[],\"defaults\":{},\"date_orders\":[],\"fields\":[{\"name\":\"id\",\"member\":\"id\",\"label\":\"Id\",\"kind\":\"unsupported\",\"nullable\":false,\"managed\":true,\"context_root\":false,\"target\":\"\"},{\"name\":\"work_space\",\"member\":\"workSpace\",\"label\":\"Work Space\",\"kind\":\"reference\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"work_space\"},{\"name\":\"project\",\"member\":\"project\",\"label\":\"Project\",\"kind\":\"reference\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"work_project\"},{\"name\":\"field_name\",\"member\":\"fieldName\",\"label\":\"Field Name\",\"kind\":\"text\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"\"},{\"name\":\"version\",\"member\":\"version\",\"label\":\"Version\",\"kind\":\"unsupported\",\"nullable\":false,\"managed\":true,\"context_root\":false,\"target\":\"\"}],\"application_required\":[\"field_name\"]},\"field_option\":{\"name\":\"field_option\",\"label\":\"Field option\",\"primary\":false,\"enabled\":false,\"editable\":[],\"container\":\"field\",\"authorization\":\"\",\"create_handler\":\"\",\"title\":\"option_name\",\"root\":\"work_space\",\"group\":\"\",\"group_query\":\"\",\"candidates\":{},\"multiline\":[],\"defaults\":{},\"date_orders\":[],\"fields\":[{\"name\":\"id\",\"member\":\"id\",\"label\":\"Id\",\"kind\":\"unsupported\",\"nullable\":false,\"managed\":true,\"context_root\":false,\"target\":\"\"},{\"name\":\"work_space\",\"member\":\"workSpace\",\"label\":\"Work Space\",\"kind\":\"reference\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"work_space\"},{\"name\":\"field\",\"member\":\"field\",\"label\":\"Field\",\"kind\":\"reference\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"project_field\"},{\"name\":\"option_name\",\"member\":\"optionName\",\"label\":\"Option Name\",\"kind\":\"text\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"\"},{\"name\":\"option_order\",\"member\":\"optionOrder\",\"label\":\"Option Order\",\"kind\":\"number\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"\"},{\"name\":\"version\",\"member\":\"version\",\"label\":\"Version\",\"kind\":\"unsupported\",\"nullable\":false,\"managed\":true,\"context_root\":false,\"target\":\"\"}],\"application_required\":[\"option_name\",\"option_order\"]},\"task_field_choice\":{\"name\":\"task_field_choice\",\"label\":\"Task field value\",\"primary\":false,\"enabled\":false,\"editable\":[],\"container\":\"task\",\"authorization\":\"\",\"create_handler\":\"\",\"title\":\"id\",\"root\":\"work_space\",\"group\":\"\",\"group_query\":\"\",\"candidates\":{},\"multiline\":[],\"defaults\":{},\"date_orders\":[],\"fields\":[{\"name\":\"id\",\"member\":\"id\",\"label\":\"Id\",\"kind\":\"unsupported\",\"nullable\":false,\"managed\":true,\"context_root\":false,\"target\":\"\"},{\"name\":\"work_space\",\"member\":\"workSpace\",\"label\":\"Work Space\",\"kind\":\"reference\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"work_space\"},{\"name\":\"task\",\"member\":\"task\",\"label\":\"Task\",\"kind\":\"reference\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"work_task\"},{\"name\":\"field\",\"member\":\"field\",\"label\":\"Field\",\"kind\":\"reference\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"project_field\"},{\"name\":\"selected_option\",\"member\":\"selectedOption\",\"label\":\"Selected Option\",\"kind\":\"reference\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"field_option\"},{\"name\":\"version\",\"member\":\"version\",\"label\":\"Version\",\"kind\":\"unsupported\",\"nullable\":false,\"managed\":true,\"context_root\":false,\"target\":\"\"}],\"application_required\":[\"field\",\"selected_option\"]},\"work_subtask\":{\"name\":\"work_subtask\",\"label\":\"Subtask\",\"primary\":false,\"enabled\":false,\"editable\":[],\"container\":\"task\",\"authorization\":\"\",\"create_handler\":\"\",\"title\":\"subtask_title\",\"root\":\"work_space\",\"group\":\"\",\"group_query\":\"\",\"candidates\":{},\"multiline\":[],\"defaults\":{},\"date_orders\":[],\"fields\":[{\"name\":\"id\",\"member\":\"id\",\"label\":\"Id\",\"kind\":\"unsupported\",\"nullable\":false,\"managed\":true,\"context_root\":false,\"target\":\"\"},{\"name\":\"work_space\",\"member\":\"workSpace\",\"label\":\"Work Space\",\"kind\":\"reference\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"work_space\"},{\"name\":\"task\",\"member\":\"task\",\"label\":\"Task\",\"kind\":\"reference\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"work_task\"},{\"name\":\"subtask_title\",\"member\":\"subtaskTitle\",\"label\":\"Subtask Title\",\"kind\":\"text\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"\"},{\"name\":\"assignee\",\"member\":\"assignee\",\"label\":\"Assignee\",\"kind\":\"reference\",\"nullable\":true,\"managed\":false,\"context_root\":false,\"target\":\"work_account\"},{\"name\":\"due_date\",\"member\":\"dueDate\",\"label\":\"Due Date\",\"kind\":\"date\",\"nullable\":true,\"managed\":false,\"context_root\":false,\"target\":\"\"},{\"name\":\"completed\",\"member\":\"completed\",\"label\":\"Completed\",\"kind\":\"boolean\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"\"},{\"name\":\"version\",\"member\":\"version\",\"label\":\"Version\",\"kind\":\"unsupported\",\"nullable\":false,\"managed\":true,\"context_root\":false,\"target\":\"\"}],\"application_required\":[\"subtask_title\",\"completed\"]},\"task_comment\":{\"name\":\"task_comment\",\"label\":\"Task comment\",\"primary\":false,\"enabled\":false,\"editable\":[],\"container\":\"task\",\"authorization\":\"\",\"create_handler\":\"\",\"title\":\"comment_text\",\"root\":\"work_space\",\"group\":\"\",\"group_query\":\"\",\"candidates\":{},\"multiline\":[],\"defaults\":{},\"date_orders\":[],\"fields\":[{\"name\":\"id\",\"member\":\"id\",\"label\":\"Id\",\"kind\":\"unsupported\",\"nullable\":false,\"managed\":true,\"context_root\":false,\"target\":\"\"},{\"name\":\"work_space\",\"member\":\"workSpace\",\"label\":\"Work Space\",\"kind\":\"reference\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"work_space\"},{\"name\":\"task\",\"member\":\"task\",\"label\":\"Task\",\"kind\":\"reference\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"work_task\"},{\"name\":\"author\",\"member\":\"author\",\"label\":\"Author\",\"kind\":\"reference\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"work_account\"},{\"name\":\"comment_text\",\"member\":\"commentText\",\"label\":\"Comment Text\",\"kind\":\"text\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"\"},{\"name\":\"edited\",\"member\":\"edited\",\"label\":\"Edited\",\"kind\":\"boolean\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"\"},{\"name\":\"create_time\",\"member\":\"createTime\",\"label\":\"Create Time\",\"kind\":\"unsupported\",\"nullable\":false,\"managed\":true,\"context_root\":false,\"target\":\"\"},{\"name\":\"version\",\"member\":\"version\",\"label\":\"Version\",\"kind\":\"unsupported\",\"nullable\":false,\"managed\":true,\"context_root\":false,\"target\":\"\"}],\"application_required\":[\"author\",\"comment_text\",\"edited\"]},\"task_dependency\":{\"name\":\"task_dependency\",\"label\":\"Task dependency\",\"primary\":false,\"enabled\":false,\"editable\":[],\"container\":\"dependent\",\"authorization\":\"\",\"create_handler\":\"\",\"title\":\"id\",\"root\":\"work_space\",\"group\":\"\",\"group_query\":\"\",\"candidates\":{},\"multiline\":[],\"defaults\":{},\"date_orders\":[],\"fields\":[{\"name\":\"id\",\"member\":\"id\",\"label\":\"Id\",\"kind\":\"unsupported\",\"nullable\":false,\"managed\":true,\"context_root\":false,\"target\":\"\"},{\"name\":\"work_space\",\"member\":\"workSpace\",\"label\":\"Work Space\",\"kind\":\"reference\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"work_space\"},{\"name\":\"dependent\",\"member\":\"dependent\",\"label\":\"Dependent\",\"kind\":\"reference\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"work_task\"},{\"name\":\"blocker\",\"member\":\"blocker\",\"label\":\"Blocker\",\"kind\":\"reference\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"work_task\"},{\"name\":\"version\",\"member\":\"version\",\"label\":\"Version\",\"kind\":\"unsupported\",\"nullable\":false,\"managed\":true,\"context_root\":false,\"target\":\"\"}],\"application_required\":[\"blocker\"]},\"task_placement\":{\"name\":\"task_placement\",\"label\":\"Project task placement\",\"primary\":false,\"enabled\":false,\"editable\":[],\"container\":\"task\",\"authorization\":\"\",\"create_handler\":\"\",\"title\":\"id\",\"root\":\"work_space\",\"group\":\"\",\"group_query\":\"\",\"candidates\":{},\"multiline\":[],\"defaults\":{},\"date_orders\":[],\"fields\":[{\"name\":\"id\",\"member\":\"id\",\"label\":\"Id\",\"kind\":\"unsupported\",\"nullable\":false,\"managed\":true,\"context_root\":false,\"target\":\"\"},{\"name\":\"work_space\",\"member\":\"workSpace\",\"label\":\"Work Space\",\"kind\":\"reference\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"work_space\"},{\"name\":\"task\",\"member\":\"task\",\"label\":\"Task\",\"kind\":\"reference\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"work_task\"},{\"name\":\"project\",\"member\":\"project\",\"label\":\"Project\",\"kind\":\"reference\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"work_project\"},{\"name\":\"section\",\"member\":\"section\",\"label\":\"Section\",\"kind\":\"reference\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"project_section\"},{\"name\":\"placement_order\",\"member\":\"placementOrder\",\"label\":\"Placement Order\",\"kind\":\"number\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"\"},{\"name\":\"version\",\"member\":\"version\",\"label\":\"Version\",\"kind\":\"unsupported\",\"nullable\":false,\"managed\":true,\"context_root\":false,\"target\":\"\"}],\"application_required\":[\"project\",\"section\",\"placement_order\"]},\"recurrence_link\":{\"name\":\"recurrence_link\",\"label\":\"Recurring occurrence\",\"primary\":false,\"enabled\":false,\"editable\":[],\"container\":\"source_task\",\"authorization\":\"\",\"create_handler\":\"\",\"title\":\"id\",\"root\":\"work_space\",\"group\":\"\",\"group_query\":\"\",\"candidates\":{},\"multiline\":[],\"defaults\":{},\"date_orders\":[],\"fields\":[{\"name\":\"id\",\"member\":\"id\",\"label\":\"Id\",\"kind\":\"unsupported\",\"nullable\":false,\"managed\":true,\"context_root\":false,\"target\":\"\"},{\"name\":\"work_space\",\"member\":\"workSpace\",\"label\":\"Work Space\",\"kind\":\"reference\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"work_space\"},{\"name\":\"source_task\",\"member\":\"sourceTask\",\"label\":\"Source Task\",\"kind\":\"reference\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"work_task\"},{\"name\":\"next_task\",\"member\":\"nextTask\",\"label\":\"Next Task\",\"kind\":\"reference\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"work_task\"},{\"name\":\"version\",\"member\":\"version\",\"label\":\"Version\",\"kind\":\"unsupported\",\"nullable\":false,\"managed\":true,\"context_root\":false,\"target\":\"\"}],\"application_required\":[\"next_task\"]},\"task_event\":{\"name\":\"task_event\",\"label\":\"Task activity\",\"primary\":false,\"enabled\":false,\"editable\":[],\"container\":\"task\",\"authorization\":\"\",\"create_handler\":\"\",\"title\":\"event_kind\",\"root\":\"work_space\",\"group\":\"\",\"group_query\":\"\",\"candidates\":{},\"multiline\":[],\"defaults\":{},\"date_orders\":[],\"fields\":[{\"name\":\"id\",\"member\":\"id\",\"label\":\"Id\",\"kind\":\"unsupported\",\"nullable\":false,\"managed\":true,\"context_root\":false,\"target\":\"\"},{\"name\":\"work_space\",\"member\":\"workSpace\",\"label\":\"Work Space\",\"kind\":\"reference\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"work_space\"},{\"name\":\"task\",\"member\":\"task\",\"label\":\"Task\",\"kind\":\"reference\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"work_task\"},{\"name\":\"actor\",\"member\":\"actor\",\"label\":\"Actor\",\"kind\":\"reference\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"work_account\"},{\"name\":\"scope_project\",\"member\":\"scopeProject\",\"label\":\"Scope Project\",\"kind\":\"reference\",\"nullable\":true,\"managed\":false,\"context_root\":false,\"target\":\"work_project\"},{\"name\":\"related_task\",\"member\":\"relatedTask\",\"label\":\"Related Task\",\"kind\":\"reference\",\"nullable\":true,\"managed\":false,\"context_root\":false,\"target\":\"work_task\"},{\"name\":\"event_kind\",\"member\":\"eventKind\",\"label\":\"Event Kind\",\"kind\":\"text\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"\"},{\"name\":\"field_label\",\"member\":\"fieldLabel\",\"label\":\"Field Label\",\"kind\":\"text\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"\"},{\"name\":\"old_value\",\"member\":\"oldValue\",\"label\":\"Old Value\",\"kind\":\"text\",\"nullable\":true,\"managed\":false,\"context_root\":false,\"target\":\"\"},{\"name\":\"new_value\",\"member\":\"newValue\",\"label\":\"New Value\",\"kind\":\"text\",\"nullable\":true,\"managed\":false,\"context_root\":false,\"target\":\"\"},{\"name\":\"event_time\",\"member\":\"eventTime\",\"label\":\"Event Time\",\"kind\":\"unsupported\",\"nullable\":false,\"managed\":true,\"context_root\":false,\"target\":\"\"},{\"name\":\"version\",\"member\":\"version\",\"label\":\"Version\",\"kind\":\"unsupported\",\"nullable\":false,\"managed\":true,\"context_root\":false,\"target\":\"\"}],\"application_required\":[\"actor\",\"event_kind\",\"field_label\"]},\"task_participant\":{\"name\":\"task_participant\",\"label\":\"Task participant\",\"primary\":false,\"enabled\":false,\"editable\":[],\"container\":\"task\",\"authorization\":\"\",\"create_handler\":\"\",\"title\":\"id\",\"root\":\"work_space\",\"group\":\"\",\"group_query\":\"\",\"candidates\":{},\"multiline\":[],\"defaults\":{},\"date_orders\":[],\"fields\":[{\"name\":\"id\",\"member\":\"id\",\"label\":\"Id\",\"kind\":\"unsupported\",\"nullable\":false,\"managed\":true,\"context_root\":false,\"target\":\"\"},{\"name\":\"work_space\",\"member\":\"workSpace\",\"label\":\"Work Space\",\"kind\":\"reference\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"work_space\"},{\"name\":\"task\",\"member\":\"task\",\"label\":\"Task\",\"kind\":\"reference\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"work_task\"},{\"name\":\"participant\",\"member\":\"participant\",\"label\":\"Participant\",\"kind\":\"reference\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"work_account\"},{\"name\":\"version\",\"member\":\"version\",\"label\":\"Version\",\"kind\":\"unsupported\",\"nullable\":false,\"managed\":true,\"context_root\":false,\"target\":\"\"}],\"application_required\":[\"participant\"]},\"deleted_task_viewer\":{\"name\":\"deleted_task_viewer\",\"label\":\"Deleted task viewer\",\"primary\":false,\"enabled\":false,\"editable\":[],\"container\":\"task\",\"authorization\":\"\",\"create_handler\":\"\",\"title\":\"id\",\"root\":\"work_space\",\"group\":\"\",\"group_query\":\"\",\"candidates\":{},\"multiline\":[],\"defaults\":{},\"date_orders\":[],\"fields\":[{\"name\":\"id\",\"member\":\"id\",\"label\":\"Id\",\"kind\":\"unsupported\",\"nullable\":false,\"managed\":true,\"context_root\":false,\"target\":\"\"},{\"name\":\"work_space\",\"member\":\"workSpace\",\"label\":\"Work Space\",\"kind\":\"reference\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"work_space\"},{\"name\":\"task\",\"member\":\"task\",\"label\":\"Task\",\"kind\":\"reference\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"work_task\"},{\"name\":\"viewer\",\"member\":\"viewer\",\"label\":\"Viewer\",\"kind\":\"reference\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"work_account\"},{\"name\":\"version\",\"member\":\"version\",\"label\":\"Version\",\"kind\":\"unsupported\",\"nullable\":false,\"managed\":true,\"context_root\":false,\"target\":\"\"}],\"application_required\":[\"viewer\"]},\"task_blueprint\":{\"name\":\"task_blueprint\",\"label\":\"Task template\",\"primary\":false,\"enabled\":false,\"editable\":[],\"container\":\"project\",\"authorization\":\"\",\"create_handler\":\"\",\"title\":\"template_name\",\"root\":\"work_space\",\"group\":\"\",\"group_query\":\"\",\"candidates\":{},\"multiline\":[],\"defaults\":{},\"date_orders\":[],\"fields\":[{\"name\":\"id\",\"member\":\"id\",\"label\":\"Id\",\"kind\":\"unsupported\",\"nullable\":false,\"managed\":true,\"context_root\":false,\"target\":\"\"},{\"name\":\"work_space\",\"member\":\"workSpace\",\"label\":\"Work Space\",\"kind\":\"reference\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"work_space\"},{\"name\":\"project\",\"member\":\"project\",\"label\":\"Project\",\"kind\":\"reference\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"work_project\"},{\"name\":\"template_name\",\"member\":\"templateName\",\"label\":\"Template Name\",\"kind\":\"text\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"\"},{\"name\":\"initial_title\",\"member\":\"initialTitle\",\"label\":\"Initial Title\",\"kind\":\"text\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"\"},{\"name\":\"initial_description\",\"member\":\"initialDescription\",\"label\":\"Initial Description\",\"kind\":\"text\",\"nullable\":true,\"managed\":false,\"context_root\":false,\"target\":\"\"},{\"name\":\"assignee\",\"member\":\"assignee\",\"label\":\"Assignee\",\"kind\":\"reference\",\"nullable\":true,\"managed\":false,\"context_root\":false,\"target\":\"work_account\"},{\"name\":\"due_offset\",\"member\":\"dueOffset\",\"label\":\"Due Offset\",\"kind\":\"number\",\"nullable\":true,\"managed\":false,\"context_root\":false,\"target\":\"\"},{\"name\":\"repeat_period\",\"member\":\"repeatPeriod\",\"label\":\"Repeat Period\",\"kind\":\"text\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"\"},{\"name\":\"approval\",\"member\":\"approval\",\"label\":\"Approval\",\"kind\":\"boolean\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"\"},{\"name\":\"version\",\"member\":\"version\",\"label\":\"Version\",\"kind\":\"unsupported\",\"nullable\":false,\"managed\":true,\"context_root\":false,\"target\":\"\"}],\"application_required\":[\"template_name\",\"initial_title\",\"repeat_period\",\"approval\"]},\"blueprint_choice\":{\"name\":\"blueprint_choice\",\"label\":\"Template field\",\"primary\":false,\"enabled\":false,\"editable\":[],\"container\":\"blueprint\",\"authorization\":\"\",\"create_handler\":\"\",\"title\":\"id\",\"root\":\"work_space\",\"group\":\"\",\"group_query\":\"\",\"candidates\":{},\"multiline\":[],\"defaults\":{},\"date_orders\":[],\"fields\":[{\"name\":\"id\",\"member\":\"id\",\"label\":\"Id\",\"kind\":\"unsupported\",\"nullable\":false,\"managed\":true,\"context_root\":false,\"target\":\"\"},{\"name\":\"work_space\",\"member\":\"workSpace\",\"label\":\"Work Space\",\"kind\":\"reference\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"work_space\"},{\"name\":\"blueprint\",\"member\":\"blueprint\",\"label\":\"Blueprint\",\"kind\":\"reference\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"task_blueprint\"},{\"name\":\"field\",\"member\":\"field\",\"label\":\"Field\",\"kind\":\"reference\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"project_field\"},{\"name\":\"selected_option\",\"member\":\"selectedOption\",\"label\":\"Selected Option\",\"kind\":\"reference\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"field_option\"},{\"name\":\"version\",\"member\":\"version\",\"label\":\"Version\",\"kind\":\"unsupported\",\"nullable\":false,\"managed\":true,\"context_root\":false,\"target\":\"\"}],\"application_required\":[\"field\",\"selected_option\"]},\"blueprint_subtask\":{\"name\":\"blueprint_subtask\",\"label\":\"Template subtask\",\"primary\":false,\"enabled\":false,\"editable\":[],\"container\":\"blueprint\",\"authorization\":\"\",\"create_handler\":\"\",\"title\":\"subtask_title\",\"root\":\"work_space\",\"group\":\"\",\"group_query\":\"\",\"candidates\":{},\"multiline\":[],\"defaults\":{},\"date_orders\":[],\"fields\":[{\"name\":\"id\",\"member\":\"id\",\"label\":\"Id\",\"kind\":\"unsupported\",\"nullable\":false,\"managed\":true,\"context_root\":false,\"target\":\"\"},{\"name\":\"work_space\",\"member\":\"workSpace\",\"label\":\"Work Space\",\"kind\":\"reference\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"work_space\"},{\"name\":\"blueprint\",\"member\":\"blueprint\",\"label\":\"Blueprint\",\"kind\":\"reference\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"task_blueprint\"},{\"name\":\"subtask_title\",\"member\":\"subtaskTitle\",\"label\":\"Subtask Title\",\"kind\":\"text\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"\"},{\"name\":\"assignee\",\"member\":\"assignee\",\"label\":\"Assignee\",\"kind\":\"reference\",\"nullable\":true,\"managed\":false,\"context_root\":false,\"target\":\"work_account\"},{\"name\":\"due_offset\",\"member\":\"dueOffset\",\"label\":\"Due Offset\",\"kind\":\"number\",\"nullable\":true,\"managed\":false,\"context_root\":false,\"target\":\"\"},{\"name\":\"version\",\"member\":\"version\",\"label\":\"Version\",\"kind\":\"unsupported\",\"nullable\":false,\"managed\":true,\"context_root\":false,\"target\":\"\"}],\"application_required\":[\"subtask_title\"]},\"inbox_notice\":{\"name\":\"inbox_notice\",\"label\":\"Inbox notification\",\"primary\":false,\"enabled\":false,\"editable\":[],\"container\":\"task\",\"authorization\":\"\",\"create_handler\":\"\",\"title\":\"id\",\"root\":\"work_space\",\"group\":\"\",\"group_query\":\"\",\"candidates\":{},\"multiline\":[],\"defaults\":{},\"date_orders\":[],\"fields\":[{\"name\":\"id\",\"member\":\"id\",\"label\":\"Id\",\"kind\":\"unsupported\",\"nullable\":false,\"managed\":true,\"context_root\":false,\"target\":\"\"},{\"name\":\"work_space\",\"member\":\"workSpace\",\"label\":\"Work Space\",\"kind\":\"reference\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"work_space\"},{\"name\":\"task\",\"member\":\"task\",\"label\":\"Task\",\"kind\":\"reference\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"work_task\"},{\"name\":\"recipient\",\"member\":\"recipient\",\"label\":\"Recipient\",\"kind\":\"reference\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"work_account\"},{\"name\":\"event\",\"member\":\"event\",\"label\":\"Event\",\"kind\":\"reference\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"task_event\"},{\"name\":\"read_flag\",\"member\":\"readFlag\",\"label\":\"Read Flag\",\"kind\":\"boolean\",\"nullable\":false,\"managed\":false,\"context_root\":false,\"target\":\"\"},{\"name\":\"version\",\"member\":\"version\",\"label\":\"Version\",\"kind\":\"unsupported\",\"nullable\":false,\"managed\":true,\"context_root\":false,\"target\":\"\"}],\"application_required\":[\"recipient\",\"event\",\"read_flag\"]}}}")

QUERIES = {
    "work_account": Q.work_accounts,
    "work_project": Q.work_projects,
    "project_membership": Q.project_memberships,
    "project_section": Q.project_sections,
    "work_task": Q.work_tasks,
    "project_field": Q.project_fields,
    "field_option": Q.field_options,
    "task_field_choice": Q.task_field_choices,
    "work_subtask": Q.work_subtasks,
    "task_comment": Q.task_comments,
    "task_dependency": Q.task_dependencies,
    "task_placement": Q.task_placements,
    "recurrence_link": Q.recurrence_links,
    "task_event": Q.task_events,
    "task_participant": Q.task_participants,
    "deleted_task_viewer": Q.deleted_task_viewers,
    "task_blueprint": Q.task_blueprints,
    "blueprint_choice": Q.blueprint_choices,
    "blueprint_subtask": Q.blueprint_subtasks,
    "inbox_notice": Q.inbox_notices,
}

BY_ID = {
    "work_account": lambda query, value: query.whose_id_is(value),
    "work_project": lambda query, value: query.with_id_is(value),
    "project_membership": lambda query, value: query.with_id_is(value),
    "project_section": lambda query, value: query.with_id_is(value),
    "work_task": lambda query, value: query.with_id_is(value),
    "project_field": lambda query, value: query.with_id_is(value),
    "field_option": lambda query, value: query.with_id_is(value),
    "task_field_choice": lambda query, value: query.with_id_is(value),
    "work_subtask": lambda query, value: query.with_id_is(value),
    "task_comment": lambda query, value: query.with_id_is(value),
    "task_dependency": lambda query, value: query.with_id_is(value),
    "task_placement": lambda query, value: query.with_id_is(value),
    "recurrence_link": lambda query, value: query.with_id_is(value),
    "task_event": lambda query, value: query.with_id_is(value),
    "task_participant": lambda query, value: query.with_id_is(value),
    "deleted_task_viewer": lambda query, value: query.with_id_is(value),
    "task_blueprint": lambda query, value: query.with_id_is(value),
    "blueprint_choice": lambda query, value: query.with_id_is(value),
    "blueprint_subtask": lambda query, value: query.with_id_is(value),
    "inbox_notice": lambda query, value: query.with_id_is(value),
}

BY_IDS = {
    "work_account": lambda query, values: query.whose_id_in(*values) if values else query.whose_id_is_unknown(),  # persisted IDs are never NULL
    "work_project": lambda query, values: query.with_id_in(*values) if values else query.with_id_is_unknown(),  # persisted IDs are never NULL
    "project_membership": lambda query, values: query.with_id_in(*values) if values else query.with_id_is_unknown(),  # persisted IDs are never NULL
    "project_section": lambda query, values: query.with_id_in(*values) if values else query.with_id_is_unknown(),  # persisted IDs are never NULL
    "work_task": lambda query, values: query.with_id_in(*values) if values else query.with_id_is_unknown(),  # persisted IDs are never NULL
    "project_field": lambda query, values: query.with_id_in(*values) if values else query.with_id_is_unknown(),  # persisted IDs are never NULL
    "field_option": lambda query, values: query.with_id_in(*values) if values else query.with_id_is_unknown(),  # persisted IDs are never NULL
    "task_field_choice": lambda query, values: query.with_id_in(*values) if values else query.with_id_is_unknown(),  # persisted IDs are never NULL
    "work_subtask": lambda query, values: query.with_id_in(*values) if values else query.with_id_is_unknown(),  # persisted IDs are never NULL
    "task_comment": lambda query, values: query.with_id_in(*values) if values else query.with_id_is_unknown(),  # persisted IDs are never NULL
    "task_dependency": lambda query, values: query.with_id_in(*values) if values else query.with_id_is_unknown(),  # persisted IDs are never NULL
    "task_placement": lambda query, values: query.with_id_in(*values) if values else query.with_id_is_unknown(),  # persisted IDs are never NULL
    "recurrence_link": lambda query, values: query.with_id_in(*values) if values else query.with_id_is_unknown(),  # persisted IDs are never NULL
    "task_event": lambda query, values: query.with_id_in(*values) if values else query.with_id_is_unknown(),  # persisted IDs are never NULL
    "task_participant": lambda query, values: query.with_id_in(*values) if values else query.with_id_is_unknown(),  # persisted IDs are never NULL
    "deleted_task_viewer": lambda query, values: query.with_id_in(*values) if values else query.with_id_is_unknown(),  # persisted IDs are never NULL
    "task_blueprint": lambda query, values: query.with_id_in(*values) if values else query.with_id_is_unknown(),  # persisted IDs are never NULL
    "blueprint_choice": lambda query, values: query.with_id_in(*values) if values else query.with_id_is_unknown(),  # persisted IDs are never NULL
    "blueprint_subtask": lambda query, values: query.with_id_in(*values) if values else query.with_id_is_unknown(),  # persisted IDs are never NULL
    "inbox_notice": lambda query, values: query.with_id_in(*values) if values else query.with_id_is_unknown(),  # persisted IDs are never NULL
}

FILTERS = {
    "work_account": {
        "work_space": lambda query, value: query.filter_by_work_space(value),
    },
    "work_project": {
        "work_space": lambda query, value: query.filter_by_work_space(value),
        "owner_account": lambda query, value: query.filter_by_owner_account(value),
    },
    "project_membership": {
        "work_space": lambda query, value: query.filter_by_work_space(value),
        "project": lambda query, value: query.filter_by_project(value),
        "member_account": lambda query, value: query.filter_by_member_account(value),
    },
    "project_section": {
        "work_space": lambda query, value: query.filter_by_work_space(value),
        "project": lambda query, value: query.filter_by_project(value),
    },
    "work_task": {
        "work_space": lambda query, value: query.filter_by_work_space(value),
        "project": lambda query, value: query.filter_by_project(value),
        "section": lambda query, value: query.filter_by_section(value),
        "created_by": lambda query, value: query.filter_by_created_by(value),
        "assignee": lambda query, value: query.filter_by_assignee(value),
    },
    "project_field": {
        "work_space": lambda query, value: query.filter_by_work_space(value),
        "project": lambda query, value: query.filter_by_project(value),
    },
    "field_option": {
        "work_space": lambda query, value: query.filter_by_work_space(value),
        "field": lambda query, value: query.filter_by_field(value),
    },
    "task_field_choice": {
        "work_space": lambda query, value: query.filter_by_work_space(value),
        "task": lambda query, value: query.filter_by_task(value),
        "field": lambda query, value: query.filter_by_field(value),
        "selected_option": lambda query, value: query.filter_by_selected_option(value),
    },
    "work_subtask": {
        "work_space": lambda query, value: query.filter_by_work_space(value),
        "task": lambda query, value: query.filter_by_task(value),
        "assignee": lambda query, value: query.filter_by_assignee(value),
    },
    "task_comment": {
        "work_space": lambda query, value: query.filter_by_work_space(value),
        "task": lambda query, value: query.filter_by_task(value),
        "author": lambda query, value: query.filter_by_author(value),
    },
    "task_dependency": {
        "work_space": lambda query, value: query.filter_by_work_space(value),
        "dependent": lambda query, value: query.filter_by_dependent(value),
        "blocker": lambda query, value: query.filter_by_blocker(value),
    },
    "task_placement": {
        "work_space": lambda query, value: query.filter_by_work_space(value),
        "task": lambda query, value: query.filter_by_task(value),
        "project": lambda query, value: query.filter_by_project(value),
        "section": lambda query, value: query.filter_by_section(value),
    },
    "recurrence_link": {
        "work_space": lambda query, value: query.filter_by_work_space(value),
        "source_task": lambda query, value: query.filter_by_source_task(value),
        "next_task": lambda query, value: query.filter_by_next_task(value),
    },
    "task_event": {
        "work_space": lambda query, value: query.filter_by_work_space(value),
        "task": lambda query, value: query.filter_by_task(value),
        "actor": lambda query, value: query.filter_by_actor(value),
        "scope_project": lambda query, value: query.filter_by_scope_project(value),
        "related_task": lambda query, value: query.filter_by_related_task(value),
    },
    "task_participant": {
        "work_space": lambda query, value: query.filter_by_work_space(value),
        "task": lambda query, value: query.filter_by_task(value),
        "participant": lambda query, value: query.filter_by_participant(value),
    },
    "deleted_task_viewer": {
        "work_space": lambda query, value: query.filter_by_work_space(value),
        "task": lambda query, value: query.filter_by_task(value),
        "viewer": lambda query, value: query.filter_by_viewer(value),
    },
    "task_blueprint": {
        "work_space": lambda query, value: query.filter_by_work_space(value),
        "project": lambda query, value: query.filter_by_project(value),
        "assignee": lambda query, value: query.filter_by_assignee(value),
    },
    "blueprint_choice": {
        "work_space": lambda query, value: query.filter_by_work_space(value),
        "blueprint": lambda query, value: query.filter_by_blueprint(value),
        "field": lambda query, value: query.filter_by_field(value),
        "selected_option": lambda query, value: query.filter_by_selected_option(value),
    },
    "blueprint_subtask": {
        "work_space": lambda query, value: query.filter_by_work_space(value),
        "blueprint": lambda query, value: query.filter_by_blueprint(value),
        "assignee": lambda query, value: query.filter_by_assignee(value),
    },
    "inbox_notice": {
        "work_space": lambda query, value: query.filter_by_work_space(value),
        "task": lambda query, value: query.filter_by_task(value),
        "recipient": lambda query, value: query.filter_by_recipient(value),
        "event": lambda query, value: query.filter_by_event(value),
    },
}

MATCHERS = {
    "work_account": {
        "work_space": lambda query, nested: query.with_work_space_matching(nested),
        "work_project_list": lambda query, nested: query.with_work_project_list_matching(nested),
        "project_membership_list": lambda query, nested: query.with_project_membership_list_matching(nested),
        "work_task_list_as_created_by": lambda query, nested: query.with_work_task_list_as_created_by_matching(nested),
        "work_task_list_as_assignee": lambda query, nested: query.with_work_task_list_as_assignee_matching(nested),
        "work_subtask_list": lambda query, nested: query.with_work_subtask_list_matching(nested),
        "task_comment_list": lambda query, nested: query.with_task_comment_list_matching(nested),
        "task_event_list": lambda query, nested: query.with_task_event_list_matching(nested),
        "task_participant_list": lambda query, nested: query.with_task_participant_list_matching(nested),
        "deleted_task_viewer_list": lambda query, nested: query.with_deleted_task_viewer_list_matching(nested),
        "task_blueprint_list": lambda query, nested: query.with_task_blueprint_list_matching(nested),
        "blueprint_subtask_list": lambda query, nested: query.with_blueprint_subtask_list_matching(nested),
        "inbox_notice_list": lambda query, nested: query.with_inbox_notice_list_matching(nested),
    },
    "work_project": {
        "work_space": lambda query, nested: query.with_work_space_matching(nested),
        "owner_account": lambda query, nested: query.with_owner_account_matching(nested),
        "project_membership_list": lambda query, nested: query.with_project_membership_list_matching(nested),
        "project_section_list": lambda query, nested: query.with_project_section_list_matching(nested),
        "work_task_list": lambda query, nested: query.with_work_task_list_matching(nested),
        "project_field_list": lambda query, nested: query.with_project_field_list_matching(nested),
        "task_placement_list": lambda query, nested: query.with_task_placement_list_matching(nested),
        "task_event_list": lambda query, nested: query.with_task_event_list_matching(nested),
        "task_blueprint_list": lambda query, nested: query.with_task_blueprint_list_matching(nested),
    },
    "project_membership": {
        "work_space": lambda query, nested: query.with_work_space_matching(nested),
        "project": lambda query, nested: query.with_project_matching(nested),
        "member_account": lambda query, nested: query.with_member_account_matching(nested),
    },
    "project_section": {
        "work_space": lambda query, nested: query.with_work_space_matching(nested),
        "project": lambda query, nested: query.with_project_matching(nested),
        "work_task_list": lambda query, nested: query.with_work_task_list_matching(nested),
        "task_placement_list": lambda query, nested: query.with_task_placement_list_matching(nested),
    },
    "work_task": {
        "work_space": lambda query, nested: query.with_work_space_matching(nested),
        "project": lambda query, nested: query.with_project_matching(nested),
        "section": lambda query, nested: query.with_section_matching(nested),
        "created_by": lambda query, nested: query.with_created_by_matching(nested),
        "assignee": lambda query, nested: query.with_assignee_matching(nested),
        "task_field_choice_list": lambda query, nested: query.with_task_field_choice_list_matching(nested),
        "work_subtask_list": lambda query, nested: query.with_work_subtask_list_matching(nested),
        "task_comment_list": lambda query, nested: query.with_task_comment_list_matching(nested),
        "task_dependency_list_as_dependent": lambda query, nested: query.with_task_dependency_list_as_dependent_matching(nested),
        "task_dependency_list_as_blocker": lambda query, nested: query.with_task_dependency_list_as_blocker_matching(nested),
        "task_placement_list": lambda query, nested: query.with_task_placement_list_matching(nested),
        "recurrence_link_list_as_source_task": lambda query, nested: query.with_recurrence_link_list_as_source_task_matching(nested),
        "recurrence_link_list_as_next_task": lambda query, nested: query.with_recurrence_link_list_as_next_task_matching(nested),
        "task_event_list_as_task": lambda query, nested: query.with_task_event_list_as_task_matching(nested),
        "task_event_list_as_related_task": lambda query, nested: query.with_task_event_list_as_related_task_matching(nested),
        "task_participant_list": lambda query, nested: query.with_task_participant_list_matching(nested),
        "deleted_task_viewer_list": lambda query, nested: query.with_deleted_task_viewer_list_matching(nested),
        "inbox_notice_list": lambda query, nested: query.with_inbox_notice_list_matching(nested),
    },
    "project_field": {
        "work_space": lambda query, nested: query.with_work_space_matching(nested),
        "project": lambda query, nested: query.with_project_matching(nested),
        "field_option_list": lambda query, nested: query.with_field_option_list_matching(nested),
        "task_field_choice_list": lambda query, nested: query.with_task_field_choice_list_matching(nested),
        "blueprint_choice_list": lambda query, nested: query.with_blueprint_choice_list_matching(nested),
    },
    "field_option": {
        "work_space": lambda query, nested: query.with_work_space_matching(nested),
        "field": lambda query, nested: query.with_field_matching(nested),
        "task_field_choice_list": lambda query, nested: query.with_task_field_choice_list_matching(nested),
        "blueprint_choice_list": lambda query, nested: query.with_blueprint_choice_list_matching(nested),
    },
    "task_field_choice": {
        "work_space": lambda query, nested: query.with_work_space_matching(nested),
        "task": lambda query, nested: query.with_task_matching(nested),
        "field": lambda query, nested: query.with_field_matching(nested),
        "selected_option": lambda query, nested: query.with_selected_option_matching(nested),
    },
    "work_subtask": {
        "work_space": lambda query, nested: query.with_work_space_matching(nested),
        "task": lambda query, nested: query.with_task_matching(nested),
        "assignee": lambda query, nested: query.with_assignee_matching(nested),
    },
    "task_comment": {
        "work_space": lambda query, nested: query.with_work_space_matching(nested),
        "task": lambda query, nested: query.with_task_matching(nested),
        "author": lambda query, nested: query.with_author_matching(nested),
    },
    "task_dependency": {
        "work_space": lambda query, nested: query.with_work_space_matching(nested),
        "dependent": lambda query, nested: query.with_dependent_matching(nested),
        "blocker": lambda query, nested: query.with_blocker_matching(nested),
    },
    "task_placement": {
        "work_space": lambda query, nested: query.with_work_space_matching(nested),
        "task": lambda query, nested: query.with_task_matching(nested),
        "project": lambda query, nested: query.with_project_matching(nested),
        "section": lambda query, nested: query.with_section_matching(nested),
    },
    "recurrence_link": {
        "work_space": lambda query, nested: query.with_work_space_matching(nested),
        "source_task": lambda query, nested: query.with_source_task_matching(nested),
        "next_task": lambda query, nested: query.with_next_task_matching(nested),
    },
    "task_event": {
        "work_space": lambda query, nested: query.with_work_space_matching(nested),
        "task": lambda query, nested: query.with_task_matching(nested),
        "actor": lambda query, nested: query.with_actor_matching(nested),
        "scope_project": lambda query, nested: query.with_scope_project_matching(nested),
        "related_task": lambda query, nested: query.with_related_task_matching(nested),
        "inbox_notice_list": lambda query, nested: query.with_inbox_notice_list_matching(nested),
    },
    "task_participant": {
        "work_space": lambda query, nested: query.with_work_space_matching(nested),
        "task": lambda query, nested: query.with_task_matching(nested),
        "participant": lambda query, nested: query.with_participant_matching(nested),
    },
    "deleted_task_viewer": {
        "work_space": lambda query, nested: query.with_work_space_matching(nested),
        "task": lambda query, nested: query.with_task_matching(nested),
        "viewer": lambda query, nested: query.with_viewer_matching(nested),
    },
    "task_blueprint": {
        "work_space": lambda query, nested: query.with_work_space_matching(nested),
        "project": lambda query, nested: query.with_project_matching(nested),
        "assignee": lambda query, nested: query.with_assignee_matching(nested),
        "blueprint_choice_list": lambda query, nested: query.with_blueprint_choice_list_matching(nested),
        "blueprint_subtask_list": lambda query, nested: query.with_blueprint_subtask_list_matching(nested),
    },
    "blueprint_choice": {
        "work_space": lambda query, nested: query.with_work_space_matching(nested),
        "blueprint": lambda query, nested: query.with_blueprint_matching(nested),
        "field": lambda query, nested: query.with_field_matching(nested),
        "selected_option": lambda query, nested: query.with_selected_option_matching(nested),
    },
    "blueprint_subtask": {
        "work_space": lambda query, nested: query.with_work_space_matching(nested),
        "blueprint": lambda query, nested: query.with_blueprint_matching(nested),
        "assignee": lambda query, nested: query.with_assignee_matching(nested),
    },
    "inbox_notice": {
        "work_space": lambda query, nested: query.with_work_space_matching(nested),
        "task": lambda query, nested: query.with_task_matching(nested),
        "recipient": lambda query, nested: query.with_recipient_matching(nested),
        "event": lambda query, nested: query.with_event_matching(nested),
    },
}

UPDATERS = {
    "work_account": {
        "work_space": lambda entity, value: entity.update_work_space(value),
        "display_name": lambda entity, value: entity.update_display_name(value),
        "email_address": lambda entity, value: entity.update_email_address(value),
        "password_hash": lambda entity, value: entity.update_password_hash(value),
    },
    "work_project": {
        "work_space": lambda entity, value: entity.update_work_space(value),
        "owner_account": lambda entity, value: entity.update_owner_account(value),
        "project_name": lambda entity, value: entity.update_project_name(value),
        "shift_dates": lambda entity, value: entity.update_shift_dates(value),
    },
    "project_membership": {
        "work_space": lambda entity, value: entity.update_work_space(value),
        "project": lambda entity, value: entity.update_project(value),
        "member_account": lambda entity, value: entity.update_member_account(value),
        "access_role": lambda entity, value: entity.update_access_role(value),
    },
    "project_section": {
        "work_space": lambda entity, value: entity.update_work_space(value),
        "project": lambda entity, value: entity.update_project(value),
        "section_name": lambda entity, value: entity.update_section_name(value),
        "section_order": lambda entity, value: entity.update_section_order(value),
        "default_section": lambda entity, value: entity.update_default_section(value),
    },
    "work_task": {
        "work_space": lambda entity, value: entity.update_work_space(value),
        "project": lambda entity, value: entity.update_project(value),
        "section": lambda entity, value: entity.update_section(value),
        "deleted_epoch": lambda entity, value: entity.update_deleted_epoch(value),
        "approval": lambda entity, value: entity.update_approval(value),
        "decision": lambda entity, value: entity.update_decision(value),
        "repeat_period": lambda entity, value: entity.update_repeat_period(value),
        "created_by": lambda entity, value: entity.update_created_by(value),
        "primary_detached": lambda entity, value: entity.update_primary_detached(value),
        "task_order": lambda entity, value: entity.update_task_order(value),
        "task_title": lambda entity, value: entity.update_task_title(value),
        "description": lambda entity, value: entity.update_description(value),
        "assignee": lambda entity, value: entity.update_assignee(value),
        "start_date": lambda entity, value: entity.update_start_date(value),
        "due_date": lambda entity, value: entity.update_due_date(value),
        "completed": lambda entity, value: entity.update_completed(value),
    },
    "project_field": {
        "work_space": lambda entity, value: entity.update_work_space(value),
        "project": lambda entity, value: entity.update_project(value),
        "field_name": lambda entity, value: entity.update_field_name(value),
    },
    "field_option": {
        "work_space": lambda entity, value: entity.update_work_space(value),
        "field": lambda entity, value: entity.update_field(value),
        "option_name": lambda entity, value: entity.update_option_name(value),
        "option_order": lambda entity, value: entity.update_option_order(value),
    },
    "task_field_choice": {
        "work_space": lambda entity, value: entity.update_work_space(value),
        "task": lambda entity, value: entity.update_task(value),
        "field": lambda entity, value: entity.update_field(value),
        "selected_option": lambda entity, value: entity.update_selected_option(value),
    },
    "work_subtask": {
        "work_space": lambda entity, value: entity.update_work_space(value),
        "task": lambda entity, value: entity.update_task(value),
        "subtask_title": lambda entity, value: entity.update_subtask_title(value),
        "assignee": lambda entity, value: entity.update_assignee(value),
        "due_date": lambda entity, value: entity.update_due_date(value),
        "completed": lambda entity, value: entity.update_completed(value),
    },
    "task_comment": {
        "work_space": lambda entity, value: entity.update_work_space(value),
        "task": lambda entity, value: entity.update_task(value),
        "author": lambda entity, value: entity.update_author(value),
        "comment_text": lambda entity, value: entity.update_comment_text(value),
        "edited": lambda entity, value: entity.update_edited(value),
    },
    "task_dependency": {
        "work_space": lambda entity, value: entity.update_work_space(value),
        "dependent": lambda entity, value: entity.update_dependent(value),
        "blocker": lambda entity, value: entity.update_blocker(value),
    },
    "task_placement": {
        "work_space": lambda entity, value: entity.update_work_space(value),
        "task": lambda entity, value: entity.update_task(value),
        "project": lambda entity, value: entity.update_project(value),
        "section": lambda entity, value: entity.update_section(value),
        "placement_order": lambda entity, value: entity.update_placement_order(value),
    },
    "recurrence_link": {
        "work_space": lambda entity, value: entity.update_work_space(value),
        "source_task": lambda entity, value: entity.update_source_task(value),
        "next_task": lambda entity, value: entity.update_next_task(value),
    },
    "task_event": {
        "work_space": lambda entity, value: entity.update_work_space(value),
        "task": lambda entity, value: entity.update_task(value),
        "actor": lambda entity, value: entity.update_actor(value),
        "scope_project": lambda entity, value: entity.update_scope_project(value),
        "related_task": lambda entity, value: entity.update_related_task(value),
        "event_kind": lambda entity, value: entity.update_event_kind(value),
        "field_label": lambda entity, value: entity.update_field_label(value),
        "old_value": lambda entity, value: entity.update_old_value(value),
        "new_value": lambda entity, value: entity.update_new_value(value),
    },
    "task_participant": {
        "work_space": lambda entity, value: entity.update_work_space(value),
        "task": lambda entity, value: entity.update_task(value),
        "participant": lambda entity, value: entity.update_participant(value),
    },
    "deleted_task_viewer": {
        "work_space": lambda entity, value: entity.update_work_space(value),
        "task": lambda entity, value: entity.update_task(value),
        "viewer": lambda entity, value: entity.update_viewer(value),
    },
    "task_blueprint": {
        "work_space": lambda entity, value: entity.update_work_space(value),
        "project": lambda entity, value: entity.update_project(value),
        "template_name": lambda entity, value: entity.update_template_name(value),
        "initial_title": lambda entity, value: entity.update_initial_title(value),
        "initial_description": lambda entity, value: entity.update_initial_description(value),
        "assignee": lambda entity, value: entity.update_assignee(value),
        "due_offset": lambda entity, value: entity.update_due_offset(value),
        "repeat_period": lambda entity, value: entity.update_repeat_period(value),
        "approval": lambda entity, value: entity.update_approval(value),
    },
    "blueprint_choice": {
        "work_space": lambda entity, value: entity.update_work_space(value),
        "blueprint": lambda entity, value: entity.update_blueprint(value),
        "field": lambda entity, value: entity.update_field(value),
        "selected_option": lambda entity, value: entity.update_selected_option(value),
    },
    "blueprint_subtask": {
        "work_space": lambda entity, value: entity.update_work_space(value),
        "blueprint": lambda entity, value: entity.update_blueprint(value),
        "subtask_title": lambda entity, value: entity.update_subtask_title(value),
        "assignee": lambda entity, value: entity.update_assignee(value),
        "due_offset": lambda entity, value: entity.update_due_offset(value),
    },
    "inbox_notice": {
        "work_space": lambda entity, value: entity.update_work_space(value),
        "task": lambda entity, value: entity.update_task(value),
        "recipient": lambda entity, value: entity.update_recipient(value),
        "event": lambda entity, value: entity.update_event(value),
        "read_flag": lambda entity, value: entity.update_read_flag(value),
    },
}
