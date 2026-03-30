import asyncio

from aiohttp import web 
import logging
import logging.handlers
import queue
import sys
from typing import Optional
try:
    import uvloop
except ImportError:
    uvloop = None


from codebara import bodyRoute, noBodyRoute  
#from codebara.errors import HttpOutputResponse

from aiohttp_middlewares import cors_middleware
from aiohttp_middlewares.cors import DEFAULT_ALLOW_HEADERS

class AsyncHTTPServer:
    """
    Serveur HTTP async haute charge - CORE
    """
    def __init__(
        self,
        host: str = "0.0.0.0",
        port: int = 8080,
        request_timeout: int = 25000000,
        max_body_size: int = 1 * 1024 * 1024,
        log_level: int = logging.DEBUG
    ):
        self.host = host
        self.port = port
        self.request_timeout = request_timeout
        self.max_body_size = max_body_size
        self.log_level = log_level
        if uvloop is not None:
            asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        #asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

        self.logger = self._setup_logger()
        self.app = self._create_app()

    # ======================================================
    # LOGGING ASYNC (NON BLOQUANT)
    # ======================================================

    def _setup_logger(self) -> logging.Logger:
        log_queue = queue.Queue(-1)

        queue_handler = logging.handlers.QueueHandler(log_queue)
        stream_handler = logging.StreamHandler(sys.stdout)

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )
        stream_handler.setFormatter(formatter)

        listener = logging.handlers.QueueListener(
            log_queue,
            stream_handler,
            respect_handler_level=True
        )
        listener.start()

        logger = logging.getLogger("http_core")
        logger.setLevel(self.log_level)
        logger.addHandler(queue_handler)
        logger.propagate = False

        return logger

    # ======================================================
    # MIDDLEWARE
    # ======================================================

    @web.middleware
    async def timeout_middleware(self, request: web.Request, handler):
        try:
            return await asyncio.wait_for(
                handler(request),
                timeout=self.request_timeout
            )
        except asyncio.TimeoutError:
            self.logger.warning(
                "408 Timeout | %s %s | %s",
                request.method,
                request.path,
                request.remote
            )
            return web.Response(status=408, text="Request Timeout")

    # ======================================================
    # HANDLERS HTTP
    # ======================================================
    async def handle_options(self, request: web.Request) -> web.Response:
        return web.Response(status=200)
    async def handle_get(self, request: web.Request) -> web.Response:
        #await asyncio.sleep(20)  # > REQUEST_TIMEOUT
        self.logger.info(
            "GET %s | from %s | %s | headers=%d",
            request.path,
            request.remote,
            request.headers,
            len(request.headers)
        )
        for k, v in request.headers.items():
            self.logger.debug("HEADER %s=%s", k, v)
        #await routes.get(request,self.getQueryValue(request=request))
        #resp=
        resp=await noBodyRoute(request=request,queryArray=self.getQueryValue(request=request))
        self.logger.info("end %s", request.method)
        return resp#web.Response(text="OK")

    async def handle_with_body(self, request: web.Request) -> web.Response:
        body = await request.read()
        returnedError:web.Response=web.Response(status=404) #'{"status":200, "ok":true}'
        self.logger.info(
            "%s %s | from %s | %s | body_size=%d",
            request.method,
            request.path,
            request.remote,
            body,
            len(body)
        )

        self.logger.debug(
            "BODY %s",
            body.decode(errors="replace")
        )

        queryArray=self.getQueryValue(request=request)

        returnedError=await bodyRoute(request=request,body=body,queryArray=queryArray)
        self.logger.info("end %s", request.method)
        #self.logger.info(returnedError)
        #return web.Response(text=returnedError.toJson(), status=returnedError.status)
        return returnedError
    # ======================================================
    # APP FACTORY
    # ======================================================

    def _create_app(self) -> web.Application:
        app = web.Application(
            middlewares=[self.timeout_middleware, cors_middleware(  origins=["http://localhost:8081","http://localhost:5173"],
                                                                    allow_methods=("POST", "PATCH","PUT", "DELETE", "GET","OPTIONS"),
                                                                    allow_headers=DEFAULT_ALLOW_HEADERS+ ("email","token","datas")
                                                                  )
                                                                  ],
            client_max_size=self.max_body_size
        )
        app.router.add_options("/{path:.*}", self.handle_options)
        app.router.add_get("/{path:.*}", self.handle_get)
        app.router.add_post("/{path:.*}", self.handle_with_body)
        app.router.add_put("/{path:.*}", self.handle_with_body)
        app.router.add_patch("/{path:.*}", self.handle_with_body)
        app.router.add_delete("/{path:.*}", self.handle_with_body)

        return app

    # ======================================================
    # PUBLIC API
    # ======================================================

    def run(self):
        self.logger.info(
            "🚀 HTTP server running on http://%s:%d | timeout=%ds",
            self.host,
            self.port,
            self.request_timeout
        )

        web.run_app(
            self.app,
            host=self.host,
            port=self.port,
            reuse_port=(sys.platform != "win32"),
            access_log=None
        )

    def shutdown(self, signal_name: Optional[str] = None):
        self.logger.warning("🛑 Server shutdown (%s)", signal_name)
        sys.exit(0)

    def getQueryValue(self,request :web.Request):
        values:dict={}
        if len(request.query_string)==0:
            return values
        qs=str(request.query_string)
        splitvals=qs.split('&')
        for val in splitvals:
            kv=val.split('=')
            values[kv[0]]=kv[1]
        return values