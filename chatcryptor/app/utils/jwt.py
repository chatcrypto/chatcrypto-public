
from datetime import datetime, timedelta, timezone
import jwt
from chatcryptor.config import MainConfig


def encode(payload):
    return jwt.encode({
                **payload,
                "exp": (datetime.now(tz=timezone.utc) + timedelta(seconds=60 * 60 * 24 * 5)), # 5 days
                "iat": datetime.now(tz=timezone.utc)
                },
                MainConfig.JWT_SECRET.value, algorithm="HS256")
    

def decode(encoded):
    return jwt.decode(encoded, MainConfig.JWT_SECRET.value, algorithm="HS256")