from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from uuid import uuid4

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from config import settings

DATABASE_URL = settings.DATABASE_URL
engine = create_engine(DATABASE_URL)

# Call declarative_base to create Base class
Base = declarative_base()

app = FastAPI()

inventory_db = {}

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int

class ItemResponse(Item):
    id: str

@app.post("/items/", response_model=ItemResponse)
async def create_item(item: Item):
    item_id = str(uuid4())
    inventory_db[item_id] = item
    return {**item.dict(), "id": item_id}

@app.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: str):
    item = inventory_db.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {**item.dict(), "id": item_id}

@app.put("/items/{item_id}", response_model=ItemResponse)
async def update_item(item_id: str, item: Item):
    if item_id not in inventory_db:
        raise HTTPException(status_code=404, detail="Item not found")
    inventory_db[item_id] = item
    return {**item.dict(), "id": item_id}

@app.delete("/items/{item_id}")
async def delete_item(item_id: str):
    if item_id not in inventory_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del inventory_db[item_id]
    return {"message": "Item deleted successfully"}

@app.get("/items/", response_model=List[ItemResponse])
async def get_inventory():
    items = [{**item.dict(), "id": item_id} for item_id, item in inventory_db.items()]
    return items
