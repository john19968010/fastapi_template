import logging
import time
from typing import Any, Optional, Union


from starlette.background import BackgroundTask
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import HTTPConnection, Request
from starlette.responses import Response
from starlette.types import ASGIApp, Receive, Scope, Send
from starlette_context.plugins.base import Plugin
from uvicorn.protocols.utils import get_path_with_query_string


class RequestPlugin(Plugin):
    key: str = "request"

    async def process_request(
        self, request: Union[Request, HTTPConnection]
    ) -> Optional[Any]:
        return request


class LogRequestMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: ASGIApp,
    ) -> None:
        super().__init__(app)

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        # process the request and get the response
        start_time: float = time.time()
        response: Response = await call_next(request)
        process_time: float = time.time() - start_time

        response.headers["X-Process-Time"] = str(process_time)
        response.background = BackgroundTask(
            self.logging_time,
            request,
            response,
            process_time,
        )

        return response

    @staticmethod
    def logging_time(request: Request, response: Response, _time: float):
        log: logging.Logger = logging.getLogger("uvicorn.addition")

        log.info(
            '"%s %s HTTP/%s" in %s second, response bytes: %s',
            request.scope["method"],
            get_path_with_query_string(request.scope),
            request.scope["http_version"],
            f"{_time:.6f}",
            response.headers.get("Content-Length", 0),
        )
