from chatcryptor.config import MainConfig, logging
import requests
from chatcryptor.db.redis import RedisClient
logger = logging.getLogger(__name__)


def get_token_price(token_id):
    try:
        redis = RedisClient()
        url = f"https://www.coingecko.com/price_charts/{token_id}/usd/7_days.json"
        key = f"cache_coingecko_{url}"
        cache = redis.get(key)
        if cache:
            return cache
        logger.debug(f'Start call api of coingecko: {url}')
        response = requests.get(url,  headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        })
        if (response.status_code < 300):
            data = response.json().get('stats')
            redis.set(key, data, 1*60*60)
            return data
        logger.error(f'Call api {url} error: {response.text}')
    except BaseException as e:
        logger.debug(e)
    return None
