import pandas as pd

def clean_data(df):
    """Xử lý missing values, dữ liệu lỗi"""
    df.dropna(inplace=True)
    df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d')
    return df

def aggregate_data(df):
    """Tính toán các thống kê cơ bản như tổng, trung bình, v.v."""
    df_agg = df.groupby('Ticker').agg({'Close': 'mean', 'Volume': 'sum'}).reset_index()
    return df_agg
