# connect_to_db.py
import psycopg2
import pandas as pd
from config import get_db_config


db_config = get_db_config()


conn = psycopg2.connect(
    host=db_config['host'],
    database=db_config['database'],
    user=db_config['user'],
    password=db_config['password']
)

query = "SELECT ticker, date, open, close, volume FROM stock_data;"
df = pd.read_sql(query, conn)

conn.close()

print(df.head())
