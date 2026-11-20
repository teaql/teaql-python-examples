"""One conversion contract for services; model nullability remains authoritative."""
from datetime import date, datetime, timezone
from .errors import ServiceError
from ._usage import record

UNSET = object()


def date_value(raw, *, field, nullable=False):
    record("temporal", "date_value")
    if raw is None or raw == "":
        if nullable: return None
        raise ServiceError(field + " is required by KSML; use ? in the model only if the business allows clearing it")
    if isinstance(raw, datetime):
        raise ServiceError(field + " requires a whole-day date, not a timestamp")
    if isinstance(raw, date): return raw
    if isinstance(raw, str):
        try:
            parsed = date.fromisoformat(raw)
            if parsed.isoformat() == raw: return parsed
        except ValueError: pass
    raise ServiceError(field + " requires YYYY-MM-DD")


def instant_value(raw, *, field, nullable=False):
    record("temporal", "instant_value")
    if raw is None or raw == "":
        if nullable: return None
        raise ServiceError(field + " is required by KSML")
    try:
        parsed = datetime.fromisoformat(raw.replace("Z", "+00:00")) if isinstance(raw, str) else raw
        if not isinstance(parsed, datetime) or parsed.tzinfo is None or parsed.utcoffset() is None:
            raise ValueError()
        return parsed.astimezone(timezone.utc)
    except (ValueError, TypeError):
        raise ServiceError(field + " requires an ISO timestamp with an explicit timezone") from None


def business_time(context):
    return context.business_time()


def business_date(context):
    return context.business_date()
