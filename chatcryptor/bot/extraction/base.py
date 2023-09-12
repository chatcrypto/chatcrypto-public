from langchain.chat_models import ChatOpenAI
from langchain.chains import create_tagging_chain_pydantic
from langchain.prompts import (
    ChatPromptTemplate,
)
from chatcryptor.bot.extraction.prompt import EXTRACTION_ENTITY
from chatcryptor.bot.extraction.schema import EntityExtraction
from chatcryptor.bot.base.base_executor import BaseExecutor

import chatcryptor.config as MainConfig

logger = MainConfig.logging.getLogger(__name__)


class EntityExecutor(BaseExecutor):

    executor: EntityExtraction

    def setup(self, **kwargs) -> None:
        logger.debug(f'Create EntityParser instance and save to singleton')
        _llm = ChatOpenAI(temperature=kwargs.get('temperature', 0), model=kwargs.get(
            'model', MainConfig.MainConfig.MODEL_GPT.value))
        self.executor = create_tagging_chain_pydantic(
            pydantic_schema=EntityExtraction, llm=_llm,
            prompt=ChatPromptTemplate.from_template(EXTRACTION_ENTITY)
        )
        return self
