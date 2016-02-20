
import asyncio
from aiohttp import web
import aioes
import json
import base64

from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner

from settings import settings


class Component(ApplicationSession):

    @asyncio.coroutine
    def onJoin(self, details):
        ess = settings.es
        self.es = aioes.Elasticsearch(["{}:{}".format(ess.host, ess.port)])
        yield from self.es.ping()

        yield from self.setup_http_server()

    @asyncio.coroutine
    def consume(self, _index, _type, _source):
        rv = yield from self.es.percolate(_index, _type, body={"doc": _source})
        print(json.dumps(rv, indent=2))
        yield from self.notify(rv["matches"], _source)

    @asyncio.coroutine
    def notify(self, matches, source):
        for match in matches:
            index = match["_index"]
            qid = match["_id"]
            sid = base64.b32encode(index.encode()).decode().strip("=") + "_" + qid
            topic = settings.crossbar.ns + "." + sid
            self.publish(topic, source)
            print("Published to {}".format(topic))

    @asyncio.coroutine
    def post(self, request):
        data = yield from request.read()
        try:
            data = json.loads(data.decode())
        except ValueError:
            return web.Response(status=400)

        yield from self.consume(**data)  # FIXME: Too hacky
        return web.Response(status=204)

    def setup_http_server(self):
        self.app = web.Application()
        self.app.router.add_route("POST", "/beat", self.post)

        loop = asyncio.get_event_loop()
        handler = self.app.make_handler()
        bs = settings.beater
        yield from loop.create_server(handler, bs.host, bs.port)
        print("Http server ready")


if __name__ == "__main__":
    cbs = settings.crossbar
    runner = ApplicationRunner(
        u"ws://{}:{}/ws".format(cbs.host, cbs.port),
        cbs.realm,
        debug=True,  # optional; log even more details
    )
    runner.run(Component)
