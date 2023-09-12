from chatcryptor.config import  MainConfig, logging
import requests
logger = logging.getLogger(__name__)


def _call_api(path, params={}):
    url = MainConfig.SOLSCAN_API.value
    url = f'{url}/{path}'
    logger.debug(f'Start call api of solscan: {url} and params: {params}')
    response = requests.get(url, params=params, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    })
    if (response.status_code < 300):
        return response.json()
    logger.error(f'Call api {url} error: {response.text}')
    return None

def _call_pro_api(path, params={}):
    url = MainConfig.SOLSCAN_PRO_API.value
    url = f'{url}/{path}'
    logger.debug(f'Start call api pro of solscan: {url} and params: {params}')
    response = requests.get(url, params=params, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    })
    if (response.status_code < 300):
        return response.json()
    logger.error(f'Call api {url} error: {response.text}')
    return None
