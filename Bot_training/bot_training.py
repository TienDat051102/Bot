import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

def read_csv_file(file_path):
    """
    Đọc dữ liệu từ file CSV và xử lý cột ngày tháng.
    """
    data = pd.read_csv(file_path)

    # Chuyển đổi cột ngày 'DTYYYYMMDD' thành định dạng datetime
    data['Date'] = pd.to_datetime(data['<DTYYYYMMDD>'], format='%Y%m%d')

    # Đặt 'Date' làm index
    data.set_index('Date', inplace=True)

    # Lọc dữ liệu cần thiết (ví dụ, chỉ giữ lại cột 'Close' và mã cổ phiếu cụ thể)
    ticker = "AAV"  # Thay đổi theo mã chứng khoán bạn muốn phân tích
    filtered_data = data[data['<Ticker>'] == ticker][['<Close>']]
    filtered_data.rename(columns={'<Close>': 'Close'}, inplace=True)

    return filtered_data

def calculate_macd(data, short_window=12, long_window=26, signal_window=9):
    """
    Tính toán MACD và đường Signal.
    """
    data['EMA12'] = data['Close'].ewm(span=short_window, adjust=False).mean()
    data['EMA26'] = data['Close'].ewm(span=long_window, adjust=False).mean()
    data['MACD'] = data['EMA12'] - data['EMA26']
    data['Signal'] = data['MACD'].ewm(span=signal_window, adjust=False).mean()
    return data

def backtest_macd(data, initial_balance=10000, trade_size=0.1):
    """
    Mô phỏng giao dịch dựa trên chiến lược MACD và đánh dấu giá khi mua/bán.
    """
    balance = initial_balance
    position = 0  # Số lượng cổ phiếu đang nắm giữ
    buy_signals = []  # Lưu trữ thông tin điểm mua
    sell_signals = []  # Lưu trữ thông tin điểm bán

    for i in range(1, len(data)):
        # Chiến lược giao dịch dựa trên MACD
        if data['MACD'].iloc[i] > data['Signal'].iloc[i] and data['MACD'].iloc[i - 1] <= data['Signal'].iloc[i - 1]:
            # Tín hiệu mua
            if balance > 0:
                position = (balance * trade_size) / data['Close'].iloc[i]
                balance -= position * data['Close'].iloc[i]
                buy_signals.append((data.index[i], data['Close'].iloc[i]))
        elif data['MACD'].iloc[i] < data['Signal'].iloc[i] and data['MACD'].iloc[i - 1] >= data['Signal'].iloc[i - 1]:
            # Tín hiệu bán
            if position > 0:
                balance += position * data['Close'].iloc[i]
                sell_signals.append((data.index[i], data['Close'].iloc[i]))
                position = 0

    # Tính toán giá trị cuối cùng
    balance += position * data['Close'].iloc[-1]
    print(f"Số dư cuối: {balance}")
    
    return buy_signals, sell_signals, balance

def plot_macd(data, buy_signals, sell_signals):
    """
    Vẽ biểu đồ giá với các dấu hiệu mua/bán và hỗ trợ phóng to/thu nhỏ.
    """
    fig, ax = plt.subplots(figsize=(14, 7))

    # Vẽ biểu đồ giá đóng cửa
    ax.plot(data.index, data['Close'], label='Close Price', color='black', alpha=0.6)

    # Đánh dấu điểm mua
    if buy_signals:
        buy_dates, buy_prices = zip(*buy_signals)
        ax.scatter(buy_dates, buy_prices, marker='^', color='green', label='Buy Signal', alpha=1)

    # Đánh dấu điểm bán
    if sell_signals:
        sell_dates, sell_prices = zip(*sell_signals)
        ax.scatter(sell_dates, sell_prices, marker='v', color='red', label='Sell Signal', alpha=1)

    ax.set_title('MACD and Price with Buy/Sell Signals')
    ax.legend(loc='upper left')

    # Thêm các công cụ điều khiển zoom (sử dụng Slider)
    axcolor = 'lightgoldenrodyellow'
    ax_zoom = plt.axes([0.25, 0.01, 0.65, 0.03], facecolor=axcolor)
    zoom_slider = Slider(ax_zoom, 'Zoom', 1, 5, valinit=1, valstep=0.1)

    # Chức năng để điều chỉnh phạm vi hiển thị của biểu đồ khi phóng to/thu nhỏ
    def update(val):
        zoom_factor = zoom_slider.val
        # Đảm bảo chỉ mục không vượt quá độ dài dữ liệu
        end_index = int(len(data) / zoom_factor)
        end_index = min(end_index, len(data) - 1)  # Đảm bảo không vượt quá phạm vi
        ax.set_xlim([data.index[0], data.index[end_index]])  # Cập nhật phạm vi xlim
        ax.set_ylim([data['Close'].min(), data['Close'].max()])  # Cập nhật phạm vi ylim
        fig.canvas.draw_idle()

    zoom_slider.on_changed(update)

    plt.show()

def main():
    # Đường dẫn đến file CSV
    file_path = "./du_lieu/du_lieu_chung_khoan.csv"  # Thay bằng đường dẫn thực tế

    # Đọc dữ liệu từ file CSV
    data = read_csv_file(file_path)

    # Tính toán MACD
    data = calculate_macd(data)

    # Mô phỏng chiến lược và lấy các điểm mua/bán
    buy_signals, sell_signals, final_balance = backtest_macd(data)

    # Vẽ biểu đồ MACD và đánh dấu các điểm mua/bán
    plot_macd(data, buy_signals, sell_signals)

    print(f"Số dư ban đầu: 10,000 USD")
    print(f"Số dư cuối cùng: {final_balance:.2f} USD")

if __name__ == "__main__":
    main()
