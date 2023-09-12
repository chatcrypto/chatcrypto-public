
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
# TODO: define list of functions to work with aptos blockchain