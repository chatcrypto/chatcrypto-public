
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from chatcryptor.enums.entity import MAIN_ENTITY_TYPE, ENTITY_PROPERTIES, EXTRACTION_ACTION_TYPE
from chatcryptor.enums.platform import SUPPORT_PLATFORM
from pydantic import (
    BaseModel,
    ValidationError
)


class EntityExtraction(BaseModel):
    entity_type: Optional[List[str]] = Field(
        enum=MAIN_ENTITY_TYPE.values(),
        description=f"describle entity type from input. Entity type is object that is related to Blockchain. Eg: {','.join(MAIN_ENTITY_TYPE.values())}",
        default=[]
    )
    entity_properties: Optional[List[str]] = Field(
        enum=ENTITY_PROPERTIES.values(),
        description=f"describle entity properties from input. Entity properties is property that an entity have. Example Token has amount tokens, Account has holders...",
        default=[]
    )
    blockchain_platform: Optional[List[str]] = Field(
        description=f"describle blockchain network platform from input. For example: {','.join([k.value for k in SUPPORT_PLATFORM])}",
        default=[],
        enum=[e.value for e in SUPPORT_PLATFORM],
    )

    action: Optional[List[str]] = Field(
        description=f"describle what type of actions from input. For example: {','.join(EXTRACTION_ACTION_TYPE.values())}",
        default=[]
    )

    def clean(self, is_copy=True):
        entity_type = [k.lower() for k in self.entity_type if k.lower()
                       in MAIN_ENTITY_TYPE.values()]
        entity_properties = [
            k.lower() for k in self.entity_properties if k.lower() in ENTITY_PROPERTIES.values()]
        blockchain_platform = [k.lower() for k in self.blockchain_platform if k.lower() in [
            e.value for e in SUPPORT_PLATFORM]]
        action = [k.lower() for k in self.action]
        if is_copy:
            return EntityExtraction(
                entity_type=entity_type,
                entity_properties=entity_properties,
                blockchain_platform=blockchain_platform,
                action=action
            )
        else:
            self.entity_type = entity_type
            self.entity_properties = entity_properties
            self.blockchain_platform = blockchain_platform
            return self

    @property
    def all_values(self):
        return self.entity_properties + self.entity_type + self.blockchain_platform

    @property
    def required_values(self):
        return self.entity_properties + self.entity_type + self.blockchain_platform
