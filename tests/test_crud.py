from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.database import Base, SessionLocal
from api import crud, models
from api.schemas import item_schema

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


def test_create_item():
    # Create tables
    Base.metadata.create_all(bind=engine)

    # Setup test session
    db = TestingSessionLocal()
    item_in = item_schema.ItemCreate(
        name="Test Item", description="Test Description")
    item = crud.create_item(db=db, item=item_in)

    assert item.name == "Test Item"
    assert item.description == "Test Description"

    # Clean up
    Base.metadata.drop_all(bind=engine)
