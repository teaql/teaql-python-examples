"""Input contracts from the same KSML metadata as generated entities and Assist."""
from functools import lru_cache
import json
from pathlib import Path
from .errors import ServiceError, ServiceConfigurationError
from .inputs import normalize
from .temporal import UNSET


@lru_cache(maxsize=1)
def _entities():
    manifest = Path(__file__).resolve().parents[2] / "CAPABILITIES.json"
    try:
        return {item["name"]: item["field_contracts"] for item in json.loads(manifest.read_text())["entities"]}
    except (OSError, KeyError, ValueError, TypeError) as error:
        raise ServiceConfigurationError("Regenerate the workspace with its field contracts beside the generated modules") from error


def field_contract(entity, field):
    try:
        return dict(_entities()[entity][field])
    except KeyError:
        raise ServiceConfigurationError("Unknown generated field: " + entity + "." + field) from None


def field_input(entity, field, raw=UNSET, *, operation="create", default=UNSET):
    """Defaults apply to omission. None is an explicit clear, never a default request."""
    spec = field_contract(entity, field)
    name = entity + "." + field
    if operation not in ("create", "update"):
        raise ServiceConfigurationError("Input operation must be create or update")
    if spec["managed"]:
        raise ServiceError(name + " is server-managed")
    if raw is UNSET:
        if operation == "update":
            return UNSET
        raw = default if default is not UNSET else None
    return normalize(raw, field=name, kind=spec["kind"], nullable=spec["nullable"])
