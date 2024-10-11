import os
import jwt
from fastapi import HTTPException
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """Create an access token for the user

    Args:
        data (dict): User details
        expires_delta (timedelta, optional): Token expiration time. Defaults to None.    
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(datetime.astimezone.utc) + \
            timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str):
    """Verify the token

    Args:
        token (str): Token to verify
    """
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # palyoad
    except jwt.ExpiredSignatureError:
        return HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        return HTTPException(status_code=401, detail="Token has expired")
    except Exception as e:
        return {"token_error": str(e)}
