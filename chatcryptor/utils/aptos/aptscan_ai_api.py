from chatcryptor.config import MainConfig, logging
import requests
from chatcryptor.db.redis import RedisClient
logger = logging.getLogger(__name__)


def _call_api(path, params={}):
    url = 'https://api.aptscan.ai/v1'
    url = f'{url}/{path}'
    key = f"cache_aptscan_ai_{url}_{params}"
    redis = RedisClient()
    cache = redis.get(key)
    if cache is not None:
        return cache
    logger.debug(f'Start call api of aptscan.ai: {url} and params: {params}')
    response = requests.get(url, params=params, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    })

    if (response.status_code < 300):
        data = response.json()
        if data.get('success') is True:
            redis.set(key, data, 5*60)
            return data
    logger.error(f'Call api {url} error: {response.text}')
    return None
