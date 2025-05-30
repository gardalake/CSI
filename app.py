# FILE_VERSION_START
# Project: CryptoAndStocksIndicators
# File: app.py
# Version: 0.1.2
# Date: 2024-03-19
# Author: [Il Tuo Nome/Nickname]
# Description: Ripristino st.dataframe per stabilità layout, link TV testuale. Correzione colori.
# FILE_VERSION_END

import streamlit as st
import pandas as pd
from datetime import datetime

# --- Configurazione Iniziale e Stato Sessione per Error Logs ---
if 'error_logs' not in st.session_state:
    st.session_state.error_logs = []

# --- Funzioni Helper ---
def get_fictional_data():
    data = [
        # Crypto
        {'Asset Type': 'Crypto', 'Crypto Rank': 1, 'Market Cap': 1.35e12, 'Nome Asset': 'Bitcoin', 'Ticker': 'BTC', 'TradingViewSymbol': 'BTCUSD', 'Prezzo Attuale ($)': 68500.50, 'Var. 1H (%)': 0.8, 'Var. 12H (%)': 2.0, 'Var. 24H (%)': 1.5, 'Var. 1W (%)': 3.0,
         'AI Signal': 'Buy', 'OBV Signal': 'Buy', 'ATR Signal': 'Buy',
         'RSI (14)': 'Buy', 'StochRSI %K': 'Wait', 'MACD Signal': 'Buy', 'Stoch %K': 'Wait', 'Awesome Osc.': 'Buy', 'ADX (14)': 'Strong (40)', 'BBands Pos.': 'Mid',
         'EMA (20) vs Prezzo': 'Buy', 'SMA (50/200)': 'Buy', 'VWAP vs Prezzo': 'Buy'},
        {'Asset Type': 'Crypto', 'Crypto Rank': 2, 'Market Cap': 4.50e11, 'Nome Asset': 'Ethereum', 'Ticker': 'ETH', 'TradingViewSymbol': 'ETHUSD', 'Prezzo Attuale ($)': 3750.00, 'Var. 1H (%)': 0.3, 'Var. 12H (%)': 1.0, 'Var. 24H (%)': 0.8, 'Var. 1W (%)': 2.5,
         'AI Signal': 'Buy', 'OBV Signal': 'Wait', 'ATR Signal': 'Wait',
         'RSI (14)': 'Wait', 'StochRSI %K': 'Buy', 'MACD Signal': 'Buy', 'Stoch %K': 'Buy', 'Awesome Osc.': 'Buy', 'ADX (14)': 'Trend (30)', 'BBands Pos.': 'Upper',
         'EMA (20) vs Prezzo': 'Buy', 'SMA (50/200)': 'Buy', 'VWAP vs Prezzo': 'Buy'},
        # Stocks
        {'Asset Type': 'Stock', 'Crypto Rank': 99999, 'Market Cap': 3.12e12, 'Nome Asset': 'Microsoft Corp.', 'Ticker': 'MSFT', 'TradingViewSymbol': 'NASDAQ:MSFT', 'Prezzo Attuale ($)': 420.55, 'Var. 1H (%)': 0.1, 'Var. 12H (%)': 0.5, 'Var. 24H (%)': 0.2, 'Var. 1W (%)': 1.5,
         'AI Signal': '🔥 Strong Buy', 'OBV Signal': 'Buy', 'ATR Signal': 'Buy',
         'RSI (14)': 'Wait', 'StochRSI %K': 'Buy', 'MACD Signal': 'Buy', 'Stoch %K': 'Wait', 'Awesome Osc.': 'Buy', 'ADX (14)': 'Trend (28)', 'BBands Pos.': 'Mid',
         'EMA (20) vs Prezzo': 'Buy', 'SMA (50/200)': 'Buy', 'VWAP vs Prezzo': 'Buy'},
        {'Asset Type': 'Stock', 'Crypto Rank': 99999, 'Market Cap': 2.63e12, 'Nome Asset': 'Apple Inc.', 'Ticker': 'AAPL', 'TradingViewSymbol': 'NASDAQ:AAPL', 'Prezzo Attuale ($)': 170.34, 'Var. 1H (%)': -0.2, 'Var. 12H (%)': -0.8, 'Var. 24H (%)': -0.5, 'Var. 1W (%)': -2.0,
         'AI Signal': 'Sell', 'OBV Signal': 'Sell', 'ATR Signal': 'Sell',
         'RSI (14)': 'Sell', 'StochRSI %K': 'Sell', 'MACD Signal': 'Sell', 'Stoch %K': 'Sell', 'Awesome Osc.': 'Sell', 'ADX (14)': 'Weak (18)', 'BBands Pos.': 'Upper',
         'EMA (20) vs Prezzo': 'Sell', 'SMA (50/200)': 'Wait', 'VWAP vs Prezzo': 'Sell'},
        # ... (altri dati come prima)
        {'Asset Type': 'Stock', 'Crypto Rank': 99999, 'Market Cap': 2.20e8, 'Nome Asset': 'Rigetti Comp.', 'Ticker': 'RGTI', 'TradingViewSymbol': 'NASDAQ:RGTI', 'Prezzo Attuale ($)': 1.52, 'Var. 1H (%)': -0.5, 'Var. 12H (%)': -1.0, 'Var. 24H (%)': -1.2, 'Var. 1W (%)': -3.5,
         'AI Signal': 'Sell', 'OBV Signal': 'Sell', 'ATR Signal': 'Wait',
         'RSI (14)': 'Buy', 'StochRSI %K': 'Buy', 'MACD Signal': 'Sell', 'Stoch %K': 'Buy', 'Awesome Osc.': 'Sell', 'ADX (14)': 'Weak (17)', 'BBands Pos.': 'Lower',
         'EMA (20) vs Prezzo': 'Sell', 'SMA (50/200)': 'Sell', 'VWAP vs Prezzo': 'Sell'},
    ]
    df = pd.DataFrame(data)
    asset_type_order = {'Crypto': 0, 'Stock': 1, 'ETF': 2}
    df['AssetTypeSort'] = df['Asset Type'].map(asset_type_order)
    df['PrimarySortKey'] = df.apply(lambda row: row['Crypto Rank'] if row['Asset Type'] == 'Crypto' else -row['Market Cap'], axis=1)
    df.sort_values(by=['AssetTypeSort', 'PrimarySortKey'], ascending=[True, True], inplace=True)
    return df

def determine_style_for_cell(val, column_name=""):
    """Determina solo gli attributi CSS color e font-weight per una cella."""
    color_css = ""
    font_weight_css = ""

    # Gestione Variazioni Percentuali (valore numerico)
    if isinstance(val, (int, float)) and "%" in column_name:
        if val > 0: color_css = 'color: green'
        elif val < 0: color_css = 'color: red'
        else: color_css = 'color: gray' # Per 0.0%

    # Gestione Segnali Testuali
    elif isinstance(val, str):
        val_upper = val.upper()
        # Segnali AI
        if "AI SIGNAL" in column_name.upper():
            if 'STRONG BUY' in val_upper: color_css = 'color: darkgreen'; font_weight_css = 'font-weight: bold'
            elif 'BUY' in val_upper: color_css = 'color: green'; font_weight_css = 'font-weight: bold'
            elif 'STRONG SELL' in val_upper: color_css = 'color: darkred'; font_weight_css = 'font-weight: bold'
            elif 'SELL' in val_upper: color_css = 'color: red'; font_weight_css = 'font-weight: bold'
            elif 'NEUTRAL' in val_upper: color_css = 'color: gray'
        # ADX
        elif "ADX" == column_name.upper():
            if 'STRONG' in val_upper or 'TREND' in val_upper: color_css = 'color: green'
            elif 'WEAK' in val_upper or 'NO TREND' in val_upper: color_css = 'color: gray'
            else: color_css = 'color: gray' # Default
        # Bollinger Bands Position
        elif "BB POS." == column_name.upper():
            if 'UPPER' in val_upper: color_css = 'color: red'
            elif 'LOWER' in val_upper: color_css = 'color: green'
            elif 'MID' in val_upper: color_css = 'color: gray'
        # OBV Signal, ATR Signal e altri indicatori Buy/Sell/Wait
        else:
            if 'BUY' in val_upper: color_css = 'color: green'; font_weight_css = 'font-weight: bold'
            elif 'SELL' in val_upper: color_css = 'color: red'; font_weight_css = 'font-weight: bold'
            elif 'WAIT' in val_upper or 'NEUTRAL' in val_upper: color_css = 'color: gray'
    
    # Combina gli stili CSS
    final_style = []
    if color_css: final_style.append(color_css)
    if font_weight_css: final_style.append(font_weight_css)
    
    return '; '.join(final_style) if final_style else None


# --- Interfaccia Utente Streamlit ---
st.set_page_config(layout="wide", page_title="Indicatori Trading Dashboard")
st.title("🔥📊 Dashboard Indicatori Crypto & Stocks")
st.caption(f"Versione: 0.1.2 | Data: {datetime.now().strftime('%Y-%m-%d')}")

df_data_processed = get_fictional_data()

# Colonna Link TradingView come testo Markdown
df_data_processed['TV Link'] = df_data_processed['TradingViewSymbol'].apply(
    lambda x: f"[📈](https://www.tradingview.com/chart/?symbol={x})" # Solo icona come testo del link
)

original_display_cols_ordered = [
    'Nome Asset', 'Ticker', 'TV Link', 'Prezzo Attuale ($)',
    'Var. 1H (%)', 'Var. 12H (%)', 'Var. 24H (%)', 'Var. 1W (%)',
    'AI Signal', 'OBV Signal', 'ATR Signal',
    'RSI (14)', 'StochRSI %K', 'MACD Signal', 'Stoch %K', 'Awesome Osc.',
    'ADX (14)', 'BBands Pos.',
    'EMA (20) vs Prezzo', 'SMA (50/200)', 'VWAP vs Prezzo'
]
df_display = df_data_processed[original_display_cols_ordered].copy()

df_display.rename(columns={
    'Prezzo Attuale ($)': 'Prezzo ($)', 'TV Link': '📈 TV', # Header per il link
    'Awesome Osc.': 'AO', 'StochRSI %K': 'SRSI %K', 'MACD Signal': 'MACD', 'Stoch %K': 'Stoch K',
    'ADX (14)': 'ADX', 'BBands Pos.': 'BB Pos.', 'OBV Signal': 'OBV', 'ATR Signal': 'ATR',
    'EMA (20) vs Prezzo': 'EMA20/P', 'SMA (50/200)': 'SMA50/200', 'VWAP vs Prezzo': 'VWAP/P'
}, inplace=True)

renamed_price_col = ['Prezzo ($)']
renamed_var_cols = ['Var. 1H (%)', 'Var. 12H (%)', 'Var. 24H (%)', 'Var. 1W (%)']
renamed_ai_signal_col = ['AI Signal']
renamed_oscillator_cols = ['RSI (14)', 'SRSI %K', 'MACD', 'Stoch K', 'AO']
renamed_trend_strength_vol_cols = ['ADX', 'BB Pos.', 'OBV', 'ATR']
renamed_ma_cols = ['EMA20/P', 'SMA50/200', 'VWAP/P']
# Non includere '📈 TV' in cols_to_style se non vuoi applicare determine_style_for_cell ad esso
cols_to_style = renamed_var_cols + renamed_ai_signal_col + renamed_oscillator_cols + \
                renamed_trend_strength_vol_cols + renamed_ma_cols

formatters = {}
for col in renamed_var_cols:
    formatters[col] = lambda x: f"{x:+.1f}%" if isinstance(x, (int, float)) else x
formatters[renamed_price_col[0]] = "${:,.2f}"

# Applicazione dello Styler
styled_df = df_display.style

# Applica stili di colore/peso
for col_name in df_display.columns:
    if col_name in cols_to_style:
        styled_df = styled_df.apply(lambda s: s.map(lambda x: determine_style_for_cell(x, column_name=col_name)), subset=[col_name])

styled_df = styled_df.format(formatters) # Applica formattazione testuale

# Applica proprietà generali della tabella (allineamenti, etc.)
# Nota: '📈 TV' è la colonna rinominata per il link
styled_df = styled_df.set_properties(**{'text-align': 'center'}, subset=cols_to_style + ['Ticker', '📈 TV'])
styled_df = styled_df.set_properties(**{'text-align': 'right'}, subset=renamed_price_col)
styled_df = styled_df.set_properties(**{'text-align': 'left'}, subset=['Nome Asset'])
# Stili di tabella per padding e font size (non più necessari qui se st.dataframe li gestisce bene)
# styled_df = styled_df.set_table_styles([
#     {'selector': 'th', 'props': [('text-align', 'center'), ('background-color', '#f0f2f6'), ('padding', '0.2rem'), ('font-size', '0.75em')]},
#     {'selector': 'td', 'props': [('padding', '0.2rem 0.3rem'), ('font-size', '0.75em')]},
# ])

st.markdown("#### Segnali Tecnici Aggregati e Individuali")
st.dataframe(styled_df, use_container_width=True, hide_index=True)


# --- Legenda Indicatori ---
st.subheader("📜 Legenda Dettagliata Indicatori e Colonne")
st.markdown("---")
st.markdown("##### Informazioni Generali & Link")
st.markdown("""
- **Nome Asset**: Nome completo dell'azione o criptovaluta/ETF.
- **Ticker**: Simbolo univoco dell'asset sul mercato.
- **📈 TV**: Link all'analisi grafica dell'asset su TradingView (l'icona è cliccabile).
- **Prezzo ($)**: Ultimo prezzo registrato per l'asset, espresso in USD.
""")
# ... (Il resto della legenda come nella v0.1.1, assicurandosi che i nomi corrispondano)
st.markdown("##### Variazioni di Prezzo (Momentum a Breve Termine)")
st.markdown("""
- **Var. 1H (%)**: Variazione percentuale del prezzo nelle ultime 1 ora.
- **Var. 12H (%)**: Variazione percentuale del prezzo nelle ultime 12 ore.
- **Var. 24H (%)**: Variazione percentuale del prezzo nelle ultime 24 ore.
- **Var. 1W (%)**: Variazione percentuale del prezzo nell'ultima settimana.
*<span style='color:green;'>Verde</span> indica un aumento (+), <span style='color:red;'>Rosso</span> una diminuzione (-), <span style='color:gray;'>Grigio</span> per variazioni nulle (0.0%).*
""", unsafe_allow_html=True)

st.markdown("##### Segnale di Sintesi AI")
st.markdown("""
- **AI Signal**: Un segnale di trading di sintesi (<span style='color:darkgreen; font-weight:bold;'>🔥 Strong Buy</span>, <span style='color:green; font-weight:bold;'>Buy</span>, <span style='color:gray;'>Neutral</span>, <span style='color:red; font-weight:bold;'>Sell</span>, <span style='color:darkred; font-weight:bold;'>Strong Sell</span>).
    - *Descrizione*: Valuta e aggrega i segnali dei singoli indicatori tecnici.
    - *Utilità*: Fornisce una rapida valutazione complessiva. *Nota: è un ausilio, non una garanzia.*
""", unsafe_allow_html=True)

st.markdown("##### Indicatori di Volume, Momentum e Ipercomprato/Ipervenduto")
st.markdown("""
- **OBV** (On-Balance Volume Signal):
    - *Descrizione*: Indicatore di momentum che usa il flusso di volume per predire cambiamenti nel prezzo.
    - *Segnali Base*: <span style='color:green; font-weight:bold;'>BUY</span> se l'OBV mostra accumulo. <span style='color:red; font-weight:bold;'>SELL</span> se OBV mostra distribuzione. <span style='color:gray;'>WAIT</span> altrimenti.
    - *Utilità*: Conferma trend o segnala divergenze.
- **ATR** (Average True Range Signal):
    - *Descrizione*: Misura la volatilità del mercato.
    - *Segnali Base (Proposta)*: <span style='color:green; font-weight:bold;'>BUY/SELL</span> se ATR è alto e suggerisce potenziale breakout/breakdown in linea con altri segnali. <span style='color:gray;'>WAIT</span> se ATR è basso (bassa volatilità).
    - *Utilità*: Aiuta a valutare il rischio e la potenziale magnitudine di un movimento. Un segnale derivato dall'ATR è un'interpretazione.
- **RSI (14)** (Relative Strength Index): Segnali: <30 <span style='color:green; font-weight:bold;'>BUY</span>, >70 <span style='color:red; font-weight:bold;'>SELL</span>, 30-70 (<span style='color:gray;'>WAIT</span>).
- **SRSI %K** (Stochastic RSI %K): Segnali: <20 <span style='color:green; font-weight:bold;'>BUY</span>, >80 <span style='color:red; font-weight:bold;'>SELL</span>, 20-80 (<span style='color:gray;'>WAIT</span>).
- **MACD** (MACD Crossover): Segnali: <span style='color:green; font-weight:bold;'>BUY</span> MACD > Segnale, <span style='color:red; font-weight:bold;'>SELL</span> MACD < Segnale, <span style='color:gray;'>WAIT</span>.
- **Stoch K** (Stochastic %K): Segnali: <20 <span style='color:green; font-weight:bold;'>BUY</span>, >80 <span style='color:red; font-weight:bold;'>SELL</span>, 20-80 (<span style='color:gray;'>WAIT</span>).
- **AO** (Awesome Oscillator): Segnali: <span style='color:green; font-weight:bold;'>BUY</span> AO > 0, <span style='color:red; font-weight:bold;'>SELL</span> AO < 0, <span style='color:gray;'>WAIT</span>.
""", unsafe_allow_html=True)

st.markdown("##### Indicatori di Forza del Trend & Volatilità (Continuazione)")
st.markdown("""
- **ADX** (Average Directional Index):
    - *Interpretazione*: >20 (<span style='color:green;'>Trend Forte/In Sviluppo</span>), <20 (<span style='color:gray;'>Trend Debole/Assente</span>). Non dà direzione.
- **BB Pos.** (Bollinger Bands Position):
    - *Interpretazione*: <span style='color:green;'>Lower</span> (vicino banda inf.), <span style='color:gray;'>Mid</span> (tra bande), <span style='color:red;'>Upper</span> (vicino banda sup.).
""", unsafe_allow_html=True)

st.markdown("##### M E D I E   M O B I L I")
st.markdown("""
- **EMA20/P** (Prezzo vs EMA 20): <span style='color:green; font-weight:bold;'>BUY</span> P > EMA, <span style='color:red; font-weight:bold;'>SELL</span> P < EMA, <span style='color:gray;'>WAIT</span>.
- **SMA50/200** (SMA Crossover 50/200): <span style='color:green; font-weight:bold;'>BUY</span> Golden Cross, <span style='color:red; font-weight:bold;'>SELL</span> Death Cross, <span style='color:gray;'>WAIT</span>.
- **VWAP/P** (Prezzo vs VWAP): <span style='color:green; font-weight:bold;'>BUY</span> P > VWAP, <span style='color:red; font-weight:bold;'>SELL</span> P < VWAP, <span style='color:gray;'>WAIT</span>.
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
st.caption(f"File: app.py | Versione: 0.1.2 | Ultima Modifica: {datetime.now().strftime('%Y-%m-%d')}")

# FILE_FOOTER_START
# End of file: app.py
# Version: 0.1.2
# Last Modified: 2024-03-19
# FILE_FOOTER_END
