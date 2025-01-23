import requests
import pandas as pd

def extract_from_api(api_url):
    """Lấy dữ liệu từ API"""
    response = requests.get(api_url)
    data = response.json()
    df = pd.DataFrame(data)
    return df

def extract_from_db(connection_string, query):
    """Lấy dữ liệu từ cơ sở dữ liệu"""
    import sqlalchemy
    engine = sqlalchemy.create_engine(connection_string)
    df = pd.read_sql(query, engine)
    return df
