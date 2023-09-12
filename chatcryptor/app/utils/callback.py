"""Callback handlers used in the app."""
from typing import Any, Dict, List

from langchain.callbacks.base import BaseCallbackHandler, AsyncCallbackHandler
from app.utils.enums import BOT_STATUS, SENDER_TYPE
from app.utils.response import ChatResponse


class StreamingLLMCallbackHandler(AsyncCallbackHandler):
    """Callback handler for streaming LLM responses."""

    def __init__(self, websocket, wallet: str):
        self.websocket = websocket
        self.wallet = wallet

    async def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        resp = ChatResponse(wallet=self.wallet, sender=SENDER_TYPE.BOT.value,
                            message=token, type=BOT_STATUS.STREAMING.value,
                            handler='on_llm_new_token'
                            )
        await self.websocket.send_json(resp.dict())


class QuestionGenCallbackHandler(AsyncCallbackHandler):
    """Callback handler for question generation."""

    def __init__(self, websocket, wallet: str):
        self.websocket = websocket
        self.wallet = wallet

    async def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        """Run when LLM starts running."""
        resp = ChatResponse(
            wallet=self.wallet,
            handler='on_llm_start',
            sender=SENDER_TYPE.BOT.value, message="Synthesizing question...", type=BOT_STATUS.THINKING.value
        )
        await self.websocket.send_json(resp.dict())
