
from enum import Enum


class AI_METHOD(Enum):
    AGENT = 'agent'
    CHAIN = 'chain'
    TOOL = 'tool'


class REPONSE_CHART_TYPE(Enum):
    TABLE = 'table'
    PIE = 'pie'
    BAR = 'bar'
    GROUPED_BAR = 'grouped_bar'
    LINE = 'line'
    LIST = 'list'
    TEXT = 'text'
    JS_CODE = 'js_code'
    SOURCE_CODE = 'source_code'


class MODEL_TYPE(Enum):
    ONCHAIN = 'onchain'
    STATISTIC = 'statistic'
    TRAINING = 'training'
