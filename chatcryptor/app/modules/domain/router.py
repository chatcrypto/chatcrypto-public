
from chatcryptor.app.utils.response import json_response_error, json_response_success, json_response_as_stream
from chatcryptor.app.app import api_router
from fastapi import Request
from chatcryptor.config import MainConfig, logging
from chatcryptor.models.db_models import FavouriteQuestion
from typing import Optional
from fastapi import Query
from chatcryptor.app.modules.domain.service import process_by_plugins, get_plugins_of_domain
import traceback


@api_router('/domain/plugins')
async def api_plugins_of_domain(request: Request, domain: str = Query(..., max_length=100, min_length=2)):
    try:
        data = await get_plugins_of_domain(domain)
        return json_response_success(data)
    except BaseException as e:
        logging.debug(traceback.print_exc())
        return json_response_error(error="Sorry we can not get data because of some unknown errors.", status_code=500)


@api_router('/domain/plugin/detail')
async def api_plugin_defail_of_domain(request: Request, domain: str = Query(..., max_length=100, min_length=2), plugin_id: str = Query(..., max_length=100, min_length=2)):
    try:
        data = await process_by_plugins(domain, plugin_id=plugin_id, response_json=True)
        async for item in data:
            return json_response_success(item)
        return json_response_error(error=f"plugin_id [{plugin_id}] does not exist", status_code=422)
    except BaseException as e:
        logging.debug(traceback.print_exc())
        return json_response_error(error="Sorry we can not get data because of some unknown errors.", status_code=500)
