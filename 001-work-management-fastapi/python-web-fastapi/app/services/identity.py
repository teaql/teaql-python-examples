"""Trusted identity and deny-by-default service policy; never inferred from request fields."""
from inspect import isawaitable
from fastapi import Request
from teaql.runtime import UserContext
from .errors import AuthenticationRequired, AccessDenied, ServiceConfigurationError
from ._usage import record

ACTOR = "workspace.service_actor"
POLICY = "workspace.service_policy"


async def invoke(callback, *args):
    result = callback(*args)
    return await result if isawaitable(result) else result


def bind_actor(context, actor):
    """Server/test construction only. Obtain HTTP actors from the trusted session loader."""
    identifier = getattr(actor, "id", None)
    if not isinstance(context, UserContext) or identifier is None:
        raise AuthenticationRequired("A trusted actor and UserContext are required")
    if context.user_identifier() != str(identifier):
        raise AuthenticationRequired("Actor does not match the trusted context")
    context.insert_resource(ACTOR, actor)
    return context


def actor(context):
    if not isinstance(context, UserContext):
        raise AuthenticationRequired("One trusted UserContext is required")
    value = context.get_resource(ACTOR)
    if value is None or context.user_identifier() != str(getattr(value, "id", None)):
        raise AuthenticationRequired("Bind the authenticated actor before calling a data service")
    return value


def install_policy(context, policy):
    if not callable(getattr(policy, "scope", None)) or not callable(getattr(policy, "allows", None)):
        raise ServiceConfigurationError("Service policy requires scope and allows callbacks")
    context.insert_resource(POLICY, policy)
    return context


def policy_for(context):
    actor(context)
    policy = context.get_resource(POLICY)
    if policy is None:
        raise AccessDenied("No application service policy is configured; access is closed")
    return policy


async def authorize(context, entity, action, current=None, changes=None):
    policy = policy_for(context)
    if await invoke(policy.allows, context, actor(context), entity, action, current, changes) is not True:
        raise AccessDenied("The application policy refused this action")
    record("data", action, entity)


async def scoped_query(context, entity, action, query):
    policy = policy_for(context)
    scoped = await invoke(policy.scope, context, actor(context), entity, action, query)
    if not isinstance(scoped, type(query)):
        raise ServiceConfigurationError("Policy scope must return the same generated request type: " + entity)
    return scoped


async def reference_query(context, entity, field, query, current=None):
    policy = policy_for(context)
    callback = getattr(policy, "reference_scope", None)
    if not callable(callback):
        raise AccessDenied("No reference candidate scope is configured: " + entity + "." + field)
    scoped = await invoke(callback, context, actor(context), entity, field, query, current)
    if not isinstance(scoped, type(query)):
        raise ServiceConfigurationError("Reference scope returned the wrong request type: " + entity + "." + field)
    return scoped


async def service_context(request: Request) -> UserContext:
    loader = getattr(request.app.state, "teaql_current", None)
    if loader is None:
        raise AuthenticationRequired("Authentication is not configured")
    trusted_actor, context = await loader(request)
    bind_actor(context, trusted_actor)
    policy = getattr(request.app.state, "workspace_service_policy", None)
    if policy is not None: install_policy(context, policy)
    return context
