# from datetime import datetime, timedelta, timezone
# from typing import Any, Union
# import jwt
from passlib.context import CryptContext
# from app.core.config import settings

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)