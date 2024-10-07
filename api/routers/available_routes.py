# Description: API routes for the application
import os
from .. import crud_available, database
from ..schemas import available_schema as schemas
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
def create_availability(availability: schemas.CreateAvailability, db: Session = Depends(database.get_db)) -> schemas.Available:
    """Add a new availability: Enter day and time available

    Args:

        availability (schemas.CreateAvailability): Availability details 

    Returns:

        schemas.Available: Availability details"""

    return available.create_availability(db, availability)

# Get availability by ID


@router.get("/availability/get-by-id/{available_id}", response_model=schemas.Available)
def get_availability_by_id(available_id: int, db: Session = Depends(database.get_db)):
    """Get availability by ID

    Args:

        available_id (int): Availability ID

    Returns:

    schemas.Available: Availability details"""

    availability = available.get_availability_by_id(db, available_id)
    if not availability:
        raise HTTPException(status_code=404, detail="Availability not found")
    return availability

# Get all availabilities


@router.get("/availabilities/", response_model=List[schemas.Available])
def get_all_availabilities(db: Session = Depends(database.get_db)) -> List[schemas.Available]:
    """Get all availabilities

    Returns: 

        List[schemas.Available]: List of all availabilities"""

    return available.get_availabilities(db)

# Update availability by ID


@router.put("/availability/update/{available_id}", response_model=schemas.Available)
def update_availability(available_id: int, availability_update: schemas.AvailableUpdate,
                        db: Session = Depends(database.get_db)) -> schemas.Available:
    """Update an availability by ID

    Args:

        available_id (int): Availability ID
        availability_update (schemas.AvailableUpdate): Updated availability details

    Returns:

        schemas.Available: Updated availability details"""
    return available.update_availability(db, available_id, availability_update)


@router.delete("/availability/delete/{available_id}", response_model=Optional[bool])
def delete_availability(available_id: int, db: Session = Depends(database.get_db)) -> bool:
    """Delete an availability by ID

    Args:

            available_id (int): Availability ID 

    Returns:

        bool: True if availability was deleted, False otherwise"""

    deleted = available.delete_availability(db, available_id)
    if not deleted:
        raise HTTPException(
            status_code=404, detail="Availability not found or already deleted")
    return True
