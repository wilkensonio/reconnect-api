from fastapi import Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from hashlib import sha256
from .. import models, database


api_key_header = APIKeyHeader(name="R-API-KEY", auto_error=False)


async def validate_api_key(api_key: str = Security(api_key_header),
                           db: Session = Depends(database.get_db)):
    if not api_key:
        raise HTTPException(
            status_code=403, detail="API key is required")

    secret_entries = db.query(models.Secret).all()

    if not secret_entries:
        raise HTTPException(
            status_code=403, detail="your are not authorized")

    hashed_secret_keys = {
        secret_entry.api_secret_key for secret_entry in secret_entries}

    hashed_api_key = sha256(api_key.encode()).hexdigest()

    if hashed_api_key not in hashed_secret_keys:
        raise HTTPException(
            status_code=403, detail="Could not validate API key")

    return True  # API key is valid
