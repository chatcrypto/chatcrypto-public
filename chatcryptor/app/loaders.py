import logging
from chatcryptor.app.utils.response import json_response_error, json_response_success
from chatcryptor.app.app import app
from fastapi import Request

logger = logging.getLogger(__name__)


@app.get('/')
async def default(request: Request):
    return json_response_success(data='Welcome to ChatCryptor APIs!')


def loaders():
    import chatcryptor.app.routers.ws
    import chatcryptor.app.routers.auth
    import chatcryptor.app.routers.api
    import chatcryptor.app.middlewares

    # load router for process domain analysis
    import chatcryptor.app.modules.domain.router
