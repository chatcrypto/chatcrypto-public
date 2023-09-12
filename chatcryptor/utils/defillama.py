from chatcryptor.config import MainConfig, logging
import requests
from chatcryptor.db.redis import RedisClient
from chatcryptor.utils.array import get_last_n_elements
logger = logging.getLogger(__name__)


def get_defillama_tvl(defillama_id):
    try:
        url = f"https://api.llama.fi/updatedProtocol/{defillama_id}"
        key = f"cache_defillama_{url}"
        redis = RedisClient()
        cache = redis.get(key)
        if cache:
            return cache
        logger.debug(f'Start call api of defillma: {url}')
        response = requests.get(url,  headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        })
        if (response.status_code < 300):
            resp_json = response.json()
            current_chain_tvls = resp_json.get('currentChainTvls')
            market_cap = resp_json.get('mcap')
            chain_tvls = resp_json.get('chainTvls')
            for chain in chain_tvls:
                tvls = chain_tvls[chain]['tvl']
                chain_tvls[chain]['tvl'] = get_last_n_elements(tvls, 200)
            data = {
                "market_cap": market_cap,
                "current_chain_tvls": current_chain_tvls,
                "chain_tvls": chain_tvls,
            }
            redis.set(key, data, 1*60*60)
            return data
        logger.error(f'Call api {url} error: {response.text}')
    except BaseException as e:
        logger.debug(e)
    return None

def get_defillama_vol(defillama_id):
    try:
        url = f"https://api.llama.fi/summary/dexs/{defillama_id}"
        key = f"cache_defillama_{url}"
        redis = RedisClient()
        cache = redis.get(key)
        if cache:
            return cache
        logger.debug(f'Start call api of defillma: {url}')
        response = requests.get(url,  headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        })
        if (response.status_code < 300):
            resp_json = response.json()
            total_data_breakdowns = get_last_n_elements(resp_json.get('totalDataChartBreakdown'), 200)

            vol_by_chains = []
            chains = set()
            for breakdown_data in total_data_breakdowns:
                chain_vols = breakdown_data[1]
                new_chain_vols = {}
                for k1 in chain_vols:
                    chains.add(k1)
                    chain_dapp_vols = chain_vols[k1]
                    chain_vol = 0.0
                    for k2 in chain_dapp_vols:
                        chain_vol += chain_dapp_vols[k2]

                    new_chain_vols[k1] = chain_vol
                vol_by_chains.append([
                    breakdown_data[0],
                    new_chain_vols
                ])
            data = {
                "total_vol_24h": resp_json.get('total24h'),
                "chains": list(chains),
                "vol_by_chains": vol_by_chains
            }
            redis.set(key, data, 1*60*60)
            return data
        logger.error(f'Call api {url} error: {response.text}')
    except BaseException as e:
        logger.debug(e)
    return None
