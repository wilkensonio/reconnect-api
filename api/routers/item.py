from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, database
from ..schemas import item_schema

router = APIRouter()


@router.post("/items/", response_model=item_schema.Item)
def create_item(item: item_schema.ItemCreate, db: Session = Depends(database.get_db)):
    return crud.create_item(db=db, item=item)


@router.get("/items/", response_model=list[item_schema.Item])
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    return crud.get_items(db=db, skip=skip, limit=limit)
