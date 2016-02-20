
import base64
import json
import asyncio
from hashlib import md5
import gzip

from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner

from settings import settings


class Component(ApplicationSession):

    @asyncio.coroutine
    def onJoin(self, details):
        yield from self.register(self.register_query, "com.estrom.register_query")

    @asyncio.coroutine
    def register_query(self, index, query):
        if not isinstance(query, dict):
            query = {
                "query_string": {
                    "query": query,
                }
            }
        query = {"query": query}
        qid = md5(json.dumps(query).encode()).hexdigest().encode()
        sid = base64.b32encode(index.encode()).decode().strip("=").encode() + b"_" + qid
        return sid


if __name__ == "__main__":
    cbs = settings.crossbar
    runner = ApplicationRunner(
        u"ws://{}:{}/ws".format(cbs.host, cbs.port),
        cbs.realm,
        debug=True,  # optional; log even more details
    )
    runner.run(Component)
