# FILE_VERSION_START
# Project: CryptoAndStocksIndicators
# File: app.py
# Version: 0.0.6
# Date: 2024-03-17
# Author: [Il Tuo Nome/Nickname]
# Description: Correzione KeyError dovuto all'ordine di rename e selezione colonne.
# FILE_VERSION_END

import streamlit as st
import pandas as pd
from datetime import datetime

# --- Configurazione Iniziale e Stato Sessione per Error Logs ---
if 'error_logs' not in st.session_state:
    st.session_state.error_logs = []

# --- Funzioni Helper ---
def get_fictional_data():
    """
    Genera dati fittizi per la tabella.
    """
    # Nomi di colonna originali e lunghi qui
    data = [
        {'Nome Asset': 'Microsoft Corp.', 'Ticker': 'MSFT', 'Prezzo Attuale ($)': 420.55, 'Var. 1H (%)': 0.1, 'Var. 12H (%)': 0.5, 'Var. 24H (%)': 0.2, 'Var. 1W (%)': 1.5,
         'AI Signal': '🔥 Strong Buy',
         'RSI (14)': 'Wait', 'StochRSI %K': 'Buy', 'MACD Signal': 'Buy', 'Stoch %K': 'Wait', 'Awesome Osc.': 'Buy', 'ADX (14)': 'Trend (28)', 'BBands Pos.': 'Mid',
         'EMA (20) vs Prezzo': 'Buy', 'SMA (50/200)': 'Buy', 'VWAP vs Prezzo': 'Buy'},
        {'Nome Asset': 'Apple Inc.', 'Ticker': 'AAPL', 'Prezzo Attuale ($)': 170.34, 'Var. 1H (%)': -0.2, 'Var. 12H (%)': -0.8, 'Var. 24H (%)': -0.5, 'Var. 1W (%)': -2.0,
         'AI Signal': 'Sell',
         'RSI (14)': 'Sell', 'StochRSI %K': 'Sell', 'MACD Signal': 'Sell', 'Stoch %K': 'Sell', 'Awesome Osc.': 'Sell', 'ADX (14)': 'Weak (18)', 'BBands Pos.': 'Upper',
         'EMA (20) vs Prezzo': 'Sell', 'SMA (50/200)': 'Wait', 'VWAP vs Prezzo': 'Sell'},
        {'Nome Asset': 'NVIDIA Corp.', 'Ticker': 'NVDA', 'Prezzo Attuale ($)': 880.27, 'Var. 1H (%)': 0.5, 'Var. 12H (%)': 1.2, 'Var. 24H (%)': 2.1, 'Var. 1W (%)': 5.3,
         'AI Signal': '🔥 Strong Buy',
         'RSI (14)': 'Buy', 'StochRSI %K': 'Buy', 'MACD Signal': 'Buy', 'Stoch %K': 'Buy', 'Awesome Osc.': 'Buy', 'ADX (14)': 'Strong (35)', 'BBands Pos.': 'Upper',
         'EMA (20) vs Prezzo': 'Buy', 'SMA (50/200)': 'Buy', 'VWAP vs Prezzo': 'Buy'},
        {'Nome Asset': 'Alphabet Inc.', 'Ticker': 'GOOGL', 'Prezzo Attuale ($)': 140.10, 'Var. 1H (%)': 0.0, 'Var. 12H (%)': 0.1, 'Var. 24H (%)': 0.7, 'Var. 1W (%)': 0.5,
         'AI Signal': 'Neutral',
         'RSI (14)': 'Wait', 'StochRSI %K': 'Wait', 'MACD Signal': 'Wait', 'Stoch %K': 'Wait', 'Awesome Osc.': 'Wait', 'ADX (14)': 'No Trend (15)', 'BBands Pos.': 'Mid',
         'EMA (20) vs Prezzo': 'Wait', 'SMA (50/200)': 'Buy', 'VWAP vs Prezzo': 'Wait'},
        {'Nome Asset': 'Amazon.com Inc.', 'Ticker': 'AMZN', 'Prezzo Attuale ($)': 175.80, 'Var. 1H (%)': -0.3, 'Var. 12H (%)': -0.5, 'Var. 24H (%)': -1.0, 'Var. 1W (%)': -1.2,
         'AI Signal': 'Strong Sell',
         'RSI (14)': 'Sell', 'StochRSI %K': 'Sell', 'MACD Signal': 'Sell', 'Stoch %K': 'Sell', 'Awesome Osc.': 'Sell', 'ADX (14)': 'Trend (26)', 'BBands Pos.': 'Lower',
         'EMA (20) vs Prezzo': 'Sell', 'SMA (50/200)': 'Wait', 'VWAP vs Prezzo': 'Sell'},
        {'Nome Asset': 'Bitcoin', 'Ticker': 'BTC', 'Prezzo Attuale ($)': 68500.50, 'Var. 1H (%)': 0.8, 'Var. 12H (%)': 2.0, 'Var. 24H (%)': 1.5, 'Var. 1W (%)': 3.0,
         'AI Signal': 'Buy',
         'RSI (14)': 'Buy', 'StochRSI %K': 'Wait', 'MACD Signal': 'Buy', 'Stoch %K': 'Wait', 'Awesome Osc.': 'Buy', 'ADX (14)': 'Strong (40)', 'BBands Pos.': 'Mid',
         'EMA (20) vs Prezzo': 'Buy', 'SMA (50/200)': 'Buy', 'VWAP vs Prezzo': 'Buy'},
        {'Nome Asset': 'Meta Platforms', 'Ticker': 'META', 'Prezzo Attuale ($)': 480.12, 'Var. 1H (%)': -0.1, 'Var. 12H (%)': 0.0, 'Var. 24H (%)': -0.8, 'Var. 1W (%)': 0.2,
         'AI Signal': 'Neutral',
         'RSI (14)': 'Wait', 'StochRSI %K': 'Sell', 'MACD Signal': 'Wait', 'Stoch %K': 'Sell', 'Awesome Osc.': 'Wait', 'ADX (14)': 'Weak (19)', 'BBands Pos.': 'Mid',
         'EMA (20) vs Prezzo': 'Wait', 'SMA (50/200)': 'Wait', 'VWAP vs Prezzo': 'Sell'},
        {'Nome Asset': 'Ethereum', 'Ticker': 'ETH', 'Prezzo Attuale ($)': 3750.00, 'Var. 1H (%)': 0.3, 'Var. 12H (%)': 1.0, 'Var. 24H (%)': 0.8, 'Var. 1W (%)': 2.5,
         'AI Signal': 'Buy',
         'RSI (14)': 'Wait', 'StochRSI %K': 'Buy', 'MACD Signal': 'Buy', 'Stoch %K': 'Buy', 'Awesome Osc.': 'Buy', 'ADX (14)': 'Trend (30)', 'BBands Pos.': 'Upper',
         'EMA (20) vs Prezzo': 'Buy', 'SMA (50/200)': 'Buy', 'VWAP vs Prezzo': 'Buy'},
        {'Nome Asset': 'UltraPro QQQ', 'Ticker': 'TQQQ', 'Prezzo Attuale ($)': 55.60, 'Var. 1H (%)': 0.4, 'Var. 12H (%)': 1.1, 'Var. 24H (%)': 1.5, 'Var. 1W (%)': 4.0,
         'AI Signal': '🔥 Strong Buy',
         'RSI (14)': 'Buy', 'StochRSI %K': 'Buy', 'MACD Signal': 'Buy', 'Stoch %K': 'Buy', 'Awesome Osc.': 'Buy', 'ADX (14)': 'Strong (38)', 'BBands Pos.': 'Upper',
         'EMA (20) vs Prezzo': 'Buy', 'SMA (50/200)': 'Buy', 'VWAP vs Prezzo': 'Buy'},
        {'Nome Asset': 'Tesla, Inc.', 'Ticker': 'TSLA', 'Prezzo Attuale ($)': 177.45, 'Var. 1H (%)': -0.7, 'Var. 12H (%)': -1.5, 'Var. 24H (%)': -3.0, 'Var. 1W (%)': -6.5,
         'AI Signal': 'Strong Sell',
         'RSI (14)': 'Sell', 'StochRSI %K': 'Sell', 'MACD Signal': 'Sell', 'Stoch %K': 'Sell', 'Awesome Osc.': 'Sell', 'ADX (14)': 'Strong (42)', 'BBands Pos.': 'Lower',
         'EMA (20) vs Prezzo': 'Sell', 'SMA (50/200)': 'Sell', 'VWAP vs Prezzo': 'Sell'},
        {'Nome Asset': 'IonQ Inc.', 'Ticker': 'IONQ', 'Prezzo Attuale ($)': 10.30, 'Var. 1H (%)': 0.0, 'Var. 12H (%)': -0.2, 'Var. 24H (%)': 0.1, 'Var. 1W (%)': -1.0,
         'AI Signal': 'Neutral',
         'RSI (14)': 'Wait', 'StochRSI %K': 'Wait', 'MACD Signal': 'Wait', 'Stoch %K': 'Wait', 'Awesome Osc.': 'Wait', 'ADX (14)': 'No Trend (12)', 'BBands Pos.': 'Mid',
         'EMA (20) vs Prezzo': 'Wait', 'SMA (50/200)': 'Wait', 'VWAP vs Prezzo': 'Wait'},
        {'Nome Asset': 'Volatil ST Fut', 'Ticker': 'UVXY', 'Prezzo Attuale ($)': 8.50, 'Var. 1H (%)': 1.0, 'Var. 12H (%)': 2.5, 'Var. 24H (%)': 5.1, 'Var. 1W (%)': 10.0,
         'AI Signal': 'Buy',
         'RSI (14)': 'Sell', 'StochRSI %K': 'Sell', 'MACD Signal': 'Buy', 'Stoch %K': 'Sell', 'Awesome Osc.': 'Buy', 'ADX (14)': 'Trend (25)', 'BBands Pos.': 'Upper',
         'EMA (20) vs Prezzo': 'Buy', 'SMA (50/200)': 'Wait', 'VWAP vs Prezzo': 'Buy'},
        {'Nome Asset': 'Rigetti Comp.', 'Ticker': 'RGTI', 'Prezzo Attuale ($)': 1.52, 'Var. 1H (%)': -0.5, 'Var. 12H (%)': -1.0, 'Var. 24H (%)': -1.2, 'Var. 1W (%)': -3.5,
         'AI Signal': 'Sell',
         'RSI (14)': 'Buy', 'StochRSI %K': 'Buy', 'MACD Signal': 'Sell', 'Stoch %K': 'Buy', 'Awesome Osc.': 'Sell', 'ADX (14)': 'Weak (17)', 'BBands Pos.': 'Lower',
         'EMA (20) vs Prezzo': 'Sell', 'SMA (50/200)': 'Sell', 'VWAP vs Prezzo': 'Sell'},
    ]
    df = pd.DataFrame(data)
    return df

def style_signals_and_variations(val, column_name=""):
    color = 'inherit'
    font_weight = 'normal'
    text_to_display = val

    if isinstance(val, str):
        if "AI Signal" in column_name:
            if 'Strong Buy' in val: color = 'darkgreen'; font_weight = 'bold'
            elif 'Buy' in val: color = 'green'; font_weight = 'bold'
            elif 'Strong Sell' in val: color = 'darkred'; font_weight = 'bold'
            elif 'Sell' in val: color = 'red'; font_weight = 'bold'
            elif 'Neutral' in val: color = 'gray'
        else: # Per altri indicatori testuali
            if 'Buy' in val.capitalize(): color = 'green'; font_weight = 'bold'
            elif 'Sell' in val.capitalize(): color = 'red'; font_weight = 'bold'
            elif 'Wait' in val.capitalize() or 'Mid' in val.capitalize() or 'Neutral' in val.capitalize(): color = 'gray'
            elif 'Strong' in val: color = 'blue'; font_weight = 'bold'
            elif 'Trend' in val: color = 'orange'
            elif 'Weak' in val or 'No Trend' in val: color = 'purple'
            elif 'Upper' in val: color = 'red'
            elif 'Lower' in val: color = 'green'
    elif isinstance(val, (int, float)):
        if val > 0: color = 'green'; text_to_display = f"+{val:.1f}%"
        elif val < 0: color = 'red'; text_to_display = f"{val:.1f}%"
        else: color = 'gray'; text_to_display = f"{val:.1f}%"
    return f'color: {color}; font-weight: {font_weight};'


# --- Interfaccia Utente Streamlit ---
st.set_page_config(layout="wide", page_title="Indicatori Trading Dashboard")
st.title("🔥📊 Dashboard Indicatori Crypto & Stocks")
st.caption(f"Versione: 0.0.6 | Data: {datetime.now().strftime('%Y-%m-%d')}")

df_data_raw = get_fictional_data()

# 1. Definisci l'ordine delle colonne usando i NOMI ORIGINALI (lunghi)
original_info_cols = ['Nome Asset', 'Ticker']
original_price_col = ['Prezzo Attuale ($)'] # Nome originale
original_var_cols = ['Var. 1H (%)', 'Var. 12H (%)', 'Var. 24H (%)', 'Var. 1W (%)']
original_ai_signal_col = ['AI Signal']
original_oscillator_cols = ['RSI (14)', 'StochRSI %K', 'MACD Signal', 'Stoch %K', 'Awesome Osc.']
original_trend_strength_vol_cols = ['ADX (14)', 'BBands Pos.']
original_ma_cols = ['EMA (20) vs Prezzo', 'SMA (50/200)', 'VWAP vs Prezzo']

display_columns_original_order = original_info_cols + original_price_col + original_var_cols + original_ai_signal_col + \
                                 original_oscillator_cols + original_trend_strength_vol_cols + original_ma_cols

# 2. Crea df_display selezionando le colonne con i nomi originali
df_display = df_data_raw[display_columns_original_order].copy() # Aggiunto .copy() per evitare SettingWithCopyWarning

# 3. RINOMINA le colonne in df_display
df_display.rename(columns={
    'Prezzo Attuale ($)': 'Prezzo ($)', # Chiave: nome vecchio, Valore: nome nuovo
    'Awesome Osc.': 'AO',
    'StochRSI %K': 'SRSI %K',
    'MACD Signal': 'MACD',
    'Stoch %K': 'Stoch K',
    'ADX (14)': 'ADX',
    'BBands Pos.': 'BB Pos.',
    'EMA (20) vs Prezzo': 'EMA20/P',
    'SMA (50/200)': 'SMA50/200',
    'VWAP vs Prezzo': 'VWAP/P'
}, inplace=True)

# 4. Definisci le liste di colonne per lo STYLING usando i NUOVI NOMI (quelli rinominati)
renamed_price_col = ['Prezzo ($)'] # Nomi rinominati
renamed_var_cols = ['Var. 1H (%)', 'Var. 12H (%)', 'Var. 24H (%)', 'Var. 1W (%)'] # Questi non sono stati rinominati, ma è bene essere espliciti
renamed_ai_signal_col = ['AI Signal'] # Non rinominato
renamed_oscillator_cols = ['RSI (14)', 'SRSI %K', 'MACD', 'Stoch K', 'AO']
renamed_trend_strength_vol_cols = ['ADX', 'BB Pos.']
renamed_ma_cols = ['EMA20/P', 'SMA50/200', 'VWAP/P']

all_individual_indicator_cols_renamed = renamed_oscillator_cols + renamed_trend_strength_vol_cols + renamed_ma_cols
all_styled_cols_renamed = renamed_var_cols + renamed_ai_signal_col + all_individual_indicator_cols_renamed

# Formattatori
formatters = {}
formatters[renamed_price_col[0]] = "${:,.2f}"

# Applica lo styling usando i nomi rinominati nelle liste per `subset`
styled_df = df_display.style
for col_name in df_display.columns: # Itera sulle colonne di df_display (che ora hanno nomi brevi)
    if col_name in all_styled_cols_renamed: # Controlla se la colonna (con nome breve) è da stilare
        styled_df = styled_df.apply(lambda series: series.apply(style_signals_and_variations, column_name=col_name), subset=[col_name])

styled_df = styled_df.format(formatters) \
    .set_properties(**{'text-align': 'center'}, subset=all_styled_cols_renamed + ['Ticker']) \
    .set_properties(**{'text-align': 'right'}, subset=renamed_price_col) \
    .set_properties(**{'text-align': 'left'}, subset=['Nome Asset']) \
    .set_table_styles([
        {'selector': 'th', 'props': [('text-align', 'center'), ('background-color', '#f0f2f6'), ('padding', '0.2rem'), ('font-size', '0.85em')]},
        {'selector': 'td', 'props': [('padding', '0.2rem 0.3rem'), ('font-size', '0.85em')]},
    ])

st.markdown("#### Segnali Tecnici Aggregati e Individuali")
st.dataframe(styled_df, use_container_width=True, hide_index=True)


# --- Legenda Indicatori ---
# (Legenda rimane invariata rispetto alla v0.0.5, ma assicurati che i nomi degli indicatori nella legenda
# corrispondano a quelli visualizzati nella tabella, cioè i nomi abbreviati)
st.subheader("📜 Legenda Indicatori")
st.markdown("---")

st.markdown("""
**AI Signal (Segnale Aggregato)**
- <span style='color:darkgreen; font-weight:bold;'>🔥 Strong Buy</span>, <span style='color:green; font-weight:bold;'>Buy</span>, <span style='color:gray;'>Neutral</span>, <span style='color:red; font-weight:bold;'>Sell</span>, <span style='color:darkred; font-weight:bold;'>Strong Sell</span>
- *Obiettivo:* Fornire una valutazione rapida e di alto livello basata sull'analisi combinata degli indicatori. *Non una garanzia di risultati.*
""", unsafe_allow_html=True)

st.markdown("#### Variazioni Prezzo")
st.markdown("""
- **Var. 1H, 12H, 24H, 1W (%)**: Variazione percentuale del prezzo. Verde per positivo, Rosso per negativo.
""", unsafe_allow_html=True)

st.markdown("#### O S C I L L A T O R S")
st.markdown("""
**RSI (14)**: Relative Strength Index. Segnali base: <30 <span style='color:green; font-weight:bold;'>BUY</span>, >70 <span style='color:red; font-weight:bold;'>SELL</span>.
**SRSI %K**: Stochastic RSI. Segnali base (%K): <20 <span style='color:green; font-weight:bold;'>BUY</span>, >80 <span style='color:red; font-weight:bold;'>SELL</span>.
**MACD**: MACD Signal Crossover. <span style='color:green; font-weight:bold;'>BUY</span> MACD sopra Segnale, <span style='color:red; font-weight:bold;'>SELL</span> MACD sotto Segnale.
**Stoch K**: Stochastic Oscillator %K. Segnali base (%K): <20 <span style='color:green; font-weight:bold;'>BUY</span>, >80 <span style='color:red; font-weight:bold;'>SELL</span>.
**AO**: Awesome Oscillator. <span style='color:green; font-weight:bold;'>BUY</span> sopra zero, <span style='color:red; font-weight:bold;'>SELL</span> sotto zero (semplificato).
""", unsafe_allow_html=True)

st.markdown("#### TREND & VOLATILITÀ")
st.markdown("""
**ADX**: Average Directional Index. Forza trend: <span style='color:purple;'>No/Weak</span>, <span style='color:orange;'>Trend</span>, <span style='color:blue; font-weight:bold;'>Strong</span>.
**BB Pos.**: Posizione Prezzo nelle Bande di Bollinger. <span style='color:green;'>Lower</span>, <span style='color:gray;'>Mid</span>, <span style='color:red;'>Upper</span>.
""", unsafe_allow_html=True)

st.markdown("#### M O V I N G   A V E R A G E S") # Rinominati EMA20/P, SMA50/200, VWAP/P
st.markdown("""
**EMA20/P**: Prezzo vs EMA (20). <span style='color:green; font-weight:bold;'>BUY</span> P > EMA, <span style='color:red; font-weight:bold;'>SELL</span> P < EMA.
**SMA50/200**: SMA Crossover (50/200). <span style='color:green; font-weight:bold;'>BUY</span> Golden Cross, <span style='color:red; font-weight:bold;'>SELL</span> Death Cross.
**VWAP/P**: Prezzo vs VWAP. <span style='color:green; font-weight:bold;'>BUY</span> P > VWAP, <span style='color:red; font-weight:bold;'>SELL</span> P < VWAP.
""", unsafe_allow_html=True)


# --- Sezione Error Logs ---
st.subheader("⚠️ Error Logs")
st.markdown("---")
with st.expander("Mostra/Nascondi Error Logs", expanded=False):
    if 'error_logs' in st.session_state and st.session_state.error_logs:
        for i, log_entry in enumerate(reversed(st.session_state.error_logs)):
            st.error(f"{len(st.session_state.error_logs) - i}. {log_entry}")
    else:
        st.info("Nessun errore registrato finora.")

    if st.button("Simula Errore"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        asset_involved = "TEST_ASSET"; function_name = "test_function"; error_message = "Questo è un errore di test simulato."
        log_entry_content = f"[{timestamp}] Asset: {asset_involved} | Funzione: {function_name} | Errore: {error_message}"
        st.session_state.error_logs.append(log_entry_content)
        st.rerun()

    if st.button("Clear Error Logs"):
        st.session_state.error_logs = []
        st.rerun()

st.markdown("---")
st.caption(f"File: app.py | Versione: 0.0.6 | Ultima Modifica: {datetime.now().strftime('%Y-%m-%d')}")

# FILE_FOOTER_START
# End of file: app.py
# Version: 0.0.6
# Last Modified: 2024-03-17
# FILE_FOOTER_END
