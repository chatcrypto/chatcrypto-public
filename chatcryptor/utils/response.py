
from pydantic import BaseModel, validator, Field
from chatcryptor.enums.response import AI_METHOD, MODEL_TYPE, REPONSE_CHART_TYPE
from typing import (
    Any,
    Dict,
    List,
    Optional

)


class ChatResponse(BaseModel):
    """
    Define response to user.
    Data will be includes some fields:
        method: agent, chain, or tool
        model_type: onchain, statistic or training...
    """
    method: str
    title: str
    description: Optional[str] = ""
    model_type: str
    chart_type: Optional[str] = REPONSE_CHART_TYPE.TEXT.value
    data: Optional[Any]
    tool: Optional[str]
    referencer: Optional[str]
    is_raw: Optional[bool] = False
    error: Optional[bool] = False
    error_message: Optional[str] = ""

    @validator("method")
    def method_need_valid(cls, v):
        if v not in [e.value for e in AI_METHOD]:
            raise ValueError("method is invalid")
        return v

    @validator("model_type")
    def model_typeneed_valid(cls, v):
        if v not in [e.value for e in MODEL_TYPE]:
            raise ValueError("model_type is invalid")
        return v

    @validator("chart_type")
    def chart_type_need_valid(cls, v):
        if v not in [e.value for e in REPONSE_CHART_TYPE]:
            raise ValueError("chart_type is invalid")
        return v


class TableResponse(BaseModel):
    '''
    Help define data with table format
    '''
    table_header: List[str]
    row_data: List[List[Any]]

    @staticmethod
    def render(header: Dict, data: List[Dict]):
        """
        Convert a list of dict to Table Response
        Eg: header: {"name": "Name"}
        data: [{"name": "phong"}]
        """
        list_keys = header.keys()
        return TableResponse(
            table_header=[header.get(k, "") for k in list_keys],
            row_data=[[k.get(i, "") for i in list_keys] for k in data]
        )


class BarOrLineChartReponse(BaseModel):
    '''
    Help define data with Bar Chart format
    '''
    row_data: List[Dict]
    x_field: str
    y_field: str
    x_label: Optional[str] = ""
    y_label: Optional[str] = ""
    label: str

    @staticmethod
    def render(x_field: str, y_field: str, data: List[Dict], label: str):
        return BarOrLineChartReponse(x_field=x_field, y_field=y_field, row_data=data, label=label)


class PieChartReponse(BaseModel):
    '''
    Help define data with Pie Chart format
    '''
    row_data: List[Any]
    label: List[str]

    @staticmethod
    def render(data: List[Any], label: List[str]):
        return PieChartReponse(row_data=data, label=label)


class EvalJsCodeResponse(BaseModel):
    code: str


class SourceCodeResponse(BaseModel):
    code: str
    language: str


class DataResponse(BaseModel):
    title: str
    description: Optional[str] = ""
    chart_type: Optional[str] = REPONSE_CHART_TYPE.TEXT.value
    data: Optional[Any] = ''
    tags: Optional[List[str]] = []
    success: bool = True
    debug_plugin_name: Optional[str] = None
    debug_plugin_metadata: Optional[dict] = {}
    plugin_id: Optional[str] = None

    @validator("chart_type")
    def chart_type_need_valid(cls, v):
        if v not in [e.value for e in REPONSE_CHART_TYPE]:
            raise ValueError("chart_type is invalid")
        return v

    def to_dict():
        pass


class APIResponse(BaseModel):
    message: str = ""
    data: Any = ""
    status: bool = False
    error: str = ""
