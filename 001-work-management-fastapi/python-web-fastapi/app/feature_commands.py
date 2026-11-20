"""Generated CRUD mechanics; business permissions, reference scopes and creation rules are application hooks."""
from datetime import date
import hashlib
import json
import math

from fastapi import HTTPException
from teaql.runtime import BusinessOperation, BusinessOperationError
from . import auth_model as model
from .feature_bindings import SCHEMA, QUERIES, BY_ID, FILTERS, UPDATERS
from .feature_policy import REGISTRY, invoke
from .services.temporal import date_value
from .services.errors import ServiceError

ENTITIES = SCHEMA["entities"]
COMMANDS = {}


def field(name, key):
    return next(item for item in ENTITIES[name]["fields"] if item["name"] == key)


def value(name, entity, key):
    return getattr(entity, field(name, key)["member"])


def identifier(item):
    return getattr(item, "id", item)


async def read_one(context, name, entity_id):
    return await (BY_ID[name](QUERIES[name](), entity_id).comment("Read a command participant")
                  .purpose("Prepare application-owned business logic").execute_for_one(context))


async def related(context, name, via, parent_id, limit=10000):
    """Low-level query helper for trusted application policies, not an authorization decision."""
    return await (FILTERS[name][via](QUERIES[name](), parent_id).limit(limit)
                  .comment("Read an explicitly filtered relation")
                  .purpose("Evaluate an application query").execute_for_list(context))


async def allows(context, actor, name, action, entity=None, parent=None):
    policy = REGISTRY.policies[ENTITIES[name]["authorization"]]
    if await invoke(policy.allows, context, actor, action, entity, parent) is not True:
        raise HTTPException(403, "Action is not permitted")


async def scoped(context, actor, name, action, parent=None):
    policy = REGISTRY.policies[ENTITIES[name]["authorization"]]
    query = await invoke(policy.scope, context, actor, action, QUERIES[name](), parent)
    if not isinstance(query, type(QUERIES[name]())):
        raise TypeError("Policy must return the declared generated request: " + name)
    return query


async def accessible(context, actor, name, entity_id, action="read"):
    query = BY_ID[name](await scoped(context, actor, name, action), entity_id)
    entity = await (query.comment("Read a policy-scoped resource")
                    .purpose("Authorize a resource action").execute_for_one(context))
    if entity is None:
        raise HTTPException(404, "Resource not found")
    await allows(context, actor, name, action, entity)
    return entity


async def collection(context, actor, name, parent=None):
    await allows(context, actor, name, "list", parent=parent)
    query = await scoped(context, actor, name, "read", parent)
    container = ENTITIES[name]["container"]
    if container and parent is not None:
        query = FILTERS[name][container](query, parent.id)
    rows = await (query.limit(10000).comment("Read the authorized collection")
                  .purpose("Render a resource List view").execute_for_list(context))
    visible = []
    for row in rows:
        try: await allows(context, actor, name, "read", row, parent)
        except HTTPException as error:
            if error.status_code == 403: continue
            raise
        visible.append(row)
    return visible


async def container(context, name, parent_id):
    key = ENTITIES[name]["container"]
    if not key:
        return None
    parent = await read_one(context, field(name, key)["target"], parent_id)
    if parent is None:
        raise HTTPException(404, "Container not found")
    return parent


async def reference_query(context, actor, provider, target, parent=None, current=None):
    registration = REGISTRY.queries[provider]
    if registration.target != target:
        raise TypeError("Reference query target does not match " + target)
    query = await invoke(registration.query, context, actor, parent, current)
    if not isinstance(query, type(QUERIES[target]())):
        raise TypeError("Reference query returned the wrong generated request: " + provider)
    return query


async def candidates(context, actor, name, key, parent=None, current=None):
    target = field(name, key)["target"]
    query = await reference_query(context, actor, ENTITIES[name]["candidates"][key], target, parent, current)
    return await (query.limit(10000).comment("Read application-declared reference candidates")
                  .purpose("Populate an authorized reference control").execute_for_list(context))


def parse_field(data, raw):
    kind = data["kind"]
    if raw is None or raw == "":
        if data["nullable"]:
            return None
        if kind == "boolean":
            return False
        raise ValueError(data["label"] + " is required")
    if kind == "text":
        if not isinstance(raw, str) or len(raw) > 4000 or (not data["nullable"] and not raw.strip()):
            raise ValueError(data["label"] + " must contain valid text")
        return raw
    if kind == "boolean":
        if raw in (True, "true", "on", "1", 1): return True
        if raw in (False, "false", "0", 0): return False
        raise ValueError(data["label"] + " must be boolean")
    if kind == "date":
        try:
            return date_value(raw, field=data["label"], nullable=data["nullable"])
        except ServiceError as error:
            raise ValueError(str(error)) from error
    if kind == "number":
        text = str(raw)
        number = float(text) if any(char in text.lower() for char in ".e") else int(text)
        if isinstance(number, float) and not math.isfinite(number): raise ValueError("Number must be finite")
        return number
    if kind == "reference":
        ref = identifier(raw)
        if type(ref) is int:
            return ref
        if isinstance(ref, str) and ref.isdecimal():
            return int(ref)
        raise ValueError(data["label"] + " must be a record ID")
    raise ValueError("Unsupported form field: " + data["name"])


def parse_values(name, submitted, current=None):
    spec = ENTITIES[name]
    if set(submitted) - set(spec["editable"]): raise ValueError("Unlisted business input")
    result = {key: parse_field(field(name, key), submitted.get(key,
              value(name, current, key) if current is not None else spec["defaults"].get(key)))
              for key in spec["editable"]}
    for first, last in spec["date_orders"]:
        if result[first] and result[last] and result[first] > result[last]:
            raise ValueError(field(name, first)["label"] + " cannot be after " + field(name, last)["label"])
    return result


async def resolve_references(context, actor, name, values, parent=None, current=None):
    result = dict(values)
    for key, item in values.items():
        data = field(name, key)
        if data["kind"] != "reference" or item is None: continue
        query = await reference_query(context, actor, ENTITIES[name]["candidates"][key], data["target"], parent, current)
        selected = await (BY_ID[data["target"]](query, item).limit(1)
            .comment("Validate submitted reference against its candidate query")
            .purpose("Enforce application reference scope").execute_for_one(context))
        if selected is None: raise ValueError(data["label"] + " is not an allowed reference")
        result[key] = selected
    return result


async def initial_values(context, actor, name, parent=None, submitted=None):
    spec = ENTITIES[name]
    defaults = dict(spec["defaults"])
    hook = REGISTRY.creations.get(spec["create_handler"])
    if hook and hook.defaults:
        defaults.update(await invoke(hook.defaults, context, actor, parent, dict(submitted or {})))
    defaults.update(submitted or {})
    if set(defaults) - set(spec["editable"]): raise ValueError("Creation defaults must target editable fields")
    return defaults


async def prepare(context, name, parent, values):
    """Trusted application construction; callers supply business fields explicitly."""
    spec = ENTITIES[name]
    entity = (QUERIES[name]().comment("Prepare explicit business values")
              .purpose("Construct a command participant").new_entity(context))
    reserved = {spec["root"], spec["container"]}
    if set(values) & reserved: raise ValueError("Root/container relations are server-bound")
    if not field(name, spec["root"])["context_root"]:
        UPDATERS[name][spec["root"]](entity, await model.load_root(context))
    if spec["container"]: UPDATERS[name][spec["container"]](entity, parent)
    for key, item in values.items(): UPDATERS[name][key](entity, item)
    supplied = reserved | set(values)
    for data in spec["fields"]:
        if data["nullable"] and not data["managed"] and data["name"] not in supplied:
            UPDATERS[name][data["name"]](entity, None)
    return entity


def operation(name):
    spec = ENTITIES[name]
    hook = REGISTRY.creations.get(spec["create_handler"])

    async def participants(context, inputs):
        actor = await model.account_by_id(context, inputs["actor_id"])
        if actor is None: raise HTTPException(403, "Actor no longer exists")
        parent = await container(context, name, inputs["parent_id"])
        return actor, parent

    async def authorize(context, inputs):
        if context.user_identifier() != str(inputs["actor_id"]): return False
        actor, parent = await participants(context, inputs)
        try: await allows(context, actor, name, "create", parent=parent)
        except HTTPException: return False
        return True

    async def snapshot(context, inputs):
        actor, parent = await participants(context, inputs)
        return {"actor": actor, "parent": parent}

    async def handler(context, inputs):
        actor, parent = await participants(context, inputs)
        raw = await initial_values(context, actor, name, parent, json.loads(inputs["payload"]))
        values = await resolve_references(context, actor, name, parse_values(name, raw), parent)
        if hook and hook.handler:
            return await invoke(hook.handler, context, actor, parent, values)
        entity = await prepare(context, name, parent, values)
        await entity.audit_as("Create an owned record" if spec["primary"] else "Create declared resource").save(context)
        return {"id": entity.id}

    async def validate(context, inputs, before, result):
        if await read_one(context, name, result["id"]) is None: return False
        if hook and hook.validate:
            return await invoke(hook.validate, context, before["actor"], before["parent"], result) is True
        return True

    version = hashlib.sha256(json.dumps(SCHEMA, sort_keys=True).encode()).hexdigest()[:16] + (hook.version if hook else "")
    return BusinessOperation(name="Create:" + name, version=version, root_type=SCHEMA["root_type"],
        parameters={"actor_id": int, "parent_id": int, "payload": str},
        authorize=authorize, prepare=snapshot, handler=handler, validate=validate)


def configure():
    REGISTRY.validate(SCHEMA)
    COMMANDS.update({name: operation(name) for name, spec in ENTITIES.items() if spec["enabled"]})


async def create(context, actor, name, submitted, *, parent_id=0, key):
    if set(submitted) - set(ENTITIES[name]["editable"]): raise ValueError("Unlisted business input")
    payload = json.dumps({key: item.isoformat() if isinstance(item, date) else identifier(item)
                          for key, item in submitted.items()}, sort_keys=True)
    try:
        return await COMMANDS[name].execute(context, key=key,
            parameters={"actor_id": actor.id, "parent_id": parent_id, "payload": payload}, comment="Execute application creation command")
    except BusinessOperationError as error:
        if isinstance(error.__cause__, (ValueError, HTTPException)): raise error.__cause__
        raise


async def update(context, actor, name, entity, submitted):
    await accessible(context, actor, name, entity.id, "update")
    parent = await container(context, name, identifier(value(name, entity, ENTITIES[name]["container"]))) if ENTITIES[name]["container"] else None
    values = await resolve_references(context, actor, name, parse_values(name, submitted, entity), parent, entity)
    for key, item in values.items(): UPDATERS[name][key](entity, item)
    await entity.audit_as("Update validated declared fields").save(context)


async def delete(context, actor, name, entity):
    await accessible(context, actor, name, entity.id, "delete")
    await entity.mark_for_deletion().audit_as("Delete authorized declared resource").save(context)
