# FILE_VERSION_START
# Project: CryptoAndStocksIndicators
# File: app.py
# Version: 0.0.3
# Date: 2024-03-16
# Author: [Il Tuo Nome/Nickname]
# Description: Correzione AttributeError per .hide_index() con Pandas Styler.
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
        {'Rank': 1, 'Nome Asset': 'Microsoft Corp.', 'Ticker': 'MSFT', 'Market Cap ($)': '3.12 T', 'Prezzo Attuale ($)': 420.55, 'Var. 24H (%)': 0.2,
         'RSI (14)': 'Wait', 'StochRSI %K': 'Buy', 'MACD Signal': 'Buy', 'Stoch %K': 'Wait', 'Awesome Osc.': 'Buy',
         'EMA (20) vs Prezzo': 'Buy', 'SMA (50/200)': 'Buy', 'VWAP vs Prezzo': 'Buy'},
        {'Rank': 2, 'Nome Asset': 'Apple Inc.', 'Ticker': 'AAPL', 'Market Cap ($)': '2.63 T', 'Prezzo Attuale ($)': 170.34, 'Var. 24H (%)': -0.5,
         'RSI (14)': 'Sell', 'StochRSI %K': 'Sell', 'MACD Signal': 'Sell', 'Stoch %K': 'Sell', 'Awesome Osc.': 'Sell',
         'EMA (20) vs Prezzo': 'Sell', 'SMA (50/200)': 'Wait', 'VWAP vs Prezzo': 'Sell'},
        {'Rank': 3, 'Nome Asset': 'NVIDIA Corp.', 'Ticker': 'NVDA', 'Market Cap ($)': '2.20 T', 'Prezzo Attuale ($)': 880.27, 'Var. 24H (%)': 2.1,
         'RSI (14)': 'Buy', 'StochRSI %K': 'Buy', 'MACD Signal': 'Buy', 'Stoch %K': 'Buy', 'Awesome Osc.': 'Buy',
         'EMA (20) vs Prezzo': 'Buy', 'SMA (50/200)': 'Buy', 'VWAP vs Prezzo': 'Buy'},
        {'Rank': 4, 'Nome Asset': 'Alphabet Inc. (Google)', 'Ticker': 'GOOGL', 'Market Cap ($)': '1.75 T', 'Prezzo Attuale ($)': 140.10, 'Var. 24H (%)': 0.7,
         'RSI (14)': 'Wait', 'StochRSI %K': 'Wait', 'MACD Signal': 'Wait', 'Stoch %K': 'Wait', 'Awesome Osc.': 'Wait',
         'EMA (20) vs Prezzo': 'Wait', 'SMA (50/200)': 'Buy', 'VWAP vs Prezzo': 'Wait'},
        {'Rank': 5, 'Nome Asset': 'Amazon.com Inc.', 'Ticker': 'AMZN', 'Market Cap ($)': '1.82 T', 'Prezzo Attuale ($)': 175.80, 'Var. 24H (%)': -1.0,
         'RSI (14)': 'Sell', 'StochRSI %K': 'Sell', 'MACD Signal': 'Sell', 'Stoch %K': 'Sell', 'Awesome Osc.': 'Sell',
         'EMA (20) vs Prezzo': 'Sell', 'SMA (50/200)': 'Wait', 'VWAP vs Prezzo': 'Sell'},
        {'Rank': 6, 'Nome Asset': 'Bitcoin', 'Ticker': 'BTC', 'Market Cap ($)': '1.35 T', 'Prezzo Attuale ($)': 68500.50, 'Var. 24H (%)': 1.5,
         'RSI (14)': 'Buy', 'StochRSI %K': 'Wait', 'MACD Signal': 'Buy', 'Stoch %K': 'Wait', 'Awesome Osc.': 'Buy',
         'EMA (20) vs Prezzo': 'Buy', 'SMA (50/200)': 'Buy', 'VWAP vs Prezzo': 'Buy'},
        {'Rank': 7, 'Nome Asset': 'Meta Platforms Inc.', 'Ticker': 'META', 'Market Cap ($)': '1.22 T', 'Prezzo Attuale ($)': 480.12, 'Var. 24H (%)': -0.8,
         'RSI (14)': 'Wait', 'StochRSI %K': 'Sell', 'MACD Signal': 'Wait', 'Stoch %K': 'Sell', 'Awesome Osc.': 'Wait',
         'EMA (20) vs Prezzo': 'Wait', 'SMA (50/200)': 'Wait', 'VWAP vs Prezzo': 'Sell'},
        {'Rank': 8, 'Nome Asset': 'Ethereum', 'Ticker': 'ETH', 'Market Cap ($)': '450.2 B', 'Prezzo Attuale ($)': 3750.00, 'Var. 24H (%)': 0.8,
         'RSI (14)': 'Wait', 'StochRSI %K': 'Buy', 'MACD Signal': 'Buy', 'Stoch %K': 'Buy', 'Awesome Osc.': 'Buy',
         'EMA (20) vs Prezzo': 'Buy', 'SMA (50/200)': 'Buy', 'VWAP vs Prezzo': 'Buy'},
        {'Rank': 9, 'Nome Asset': 'ProSh UltraPro QQQ', 'Ticker': 'TQQQ', 'Market Cap ($)': '22.1 B', 'Prezzo Attuale ($)': 55.60, 'Var. 24H (%)': 1.5,
         'RSI (14)': 'Buy', 'StochRSI %K': 'Buy', 'MACD Signal': 'Buy', 'Stoch %K': 'Buy', 'Awesome Osc.': 'Buy',
         'EMA (20) vs Prezzo': 'Buy', 'SMA (50/200)': 'Buy', 'VWAP vs Prezzo': 'Buy'},
        {'Rank': 10, 'Nome Asset': 'Tesla, Inc.', 'Ticker': 'TSLA', 'Market Cap ($)': '560.5 B', 'Prezzo Attuale ($)': 177.45, 'Var. 24H (%)': -3.0,
         'RSI (14)': 'Sell', 'StochRSI %K': 'Sell', 'MACD Signal': 'Sell', 'Stoch %K': 'Sell', 'Awesome Osc.': 'Sell',
         'EMA (20) vs Prezzo': 'Sell', 'SMA (50/200)': 'Sell', 'VWAP vs Prezzo': 'Sell'},
        {'Rank': 11, 'Nome Asset': 'IonQ Inc.', 'Ticker': 'IONQ', 'Market Cap ($)': '2.1 B', 'Prezzo Attuale ($)': 10.30, 'Var. 24H (%)': 0.1,
         'RSI (14)': 'Wait', 'StochRSI %K': 'Wait', 'MACD Signal': 'Wait', 'Stoch %K': 'Wait', 'Awesome Osc.': 'Wait',
         'EMA (20) vs Prezzo': 'Wait', 'SMA (50/200)': 'Wait', 'VWAP vs Prezzo': 'Wait'},
        {'Rank': 12, 'Nome Asset': 'ProSh Volatil ST Fut', 'Ticker': 'UVXY', 'Market Cap ($)': '550 M', 'Prezzo Attuale ($)': 8.50, 'Var. 24H (%)': 5.1,
         'RSI (14)': 'Sell', 'StochRSI %K': 'Sell', 'MACD Signal': 'Buy', 'Stoch %K': 'Sell', 'Awesome Osc.': 'Buy',
         'EMA (20) vs Prezzo': 'Buy', 'SMA (50/200)': 'Wait', 'VWAP vs Prezzo': 'Buy'},
        {'Rank': 13, 'Nome Asset': 'Rigetti Computing', 'Ticker': 'RGTI', 'Market Cap ($)': '220 M', 'Prezzo Attuale ($)': 1.52, 'Var. 24H (%)': -1.2,
         'RSI (14)': 'Buy', 'StochRSI %K': 'Buy', 'MACD Signal': 'Sell', 'Stoch %K': 'Buy', 'Awesome Osc.': 'Sell',
         'EMA (20) vs Prezzo': 'Sell', 'SMA (50/200)': 'Sell', 'VWAP vs Prezzo': 'Sell'},
    ]
    df = pd.DataFrame(data)
    df = df.sort_values(by='Rank')
    # Se 'Rank' non dovesse essere usato come indice Pandas, l'indice di default (0,1,2...)
    # verrà nascosto da st.dataframe quando gli si passa un oggetto Styler,
    # oppure possiamo passare hide_index=True a st.dataframe.
    return df

def style_signals(val):
    """Applica stili condizionali per i segnali Buy/Sell/Wait."""
    color = 'inherit'
    font_weight = 'normal'
    if isinstance(val, str):
        if 'Buy' in val.capitalize():
            color = 'green'
            font_weight = 'bold'
        elif 'Sell' in val.capitalize():
            color = 'red'
            font_weight = 'bold'
        elif 'Wait' in val.capitalize():
            color = 'gray'
    return f'color: {color}; font-weight: {font_weight};'

# --- Interfaccia Utente Streamlit ---
st.set_page_config(layout="wide", page_title="Indicatori Trading Dashboard")
st.title("📊 Dashboard Indicatori Crypto & Stocks")
st.caption(f"Versione: 0.0.3 | Data: {datetime.now().strftime('%Y-%m-%d')}")

# Carica i dati (fittizi per ora)
df_data = get_fictional_data()

# Definisci le colonne
info_cols = ['Rank', 'Nome Asset', 'Ticker', 'Market Cap ($)']
price_cols = ['Prezzo Attuale ($)']
percentage_cols = ['Var. 24H (%)']
oscillator_cols = ['RSI (14)', 'StochRSI %K', 'MACD Signal', 'Stoch %K', 'Awesome Osc.']
ma_cols = ['EMA (20) vs Prezzo', 'SMA (50/200)', 'VWAP vs Prezzo']
all_indicator_cols = oscillator_cols + ma_cols

display_columns = info_cols + price_cols + percentage_cols + oscillator_cols + ma_cols
df_display = df_data[display_columns]


formatters = {}
for col in price_cols:
    if col in df_display.columns:
        formatters[col] = "${:,.2f}"
for col in percentage_cols:
    if col in df_display.columns:
        formatters[col] = "{:+.1f}%"

styled_df = df_display.style.apply(lambda x: x.map(style_signals), subset=all_indicator_cols) \
                           .format(formatters) \
                           .set_properties(**{'text-align': 'center'}, subset=all_indicator_cols + percentage_cols + ['Rank']) \
                           .set_properties(**{'text-align': 'right'}, subset=price_cols) \
                           .set_properties(**{'text-align': 'left'}, subset=['Nome Asset', 'Ticker', 'Market Cap ($)']) \
                           .set_table_styles([
                               {'selector': 'th', 'props': [('text-align', 'center'), ('background-color', '#f0f2f6')]},
                               {'selector': 'td', 'props': [('padding', '0.3rem 0.5rem')]},
                               {'selector': 'th.col_heading', 'props': [('font-size', '0.9em')]}
                           ])
                           # .hide_index() # RIMOSSO DA QUI


st.markdown("### Indicatori Tecnici")
# Passiamo hide_index=True direttamente a st.dataframe
st.dataframe(styled_df, use_container_width=True, hide_index=True)


st.subheader("📜 Legenda Indicatori")
st.markdown("---")
st.markdown("#### O S C I L L A T O R S")
st.markdown("""
**Relative Strength Index (RSI 14)**
- *Segnali Base:* <span style='color:green; font-weight:bold;'>BUY</span> < 30 (ipervenduto), <span style='color:red; font-weight:bold;'>SELL</span> > 70 (ipercomprato).
- *Utilità:* Misura velocità e cambiamento dei prezzi. Attenzione a divergenze e trend primario.

**Stochastic RSI (SRSI %K - 14,14,3,3)**
- *Segnali Base (%K):* <span style='color:green; font-weight:bold;'>BUY</span> < 20 (RSI ipervenduto), <span style='color:red; font-weight:bold;'>SELL</span> > 80 (RSI ipercomprato).
- *Utilità:* Più sensibile dell'RSI, buono per segnali a breve. Crossover %K/%D sono più forti.

**MACD (Moving Average Convergence Divergence - 12,26,9) Signal Crossover**
- *Segnali Base:* <span style='color:green; font-weight:bold;'>BUY</span> quando linea MACD incrocia sopra la linea Segnale. <span style='color:red; font-weight:bold;'>SELL</span> quando linea MACD incrocia sotto la linea Segnale.
- *Utilità:* Identifica cambiamenti di momentum e direzione del trend.

**Stochastic Oscillator (%K - 14,3,3)**
- *Segnali Base (%K):* <span style='color:green; font-weight:bold;'>BUY</span> < 20 (ipervenduto), <span style='color:red; font-weight:bold;'>SELL</span> > 80 (ipercomprato).
- *Utilità:* Compara il prezzo di chiusura al suo range di prezzo su un periodo. Crossover %K/%D e divergenze sono importanti.

**Awesome Oscillator (AO)**
- *Segnali Base (semplificato):* <span style='color:green; font-weight:bold;'>BUY</span> quando AO attraversa la linea zero verso l'alto. <span style='color:red; font-weight:bold;'>SELL</span> quando AO attraversa la linea zero verso il basso. (Pattern "Saucer" e "Twin Peaks" offrono altri segnali).
- *Utilità:* Misura il momentum del mercato.
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("#### M O V I N G   A V E R A G E S")
st.markdown("""
**EMA (20) vs Prezzo**
- *Segnali Base:* <span style='color:green; font-weight:bold;'>BUY</span> quando il prezzo chiude sopra l'EMA(20) (da sotto). <span style='color:red; font-weight:bold;'>SELL</span> quando il prezzo chiude sotto l'EMA(20) (da sopra).
- *Utilità:* Media mobile reattiva, usata per segnali a breve/medio termine e come supporto/resistenza dinamica.

**SMA Crossover (50/200) - Golden/Death Cross**
- *Segnali Base:* <span style='color:green; font-weight:bold;'>BUY</span> (Golden Cross) quando SMA(50) incrocia sopra SMA(200). <span style='color:red; font-weight:bold;'>SELL</span> (Death Cross) quando SMA(50) incrocia sotto SMA(200).
- *Utilità:* Segnali di trend a lungo termine molto seguiti.

**VWAP (Volume Weighted Average Price) vs Prezzo**
- *Segnali Base (concettuale giornaliero):* <span style='color:green; font-weight:bold;'>BUY</span> se il prezzo è significativamente sopra il VWAP giornaliero. <span style='color:red; font-weight:bold;'>SELL</span> se il prezzo è significativamente sotto il VWAP giornaliero.
- *Utilità:* Prezzo medio ponderato per volume. Cruciale per intraday; indica il "prezzo equo" della sessione. Per analisi giornaliera, si guarda se la chiusura è sopra/sotto il VWAP del giorno.
""", unsafe_allow_html=True)


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
st.caption(f"File: app.py | Versione: 0.0.3 | Ultima Modifica: {datetime.now().strftime('%Y-%m-%d')}")

# FILE_FOOTER_START
# End of file: app.py
# Version: 0.0.3
# Last Modified: 2024-03-16
# FILE_FOOTER_END
