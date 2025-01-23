
import pandas as pd
from sqlalchemy import create_engine

def load_to_sql(df, table_name, connection_string):
    """Tải dữ liệu vào cơ sở dữ liệu SQL"""
    engine = create_engine(connection_string)
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)
