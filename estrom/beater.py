
import asyncio
from aiohttp import web
import aioes
import json
import base64

from autobahn.asyncio.wamp import ApplicationSession

from settings import settings as s
from .es import ESClient
from .utils import Hasher
from .logging import LoggerMixIn


class Component(LoggerMixIn, ApplicationSession):
    __logger_name__ = "Beater"

    @asyncio.coroutine
    def onJoin(self, details):
        self.esclient = ESClient()
        yield from self.esclient.connect()
        yield from self.setup_http_server()

        # FIXME: Use annotations on API methods and auto-register queries
        yield from self.register(self.register_query, s.crossbar.api_ns + ".register_query")
        self.logger.info("API Registered")

    @asyncio.coroutine
    def setup_http_server(self):
        self.app = web.Application()
        self.app.router.add_route("POST", "/beat", self.post)

        loop = asyncio.get_event_loop()
        handler = self.app.make_handler()
        sb = s.beater
        yield from loop.create_server(handler, sb.host, sb.port)
        self.logger.info("HTTP server ready")

    # API
    @asyncio.coroutine
    def register_query(self, index, query):
        self.logger.info("Registering")
        if not isinstance(query, dict):
            query = {
                "query_string": {
                    "query": query,
                }
            }
        query = {"query": query}
        sid = yield from self.esclient.register_percolator(index, query)
        self.logger.info("Registered query %s", sid)
        return sid

    @asyncio.coroutine
    def post(self, request):
        data = yield from request.read()
        try:
            data = json.loads(data.decode())
        except ValueError:
            return web.Response(status=400)

        yield from self.percolate(**data)  # FIXME: Too hacky
        return web.Response(status=204)

    @asyncio.coroutine
    def percolate(self, _index, _type, _source):
        rv = yield from self.esclient.es.percolate(_index, _type, body={"doc": _source})
        matches = rv["matches"]
        if self.logger.isEnabledFor(self.logger.DEBUG):
            self.logger.debug("Percolation result: %s", json.dumps(rv, indent=2))
        else:
            self.logger.info("Found %s matches", len(matches))
        yield from self.notify(matches, _source)

    @asyncio.coroutine
    def notify(self, matches, source):
        for match in matches:
            index = match["_index"]
            qid = match["_id"]
            sid = Hasher.index_qid_to_sid(index, qid)
            topic = s.crossbar.ns + "." + sid
            self.publish(topic, source)
            self.logger.info("Published to %s", topic)
