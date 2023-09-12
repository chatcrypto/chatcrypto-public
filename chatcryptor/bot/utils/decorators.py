from langchain.tools import StructuredTool, Tool
from chatcryptor.config import  MainConfig, logging
from chatcryptor.bot.base.base_tool import CustomeTool, CustomeStructuredTool
import traceback
import functools
import json
import chatcryptor.utils.response as Response
from pydantic import BaseModel, ValidationError
from typing import Any, Awaitable, Callable, Dict, Optional, Tuple, Type, Union, List
from chatcryptor.bot.utils.exceptions import ExceptionNeedShowMessage
from chatcryptor.utils.response import ChatResponse, MODEL_TYPE, AI_METHOD
import re
logger = logging.getLogger(__name__)


def force_async(fn):
    '''
    turns a sync function to async function using threads
    '''
    from concurrent.futures import ThreadPoolExecutor
    import asyncio
    pool = ThreadPoolExecutor()

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        future = pool.submit(fn, *args, **kwargs)
        return asyncio.wrap_future(future)  # make it awaitable

    return wrapper


def force_sync(fn):
    '''
    turn an async function to sync function
    '''
    import asyncio

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        res = fn(*args, **kwargs)
        if asyncio.iscoroutine(res):
            return asyncio.get_event_loop().run_until_complete(res)
        return res

    return wrapper


def generate_tool_from_func(name: str, description: str, is_structured_tool=False,
                            prefix_name: str = "",
                            suffix_name="",
                            prefix_description="",
                            suffix_description="",
                            args_schema: Optional[Type[BaseModel]] = None,
                            groups=[],
                            **tool_kwargs):
    """
      A decorator help create a Tool from a function
    """
    def inner_handle(func):
        def wrapper_func(direct=False, *args, **kwargs) -> Tool:
            """
                If need to process function directly and dont need to generate a Tool,
                please set direct param is True
            """
            tool_name = f"{prefix_name}{name}{suffix_name}"
            clean_description = description.replace(
                '\n', ' ').strip() if description else ''
            des = f"{prefix_description} {(re.sub(' +', ' ',clean_description.strip()) if clean_description else '')} {suffix_description}"
            if (direct is True):
                kwargs['direct'] = True
                return func(*args, **kwargs)
            tool_tags = groups or kwargs.get('groups')
            logger.debug(
                f"Create tool by decorator for function: [{tool_name}]. Groups: {tool_tags}")

            if not is_structured_tool:
                return CustomeTool.from_function(
                    name=tool_name,
                    func=func,
                    description=des,
                    coroutine=force_async(func),
                    groups=tool_tags,
                    args_schema=args_schema,
                    **tool_kwargs
                )
            else:
                return CustomeStructuredTool.from_function(
                    name=tool_name,
                    func=func,
                    description=des,
                    coroutine=force_async(func),
                    groups=tool_tags,
                    args_schema=args_schema,
                    **tool_kwargs
                )
        return wrapper_func
    return inner_handle


def handle_error_validator(message="Error when excecute this function", data=""):
    """
      A decorator help handle exception of validating params for a function
    """
    def inner_handle(func):
        def wrapper_func(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ExceptionNeedShowMessage as e:
                logger.error(
                    f'Error when execute function [{func.__name__}. Error: {str(e)}]')
                logger.debug(traceback.print_exc())
                return ChatResponse(
                    error=True,
                    data=data or f'Apologies, but it seems that we have no answer for your input. {e}',
                    error_message=message or str(e),
                    is_raw=True,
                    model_type=MODEL_TYPE.TRAINING.value,
                    title='',
                    method=AI_METHOD.AGENT.value
                )

            except BaseException as e:
                logger.error(
                    f'Error when execute function [{func.__name__}. Error: {str(e)}]')
                logger.debug(traceback.print_exc())
                return ChatResponse(
                    error=True,
                    data=data or f'Apologies, but it seems that we have no answer for your input.',
                    error_message=message or str(e),
                    is_raw=True,
                    model_type=MODEL_TYPE.TRAINING.value,
                    title='',
                    method=AI_METHOD.AGENT.value
                )

        return wrapper_func
    return inner_handle


def logging_params(func):
    def wrapper_func(*args, **kwargs):
        logger.debug(
            f'[LOGGING_PARAMS] Params for func: [{func.__name__}] are: {args} or {kwargs}]')
        return func(*args, **kwargs)
    return wrapper_func
