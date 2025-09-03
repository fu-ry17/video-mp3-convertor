from datetime import datetime, timedelta
import logging
import uuid
from jwt.exceptions import PyJWTError
import bcrypt
import jwt

from src.settings import settings

def hash_password(password: str):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def compare_password(password: str, hash: str):
    return bcrypt.checkpw(password.encode('utf-8'), hash.encode('utf-8'))

def generate_token(user_data: dict, exp: timedelta, refresh: bool = False):
    payload = {
        'user': user_data,
        'exp': datetime.now() + exp,
        'jti': str(uuid.uuid4()),
        'refresh': refresh
    }

    return jwt.encode(
        payload=payload,
        key=settings.JWT_SECRET,
        algorithm="HS256"
    )

def decode(token):
    try:
        return jwt.decode(token, key=settings.JWT_SECRET, algorithms=["HS256"])
    except jwt.PyJWTError as e:
        logging.error(e)
        return None
