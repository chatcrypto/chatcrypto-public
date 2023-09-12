
from chatcryptor.config import MainConfig, logging
from sqlalchemy import create_engine, Column, MetaData

from clickhouse_sqlalchemy import (
    Table, make_session, get_declarative_base, types, engines
)
logger = logging.getLogger(__name__)


class ClickhouseClient():
    instance = {}
    _config = {}
    _client = None

    @property
    def client(self):
        return self._client

    @property
    def config(self):
        return self._config

    def connect(self):
        uri = self._config.get('uri')
        if not uri:
            raise ValueError(
                f'Uri is empty')

        if (ClickhouseClient.instance.get(uri)):
            self._client = ClickhouseClient.instance[uri]
        else:
            logger.info(f'Create connection to clickhouse with uri: {uri}')
            engine = create_engine(uri)
            session = make_session(engine)
            self._client = session
            ClickhouseClient.instance[uri] = self._client
        return self

    def __init__(self, conn_id: str = 'main') -> None:
        self._config = MainConfig.CLICKHOUSE_URI.value.get(conn_id)
        if not self._config:
            raise ValueError(
                f'You need config clickhouse with connection_id: {conn_id}')

    def query(self, query: str, **kwargs):
        data = self.client.execute(query, **kwargs)
        for proxy in data:
             yield dict(proxy)
        