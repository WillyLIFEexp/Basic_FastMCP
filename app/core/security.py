from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt, ExpiredSignatureError
from passlib.context import CryptContext
from app.core.config import settings
from fastapi import HTTPException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """getting the hashed password from database

    Args:
        password (str): User's input password

    Returns:
        str: Hashed password
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Chekcing if the password is valid

    Args:
        plain_password (str): User input password
        hashed_password (str): Hashed password 

    Returns:
        bool: Check if the input and the hashed password is the same.
    """
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Getting Access token and the expired time is 1 min

    Args:
        data (dict): The information about the key that will be created.
        expires_delta (timedelta | None, optional): The expired time to set. Defaults to None.

    Returns:
        str: The Access string for the JWT
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")

def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    """Getting refresh token and the expired time is 1 min

    Args:
        data (dict): The information about the key that will be created.
        expires_delta (timedelta | None, optional): The expired time to set. Defaults to None.

    Returns:
        str: The refresh string for the JWT
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc)+ (expires_delta or timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_DAYS))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")

def decode_token(token: str) -> dict:
    """Decode the token to check if the token is expired or not

    Args:
        token (str): User input token

    Raises:
        ExpiredSignatureError: Token has expired
        JWTError: Invalid token

    Returns:
        dict: Decode JWT data
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"], options={"verify_exp": True}) 
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")