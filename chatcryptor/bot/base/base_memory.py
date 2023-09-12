import json
import logging
from typing import List, Optional, Dict, Tuple, Any
from langchain.schema import (
    BaseChatMessageHistory,
    BaseMessage,
    _message_to_dict,
    messages_from_dict,
)
from langchain.memory.chat_message_histories import RedisChatMessageHistory
from langchain.memory import ConversationBufferMemory
from langchain.memory.utils import get_prompt_input_key

logger = logging.getLogger(__name__)


class CustomRedisChatMessageHistory(RedisChatMessageHistory):
    """Chat message history stored in a Redis database."""

    def add_ai_message(self, message: str) -> None:
        """
        HACK: Disable ai message for memory
        """
        return True


class CustomConversationBufferMemory(ConversationBufferMemory):
    def _get_input_output(self, inputs: Dict[str, Any], outputs: Dict[str, str]) -> Tuple[str, str]:
        # HACK: because key `groups`` is used for filter which tools that are allowed to execute,
        # but its conflict with `inputs` of memory, so will be removed from inputs.
        if 'groups' in inputs:
            del inputs['groups']
        return super()._get_input_output(inputs, outputs)
