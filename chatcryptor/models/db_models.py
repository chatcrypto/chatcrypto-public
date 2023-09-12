from chatcryptor.db.mongodb import MongodbClient
from pydantic import BaseModel, Field
from typing import (
    Any,
    Dict,
    List,
    Optional

)


class TokenInfo (BaseModel):

    token_address: str
    platform: str
    symbol: str
    name: str
    current_price: Optional[float]
    description: Optional[str]
    icon: Optional[str]
    metadata: Optional[dict]

    @staticmethod
    def mongodb_collection():
        return MongodbClient().get_collection('dim_coingecko_token_detail')

    @staticmethod
    def get_token_info(token_address, platform):
        info = TokenInfo.mongodb_collection().find_one({
            f'data.platforms.{platform}': token_address
        })
        if (info):
            data = info.get('data', {})
            return TokenInfo(
                token_address=token_address,
                platform=platform,
                symbol=data.get('symbol', ''),
                name=data.get('name', ''),
                icon=data.get('image', {}).get('thumb'),
                description=(data.get('description', {}) or {}).get('en')
            )
        return


class FavouriteQuestion(BaseModel):
    text: str
    user_creator: Optional[str]
    created_time: Optional[int]
    status: Optional[int]

    @staticmethod
    def mongodb_collection():
        return MongodbClient().get_collection('favourite_question')

    @staticmethod
    def get_all_messages():
        info = FavouriteQuestion.mongodb_collection().find({
            "status": 1
        }).sort("created_time", -1)
        ls = []
        for item in info:
            ls.append(FavouriteQuestion(
                text=item.get('text', ''),
                user_creator=item.get('user_creator')
            ))
        return ls


class DomainConfiguration(BaseModel):
    domain: str
    token_symbol: Optional[str]
    token_name: Optional[str]
    network: Optional[List[str]]
    defillama_id: Optional[str]
    coingecko_id: Optional[str]
    tags: Optional[List[str]] = []
    token_id: Optional[dict] = {}

    @staticmethod
    def mongodb_collection():
        return MongodbClient().get_collection('domain_configuration')

    @staticmethod
    def find_by_domain(domain: str):
        info = DomainConfiguration.mongodb_collection().find_one({
            "domain": domain})
        if info:
            return DomainConfiguration(
                domain=info.get('domain'),
                token_symbol=info.get('token_symbol', ''),
                token_name=info.get('token_name', ''),
                network=info.get('network', ''),
                defillama_id=info.get('defillama_id', ''),
                coingecko_id=info.get('coingecko_id', ''),
                tags=info.get('tags', []) or [],
                token_id=info.get('token_id', {}) or {}
            )
        return
