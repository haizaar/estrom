
import asyncio
import aioes

from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner


class Component(ApplicationSession):

    @asyncio.corouting
    def onJoin(self, details):
        kk