from chatcryptor.config import MainConfig, logging
import redis
import json

logger = logging.getLogger(__name__)


class RedisClient:
    _instance = {}
    _config = {}
    _client = None
    PREFIX_KEY = 'chatcryptor_'

    @property
    def client(self):
        if self._client is None:
            self.connect()
        return self._client

    def connect(self):
        uri = self._config
        if not uri:
            raise ValueError(
                f'Uri is empty')
        if (RedisClient._instance.get(uri)):
            self._client = RedisClient._instance[uri]
        else:
            self._client = redis.from_url(uri)
            RedisClient._instance[uri] = self._client
            logger.info(f'Create connection to redis with uri: {uri}')

        return self._client

    def __init__(self, uri: str = MainConfig.REDIS_URL.value) -> None:
        self._config = uri
        if not self._config:
            raise ValueError(
                f'You need config Redis')

    def get(self, key, default=None):
        key = f"{RedisClient.PREFIX_KEY}{key}"
        data = self.client.get(key)
        try:
            return json.loads(data)
        except BaseException as e:
            pass
        return data if data is not None else default

    def set(self, key, value, ttl=0):
        key = f"{RedisClient.PREFIX_KEY}{key}"
        if type(value) in [dict, list]:
            value = json.dumps(value)
        self.client.set(key, value=value)
        if ttl > 0:
            self.client.expire(key, ttl)
