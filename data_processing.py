# FILE_VERSION_START
# Project: CryptoAndStocksIndicators
# File: data_processing.py
# Version: 0.2.0
# Date: 2024-03-21
# Author: [Your Name/Nickname]
# Description: Functions for fetching, processing, and calculating indicator data.
# FILE_VERSION_END

import pandas as pd
from datetime import datetime, timedelta
import yfinance as yf
import pandas_ta as ta
import streamlit as st # For st.session_state (for logging)
import traceback

# Import config variables (assuming config.py is in the same directory)
try:
    from config import ASSET_LIST_FICTIONAL_BASE, RSI_PERIOD, RSI_OVERSOLD, RSI_OVERBOUGHT
except ImportError: # Fallback if running a script directly that relies on this structure
    ASSET_LIST_FICTIONAL_BASE = [] # Provide a default empty list or handle error
    RSI_PERIOD = 14
    RSI_OVERSOLD = 30
    RSI_OVERBOUGHT = 70
    print("Warning: Could not import from config.py. Using default values.")


def log_error_from_data_processing(message, asset_ticker=None, function_name=None, e=None):
    """Appends a detailed error message to the session state error logs."""
    # This function is a copy of the one in app.py, ideally, this would be in a shared utils.py
    # For now, we duplicate it to avoid circular imports if utils.py imported app.py elements.
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"**Timestamp:** {timestamp}"
    if function_name: log_entry += f" | **Function:** `{function_name}`"
    if asset_ticker: log_entry += f" | **Asset:** `{asset_ticker}`"
    log_entry += f" | **Error:** {message}"
    if e:
        tb_str = traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)
        log_entry += f"\n**Traceback Snippet:**\n```\n{''.join(tb_str[-2:])}\n```"
    if 'error_logs' in st.session_state: # Check if running in Streamlit context
        st.session_state.error_logs.append(log_entry)
    else: # If not in Streamlit context (e.g., testing script directly)
        print(f"LOG ERROR (non-Streamlit): {log_entry.replace('**', '').replace('`', '')}")


def calculate_real_rsi_for_asset(ticker, rsi_period=RSI_PERIOD, rsi_oversold=RSI_OVERSOLD, rsi_overbought=RSI_OVERBOUGHT):
    """
    Fetches historical data for a given ticker using yfinance,
    calculates the RSI, and returns the RSI signal ('Buy', 'Sell', 'Wait').
    """
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=180)
        stock_data = yf.download(ticker.upper(), start=start_date, end=end_date, progress=False, timeout=10) # Added timeout

        if stock_data.empty:
            log_error_from_data_processing(f"No data returned for {ticker}.", ticker, "calculate_real_rsi_for_asset")
            return "N/A"

        # Calculate RSI using pandas_ta
        stock_data.ta.rsi(length=rsi_period, append=True)
        
        rsi_col_name = f'RSI_{rsi_period}'
        if rsi_col_name not in stock_data.columns or stock_data[rsi_col_name].empty or stock_data[rsi_col_name].isna().all():
            log_error_from_data_processing(f"RSI column '{rsi_col_name}' not found, empty, or all NaN for {ticker}.", ticker, "calculate_real_rsi_for_asset")
            return "N/A"

        last_rsi = stock_data[rsi_col_name].dropna().iloc[-1] # Drop NaNs before taking last
        
        if pd.isna(last_rsi): # Should be caught by previous check, but good to have
            log_error_from_data_processing(f"Last RSI value is NaN for {ticker} after dropna.", ticker, "calculate_real_rsi_for_asset")
            return "N/A"

        if last_rsi < rsi_oversold:
            return "Buy"
        elif last_rsi > rsi_overbought:
            return "Sell"
        else:
            return "Wait"
            
    except Exception as e:
        log_error_from_data_processing(f"Failed to calculate RSI for {ticker}.", ticker, "calculate_real_rsi_for_asset", e)
        return "Error"

def get_processed_data_with_real_aapl_rsi():
    """
    Generates data for the table. For AAPL, RSI is calculated from real data.
    """
    base_df = pd.DataFrame(ASSET_LIST_FICTIONAL_BASE)

    # Calculate real RSI for AAPL and update its row
    # Check if 'AAPL' is in the dataframe first
    if 'AAPL' in base_df['Ticker'].values:
        aapl_rsi_signal = calculate_real_rsi_for_asset("AAPL")
        base_df.loc[base_df['Ticker'] == 'AAPL', 'RSI (14)'] = aapl_rsi_signal
    else:
        log_error_from_data_processing("AAPL ticker not found in base data for RSI update.", "AAPL", "get_processed_data_with_real_aapl_rsi")


    # Sorting logic
    asset_type_order = {'Crypto': 0, 'Stock': 1, 'ETF': 2}
    # Ensure 'Asset Type' column exists from the base data
    if 'Asset Type' in base_df.columns:
        base_df['AssetTypeSortCol'] = base_df['Asset Type'].map(asset_type_order)
        # Ensure 'Crypto Rank' and 'Market Cap' columns exist
        if 'Crypto Rank' in base_df.columns and 'Market Cap' in base_df.columns:
            base_df['PrimarySortKeyCol'] = base_df.apply(
                lambda row: row['Crypto Rank'] if row['Asset Type'] == 'Crypto' and pd.notna(row['Crypto Rank']) else -row['Market Cap'], 
                axis=1
            )
            base_df.sort_values(by=['AssetTypeSortCol', 'PrimarySortKeyCol'], ascending=[True, True], inplace=True)
            base_df.drop(columns=['AssetTypeSortCol', 'PrimarySortKeyCol'], inplace=True, errors='ignore')
        else:
            log_error_from_data_processing("Missing 'Crypto Rank' or 'Market Cap' for sorting.", function_name="get_processed_data_with_real_aapl_rsi")
    else:
        log_error_from_data_processing("Missing 'Asset Type' for sorting.", function_name="get_processed_data_with_real_aapl_rsi")
    
    # Drop original columns used for sorting logic if they were part of ASSET_LIST_FICTIONAL_BASE
    # (Asset Type, Crypto Rank, Market Cap)
    # This is to ensure only display columns remain, as per previous logic
    base_df.drop(columns=['Asset Type', 'Crypto Rank', 'Market Cap'], inplace=True, errors='ignore')

    return base_df

# FILE_FOOTER_START
# End of file: data_processing.py
# Version: 0.2.0
# Last Modified: 2024-03-21
# FILE_FOOTER_END
