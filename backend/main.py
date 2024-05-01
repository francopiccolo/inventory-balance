from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from src import crud, schemas
from src.calculate_stock import calculate_stock
from src.database import SessionLocal

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/items", response_model=list[schemas.Item])
def get_items(db: Session=Depends(get_db)):
    items = crud.get_items(db)
    return items

@app.get('/daily_stock/{item_id}', response_model=list[schemas.DailyStock])
def get_item_transactions(item_id: int, db: Session=Depends(get_db)):
    transactions = crud.get_item_transactions(db, item_id)
    transactions = [
        {'transaction_id': transaction.id,
         'date': transaction.date,
         'quantity': transaction.quantity}
        for transaction in transactions
    ]
    daily_stock = calculate_stock(transactions)
    return daily_stock