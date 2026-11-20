"""Public service failures; responses never include SQL, credentials or exception payloads."""
import logging
import traceback
from pathlib import Path
from fastapi.responses import JSONResponse
from teaql.runtime import BusinessOperationError
from teaql.runtime.i18n import CheckException


class ServiceError(Exception):
    status = 400
    code = "SERVICE_INPUT_INVALID"


class AuthenticationRequired(ServiceError):
    status = 401
    code = "SERVICE_AUTHENTICATION_REQUIRED"


class AccessDenied(ServiceError):
    status = 403
    code = "SERVICE_ACCESS_DENIED"


class NotFound(ServiceError):
    status = 404
    code = "SERVICE_RECORD_NOT_FOUND"


class VersionConflict(ServiceError):
    status = 409
    code = "SERVICE_VERSION_CONFLICT"


class ServiceConfigurationError(ServiceError):
    status = 503
    code = "SERVICE_NOT_CONFIGURED"


def install_handlers(app):
    async def known(request, error):
        return JSONResponse({"code": error.code, "detail": str(error)}, status_code=error.status)

    async def model_validation(request, error):
        # Schema locations and rule IDs are useful diagnostics. Input/system values,
        # rendered messages and exception payloads can contain business secrets.
        violations = [{"field": item.location.model_path, "rule_id": item.rule_id}
                      for item in error.violations]
        return JSONResponse({"code": "MODEL_VALIDATION_FAILED",
            "detail": "Correct the listed fields or their KSML definitions; evaluate and regenerate after model changes.",
            "violations": violations}, status_code=422)

    async def operation(request, error):
        if error.outcome != "unknown" and isinstance(error.__cause__, ServiceError):
            return await known(request, error.__cause__)
        if error.outcome != "unknown" and isinstance(error.__cause__, CheckException):
            return await model_validation(request, error.__cause__)
        status = (503 if error.outcome == "unknown" else 403 if error.code == "OPERATION_DENIED"
                  else 409 if error.code == "IDEMPOTENCY_CONFLICT" else 500)
        return JSONResponse({"code": error.code, "outcome": error.outcome,
            "detail": "The command did not complete normally. Retry unknown outcomes with the original key."}, status_code=status)

    async def unexpected(request, error):
        frames = [(Path(frame.filename).name, frame.lineno, frame.name)
                  for frame in traceback.extract_tb(error.__traceback__)]
        logging.getLogger(__name__).error("Service failure type=%s frames=%s", type(error).__name__, frames)
        return JSONResponse({"code": "SERVICE_INTERNAL_ERROR", "detail": "The service could not complete the request."}, status_code=500)

    app.add_exception_handler(ServiceError, known)
    app.add_exception_handler(CheckException, model_validation)
    app.add_exception_handler(BusinessOperationError, operation)
    app.add_exception_handler(Exception, unexpected)
