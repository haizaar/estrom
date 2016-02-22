
import asyncio
import json
import aioes
from hashlib import md5

from .utils import Hasher
from .logging import LoggerMixIn
from .settings import settings as s


class ESClient(LoggerMixIn):

    @asyncio.coroutine
    def connect(self):
        ses = s.es
        esurl = "{}:{}".format(ses.host, ses.port)
        self.es = aioes.Elasticsearch([esurl])
        yield from self.es.transport.perform_request("HEAD", "/")
        self.logger.info("Connected to ElasticSearch")

    @asyncio.coroutine
    def register_percolator(self, index, query):
        qid = md5(json.dumps(query).encode()).hexdigest()
        yield from self.es.index(index, s.es.percolator_type, query, id=qid)

        sid = Hasher.index_qid_to_sid(index, qid)
        return sid
