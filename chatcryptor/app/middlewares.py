import time
import traceback
from chatcryptor.bot.utils.exceptions import ExceptionRequestAPIError
from chatcryptor.config import MainConfig, logging
from chatcryptor.app.app import app
from fastapi import Request
from chatcryptor.app.utils.response import json_response_error
from chatcryptor.config import MainConfig
logger = logging.getLogger(__name__)


@app.middleware("http")
async def add_middleware_here(request: Request, call_next):
    try:
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        if MainConfig.LOG_LEVEL.value < 20:
            response.headers["X-Process-Time"] = str(process_time)
        if (response.status_code == 404):
            return json_response_error(error="URL Not Found", status_code=404)
        return response
    except ExceptionRequestAPIError as er:
        return json_response_error(error=er.message, status_code=400)
    except BaseException as er:
        logger.error(f"Error when process endpoint: {request.url}.Error: {er}")
        logger.debug(traceback.format_exc())
        return json_response_error(error="Internal server error", status_code=500)
