from pydantic import BaseModel
from typing import List, Any, Optional
from langchain.memory import ConversationBufferMemory, ReadOnlySharedMemory
from langchain.tools import Tool
from chatcryptor.config import  MainConfig


class BaseExecutor():
    tools: Optional[List[Tool]] = []
    executor: Any = None
    memory: Optional[ConversationBufferMemory] = None
    groups: Optional[List[str]] = []
    session_id: Optional[str]
    __cache_groups: Optional[List[str]] = []

    @ property
    def extract_group_from_tools(self) -> List[str]:
        if self.tools:
            g = []
            for k in self.tools:
                if hasattr(k, 'groups') and getattr(k, 'groups'):
                    g += getattr(k, 'groups')
            return list(set(g))
        return []

    @ property
    def all_groups(self) -> List[str]:
        if not self.__cache_groups:
            self.__cache_groups = list(
                set(self.groups + self.extract_group_from_tools))
        return self.__cache_groups

    def setup(self, memory=None, **kwargs):
        raise NotImplementedError(
            "Need to implement this method to init executor")

    def run(self, *args, **kwargs):
        if self.executor is None:
            raise NotImplementedError("executor need to be initialized")
        return self.executor.run(*args, **kwargs)


class DefaultExcecutor(BaseExecutor):
    """
    Default excecutor that will be used for answer question of user
    """

    def setup(self, memory=None, verbose=False, **kwargs):
        from langchain import PromptTemplate, LLMChain
        from chatcryptor.bot.prompts.main import DEFAULT_PROMPT_EXECUTOR
        from langchain.chains import ConversationChain
        from langchain.chat_models import ChatOpenAI
        llm = ChatOpenAI(temperature=kwargs.get("temperature", 0), model=kwargs.get("model", MainConfig.MODEL_GPT.value),
                         verbose=kwargs.get("verbose", False))

        if not memory:
            prombt = PromptTemplate(
                template=DEFAULT_PROMPT_EXECUTOR.replace('{chat_history}', ''), input_variables=['input'])
            self.executor = LLMChain(
                prompt=prombt, llm=llm, **kwargs.get('chain_kwargs', {}))
        else:
            prombt = PromptTemplate(
                template=DEFAULT_PROMPT_EXECUTOR, input_variables=["input", "chat_history"])
            self.executor = ConversationChain(
                prompt=prombt,
                llm=llm,
                memory=memory,
                **kwargs.get('chain_kwargs', {}),
                verbose=verbose)
        return self
