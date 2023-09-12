
from chatcryptor.config import  MainConfig, logging
from chatcryptor.bot.utils.decorators import generate_tool_from_func
from chatcryptor.utils.solana.solscan_api import _call_api, _call_pro_api
from chatcryptor.utils.solana.solana_rpc import _call_rpc
import chatcryptor.bot.utils.exceptions as Exceptions
import chatcryptor.bot.utils.validator as validators
from chatcryptor.bot.tools.solana.utils import get_type_of_address, find_token_address
from chatcryptor.bot.tools.solana.schemas import *
import datetime
import chatcryptor.utils.response as Response
import chatcryptor.utils.format as FormatData
from chatcryptor.bot.utils.exceptions import ExceptionNeedShowMessage
from chatcryptor.models.db_models import TokenInfo
import chatcryptor.bot.tools.solana.schemas as AptosInputSchemas
import json
from chatcryptor.enums.platform import SUPPORT_PLATFORM
from chatcryptor.enums.entity import MAIN_ENTITY_TYPE, ENTITY_PROPERTIES
logger = logging.getLogger(__name__)

SUFFIX_TOOL_NAME = "OnSolana"
MAIN_GROUPS = [SUPPORT_PLATFORM.SOLANA.value]


from chatcryptor.config import MainConfig, logging
from chatcryptor.bot.utils.decorators import generate_tool_from_func
from chatcryptor.utils.aptos.aptscan_ai_api import _call_api
import chatcryptor.bot.utils.exceptions as Exceptions
import chatcryptor.bot.utils.validator as validators
import datetime
import chatcryptor.utils.response as Response
import chatcryptor.utils.format as FormatData
from chatcryptor.bot.utils.exceptions import ExceptionNeedShowMessage
from chatcryptor.models.db_models import TokenInfo
import chatcryptor.bot.tools.aptos.schemas as AptosInputSchemas
import json
from chatcryptor.enums.platform import SUPPORT_PLATFORM
from chatcryptor.enums.entity import MAIN_ENTITY_TYPE, ENTITY_PROPERTIES
from chatcryptor.bot.tools.aptos.utils import get_type_of_address
import chatcryptor.utils.format as FormatResult

logger = logging.getLogger(__name__)

SUFFIX_TOOL_NAME = "OnAptos"
MAIN_GROUPS = [SUPPORT_PLATFORM.APTOS.value]
# TODO: define list of functions to work with solana blockchain