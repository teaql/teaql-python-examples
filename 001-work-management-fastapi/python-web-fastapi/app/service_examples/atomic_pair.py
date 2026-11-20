"""Two model-bound service writes in one native transaction; no route or default authorizer."""
from app.services import transactions
from .work_project import WorkProjectService
from .work_subtask import WorkSubtaskService


def build(*, version, authorize, validate):
    async def prepare(context, inputs):
        first = await WorkProjectService.get(context, inputs["left_id"])
        second = await WorkSubtaskService.get(context, inputs["right_id"])
        return {"left_version": first.version, "right_version": second.version}

    async def handler(context, inputs):
        first = await WorkProjectService.update(context, inputs["left_id"],
            expected_version=inputs["left_version"], value_project_name=inputs["left_value"],
            audit_reason="Apply the first participant of an explicit command")
        second = await WorkSubtaskService.update(context, inputs["right_id"],
            expected_version=inputs["right_version"], value_subtask_title=inputs["right_value"],
            audit_reason="Apply the second participant of an explicit command")
        return {"left_id": first.id, "right_id": second.id}

    return transactions.command(name="ExamplePair:work_project:work_subtask", version=version,
        root_type="WorkSpace", parameters={"left_id": int, "right_id": int,
        "left_version": int, "right_version": int, "left_value": str, "right_value": str},
        authorize=authorize, prepare=prepare, handler=handler, validate=validate)