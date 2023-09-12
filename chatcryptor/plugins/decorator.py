from chatcryptor.config import MainConfig, logging
from typing import *
import functools

logger = logging.getLogger(__name__)


def set_plugin(name: str,
               description: str,
               tags: Optional[str] = []):
    """
      A decorator help create a plugin from a function
    """
    logger.debug(f"Add plugin: [{name}] with tags: [{tags}]")

    def inner_handle(func):
        def wrapper_func(*args, **kwargs):
            return func(*args, **kwargs)
        wrapper_func._plugin_metadata = {
            "name": name,
            "description": description,
            "tags": tags,
            "func": func.__name__
        }
        return wrapper_func
    return inner_handle


def aset_plugin(name: str,
                description: str,
                tags: Optional[str] = [],
                priority: Optional[int] = 0
                ):
    """
      A decorator help create a plugin from a function
    """
    logger.debug(f"Add plugin: [{name}] with tags: [{tags}]")

    def inner_handle(func):

        @functools.wraps(func)
        async def wrapper_func(*args, **kwargs):
            return await func(*args, **kwargs)
        wrapper_func._plugin_metadata = {
            "name": name,
            "description": description,
            "tags": tags,
            "func": func.__name__,
            "priority": priority or 0
        }
        return wrapper_func
    return inner_handle
