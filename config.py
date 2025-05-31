# FILE_VERSION_START
# Project: CryptoAndStocksIndicators
# File: config.py
# Version: 0.2.0
# Date: 2024-03-21
# Author: [Your Name/Nickname]
# Description: Configuration file for tickers, columns, and default parameters.
# FILE_VERSION_END

# List of assets (can be expanded) - Ticker and TradingViewSymbol might be fetched dynamically later
# For now, this helps structure the fictional data
ASSET_LIST_FICTIONAL_BASE = [
    # Crypto
    {'Asset Type': 'Crypto', 'Crypto Rank': 1, 'Market Cap': 1.35e12, 'Asset Name': 'Bitcoin', 'Ticker': 'BTC', 'TradingViewSymbol': 'BTCUSD', 'Current Price ($)': 68500.50, 'Var. 1H (%)': 0.8, 'Var. 12H (%)': 2.0, 'Var. 24H (%)': 1.5, 'Var. 1W (%)': 3.0,
        'AI Signal': 'Buy', 'MA Cross': 'Wait', 'RSI Div.': 'None', 'MACD Div.': 'None', 'Vol. Breakout': 'No Break', 'OBV Signal': 'Buy', 'ATR Signal': 'Buy',
        'RSI (14)': 'Buy', 'StochRSI %K': 'Wait', 'MACD Signal': 'Buy', 'Stoch %K': 'Wait', 'Awesome Osc.': 'Buy', 'ADX (14)': 'Strong (40)', 'BBands Pos.': 'Mid',
        'EMA (20) vs Price': 'Buy', 'SMA (50/200)': 'Buy', 'VWAP vs Price': 'Buy'},
    {'Asset Type': 'Crypto', 'Crypto Rank': 2, 'Market Cap': 4.50e11, 'Asset Name': 'Ethereum', 'Ticker': 'ETH', 'TradingViewSymbol': 'ETHUSD', 'Current Price ($)': 3750.00, 'Var. 1H (%)': -0.3, 'Var. 12H (%)': 1.0, 'Var. 24H (%)': 0.8, 'Var. 1W (%)': 2.5,
        'AI Signal': 'Buy', 'MA Cross': 'Golden Cross (Buy)', 'RSI Div.': 'Bullish Div. (Buy)', 'MACD Div.': 'None', 'Vol. Breakout': 'No Break','OBV Signal': 'Wait', 'ATR Signal': 'Wait',
        'RSI (14)': 'Wait', 'StochRSI %K': 'Buy', 'MACD Signal': 'Buy', 'Stoch %K': 'Buy', 'Awesome Osc.': 'Buy','ADX (14)': 'Trend (30)', 'BBands Pos.': 'Upper',
        'EMA (20) vs Price': 'Buy', 'SMA (50/200)': 'Buy', 'VWAP vs Price': 'Buy'},
    # Stocks & ETFs
    {'Asset Type': 'Stock', 'Crypto Rank': None, 'Market Cap': 3.12e12, 'Asset Name': 'Microsoft Corp.', 'Ticker': 'MSFT', 'TradingViewSymbol': 'NASDAQ:MSFT', 'Current Price ($)': 420.55, 'Var. 1H (%)': 0.1, 'Var. 12H (%)': 0.5, 'Var. 24H (%)': 0.2, 'Var. 1W (%)': 1.5,
        'AI Signal': '🔥 Strong Buy', 'MA Cross': 'Golden Cross (Buy)', 'RSI Div.': 'None', 'MACD Div.': 'None', 'Vol. Breakout': 'Bullish Break (Buy)', 'OBV Signal': 'Buy', 'ATR Signal': 'Buy',
        'RSI (14)': 'Wait', 'StochRSI %K': 'Buy', 'MACD Signal': 'Buy', 'Stoch %K': 'Wait', 'Awesome Osc.': 'Buy', 'ADX (14)': 'Trend (28)', 'BBands Pos.': 'Mid',
        'EMA (20) vs Price': 'Buy', 'SMA (50/200)': 'Buy', 'VWAP vs Price': 'Buy'},
    {'Asset Type': 'Stock', 'Crypto Rank': None, 'Market Cap': 2.63e12, 'Asset Name': 'Apple Inc.', 'Ticker': 'AAPL', 'TradingViewSymbol': 'NASDAQ:AAPL', 'Current Price ($)': 170.34, 'Var. 1H (%)': -0.2, 'Var. 12H (%)': -0.8, 'Var. 24H (%)': -0.5, 'Var. 1W (%)': -2.0,
        'AI Signal': 'Sell', 'MA Cross': 'Wait', 'RSI Div.': 'Bearish Div. (Sell)', 'MACD Div.': 'Bearish Div. (Sell)', 'Vol. Breakout': 'No Break', 'OBV Signal': 'Sell', 'ATR Signal': 'Sell',
        'RSI (14)': 'FICTIONAL_AAPL_RSI', 'StochRSI %K': 'Sell', 'MACD Signal': 'Sell', 'Stoch %K': 'Sell', 'Awesome Osc.': 'Sell', 'ADX (14)': 'Weak (18)', 'BBands Pos.': 'Upper',
        'EMA (20) vs Price': 'Sell', 'SMA (50/200)': 'Wait', 'VWAP vs Price': 'Sell'},
    {'Asset Type': 'Stock', 'Crypto Rank': None, 'Market Cap': 2.20e12, 'Asset Name': 'NVIDIA Corp.', 'Ticker': 'NVDA', 'TradingViewSymbol': 'NASDAQ:NVDA', 'Current Price ($)': 880.27, 'Var. 1H (%)': 0.5, 'Var. 12H (%)': 1.2, 'Var. 24H (%)': 2.1, 'Var. 1W (%)': 5.3,
        'AI Signal': '🔥 Strong Buy', 'MA Cross': 'Golden Cross (Buy)', 'RSI Div.': 'None', 'MACD Div.': 'Bullish Div. (Buy)', 'Vol. Breakout': 'Bullish Break (Buy)', 'OBV Signal': 'Buy', 'ATR Signal': 'Buy',
        'RSI (14)': 'Buy', 'StochRSI %K': 'Buy', 'MACD Signal': 'Buy', 'Stoch %K': 'Buy', 'Awesome Osc.': 'Buy', 'ADX (14)': 'Strong (35)', 'BBands Pos.': 'Upper',
        'EMA (20) vs Price': 'Buy', 'SMA (50/200)': 'Buy', 'VWAP vs Price': 'Buy'},
    {'Asset Type': 'Stock', 'Crypto Rank': None, 'Market Cap': 1.82e12, 'Asset Name': 'Amazon.com Inc.', 'Ticker': 'AMZN', 'TradingViewSymbol': 'NASDAQ:AMZN', 'Current Price ($)': 175.80, 'Var. 1H (%)': 0.0, 'Var. 12H (%)': -0.5, 'Var. 24H (%)': -1.0, 'Var. 1W (%)': -1.2,
        'AI Signal': 'Strong Sell', 'MA Cross': 'Death Cross (Sell)', 'RSI Div.': 'None', 'MACD Div.': 'None', 'Vol. Breakout': 'Bearish Break (Sell)', 'OBV Signal': 'Sell', 'ATR Signal': 'Sell',
        'RSI (14)': 'Sell', 'StochRSI %K': 'Sell', 'MACD Signal': 'Sell', 'Stoch %K': 'Sell', 'Awesome Osc.': 'Sell', 'ADX (14)': 'Trend (26)', 'BBands Pos.': 'Lower',
        'EMA (20) vs Price': 'Sell', 'SMA (50/200)': 'Sell', 'VWAP vs Price': 'Sell'},
    {'Asset Type': 'Stock', 'Crypto Rank': None, 'Market Cap': 1.75e12, 'Asset Name': 'Alphabet Inc. (GOOGL)', 'Ticker': 'GOOGL', 'TradingViewSymbol': 'NASDAQ:GOOGL', 'Current Price ($)': 140.10, 'Var. 1H (%)': 0.0, 'Var. 12H (%)': 0.1, 'Var. 24H (%)': 0.7, 'Var. 1W (%)': 0.5,
        'AI Signal': 'Neutral', 'MA Cross': 'Wait', 'RSI Div.': 'None', 'MACD Div.': 'None', 'Vol. Breakout': 'No Break', 'OBV Signal': 'Wait', 'ATR Signal': 'Wait',
        'RSI (14)': 'Wait', 'StochRSI %K': 'Wait', 'MACD Signal': 'Wait', 'Stoch %K': 'Wait', 'Awesome Osc.': 'Wait', 'ADX (14)': 'No Trend (15)', 'BBands Pos.': 'Mid',
        'EMA (20) vs Price': 'Wait', 'SMA (50/200)': 'Buy', 'VWAP vs Price': 'Wait'},
    {'Asset Type': 'Stock', 'Crypto Rank': None, 'Market Cap': 1.22e12, 'Asset Name': 'Meta Platforms Inc.', 'Ticker': 'META', 'TradingViewSymbol': 'NASDAQ:META', 'Current Price ($)': 480.12, 'Var. 1H (%)': -0.1, 'Var. 12H (%)': 0.0, 'Var. 24H (%)': -0.8, 'Var. 1W (%)': 0.2,
        'AI Signal': 'Neutral', 'MA Cross': 'Wait', 'RSI Div.': 'None', 'MACD Div.': 'None', 'Vol. Breakout': 'No Break', 'OBV Signal': 'Wait', 'ATR Signal': 'Wait',
        'RSI (14)': 'Wait', 'StochRSI %K': 'Sell', 'MACD Signal': 'Wait', 'Stoch %K': 'Sell', 'Awesome Osc.': 'Wait', 'ADX (14)': 'Weak (19)', 'BBands Pos.': 'Mid',
        'EMA (20) vs Price': 'Wait', 'SMA (50/200)': 'Wait', 'VWAP vs Price': 'Sell'},
    {'Asset Type': 'Stock', 'Crypto Rank': None, 'Market Cap': 5.60e11, 'Asset Name': 'Tesla, Inc.', 'Ticker': 'TSLA', 'TradingViewSymbol': 'NASDAQ:TSLA', 'Current Price ($)': 177.45, 'Var. 1H (%)': -0.7, 'Var. 12H (%)': -1.5, 'Var. 24H (%)': -3.0, 'Var. 1W (%)': -6.5,
        'AI Signal': 'Strong Sell', 'MA Cross': 'Death Cross (Sell)', 'RSI Div.': 'Bearish Div. (Sell)', 'MACD Div.': 'Bearish Div. (Sell)', 'Vol. Breakout': 'Bearish Break (Sell)', 'OBV Signal': 'Sell', 'ATR Signal': 'Sell',
        'RSI (14)': 'Sell', 'StochRSI %K': 'Sell', 'MACD Signal': 'Sell', 'Stoch %K': 'Sell', 'Awesome Osc.': 'Sell', 'ADX (14)': 'Strong (42)', 'BBands Pos.': 'Lower',
        'EMA (20) vs Price': 'Sell', 'SMA (50/200)': 'Sell', 'VWAP vs Price': 'Sell'},
    {'Asset Type': 'Stock', 'Crypto Rank': None, 'Market Cap': 2.20e8, 'Asset Name': 'Rigetti Computing (GTI)', 'Ticker': 'RGTI', 'TradingViewSymbol': 'NASDAQ:RGTI', 'Current Price ($)': 1.52, 'Var. 1H (%)': -0.5, 'Var. 12H (%)': -1.0, 'Var. 24H (%)': -1.2, 'Var. 1W (%)': -3.5,
        'AI Signal': 'Sell', 'MA Cross': 'Death Cross (Sell)', 'RSI Div.': 'None', 'MACD Div.': 'None', 'Vol. Breakout': 'No Break', 'OBV Signal': 'Sell', 'ATR Signal': 'Wait',
        'RSI (14)': 'Buy', 'StochRSI %K': 'Buy', 'MACD Signal': 'Sell', 'Stoch %K': 'Buy', 'Awesome Osc.': 'Sell', 'ADX (14)': 'Weak (17)', 'BBands Pos.': 'Lower',
        'EMA (20) vs Price': 'Sell', 'SMA (50/200)': 'Sell', 'VWAP vs Price': 'Sell'},
    {'Asset Type': 'Stock', 'Crypto Rank': None, 'Market Cap': 2.10e9, 'Asset Name': 'IonQ Inc. (Quantum)', 'Ticker': 'IONQ', 'TradingViewSymbol': 'NYSE:IONQ', 'Current Price ($)': 10.30, 'Var. 1H (%)': 0.0, 'Var. 12H (%)': -0.2, 'Var. 24H (%)': 0.1, 'Var. 1W (%)': -1.0,
        'AI Signal': 'Neutral', 'MA Cross': 'Wait', 'RSI Div.': 'None', 'MACD Div.': 'None', 'Vol. Breakout': 'No Break', 'OBV Signal': 'Wait', 'ATR Signal': 'Wait',
        'RSI (14)': 'Wait', 'StochRSI %K': 'Wait', 'MACD Signal': 'Wait', 'Stoch %K': 'Wait', 'Awesome Osc.': 'Wait', 'ADX (14)': 'No Trend (12)', 'BBands Pos.': 'Mid',
        'EMA (20) vs Price': 'Wait', 'SMA (50/200)': 'Wait', 'VWAP vs Price': 'Wait'},
    {'Asset Type': 'ETF', 'Crypto Rank': None, 'Market Cap': 5.50e8, 'Asset Name': 'ProSh Volatil ST Fut (UVXY)', 'Ticker': 'UVXY', 'TradingViewSymbol': 'AMEX:UVXY', 'Current Price ($)': 8.50, 'Var. 1H (%)': 1.0, 'Var. 12H (%)': 2.5, 'Var. 24H (%)': 5.1, 'Var. 1W (%)': 10.0,
        'AI Signal': 'Buy', 'MA Cross': 'Wait', 'RSI Div.': 'None', 'MACD Div.': 'None', 'Vol. Breakout': 'Bullish Break (Buy)', 'OBV Signal': 'Buy', 'ATR Signal': 'Buy',
        'RSI (14)': 'Sell', 'StochRSI %K': 'Sell', 'MACD Signal': 'Buy', 'Stoch %K': 'Sell', 'Awesome Osc.': 'Buy', 'ADX (14)': 'Trend (25)', 'BBands Pos.': 'Upper',
        'EMA (20) vs Price': 'Buy', 'SMA (50/200)': 'Wait', 'VWAP vs Price': 'Buy'},
    {'Asset Type': 'ETF', 'Crypto Rank': None, 'Market Cap': 2.21e10, 'Asset Name': 'ProSh UltraPro QQQ (TQQQ)', 'Ticker': 'TQQQ', 'TradingViewSymbol': 'NASDAQ:TQQQ', 'Current Price ($)': 55.60, 'Var. 1H (%)': 0.4, 'Var. 12H (%)': 1.1, 'Var. 24H (%)': 1.5, 'Var. 1W (%)': 4.0,
        'AI Signal': '🔥 Strong Buy', 'MA Cross': 'Golden Cross (Buy)', 'RSI Div.': 'None', 'MACD Div.': 'None', 'Vol. Breakout': 'No Break', 'OBV Signal': 'Buy', 'ATR Signal': 'Buy',
        'RSI (14)': 'Buy', 'StochRSI %K': 'Buy', 'MACD Signal': 'Buy', 'Stoch %K': 'Buy', 'Awesome Osc.': 'Buy', 'ADX (14)': 'Strong (38)', 'BBands Pos.': 'Upper',
        'EMA (20) vs Price': 'Buy', 'SMA (50/200)': 'Buy', 'VWAP vs Price': 'Buy'},
]

# Column display order and renaming map
# Original names as keys in the data, display names for headers
# This defines the structure of our data processing and display logic
COLS_TO_DISPLAY_ORDER_ORIGINAL_NAMES = [
    'Asset Name', 'Ticker', 'Current Price ($)',
    'Var. 1H (%)', 'Var. 12H (%)', 'Var. 24H (%)', 'Var. 1W (%)',
    'AI Signal', 
    'MA Cross', 'RSI Div.', 'MACD Div.', 'Vol. Breakout',
    'OBV Signal', 'ATR Signal',
    'RSI (14)', 'StochRSI %K', 'MACD Signal', 'Stoch %K', 'Awesome Osc.',
    'ADX (14)', 'BBands Pos.',
    'EMA (20) vs Price', 'SMA (50/200)', 'VWAP vs Price'
]

RENAME_MAP_FOR_DISPLAY_HEADERS = {
    'Current Price ($)': 'Price ($)',
    'Awesome Osc.': 'AO', 'StochRSI %K': 'SRSI %K', 'MACD Signal': 'MACD', 'Stoch %K': 'Stoch K',
    'ADX (14)': 'ADX', 'BBands Pos.': 'BB Pos.', 'OBV Signal': 'OBV', 'ATR Signal': 'ATR',
    'EMA (20) vs Price': 'EMA20/P', 'SMA (50/200)': 'SMA50/200', 
    'VWAP vs Price': 'VWAP/P',
    'MA Cross': 'MA Cross', 'RSI Div.': 'RSI Div', 'MACD Div.': 'MACD Div', 'Vol. Breakout': 'Vol Break'
}

RSI_PERIOD = 14
RSI_OVERSOLD = 30
RSI_OVERBOUGHT = 70

# FILE_FOOTER_START
# End of file: config.py
# Version: 0.2.0
# Last Modified: 2024-03-21
# FILE_FOOTER_END
