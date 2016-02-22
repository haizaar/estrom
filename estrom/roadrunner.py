
from autobahn.asyncio.wamp import ApplicationRunner

from .settings import settings as s


def run_componenet(Component):
    scb = s.crossbar
    crossbar_url = "ws://{}:{}/ws".format(scb.host, scb.port)
    runner = ApplicationRunner(crossbar_url, scb.realm, debug=scb.debug)
    runner.run(Component)
