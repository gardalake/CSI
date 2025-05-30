# FILE_VERSION_START
# Project: CryptoAndStocksIndicators
# File: app.py
# Version: 0.0.8
# Date: 2024-03-17
# Author: [Il Tuo Nome/Nickname]
# Description: Correzione visibilità testo celle (colore di default).
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
         'RSI (14)': 'Wait', 'StochRSI %K': 'Buy', 'MACD Signal': 'Buy', 'Stoch %K': 'NeutralValue', 'Awesome Osc.': 'Buy', 'ADX (14)': 'Trend (28)', 'BBands Pos.': 'Mid', # Stoch %K cambiato per test
         'EMA (20) vs Prezzo': 'Buy', 'SMA (50/200)': 'Buy', 'VWAP vs Prezzo': 'Buy'},
        {'Nome Asset': 'Apple Inc.', 'Ticker': 'AAPL', 'Prezzo Attuale ($)': 170.34, 'Var. 1H (%)': -0.2, 'Var. 12H (%)': -0.8, 'Var. 24H (%)': -0.5, 'Var. 1W (%)': -2.0,
         'AI Signal': 'Sell',
         'RSI (14)': 'Sell', 'StochRSI %K': 'Sell', 'MACD Signal': 'Sell', 'Stoch %K': 'Sell', 'Awesome Osc.': 'Sell', 'ADX (14)': 'Weak (18)', 'BBands Pos.': 'Upper',
         'EMA (20) vs Prezzo': 'Sell', 'SMA (50/200)': 'Wait', 'VWAP vs Prezzo': 'Sell'},
        {'Nome Asset': 'NVIDIA Corp.', 'Ticker': 'NVDA', 'Prezzo Attuale ($)': 880.27, 'Var. 1H (%)': 0.5, 'Var. 12H (%)': 1.2, 'Var. 24H (%)': 2.1, 'Var. 1W (%)': 5.3,
         'AI Signal': '🔥 Strong Buy',
         'RSI (14)': 'Buy', 'StochRSI %K': 'Buy', 'MACD Signal': 'Buy', 'Stoch %K': 'Buy', 'Awesome Osc.': 'Buy', 'ADX (14)': 'Strong (35)', 'BBands Pos.': 'DefaultCase', # BBands cambiato per test
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
    # Inizializza gli stili come stringhe vuote
    # In questo modo, se nessuna condizione è soddisfatta, non viene applicato alcuno stile specifico per colore/peso
    # e Pandas/Streamlit useranno i default, che dovrebbero gestire i temi chiaro/scuro.
    style_str = ""
    font_weight_str = ""

    if isinstance(val, str):
        # Per segnali AI e indicatori testuali
        color_val = "" # Variabile temporanea per il colore
        if "AI Signal" in column_name:
            if 'Strong Buy' in val: color_val = 'darkgreen'; font_weight_str = 'bold'
            elif 'Buy' in val: color_val = 'green'; font_weight_str = 'bold'
            elif 'Strong Sell' in val: color_val = 'darkred'; font_weight_str = 'bold'
            elif 'Sell' in val: color_val = 'red'; font_weight_str = 'bold'
            elif 'Neutral' in val: color_val = 'gray'
        elif "ADX" in column_name:
            try:
                adx_val_str = val.split('(')[-1].replace(')', '')
                adx_numeric = float(adx_val_str)
                if adx_numeric > 20: color_val = 'green' # Trend presente
                else: color_val = 'gray' # Trend debole/assente
            except:
                color_val = 'gray' # Default se l'estrazione fallisce
        elif "BB Pos." in column_name:
            if 'Upper' in val: color_val = 'red'
            elif 'Lower' in val: color_val = 'green'
            elif 'Mid' in val: color_val = 'gray'
        else: # Per altri indicatori testuali (RSI, MACD, etc.)
            val_cap = val.capitalize()
            if 'Buy' in val_cap: color_val = 'green'; font_weight_str = 'bold'
            elif 'Sell' in val_cap: color_val = 'red'; font_weight_str = 'bold'
            elif 'Wait' in val_cap or 'Neutral' in val_cap: color_val = 'gray'
            # Se val non è "Buy", "Sell", "Wait", "Neutral", color_val rimane vuoto
            # e il testo userà il colore di default del tema.

        if color_val: # Applica il colore solo se è stato impostato
            style_str += f'color: {color_val};'

    elif isinstance(val, (int, float)) and "%" in column_name: # Per variazioni percentuali
        color_val = ""
        if val > 0: color_val = 'green'
        elif val < 0: color_val = 'red'
        else: color_val = 'gray'
        if color_val:
            style_str += f'color: {color_val};'

    if font_weight_str: # Applica il font-weight solo se è stato impostato
        style_str += f'font-weight: {font_weight_str};'

    return style_str if style_str else None # Ritorna None se non ci sono stili da applicare


# --- Interfaccia Utente Streamlit ---
st.set_page_config(layout="wide", page_title="Indicatori Trading Dashboard")
st.title("🔥📊 Dashboard Indicatori Crypto & Stocks")
st.caption(f"Versione: 0.0.8 | Data: {datetime.now().strftime('%Y-%m-%d')}")

df_data_raw = get_fictional_data()

original_info_cols = ['Nome Asset', 'Ticker']
original_price_col = ['Prezzo Attuale ($)']
original_var_cols = ['Var. 1H (%)', 'Var. 12H (%)', 'Var. 24H (%)', 'Var. 1W (%)']
original_ai_signal_col = ['AI Signal']
original_oscillator_cols = ['RSI (14)', 'StochRSI %K', 'MACD Signal', 'Stoch %K', 'Awesome Osc.']
original_trend_strength_vol_cols = ['ADX (14)', 'BBands Pos.']
original_ma_cols = ['EMA (20) vs Prezzo', 'SMA (50/200)', 'VWAP vs Prezzo']

display_columns_original_order = original_info_cols + original_price_col + original_var_cols + original_ai_signal_col + \
                                 original_oscillator_cols + original_trend_strength_vol_cols + original_ma_cols
df_display = df_data_raw[display_columns_original_order].copy()

df_display.rename(columns={
    'Prezzo Attuale ($)': 'Prezzo ($)',
    'Awesome Osc.': 'AO', 'StochRSI %K': 'SRSI %K', 'MACD Signal': 'MACD', 'Stoch %K': 'Stoch K',
    'ADX (14)': 'ADX', 'BBands Pos.': 'BB Pos.',
    'EMA (20) vs Prezzo': 'EMA20/P', 'SMA (50/200)': 'SMA50/200', 'VWAP vs Prezzo': 'VWAP/P'
}, inplace=True)

renamed_price_col = ['Prezzo ($)']
renamed_var_cols = ['Var. 1H (%)', 'Var. 12H (%)', 'Var. 24H (%)', 'Var. 1W (%)']
renamed_ai_signal_col = ['AI Signal']
renamed_oscillator_cols = ['RSI (14)', 'SRSI %K', 'MACD', 'Stoch K', 'AO']
renamed_trend_strength_vol_cols = ['ADX', 'BB Pos.']
renamed_ma_cols = ['EMA20/P', 'SMA50/200', 'VWAP/P']

all_individual_indicator_cols_renamed = renamed_oscillator_cols + renamed_trend_strength_vol_cols + renamed_ma_cols
# Colonne che ricevono uno styling specifico (colore e/o peso)
cols_with_specific_styling = renamed_var_cols + renamed_ai_signal_col + all_individual_indicator_cols_renamed


formatters = {col: lambda x: f"{x:+.1f}%" if isinstance(x, (int,float)) else x for col in renamed_var_cols}
formatters[renamed_price_col[0]] = "${:,.2f}"

styled_df = df_display.style
for col_name in df_display.columns:
    if col_name in cols_with_specific_styling:
        # Per le variazioni %, applichiamo sia lo stile che la formattazione stringa
        if col_name in renamed_var_cols:
            styled_df = styled_df.apply(lambda series: series.apply(style_signals_and_variations, column_name=col_name), subset=[col_name])\
                                 .format({col_name: lambda x: f"{x:+.1f}%"}) # Applica formattazione % qui
        else: # Per AI Signal e altri indicatori
            styled_df = styled_df.apply(lambda series: series.apply(style_signals_and_variations, column_name=col_name), subset=[col_name])

# Applica formattatore prezzo
styled_df = styled_df.format(formatters) \
    .set_properties(**{'text-align': 'center'}, subset=cols_with_specific_styling + ['Ticker']) \
    .set_properties(**{'text-align': 'right'}, subset=renamed_price_col) \
    .set_properties(**{'text-align': 'left'}, subset=['Nome Asset']) \
    .set_table_styles([
        {'selector': 'th', 'props': [('text-align', 'center'), ('background-color', '#f0f2f6'), ('padding', '0.2rem'), ('font-size', '0.8em')]},
        {'selector': 'td', 'props': [('padding', '0.2rem 0.3rem'), ('font-size', '0.8em')]},
    ])

st.markdown("#### Segnali Tecnici Aggregati e Individuali")
st.dataframe(styled_df, use_container_width=True, hide_index=True)


# --- Legenda Indicatori ---
# (Legenda dalla v0.0.7, assicurati che i nomi corrispondano)
st.subheader("📜 Legenda Dettagliata Indicatori e Colonne")
st.markdown("---")

st.markdown("##### Informazioni Generali")
st.markdown("""
- **Nome Asset**: Nome completo dell'azione o criptovaluta.
- **Ticker**: Simbolo univoco dell'asset sul mercato.
- **Prezzo ($)**: Ultimo prezzo registrato per l'asset, espresso in USD.
""")

st.markdown("##### Variazioni di Prezzo (Momentum a Breve Termine)")
st.markdown("""
- **Var. 1H (%)**: Variazione percentuale del prezzo nelle ultime 1 ora. Utile per il momentum intraday.
- **Var. 12H (%)**: Variazione percentuale del prezzo nelle ultime 12 ore. Utile per il momentum a brevissimo termine.
- **Var. 24H (%)**: Variazione percentuale del prezzo nelle ultime 24 ore. Standard per il rendimento giornaliero.
- **Var. 1W (%)**: Variazione percentuale del prezzo nell'ultima settimana. Indica il trend a breve termine.
*Verde indica un aumento, Rosso una diminuzione.*
""")

st.markdown("##### Segnale di Sintesi AI")
st.markdown("""
- **AI Signal**: Un segnale di trading di sintesi (<span style='color:darkgreen; font-weight:bold;'>🔥 Strong Buy</span>, <span style='color:green; font-weight:bold;'>Buy</span>, <span style='color:gray;'>Neutral</span>, <span style='color:red; font-weight:bold;'>Sell</span>, <span style='color:darkred; font-weight:bold;'>Strong Sell</span>) generato algoritmicamente.
    - *Descrizione*: Valuta e aggrega i segnali dei singoli indicatori tecnici.
    - *Utilità*: Fornisce una rapida valutazione complessiva del potenziale di trading. Un forte consenso tra gli indicatori porta a segnali "Strong". *Nota: è un ausilio, non una garanzia.*
""", unsafe_allow_html=True)

st.markdown("##### O S C I L L A T O R S (Indicatori di Momentum e Ipercomprato/Ipervenduto)")
st.markdown("""
- **RSI (14)** (Relative Strength Index):
    - *Descrizione*: Misura la velocità e il cambiamento dei movimenti di prezzo su 14 periodi. Scala 0-100.
    - *Segnali Base*: <30 (ipervenduto, potenziale <span style='color:green; font-weight:bold;'>BUY</span>), >70 (ipercomprato, potenziale <span style='color:red; font-weight:bold;'>SELL</span>).
    - *Utilità*: Identifica condizioni estreme di mercato. Utile per divergenze e conferme di trend.
- **SRSI %K** (Stochastic RSI %K):
    - *Descrizione*: Applica l'oscillatore stocastico ai valori dell'RSI. Più sensibile dell'RSI.
    - *Segnali Base (%K)*: <20 (RSI ipervenduto, <span style='color:green; font-weight:bold;'>BUY</span>), >80 (RSI ipercomprato, <span style='color:red; font-weight:bold;'>SELL</span>).
    - *Utilità*: Segnali a più breve termine. I crossover %K/%D (non mostrati qui) rafforzano il segnale.
- **MACD** (Moving Average Convergence Divergence - Segnale Crossover):
    - *Descrizione*: Mostra la relazione tra due medie mobili esponenziali (EMA) del prezzo. Composto da linea MACD, linea Segnale (EMA della linea MACD) e Istogramma (differenza tra le due).
    - *Segnali Base*: <span style='color:green; font-weight:bold;'>BUY</span> quando linea MACD incrocia sopra la linea Segnale. <span style='color:red; font-weight:bold;'>SELL</span> quando incrocia sotto.
    - *Utilità*: Identifica cambiamenti di momentum, direzione del trend e potenziale forza del trend.
- **Stoch K** (Stochastic Oscillator %K):
    - *Descrizione*: Compara il prezzo di chiusura di un asset al suo range di prezzo su 14 periodi. Scala 0-100.
    - *Segnali Base (%K)*: <20 (ipervenduto, <span style='color:green; font-weight:bold;'>BUY</span>), >80 (ipercomprato, <span style='color:red; font-weight:bold;'>SELL</span>).
    - *Utilità*: Simile all'RSI per ipercomprato/venduto. Crossover %K/%D e divergenze sono importanti.
- **AO** (Awesome Oscillator):
    - *Descrizione*: Misura il momentum del mercato confrontando il momentum recente (SMA 5 periodi della mediana del prezzo) con un momentum più ampio (SMA 34 periodi).
    - *Segnali Base (semplificato)*: <span style='color:green; font-weight:bold;'>BUY</span> quando AO attraversa la linea zero verso l'alto. <span style='color:red; font-weight:bold;'>SELL</span> quando attraversa verso il basso.
    - *Utilità*: Conferma trend e avvisa di possibili inversioni. Altri pattern (Saucer, Twin Peaks) forniscono ulteriori segnali.
""", unsafe_allow_html=True)

st.markdown("##### Indicatori di TREND & VOLATILITÀ")
st.markdown("""
- **ADX** (Average Directional Index):
    - *Descrizione*: Misura la forza di un trend su 14 periodi, non la sua direzione. Scala da 0 a 100.
    - *Interpretazione*: >20 indica un trend presente o in sviluppo (<span style='color:green;'>Verde</span> in tabella). Sotto 20, il trend è debole o il mercato è laterale (<span style='color:gray;'>Grigio</span>). Valori alti (es. >40) indicano trend molto forti.
    - *Utilità*: Aiuta a decidere se usare indicatori di trend (ADX alto) o oscillatori (ADX basso). Non genera segnali Buy/Sell diretti.
- **BB Pos.** (Bollinger Bands Position):
    - *Descrizione*: Le Bande di Bollinger consistono in una media mobile semplice (SMA 20 periodi) più due deviazioni standard sopra (banda superiore) e sotto (banda inferiore).
    - *Interpretazione*: Mostra la posizione del prezzo rispetto alle bande: <span style='color:green;'>Lower</span> (vicino/sotto banda inferiore, potenziale ipervenduto), <span style='color:gray;'>Mid</span> (tra le bande), <span style='color:red;'>Upper</span> (vicino/sopra banda superiore, potenziale ipercomprato).
    - *Utilità*: Indica volatilità (bande strette = bassa vol., bande larghe = alta vol.) e livelli relativi di prezzo. Tocco delle bande non è un segnale da solo, ma va contestualizzato.
""", unsafe_allow_html=True)

st.markdown("##### M E D I E   M O B I L I (Indicatori di Trend e Supporto/Resistenza Dinamici)")
st.markdown("""
- **EMA20/P** (Prezzo vs EMA a 20 periodi):
    - *Descrizione*: Confronta il prezzo di chiusura attuale con la sua Media Mobile Esponenziale a 20 periodi.
    - *Segnali Base*: <span style='color:green; font-weight:bold;'>BUY</span> se il prezzo è sopra l'EMA(20). <span style='color:red; font-weight:bold;'>SELL</span> se il prezzo è sotto l'EMA(20).
    - *Utilità*: L'EMA è più reattiva ai recenti cambiamenti di prezzo rispetto alla SMA. Usata per trend a breve-medio e come livello di supporto/resistenza dinamico.
- **SMA50/200** (SMA Crossover 50/200 periodi):
    - *Descrizione*: Confronta la Media Mobile Semplice a 50 periodi con quella a 200 periodi.
    - *Segnali Base*: <span style='color:green; font-weight:bold;'>BUY</span> (Golden Cross) quando la SMA50 incrocia sopra la SMA200. <span style='color:red; font-weight:bold;'>SELL</span> (Death Cross) quando la SMA50 incrocia sotto la SMA200.
    - *Utilità*: Segnali di trend a lungo termine molto noti e seguiti. Possono indicare importanti cambiamenti nel sentiment del mercato.
- **VWAP/P** (Prezzo vs VWAP - Volume Weighted Average Price):
    - *Descrizione*: Confronta il prezzo attuale con il prezzo medio ponderato per i volumi. Per il timeframe giornaliero, si riferisce al VWAP della giornata.
    - *Segnali Base (concetto giornaliero)*: <span style='color:green; font-weight:bold;'>BUY</span> se il prezzo è sopra il VWAP. <span style='color:red; font-weight:bold;'>SELL</span> se il prezzo è sotto il VWAP.
    - *Utilità*: Considerato un indicatore del "valore equo" durante una sessione. Le istituzioni spesso lo usano come benchmark. Sopra VWAP è generalmente bullish, sotto è bearish per la sessione/giornata.
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
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S"); asset_involved = "TEST_ASSET"; function_name = "test_function"; error_message = "Questo è un errore di test simulato."
        log_entry_content = f"[{timestamp}] Asset: {asset_involved} | Funzione: {function_name} | Errore: {error_message}"
        st.session_state.error_logs.append(log_entry_content)
        st.rerun()

    if st.button("Clear Error Logs"):
        st.session_state.error_logs = []
        st.rerun()

st.markdown("---")
st.caption(f"File: app.py | Versione: 0.0.8 | Ultima Modifica: {datetime.now().strftime('%Y-%m-%d')}")

# FILE_FOOTER_START
# End of file: app.py
# Version: 0.0.8
# Last Modified: 2024-03-17
# FILE_FOOTER_END
