
from enum import Enum
import logging
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path='./.env')


class MainConfig(Enum):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    API_VERSION = os.getenv('API_VERSION') or 'v1.0'
    # Define API KEY for OpenAI
    OPENAI_API_KEY = str(os.getenv('OPENAI_API_KEY')
                         )
    LOG_LEVEL = int(os.getenv('LOG_LEVEL')) or logging.INFO
    
    MAXIMUM_RESULT_OF_PLUGINS = 200

    # Define Mainnet Node of Solana
    SOLANA_MAINNET = os.getenv(
        'SOLANA_MAINNET') 

    # Define APIs of Solscan
    SOLSCAN_API = os.getenv(
        'SOLSCAN_API') or "https://api.solscan.io"

    # Define APIs of Solscan
    SOLSCAN_PRO_API = os.getenv(
        'SOLSCAN_PRO_API') or "https://pro-api.solscan.io"

    # Define URL of redis
    REDIS_URL = os.getenv(
        'REDIS_URL') or "redis://localhost:6379/0"

    # Define max data return to user
    MAX_ITEMS_RESULT = int(os.getenv('MAX_ITEMS_RESULT') or 0) or 5

    # Maximum length for user question
    MAX_USER_INPUT_LENGTH = int(os.getenv('MAX_USER_INPUT_LENGTH') or 0) or 200

    # Define port for http app
    WEBSOCKET_PORT = int(os.getenv('WEBSOCKET_PORT') or 0) or 9999
    HTTP_PORT = int(os.getenv('HTTP_PORT') or 0) or 8080
    HTTP_HOST = os.getenv('HTTP_HOST') or "localhost"

    SOLSCAN_DOMAIN = os.getenv(
        'SOLSCAN_DOMAIN') or "https://solscan.io"
    APTSCAN_DOMAIN = os.getenv(
        'APTSCAN_DOMAIN') or "https://aptscan.ai"

    MODEL_GPT = os.getenv('MODEL_GPT') or "gpt-3.5-turbo-16k"

    # Define config for google oauth client
    GG_CLIENT_ID = os.getenv('GG_CLIENT_ID')
    GG_CLIENT_SECRET = os.getenv('GG_CLIENT_SECRET')
    GG_API_KEY = os.getenv('GG_API_KEY') or ''
    GG_AUTHENT_URL = os.getenv(
        'GG_AUTHENT_URL') or "https://people.googleapis.com/v1/people/me?personFields=names,emailAddresses&key={api_key}"

    # Define jwt
    JWT_SECRET = os.getenv('JWT_SECRET') or "Z3YNfe19volX3iffrUwv8IVJoM9tSw76"

    MONGODB_URI = {
        'main': {
            'uri': os.getenv('MONGODB_MAIN') or 'localhost:27017',
            'db':  os.getenv('MONGODB_MAIN_DB') or '',
            'options': {
                'directConnection': True if os.getenv('MONGODB_MAIN_DIRECTCONNECTION') == 'true' else False,
            }
        },
        'crawl_data': {
            'uri': os.getenv('MONGODB_CRAWL') or 'localhost:27017',
            'db':  os.getenv('MONGODB_CRAWL_DB') or '',
            'options': {
                'tls': True,
                'tlsCAFile': f'{ROOT_DIR}/ssl/global-bundle.pem',
                'tlsAllowInvalidHostnames': True,
                'directConnection': True
            }
        }
    }

    CLICKHOUSE_URI = {
        'main': {
            'uri': os.getenv('CLICKHOUSE_MAIN') or 'localhost:8123',
            'options': {}
        }
    }

    

# Init Logger
logging.basicConfig(
    level=MainConfig.LOG_LEVEL.value,
    format="[%(filename)s:%(lineno)s] %(asctime)s [%(levelname)s] %(message)s" if MainConfig.LOG_LEVEL.value < 11 else "%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)

# Init API KEY
os.environ["OPENAI_API_KEY"] = MainConfig.OPENAI_API_KEY.value
