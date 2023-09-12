
from enum import Enum


class MAIN_ENTITY_TYPE(Enum):
    """
    Define Enums for Entity types. Thats used for defining objects on blockchain like token, account, ....
    """
    TOKEN = 'token'
    COIN = 'coin'
    ACCOUNT = 'account'
    NFT_COLLECTION = 'nft_collection'
    NFT_ITEM = 'nft_item'
    ADDRESS = 'address'
    FUNGIBLE_TOKEN = 'fungible_token'
    PLATFORM = 'platform'
    TRANSACTION = 'transaction'
    TRANSFER = 'transfer'
    STAKE = 'stake'
    DOMAIN = 'domain'
    MODULE = 'module'
    SOURCE_CODE = 'source_code'
    ABI = 'abi'

    @staticmethod
    def values():
        return [k.value for k in MAIN_ENTITY_TYPE]


class ENTITY_PROPERTIES(Enum):
    HOLDER = 'holder'
    PRICE = 'price'
    INFORMATION = 'information'
    SEARCH = 'search'
    BALANCE = 'balance'
    AMOUNT = 'amount'

    @staticmethod
    def values():
        return [k.value for k in ENTITY_PROPERTIES]


class EXTRACTION_ACTION_TYPE(Enum):
    ACTION_GET = 'get'
    ACTION_FIND = 'find'
    ACTION_DEFINITION = 'definition'

    @staticmethod
    def values():
        return [k.value for k in EXTRACTION_ACTION_TYPE]
