
import logging
from chatcryptor.app.modules.authentication.auth import sign_by_email, sign_by_email_for_extension
from chatcryptor.app.utils.response import json_response_error, json_response_success
from chatcryptor.app.app import app
from fastapi import Request
import json
logger = logging.getLogger(__name__)


@app.post('/auth/gmail')
async def auth_gmail(request: Request):
    # Specify the CLIENT_ID of the app that accesses the backend:
    payload = await request.json()
    token = payload['token']
    logger.debug(f"User: {token} require login for website...")
    jwt_token = await sign_by_email(token)
    return json_response_success({'access_token': jwt_token})

@app.post('/auth/gmail/extension')
async def auth_gmail_extension(request: Request):
    # Specify the CLIENT_ID of the app that accesses the backend:
    try:
        payload = await request.json()
    except BaseException as e:
        payload = await request.body()
        payload = json.loads(payload)
    
    if not payload.get('token') or payload.get('token', '').strip() == '':
        return json_response_error(error='Missing token param')
    token = payload.get('token')
    logger.debug(f"User: {token} require login for extension...")
    jwt_token = await sign_by_email_for_extension(token)
    return json_response_success({'access_token': jwt_token})