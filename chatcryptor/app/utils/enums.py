
from enum import Enum


class BOT_STATUS(Enum):
    RECEIVED_MESSAGE = 'receive'
    THINKING = 'thinking'
    STREAMING = 'stream'
    END = 'end'
    ERROR = 'error'
    BUSY = 'busy'


class SENDER_TYPE(Enum):
    BOT = 'bot'
    CLIENT = 'client'
