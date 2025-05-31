# FILE_VERSION_START
# Project: CryptoAndStocksIndicators
# File: app.py
# Version: 0.2.0
# Date: 2024-03-21
# Author: [Your Name/Nickname]
# Description: Implemented real RSI calculation for AAPL using yfinance and pandas-ta.
# FILE_VERSION_END

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import traceback
import yfinance as yf # For fetching stock data
import pandas_ta as ta # For technical analysis indicators

# --- Initial Setup and Session State for Error Logs ---
if 'error_logs' not in st.session_state:
    st.session_state.error_logs = []

# --- Helper Functions ---
def log_error(message, asset_ticker=None, function_name=None, e=None):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"**Timestamp:** {timestamp}"
    if function_name: log_entry += f" | **Function:** `{function_name}`"
    if asset_ticker: log_entry += f" | **Asset:** `{asset_ticker}`"
    log_entry += f" | **Error:** {message}"
    if e:
        tb_str = traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)
        log_entry += f"\n**Traceback Snippet:**\n```\n{''.join(tb_str[-2:])}\n```" # Last 2 lines
    st.session_state.error_logs.append(log_entry)

def calculate_real_rsi_for_asset(ticker, rsi_period=14, rsi_oversold=30, rsi_overbought=70):
    """
    Fetches historical data for a given ticker using yfinance,
    calculates the RSI, and returns the RSI signal ('Buy', 'Sell', 'Wait') and its value.
    """
    try:
        # Fetch historical data (e.g., last 6 months to have enough data for RSI)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=180) # Approx 6 months
        
        # yfinance uses uppercase tickers
        stock_data = yf.download(ticker.upper(), start=start_date, end=end_date, progress=False)

        if stock_data.empty:
            log_error(f"No data returned for {ticker}.", ticker, "calculate_real_rsi_for_asset")
            return "N/A", None # No data

        # Calculate RSI using pandas_ta
        stock_data.ta.rsi(length=rsi_period, append=True)
        
        # Get the last RSI value
        # The column name from pandas-ta is typically 'RSI_14'
        rsi_col_name = f'RSI_{rsi_period}'
        if rsi_col_name not in stock_data.columns or stock_data[rsi_col_name].empty:
            log_error(f"RSI column '{rsi_col_name}' not found or empty for {ticker}.", ticker, "calculate_real_rsi_for_asset")
            return "N/A", None

        last_rsi = stock_data[rsi_col_name].iloc[-1]
        
        if pd.isna(last_rsi):
            log_error(f"Last RSI value is NaN for {ticker}.", ticker, "calculate_real_rsi_for_asset")
            return "N/A", None

        # Determine signal
        rsi_value_for_display = f"{last_rsi:.2f}" # Format for potential display if needed
        if last_rsi < rsi_oversold:
            return "Buy", rsi_value_for_display
        elif last_rsi > rsi_overbought:
            return "Sell", rsi_value_for_display
        else:
            return "Wait", rsi_value_for_display
            
    except Exception as e:
        log_error(f"Failed to calculate RSI for {ticker}.", ticker, "calculate_real_rsi_for_asset", e)
        return "Error", None

def get_processed_data(): # Renamed from get_fictional_data
    """
    Generates data for the table. For AAPL, RSI is calculated from real data.
    """
    # Base fictional data structure
    # (Shortened for brevity, full list assumed)
    base_data_list = [
        {'Asset Type': 'Crypto', 'Crypto Rank': 1, 'Market Cap': 1.35e12, 'Asset Name': 'Bitcoin', 'Ticker': 'BTC', 'Current Price ($)': 68500.50, 'Var. 1H (%)': 0.8, 'Var. 12H (%)': 2.0, 'Var. 24H (%)': 1.5, 'Var. 1W (%)': 3.0,
         'AI Signal': 'Buy', 'MA Cross': 'Wait', 'RSI Div.': 'None', 'MACD Div.': 'None', 'Vol. Breakout': 'No Break', 'OBV Signal': 'Buy', 'ATR Signal': 'Buy',
         'RSI (14)': 'Buy', 'StochRSI %K': 'Wait', 'MACD Signal': 'Buy', 'Stoch %K': 'Wait', 'Awesome Osc.': 'Buy', 'ADX (14)': 'Strong (40)', 'BBands Pos.': 'Mid',
         'EMA (20) vs Price': 'Buy', 'SMA (50/200)': 'Buy', 'VWAP vs Price': 'Buy'},
        {'Asset Type': 'Crypto', 'Crypto Rank': 2, 'Market Cap': 4.50e11, 'Asset Name': 'Ethereum', 'Ticker': 'ETH', 'Current Price ($)': 3750.00, 'Var. 1H (%)': -0.3, 'Var. 12H (%)': 1.0, 'Var. 24H (%)': 0.8, 'Var. 1W (%)': 2.5,
         'AI Signal': 'Buy', 'MA Cross': 'Golden Cross (Buy)', 'RSI Div.': 'Bullish Div. (Buy)', 'MACD Div.': 'None', 'Vol. Breakout': 'No Break','OBV Signal': 'Wait', 'ATR Signal': 'Wait',
         'RSI (14)': 'Wait', 'StochRSI %K': 'Buy', 'MACD Signal': 'Buy', 'Stoch %K': 'Buy', 'Awesome Osc.': 'Buy','ADX (14)': 'Trend (30)', 'BBands Pos.': 'Upper',
         'EMA (20) vs Price': 'Buy', 'SMA (50/200)': 'Buy', 'VWAP vs Price': 'Buy'},
        {'Asset Type': 'Stock', 'Crypto Rank': None, 'Market Cap': 3.12e12, 'Asset Name': 'Microsoft Corp.', 'Ticker': 'MSFT', 'Current Price ($)': 420.55, 'Var. 1H (%)': 0.1, 'Var. 12H (%)': 0.5, 'Var. 24H (%)': 0.2, 'Var. 1W (%)': 1.5,
         'AI Signal': '🔥 Strong Buy', 'MA Cross': 'Golden Cross (Buy)', 'RSI Div.': 'None', 'MACD Div.': 'None', 'Vol. Breakout': 'Bullish Break (Buy)', 'OBV Signal': 'Buy', 'ATR Signal': 'Buy',
         'RSI (14)': 'Wait', 'StochRSI %K': 'Buy', 'MACD Signal': 'Buy', 'Stoch %K': 'Wait', 'Awesome Osc.': 'Buy', 'ADX (14)': 'Trend (28)', 'BBands Pos.': 'Mid',
         'EMA (20) vs Price': 'Buy', 'SMA (50/200)': 'Buy', 'VWAP vs Price': 'Buy'},
        # AAPL - This will be overridden
        {'Asset Type': 'Stock', 'Crypto Rank': None, 'Market Cap': 2.63e12, 'Asset Name': 'Apple Inc.', 'Ticker': 'AAPL', 'Current Price ($)': 170.34, 'Var. 1H (%)': -0.2, 'Var. 12H (%)': -0.8, 'Var. 24H (%)': -0.5, 'Var. 1W (%)': -2.0,
         'AI Signal': 'Sell', 'MA Cross': 'Wait', 'RSI Div.': 'Bearish Div. (Sell)', 'MACD Div.': 'Bearish Div. (Sell)', 'Vol. Breakout': 'No Break', 'OBV Signal': 'Sell', 'ATR Signal': 'Sell',
         'RSI (14)': 'FICTIONAL', 'StochRSI %K': 'Sell', 'MACD Signal': 'Sell', 'Stoch %K': 'Sell', 'Awesome Osc.': 'Sell', 'ADX (14)': 'Weak (18)', 'BBands Pos.': 'Upper',
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
    df = pd.DataFrame(base_data_list)

    # Calculate real RSI for AAPL and update its row
    aapl_rsi_signal, _ = calculate_real_rsi_for_asset("AAPL") # We only need the signal string for now
    if aapl_rsi_signal != "Error" and aapl_rsi_signal != "N/A":
        df.loc[df['Ticker'] == 'AAPL', 'RSI (14)'] = aapl_rsi_signal
    else:
        # If error, keep 'FICTIONAL' or set to 'N/A' to indicate problem
        df.loc[df['Ticker'] == 'AAPL', 'RSI (14)'] = aapl_rsi_signal 


    # Sorting logic (same as before)
    asset_type_order = {'Crypto': 0, 'Stock': 1, 'ETF': 2}
    df['AssetTypeSortCol'] = df['Asset Type'].map(asset_type_order)
    df['PrimarySortKeyCol'] = df.apply(
        lambda row: row['Crypto Rank'] if row['Asset Type'] == 'Crypto' else -row['Market Cap'], 
        axis=1
    )
    df.sort_values(by=['AssetTypeSortCol', 'PrimarySortKeyCol'], ascending=[True, True], inplace=True)
    df.drop(columns=['Asset Type', 'Crypto Rank', 'Market Cap', 'AssetTypeSortCol', 'PrimarySortKeyCol'], inplace=True, errors='ignore')
    return df

def apply_cell_styles(val, column_name_in_styled_df=""):
    color_css = ""
    font_weight_css = ""
    if isinstance(val, (int, float)) and "%" in column_name_in_styled_df:
        if val > 0: color_css = 'color: green'
        elif val < 0: color_css = 'color: red'
        else: color_css = 'color: gray'
    elif isinstance(val, str):
        val_upper = val.upper()
        current_col_name_upper = column_name_in_styled_df.upper()

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
            if 'BUY' in val_upper or 'BULLISH' in val_upper or 'GOLDEN' in val_upper:
                color_css = 'color: green'; font_weight_css = 'font-weight: bold'
            elif 'SELL' in val_upper or 'BEARISH' in val_upper or 'DEATH' in val_upper:
                color_css = 'color: red'; font_weight_css = 'font-weight: bold'
            elif 'WAIT' in val_upper or 'NEUTRAL' in val_upper or 'NONE' in val_upper or 'NO BREAK' in val_upper or 'MID' in val_upper or 'N/A' in val_upper or 'ERROR' in val_upper:
                color_css = 'color: gray' # N/A and Error will also be gray
    
    final_style = []
    if color_css: final_style.append(color_css)
    if font_weight_css: final_style.append(font_weight_css)
    return '; '.join(final_style) if final_style else None

# --- User Interface ---
st.set_page_config(layout="wide", page_title="Trading Indicators Dashboard")
st.title("🔥📊 Trading Indicators Dashboard")
st.caption(f"Version: 0.2.0 | Date: {datetime.now().strftime('%Y-%m-%d')}")

df_for_display = get_processed_data() # Changed function name

# Rename columns for the final display (table headers)
# Ensure this map uses the exact column names present in the DataFrame returned by get_processed_data()
rename_map_for_display_headers = {
    'Current Price ($)': 'Price ($)', # This name comes from get_fictional_data
    'Awesome Osc.': 'AO', 'StochRSI %K': 'SRSI %K', 'MACD Signal': 'MACD', 'Stoch %K': 'Stoch K',
    'ADX (14)': 'ADX', 'BBands Pos.': 'BB Pos.', 'OBV Signal': 'OBV', 'ATR Signal': 'ATR',
    'EMA (20) vs Price': 'EMA20/P', 'SMA (50/200)': 'SMA50/200', 
    'VWAP vs Price': 'VWAP/P',
    'MA Cross': 'MA Cross', 'RSI Div.': 'RSI Div', 'MACD Div.': 'MACD Div', 'Vol. Breakout': 'Vol Break'
}
# Create a new DataFrame for display to avoid modifying the one used for styling logic if names differ greatly
df_display_renamed = df_for_display.copy()
df_display_renamed.rename(columns=rename_map_for_display_headers, inplace=True)


formatters = {}
for col_header in df_display_renamed.columns: # Use columns from the renamed df
    if "%" in col_header:
         formatters[col_header] = lambda x: f"{x:+.1f}%" if isinstance(x, (int, float)) else x
    elif col_header == 'Price ($)':
        formatters[col_header] = "${:,.2f}"

styled_df = df_display_renamed.style # Style the renamed DataFrame

for col_name_in_styled_df in df_display_renamed.columns: # Iterate over renamed columns
    styled_df = styled_df.apply(
        lambda series: series.map(lambda val: apply_cell_styles(val, column_name_in_styled_df=series.name)),
        subset=[col_name_in_styled_df]
    )
styled_df = styled_df.format(formatters)
styled_df = styled_df.set_properties(**{'text-align': 'center'}, subset=df_display_renamed.columns.drop(['Asset Name', 'Price ($)']))
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
# (As in version 0.1.9)
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
- **SMA50/200**: *This now refers to general price relation to these long-term MAs, MA Cross column covers the crossover event.* Signals: <span style='color:green; font-weight:bold;'>BUY</span> (e.g. Price > SMA50/200 in uptrend context), <span style='color:red; font-weight:bold;'>SELL</span> (e.g. Price < SMA50/200 in downtrend context), <span style='color:gray;'>WAIT</span>.
- **VWAP/P**: <span style='color:green; font-weight:bold;'>BUY</span> P > VWAP, <span style='color:red; font-weight:bold;'>SELL</span> P < VWAP, <span style='color:gray;'>WAIT</span>.
""", unsafe_allow_html=True)

# --- Error Logs Section ---
st.subheader("⚠️ Error Logs")
st.markdown("---")
error_count = len(st.session_state.error_logs)
expander_title = f"Show/Hide Error Logs ({error_count} {'error' if error_count == 1 else 'errors'})"
with st.expander(expander_title, expanded=error_count > 0):
    if error_count > 0:
        for i, log_entry in enumerate(reversed(st.session_state.error_logs)):
            st.markdown(f"**Log #{error_count - i}:**\n{log_entry}", unsafe_allow_html=True)
            if i < error_count - 1: st.markdown("---")
    else:
        st.info("No errors recorded so far.")
    if st.button("Simulate Error   "): # Added more space
        try: 1 / 0
        except Exception as e_sim: log_error("This is a simulated test error.", asset_ticker="SIM_TEST", function_name="simulate_error_button", e=e_sim)
        st.rerun()
    if error_count > 0 and st.button("Clear Error Logs   "): # Added more space
        st.session_state.error_logs = []
        st.rerun()

st.markdown("---")
st.caption(f"File: app.py | Version: 0.2.0 | Last Modified: {datetime.now().strftime('%Y-%m-%d')}")

# FILE_FOOTER_START
# End of file: app.py
# Version: 0.2.0
# Last Modified: 2024-03-21
# FILE_FOOTER_END
