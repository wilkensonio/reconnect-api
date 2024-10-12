import os
import jwt
from fastapi import HTTPException
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from fastapi import status
from dotenv import load_dotenv


load_dotenv()  # Load environment variables from .env file

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 45

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/token")


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create an access token for the user

    Args:
        data (dict): User details
        expires_delta (timedelta, optional): Token expiration time. Defaults to None.    
    """

    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + \
            timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str):
    """Verify the token

    Args:
        token (str): Token to verify
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[
                             ALGORITHM])
        current_user = payload.get("sub")
        if not current_user:
            raise credentials_exception
        return current_user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Token verification error: {str(e)}")
