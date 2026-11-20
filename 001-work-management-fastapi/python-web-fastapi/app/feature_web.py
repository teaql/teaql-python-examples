"""Generated presentation; application policy and query hooks supply business meaning."""
from html import escape
import json
import logging
import os
import secrets

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from teaql.runtime import BusinessOperationError
from .auth import current_identity, Identity
from .auth import form, page, logout_form
from .web_transport import api_request, browser_shell, destination, json_fields, private_response
from . import feature_commands as commands

ENTITIES = commands.ENTITIES
SCHEMA = commands.SCHEMA


def spec_for(name):
    spec = ENTITIES.get(name)
    if spec is None or not spec["enabled"] or spec["primary"]: raise HTTPException(404, "Resource not found")
    return spec


def title(name, entity):
    return str(commands.value(name, entity, ENTITIES[name]["title"]))


def display(data, raw, labels=None):
    if raw is None: return ""
    if data["kind"] == "reference": return (labels or {}).get(commands.identifier(raw), str(commands.identifier(raw)))
    if data["kind"] == "boolean": return "Yes" if raw else "No"
    return str(raw)


async def permitted(identity, name, action, entity=None, parent=None):
    try:
        await commands.allows(identity.context, identity.actor, name, action, entity, parent)
        return True
    except HTTPException as error:
        if error.status_code == 403: return False
        raise


async def home_permitted(identity, name, action, trace):
    allowed = await permitted(identity, name, action)
    if trace and not allowed:
        policy = ENTITIES[name]["authorization"]
        callback = commands.REGISTRY.policies[policy].allows
        event = {"trace": trace, "entity": name, "policy": policy, "action": action,
                 "callback": getattr(callback, "__qualname__", type(callback).__name__),
                 "entity_argument": None, "parent_argument": None}
        logging.getLogger(__name__).warning("TEAQL_HOME_DENIAL %s", json.dumps(event))
    return allowed


async def record_form_data(name, identity, *, entity=None, parent=None, submitted=None):
    spec = ENTITIES[name]
    create = entity is None
    base = f"/crud/{name}"
    action = f"{base}/{parent.id if parent else 0}/create" if create else f"{base}/{entity.id}"
    editable = create or await permitted(identity, name, "update", entity, parent)
    deletable = not create and await permitted(identity, name, "delete", entity, parent)
    defaults = await commands.initial_values(identity.context, identity.actor, name, parent) if create else {}
    fields = []
    for key in spec["editable"]:
        data = commands.field(name, key)
        raw = defaults.get(key) if create else commands.value(name, entity, key)
        if submitted and key in submitted:
            raw = submitted[key]
        options = []
        if data["kind"] == "reference" and editable:
            rows = await commands.candidates(identity.context, identity.actor, name, key, parent, entity)
            options = [{"id": str(row.id), "label": title(data["target"], row)} for row in rows]
        if data["kind"] == "reference" and raw is not None:
            raw = str(commands.identifier(raw))
        fields.append({"name": key, "label": data["label"], "kind": "multiline" if key in spec["multiline"] else data["kind"],
                       "value": raw,
                       "required": not data["nullable"], "options": options})
    return {"label": spec["label"], "fields": fields, "action": action if editable else None,
            "submit": "Create " + spec["label"] if create else "Save changes",
            "delete": action + "/delete" if deletable else None,
            "commandKey": secrets.token_urlsafe(24) if create else None}


def legacy_form(view, message=""):
    controls = []
    for field in view["fields"]:
        key, label, kind = field["name"], escape(field["label"]), field["kind"]
        raw = field["value"]
        current = escape(str(raw) if raw is not None else "", quote=True)
        required = " required" if field["required"] else ""
        if not view["action"]:
            contents = display({"kind": kind}, raw)
            controls.append(f"<dt>{label}</dt><dd>{escape(contents)}</dd>")
            continue
        if kind == "reference":
            options = ['<option value="">Choose…</option>']
            for option in field["options"]:
                selected = " selected" if str(raw) == option["id"] else ""
                options.append(f'<option value="{option["id"]}"{selected}>{escape(option["label"])}</option>')
            control = f'<select name="{key}"{required}>' + "".join(options) + '</select>'
        elif kind == "boolean":
            checked = ' checked' if raw in (True, 1, "1", "on", "true") else ''
            control = f'<input type="checkbox" name="{key}" value="1"{checked}>'
        elif kind == "multiline":
            control = f'<textarea name="{key}" maxlength="4000"{required}>{current}</textarea>'
        else:
            input_type = kind if kind in ("date", "number") else "text"
            step = ' step="any"' if kind == "number" else ""
            control = f'<input name="{key}" type="{input_type}" value="{current}"{required}{step} maxlength="4000">'
        controls.append(f'<label>{label} {control}</label>')
    markup = "".join(controls)
    if view["action"]:
        key = view["commandKey"] or ""
        markup = (f'<form class="teaql-fields" method="post" action="{view["action"]}">{markup}'
                  f'<input type="hidden" name="_full_form" value="1"><input type="hidden" name="command_key" value="{key}">'
                  f'<button>{escape(view["submit"])}</button></form>')
    else:
        markup = "<dl>" + markup + "</dl>"
    if view["delete"]:
        markup += f'<form method="post" action="{view["delete"]}"><button>Delete {escape(view["label"])}</button></form>'
    return (f'<p role="alert">{escape(message)}</p>' if message else "") + markup


async def collection_data(identity, parent_name=None, parent=None, trace=None):
    result = []
    for name, spec in ENTITIES.items():
        via = spec["container"]
        if not spec["enabled"] or (commands.field(name, via)["target"] if via else None) != parent_name:
            continue
        async def allowed(action):
            if parent is None:
                return await home_permitted(identity, name, action, trace)
            return await permitted(identity, name, action, parent=parent)
        if not await allowed("list"):
            continue
        entries = await commands.collection(identity.context, identity.actor, name, parent)
        base = f"/crud/{name}"
        create = f"{base}/{parent.id if parent else 0}/new" if await allowed("create") else None
        listing = {"label": spec["label"], "create": create}
        if parent is None:
            listing["links"] = [{"href": f"{base}/{row.id}", "label": title(name, row)} for row in entries]
        else:
            listing.update(await grouped_rows(identity, name, spec, parent, entries))
        result.append(listing)
    return result


async def grouped_rows(identity, name, spec, parent, entries):
    labels = {}
    for key in spec["candidates"]:
        data = commands.field(name, key)
        rows = await commands.candidates(identity.context, identity.actor, name, key, parent)
        labels[key] = {row.id: title(data["target"], row) for row in rows}
    group_key = spec["group"]
    group_labels = {}
    if group_key and spec["group_query"]:
        target = commands.field(name, group_key)["target"]
        query = await commands.reference_query(identity.context, identity.actor, spec["group_query"], target, parent)
        rows = await (query.limit(10000).comment("Read declared presentation groups")
                      .purpose("Render empty and populated groups").execute_for_list(identity.context))
        group_labels.update({row.id: title(target, row) for row in rows})
    keys = [spec["title"]] + [key for key in spec["editable"] if key != spec["title"]]
    groups = {key: {"label": label, "rows": []} for key, label in group_labels.items()}
    if not group_key:
        groups[None] = {"label": spec["label"], "rows": []}
    for row in entries:
        group = commands.identifier(commands.value(name, row, group_key)) if group_key else None
        if group not in groups:
            groups[group] = {"label": display(commands.field(name, group_key), group, labels.get(group_key)), "rows": []}
        cells = [display(commands.field(name, key), commands.value(name, row, key), labels.get(key)) for key in keys]
        groups[group]["rows"].append({"href": f"/crud/{name}/{row.id}", "cells": cells})
    return {"columns": [commands.field(name, key)["label"] for key in keys], "groups": list(groups.values())}


def legacy_collections(collections, *, home=False):
    markup = "" if home else "<h2>List</h2>"
    for item in collections:
        label = escape(item["label"])
        if home:
            markup += f"<h2>{label}</h2>"
        if item["create"]:
            markup += f'<p><a href="{item["create"]}">Create {label}</a></p>'
        if home:
            markup += "<ul>" + "".join(f'<li><a href="{link["href"]}">{escape(link["label"])}</a></li>'
                                       for link in item["links"]) + "</ul>"
            continue
        headers = "".join(f"<th>{escape(key)}</th>" for key in item["columns"])
        for group in item["groups"]:
            markup += f'<h3>{escape(group["label"])}</h3><div class="teaql-table"><table><thead><tr>{headers}</tr></thead><tbody>'
            for row in group["rows"]:
                cells = [escape(str(cell)) for cell in row["cells"]]
                cells[0] = f'<a href="{row["href"]}">{cells[0]}</a>'
                markup += "<tr>" + "".join(f"<td>{cell}</td>" for cell in cells) + "</tr>"
            markup += "</tbody></table></div>"
    return markup


async def posted(request, spec, *, creation=False):
    keys = spec["editable"]
    if api_request(request):
        data = await json_fields(request, keys)
        key = request.headers.get("Idempotency-Key", "")
        if creation and not 1 <= len(key) <= 200:
            raise HTTPException(400, "Provide an Idempotency-Key of 1–200 characters")
        return data, key
    values = await form(request, *keys, "command_key", "_full_form", missing=None)
    data = {key: item for key, item in zip(keys, values[:-2]) if item is not None}
    if values[-1] == "1":
        for key in keys:
            if commands.field(spec["name"], key)["kind"] == "boolean" and key not in data: data[key] = False
    return data, values[-2] or secrets.token_urlsafe(24)


async def detail_destination(context, actor, name, entity_id):
    try: await commands.accessible(context, actor, name, entity_id)
    except HTTPException as error:
        if error.status_code in (403, 404): return "/saved"
        raise
    return f"/records/{entity_id}" if name == SCHEMA["primary"] else f"/crud/{name}/{entity_id}"


def install_features(app):
    api = APIRouter(prefix="/api", dependencies=[Depends(private_response)])
    commands.configure()
    primary = SCHEMA["primary"]

    @app.exception_handler(BusinessOperationError)
    async def operation_error(request, error):
        status = 409 if error.code == "IDEMPOTENCY_CONFLICT" else 403 if error.code == "OPERATION_DENIED" else 500
        if error.outcome == "unknown": status = 503
        logging.getLogger(__name__).error("Business operation failed: %s/%s", error.code, error.outcome, exc_info=error)
        return JSONResponse({"detail": "Business operation did not complete normally", "code": error.code, "outcome": error.outcome}, status_code=status)

    app.state.teaql_commands = commands.COMMANDS
    if primary:
        from .crud_example import record_form
        from . import crud_model as model
        async def create_primary(context, actor, name, key):
            result = await commands.create(context, actor, primary, {ENTITIES[primary]["editable"][0]: name}, key=key)
            return result["id"]

        async def primary_view(request, context, entity):
            identity = await current_identity(request)
            body = '<p><a href="/">Your records</a></p>' + legacy_collections(await collection_data(identity, primary, entity))
            path = f"/records/{entity.id}"
            if await permitted(identity, primary, "update", entity):
                body += '<details><summary>Settings</summary>' + record_form(path, "Save", title(primary, entity)) + '</details>'
            if await permitted(identity, primary, "delete", entity):
                body += f'<form method="post" action="{path}/delete"><button>Delete {escape(model.LABEL)}</button></form>'
            return page(title(primary, entity), body)

        app.state.teaql_create_resource = create_primary
        app.state.teaql_resource_view = primary_view
        app.state.teaql_find_resource = lambda context, actor, entity_id, action: commands.accessible(context, actor, primary, entity_id, action)
        app.state.teaql_list_resources = lambda context, actor: commands.collection(context, actor, primary)
        app.state.teaql_new_resource = lambda context, actor: commands.allows(context, actor, primary, "create")
        app.state.teaql_create_destination = lambda context, actor, entity_id: detail_destination(context, actor, primary, entity_id)
        app.state.teaql_deleted_destination = "/saved"

    else:
        async def home(request):
            identity = await current_identity(request)
            trace = secrets.token_hex(12) if os.getenv("TEAQL_HOME_POLICY_TRACE") == "1" else None
            collections = await collection_data(identity, trace=trace)
            if api_request(request):
                return {"kind": "home", "collections": collections, "trace": trace}
            body = f'<span hidden data-teaql-home-trace="{trace}"></span>' if trace else ""
            body += legacy_collections(collections, home=True)
            body += logout_form()
            return page("Your records", body)
        app.state.teaql_homepage = home

    @api.get("/saved")
    @app.get("/saved")
    async def saved(request: Request, identity: Identity = Depends(current_identity)):
        if shell := browser_shell(request): return shell
        if api_request(request): return {"kind": "saved"}
        return page("Saved", "<p>Your change has been saved.</p>")

    @api.get("/crud/{name}/{parent_id}/new")
    @app.get("/crud/{name}/{parent_id}/new")
    async def new(request: Request, name: str, parent_id: int, identity: Identity = Depends(current_identity)):
        spec_for(name)
        parent = await commands.container(identity.context, name, parent_id)
        await commands.allows(identity.context, identity.actor, name, "create", parent=parent)
        if shell := browser_shell(request): return shell
        heading = "Create " + ENTITIES[name]["label"]
        view = await record_form_data(name, identity, parent=parent)
        if api_request(request):
            return {"kind": "record", "title": heading, "form": view, "collections": []}
        return page(heading, legacy_form(view))

    @api.post("/crud/{name}/{parent_id}/create")
    @app.post("/crud/{name}/{parent_id}/create")
    async def create(request: Request, name: str, parent_id: int, identity: Identity = Depends(current_identity)):
        spec = spec_for(name)
        data, key = await posted(request, spec, creation=True)
        try:
            result = await commands.create(identity.context, identity.actor, name, data, parent_id=parent_id, key=key)
        except ValueError as error:
            if api_request(request): raise HTTPException(400, str(error)) from error
            parent = await commands.container(identity.context, name, parent_id)
            response = page("Create " + spec["label"], legacy_form(
                await record_form_data(name, identity, parent=parent, submitted=data), str(error)))
            response.status_code = 400
            return response
        return destination(request, await detail_destination(identity.context, identity.actor, name, result["id"]))

    @api.get("/crud/{name}/{entity_id}")
    @app.get("/crud/{name}/{entity_id}")
    async def details(request: Request, name: str, entity_id: int, identity: Identity = Depends(current_identity)):
        spec = spec_for(name)
        entity = await commands.accessible(identity.context, identity.actor, name, entity_id)
        parent = await commands.container(identity.context, name, commands.identifier(commands.value(name, entity, spec["container"]))) if spec["container"] else None
        if shell := browser_shell(request): return shell
        view = await record_form_data(name, identity, entity=entity, parent=parent)
        children = await collection_data(identity, name, entity)
        if api_request(request):
            return {"kind": "record", "title": title(name, entity), "form": view, "collections": children}
        return page(title(name, entity), legacy_form(view) + legacy_collections(children))

    @api.post("/crud/{name}/{entity_id}")
    @app.post("/crud/{name}/{entity_id}")
    async def update(request: Request, name: str, entity_id: int, identity: Identity = Depends(current_identity)):
        spec = spec_for(name)
        entity = await commands.accessible(identity.context, identity.actor, name, entity_id, "update")
        data, _ = await posted(request, spec)
        try: await commands.update(identity.context, identity.actor, name, entity, data)
        except ValueError as error:
            if api_request(request): raise HTTPException(400, str(error)) from error
            parent = await commands.container(identity.context, name, commands.identifier(commands.value(name, entity, spec["container"]))) if spec["container"] else None
            response = page(title(name, entity), legacy_form(
                await record_form_data(name, identity, entity=entity, parent=parent, submitted=data), str(error)))
            response.status_code = 400
            return response
        return destination(request, await detail_destination(identity.context, identity.actor, name, entity_id))

    @api.post("/crud/{name}/{entity_id}/delete")
    @app.post("/crud/{name}/{entity_id}/delete")
    async def delete(request: Request, name: str, entity_id: int, identity: Identity = Depends(current_identity)):
        spec = spec_for(name)
        entity = await commands.accessible(identity.context, identity.actor, name, entity_id, "delete")
        await form(request)
        parent_id = commands.identifier(commands.value(name, entity, spec["container"])) if spec["container"] else 0
        parent_name = commands.field(name, spec["container"])["target"] if spec["container"] else ""
        await commands.delete(identity.context, identity.actor, name, entity)
        location = f"/records/{parent_id}" if primary and parent_name == primary else f"/crud/{parent_name}/{parent_id}" if parent_name else "/"
        if parent_name:
            try: await commands.accessible(identity.context, identity.actor, parent_name, parent_id)
            except HTTPException as error:
                if error.status_code in (403, 404): location = "/saved"
                else: raise
        return destination(request, location)

    if getattr(app.state, "react_ui", False):
        app.include_router(api)
