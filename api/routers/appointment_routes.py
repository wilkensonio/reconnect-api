# Description: API routes for the application
import os
from .. import database
from  ..crud import crud_appointment
from ..schemas import available_schema as schemas
from ..schemas import response_schema
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from dotenv import load_dotenv

load_dotenv()
EXPRIRES_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")


router = APIRouter()


appointment_crud = crud_appointment.CrudAppointment()


@router.post("/appointment/create/", response_model=response_schema.CreateAppointmentResponse)
def create_appointment(appointment: schemas.CreateAppointment, db: Session = Depends(database.get_db)):
    """Create a new appointment 

    Args:

        appointment (schemas.CreateAppointment): appointment details 

    Returns:

       response_schema.CreateAppointmentResponse: appointment details"""

    return appointment_crud.appointment_create(db, appointment)


@router.get("/appointments/", response_model=List[response_schema.CreateAppointmentResponse])
def get_appointments(db: Session = Depends(database.get_db)):
    """Get all availabilities

    Args:

        None

    Returns:

        List[Available]: List of all availabilities"""

    try:
        return appointment_crud.get_appointments(db)

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=f"An error occurred while attempting to get appointments {
                e}"
        )


@router.get("/appointment/get-by-id/{appointment_id}", response_model=response_schema.GetAppointmentByIdResponse)
def get_appointment_by_id(appointment_id: int, db: Session = Depends(database.get_db)):
    """Get appointment by ID

    Args:

        available_id (int): Availability ID

    Returns:

    schemas.Available: Availability details"""

    appointment = appointment_crud.get_appointment_by_id(db, appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Availability not found")
    return appointment


@router.put("/appointment/update/{appointment_id}", response_model=response_schema.GetAppointmentByIdResponse)
def update_appointment(appointment_id: int, appointment_update: schemas.AppointmentUpdate,
                       db: Session = Depends(database.get_db)) -> response_schema.GetAppointmentByIdResponse:
    """Update an appointment by ID

    Args:

        appointment_id (int): id
        appointment_update (schemas.AppointmentUpdate): Updated appointment details

    Returns:

        schemas.GetAppointmentByIdResponse: Updated appointment details"""

    return appointment_crud.update_appointment(db, appointment_id, appointment_update)


@router.delete("/appointment/delete/{appointment_id}", response_model=Optional[bool])
def delete_update_appointment(appointment_id: int, db: Session = Depends(database.get_db)) -> bool:
    """Delete an appointment by ID

    Args:

        available_id (int): Availability ID 

    Returns:

        bool: True if appointment was deleted, False otherwise"""

    deleted = appointment_crud.delete_appointment(db, appointment_id)
    if not deleted:
        raise HTTPException(
            status_code=404, detail="Appointment not found or already deleted")
    elif deleted:
        return True
    raise HTTPException(
        status_code=500, detail="Internal server error. Please try again later.")
