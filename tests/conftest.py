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


@pytest.fixture
def mock_secret_key(mocker):
    """Mock the database query to return a valid secret key."""
    mock_secret_entry = MagicMock()
    mock_secret_entry.api_secret_key = "478f053bfdaa7699a6ba4c0f236b75a54793b6317d41aeb0c5797a00c221af8b"

    # Mock the query method on the Secret model
    mock_query = mocker.patch('sqlalchemy.orm.Session.query')
    mock_query.return_value.filter.return_value.all.return_value = mock_secret_entry
