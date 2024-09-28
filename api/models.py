import bcrypt
from sqlalchemy import Column, Integer, String
from api.database import Base
from datetime import datetime
from passlib.context import CryptContext


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
