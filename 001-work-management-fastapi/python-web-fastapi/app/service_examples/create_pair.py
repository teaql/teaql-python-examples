"""Parent and referenced child creation in one transaction. No route or default policy."""
from app.services import transactions
from app.services.identity import invoke
from app.services.errors import ServiceConfigurationError, ServiceError
from .work_project import WorkProjectService
from .work_task import WorkTaskService


def build(*, version, parameters, authorize, parent_values, child_values, validate):
    for callback in (parent_values, child_values):
        if not callable(callback): raise ServiceConfigurationError("Creation values require explicit application callbacks")

    async def prepare(context, inputs):
        return {}

    async def handler(context, inputs):
        first_values = await invoke(parent_values, context, inputs)
        if not isinstance(first_values, dict): raise ServiceError("parent_values must return service keyword arguments")
        first = await WorkProjectService.create(context, audit_reason="Create a declared command parent", **first_values)
        second_values = await invoke(child_values, context, inputs, first)
        if not isinstance(second_values, dict): raise ServiceError("child_values must return service keyword arguments")
        if "value_project" in second_values: raise ServiceError("The command supplies the new parent link; omit it from child_values")
        second = await WorkTaskService.create(context, audit_reason="Create a declared command child",
            **(second_values | {"value_project": first.id}))
        return {"parent_id": first.id, "child_id": second.id}

    return transactions.command(name="CreatePair:work_project:work_task:Project", version=version,
        root_type="WorkSpace", parameters=parameters,
        authorize=authorize, prepare=prepare, handler=handler, validate=validate)