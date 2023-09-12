
from chatcryptor.app.utils.response import json_response_error, json_response_success
from chatcryptor.app.app import api_router, app
from fastapi import Request
from chatcryptor.models.db_models import FavouriteQuestion


@api_router('/question/favourite')
async def get_favourite_questions(request: Request):
    rs = FavouriteQuestion.get_all_messages()
    rs = [k.dict() for k in rs]
    return json_response_success(rs)

