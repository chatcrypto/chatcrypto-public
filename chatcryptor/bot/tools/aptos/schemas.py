
from pydantic import BaseModel, Field
from typing import Optional


class InputCoinAddress(BaseModel):
    coin: str = Field(
        description="Token Address String, a hash string or a symbol string. Eg 0x4def3d3dee27308886f0a3611dd161ce34f977a9a5de4e80b237225923492a2a::coin::T or USDC")


class InputAccountAddress(BaseModel):
    address: str = Field(
        description="Account Address String, a hash string or a symbol string. Eg GS8E7WcrNL9dW8epVzUETnVvqJGz1ysc1uhNZhMCSaKS")


class InputSearchKeyword(BaseModel):
    keyword: str = Field(
        description="A keyword string, it is a symbol string or name of token")


class InputAccountBalance(BaseModel):
    address: str = Field(
        description="Account Address String, a hash string or a symbol string. Eg GS8E7WcrNL9dW8epVzUETnVvqJGz1ysc1uhNZhMCSaKS")
    coin: Optional[str] = Field(
        description="Coin Address String, a hash string or a symbol string. Eg 0xf22bede237a07e121b56d91a491eb7bcdfd1f5907926a9e58338f964a01b17fa::asset::USDT or USDC")


class InputModule(BaseModel):
    module_id: str = Field(
        description="Module Id in aptos. Eg 0x1::Account")
