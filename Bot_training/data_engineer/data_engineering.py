from src.extraction import extract_data
from src.transformation import preprocess_data
from src.loading import load_data
from src.utils import plot_stock_data

def run_pipeline():
    # Extract data
    df = extract_data.extract_data()
    
    # Transform data
    df_cleaned = preprocess_data.preprocess_data(df)
    
    # Load data to DB
    load_data.load_data(df_cleaned)
    
    # Plot data
    plot_stock_data(df_cleaned)

if __name__ == '__main__':
    run_pipeline()
