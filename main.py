# Import things that are needed generically
from chatcryptor.bot.tools.solana.solana_onchain_tool import *
from chatcryptor.bot.tools.solana.utils import get_type_of_address
from chatcryptor.config import MainConfig, logging
import chatcryptor.app.server as http_app

if __name__ == "__main__":
    http_app.create_server()
