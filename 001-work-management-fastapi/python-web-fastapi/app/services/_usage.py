"""Optional server-side adoption evidence; never record inputs, identities or credentials."""
import json
import os


def record(service, action, entity=None):
    path = os.environ.get("TEAQL_WORKSPACE_SERVICE_TRACE_FILE")
    if not path: return
    row = {"service": service, "action": action}
    if entity is not None: row["entity"] = entity
    try:
        with open(path, "a", encoding="utf-8") as output:
            output.write(json.dumps(row) + "\n")
    except OSError:
        pass  # Optional evidence must not change operation results.
