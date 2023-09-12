import pymongo
from chatcryptor.config import  MainConfig, logging
import copy
logger = logging.getLogger(__name__)


class MongodbClient():
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
        if (MongodbClient.instance.get(uri)):
            self._client = MongodbClient.instance[uri]
        else:
            logger.info(f'Create connection to mongodb with uri: {uri}')
            kw = self.config.get('options', {})
            self._client = pymongo.MongoClient(uri, **kw)
            MongodbClient.instance[uri] = self._client
        return self._client

    def __init__(self, conn_id: str = 'main') -> None:
        self._config = MainConfig.MONGODB_URI.value.get(conn_id)
        if not self._config:
            raise ValueError(
                f'You need config Mongodb with connection_id: {conn_id}')

    def get_collection(self, collection: str, db: str = None):
        if not db:
            db = self.config.get('db')
        logger.info(f'Connect to Collection: {db}.{collection}')
        return self.get_db(db)[collection]

    def get_db(self, db: str = ''):
        if not db:
            db = self.config['db']
        return self.connect()[db]
