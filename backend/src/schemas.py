from datetime import date

from pydantic import BaseModel

class Transaction(BaseModel):
    id: int
    item_id: int
    date: date
    quantity: int

class Item(BaseModel):
    item_id: int

class DailyStock(BaseModel):
    date: date
    stock: int