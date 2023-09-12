import logging
from chatcryptor.app.utils.jwt import encode
from google.oauth2 import id_token
from google.auth.transport import requests
from chatcryptor.bot.utils.exceptions import ExceptionRequestAPIError
from chatcryptor.db.mongodb import MongodbClient

from chatcryptor.config import MainConfig

logger = logging.getLogger(__name__)


async def __check_email_exist(email):
    mongo = MongodbClient()
    db = mongo.get_db(mongo.config.get('db'))
    user = db.user.find_one({"email": email})
    if (user):
        return True
    else:
        return False


async def create_user(email: str, name: str):
    mongo = MongodbClient()
    db = mongo.get_db()
    db.user.insert_one({"email": email, "name": name})


async def sign_by_email(token: str):
    try:
        idinfo = id_token.verify_oauth2_token(
            token, requests.Request(), MainConfig.GG_CLIENT_ID.value)
    except BaseException as er:
        raise ExceptionRequestAPIError("Token is invalid or expired")
    else:
        email = idinfo['email']
        name = idinfo['name']

        email_exist = await __check_email_exist(email)
        if (email_exist == False):
            await create_user(email, name)

        return encode({"email": email, "name": name, "token": token }) 
    
async def sign_by_email_for_extension(token: str):
    import requests
    api_key = MainConfig.GG_API_KEY.value
    error = None
    try:
        if token.strip() == '':
            raise ValueError()
        api_url = MainConfig.GG_AUTHENT_URL.value.replace('{api_key}', api_key)
        logger.debug(f"Using api to authent: {api_url}")
                                                          
        request = requests.get(api_url, headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json' 
        })
        data = error = request.json()
        if request.status_code < 400:
            data = request.json()
            email = data.get('emailAddresses')[0]['value']
            name = data.get('names')[0]['displayName']

            email_exist = await __check_email_exist(email)
            if (email_exist == False):
                await create_user(email, name)
            return encode({"email": email, "name": name, "token": token }) 
    except BaseException as e:
        logger.debug(f'Error when try to authent user: {token}: error: {error}')
    raise ExceptionRequestAPIError("Token is invalid or expired")