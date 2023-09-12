from chatcryptor.bot.base.base_memory import CustomRedisChatMessageHistory, RedisChatMessageHistory
from chatcryptor.config import  MainConfig, logging
from langchain.memory import ConversationBufferMemory, ConversationBufferWindowMemory, ReadOnlySharedMemory
from chatcryptor.bot.base.base_memory import CustomConversationBufferMemory

logger = logging.getLogger(__name__)


def create_memory_instance(session_id: str = '', store_ai_answer=False, ttl=60, **kwargs):
    """
    Create base memory instance that used for all agents, chains.
    """
    if session_id.strip() == '':
        raise ValueError(f'session_id must be set')
    logger.debug(
        f"Start create memory instance with Redis and session_id: {session_id}")
    if store_ai_answer is False:
        message_history = CustomRedisChatMessageHistory(
            url=str(MainConfig.REDIS_URL.value), ttl=ttl, session_id=session_id
        )
    else:
        message_history = RedisChatMessageHistory(
            url=str(MainConfig.REDIS_URL.value), ttl=ttl, session_id=session_id
        )
    memory = CustomConversationBufferMemory(
        memory_key="chat_history",
        chat_memory=message_history,
        return_messages=True)
    return memory


def create_readonly_memory(memory=None):
    if memory:
        return ReadOnlySharedMemory(memory=memory)
    return None
