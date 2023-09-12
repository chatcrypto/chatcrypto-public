
from enum import Enum


class SUPPORT_PLATFORM(Enum):
    SOLANA = 'solana'
    APTOS = 'aptos'

    @staticmethod
    def values():
        return [k.value for k in SUPPORT_PLATFORM]
