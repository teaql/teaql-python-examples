"""Check authentication without assuming any business entity, owner or CRUD routes."""
from contextlib import contextmanager
from http.cookiejar import CookieJar
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import HTTPCookieProcessor, ProxyHandler, build_opener
import os
import re
import secrets
import socket
import subprocess
import sys
import time



def require(condition, step):
    if not condition:
        raise RuntimeError(f"AUTH_SMOKE_FAILED: {step}")


def browser():
    return build_opener(ProxyHandler({}), HTTPCookieProcessor(CookieJar()))


def exercise(workspace, scratch):
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        port = listener.getsockname()[1]
    base = f"http://127.0.0.1:{port}"
    env = {**os.environ, "DATABASE_PATH": str(scratch / "fresh.sqlite3"),
           "TEAQL_EXAMPLE_SESSION_SECRET": secrets.token_hex(32),
           "HOST": "127.0.0.1", "PORT": str(port), "PYTHONDONTWRITEBYTECODE": "1"}
    env.pop("TEAQL_DATABASE_CONNECTION_STRING", None)

    def visit(client, path, values=None):
        data = None if values is None else urlencode(values).encode()
        try:
            response = client.open(base + path, data=data, timeout=4)
        except HTTPError as error:
            response = error
        with response:
            return response.status, response.url, response.read().decode()

    @contextmanager
    def server():
        log = scratch / f"server-{time.time_ns()}.log"
        with log.open("wb") as output:
            process = subprocess.Popen([sys.executable, "app.py"], cwd=workspace,
                                       env=env, stdout=output, stderr=subprocess.STDOUT)
            try:
                for _ in range(100):
                    require(process.poll() is None, "startup: process exited; inspect server log below")
                    try:
                        if visit(browser(), "/health")[0] == 200:
                            break
                    except URLError:
                        pass
                    time.sleep(0.1)
                else:
                    require(False, "startup: health endpoint did not become ready")
                yield
            finally:
                if process.poll() is None:
                    process.terminate()
                    try:
                        process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        process.kill()
                        process.wait(timeout=3)
                if sys.exc_info()[0] is not None:
                    print(log.read_text(errors="replace"), file=sys.stderr)

    alice, bob = browser(), browser()
    password = "smoke-test-password"
    account = {"name": "Alice", "email": "alice@example.com", "password": password}
    from .auth_model import ALLOW_SELF_REGISTRATION
    if not ALLOW_SELF_REGISTRATION:
        with server():
            require("Sign up" not in visit(alice, "/")[2], "registration link is closed")
            require(visit(alice, "/signup")[0] == 403, "registration page is closed")
            require(visit(alice, "/signup", account)[0] == 403, "registration write is closed")
            require(visit(alice, "/login", {"email": account["email"], "password": password})[0] == 401,
                    "unknown account cannot sign in")
        print("PASS default-closed registration and invalid login")
        return
    with server():
        require("Sign up" in visit(alice, "/")[2], "signup navigation")
        require("Sign out" in visit(alice, "/signup", account)[2], "register account")
        require(visit(bob, "/signup", account | {"email": "ALICE@example.com"})[0] == 409,
                "reject duplicate case-insensitive account")
    with server():
        require("Sign out" in visit(alice, "/")[2], "session survives restart")
        require("Sign in" in visit(alice, "/logout", {})[2], "logout")
        require(visit(alice, "/login", {"email": "ALICE@example.com", "password": "wrong"})[0] == 401,
                "reject invalid password")
        require("Sign out" in visit(alice, "/login", {"email": "ALICE@example.com", "password": password})[2],
                "case-insensitive login")

    logs = "\n".join(log.read_text() for log in scratch.glob("server-*.log"))
    require("auditReason='Register a workspace member'" in logs, "registration audit")
    require(password not in logs and "alice@example.com" not in logs, "audit masking")
    print("PASS signup, duplicate rejection, session restart, logout, login, and audit masking")


if __name__ == "__main__":
    with TemporaryDirectory(prefix="teaql-auth-smoke-") as temporary:
        exercise(Path(__file__).resolve().parent.parent, Path(temporary))
