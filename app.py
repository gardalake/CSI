# FILE_VERSION_START
# Project: CryptoAndStocksIndicators
# File: app.py
# Version: 0.2.0
# Date: 2024-03-21
# Author: [Your Name/Nickname]
# Description: Main Streamlit application. Imports data and UI utilities.
# FILE_VERSION_END

import streamlit as st
import pandas as pd
from datetime import datetime
import traceback

# Import from our new modules
try:
    from config import COLS_TO_DISPLAY_ORDER_ORIGINAL_NAMES, RENAME_MAP_FOR_DISPLAY_HEADERS
    from data_processing import get_processed_data_with_real_aapl_rsi, log_error_from_data_processing # Using the specific log func for now
    from ui_utils import apply_cell_styles_for_display
except ImportError as e:
    st.error(f"Failed to import necessary modules. Please ensure config.py, data_processing.py, and ui_utils.py are in the same directory. Error: {e}")
    st.stop()


# --- Initial Setup and Session State for Error Logs ---
if 'error_logs' not in st.session_state:
    st.session_state.error_logs = []

# Re-define log_error here to use st.session_state, or pass st.session_state to data_processing
# For simplicity here, data_processing.log_error_from_data_processing will handle its own logging
# if called from within data_processing.py. If app.py needs to log, it can use its own instance.
def log_error_app(message, asset_ticker=None, function_name=None, e=None):
    """App-specific error logger that uses st.session_state."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"**Timestamp:** {timestamp}"
    if function_name: log_entry += f" | **Function:** `{function_name}`"
    if asset_ticker: log_entry += f" | **Asset:** `{asset_ticker}`"
    log_entry += f" | **Error:** {message}"
    if e:
        tb_str = traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)
        log_entry += f"\n**Traceback Snippet:**\n```\n{''.join(tb_str[-2:])}\n```"
    st.session_state.error_logs.append(log_entry)


# --- User Interface ---
st.set_page_config(layout="wide", page_title="Trading Indicators Dashboard")
st.title("🔥📊 Trading Indicators Dashboard")
st.caption(f"Version: 0.2.0 | Date: {datetime.now().strftime('%Y-%m-%d')}")

# Get data (potentially with real AAPL RSI)
try:
    df_processed_data = get_processed_data_with_real_aapl_rsi()
except Exception as e_data:
    log_error_app("Critical error in get_processed_data_with_real_aapl_rsi.", function_name="main_app_flow", e=e_data)
    st.error("Could not load data. Please check the error logs.")
    st.stop()


# Select and rename columns for display
if not df_processed_data.empty:
    # Ensure all columns in COLS_TO_DISPLAY_ORDER_ORIGINAL_NAMES exist in df_processed_data
    missing_cols = [col for col in COLS_TO_DISPLAY_ORDER_ORIGINAL_NAMES if col not in df_processed_data.columns]
    if missing_cols:
        log_error_app(f"Columns missing from processed data: {missing_cols}", function_name="main_app_flow_column_selection")
        st.error(f"Data processing error: columns {missing_cols} are missing. Displaying available data.")
        # Attempt to display with available columns, or stop
        available_cols_for_display = [col for col in COLS_TO_DISPLAY_ORDER_ORIGINAL_NAMES if col in df_processed_data.columns]
        if not available_cols_for_display:
            st.error("No displayable columns found after data processing errors.")
            st.stop()
        df_for_styling = df_processed_data[available_cols_for_display].copy()
    else:
        df_for_styling = df_processed_data[COLS_TO_DISPLAY_ORDER_ORIGINAL_NAMES].copy()

    df_for_styling.rename(columns=RENAME_MAP_FOR_DISPLAY_HEADERS, inplace=True)
else:
    st.warning("No data to display after processing.")
    st.stop()


# Define text formatters
formatters = {}
for col_header in df_for_styling.columns:
    if "%" in col_header:
         formatters[col_header] = lambda x: f"{x:+.1f}%" if isinstance(x, (int, float)) else x
    elif col_header == 'Price ($)':
        formatters[col_header] = "${:,.2f}"

# Apply Styler
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
# (Legend content remains the same as in v0.1.9, ensure it's all in English)
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
with st.expander(expander_title, expanded=error_count > 0):
    if error_count > 0:
        for i, log_entry in enumerate(reversed(st.session_state.error_logs)):
            st.markdown(f"**Log #{error_count - i}:**\n{log_entry}", unsafe_allow_html=True)
            if i < error_count - 1: st.markdown("---")
    else:
        st.info("No errors recorded so far.")
    if st.button("Simulate App Error"): # Differentiated button name
        try: 1 / 0
        except Exception as e_sim: log_error_app("This is a simulated app error.", asset_ticker="APP_SIM", function_name="simulate_app_error_button", e=e_sim)
        st.rerun()
    if error_count > 0 and st.button("Clear All Error Logs"): # Differentiated button name
        st.session_state.error_logs = []
        st.rerun()

st.markdown("---")
st.caption(f"File: app.py | Version: 0.2.0 | Last Modified: {datetime.now().strftime('%Y-%m-%d')}")


# FILE_FOOTER_START
# End of file: app.py
# Version: 0.2.0
# Last Modified: 2024-03-21
# FILE_FOOTER_END
