"""Generated account authentication independent of business resources."""
import asyncio
from hashlib import pbkdf2_hmac
from hmac import compare_digest, digest
from html import escape
import os
from pathlib import Path
import secrets
import time
from urllib.parse import parse_qs

from dataclasses import dataclass
from typing import Any
from teaql.runtime import UserContext

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import FileResponse, HTMLResponse, Response

from . import auth_model as model
from .web_transport import api_request, body, browser_shell, destination, json_fields, private_response
from .services.identity import bind_actor, install_policy

COOKIE = "teaql_example_session"
SESSION_AGE = 86400
DUMMY_HASH = "0" * 32 + ":" + "0" * 64
THEME_URL = "/teaql-theme.css"
THEME_FILE = Path(__file__).resolve().parents[1] / "theme.css"


def password_hash(password, salt):
    return pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), 600_000).hex()


def password_matches(password, encoded):
    try:
        salt, expected = encoded.split(":", 1)
        return compare_digest(password_hash(password, salt), expected)
    except (AttributeError, ValueError):
        return False


async def form(request, *fields, missing=""):
    if api_request(request):
        data = await json_fields(request, fields)
        if not all(isinstance(value, str) for value in data.values()):
            raise HTTPException(400, "Expected text fields")
        return [data.get(field, missing) for field in fields]
    payload = await body(request, "application/x-www-form-urlencoded")
    try:
        data = parse_qs(payload.decode(), max_num_fields=20, keep_blank_values=True)
    except ValueError as error:
        raise HTTPException(400, "Invalid form") from error
    return [data.get(field, [missing])[0] for field in fields]


def page(title, contents):
    return HTMLResponse(f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title><style>
body {{font: 1rem system-ui; max-width: 42rem; margin: 3rem auto; padding: 0 1rem}}
label {{display: block; margin: .75rem 0}} input, button {{font: inherit}}
</style><link rel="stylesheet" href="{THEME_URL}"></head>
<body><main class="teaql-page"><h1>{escape(title)}</h1>{contents}</main></body></html>""")


def logout_form(label="Sign out"):
    """Use the POST authentication contract from application-owned navigation."""
    return f'<form method="post" action="/logout"><button>{escape(label)}</button></form>'


def auth_page(signup=False, message="", status=200):
    title = "Sign up" if signup else "Sign in"
    action = "/signup" if signup else "/login"
    name_field = '<label>Name <input name="name" required maxlength="120"></label>' if signup else ""
    link = '<a href="/">Sign in</a>' if signup else '<a href="/signup">Sign up</a>' if model.ALLOW_SELF_REGISTRATION else ""
    response = page(title, f"""
<p role="status">{escape(message)}</p>
<form method="post" action="{action}">{name_field}
<label>Email <input name="email" type="email" required maxlength="254"></label>
<label>Password <input name="password" type="password" required maxlength="256"></label>
<button>{title}</button></form><p>{link}</p>""")
    response.status_code = status
    return response



@dataclass(frozen=True)
class Identity:
    actor: Any
    context: UserContext


async def current_identity(request: Request) -> Identity:
    actor, context = await request.app.state.teaql_current(request)
    return Identity(actor, context)


async def current_actor(request: Request):
    return (await current_identity(request)).actor


async def current_context(request: Request) -> UserContext:
    return (await current_identity(request)).context


def install_auth(app, trusted_context):
    api = APIRouter(prefix="/api", dependencies=[Depends(private_response)])
    # Use a stable secret to keep existing sessions valid after a process restart.
    configured = os.environ.get("TEAQL_EXAMPLE_SESSION_SECRET")
    secret = configured.encode() if configured else secrets.token_bytes(32)
    accounts_lock = asyncio.Lock()

    @app.get(THEME_URL, include_in_schema=False)
    async def theme_stylesheet():
        headers = {"Cache-Control": "no-store", "X-Content-Type-Options": "nosniff"}
        if THEME_FILE.is_file():
            return FileResponse(THEME_FILE, media_type="text/css", headers=headers)
        return Response(media_type="text/css", headers=headers)

    def ctx(request, actor=None):
        context = getattr(request.state, "teaql_context", None)
        if context is None:
            context = model.bind_context(trusted_context(request), actor)
            request.state.teaql_context = context
        elif actor is not None:
            model.bind_context(context, actor)
        return context

    def signature(payload):
        return digest(secret, payload.encode(), "sha256").hex()

    def signed_in(request, user):
        payload = f"{user.id}:{int(time.time()) + SESSION_AGE}"
        response = destination(request, "/")
        response.set_cookie(COOKIE, f"{payload}:{signature(payload)}", max_age=SESSION_AGE,
                            secure=request.url.scheme == "https", httponly=True, samesite="strict")
        return response

    async def actor(request):
        try:
            payload, submitted = request.cookies.get(COOKIE, "").rsplit(":", 1)
            identifier, expires = (int(part) for part in payload.split(":"))
            if expires <= time.time() or not compare_digest(signature(payload), submitted):
                return None
        except (TypeError, ValueError):
            return None
        return await model.account_by_id(ctx(request, identifier), identifier)

    async def current(request):
        cached = getattr(request.state, "teaql_current", None)
        if cached is not None:
            return cached
        user = await actor(request)
        if user is None:
            raise HTTPException(401, "Sign in first")
        context = bind_actor(ctx(request, user.id), user)
        policy = getattr(app.state, "workspace_service_policy", None)
        if policy is not None: install_policy(context, policy)
        identity = (user, context)
        request.state.teaql_current = identity
        return identity

    app.state.teaql_current = current

    app.state.teaql_context = ctx
    app.state.teaql_actor = actor

    @api.get("/")
    @app.get("/", response_class=HTMLResponse)
    async def home(request: Request):
        if shell := browser_shell(request):
            return shell
        user = await actor(request)
        if user is None:
            if api_request(request):
                return {"kind": "login", "signup": model.ALLOW_SELF_REGISTRATION}
            return auth_page()
        render = getattr(app.state, "teaql_homepage", None)
        if render is not None:
            return await render(request)
        if api_request(request):
            return {"kind": "home", "collections": []}
        return page("Signed in", logout_form())

    @api.get("/signup")
    @app.get("/signup", response_class=HTMLResponse)
    async def signup_page(request: Request):
        if not model.ALLOW_SELF_REGISTRATION: raise HTTPException(403, "Self registration is disabled")
        if shell := browser_shell(request):
            return shell
        if api_request(request):
            return {"kind": "signup"}
        return auth_page(signup=True)

    def rejected(request, message, status, signup=False):
        if api_request(request):
            raise HTTPException(status, message)
        return auth_page(signup=signup, message=message, status=status)

    @api.post("/signup")
    @app.post("/signup")
    async def signup(request: Request):
        if not model.ALLOW_SELF_REGISTRATION: raise HTTPException(403, "Self registration is disabled")
        name, address, password = await form(request, "name", "email", "password")
        address = address.strip().casefold()
        if not (1 <= len(name.strip()) <= 120 and len(address) <= 254 and
                "@" in address and not any(char.isspace() for char in address) and 6 <= len(password) <= 256):
            return rejected(request, "Enter a name, email and a password of at least 6 characters.", 400, signup=True)
        salt = secrets.token_hex(16)
        hashed = await run_in_threadpool(password_hash, password, salt)
        context = ctx(request)
        async with accounts_lock:
            if await model.account_by_email(context, address) is not None:
                return rejected(request, "That email is already registered.", 409, signup=True)
            user = await model.create_account(context, name.strip(), address, f"{salt}:{hashed}")
        return signed_in(request, user)

    @api.post("/login")
    @app.post("/login")
    async def login(request: Request):
        address, password = await form(request, "email", "password")
        user = await model.account_by_email(ctx(request), address.strip().casefold())
        encoded = model.credential(user) if user is not None else DUMMY_HASH
        valid = await run_in_threadpool(password_matches, password, encoded)
        if user is None or not valid:
            return rejected(request, "Email or password is incorrect.", 401)
        return signed_in(request, user)

    @api.post("/logout")
    @app.post("/logout")
    async def logout(request: Request):
        await form(request)
        response = destination(request, "/")
        response.delete_cookie(COOKIE)
        return response

    if getattr(app.state, "react_ui", False):
        app.include_router(api)
