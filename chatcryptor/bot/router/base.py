
from ...config import MainConfig, logging
from chatcryptor.bot.router.register import REGISTER_EXECUTORS
from chatcryptor.bot.extraction.base import EntityExecutor, EntityExtraction
from chatcryptor.bot.utils.exceptions import ExceptionNoExecutorToPick, NoAvailabelTools
from langchain.memory import ReadOnlySharedMemory
from chatcryptor.bot.base.base_executor import DefaultExcecutor
from chatcryptor.bot.memory.base import create_memory_instance, create_readonly_memory
from chatcryptor.bot.prompts.main import HUNMAN_PREFIX
from chatcryptor.enums.entity import EXTRACTION_ACTION_TYPE
import json
import chatcryptor.utils.response as Response
from chatcryptor.enums.response import AI_METHOD, MODEL_TYPE, REPONSE_CHART_TYPE
from chatcryptor.enums.platform import SUPPORT_PLATFORM
import traceback
logger = logging.getLogger(__name__)


class RouterPipeLine:
    """
    A Router Pipeline that will help answer the question of users.
    This tool will pick up executors by detect group tags.
    Example usage:
    from chatcryptor.bot.router.base import RouterPipeLine
    router = RouterPipeLine().setup()
    answrer = router.set_input("I want to information of token USDC and some holders of account 12sdfa12312312312 on solana").run(callback...)
    """
    _list_executors = []
    _input: str = ""
    _extract_executor: EntityExecutor = None
    _entity_extraction: EntityExtraction = None
    _default_executor: DefaultExcecutor = None
    _default_blockchain_network: str = None
    _list_picked_executors = []
    _memory = None
    _readonly_memory = None

    def __init__(self) -> None:
        logger.info(f'Create EntityParser instance and save to singleton')

    def setup(self, enable_memory=False, session_id: str = '', default_blockchain_network=''):
        if enable_memory:
            self._memory = create_memory_instance(
                session_id=session_id, store_ai_answer=False)
            self._readonly_memory = create_readonly_memory(memory=self._memory)

        self._default_blockchain_network = default_blockchain_network if default_blockchain_network in SUPPORT_PLATFORM.values() else None
        self._extract_executor = EntityExecutor().setup(memory=self._readonly_memory)
        self._default_executor = DefaultExcecutor().setup(
            memory=self._readonly_memory,
            verbose=False if MainConfig.LOG_LEVEL.value > 11 else True
        )
        self.register_chain()
        return self

    def begin(self):
        self._entity_extraction = EntityExtraction()
        self._list_picked_executors = []
        self._input = ""
        return self

    def register_chain(self):

        self._list_executors = []
        for item in REGISTER_EXECUTORS:
            init = item()
            logger.debug(f'Add executor {item.__name__}')
            init.setup(memory=self._memory,
                       verbose=False if MainConfig.LOG_LEVEL.value > 11 else True)
            self._list_executors.append(init)
        return self

    def set_input(self, input: str):
        if input.strip() == "":
            raise ValueError('Input need to be a str and not empty')
        self._input = input
        return self

    def start_extract_tagging(self, **kwargs):
        if self._input.strip() == "":
            raise ValueError('Input need to be a str and not empty')
        self._entity_extraction = self._extract_executor.run(
            input=self._input, **kwargs).clean(is_copy=True)
        if not self._entity_extraction.blockchain_platform and self._default_blockchain_network:
            self._entity_extraction.blockchain_platform = [
                self._default_blockchain_network]
        return self

    def pick_executor(self):
        self._list_picked_executors = []
        parser = self._entity_extraction.all_values
        _entities = parser if type(parser) is list else [parser]
        for ex in self._list_executors:
            # validate platform supported
            if not list(set(self._entity_extraction.blockchain_platform) & set(ex.all_groups)) or EXTRACTION_ACTION_TYPE.ACTION_DEFINITION.value in self._entity_extraction.action:
                continue
            # validate other tag
            if list(set(_entities) & set(ex.all_groups)):
                self._list_picked_executors.append(ex)
        return self

    def validate(self):
        extract = self._entity_extraction
        if self._input.strip() == "":
            raise ValueError('Input need to be a str and not empty')
        if not extract.entity_type or not extract.blockchain_platform:
            logger.debug(
                f'Cannot extract available entities from input: {self._input}')
            self._list_picked_executors = []
            return self

    @staticmethod
    def response_message(message):
        """
        Unify response to user
        """
        if type(message) is Response.ChatResponse:
            return message
        return Response.ChatResponse(
            method=AI_METHOD.AGENT.value,
            title='',
            description='',
            model_type=MODEL_TYPE.TRAINING.value,
            chart_type=REPONSE_CHART_TYPE.TEXT.value,
            tool='',
            data=message,
            is_raw=True
        )

    def run(self, input: str,
            extract_kwargs={},
            **kwargs):
        """
        Run a pipeline router to find best answer for user question.
        Firstly, router will find tags thats extracted from question, follow model EntityExtraction.
        Next step, router will pick executors that're available with these tags.
        Finally, router will run these picked executors. If there is no picked executors, router will use default executor to run.
        """
        try:
            self.begin()
            self.set_input(input=input)
            self.start_extract_tagging(**extract_kwargs)
            self.pick_executor()
            self.validate()
            logger.debug(
                f"Extracted data from input: {self._entity_extraction}")
            rs = []

            if not self._list_picked_executors:
                logger.debug(f"Run default executor to answer question")

                rs = [RouterPipeLine.response_message(self._default_executor.run(input=HUNMAN_PREFIX.replace('{input}', self._input),
                                                                                 **kwargs))]
            else:
                for ex in self._list_picked_executors:
                    rs.append(RouterPipeLine.response_message(ex.run(
                        input=self._input, groups=self._entity_extraction.required_values, **kwargs)))
            logger.debug(f'Question: {input} has answer: \n {rs}')
            return rs
        except BaseException as e:
            logger.debug(traceback.print_exc())

            return [
                RouterPipeLine.response_message(
                    message="Apologies, but it seems that we have no answer for your input. We will upgrade knowledge in the feature."
                )
            ]

    def arun(self, input: str, **kwargs):
        return []
