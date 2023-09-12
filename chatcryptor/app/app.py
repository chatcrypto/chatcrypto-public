from chatcryptor.config import MainConfig, logging
from collections import defaultdict
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
logger = logging.getLogger(__name__)
logger.info(f'Create app FastAPI')
app = FastAPI()


def api_router(url):
    """
    Create a decorator for router APIs. API url will be add more API_VERSION to url.
    """
    logger.debug(f"Add router [{url}] for API version: {MainConfig.API_VERSION.value}")
    return app.get(f'/{MainConfig.API_VERSION.value}{url}')
