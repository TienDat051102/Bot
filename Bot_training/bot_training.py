import pandas as pd
import matplotlib.pyplot as plt
from InquirerPy import inquirer

def read_csv_file(file_path):
    """
    Đọc dữ liệu từ file CSV và xử lý cột ngày tháng, đồng thời loại bỏ dấu '<' và '>' trong tên cột.
    """
    data = pd.read_csv(file_path)
    data.columns = data.columns.str.replace('<', '').str.replace('>', '')
    data['Date'] = pd.to_datetime(data['DTYYYYMMDD'], format='%Y%m%d')
    return data

def calculate_macd(data, short_window=12, long_window=26, signal_window=9):
    """
    Tính toán MACD và đường Signal.
    """
    data.loc[:, 'EMA12'] = data['Close'].ewm(span=short_window, adjust=False).mean()
    data.loc[:, 'EMA26'] = data['Close'].ewm(span=long_window, adjust=False).mean()
    data.loc[:, 'MACD'] = data['EMA12'] - data['EMA26']
    data.loc[:, 'Signal'] = data['MACD'].ewm(span=signal_window, adjust=False).mean()
    return data

def calculate_support_resistance(data, window=10):
    """
    Xác định các mức hỗ trợ và kháng cự dựa trên giá cao/thấp trong một khoảng thời gian.
    """
    support_levels = []
    resistance_levels = []

    for i in range(window, len(data) - window):
        # Kiểm tra xem giá thấp nhất trong khoảng có phải là hỗ trợ không
        if data['Low'].iloc[i] == data['Low'].iloc[i - window:i + window].min():
            support_levels.append((data['Date'].iloc[i], data['Low'].iloc[i]))

        # Kiểm tra xem giá cao nhất trong khoảng có phải là kháng cự không
        if data['High'].iloc[i] == data['High'].iloc[i - window:i + window].max():
            resistance_levels.append((data['Date'].iloc[i], data['High'].iloc[i]))

    return support_levels, resistance_levels

def plot_macd_for_ticker(data, ticker, buy_signals, sell_signals):
    """
    Vẽ biểu đồ cho một ticker cụ thể với các mức hỗ trợ/kháng cự.
    """
    buy_signals = buy_signals[buy_signals['Ticker'] == ticker]
    sell_signals = sell_signals[sell_signals['Ticker'] == ticker]
    filtered_data = data[data['Ticker'] == ticker]

    if filtered_data.empty:
        print(f"No data available for ticker: {ticker}")
        return

    filtered_data = calculate_macd(filtered_data)
    support_levels, resistance_levels = calculate_support_resistance(filtered_data)

    fig, ax = plt.subplots(figsize=(14, 7))
    ax.plot(filtered_data['Date'], filtered_data['Close'], label='Close Price', color='black', alpha=0.6)

    # Buy/Sell signals
    if not buy_signals.empty: 
        ax.scatter(buy_signals['Buy_Date'], buy_signals['Buy_Price'], marker='^', color='green', label='Buy Signal', alpha=1)

    if not sell_signals.empty:  
        ax.scatter(sell_signals['Sell_Date'], sell_signals['Sell_Price'], marker='v', color='red', label='Sell Signal', alpha=1)

    # Support/Resistance levels
    for date, price in support_levels:
        ax.axhline(price, linestyle='--', color='blue', alpha=0.6)

    for date, price in resistance_levels:
        ax.axhline(price, linestyle='--', color='orange', alpha=0.6)

    ax.set_title(f'MACD and Price with Buy/Sell Signals and Support/Resistance for {ticker}')
    ax.legend(loc='upper left')
    plt.show()

def get_buy_sell_signals(data):
    """
    Mô phỏng chiến lược và lấy các điểm mua/bán.
    """
    buy_signals = []  
    sell_signals = []  
    balance = 10000
    position = 0  
    trade_size = 0.1
    for i in range(1, len(data)):
        if data['MACD'].iloc[i] > data['Signal'].iloc[i] and data['MACD'].iloc[i - 1] <= data['Signal'].iloc[i - 1]:
            if balance > 0:
                position = (balance * trade_size) / data['Close'].iloc[i]
                balance -= position * data['Close'].iloc[i]
                buy_signals.append((data['Ticker'].iloc[i], data['Close'].iloc[i], data['Date'].iloc[i]))
        elif data['MACD'].iloc[i] < data['Signal'].iloc[i] and data['MACD'].iloc[i - 1] >= data['Signal'].iloc[i - 1]:
            if position > 0:
                balance += position * data['Close'].iloc[i]
                sell_signals.append((data['Ticker'].iloc[i], data['Close'].iloc[i], data['Date'].iloc[i]))
                position = 0
    buy_df = pd.DataFrame(buy_signals, columns=['Ticker', 'Buy_Price','Buy_Date'])
    sell_df = pd.DataFrame(sell_signals, columns=['Ticker', 'Sell_Price','Sell_Date'])
    return buy_df, sell_df

def main():
    file_path = "./du_lieu/du_lieu_chung_khoan.csv"  
    data = read_csv_file(file_path) 
    
    tickers = data['Ticker'].unique()
    data = calculate_macd(data)
    buy_df, sell_df = get_buy_sell_signals(data)
    

    selected_ticker = inquirer.select(
        message="Chọn mã chứng khoán:",
        choices=tickers.tolist()
    ).execute()

    plot_macd_for_ticker(data, selected_ticker, buy_df, sell_df)

if __name__ == "__main__":
    main()
