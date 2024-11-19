from pydantic import BaseModel
from typing import Optional

class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int

class Item(ItemBase):
    id: int  # Assuming `id` as the primary key in the database model

    class Config:
        orm_mode = True  # Allows Pydantic models to serialize SQLAlchemy ORM instances

class ItemCreate(ItemBase):
    pass

class ItemUpdate(ItemBase): 
    pass
