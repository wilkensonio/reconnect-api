

import logging
from .. import database
from ..crud import crud_appointment
from ..schemas import available_schema as schemas
from ..schemas import response_schema
from ..utils import jwt_utils, sms_utils
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from ..routers.ws_routes import create_notification_route as ws_create_notification
from ..schemas.notification_schema import NotificationSchema
from datetime import datetime

router = APIRouter()


appointment_crud = crud_appointment.CrudAppointment()


@router.post("/appointment/create/", response_model=response_schema.CreateAppointmentResponse)
async def create_appointment(appointment: schemas.CreateAppointment, db: Session = Depends(database.get_db),
                             token: str = Depends(jwt_utils.oauth2_scheme)) -> response_schema.CreateAppointmentResponse:
    """Create a new appointment

    Args:

        appointment (schemas.CreateAppointment): appointment details
        date format: YYYY-MM-DD
        time format: 12:00

    Returns:

       response_schema.CreateAppointmentResponse: appointment details"""

    jwt_utils.verify_token(token)

    created_appt = appointment_crud.appointment_create(db, appointment)
    user_id = appointment.faculty_id

    formated_date = datetime.strptime(
        appointment.date, "%Y-%m-%d").strftime("%B %d, %Y")

    msg_notification = f"New appointment scheduled from"
    msg_notification += f" {appointment.start_time}"
    msg_notification += f" to {appointment.end_time}"
    msg_notification += f" on {formated_date}"

    notification_data = NotificationSchema(
        user_id=user_id,
        event_type="appointment_scheduled",
        message=msg_notification
    )

    try:
        await ws_create_notification(user_id, notification_data, db)
    except Exception as e:
        logging.error("Error sending notification", e)
    try:
        await sms_utils.send_sms(message=msg_notification)
    except Exception as e:
        logging.error("Error sending sms", e)

    return created_appt


@router.get("/appointments/", response_model=List[response_schema.CreateAppointmentResponse])
def get_appointments(db: Session = Depends(database.get_db),
                     token: str = Depends(jwt_utils.oauth2_scheme)) -> List[response_schema.CreateAppointmentResponse]:
    """Get all availabilities

    Args:

        None

    Returns:

        List[Available]: List of all availabilities"""

    jwt_utils.verify_token(token)

    try:
        return appointment_crud.get_appointments(db)

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=f"An error occurred while attempting to get appointments {
                e}"
        )


@router.get("/appointments/get-by-user/{user_id}",
            response_model=List[response_schema.CreateAppointmentResponse])
def get_appointments_by_user(user_id: str, db: Session = Depends(database.get_db),
                             token: str = Depends(jwt_utils.oauth2_scheme)
                             ) -> List[response_schema.CreateAppointmentResponse]:
    """Get all appointments by user

    Args:

        faculty_id Optional[str]: User ID, the hootloot ID
        student_id Optional[str]: User ID, the hootloot ID  

    Returns:

        List[Appointment]: List of all appointments by user"""

    jwt_utils.verify_token(token)

    try:
        return appointment_crud.get_appointments_by_user(db, user_id)

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"An error occurred while attempting to get appointments {
                e}"
        )


@router.get("/appointment/get-by-id/{appointment_id}",
            response_model=response_schema.GetAppointmentByIdResponse)
def get_appointment_by_id(appointment_id: int, db: Session = Depends(database.get_db),
                          token: str = Depends(jwt_utils.oauth2_scheme)) -> response_schema.GetAppointmentByIdResponse:
    """Get appointment by ID

    Args:

        available_id (int): Availability ID

    Returns:

    schemas.Available: Availability details"""

    jwt_utils.verify_token(token)

    appointment = appointment_crud.get_appointment_by_id(db, appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Availability not found")
    return appointment


@router.put("/appointment/update/{appointment_id}",
            response_model=response_schema.GetAppointmentByIdResponse)
async def update_appointment(appointment_id: int,
                             appointment_update: schemas.AppointmentUpdate,
                             db: Session = Depends(database.get_db),
                             token: str = Depends(jwt_utils.oauth2_scheme)) -> response_schema.GetAppointmentByIdResponse:
    """Update an appointment by ID

    Args:

        appointment_id (int): id
        appointment_update (schemas.AppointmentUpdate): Updated appointment details

    Returns:

        schemas.GetAppointmentByIdResponse: Updated appointment details"""

    jwt_utils.verify_token(token)

    update_appt = appointment_crud.update_appointment(
        db, appointment_id, appointment_update)

    user_id = appointment_update.faculty_id

    formated_date = datetime.strptime(
        appointment_update.date, "%Y-%m-%d").strftime("%B %d, %Y")

    msg_notification = f"Appt updated, New appt from"
    msg_notification += f" {appointment_update.start_time}"
    msg_notification += f" to {appointment_update.end_time}"
    msg_notification += f" on {formated_date}"

    notification_data = NotificationSchema(
        user_id=appointment_update.faculty_id,
        event_type="appointment_updated",
        message=msg_notification
    )
    try:
        await ws_create_notification(user_id, notification_data, db)
    except Exception as e:
        print("Error sending notification", e)
    try:
        await sms_utils.send_sms(message=msg_notification)
    except Exception as e:
        logging.error("Error sending sms", e)

    return update_appt


@router.delete("/appointment/delete/{appointment_id}", response_model=Optional[bool])
async def delete_update_appointment(appointment_id: int, db: Session = Depends(database.get_db),
                                    token: str = Depends(jwt_utils.oauth2_scheme)) -> bool:
    """Delete an appointment by ID

    Args:

        available_id (int): Availability ID 

    Returns:

        bool: True if appointment was deleted, False otherwise"""

    jwt_utils.verify_token(token)

    appointment_delete = appointment_crud.get_appointment_by_id(
        db, appointment_id)

    deleted = appointment_crud.delete_appointment(db, appointment_id)

    formated_date = datetime.strptime(
        appointment_delete.date, "%Y-%m-%d").strftime("%B %d, %Y")

    msg_notification = f"Your {appointment_delete.start_time}"
    msg_notification += f" appointment"
    msg_notification += f" on {formated_date}"
    msg_notification += f" has been canceled"

    notification_data = NotificationSchema(
        user_id=appointment_delete.faculty_id,
        event_type="appointment_canceled",
        message=msg_notification
    )

    if not deleted:
        raise HTTPException(
            status_code=404, detail="Appointment not found or already deleted")
    try:
        await ws_create_notification(appointment_delete.faculty_id,
                                     notification_data, db)
    except Exception as e:
        logging.error("Error sending notification", e)
    try:
        await sms_utils.send_sms(message=msg_notification)
    except Exception as e:
        logging.error("Error sending sms", e)

    return deleted
