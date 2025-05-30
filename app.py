# FILE_VERSION_START
# Project: CryptoAndStocksIndicators
# File: app.py
# Version: 0.0.5
# Date: 2024-03-17
# Author: [Il Tuo Nome/Nickname]
# Description: Aggiunta icona fiamma, variazioni temporali, nuovi indicatori (ADX, BBands), rimozione Market Cap.
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
    data = [
        # Nome Asset, Ticker, Prezzo, Variazioni %, AI Signal, Indicatori
        {'Nome Asset': 'Microsoft Corp.', 'Ticker': 'MSFT', 'Prezzo ($)': 420.55, 'Var. 1H (%)': 0.1, 'Var. 12H (%)': 0.5, 'Var. 24H (%)': 0.2, 'Var. 1W (%)': 1.5,
         'AI Signal': '🔥 Strong Buy',
         'RSI (14)': 'Wait', 'StochRSI %K': 'Buy', 'MACD Signal': 'Buy', 'Stoch %K': 'Wait', 'Awesome Osc.': 'Buy', 'ADX (14)': 'Trend (28)', 'BBands Pos.': 'Mid',
         'EMA (20) vs P': 'Buy', 'SMA (50/200)': 'Buy', 'VWAP vs P': 'Buy'},
        {'Nome Asset': 'Apple Inc.', 'Ticker': 'AAPL', 'Prezzo ($)': 170.34, 'Var. 1H (%)': -0.2, 'Var. 12H (%)': -0.8, 'Var. 24H (%)': -0.5, 'Var. 1W (%)': -2.0,
         'AI Signal': 'Sell',
         'RSI (14)': 'Sell', 'StochRSI %K': 'Sell', 'MACD Signal': 'Sell', 'Stoch %K': 'Sell', 'Awesome Osc.': 'Sell', 'ADX (14)': 'Weak (18)', 'BBands Pos.': 'Upper',
         'EMA (20) vs P': 'Sell', 'SMA (50/200)': 'Wait', 'VWAP vs P': 'Sell'},
        {'Nome Asset': 'NVIDIA Corp.', 'Ticker': 'NVDA', 'Prezzo ($)': 880.27, 'Var. 1H (%)': 0.5, 'Var. 12H (%)': 1.2, 'Var. 24H (%)': 2.1, 'Var. 1W (%)': 5.3,
         'AI Signal': '🔥 Strong Buy',
         'RSI (14)': 'Buy', 'StochRSI %K': 'Buy', 'MACD Signal': 'Buy', 'Stoch %K': 'Buy', 'Awesome Osc.': 'Buy', 'ADX (14)': 'Strong (35)', 'BBands Pos.': 'Upper',
         'EMA (20) vs P': 'Buy', 'SMA (50/200)': 'Buy', 'VWAP vs P': 'Buy'},
        {'Nome Asset': 'Alphabet Inc.', 'Ticker': 'GOOGL', 'Prezzo ($)': 140.10, 'Var. 1H (%)': 0.0, 'Var. 12H (%)': 0.1, 'Var. 24H (%)': 0.7, 'Var. 1W (%)': 0.5,
         'AI Signal': 'Neutral',
         'RSI (14)': 'Wait', 'StochRSI %K': 'Wait', 'MACD Signal': 'Wait', 'Stoch %K': 'Wait', 'Awesome Osc.': 'Wait', 'ADX (14)': 'No Trend (15)', 'BBands Pos.': 'Mid',
         'EMA (20) vs P': 'Wait', 'SMA (50/200)': 'Buy', 'VWAP vs P': 'Wait'},
        {'Nome Asset': 'Amazon.com Inc.', 'Ticker': 'AMZN', 'Prezzo ($)': 175.80, 'Var. 1H (%)': -0.3, 'Var. 12H (%)': -0.5, 'Var. 24H (%)': -1.0, 'Var. 1W (%)': -1.2,
         'AI Signal': 'Strong Sell',
         'RSI (14)': 'Sell', 'StochRSI %K': 'Sell', 'MACD Signal': 'Sell', 'Stoch %K': 'Sell', 'Awesome Osc.': 'Sell', 'ADX (14)': 'Trend (26)', 'BBands Pos.': 'Lower',
         'EMA (20) vs P': 'Sell', 'SMA (50/200)': 'Wait', 'VWAP vs P': 'Sell'},
        {'Nome Asset': 'Bitcoin', 'Ticker': 'BTC', 'Prezzo ($)': 68500.50, 'Var. 1H (%)': 0.8, 'Var. 12H (%)': 2.0, 'Var. 24H (%)': 1.5, 'Var. 1W (%)': 3.0,
         'AI Signal': 'Buy',
         'RSI (14)': 'Buy', 'StochRSI %K': 'Wait', 'MACD Signal': 'Buy', 'Stoch %K': 'Wait', 'Awesome Osc.': 'Buy', 'ADX (14)': 'Strong (40)', 'BBands Pos.': 'Mid',
         'EMA (20) vs P': 'Buy', 'SMA (50/200)': 'Buy', 'VWAP vs P': 'Buy'},
        {'Nome Asset': 'Meta Platforms', 'Ticker': 'META', 'Prezzo ($)': 480.12, 'Var. 1H (%)': -0.1, 'Var. 12H (%)': 0.0, 'Var. 24H (%)': -0.8, 'Var. 1W (%)': 0.2,
         'AI Signal': 'Neutral',
         'RSI (14)': 'Wait', 'StochRSI %K': 'Sell', 'MACD Signal': 'Wait', 'Stoch %K': 'Sell', 'Awesome Osc.': 'Wait', 'ADX (14)': 'Weak (19)', 'BBands Pos.': 'Mid',
         'EMA (20) vs P': 'Wait', 'SMA (50/200)': 'Wait', 'VWAP vs P': 'Sell'},
        {'Nome Asset': 'Ethereum', 'Ticker': 'ETH', 'Prezzo ($)': 3750.00, 'Var. 1H (%)': 0.3, 'Var. 12H (%)': 1.0, 'Var. 24H (%)': 0.8, 'Var. 1W (%)': 2.5,
         'AI Signal': 'Buy',
         'RSI (14)': 'Wait', 'StochRSI %K': 'Buy', 'MACD Signal': 'Buy', 'Stoch %K': 'Buy', 'Awesome Osc.': 'Buy', 'ADX (14)': 'Trend (30)', 'BBands Pos.': 'Upper',
         'EMA (20) vs P': 'Buy', 'SMA (50/200)': 'Buy', 'VWAP vs P': 'Buy'},
        {'Nome Asset': 'UltraPro QQQ', 'Ticker': 'TQQQ', 'Prezzo ($)': 55.60, 'Var. 1H (%)': 0.4, 'Var. 12H (%)': 1.1, 'Var. 24H (%)': 1.5, 'Var. 1W (%)': 4.0,
         'AI Signal': '🔥 Strong Buy',
         'RSI (14)': 'Buy', 'StochRSI %K': 'Buy', 'MACD Signal': 'Buy', 'Stoch %K': 'Buy', 'Awesome Osc.': 'Buy', 'ADX (14)': 'Strong (38)', 'BBands Pos.': 'Upper',
         'EMA (20) vs P': 'Buy', 'SMA (50/200)': 'Buy', 'VWAP vs P': 'Buy'},
        {'Nome Asset': 'Tesla, Inc.', 'Ticker': 'TSLA', 'Prezzo ($)': 177.45, 'Var. 1H (%)': -0.7, 'Var. 12H (%)': -1.5, 'Var. 24H (%)': -3.0, 'Var. 1W (%)': -6.5,
         'AI Signal': 'Strong Sell',
         'RSI (14)': 'Sell', 'StochRSI %K': 'Sell', 'MACD Signal': 'Sell', 'Stoch %K': 'Sell', 'Awesome Osc.': 'Sell', 'ADX (14)': 'Strong (42)', 'BBands Pos.': 'Lower',
         'EMA (20) vs P': 'Sell', 'SMA (50/200)': 'Sell', 'VWAP vs P': 'Sell'},
        {'Nome Asset': 'IonQ Inc.', 'Ticker': 'IONQ', 'Prezzo ($)': 10.30, 'Var. 1H (%)': 0.0, 'Var. 12H (%)': -0.2, 'Var. 24H (%)': 0.1, 'Var. 1W (%)': -1.0,
         'AI Signal': 'Neutral',
         'RSI (14)': 'Wait', 'StochRSI %K': 'Wait', 'MACD Signal': 'Wait', 'Stoch %K': 'Wait', 'Awesome Osc.': 'Wait', 'ADX (14)': 'No Trend (12)', 'BBands Pos.': 'Mid',
         'EMA (20) vs P': 'Wait', 'SMA (50/200)': 'Wait', 'VWAP vs P': 'Wait'},
        {'Nome Asset': 'Volatil ST Fut', 'Ticker': 'UVXY', 'Prezzo ($)': 8.50, 'Var. 1H (%)': 1.0, 'Var. 12H (%)': 2.5, 'Var. 24H (%)': 5.1, 'Var. 1W (%)': 10.0,
         'AI Signal': 'Buy', # UVXY è complesso, l'AI potrebbe interpretarlo come 'Buy' se si aspetta volatilità
         'RSI (14)': 'Sell', 'StochRSI %K': 'Sell', 'MACD Signal': 'Buy', 'Stoch %K': 'Sell', 'Awesome Osc.': 'Buy', 'ADX (14)': 'Trend (25)', 'BBands Pos.': 'Upper',
         'EMA (20) vs P': 'Buy', 'SMA (50/200)': 'Wait', 'VWAP vs P': 'Buy'},
        {'Nome Asset': 'Rigetti Comp.', 'Ticker': 'RGTI', 'Prezzo ($)': 1.52, 'Var. 1H (%)': -0.5, 'Var. 12H (%)': -1.0, 'Var. 24H (%)': -1.2, 'Var. 1W (%)': -3.5,
         'AI Signal': 'Sell',
         'RSI (14)': 'Buy', 'StochRSI %K': 'Buy', 'MACD Signal': 'Sell', 'Stoch %K': 'Buy', 'Awesome Osc.': 'Sell', 'ADX (14)': 'Weak (17)', 'BBands Pos.': 'Lower',
         'EMA (20) vs P': 'Sell', 'SMA (50/200)': 'Sell', 'VWAP vs P': 'Sell'},
    ]
    df = pd.DataFrame(data)
    return df

def style_signals_and_variations(val, column_name=""):
    """Applica stili condizionali per segnali e variazioni percentuali."""
    color = 'inherit'
    font_weight = 'normal'
    text_to_display = val

    if isinstance(val, str): # Per segnali AI e indicatori
        if "AI Signal" in column_name: # Colonna specifica AI Signal
            if 'Strong Buy' in val:
                color = 'darkgreen'
                font_weight = 'bold'
                # text_to_display = "🔥 " + val # Aggiunge fiamma qui
            elif 'Buy' in val:
                color = 'green'
                font_weight = 'bold'
            elif 'Strong Sell' in val:
                color = 'darkred'
                font_weight = 'bold'
            elif 'Sell' in val:
                color = 'red'
                font_weight = 'bold'
            elif 'Neutral' in val:
                color = 'gray'
        else: # Per altri indicatori testuali
            if 'Buy' in val.capitalize():
                color = 'green'
                font_weight = 'bold'
            elif 'Sell' in val.capitalize():
                color = 'red'
                font_weight = 'bold'
            elif 'Wait' in val.capitalize() or 'Mid' in val.capitalize() or 'Neutral' in val.capitalize():
                color = 'gray'
            # Per ADX (esempio)
            elif 'Strong' in val: color = 'blue'; font_weight = 'bold'
            elif 'Trend' in val: color = 'orange'
            elif 'Weak' in val or 'No Trend' in val: color = 'purple'
            # Per BBands
            elif 'Upper' in val: color = 'red' # Prezzo vicino alla banda superiore
            elif 'Lower' in val: color = 'green' # Prezzo vicino alla banda inferiore

    elif isinstance(val, (int, float)): # Per variazioni percentuali
        if val > 0:
            color = 'green'
            text_to_display = f"+{val:.1f}%"
        elif val < 0:
            color = 'red'
            text_to_display = f"{val:.1f}%"
        else:
            color = 'gray'
            text_to_display = f"{val:.1f}%"

    # Per la fiamma, dato che st.dataframe non renderizza HTML bene nello Styler direttamente
    # la aggiungiamo ai dati prima e lo Styler si occupa solo del colore/peso.
    # Oppure, si potrebbe usare st.column_config.TextColumn(validate="streamlit_emoji_shortcodes")
    # se i dati contengono già l'emoji shortcode, ma è più complesso con lo Styler.

    return f'color: {color}; font-weight: {font_weight};'


# --- Interfaccia Utente Streamlit ---
st.set_page_config(layout="wide", page_title="Indicatori Trading Dashboard")
st.title("🔥📊 Dashboard Indicatori Crypto & Stocks") # Aggiunta fiamma al titolo
st.caption(f"Versione: 0.0.5 | Data: {datetime.now().strftime('%Y-%m-%d')}")

# Carica i dati (fittizi per ora)
df_data = get_fictional_data()

# Definisci le colonne
# Rinomino alcune colonne per brevità
df_data.rename(columns={
    'Prezzo Attuale ($)': 'Prezzo ($)',
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


# Colonne informative di base
info_cols = ['Nome Asset', 'Ticker']
price_col = ['Prezzo ($)']
var_cols = ['Var. 1H (%)', 'Var. 12H (%)', 'Var. 24H (%)', 'Var. 1W (%)']
ai_signal_col = ['AI Signal']

# Colonne degli indicatori raggruppate per categoria (con nomi brevi)
oscillator_cols = ['RSI (14)', 'SRSI %K', 'MACD', 'Stoch K', 'AO']
trend_strength_vol_cols = ['ADX', 'BB Pos.'] # ADX e Bollinger Bands
ma_cols = ['EMA20/P', 'SMA50/200', 'VWAP/P']
all_individual_indicator_cols = oscillator_cols + trend_strength_vol_cols + ma_cols
all_styled_cols = var_cols + ai_signal_col + all_individual_indicator_cols

# Riorganizza le colonne per la visualizzazione
display_columns_ordered = info_cols + price_col + var_cols + ai_signal_col + oscillator_cols + trend_strength_vol_cols + ma_cols
df_display = df_data[display_columns_ordered]


formatters = {}
# La formattazione percentuale è ora gestita da style_signals_and_variations
formatters[price_col[0]] = "${:,.2f}"


# Applica lo styling
# Usiamo un approccio diverso per applicare lo style per colonna se necessario
styled_df = df_display.style
for col_name in df_display.columns:
    if col_name in all_styled_cols:
        styled_df = styled_df.apply(lambda series: series.apply(style_signals_and_variations, column_name=col_name), subset=[col_name])

styled_df = styled_df.format(formatters) \
    .set_properties(**{'text-align': 'center'}, subset=all_styled_cols + ['Ticker']) \
    .set_properties(**{'text-align': 'right'}, subset=price_col) \
    .set_properties(**{'text-align': 'left'}, subset=['Nome Asset']) \
    .set_table_styles([
        {'selector': 'th', 'props': [('text-align', 'center'), ('background-color', '#f0f2f6'), ('padding', '0.2rem'), ('font-size', '0.85em')]}, # Header più compatti
        {'selector': 'td', 'props': [('padding', '0.2rem 0.3rem'), ('font-size', '0.85em')]}, # Celle più compatte
    ])

st.markdown("#### Segnali Tecnici Aggregati e Individuali")
# Per la fiamma nell'AI Signal, la soluzione più pulita con Styler è preparare la stringa nei dati.
# Altrimenti, si deve usare HTML diretto nella tabella o st.column_config con st.data_editor (più complesso).
st.dataframe(styled_df, use_container_width=True, hide_index=True)


# --- Legenda Indicatori ---
st.subheader("📜 Legenda Indicatori")
st.markdown("---")

st.markdown("""
**AI Signal (Segnale Aggregato)**
- <span style='color:darkgreen; font-weight:bold;'>🔥 Strong Buy</span>, <span style='color:green; font-weight:bold;'>Buy</span>, <span style='color:gray;'>Neutral</span>, <span style='color:red; font-weight:bold;'>Sell</span>, <span style='color:darkred; font-weight:bold;'>Strong Sell</span>
- *Obiettivo:* Fornire una valutazione rapida e di alto livello basata sull'analisi combinata degli indicatori. *Non una garanzia di risultati.*
""", unsafe_allow_html=True)

st.markdown("#### Variazioni Prezzo")
st.markdown("""
- **Var. 1H, 12H, 24H, 1W (%)**: Variazione percentuale del prezzo rispetto a 1 ora, 12 ore, 24 ore e 1 settimana fa. Verde per positivo, Rosso per negativo.
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
**ADX**: Average Directional Index (14). Indica forza del trend: <span style='color:purple;'>No/Weak Trend</span> (<20), <span style='color:orange;'>Trend</span> (20-25), <span style='color:blue; font-weight:bold;'>Strong Trend</span> (>25). Non dà direzione.
**BB Pos.**: Posizione Prezzo nelle Bande di Bollinger (20,2). <span style='color:green;'>Lower</span> (vicino banda inf.), <span style='color:gray;'>Mid</span> (tra bande), <span style='color:red;'>Upper</span> (vicino banda sup.).
""", unsafe_allow_html=True)

st.markdown("#### M O V I N G   A V E R A G E S (vs Prezzo o Altre MA)")
st.markdown("""
**EMA20/P**: Prezzo vs EMA (20). <span style='color:green; font-weight:bold;'>BUY</span> Prezzo sopra EMA, <span style='color:red; font-weight:bold;'>SELL</span> Prezzo sotto EMA.
**SMA50/200**: SMA Crossover (50/200). <span style='color:green; font-weight:bold;'>BUY</span> Golden Cross (50 sopra 200), <span style='color:red; font-weight:bold;'>SELL</span> Death Cross (50 sotto 200).
**VWAP/P**: Prezzo vs VWAP. <span style='color:green; font-weight:bold;'>BUY</span> Prezzo sopra VWAP, <span style='color:red; font-weight:bold;'>SELL</span> Prezzo sotto VWAP (concetto giornaliero).
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
        asset_involved = "TEST_ASSET"
        function_name = "test_function"
        error_message = "Questo è un errore di test simulato."
        log_entry_content = f"[{timestamp}] Asset: {asset_involved} | Funzione: {function_name} | Errore: {error_message}"
        st.session_state.error_logs.append(log_entry_content)
        st.rerun()

    if st.button("Clear Error Logs"):
        st.session_state.error_logs = []
        st.rerun()

st.markdown("---")
st.caption(f"File: app.py | Versione: 0.0.5 | Ultima Modifica: {datetime.now().strftime('%Y-%m-%d')}")

# FILE_FOOTER_START
# End of file: app.py
# Version: 0.0.5
# Last Modified: 2024-03-17
# FILE_FOOTER_END
