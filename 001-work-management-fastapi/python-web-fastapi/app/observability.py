"""Join FastAPI requests and application operations to TeaQL's own telemetry."""

from contextlib import contextmanager

from teaql.runtime.telemetry import RuntimeOperation, start_runtime_operation
from teaql.runtime.telemetry_startup import default_telemetry


class TraceRequests:
    def __init__(self, app, tracer):
        self.app = app
        self.tracer = tracer

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http" or not scope["path"].startswith("/api/"):
            await self.app(scope, receive, send)
            return

        from opentelemetry.trace import SpanKind, StatusCode

        method = scope["method"]
        with self.tracer.start_as_current_span(
            method, kind=SpanKind.SERVER, record_exception=False, set_status_on_exception=False
        ) as span:
            span.set_attribute("http.request.method", method)
            trace_id = f"{span.get_span_context().trace_id:032x}".encode("ascii")

            async def send_with_trace_id(message):
                if message["type"] == "http.response.start":
                    status = message["status"]
                    span.set_attribute("http.response.status_code", status)
                    if status >= 500:
                        span.set_status(StatusCode.ERROR)
                    message = {
                        **message,
                        "headers": [*message.get("headers", ()), (b"x-teaql-trace-id", trace_id)],
                    }
                await send(message)

            try:
                await self.app(scope, receive, send_with_trace_id)
            except Exception:
                span.set_status(StatusCode.ERROR)
                raise
            finally:
                route = getattr(scope.get("route"), "path", None)
                if route:
                    span.set_attribute("http.route", route)
                    span.update_name(f"{method} {route}")


def install(app):
    tracer = getattr(default_telemetry(), "tracer", None)
    if tracer is not None:
        app.add_middleware(TraceRequests, tracer=tracer)


@contextmanager
def observe_business_step(context, name):
    """Record a step's outcome using a code-defined action name."""
    scope = start_runtime_operation(context.operation_telemetry(), RuntimeOperation("business", name))
    try:
        yield
    except BaseException as error:
        scope.failure(error)
        raise
    else:
        scope.success()
