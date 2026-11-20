"""Technical input conversion only; business defaults and invariants stay in application code."""
from decimal import Decimal, InvalidOperation
import json
import math
from .temporal import date_value, instant_value
from .errors import ServiceError


def normalize(raw, *, field, kind, nullable=False):
    if kind == "date": return date_value(raw, field=field, nullable=nullable)
    if kind == "instant": return instant_value(raw, field=field, nullable=nullable)
    if raw is None or (raw == "" and kind in ("integer", "reference", "number", "float")):
        if nullable: return None
        raise ServiceError(field + " is required by KSML")
    if kind == "text":
        if not isinstance(raw, str): raise ServiceError(field + " must be text")
        return raw
    if kind == "boolean":
        if raw is True or raw == "true": return True
        if raw is False or raw == "false": return False
        raise ServiceError(field + " must be true or false")
    if kind in ("integer", "reference"):
        if isinstance(raw, bool): raise ServiceError(field + " must be an integer")
        try:
            value = int(raw)
            if isinstance(raw, (float, Decimal)) and raw != value: raise ValueError()
            if kind == "reference" and value <= 0: raise ValueError()
            return value
        except (ValueError, TypeError, OverflowError):
            raise ServiceError(field + " must be a valid integer") from None
    if kind == "number":
        if isinstance(raw, bool): raise ServiceError(field + " must be numeric")
        try:
            value = Decimal(str(raw))
            if not value.is_finite(): raise ValueError()
            return value
        except (ValueError, InvalidOperation):
            raise ServiceError(field + " must be finite numeric input") from None
    if kind == "float":
        try:
            if isinstance(raw, bool): raise ValueError()
            value = float(raw)
            if not math.isfinite(value): raise ValueError()
            return value
        except (ValueError, TypeError, OverflowError):
            raise ServiceError(field + " must be finite numeric input") from None
    if kind == "json":
        try: json.dumps(raw, allow_nan=False)
        except (TypeError, ValueError): raise ServiceError(field + " must be JSON-compatible") from None
        return raw
    return raw
