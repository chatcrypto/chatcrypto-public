
from chatcryptor.config import MainConfig, logging
from chatcryptor.bot.utils.decorators import generate_tool_from_func
from chatcryptor.utils.solana.solscan_api import _call_api, _call_pro_api
from chatcryptor.utils.solana.solana_rpc import _call_rpc
import chatcryptor.utils.exceptions as Exceptions
import chatcryptor.utils.validator as validators
from chatcryptor.bot.tools.solana.utils import get_type_of_address
from chatcryptor.bot.tools.solana.schemas import *
import datetime
import chatcryptor.utils.response as Response
import chatcryptor.utils.format as FormatNumber
from decimal import Decimal
import json
logger = logging.getLogger(__name__)


def response_data_format(data, reference='', **kwargs):
    try:
        data = data.dict()
        data['referencer'] = f"{MainConfig.SOLSCAN_DOMAIN.value}/{reference}"
        return json.dumps(data)
    except BaseException as e:
        logger.debug(e)
        data['referencer'] = f"{MainConfig.SOLSCAN_DOMAIN.value}/{reference}"
        return data

