from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud import create_item, get_items, get_item, update_item, delete_item
from app.schemas import ItemCreate, ItemUpdate

router = APIRouter(prefix="/items", tags=["items"])

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ItemCreate)
def create_item_route(item: ItemCreate, db: Session = Depends(get_db)):
    return create_item(db, item)

@router.get("/", response_model=list[Item])
def read_items(db: Session = Depends(get_db)):
    return get_items(db)

@router.get("/{item_id}", response_model=Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = get_item(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@router.put("/{item_id}", response_model=Item)
def update_item_route(item_id: int, item: ItemUpdate, db: Session = Depends(get_db)):
    db_item = update_item(db, item_id, item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@router.delete("/{item_id}", response_model=Item)
def delete_item_route(item_id: int, db: Session = Depends(get_db)):
    db_item = delete_item(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item
