from ..schemas import available_schema
from .. import models
from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import Optional


class CrudAppointment:
    """Appointment crud operations"""

    def appointment_create(db: Session, appointment: available_schema.CreateAppointment) -> models.Appointment:
        """Create a new appointment

        Args:
            db (Session): Database session
            appointment (faculty_schema.AppointmentCreate): Appointment details

        return: user_schema.AppointmentResponse: Appointment details"""

        try:
            new_appointment = models.Appointment(**appointment.model_dump())
            db.add(new_appointment)
            db.commit()
            db.refresh(new_appointment)
            return new_appointment

        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"An error occurred while attempting to create appointment {
                    e}"
            )

    @staticmethod
    def appointment_create(db: Session, appointment: available_schema.CreateAppointment) -> models.Appointment:
        """Create a new appointment

        Args:
            db (Session): Database session
            appointment (faculty_schema.AppointmentCreate): Appointment details

        return: user_schema.AppointmentResponse: Appointment details"""

        try:
            new_appointment = models.Appointment(**appointment.model_dump())
            db.add(new_appointment)
            db.commit()
            db.refresh(new_appointment)
            return new_appointment

        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"An error occurred while attempting to create appointment {
                    e}"
            )

    @staticmethod
    def get_appointment_by_id(db: Session, appointment_id: int) -> Optional[models.Appointment]:
        """Get a appointment by id

        Args:
            db (Session): Database session
            appointment_id (int): Appointment id

        Returns:
            Appointment: Appointment details"""

        existing_appointment = db.query(models.Appointment).filter(
            models.Appointment.id == appointment_id).first()

        return existing_appointment

    @staticmethod
    def get_appointments_by_user(db: Session, faculty_id: Optional[str], student_id: Optional[str]) -> Optional[models.Appointment]:
        """Get a appointment by faculty hootloot id

        Args:

            db (Session): Database session
            faculty_id Optional[str]: Faculty id
            student_id Optional[str]: Student id

        Returns:

            Appointment: Appointment details"""

        if faculty_id:
            existing_appointment = db.query(models.Appointment).filter(
                models.Appointment.faculty_id == faculty_id).all()
        else:
            existing_appointment = db.query(models.Appointment).filter(
                models.Appointment.student_id == student_id).all()

        return existing_appointment

    @staticmethod
    def get_appointments(db: Session) -> list[models.Appointment]:
        """Get all appointments

        Args:
            db (Session): Database session

        Returns:
            List[Appointment]: List of all appointments"""

        return db.query(models.Appointment).all()

    @staticmethod
    def get_appointments_by_user(db: Session, user_id: int) -> list[models.Appointment]:
        """Get all appointments by user

        Args:
            db (Session): Database session
            user_id (int): User id

        Returns:
            List[Appointment]: List of all appointments by user (faculty or student)"""

        faculty_app = db.query(models.Appointment).filter(
            models.Appointment.faculty_id == user_id).all()
        if faculty_app:
            return faculty_app
        return db.query(models.Appointment).filter(models.Appointment.student_id == user_id).all()

    @staticmethod
    def update_appointment(db: Session, appointment_id: int, appointment_update: available_schema.AppointmentUpdate) -> models.Appointment:
        """Update an appointment by ID

        Args:
            appointment_id (int): Appointment ID
            appointment_update (schemas.AppointmentUpdate): Updated appointment details

        Returns:

            schemas.Appointment: Updated appointment details"""
        appointment = db.query(models.Appointment).filter(
            models.Appointment.id == appointment_id).first()
        if not appointment:
            raise HTTPException(
                status_code=404, detail="Appointment not found")
        for key, value in appointment_update.model_dump().items():
            setattr(appointment, key, value)
        db.commit()
        db.refresh(appointment)
        return appointment

    @staticmethod
    def delete_appointment(db: Session, appointment_id: int) -> bool:
        """Delete an appointment by ID

        Args:
            appointment_id (int): Appointment ID

        Returns:

            bool: True if appointment was deleted, False otherwise"""
        appointment = db.query(models.Appointment).filter(
            models.Appointment.id == appointment_id).first()
        if not appointment:
            return False
        db.delete(appointment)
        db.commit()
        return True

    @staticmethod
    def student_checkin(id: int, db: Session):
        """Get  appointment by ID

        Args: 

            id: int appointment ID

        Returns:
            None if appointment not found, Appointment details otherwise"""

        appointments = db.query(models.Appointment).filter(
            models.Appointment.id == id).first()

        return None if not appointments else appointments
