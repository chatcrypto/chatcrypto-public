"""
Some validation functions for validate data
"""
from chatcryptor.utils.solana.solana_rpc import _call_rpc
from chatcryptor.utils.solana.solscan_api import _call_api
from chatcryptor.bot.utils.validator import validate_address_blockchain, validate_arguments
from pydantic import BaseModel, ValidationError
from chatcryptor.bot.utils.exceptions import ExceptionNeedShowMessage


@validate_arguments
def get_type_of_address(address: validate_address_blockchain) -> str:
    """
    Detect an address is token, token account or account
    If this address not found, return None
    """
    q = _call_api('account', params={
        "address": address
    })
    if not q.get('succcess'):
        return None
    data = q.get('data', {})
    if data.get('ownerProgram') is 'BPFLoader2111111111111111111111111111111111' or data.get('executable') is True:
        return 'program'

    if data.get('ownerProgram') == '11111111111111111111111111111111' or data.get('type') == 'system_account':
        return 'account'

    if data.get('ownerProgram') == 'TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA' or data.get('type') == 'token_account':
        return 'token_account'
    return 'account'


def find_token_address(token) -> str:
    try:
        type_account = get_type_of_address(token)
        if (type_account != 'token'):
            raise Exception(
                'This address is not a token, please enter a valid address')
        else:
            return token
    except BaseException as e:
        rs = _call_api('search', params={
            'keyword': token
        })
        if (rs and rs.get('data')):
            datas = rs['data']
            for x in datas:
                if (x['type'] == 'tokens'):
                    tokens = x['result']
                    if (tokens):
                        k = tokens[0]
                        return {
                            'symbol': k.get('symbol'),
                            'name': k.get('name'),
                            'address': k.get('address')
                        }
        raise ExceptionNeedShowMessage(f'token "{token}" not found')
