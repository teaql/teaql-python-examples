"""Application registrations; containment never supplies permissions or candidate rules."""
from dataclasses import dataclass
from inspect import isawaitable


async def invoke(callback, *args):
    result = callback(*args)
    return await result if isawaitable(result) else result


@dataclass(frozen=True)
class AccessPolicy:
    scope: object
    allows: object


@dataclass(frozen=True)
class ReferenceQuery:
    target: str
    query: object


@dataclass(frozen=True)
class Creation:
    handler: object = None
    defaults: object = None
    validate: object = None
    version: str = "1"


class Registry:
    def __init__(self):
        self.policies = {}
        self.queries = {}
        self.creations = {}

    def policy(self, name, *, scope, allows):
        if not callable(scope) or not callable(allows):
            raise TypeError("Policies require scope and allows callbacks")
        self.policies[name] = AccessPolicy(scope, allows)

    def candidates(self, name, *, target, query):
        if not callable(query):
            raise TypeError("Reference queries require a query callback")
        self.queries[name] = ReferenceQuery(target, query)

    def creation(self, name, *, handler=None, defaults=None, validate=None, version="1"):
        for callback in (handler, defaults, validate):
            if callback is not None and not callable(callback):
                raise TypeError("Creation callbacks must be callable")
        self.creations[name] = Creation(handler, defaults, validate, version)

    def validate(self, schema):
        errors = []
        for name, spec in schema["entities"].items():
            if spec["enabled"] and spec["authorization"] not in self.policies:
                errors.append(f"MISSING_APPLICATION_POLICY: {name}: {spec['authorization']}")
            hook = spec["create_handler"]
            if hook and hook not in self.creations:
                errors.append(f"MISSING_APPLICATION_CREATION: {name}: {hook}")
            if spec["enabled"] and spec.get("application_required") and (not hook or hook not in self.creations or self.creations[hook].handler is None):
                errors.append(f"MISSING_CREATION_HANDLER: {name}: fields={spec['application_required']}")
            queries = [(field, provider) for field, provider in spec["candidates"].items()]
            if spec["group_query"]:
                queries.append((spec["group"], spec["group_query"]))
            for field, provider in queries:
                target = next(item["target"] for item in spec["fields"] if item["name"] == field)
                if provider not in self.queries or self.queries[provider].target != target:
                    errors.append(f"MISSING_APPLICATION_QUERY: {name}.{field}: {provider}, target={target}")
        if errors:
            raise RuntimeError("\n".join(errors))


REGISTRY = Registry()
