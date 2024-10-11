import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.database import Base, get_db
from api.utils import validate_api_key
from api.crud import crud_user
from fastapi.testclient import TestClient
from api.main import app
from unittest.mock import MagicMock

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"


def fake_validate_api_key():
    return True


engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={
                       "check_same_thread": False})
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[validate_api_key.validate_api_key] = fake_validate_api_key


@pytest.fixture(scope="module")
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)
    #
