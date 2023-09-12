
import json
from promisio import promisify
import time
from chatcryptor.config import MainConfig, logging
from aiohttp.http_websocket import WSCloseCode, WSMessage
from chatcryptor.app.utils.response import json_response_error, ChatResponse
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, Query
from chatcryptor.app.utils.enums import BOT_STATUS, SENDER_TYPE
from chatcryptor.app.app import app
import traceback
import tracemalloc
from chatcryptor.bot.router.base import RouterPipeLine
tracemalloc.start()
logger = logging.getLogger(__name__)


@promisify
async def run_agent(websocket, wallet, question, agent):
    try:
        result = agent.run(input=question)
        rs = [k.dict() for k in result]
        # Response to client the answer
        await websocket.send_json(ChatResponse(
            wallet=wallet,
            sender=SENDER_TYPE.BOT.value, message=rs, type=BOT_STATUS.END.value).dict())
    except BaseException as e:
        logger.error(
            f'[{wallet}] There are some error when process question. Error: {e}')
        logger.debug(traceback.print_exc())
        await websocket.send_json(ChatResponse(
            wallet=wallet,
            sender=SENDER_TYPE.BOT.value, message='Unknonw Error', type=BOT_STATUS.ERROR.value).dict())


@app.websocket("/chat/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str, network: str=None):
    # TODO: Need to implement authentication with token and wallet here...
    if (user_id == '' or not user_id):
        return json_response_error(error='wallet must be set')
    await websocket.accept()
    logging.info(f"[{user_id}] websocket connected!")   
    
    agent = RouterPipeLine().setup(
        enable_memory=True, session_id=user_id, default_blockchain_network=network if network else '')
    # main_agent(session_id=wallet, enable_history=True,
    #                    verbose=True if MainConfig.LOG_LEVEL.value == 10 else False)
    while True:
        try:
            # Receive and send back the client message
            question = await websocket.receive_text()
            logger.debug(f'[{user_id}] Question is: {question}')
            await websocket.send_json(ChatResponse(wallet=user_id, sender=SENDER_TYPE.BOT.value,
                                                   message=question, type=BOT_STATUS.RECEIVED_MESSAGE.value).dict())
            run_agent(websocket=websocket,
                      wallet=user_id,
                      question=question,
                      agent=agent
                      )

        except WebSocketDisconnect:
            logging.info(f"[{user_id}] websocket disconnect!")
            break
        except Exception as e:
            logging.error(f"[{user_id}] {e}")
            logger.debug(traceback.print_exc())
            await websocket.send_json(ChatResponse(
                wallet=user_id,
                sender=SENDER_TYPE.BOT.value,
                message="Sorry, something went wrong. Try again.",
                type=BOT_STATUS.ERROR.value,
            ).dict())
