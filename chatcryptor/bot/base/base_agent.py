from langchain.agents.openai_functions_agent.base import *
from langchain.agents.agent import *
import langchain.agents.openai_functions_agent.base as BaseOpenAIFunctionsAgent
from langchain.agents.openai_functions_agent.base import OpenAIFunctionsAgent, _format_intermediate_steps, _parse_ai_message
import langchain.agents.agent as BaseAgentExecuter
from langchain.tools.base import *
import chatcryptor.utils.response as Response
from chatcryptor.bot.utils.exceptions import NoAvailabelTools


class CustomOpenAIFunctionsAgent(OpenAIFunctionsAgent):
    """
    A Custom Class for add more functionals to OpenAIFunctionsAgent
    """
    @property
    def input_keys(self) -> List[str]:
        """Return the input keys.

        :meta private:
        """
        return super().input_keys

    def plan(
        self,
        intermediate_steps: List[Tuple[AgentAction, str]],
        callbacks: Callbacks = None,
        with_functions: bool = True,
        groups: Optional[List[str]] = [],
        **kwargs: Any,
    ) -> Union[AgentAction, AgentFinish]:
        """Given input, decided what to do.

        Args:
            intermediate_steps: Steps the LLM has taken to date, along with observations
            **kwargs: User inputs.

        Returns:
            Action specifying what tool to use.
        """
        agent_scratchpad = _format_intermediate_steps(intermediate_steps)
        selected_inputs = {
            k: kwargs[k] for k in self.prompt.input_variables if k != "agent_scratchpad" and kwargs.get(k) is not None
        }

        full_inputs = dict(**selected_inputs,
                           agent_scratchpad=agent_scratchpad)

        prompt = self.prompt.format_prompt(**full_inputs)
        messages = prompt.to_messages()
        functions = []
        # allow filter tools with groups

        if groups and type(groups) is list:
            for f in self.tools:
                if hasattr(f, 'groups') and getattr(f, 'groups') and not [k for k in groups if k.lower() not in getattr(f, 'groups')]:
                    functions.append(dict(format_tool_to_openai_function(f)))
            if not functions:
                raise ValueError(
                    f"There are no available tools for groups: {groups}")
        if with_functions:
            predicted_message = self.llm.predict_messages(
                messages,
                functions=functions or self.functions,
                callbacks=callbacks,
            )
        else:
            predicted_message = self.llm.predict_messages(
                messages,
                callbacks=callbacks,
            )
        agent_decision = _parse_ai_message(predicted_message)
        return agent_decision

    async def aplan(
        self,
        intermediate_steps: List[Tuple[AgentAction, str]],
        callbacks: Callbacks = None,
        **kwargs: Any,
    ) -> Union[AgentAction, AgentFinish]:
        """Given input, decided what to do.

        Args:
            intermediate_steps: Steps the LLM has taken to date,
                along with observations
            **kwargs: User inputs.

        Returns:
            Action specifying what tool to use.
        """
        agent_scratchpad = _format_intermediate_steps(intermediate_steps)
        selected_inputs = {
            k: kwargs[k] for k in self.prompt.input_variables if k != "agent_scratchpad"
        }
        full_inputs = dict(**selected_inputs,
                           agent_scratchpad=agent_scratchpad)
        prompt = self.prompt.format_prompt(**full_inputs)
        messages = prompt.to_messages()
        functions = []
        # allow filter tools with groups
        if kwargs.get('groups') and type(kwargs.get('groups')) is list:
            for f in self.tools:
                if hasattr(f, 'groups') and getattr(f, 'groups') and not [k for k in kwargs.get('groups') if k.lower() not in getattr(f, 'groups')]:
                    functions.append(dict(format_tool_to_openai_function(f)))
            if not functions:
                raise NoAvailabelTools(
                    f"There are no available tools for groups: {kwargs.get('groups')}")
        predicted_message = await self.llm.apredict_messages(
            messages, functions=functions or self.functions, callbacks=callbacks
        )
        agent_decision = _parse_ai_message(predicted_message)
        return agent_decision


class CustomAgentExecutor(BaseAgentExecuter.AgentExecutor):
    """
    Format all results of agents to a Defined Response.
    """
    pass
