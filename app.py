# FILE_VERSION_START
# Project: CryptoAndStocksIndicators
# File: app.py
# Version: 0.2.4
# Date: 2024-03-21
# Author: [Your Name/Nickname]
# Description: Added Python version debug output. All code in one file.
# FILE_VERSION_END

import streamlit as st
import sys # Import sys to get Python version

# --- Print Python version for debugging ---
# This will appear in the Streamlit app's browser console if it gets that far,
# and in the Streamlit Cloud app logs.
PYTHON_VERSION_INFO = f"--- PYTHON VERSION FROM APP.PY: {sys.version} ---"
print(PYTHON_VERSION_INFO)
# We can also try to write it to the app if it fully loads
# st.sidebar.text(f"Python: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")


import pandas as pd
from datetime import datetime, timedelta
import traceback

# Attempt to import yfinance and pandas_ta
try:
    import yfinance as yf
    import pandas_ta as ta
    LIBS_AVAILABLE = True
except ImportError:
    yf = None
    ta = None
    LIBS_AVAILABLE = False

# --- Initial Setup and Session State for Error Logs ---
if 'error_logs' not in st.session_state:
    st.session_state.error_logs = []

# --- Constants and Configuration ---
RSI_PERIOD = 14
RSI_OVERSOLD = 30
RSI_OVERBOUGHT = 70

# --- Logging Helper Function ---
def log_error_app(message, asset_ticker=None, function_name=None, e=None):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"**Timestamp:** {timestamp}"
    if function_name: log_entry += f" | **Function:** `{function_name}`"
    if asset_ticker: log_entry += f" | **Asset:** `{asset_ticker}`"
    log_entry += f" | **Error:** {message}"
    
    if e is not None and isinstance(e, Exception):
        try:
            tb_str_list = traceback.format_exception(type(e), e, e.__traceback__)
            log_entry += f"\n**Traceback Snippet:**\n```\n{''.join(tb_str_list[-2:])}\n```"
        except Exception as tb_ex:
            log_entry += f"\n**Traceback Formatting Error:** {str(tb_ex)}"
            log_entry += f"\n**Original Exception Details:** {str(e)}"
    elif e is not None: 
        log_entry += f"\n**Details (Non-Exception object passed):** {str(e)}"
        
    if 'error_logs' in st.session_state: # Ensure session_state is available
        st.session_state.error_logs.append(log_entry)
    else: # Fallback if session_state is not ready (e.g. very early error)
        print(f"EARLY LOG (NO SESSION): {log_entry}")


# Log library availability status once
if 'lib_status_logged' not in st.session_state:
    if LIBS_AVAILABLE:
        log_error_app("Successfully imported yfinance and pandas-ta.", function_name="main_app_imports", e=None)
    else:
        log_error_app("yfinance or pandas-ta not found/imported. Real-time calculations will be skipped.", function_name="main_app_imports", e=None)
    st.session_state.lib_status_logged = True


# --- Data Fetching and Processing Functions ---
def calculate_real_rsi_for_aapl(rsi_period=RSI_PERIOD, rsi_oversold=RSI_OVERSOLD, rsi_overbought=RSI_OVERBOUGHT):
    global yf, ta 

    if not LIBS_AVAILABLE or yf is None or ta is None:
        # This specific log might be redundant if already logged by the global check,
        # but good for specific function context if called elsewhere.
        # log_error_app("Libs yfinance/pandas-ta not available for RSI calc.", "AAPL", "calculate_real_rsi_for_aapl", e=None)
        return "N/A (Libs Missing)"

    try:
        ticker = "AAPL"
        end_date = datetime.now()
        start_date = end_date - timedelta(days=270) # Increased data for RSI stability
        
        stock_data = yf.download(ticker.upper(), start=start_date, end=end_date, progress=False, timeout=15)

        if stock_data.empty or len(stock_data) < rsi_period * 2: # Need enough data points
            log_error_app(f"Not enough or no data returned for {ticker} from yfinance (rows: {len(stock_data)}).", ticker, "calculate_real_rsi_for_aapl", e=None)
            return "N/A (No/Insufficient Data)"

        if 'Close' not in stock_data.columns:
            log_error_app(f"'Close' column missing in yfinance data for {ticker}.", ticker, "calculate_real_rsi_for_aapl", e=None)
            return "N/A (Data Format)"

        rsi_series = stock_data.ta.rsi(close=stock_data['Close'], length=rsi_period)
        
        if rsi_series is None or rsi_series.empty or rsi_series.isna().all():
            log_error_app(f"RSI calculation returned empty or all NaN for {ticker}.", ticker, "calculate_real_rsi_for_aapl", e=None)
            return "N/A (RSI Calc Issue)"

        # Get the very last valid RSI value
        last_rsi = rsi_series.dropna().iloc[-1] if not rsi_series.dropna().empty else None
        
        if last_rsi is None or pd.isna(last_rsi):
            log_error_app(f"Last RSI value is NaN or None for {ticker} after dropna.", ticker, "calculate_real_rsi_for_aapl", e=None)
            return "N/A (NaN RSI)"

        if last_rsi < rsi_oversold: return "Buy"
        elif last_rsi > rsi_overbought: return "Sell"
        else: return "Wait"
            
    except Exception as e_calc:
        log_error_app(f"Exception during RSI calculation for {ticker}.", ticker, "calculate_real_rsi_for_aapl", e=e_calc)
        return "Error (Calc)"

def get_base_fictional_data():
    """Returns the base list of fictional asset data."""
    return [
        # Crypto
        {'Asset Type': 'Crypto', 'Crypto Rank': 1, 'Market Cap': 1.35e12, 'Asset Name': 'Bitcoin', 'Ticker': 'BTC', 'Current Price ($)': 68500.50, 'Var. 1H (%)': 0.8, 'Var. 12H (%)': 2.0, 'Var. 24H (%)': 1.5, 'Var. 1W (%)': 3.0,
         'AI Signal': 'Buy', 'MA Cross': 'Wait', 'RSI Div.': 'None', 'MACD Div.': 'None', 'Vol. Breakout': 'No Break', 'OBV Signal': 'Buy', 'ATR Signal': 'Buy',
         'RSI (14)': 'Buy', 'StochRSI %K': 'Wait', 'MACD Signal': 'Buy', 'Stoch %K': 'Wait', 'Awesome Osc.': 'Buy', 'ADX (14)': 'Strong (40)', 'BBands Pos.': 'Mid',
         'EMA (20) vs Price': 'Buy', 'SMA (50/200)': 'Buy', 'VWAP vs Price': 'Buy'},
        {'Asset Type': 'Crypto', 'Crypto Rank': 2, 'Market Cap': 4.50e11, 'Asset Name': 'Ethereum', 'Ticker': 'ETH', 'Current Price ($)': 3750.00, 'Var. 1H (%)': -0.3, 'Var. 12H (%)': 1.0, 'Var. 24H (%)': 0.8, 'Var. 1W (%)': 2.5,
         'AI Signal': 'Buy', 'MA Cross': 'Golden Cross (Buy)', 'RSI Div.': 'Bullish Div. (Buy)', 'MACD Div.': 'None', 'Vol. Breakout': 'No Break','OBV Signal': 'Wait', 'ATR Signal': 'Wait',
         'RSI (14)': 'Wait', 'StochRSI %K': 'Buy', 'MACD Signal': 'Buy', 'Stoch %K': 'Buy', 'Awesome Osc.': 'Buy','ADX (14)': 'Trend (30)', 'BBands Pos.': 'Upper',
         'EMA (20) vs Price': 'Buy', 'SMA (50/200)': 'Buy', 'VWAP vs Price': 'Buy'},
        # Stocks & ETFs
        {'Asset Type': 'Stock', 'Crypto Rank': None, 'Market Cap': 3.12e12, 'Asset Name': 'Microsoft Corp.', 'Ticker': 'MSFT', 'Current Price ($)': 420.55, 'Var. 1H (%)': 0.1, 'Var. 12H (%)': 0.5, 'Var. 24H (%)': 0.2, 'Var. 1W (%)': 1.5,
         'AI Signal': '🔥 Strong Buy', 'MA Cross': 'Golden Cross (Buy)', 'RSI Div.': 'None', 'MACD Div.': 'None', 'Vol. Breakout': 'Bullish Break (Buy)', 'OBV Signal': 'Buy', 'ATR Signal': 'Buy',
         'RSI (14)': 'Wait', 'StochRSI %K': 'Buy', 'MACD Signal': 'Buy', 'Stoch %K': 'Wait', 'Awesome Osc.': 'Buy', 'ADX (14)': 'Trend (28)', 'BBands Pos.': 'Mid',
         'EMA (20) vs Price': 'Buy', 'SMA (50/200)': 'Buy', 'VWAP vs Price': 'Buy'},
        {'Asset Type': 'Stock', 'Crypto Rank': None, 'Market Cap': 2.63e12, 'Asset Name': 'Apple Inc.', 'Ticker': 'AAPL', 'Current Price ($)': 170.34, 'Var. 1H (%)': -0.2, 'Var. 12H (%)': -0.8, 'Var. 24H (%)': -0.5, 'Var. 1W (%)': -2.0,
         'AI Signal': 'Sell', 'MA Cross': 'Wait', 'RSI Div.': 'Bearish Div. (Sell)', 'MACD Div.': 'Bearish Div. (Sell)', 'Vol. Breakout': 'No Break', 'OBV Signal': 'Sell', 'ATR Signal': 'Sell',
         'RSI (14)': 'CALCULATING...', 'StochRSI %K': 'Sell', 'MACD Signal': 'Sell', 'Stoch %K': 'Sell', 'Awesome Osc.': 'Sell', 'ADX (14)': 'Weak (18)', 'BBands Pos.': 'Upper',
         'EMA (20) vs Price': 'Sell', 'SMA (50/200)': 'Wait', 'VWAP vs Price': 'Sell'},
        {'Asset Type': 'Stock', 'Crypto Rank': None, 'Market Cap': 2.20e12, 'Asset Name': 'NVIDIA Corp.', 'Ticker': 'NVDA', 'Current Price ($)': 880.27, 'Var. 1H (%)': 0.5, 'Var. 12H (%)': 1.2, 'Var. 24H (%)': 2.1, 'Var. 1W (%)': 5.3,
         'AI Signal': '🔥 Strong Buy', 'MA Cross': 'Golden Cross (Buy)', 'RSI Div.': 'None', 'MACD Div.': 'Bullish Div. (Buy)', 'Vol. Breakout': 'Bullish Break (Buy)', 'OBV Signal': 'Buy', 'ATR Signal': 'Buy',
         'RSI (14)': 'Buy', 'StochRSI %K': 'Buy', 'MACD Signal': 'Buy', 'Stoch %K': 'Buy', 'Awesome Osc.': 'Buy', 'ADX (14)': 'Strong (35)', 'BBands Pos.': 'Upper',
         'EMA (20) vs Price': 'Buy', 'SMA (50/200)': 'Buy', 'VWAP vs Price': 'Buy'},
        {'Asset Type': 'Stock', 'Crypto Rank': None, 'Market Cap': 1.82e12, 'Asset Name': 'Amazon.com Inc.', 'Ticker': 'AMZN', 'Current Price ($)': 175.80, 'Var. 1H (%)': 0.0, 'Var. 12H (%)': -0.5, 'Var. 24H (%)': -1.0, 'Var. 1W (%)': -1.2,
         'AI Signal': 'Strong Sell', 'MA Cross': 'Death Cross (Sell)', 'RSI Div.': 'None', 'MACD Div.': 'None', 'Vol. Breakout': 'Bearish Break (Sell)', 'OBV Signal': 'Sell', 'ATR Signal': 'Sell',
         'RSI (14)': 'Sell', 'StochRSI %K': 'Sell', 'MACD Signal': 'Sell', 'Stoch %K': 'Sell', 'Awesome Osc.': 'Sell', 'ADX (14)': 'Trend (26)', 'BBands Pos.': 'Lower',
         'EMA (20) vs Price': 'Sell', 'SMA (50/200)': 'Sell', 'VWAP vs Price': 'Sell'},
        {'Asset Type': 'Stock', 'Crypto Rank': None, 'Market Cap': 1.75e12, 'Asset Name': 'Alphabet Inc. (GOOGL)', 'Ticker': 'GOOGL', 'Current Price ($)': 140.10, 'Var. 1H (%)': 0.0, 'Var. 12H (%)': 0.1, 'Var. 24H (%)': 0.7, 'Var. 1W (%)': 0.5,
         'AI Signal': 'Neutral', 'MA Cross': 'Wait', 'RSI Div.': 'None', 'MACD Div.': 'None', 'Vol. Breakout': 'No Break', 'OBV Signal': 'Wait', 'ATR Signal': 'Wait',
         'RSI (14)': 'Wait', 'StochRSI %K': 'Wait', 'MACD Signal': 'Wait', 'Stoch %K': 'Wait', 'Awesome Osc.': 'Wait', 'ADX (14)': 'No Trend (15)', 'BBands Pos.': 'Mid',
         'EMA (20) vs Price': 'Wait', 'SMA (50/200)': 'Buy', 'VWAP vs Price': 'Wait'},
        {'Asset Type': 'Stock', 'Crypto Rank': None, 'Market Cap': 1.22e12, 'Asset Name': 'Meta Platforms Inc.', 'Ticker': 'META', 'Current Price ($)': 480.12, 'Var. 1H (%)': -0.1, 'Var. 12H (%)': 0.0, 'Var. 24H (%)': -0.8, 'Var. 1W (%)': 0.2,
         'AI Signal': 'Neutral', 'MA Cross': 'Wait', 'RSI Div.': 'None', 'MACD Div.': 'None', 'Vol. Breakout': 'No Break', 'OBV Signal': 'Wait', 'ATR Signal': 'Wait',
         'RSI (14)': 'Wait', 'StochRSI %K': 'Sell', 'MACD Signal': 'Wait', 'Stoch %K': 'Sell', 'Awesome Osc.': 'Wait', 'ADX (14)': 'Weak (19)', 'BBands Pos.': 'Mid',
         'EMA (20) vs Price': 'Wait', 'SMA (50/200)': 'Wait', 'VWAP vs Price': 'Sell'},
        {'Asset Type': 'Stock', 'Crypto Rank': None, 'Market Cap': 5.60e11, 'Asset Name': 'Tesla, Inc.', 'Ticker': 'TSLA', 'Current Price ($)': 177.45, 'Var. 1H (%)': -0.7, 'Var. 12H (%)': -1.5, 'Var. 24H (%)': -3.0, 'Var. 1W (%)': -6.5,
         'AI Signal': 'Strong Sell', 'MA Cross': 'Death Cross (Sell)', 'RSI Div.': 'Bearish Div. (Sell)', 'MACD Div.': 'Bearish Div. (Sell)', 'Vol. Breakout': 'Bearish Break (Sell)', 'OBV Signal': 'Sell', 'ATR Signal': 'Sell',
         'RSI (14)': 'Sell', 'StochRSI %K': 'Sell', 'MACD Signal': 'Sell', 'Stoch %K': 'Sell', 'Awesome Osc.': 'Sell', 'ADX (14)': 'Strong (42)', 'BBands Pos.': 'Lower',
         'EMA (20) vs Price': 'Sell', 'SMA (50/200)': 'Sell', 'VWAP vs Price': 'Sell'},
        {'Asset Type': 'Stock', 'Crypto Rank': None, 'Market Cap': 2.20e8, 'Asset Name': 'Rigetti Computing (GTI)', 'Ticker': 'RGTI', 'Current Price ($)': 1.52, 'Var. 1H (%)': -0.5, 'Var. 12H (%)': -1.0, 'Var. 24H (%)': -1.2, 'Var. 1W (%)': -3.5,
         'AI Signal': 'Sell', 'MA Cross': 'Death Cross (Sell)', 'RSI Div.': 'None', 'MACD Div.': 'None', 'Vol. Breakout': 'No Break', 'OBV Signal': 'Sell', 'ATR Signal': 'Wait',
         'RSI (14)': 'Buy', 'StochRSI %K': 'Buy', 'MACD Signal': 'Sell', 'Stoch %K': 'Buy', 'Awesome Osc.': 'Sell', 'ADX (14)': 'Weak (17)', 'BBands Pos.': 'Lower',
         'EMA (20) vs Price': 'Sell', 'SMA (50/200)': 'Sell', 'VWAP vs Price': 'Sell'},
        {'Asset Type': 'Stock', 'Crypto Rank': None, 'Market Cap': 2.10e9, 'Asset Name': 'IonQ Inc. (Quantum)', 'Ticker': 'IONQ', 'Current Price ($)': 10.30, 'Var. 1H (%)': 0.0, 'Var. 12H (%)': -0.2, 'Var. 24H (%)': 0.1, 'Var. 1W (%)': -1.0,
         'AI Signal': 'Neutral', 'MA Cross': 'Wait', 'RSI Div.': 'None', 'MACD Div.': 'None', 'Vol. Breakout': 'No Break', 'OBV Signal': 'Wait', 'ATR Signal': 'Wait',
         'RSI (14)': 'Wait', 'StochRSI %K': 'Wait', 'MACD Signal': 'Wait', 'Stoch %K': 'Wait', 'Awesome Osc.': 'Wait', 'ADX (14)': 'No Trend (12)', 'BBands Pos.': 'Mid',
         'EMA (20) vs Price': 'Wait', 'SMA (50/200)': 'Wait', 'VWAP vs Price': 'Wait'},
        {'Asset Type': 'ETF', 'Crypto Rank': None, 'Market Cap': 5.50e8, 'Asset Name': 'ProSh Volatil ST Fut (UVXY)', 'Ticker': 'UVXY', 'Current Price ($)': 8.50, 'Var. 1H (%)': 1.0, 'Var. 12H (%)': 2.5, 'Var. 24H (%)': 5.1, 'Var. 1W (%)': 10.0,
         'AI Signal': 'Buy', 'MA Cross': 'Wait', 'RSI Div.': 'None', 'MACD Div.': 'None', 'Vol. Breakout': 'Bullish Break (Buy)', 'OBV Signal': 'Buy', 'ATR Signal': 'Buy',
         'RSI (14)': 'Sell', 'StochRSI %K': 'Sell', 'MACD Signal': 'Buy', 'Stoch %K': 'Sell', 'Awesome Osc.': 'Buy', 'ADX (14)': 'Trend (25)', 'BBands Pos.': 'Upper',
         'EMA (20) vs Price': 'Buy', 'SMA (50/200)': 'Wait', 'VWAP vs Price': 'Buy'},
        {'Asset Type': 'ETF', 'Crypto Rank': None, 'Market Cap': 2.21e10, 'Asset Name': 'ProSh UltraPro QQQ (TQQQ)', 'Ticker': 'TQQQ', 'Current Price ($)': 55.60, 'Var. 1H (%)': 0.4, 'Var. 12H (%)': 1.1, 'Var. 24H (%)': 1.5, 'Var. 1W (%)': 4.0,
         'AI Signal': '🔥 Strong Buy', 'MA Cross': 'Golden Cross (Buy)', 'RSI Div.': 'None', 'MACD Div.': 'None', 'Vol. Breakout': 'No Break', 'OBV Signal': 'Buy', 'ATR Signal': 'Buy',
         'RSI (14)': 'Buy', 'StochRSI %K': 'Buy', 'MACD Signal': 'Buy', 'Stoch %K': 'Buy', 'Awesome Osc.': 'Buy', 'ADX (14)': 'Strong (38)', 'BBands Pos.': 'Upper',
         'EMA (20) vs Price': 'Buy', 'SMA (50/200)': 'Buy', 'VWAP vs Price': 'Buy'},
    ]


def get_processed_data_with_real_aapl_rsi():
    base_df = pd.DataFrame(get_base_fictional_data())
    if 'AAPL' in base_df['Ticker'].values:
        aapl_rsi_signal = calculate_real_rsi_for_aapl()
        base_df.loc[base_df['Ticker'] == 'AAPL', 'RSI (14)'] = aapl_rsi_signal
    else:
        log_error_app("AAPL ticker not found in base data for RSI update.", "AAPL", "get_processed_data_with_real_aapl_rsi", e=None)
    
    # --- Sorting Logic ---
    # Create a temporary DataFrame with sorting keys from the original data structure
    # This ensures we have 'Asset Type', 'Crypto Rank', 'Market Cap' for sorting
    sort_keys_df_data = [
        {'Ticker': item['Ticker'], 'Asset Type': item['Asset Type'], 'Crypto Rank': item.get('Crypto Rank'), 'Market Cap': item.get('Market Cap')}
        for item in get_base_fictional_data() # Use a fresh copy of base data structure
    ]
    sort_keys_df = pd.DataFrame(sort_keys_df_data)

    asset_type_order = {'Crypto': 0, 'Stock': 1, 'ETF': 2}
    sort_keys_df['AssetTypeSortCol'] = sort_keys_df['Asset Type'].map(asset_type_order)
    sort_keys_df['PrimarySortKeyCol'] = sort_keys_df.apply(
        lambda row: row['Crypto Rank'] if row['Asset Type'] == 'Crypto' and pd.notna(row['Crypto Rank']) else (-row['Market Cap'] if pd.notna(row['Market Cap']) else float('inf')),
        axis=1
    )
    sort_keys_df.sort_values(by=['AssetTypeSortCol', 'PrimarySortKeyCol'], ascending=[True, True], inplace=True)
    
    # Reorder base_df (which has the updated AAPL RSI) based on the sorted tickers
    # Set Ticker as index for both DataFrames for easy reordering
    base_df.set_index('Ticker', inplace=True)
    sort_keys_df.set_index('Ticker', inplace=True)
    
    # Reindex base_df according to the sorted index of sort_keys_df
    # This preserves the updated AAPL RSI value while achieving the correct order
    final_df = base_df.reindex(sort_keys_df.index).reset_index()
    
    # Drop temporary/setup columns that might have been in the original base data if they are not display columns
    # The main data structure for display is defined by cols_to_display_order later
    # So, no need to drop 'Asset Type', etc. here if they are not in cols_to_display_order
    return final_df


# --- UI Styling Function ---
def apply_cell_styles_for_display(val, column_name_displayed=""):
    color_css = ""
    font_weight_css = ""
    if isinstance(val, (int, float)) and "%" in column_name_displayed:
        if val > 0: color_css = 'color: green'
        elif val < 0: color_css = 'color: red'
        else: color_css = 'color: gray'
    elif isinstance(val, str):
        val_upper = val.upper()
        current_col_name_upper = column_name_displayed.upper()

        if current_col_name_upper == 'AI SIGNAL':
            if 'STRONG BUY' in val_upper: color_css = 'color: darkgreen'; font_weight_css = 'font-weight: bold'
            elif 'BUY' in val_upper: color_css = 'color: green'; font_weight_css = 'font-weight: bold'
            elif 'STRONG SELL' in val_upper: color_css = 'color: darkred'; font_weight_css = 'font-weight: bold'
            elif 'SELL' in val_upper: color_css = 'color: red'; font_weight_css = 'font-weight: bold'
            elif 'NEUTRAL' in val_upper: color_css = 'color: gray'
        elif current_col_name_upper == 'ADX':
            if 'STRONG' in val_upper or 'TREND' in val_upper: color_css = 'color: green'
            elif 'WEAK' in val_upper or 'NO TREND' in val_upper: color_css = 'color: gray'
            else: color_css = 'color: gray'
        elif current_col_name_upper == 'BB POS.':
            if 'UPPER' in val_upper: color_css = 'color: red'
            elif 'LOWER' in val_upper: color_css = 'color: green'
            elif 'MID' in val_upper: color_css = 'color: gray'
        elif current_col_name_upper in ['OBV', 'ATR', 'RSI (14)', 'SRSI %K', 'MACD', 'STOCH K', 'AO', 
                                        'EMA20/P', 'SMA50/200', 'VWAP/P', 
                                        'MA CROSS', 'RSI DIV', 'MACD DIV', 'VOL BREAK']:
            # Catch specific N/A or Error states first and color them distinctively
            if '(LIBS MISSING)' in val_upper or '(NO DATA)' in val_upper or \
               '(CALC ISSUE)' in val_upper or '(NAN RSI)' in val_upper or \
               'ERROR (CALC)' in val_upper or 'N/A (REAL CALC)' in val_upper : # N/A (Real Calc) from placeholder
                color_css = 'color: orange' # Orange for calculation/data issues
            elif 'BUY' in val_upper or 'BULLISH' in val_upper or 'GOLDEN' in val_upper:
                color_css = 'color: green'; font_weight_css = 'font-weight: bold'
            elif 'SELL' in val_upper or 'BEARISH' in val_upper or 'DEATH' in val_upper:
                color_css = 'color: red'; font_weight_css = 'font-weight: bold'
            elif 'WAIT' in val_upper or 'NEUTRAL' in val_upper or 'NONE' in val_upper or 'NO BREAK' in val_upper or 'MID' in val_upper:
                color_css = 'color: gray'
    
    final_style = []
    if color_css: final_style.append(color_css)
    if font_weight_css: final_style.append(font_weight_css)
    return '; '.join(final_style) if final_style else None

# --- Main User Interface ---
st.set_page_config(layout="wide", page_title="Trading Indicators Dashboard")
st.title("🔥📊 Trading Indicators Dashboard")

# Display Python version being used by Streamlit
# This will be visible in the app sidebar or as a text element
# And also printed to the console log of Streamlit Cloud during app execution
st.sidebar.markdown(f"**Python Version:**")
st.sidebar.code(sys.version)
print(PYTHON_VERSION_INFO) # This was printed at the very start of the script too

st.caption(f"Version: 0.2.4 | Date: {datetime.now().strftime('%Y-%m-%d')}")


df_processed_data = get_processed_data_with_real_aapl_rsi()

cols_to_display_order = [
    'Asset Name', 'Ticker', 'Current Price ($)',
    'Var. 1H (%)', 'Var. 12H (%)', 'Var. 24H (%)', 'Var. 1W (%)',
    'AI Signal', 
    'MA Cross', 'RSI Div.', 'MACD Div.', 'Vol. Breakout',
    'OBV Signal', 'ATR Signal',
    'RSI (14)', 'StochRSI %K', 'MACD Signal', 'Stoch %K', 'Awesome Osc.',
    'ADX (14)', 'BBands Pos.',
    'EMA (20) vs Price', 'SMA (50/200)', 'VWAP vs Price'
]
# Filter df_processed_data to only include columns that are actually expected for display
# This prevents errors if get_processed_data_with_real_aapl_rsi changes its output columns slightly
# (e.g., if sorting keys were not dropped as intended)
existing_cols_for_display = [col for col in cols_to_display_order if col in df_processed_data.columns]
df_for_styling = df_processed_data[existing_cols_for_display].copy()


rename_map_for_display_headers = {
    'Current Price ($)': 'Price ($)',
    'Awesome Osc.': 'AO', 'StochRSI %K': 'SRSI %K', 'MACD Signal': 'MACD', 'Stoch %K': 'Stoch K',
    'ADX (14)': 'ADX', 'BBands Pos.': 'BB Pos.', 'OBV Signal': 'OBV', 'ATR Signal': 'ATR',
    'EMA (20) vs Price': 'EMA20/P', 'SMA (50/200)': 'SMA50/200', 
    'VWAP vs Price': 'VWAP/P',
    'MA Cross': 'MA Cross', 'RSI Div.': 'RSI Div', 'MACD Div.': 'MACD Div', 'Vol. Breakout': 'Vol Break'
}
df_for_styling.rename(columns=rename_map_for_display_headers, inplace=True)

formatters = {}
for col_header in df_for_styling.columns:
    if "%" in col_header:
         formatters[col_header] = lambda x: f"{x:+.1f}%" if isinstance(x, (int, float)) else x
    elif col_header == 'Price ($)':
        formatters[col_header] = "${:,.2f}"

styled_df = df_for_styling.style
for col_name_in_styled_df in df_for_styling.columns:
    styled_df = styled_df.apply(
        lambda series: series.map(lambda val: apply_cell_styles_for_display(val, column_name_displayed=series.name)),
        subset=[col_name_in_styled_df]
    )
styled_df = styled_df.format(formatters)
styled_df = styled_df.set_properties(**{'text-align': 'center'}, subset=df_for_styling.columns.drop(['Asset Name', 'Price ($)']))
styled_df = styled_df.set_properties(**{'text-align': 'right'}, subset=['Price ($)'])
styled_df = styled_df.set_properties(**{'text-align': 'left'}, subset=['Asset Name'])
font_size = "0.70em" 
styled_df = styled_df.set_table_styles([
    {'selector': 'th', 'props': [('text-align', 'center'), ('background-color', '#f0f2f6'), ('padding', '0.1rem'), ('font-size', font_size), ('white-space', 'nowrap')]},
    {'selector': 'td', 'props': [('padding', '0.1rem 0.15rem'), ('font-size', font_size), ('white-space', 'nowrap')]},
])

st.markdown("#### Aggregated and Individual Technical Signals")
st.dataframe(styled_df, use_container_width=False, hide_index=True)

# --- Legend ---
# (Legend content remains the same as in v0.1.9)
st.subheader("📜 Detailed Indicators and Columns Legend")
st.markdown("---")
st.markdown("##### General Information")
st.markdown("""
- **Asset Name**: Full name of the stock, cryptocurrency, or ETF.
- **Ticker**: Unique market symbol for the asset.
- **Price ($)**: Last recorded price for the asset, in USD.
""")
st.markdown("##### Price Variations (Short-Term Momentum)")
st.markdown("""
- **Var. 1H (%)**: Percentage price change in the last 1 hour.
- **Var. 12H (%)**: Percentage price change in the last 12 hours.
- **Var. 24H (%)**: Percentage price change in the last 24 hours.
- **Var. 1W (%)**: Percentage price change in the last week.
*<span style='color:green;'>Green</span> for increase (+), <span style='color:red;'>Red</span> for decrease (-), <span style='color:gray;'>Gray</span> for no change (0.0%).*
""", unsafe_allow_html=True)

st.markdown("##### AI Synthesis Signal")
st.markdown("""
- **AI Signal**: An algorithmically generated summary trading signal (<span style='color:darkgreen; font-weight:bold;'>🔥 Strong Buy</span>, <span style='color:green; font-weight:bold;'>Buy</span>, <span style='color:gray;'>Neutral</span>, <span style='color:red; font-weight:bold;'>Sell</span>, <span style='color:darkred; font-weight:bold;'>Strong Sell</span>).
""", unsafe_allow_html=True)

st.markdown("##### Advanced Confirmation Signals")
st.markdown("""
- **MA Cross** (Moving Average Crossover): Signals: <span style='color:green; font-weight:bold;'>Golden Cross (Buy)</span>, <span style='color:red; font-weight:bold;'>Death Cross (Sell)</span>, <span style='color:gray;'>Wait</span>.
- **RSI Div** (RSI Divergence): Signals: <span style='color:green; font-weight:bold;'>Bullish Div. (Buy)</span>, <span style='color:red; font-weight:bold;'>Bearish Div. (Sell)</span>, <span style='color:gray;'>None</span>.
- **MACD Div** (MACD Divergence): Signals: <span style='color:green; font-weight:bold;'>Bullish Div. (Buy)</span>, <span style='color:red; font-weight:bold;'>Bearish Div. (Sell)</span>, <span style='color:gray;'>None</span>.
- **Vol Break** (Volume Confirmed Breakout): Signals: <span style='color:green; font-weight:bold;'>Bullish Break (Buy)</span>, <span style='color:red; font-weight:bold;'>Bearish Break (Sell)</span>, <span style='color:gray;'>No Break</span>.
""", unsafe_allow_html=True)

st.markdown("##### Volume & Volatility Based Signals")
st.markdown("""
- **OBV** (On-Balance Volume Signal): Signals: <span style='color:green; font-weight:bold;'>BUY</span>, <span style='color:red; font-weight:bold;'>SELL</span>, <span style='color:gray;'>WAIT</span>.
- **ATR** (Average True Range Signal): Signals (Proposed): <span style='color:green; font-weight:bold;'>BUY/SELL</span> (high volatility breakout), <span style='color:gray;'>WAIT</span> (low volatility).
""", unsafe_allow_html=True)

st.markdown("##### Oscillators")
st.markdown("""
- **RSI (14)**: Signals: <30 <span style='color:green; font-weight:bold;'>BUY</span>, >70 <span style='color:red; font-weight:bold;'>SELL</span>, 30-70 (<span style='color:gray;'>WAIT</span>).
- **SRSI %K**: Signals: <20 <span style='color:green; font-weight:bold;'>BUY</span>, >80 <span style='color:red; font-weight:bold;'>SELL</span>, 20-80 (<span style='color:gray;'>WAIT</span>).
- **MACD**: Signals: <span style='color:green; font-weight:bold;'>BUY</span> MACD > Signal, <span style='color:red; font-weight:bold;'>SELL</span> MACD < Signal, <span style='color:gray;'>WAIT</span>.
- **Stoch K**: Signals: <20 <span style='color:green; font-weight:bold;'>BUY</span>, >80 <span style='color:red; font-weight:bold;'>SELL</span>, 20-80 (<span style='color:gray;'>WAIT</span>).
- **AO**: Signals: <span style='color:green; font-weight:bold;'>BUY</span> AO > 0, <span style='color:red; font-weight:bold;'>SELL</span> AO < 0, <span style='color:gray;'>WAIT</span>.
""", unsafe_allow_html=True)

st.markdown("##### Trend Strength & Other Volatility")
st.markdown("""
- **ADX**: Interpretation: >20 (<span style='color:green;'>Strong/Dev. Trend</span>), <20 (<span style='color:gray;'>Weak/No Trend</span>).
- **BB Pos.** (Bollinger Bands Pos.): Interpretation: <span style='color:green;'>Lower</span>, <span style='color:gray;'>Mid</span>, <span style='color:red;'>Upper</span>.
""", unsafe_allow_html=True)

st.markdown("##### Moving Averages (Price Relationship)")
st.markdown("""
- **EMA20/P**: <span style='color:green; font-weight:bold;'>BUY</span> P > EMA, <span style='color:red; font-weight:bold;'>SELL</span> P < EMA, <span style='color:gray;'>WAIT</span>.
- **SMA50/200**: *This refers to price relation to long-term MAs. 'MA Cross' covers the crossover event.* Signals: <span style='color:green; font-weight:bold;'>BUY</span> (Price above in uptrend), <span style='color:red; font-weight:bold;'>SELL</span> (Price below in downtrend), <span style='color:gray;'>WAIT</span>.
- **VWAP/P**: <span style='color:green; font-weight:bold;'>BUY</span> P > VWAP, <span style='color:red; font-weight:bold;'>SELL</span> P < VWAP, <span style='color:gray;'>WAIT</span>.
""", unsafe_allow_html=True)


# --- Error Logs Section ---
st.subheader("⚠️ Error Logs")
st.markdown("---")
error_count = len(st.session_state.error_logs)
expander_title = f"Show/Hide Error Logs ({error_count} {'error' if error_count == 1 else 'errors'})"

# Attempt to display Python version used by the app (if app gets this far)
# Moved here to ensure it's within the main app flow and not top-level script execution only
if 'python_version_displayed' not in st.session_state:
    try:
        st.sidebar.markdown("---")
        st.sidebar.markdown(f"**App Python Version:**")
        st.sidebar.code(f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
        st.session_state.python_version_displayed = True
    except Exception: # In case st.sidebar is not ready or other issues
        pass


with st.expander(expander_title, expanded=error_count > 0):
    if error_count > 0:
        for i, log_entry in enumerate(reversed(st.session_state.error_logs)):
            st.markdown(f"**Log #{error_count - i}:**\n{log_entry}", unsafe_allow_html=True)
            if i < error_count - 1: st.markdown("---")
    else:
        st.info("No errors recorded so far.")
    if st.button("Simulate App Error     "): 
        try: 1 / 0
        except Exception as e_sim: log_error_app("This is a simulated app error.", asset_ticker="APP_SIM", function_name="simulate_app_error_button", e=e_sim)
        st.rerun()
    if error_count > 0 and st.button("Clear All Error Logs     "):
        st.session_state.error_logs = []
        st.rerun()

st.markdown("---")
st.caption(f"File: app.py | Version: 0.2.4 | Last Modified: {datetime.now().strftime('%Y-%m-%d')}")

# FILE_FOOTER_START
# End of file: app.py
# Version: 0.2.4
# Last Modified: 2024-03-21
# FILE_FOOTER_END
