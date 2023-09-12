from chatcryptor.config import  MainConfig, logging
import requests
logger = logging.getLogger(__name__)


def _call_rpc(method: str, params: any = None):
    # Make a request to Solana Node RPC
    url = MainConfig.SOLANA_MAINNET.value
    logger.debug(f"Start call rpc endpoint: {url} with method: [{method}]")

    try:

        js = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method
        }
        if (params is not None):
            js['params'] = params
        logger.debug(js)
        # Send the RPC request and get the response
        response = requests.post(url, headers={
            "Content-Type": "application/json"
        }, json=js)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse and return the JSON response
            data = response.json()
            if (data.get('error')):
                error = data['error']
                logger.error(f'Error when call api: {method}. Error: {error}')
                return None
            return data['result']
        else:
            # Handle the error response
            logger.error("RPC request failed with status code:",
                         response.status_code)
            return None

    except requests.exceptions.RequestException as e:
        # Handle any network or connection errors
        logger.error("An error occurred:", e)
        return None


def _rpc_sdk():
    # create client from sdk
    from solana.rpc.api import Client
    url = MainConfig.SOLANA_MAINNET.value
    logger.debug(f"Start call rpc endpoint: ${url}")
    return Client(url)

