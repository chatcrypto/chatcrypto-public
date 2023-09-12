
from chatcryptor.bot.prompts.main import *
from chatcryptor.config import  MainConfig
from langchain.chat_models import ChatOpenAI
from chatcryptor.bot.prompts.main import *
from langchain.schema import SystemMessage
from langchain.prompts import MessagesPlaceholder
from langchain.agents.openai_functions_agent.base import OpenAIFunctionsAgent
from chatcryptor.bot.base.base_agent import CustomOpenAIFunctionsAgent, CustomAgentExecutor
from chatcryptor.bot.agents.solana_toolkits.toolkit import SolanaToolKit
from chatcryptor.bot.base.base_executor import BaseExecutor
from chatcryptor.enums.platform import SUPPORT_PLATFORM


class SolanaExecutor(BaseExecutor):

    groups = [SUPPORT_PLATFORM.SOLANA.value]

    def setup(self, memory=None, **kwargs):
        system_message = SystemMessage(
            content=kwargs.get("prompt", MAIN_PROMPT)
            )
        extra_prombt = []
        if memory:
            self.memory = memory
            extra_prombt = [system_message, MessagesPlaceholder(
                variable_name='chat_history')]
        tools = SolanaToolKit().get_tools()
        self.tools = tools
        prombt = OpenAIFunctionsAgent.create_prompt(
            system_message=system_message, extra_prompt_messages=extra_prombt)
        llm = ChatOpenAI(temperature=kwargs.get("temperature", 0), model=kwargs.get("model", MainConfig.MODEL_GPT.value),
                         verbose=kwargs.get("verbose", False))

        agent = CustomOpenAIFunctionsAgent(
            llm=llm,
            prompt=prombt,
            tools=tools,
            memory=memory,
            **kwargs,
        )
        self.executor = CustomAgentExecutor.from_agent_and_tools(
            agent=agent,
            tools=tools,
            max_iterations=kwargs.get("max_iterations", 10),
            memory=memory,
            **(kwargs or {}),
        )
        return self
