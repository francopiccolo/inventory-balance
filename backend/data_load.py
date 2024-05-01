import polars as pl

df = pl.read_csv('./data/test-project-data.csv', null_values='NULL')

df = df.cast({
    'item_id': pl.UInt32, 
    'quantity': pl.Int32
})

df = df.with_columns(
   pl.col('date_production_start').str.to_date('%Y-%m-%d %H:%M:%S'),
   pl.col('date_received_into_inventory').str.to_date('%Y-%m-%d %H:%M:%S'),
   pl.col('date_shipped_from_inventory').str.to_date('%Y-%m-%d %H:%M:%S')
)

# We filter the two possible valid cases
# quantity > 0, date_received_into_inventory >= date_production_start and date_shipped_from_inventory null
# quantity < 0, date_production_start null, date_received_into_inventory null and date_shipped_from_inventory not null
df = df.filter(
    ((pl.col('quantity') > 0) & (pl.col('date_received_into_inventory') >= pl.col('date_production_start')) & (pl.col('date_shipped_from_inventory').is_null()))
    |
    ((pl.col('quantity') < 0) & (pl.col('date_production_start').is_null()) & (pl.col('date_received_into_inventory').is_null()) & (pl.col('date_shipped_from_inventory').is_not_null()))
)

# We transform date received inventory and date shipped to a single field date
df = df.with_columns(
    pl.when(pl.col('quantity') > 1).then(pl.col('date_received_into_inventory'))
    .when(pl.col('quantity') < 0).then(pl.col('date_shipped_from_inventory'))
    .alias('date')
)

df = df.drop(['date_received_into_inventory', 'date_shipped_from_inventory', 'date_production_start'])

df = df.with_row_index('id')

df.write_database('transactions', 'postgresql://localhost/inventory_balance')