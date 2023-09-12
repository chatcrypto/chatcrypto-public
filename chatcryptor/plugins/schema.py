from pydantic import BaseModel, Field
from typing import *
from pydantic import BaseModel, validator, Field
from chatcryptor.models.db_models import DomainConfiguration

from typing import (
    Any,
    List,
    Optional
)


class DatabaseLoader(BaseModel):

    main_mongodb: Optional[Any] = Field(
        description="Load mongodb instance", default=None)
    main_redis: Optional[Any] = Field(
        description="Load redis instance", default=None)
    main_clickhouse: Optional[Any] = Field(
        description="Load clickhouse instance", default=None)


class PluginParams(BaseModel):

    # store module chatcryptor.utils.response
    response_module: Optional[Any] = Field(default=None)
    chat_module: Optional[Any] = Field(
        default=None)  # store module chatcryptor.bot
    utils_module: Optional[Any] = Field(
        default=None)  # store module chatcryptor.utils
    domain_configuratioin: Optional[DomainConfiguration] = Field(default=None)
