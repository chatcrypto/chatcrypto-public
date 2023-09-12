"""
Validate arguments of function by library pydantic v1
Documents: https://docs.pydantic.dev/1.10/usage/validation_decorator/
Example:
 from chatcryptor.bot.utils.validator import validate_address_blockchain,validate_arguments
     
 @validate_arguments
 def how_many(num: validate_address_blockchain):
        print(num)
        return num

"""
from pydantic import Field, validate_arguments
from typing_extensions import Annotated
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Mapping, Optional, Tuple, Type, TypeVar, Union, overload
from chatcryptor.bot.utils.decorators import handle_error_validator
from chatcryptor.bot.utils.decorators import logging_params
# validate address string must be an address of blockchain account
validate_address_blockchain = Annotated[str, Field(min_length=30)]
