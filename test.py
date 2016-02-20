

import asyncio
from functools import partial
import math
import base64

from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner

from settings import settings


class Component(ApplicationSession):
    """
    An application component using the time service.
    """

    @asyncio.coroutine
    def onJoin(self, details):

        index = "events"
        query = "foo AND bar"

        sid = yield from self.call("com.estrom.register_query", index, query)
        print("got sid {}".format(sid))
        rindex = sid.decode().split("_")[0]
        rindex = base64.b32decode(self.pad(rindex).encode()).decode()
        print(rindex)
        assert rindex == index
        self.leave()

    def onDisconnect(self):
        asyncio.get_event_loop().stop()

    def pad(self, v, length=8):  # TODO: Understand why it's 8
        return v.ljust(math.ceil(float(len(v))/length)*length, "=")

if __name__ == '__main__':
    cbs = settings.crossbar
    runner = ApplicationRunner(
        u"ws://{}:{}/ws".format(cbs.host, cbs.port),
        cbs.realm,
        debug=True,  # optional; log even more details
    )
    runner.run(Component)
