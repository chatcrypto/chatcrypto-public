from fastapi.responses import JSONResponse
from pydantic import BaseModel, validator
from chatcryptor.app.utils.enums import BOT_STATUS, SENDER_TYPE
from typing import Optional, Any
from starlette.responses import StreamingResponse
from sse_starlette.sse import EventSourceResponse
from chatcryptor.config import MainConfig
import json
import asyncio


class ChatResponse(BaseModel):
    """Chat response schema."""
    wallet: str
    sender: str
    message: Any
    type: str
    handler: Optional[str]

    @validator("sender")
    def sender_must_be_bot_or_you(cls, v):
        if v not in [e.value for e in SENDER_TYPE]:
            raise ValueError("sender must be bot or you")
        return v

    @validator("wallet")
    def wallet_must_be_set(cls, v):
        if v == '':
            raise ValueError("wallet must be set")
        return v

    @validator("type")
    def validate_message_type(cls, v):
        if v not in [e.value for e in BOT_STATUS]:
            raise ValueError("type must be start, stream or end")
        return v


def json_response_success(data):
    return JSONResponse(content={
        "message": "success",
        "data": data,
    }, status_code=200)


def json_response_error(error, status_code=403):
    return JSONResponse(content={
        "message": "fail",
        "error": error,
    }, status_code=status_code)


def json_response_404(error='API not found'):
    return JSONResponse(content={
        "message": "fail",
        "error": error,
    }, status_code=404)


def json_response_as_stream(generator_func):
    async def convert_rs():
        async for item in generator_func:
            rs = '{}'
            try:
                rs = json.dumps({
                    "message": "success",
                    "data": item
                })
            except BaseException as e:
                rs = json.dumps({
                    "message": "error",
                    "data": "Error when output data",
                    "debug": f"Cannot encode data as JSON. Error: {str(e)}" if MainConfig.LOG_LEVEL.value < 20 else ""
                })
            yield rs
    return EventSourceResponse(convert_rs(), media_type="text/event-stream")
