"""
Some validation functions for validate data
"""

from chatcryptor.bot.utils.validator import validate_address_blockchain, validate_arguments
from pydantic import BaseModel, ValidationError
from chatcryptor.bot.utils.exceptions import ExceptionNeedShowMessage
from chatcryptor.utils.aptos.aptscan_ai_api import _call_api


def get_type_of_address(address: str) -> str:
    """
    Detect an address is token, token account or account
    If this address not found, return None
    """
    if address in ['0x1', '0x3', '0x4']:
        return 'account'
    if address.find('::') > 0 and address.startswith('0x1'):
        return 'coin'
    if address.find('::') > 0 and address.startswith('0x3'):
        return 'token'
    return 'account' if len(address) >= 32 else None
