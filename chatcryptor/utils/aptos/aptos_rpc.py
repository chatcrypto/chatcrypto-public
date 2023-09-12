from chatcryptor.config import MainConfig, logging
import requests
logger = logging.getLogger(__name__)


def _call_rpc(method: str, params: any = None):
    # Make a request to Solana Node RPC
    pass