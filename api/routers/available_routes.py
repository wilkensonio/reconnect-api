# Description: API routes for the application
import os
from .. import database
from ..crud import crud_available
from ..schemas import available_schema as schemas
from ..schemas import response_schema
from ..utils import jwt_utils
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from dotenv import load_dotenv

load_dotenv()
EXPRIRES_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")


router = APIRouter()


available = crud_available.AvailableCrud()


@router.post("/availability/create/", response_model=schemas.Available)
def create_availability(availability: schemas.CreateAvailability,
                        db: Session = Depends(database.get_db),
                        token: str = Depends(jwt_utils.oauth2_scheme)) -> schemas.Available:
    """Add a new availability: Enter day and time available

    Args:

        availability (schemas.CreateAvailability): Availability details 

    Returns:

        schemas.Available: Availability details"""

    jwt_utils.verify_token(token)

    return available.create_availability(db, availability)

# Get availability by ID


@router.get("/availability/get-by-id/{available_id}", response_model=response_schema.AvailableResponse)
def get_availability_by_id(available_id: int, db: Session = Depends(database.get_db),
                           token: str = Depends(jwt_utils.oauth2_scheme)) -> schemas.Available:
    """Get availability by ID

    Args:

        available_id (int): Availability ID

    Returns:

    schemas.Available: Availability details"""

    jwt_utils.verify_token(token)

    availability = available.get_availability_by_id(db, available_id)
    if not availability:
        raise HTTPException(status_code=404, detail="Availability not found")
    return availability


@router.get("/availability/get-by-user/{faculty_id}", response_model=List[response_schema.AvailableResponse])
def get_availability_by_user(faculty_id: str, db: Session = Depends(database.get_db),
                             token: str = Depends(jwt_utils.oauth2_scheme)) -> List[schemas.Available]:
    """Get availability by user

    Args:

        faculty_id (int): Faculty ID

    Returns:

        List[schemas.Available]: List of availabilities"""

    jwt_utils.verify_token(token)

    return available.get_availability_by_user(db, faculty_id)


# Get all availabilities


@router.get("/availabilities/", response_model=List[response_schema.AvailableResponse])
def get_all_availabilities(db: Session = Depends(database.get_db),
                           token: str = Depends(jwt_utils.oauth2_scheme)) -> List[schemas.Available]:
    """Get all availabilities

    Returns: 

        List[schemas.Available]: List of all availabilities"""

    jwt_utils.verify_token(token)

    return available.get_availabilities(db)

# Update availability by ID


@router.put("/availability/update/{available_id}", response_model=schemas.Available)
def update_availability(available_id: int, availability_update: schemas.AvailableUpdate,
                        db: Session = Depends(database.get_db),
                        token: str = Depends(jwt_utils.oauth2_scheme)) -> schemas.Available:
    """Update an availability by ID

    Args:

        available_id (int): Availability ID
        availability_update (schemas.AvailableUpdate): Updated availability details

    Returns:

        schemas.Available: Updated availability details"""

    jwt_utils.verify_token(token)

    return available.update_availability(db, available_id, availability_update)


@router.delete("/availability/delete/{available_id}", response_model=Optional[bool])
def delete_availability(available_id: int, db: Session = Depends(database.get_db),
                        token: str = Depends(jwt_utils.oauth2_scheme)) -> bool:
    """Delete an availability by ID

    Args:

            available_id (int): Availability ID 

    Returns:

        bool: True if availability was deleted, False otherwise"""

    jwt_utils.verify_token(token)

    deleted = available.delete_availability(db, available_id)
    if not deleted:
        raise HTTPException(
            status_code=404, detail="Availability not found or already deleted")
    return True
