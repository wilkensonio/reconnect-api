import bcrypt
import os
from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String, ForeignKey
from api.database import Base
from datetime import datetime
from passlib.context import CryptContext


load_dotenv()


class User(Base):
    """User model

    Methods:
        hash_password: Hashes the user's password
        check_password: Verifies the user's password
    """
    __tablename__ = "faculty"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(255), nullable=False, unique=True)  # school id
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), index=True, nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    phone_number = Column(String(50), index=True, unique=True)  # cell phone
    created_at = Column(
        String(255), default=lambda: datetime.now().strftime("%B %d, %Y"))

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: str) -> None:
        self.password = self.pwd_context.hash(password)

    def check_password(self, password: str) -> bool:
        return self.pwd_context.verify(password, self.password)


class Student(Base):
    """Student model"""

    __tablename__ = "student"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(String(255), nullable=False, unique=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), index=True, nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    phone_number = Column(String(50), index=True, unique=True, nullable=True)
    user_id = Column(String(255), ForeignKey('faculty.user_id'))
    created_at = Column(
        String(255), default=lambda: datetime.now().strftime("%B %d, %Y"))


class Persmission(Base):
    """Permission model"""

    __tablename__ = "permission"

    id = Column(Integer, primary_key=True, autoincrement=True)
    permission_type = Column(String(255), nullable=False,
                             unique=True, default="user")
    user_id = Column(String(255), ForeignKey('faculty.user_id'))
    created_at = Column(
        String(255), default=lambda: datetime.now().strftime("%B %d, %Y"))


class Admin(Base):
    """Admin model"""

    __tablename__ = "admin"

    id = Column(Integer, primary_key=True, autoincrement=True)
    admin_id = Column(String(255), nullable=False,
                      unique=True, default="00000000")
    first_name = Column(String(255), nullable=False, default="Root")
    last_name = Column(String(255), nullable=False, default="Admin")
    email = Column(String(255), index=True, nullable=False,
                   unique=True)
    password = Column(String(255), nullable=False)
    phone_number = Column(String(50), index=True, unique=True, nullable=True)
    created_at = Column(
        String(255), default=lambda: datetime.now().strftime("%B %d, %Y"))

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def _hash_password(self, password: str) -> None:
        self.password = self.pwd_context.hash(password)

    def __int__(self):
        self.password = self._hash_password(os.getenv('ADMIN_PASSWORD'))
        self.email = os.getenv('ADMIN_EMAIL')


class Log(Base):
    """Log model"""

    __tablename__ = "log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    action = Column(String(255), nullable=False)
    user_id = Column(String(255), ForeignKey('faculty.user_id'))
    Student_id = Column(String(255), ForeignKey('student.student_id'))
    created_at = Column(
        String(255), default=lambda: datetime.now().strftime("%B %d, %Y"))


class Note(Base):
    """Notes model"""

    __tablename__ = "note"

    id = Column(Integer, primary_key=True, autoincrement=True)
    notes = Column(String(255), nullable=False)
    user_id = Column(String(255), ForeignKey('faculty.user_id'))
    Student_id = Column(String(255), ForeignKey('student.student_id'))
    created_at = Column(
        String(255), default=lambda: datetime.now().strftime("%B %d, %Y"))


class Backlsit(Base):
    """Blacklist model"""

    __tablename__ = "blacklist"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(255), nullable=False)
    created_at = Column(
        String(255), default=lambda: datetime.now().strftime("%B %d, %Y"))


class Available(Base):
    """Available model"""

    __tablename__ = "available"

    id = Column(Integer, primary_key=True, autoincrement=True)
    day = Column(String(15), nullable=False)
    start_time = Column(String(15), nullable=False)
    end_time = Column(String(15), nullable=False)
    user_id = Column((String(255)), ForeignKey('faculty.user_id'))
    created_at = Column(
        String(50), default=lambda: datetime.now().strftime("%B %d, %Y"))


class Appointment(Base):
    """Appointment model"""

    __tablename__ = "appointment"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(String(50), nullable=False)
    start_time = Column(String(15), nullable=False)
    end_time = Column(String(15), nullable=False)
    satus = Column(String(50), nullable=False, default="pending")
    student_id = Column(String(255), ForeignKey('student.student_id'))
    faculty_id = Column(String(255), ForeignKey('faculty.user_id'))
    updated_at = Column(
        String(50), default=lambda: datetime.now().strftime("%B %d, %Y"))
    created_at = Column(
        String(50), default=lambda: datetime.now().strftime("%B %d, %Y"))
