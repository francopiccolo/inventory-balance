
import polars as pl
from datetime import timedelta

def calculate_stock(transactions):
    df = pl.DataFrame(transactions)
    min_date = df.select(pl.min('date')).item()
    max_date = df.select(pl.max('date')).item()
    date_range = pl.date_range(min_date, max_date, timedelta(days=1), eager=True).alias('date_range')
    df = df.join(pl.DataFrame(date_range), how='cross').\
        filter(pl.col('date_range') >= pl.col('date')).\
        group_by('date_range').agg(pl.col('quantity').sum()).\
        rename({'date_range': 'date', 'quantity': 'stock'})
    return df.to_dicts()