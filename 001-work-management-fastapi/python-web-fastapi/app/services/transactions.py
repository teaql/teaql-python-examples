"""Native BusinessOperation construction and execution; authorization is mandatory."""
from teaql.runtime import BusinessOperation
from .identity import actor
from .errors import ServiceConfigurationError, ServiceError
from ._usage import record


def command(*, name, version, root_type, parameters, authorize, prepare, handler, validate):
    for label, callback in (("authorize", authorize), ("prepare", prepare), ("handler", handler), ("validate", validate)):
        if not callable(callback):
            raise ServiceConfigurationError("Command requires an explicit " + label + " callback")
    return BusinessOperation(name=name, version=version, root_type=root_type, parameters=parameters,
                             authorize=authorize, prepare=prepare, handler=handler, validate=validate)


async def execute(operation, context, *, key, parameters, comment):
    actor(context)
    if not isinstance(key, str) or not key.strip():
        raise ServiceError("A stable, non-empty idempotency key is required")
    record("transactions", "execute")
    return await operation.execute(context, key=key, parameters=parameters, comment=comment)
