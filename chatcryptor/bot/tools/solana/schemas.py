
from pydantic import BaseModel, Field
from typing import Optional


class InputCoinAddress(BaseModel):
    address: str = Field(
        description="Token Address String, a hash string or a symbol string. Eg EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v or USDC")


class InputAccountAddress(BaseModel):
    address: str = Field(
        description="Account Address String, a hash string or a symbol string. Eg GS8E7WcrNL9dW8epVzUETnVvqJGz1ysc1uhNZhMCSaKS")


class InputSearchKeyword(BaseModel):
    keyword: str = Field(
        description="A keyword string, it is a symbol string or name of token")


class InputAccountBalance(BaseModel):
    address: str = Field(
        description="Account Address String, a hash string or a symbol string. Eg GS8E7WcrNL9dW8epVzUETnVvqJGz1ysc1uhNZhMCSaKS")
    token: Optional[str] = Field(
        description="Token Address String, a hash string or a symbol string. Eg GS8E7WcrNL9dW8epVzUETnVvqJGz1ysc1uhNZhMCSaKS or USDC")
