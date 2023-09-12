from chatcryptor.config import MainConfig, logging
from collections import defaultdict
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from chatcryptor.app.app import app
from chatcryptor.app.loaders import loaders
logger = logging.getLogger(__name__)


# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def create_server():
    import uvicorn
    logger.info(f'Load routers from config')
    loaders()
    uvicorn.run(app, host=MainConfig.HTTP_HOST.value,
                port=MainConfig.HTTP_PORT.value)
