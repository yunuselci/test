from binance.client import Client
from datetime import datetime
import talib
import numpy as np

def calculate_bands(close_array, length=20, stddev=2):
    # Calculate the upper, middle and lower Bollinger Bands
    upper, middle, lower = talib.BBANDS(close_array, timeperiod=length, nbdevup=stddev, nbdevdn=stddev, matype=0)
    return upper, middle, lower

def check_signal():
    # Get the last 100 candles from Binance
    candles = client.get_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_1MINUTE, limit=100)
    close_array = np.array([float(candle[4]) for candle in candles])
    upper, middle, lower = calculate_bands(close_array)

    # Check for signals
    if close_array[-1] > upper[-1]:
        return 'sell'
    elif close_array[-1] < lower[-1]:
        return 'buy'
    else:
        return None

def make_trade(signal):
    if signal == 'buy':
        ## Place your BUY order here
        client.order_market_buy(symbol='BTCUSDT', quantity=0.01)
    elif signal == 'sell':
        ## Place your SELL order here
        client.order_market_sell(symbol='BTCUSDT', quantity=0.01)

# Your Binance API keys
api_key = 'YOUR_API_KEY'
api_secret_key = 'YOUR_SECRET_API_KEY'

# Initialize Binance client
client = Client(api_key, api_secret_key)

# Main Bot Loop
while True:
    signal = check_signal()
    make_trade(signal)
