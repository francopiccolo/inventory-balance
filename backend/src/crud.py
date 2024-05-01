from sqlalchemy.orm import Session
from sqlalchemy import func 

from . import models

def get_items(db: Session):
    return db.query(models.Transaction.item_id).distinct()

def get_item_transactions(db: Session, item_id: int):
    return db.query(models.Transaction).filter(models.Transaction.item_id == item_id).all()