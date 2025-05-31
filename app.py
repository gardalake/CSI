# FILE_VERSION_START
# Project: CryptoAndStocksIndicators
# File: app.py
# Version: 0.1.7
# Date: 2024-03-20
# Author: [Your Name/Nickname]
# Description: Removed TradingView URL, full English translation, improved error logs.
# FILE_VERSION_END

import streamlit as st
import pandas as pd
from datetime import datetime
import traceback # For more detailed error logging

# --- Initial Setup and Session State for Error Logs ---
if 'error_logs' not in st.session_state:
    st.session_state.error_logs = []

# --- Helper Functions ---
def get_fictional_data():
    """
    Generates fictional data for the table.
    All assets from the original list are included.
    """
    data = [
        # Crypto (sorted by fictional Crypto Rank)
        {'Asset Type': 'Crypto', 'Crypto Rank': 1, 'Market Cap': 1.35e12, 'Asset Name': 'Bitcoin', 'Ticker': 'BTC', 'Current Price ($)': 68500.50, 'Var. 1H (%)': 0.8, 'Var. 12H (%)': 2.0, 'Var. 24H (%)': 1.5, 'Var. 1W (%)': 3.0,
         'AI Signal': 'Buy', 'OBV Signal': 'Buy', 'ATR Signal': 'Buy',
         'RSI (14)': 'Buy', 'StochRSI %K': 'Wait', 'MACD Signal': 'Buy', 'Stoch %K': 'Wait', 'Awesome Osc.': 'Buy', 'ADX (14)': 'Strong (40)', 'BBands Pos.': 'Mid',
         'EMA (20) vs Price': 'Buy', 'SMA (50/200)': 'Buy', 'VWAP vs Price': 'Buy'},
        {'Asset Type': 'Crypto', 'Crypto Rank': 2, 'Market Cap': 4.50e11, 'Asset Name': 'Ethereum', 'Ticker': 'ETH', 'Current Price ($)': 3750.00, 'Var. 1H (%)': -0.3, 'Var. 12H (%)': 1.0, 'Var. 24H (%)': 0.8, 'Var. 1W (%)': 2.5,
         'AI Signal': 'Buy', 'OBV Signal': 'Wait', 'ATR Signal': 'Wait',
         'RSI (14)': 'Wait', 'StochRSI %K': 'Buy', 'MACD Signal': 'Buy', 'Stoch %K': 'Buy', 'Awesome Osc.': 'Buy', 'ADX (14)': 'Trend (30)', 'BBands Pos.': 'Upper',
         'EMA (20) vs Price': 'Buy', 'SMA (50/200)': 'Buy', 'VWAP vs Price': 'Buy'},

        # Stocks & ETFs (sorted by fictional Market Cap descending)
        {'Asset Type': 'Stock', 'Crypto Rank': None, 'Market Cap': 3.12e12, 'Asset Name': 'Microsoft Corp.', 'Ticker': 'MSFT', 'Current Price ($)': 420.55, 'Var. 1H (%)': 0.1, 'Var. 12H (%)': 0.5, 'Var. 24H (%)': 0.2, 'Var. 1W (%)': 1.5,
         'AI Signal': '🔥 Strong Buy', 'OBV Signal': 'Buy', 'ATR Signal': 'Buy',
         'RSI (14)': 'Wait', 'StochRSI %K': 'Buy', 'MACD Signal': 'Buy', 'Stoch %K': 'Wait', 'Awesome Osc.': 'Buy', 'ADX (14)': 'Trend (28)', 'BBands Pos.': 'Mid',
         'EMA (20) vs Price': 'Buy', 'SMA (50/200)': 'Buy', 'VWAP vs Price': 'Buy'},
        {'Asset Type': 'Stock', 'Crypto Rank': None, 'Market Cap': 2.63e12, 'Asset Name': 'Apple Inc.', 'Ticker': 'AAPL', 'Current Price ($)': 170.34, 'Var. 1H (%)': -0.2, 'Var. 12H (%)': -0.8, 'Var. 24H (%)': -0.5, 'Var. 1W (%)': -2.0,
         'AI Signal': 'Sell', 'OBV Signal': 'Sell', 'ATR Signal': 'Sell',
         'RSI (14)': 'Sell', 'StochRSI %K': 'Sell', 'MACD Signal': 'Sell', 'Stoch %K': 'Sell', 'Awesome Osc.': 'Sell', 'ADX (14)': 'Weak (18)', 'BBands Pos.': 'Upper',
         'EMA (20) vs Price': 'Sell', 'SMA (50/200)': 'Wait', 'VWAP vs Price': 'Sell'},
        {'Asset Type': 'Stock', 'Crypto Rank': None, 'Market Cap': 2.20e12, 'Asset Name': 'NVIDIA Corp.', 'Ticker': 'NVDA', 'Current Price ($)': 880.27, 'Var. 1H (%)': 0.5, 'Var. 12H (%)': 1.2, 'Var. 24H (%)': 2.1, 'Var. 1W (%)': 5.3,
         'AI Signal': '🔥 Strong Buy', 'OBV Signal': 'Buy', 'ATR Signal': 'Buy',
         'RSI (14)': 'Buy', 'StochRSI %K': 'Buy', 'MACD Signal': 'Buy', 'Stoch %K': 'Buy', 'Awesome Osc.': 'Buy', 'ADX (14)': 'Strong (35)', 'BBands Pos.': 'Upper',
         'EMA (20) vs Price': 'Buy', 'SMA (50/200)': 'Buy', 'VWAP vs Price': 'Buy'},
        {'Asset Type': 'Stock', 'Crypto Rank': None, 'Market Cap': 1.82e12, 'Asset Name': 'Amazon.com Inc.', 'Ticker': 'AMZN', 'Current Price ($)': 175.80, 'Var. 1H (%)': 0.0, 'Var. 12H (%)': -0.5, 'Var. 24H (%)': -1.0, 'Var. 1W (%)': -1.2,
         'AI Signal': 'Strong Sell', 'OBV Signal': 'Sell', 'ATR Signal': 'Sell',
         'RSI (14)': 'Sell', 'StochRSI %K': 'Sell', 'MACD Signal': 'Sell', 'Stoch %K': 'Sell', 'Awesome Osc.': 'Sell', 'ADX (14)': 'Trend (26)', 'BBands Pos.': 'Lower',
         'EMA (20) vs Price': 'Sell', 'SMA (50/200)': 'Wait', 'VWAP vs Price': 'Sell'},
        {'Asset Type': 'Stock', 'Crypto Rank': None, 'Market Cap': 1.75e12, 'Asset Name': 'Alphabet Inc. (GOOGL)', 'Ticker': 'GOOGL', 'Current Price ($)': 140.10, 'Var. 1H (%)': 0.0, 'Var. 12H (%)': 0.1, 'Var. 24H (%)': 0.7, 'Var. 1W (%)': 0.5,
         'AI Signal': 'Neutral', 'OBV Signal': 'Wait', 'ATR Signal': 'Wait',
         'RSI (14)': 'Wait', 'StochRSI %K': 'Wait', 'MACD Signal': 'Wait', 'Stoch %K': 'Wait', 'Awesome Osc.': 'Wait', 'ADX (14)': 'No Trend (15)', 'BBands Pos.': 'Mid',
         'EMA (20) vs Price': 'Wait', 'SMA (50/200)': 'Buy', 'VWAP vs Price': 'Wait'},
        {'Asset Type': 'Stock', 'Crypto Rank': None, 'Market Cap': 1.22e12, 'Asset Name': 'Meta Platforms Inc.', 'Ticker': 'META', 'Current Price ($)': 480.12, 'Var. 1H (%)': -0.1, 'Var. 12H (%)': 0.0, 'Var. 24H (%)': -0.8, 'Var. 1W (%)': 0.2,
         'AI Signal': 'Neutral', 'OBV Signal': 'Wait', 'ATR Signal': 'Wait',
         'RSI (14)': 'Wait', 'StochRSI %K': 'Sell', 'MACD Signal': 'Wait', 'Stoch %K': 'Sell', 'Awesome Osc.': 'Wait', 'ADX (14)': 'Weak (19)', 'BBands Pos.': 'Mid',
         'EMA (20) vs Price': 'Wait', 'SMA (50/200)': 'Wait', 'VWAP vs Price': 'Sell'},
        {'Asset Type': 'Stock', 'Crypto Rank': None, 'Market Cap': 5.60e11, 'Asset Name': 'Tesla, Inc.', 'Ticker': 'TSLA', 'Current Price ($)': 177.45, 'Var. 1H (%)': -0.7, 'Var. 12H (%)': -1.5, 'Var. 24H (%)': -3.0, 'Var. 1W (%)': -6.5,
         'AI Signal': 'Strong Sell', 'OBV Signal': 'Sell', 'ATR Signal': 'Sell',
         'RSI (14)': 'Sell', 'StochRSI %K': 'Sell', 'MACD Signal': 'Sell', 'Stoch %K': 'Sell', 'Awesome Osc.': 'Sell', 'ADX (14)': 'Strong (42)', 'BBands Pos.': 'Lower',
         'EMA (20) vs Price': 'Sell', 'SMA (50/200)': 'Sell', 'VWAP vs Price': 'Sell'},
        {'Asset Type': 'Stock', 'Crypto Rank': None, 'Market Cap': 2.20e8, 'Asset Name': 'Rigetti Computing (GTI)', 'Ticker': 'RGTI', 'Current Price ($)': 1.52, 'Var. 1H (%)': -0.5, 'Var. 12H (%)': -1.0, 'Var. 24H (%)': -1.2, 'Var. 1W (%)': -3.5,
         'AI Signal': 'Sell', 'OBV Signal': 'Sell', 'ATR Signal': 'Wait',
         'RSI (14)': 'Buy', 'StochRSI %K': 'Buy', 'MACD Signal': 'Sell', 'Stoch %K': 'Buy', 'Awesome Osc.': 'Sell', 'ADX (14)': 'Weak (17)', 'BBands Pos.': 'Lower',
         'EMA (20) vs Price': 'Sell', 'SMA (50/200)': 'Sell', 'VWAP vs Price': 'Sell'},
        {'Asset Type': 'Stock', 'Crypto Rank': None, 'Market Cap': 2.10e9, 'Asset Name': 'IonQ Inc. (Quantum)', 'Ticker': 'IONQ', 'Current Price ($)': 10.30, 'Var. 1H (%)': 0.0, 'Var. 12H (%)': -0.2, 'Var. 24H (%)': 0.1, 'Var. 1W (%)': -1.0,
         'AI Signal': 'Neutral', 'OBV Signal': 'Wait', 'ATR Signal': 'Wait',
         'RSI (14)': 'Wait', 'StochRSI %K': 'Wait', 'MACD Signal': 'Wait', 'Stoch %K': 'Wait', 'Awesome Osc.': 'Wait', 'ADX (14)': 'No Trend (12)', 'BBands Pos.': 'Mid',
         'EMA (20) vs Price': 'Wait', 'SMA (50/200)': 'Wait', 'VWAP vs Price': 'Wait'},
        {'Asset Type': 'ETF', 'Crypto Rank': None, 'Market Cap': 5.50e8, 'Asset Name': 'ProSh Volatil ST Fut (UVXY)', 'Ticker': 'UVXY', 'Current Price ($)': 8.50, 'Var. 1H (%)': 1.0, 'Var. 12H (%)': 2.5, 'Var. 24H (%)': 5.1, 'Var. 1W (%)': 10.0,
         'AI Signal': 'Buy', 'OBV Signal': 'Buy', 'ATR Signal': 'Buy',
         'RSI (14)': 'Sell', 'StochRSI %K': 'Sell', 'MACD Signal': 'Buy', 'Stoch %K': 'Sell', 'Awesome Osc.': 'Buy', 'ADX (14)': 'Trend (25)', 'BBands Pos.': 'Upper',
         'EMA (20) vs Price': 'Buy', 'SMA (50/200)': 'Wait', 'VWAP vs Price': 'Buy'},
        {'Asset Type': 'ETF', 'Crypto Rank': None, 'Market Cap': 2.21e10, 'Asset Name': 'ProSh UltraPro QQQ (TQQQ)', 'Ticker': 'TQQQ', 'Current Price ($)': 55.60, 'Var. 1H (%)': 0.4, 'Var. 12H (%)': 1.1, 'Var. 24H (%)': 1.5, 'Var. 1W (%)': 4.0,
         'AI Signal': '🔥 Strong Buy', 'OBV Signal': 'Buy', 'ATR Signal': 'Buy',
         'RSI (14)': 'Buy', 'StochRSI %K': 'Buy', 'MACD Signal': 'Buy', 'Stoch %K': 'Buy', 'Awesome Osc.': 'Buy', 'ADX (14)': 'Strong (38)', 'BBands Pos.': 'Upper',
         'EMA (20) vs Price': 'Buy', 'SMA (50/200)': 'Buy', 'VWAP vs Price': 'Buy'},
    ]
    df = pd.DataFrame(data)
    asset_type_order = {'Crypto': 0, 'Stock': 1, 'ETF': 2}
    df['AssetTypeSortCol'] = df['Asset Type'].map(asset_type_order)
    df['PrimarySortKeyCol'] = df.apply(
        lambda row: row['Crypto Rank'] if row['Asset Type'] == 'Crypto' else -row['Market Cap'], 
        axis=1
    )
    df.sort_values(by=['AssetTypeSortCol', 'PrimarySortKeyCol'], ascending=[True, True], inplace=True)
    # Drop columns used only for sorting and not for display
    df.drop(columns=['Asset Type', 'Crypto Rank', 'Market Cap', 'AssetTypeSortCol', 'PrimarySortKeyCol'], inplace=True, errors='ignore')
    return df

def apply_cell_styles(val, column_name_in_styled_df=""):
    """Determines CSS color and font-weight attributes for a cell.
    column_name_in_styled_df refers to column names AFTER renaming for display.
    """
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
        elif current_col_name_upper in ['OBV', 'ATR', 'RSI (14)', 'SRSI %K', 'MACD', 'STOCH K', 'AO', 'EMA20/P', 'SMA50/200', 'VWAP/P']:
            if 'BUY' in val_upper: color_css = 'color: green'; font_weight_css = 'font-weight: bold'
            elif 'SELL' in val_upper: color_css = 'color: red'; font_weight_css = 'font-weight: bold'
            elif 'WAIT' in val_upper or 'NEUTRAL' in val_upper: color_css = 'color: gray'
    
    final_style = []
    if color_css: final_style.append(color_css)
    if font_weight_css: final_style.append(font_weight_css)
    return '; '.join(final_style) if final_style else None

def log_error(message, asset_ticker=None, function_name=None, e=None):
    """Appends a detailed error message to the session state error logs."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"**Timestamp:** {timestamp}"
    if function_name:
        log_entry += f" | **Function:** `{function_name}`"
    if asset_ticker:
        log_entry += f" | **Asset:** `{asset_ticker}`"
    log_entry += f" | **Error:** {message}"
    if e:
        # log_entry += f"\n**Details:** {str(e)}" # Basic exception string
        # For more detail, but can be very long:
        tb_str = traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)
        log_entry += f"\n**Traceback Snippet:**\n```\n{''.join(tb_str[-2:])}\n```" # Last 2 lines of traceback
    st.session_state.error_logs.append(log_entry)


# --- User Interface ---
st.set_page_config(layout="wide", page_title="Trading Indicators Dashboard") # English title
st.title("🔥📊 Trading Indicators Dashboard") # English title
st.caption(f"Version: 0.1.7 | Date: {datetime.now().strftime('%Y-%m-%d')}")

df_data_processed = get_fictional_data() # This df has original column names

# Define the order of columns as they exist in df_data_processed
# NO TradingView Link column for now
cols_to_display_order = [
    'Asset Name', 'Ticker', 'Current Price ($)',
    'Var. 1H (%)', 'Var. 12H (%)', 'Var. 24H (%)', 'Var. 1W (%)',
    'AI Signal', 'OBV Signal', 'ATR Signal',
    'RSI (14)', 'StochRSI %K', 'MACD Signal', 'Stoch %K', 'Awesome Osc.',
    'ADX (14)', 'BBands Pos.',
    'EMA (20) vs Price', 'SMA (50/200)', 'VWAP vs Price'
]
df_for_styling = df_data_processed[cols_to_display_order].copy()

# Rename columns for the final display (table headers)
rename_map_for_display_headers = {
    'Current Price ($)': 'Price ($)',
    'Awesome Osc.': 'AO', 'StochRSI %K': 'SRSI %K', 'MACD Signal': 'MACD', 'Stoch %K': 'Stoch K',
    'ADX (14)': 'ADX', 'BBands Pos.': 'BB Pos.', 'OBV Signal': 'OBV', 'ATR Signal': 'ATR',
    'EMA (20) vs Price': 'EMA20/P', 'SMA (50/200)': 'SMA50/200', 'VWAP vs Price': 'VWAP/P'
}
df_for_styling.rename(columns=rename_map_for_display_headers, inplace=True)

# Define text formatters (for %, $)
# Apply to column names as they are in df_for_styling (after renaming)
formatters = {}
for col_header in df_for_styling.columns:
    if "%" in col_header:
         formatters[col_header] = lambda x: f"{x:+.1f}%" if isinstance(x, (int, float)) else x
    elif col_header == 'Price ($)': # Renamed column
        formatters[col_header] = "${:,.2f}"

# Apply Styler
styled_df = df_for_styling.style

# Apply cell-specific color/font-weight styles
for col_name_in_styled_df in df_for_styling.columns:
    styled_df = styled_df.apply(
        lambda series: series.map(lambda val: apply_cell_styles(val, column_name_in_styled_df=series.name)),
        subset=[col_name_in_styled_df]
    )

styled_df = styled_df.format(formatters) # Apply text formatting

# Apply general table properties
styled_df = styled_df.set_properties(**{'text-align': 'center'}, subset=df_for_styling.columns.drop(['Asset Name', 'Price ($)']))
styled_df = styled_df.set_properties(**{'text-align': 'right'}, subset=['Price ($)'])
styled_df = styled_df.set_properties(**{'text-align': 'left'}, subset=['Asset Name'])
styled_df = styled_df.set_table_styles([
    {'selector': 'th', 'props': [('text-align', 'center'), ('background-color', '#f0f2f6'), ('padding', '0.2rem'), ('font-size', '0.75em')]},
    {'selector': 'td', 'props': [('padding', '0.2rem 0.3rem'), ('font-size', '0.75em')]},
])

st.markdown("#### Aggregated and Individual Technical Signals") # English
st.dataframe(styled_df, use_container_width=True, hide_index=True) # Removed unsafe_allow_html


# --- Legend ---
st.subheader("📜 Detailed Indicators and Columns Legend") # English
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
    - *Description*: Evaluates and aggregates signals from individual technical indicators.
    - *Utility*: Provides a quick, high-level assessment of trading potential. Strong consensus among indicators leads to "Strong" signals. *Note: This is a decision aid, not a guarantee of results.*
""", unsafe_allow_html=True)

st.markdown("##### Volume, Momentum & Overbought/Oversold Oscillators")
st.markdown("""
- **OBV** (On-Balance Volume Signal):
    - *Description*: Momentum indicator using volume flow to predict price changes.
    - *Base Signals*: <span style='color:green; font-weight:bold;'>BUY</span> for accumulation. <span style='color:red; font-weight:bold;'>SELL</span> for distribution. <span style='color:gray;'>WAIT</span> otherwise.
    - *Utility*: Confirms price trends or signals divergences.
- **ATR** (Average True Range Signal):
    - *Description*: Measures market volatility.
    - *Base Signals (Proposed)*: <span style='color:green; font-weight:bold;'>BUY/SELL</span> if ATR suggests high volatility breakout/breakdown potential aligned with other signals. <span style='color:gray;'>WAIT</span> if ATR is low (low volatility).
    - *Utility*: Helps assess risk and potential move magnitude. A derived ATR signal is an interpretation.
- **RSI (14)** (Relative Strength Index): Signals: <30 <span style='color:green; font-weight:bold;'>BUY</span>, >70 <span style='color:red; font-weight:bold;'>SELL</span>, 30-70 (<span style='color:gray;'>WAIT</span>).
- **SRSI %K** (Stochastic RSI %K): Signals: <20 <span style='color:green; font-weight:bold;'>BUY</span>, >80 <span style='color:red; font-weight:bold;'>SELL</span>, 20-80 (<span style='color:gray;'>WAIT</span>).
- **MACD** (MACD Crossover): Signals: <span style='color:green; font-weight:bold;'>BUY</span> MACD > Signal, <span style='color:red; font-weight:bold;'>SELL</span> MACD < Signal, <span style='color:gray;'>WAIT</span>.
- **Stoch K** (Stochastic %K): Signals: <20 <span style='color:green; font-weight:bold;'>BUY</span>, >80 <span style='color:red; font-weight:bold;'>SELL</span>, 20-80 (<span style='color:gray;'>WAIT</span>).
- **AO** (Awesome Oscillator): Signals: <span style='color:green; font-weight:bold;'>BUY</span> AO > 0, <span style='color:red; font-weight:bold;'>SELL</span> AO < 0, <span style='color:gray;'>WAIT</span>.
""", unsafe_allow_html=True)

st.markdown("##### Trend Strength & Volatility Indicators (Continued)")
st.markdown("""
- **ADX** (Average Directional Index):
    - *Interpretation*: >20 (<span style='color:green;'>Strong/Developing Trend</span>), <20 (<span style='color:gray;'>Weak/No Trend</span>). Does not indicate direction.
- **BB Pos.** (Bollinger Bands Position):
    - *Interpretation*: <span style='color:green;'>Lower</span> (near lower band), <span style='color:gray;'>Mid</span> (between bands), <span style='color:red;'>Upper</span> (near upper band).
""", unsafe_allow_html=True)

st.markdown("##### M o v i n g   A v e r a g e s") # English
st.markdown("""
- **EMA20/P** (Price vs 20-period EMA): <span style='color:green; font-weight:bold;'>BUY</span> P > EMA, <span style='color:red; font-weight:bold;'>SELL</span> P < EMA, <span style='color:gray;'>WAIT</span>.
- **SMA50/200** (SMA Crossover 50/200): <span style='color:green; font-weight:bold;'>BUY</span> Golden Cross, <span style='color:red; font-weight:bold;'>SELL</span> Death Cross, <span style='color:gray;'>WAIT</span>.
- **VWAP/P** (Price vs VWAP): <span style='color:green; font-weight:bold;'>BUY</span> P > VWAP, <span style='color:red; font-weight:bold;'>SELL</span> P < VWAP, <span style='color:gray;'>WAIT</span>.
""", unsafe_allow_html=True)


# --- Error Logs Section ---
st.subheader("⚠️ Error Logs") # English
st.markdown("---")
error_count = len(st.session_state.error_logs)
expander_title = f"Show/Hide Error Logs ({error_count} {'error' if error_count == 1 else 'errors'})"

with st.expander(expander_title, expanded=error_count > 0): # Expand if errors exist
    if error_count > 0:
        for i, log_entry in enumerate(reversed(st.session_state.error_logs)): # Show newest first
            st.markdown(f"**Log #{error_count - i}:**\n{log_entry}", unsafe_allow_html=True) # Use markdown for better formatting
            if i < error_count - 1: st.markdown("---") # Separator between logs
    else:
        st.info("No errors recorded so far.")

    # Simulate error for testing
    if st.button("Simulate Error"):
        try:
            1 / 0 # Example error
        except Exception as e_sim:
            log_error("This is a simulated test error.", asset_ticker="SIM_TEST", function_name="simulate_error_button", e=e_sim)
        st.rerun()

    if error_count > 0 and st.button("Clear Error Logs"):
        st.session_state.error_logs = []
        st.rerun()

st.markdown("---")
st.caption(f"File: app.py | Version: 0.1.7 | Last Modified: {datetime.now().strftime('%Y-%m-%d')}")

# FILE_FOOTER_START
# End of file: app.py
# Version: 0.1.7
# Last Modified: 2024-03-20
# FILE_FOOTER_END
