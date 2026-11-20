import os
from contextlib import asynccontextmanager

from teaql.provider.sqlite import create_sqlite_service
from fastapi import FastAPI, Request

from teaql.runtime import UserContext
from runtime_module import GENERATED_RUNTIME_MODULE
from .services.errors import install_handlers
from .auth import install_auth
def sqlite_context(data_service) -> UserContext:
    context = UserContext.new().install(GENERATED_RUNTIME_MODULE)
    context.insert_resource("dataService", data_service)
    return context


@asynccontextmanager
async def lifespan(app: FastAPI):
    database = os.environ.get("TEAQL_DATABASE_CONNECTION_STRING") or os.environ.get("DATABASE_PATH") or "runtime-example.sqlite"
    app.state.data_service = create_sqlite_service(database)
    await sqlite_context(app.state.data_service).ensure_schema()
    await app.state.data_service.ensure_business_operation_schema()
    yield


app = FastAPI(title="work-management-service", lifespan=lifespan)
def trusted_context(request: Request) -> UserContext:
    context = sqlite_context(request.app.state.data_service)
    context.insert_resource("web_request", {
        "method": request.method,
        "path": request.url.path,
    })
    # Bind the actor, active root and policy from authenticated server-side state.
    # Never copy tenant/user/permissions/policies from request JSON.
    return context


@app.get("/health")
async def health(request: Request):
    trusted_context(request)
    return {"status": "UP"}
from .web_transport import install_frontend
install_frontend(app)
install_auth(app, trusted_context)
from .feature_policy import REGISTRY
from importlib import import_module
import_module(os.environ.get("TEAQL_APPLICATION_MODULE", "app.application")).configure(REGISTRY)
from .feature_web import install_features
install_features(app)

install_handlers(app)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=os.environ.get("HOST", "127.0.0.1"), port=int(os.environ.get("PORT", "8000")))