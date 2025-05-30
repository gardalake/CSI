# FILE_VERSION_START
# Project: CryptoAndStocksIndicators
# File: app.py
# Version: 0.1.4
# Date: 2024-03-19
# Author: [Il Tuo Nome/Nickname]
# Description: Risoluzione TypeError con st.dataframe e Styler, link TV testuale + icona. Focus colori.
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
        {'Asset Type': 'Crypto', 'Crypto Rank': 2, 'Market Cap': 4.50e11, 'Nome Asset': 'Ethereum', 'Ticker': 'ETH', 'TradingViewSymbol': 'ETHUSD', 'Prezzo Attuale ($)': 3750.00, 'Var. 1H (%)': -0.3, 'Var. 12H (%)': 1.0, 'Var. 24H (%)': 0.8, 'Var. 1W (%)': 2.5,
         'AI Signal': 'Buy', 'OBV Signal': 'Wait', 'ATR Signal': 'Wait',
         'RSI (14)': 'Wait', 'StochRSI %K': 'Buy', 'MACD Signal': 'Buy', 'Stoch %K': 'Buy', 'Awesome Osc.': 'Buy', 'ADX (14)': 'Trend (30)', 'BBands Pos.': 'Upper',
         'EMA (20) vs Prezzo': 'Buy', 'SMA (50/200)': 'Buy', 'VWAP vs Prezzo': 'Buy'},
        # Stocks & ETFs
        {'Asset Type': 'Stock', 'Crypto Rank': None, 'Market Cap': 3.12e12, 'Nome Asset': 'Microsoft Corp.', 'Ticker': 'MSFT', 'TradingViewSymbol': 'NASDAQ:MSFT', 'Prezzo Attuale ($)': 420.55, 'Var. 1H (%)': 0.1, 'Var. 12H (%)': 0.5, 'Var. 24H (%)': 0.2, 'Var. 1W (%)': 1.5,
         'AI Signal': '🔥 Strong Buy', 'OBV Signal': 'Buy', 'ATR Signal': 'Buy',
         'RSI (14)': 'Wait', 'StochRSI %K': 'Buy', 'MACD Signal': 'Buy', 'Stoch %K': 'Wait', 'Awesome Osc.': 'Buy', 'ADX (14)': 'Trend (28)', 'BBands Pos.': 'Mid',
         'EMA (20) vs Prezzo': 'Buy', 'SMA (50/200)': 'Buy', 'VWAP vs Prezzo': 'Buy'},
        {'Asset Type': 'Stock', 'Crypto Rank': None, 'Market Cap': 2.63e12, 'Nome Asset': 'Apple Inc.', 'Ticker': 'AAPL', 'TradingViewSymbol': 'NASDAQ:AAPL', 'Prezzo Attuale ($)': 170.34, 'Var. 1H (%)': -0.2, 'Var. 12H (%)': -0.8, 'Var. 24H (%)': -0.5, 'Var. 1W (%)': -2.0,
         'AI Signal': 'Sell', 'OBV Signal': 'Sell', 'ATR Signal': 'Sell',
         'RSI (14)': 'Sell', 'StochRSI %K': 'Sell', 'MACD Signal': 'Sell', 'Stoch %K': 'Sell', 'Awesome Osc.': 'Sell', 'ADX (14)': 'Weak (18)', 'BBands Pos.': 'Upper',
         'EMA (20) vs Prezzo': 'Sell', 'SMA (50/200)': 'Wait', 'VWAP vs Prezzo': 'Sell'},
        {'Asset Type': 'Stock', 'Crypto Rank': None, 'Market Cap': 2.20e12, 'Nome Asset': 'NVIDIA Corp.', 'Ticker': 'NVDA', 'TradingViewSymbol': 'NASDAQ:NVDA', 'Prezzo Attuale ($)': 880.27, 'Var. 1H (%)': 0.5, 'Var. 12H (%)': 1.2, 'Var. 24H (%)': 2.1, 'Var. 1W (%)': 5.3,
         'AI Signal': '🔥 Strong Buy', 'OBV Signal': 'Buy', 'ATR Signal': 'Buy',
         'RSI (14)': 'Buy', 'StochRSI %K': 'Buy', 'MACD Signal': 'Buy', 'Stoch %K': 'Buy', 'Awesome Osc.': 'Buy', 'ADX (14)': 'Strong (35)', 'BBands Pos.': 'Upper',
         'EMA (20) vs Prezzo': 'Buy', 'SMA (50/200)': 'Buy', 'VWAP vs Prezzo': 'Buy'},
        {'Asset Type': 'Stock', 'Crypto Rank': None, 'Market Cap': 1.82e12, 'Nome Asset': 'Amazon.com Inc.', 'Ticker': 'AMZN', 'TradingViewSymbol': 'NASDAQ:AMZN', 'Prezzo Attuale ($)': 175.80, 'Var. 1H (%)': 0.0, 'Var. 12H (%)': -0.5, 'Var. 24H (%)': -1.0, 'Var. 1W (%)': -1.2,
         'AI Signal': 'Strong Sell', 'OBV Signal': 'Sell', 'ATR Signal': 'Sell',
         'RSI (14)': 'Sell', 'StochRSI %K': 'Sell', 'MACD Signal': 'Sell', 'Stoch %K': 'Sell', 'Awesome Osc.': 'Sell', 'ADX (14)': 'Trend (26)', 'BBands Pos.': 'Lower',
         'EMA (20) vs Prezzo': 'Sell', 'SMA (50/200)': 'Wait', 'VWAP vs Prezzo': 'Sell'},
        {'Asset Type': 'Stock', 'Crypto Rank': None, 'Market Cap': 1.75e12, 'Nome Asset': 'Alphabet Inc. (GOOGL)', 'Ticker': 'GOOGL', 'TradingViewSymbol': 'NASDAQ:GOOGL', 'Prezzo Attuale ($)': 140.10, 'Var. 1H (%)': 0.0, 'Var. 12H (%)': 0.1, 'Var. 24H (%)': 0.7, 'Var. 1W (%)': 0.5,
         'AI Signal': 'Neutral', 'OBV Signal': 'Wait', 'ATR Signal': 'Wait',
         'RSI (14)': 'Wait', 'StochRSI %K': 'Wait', 'MACD Signal': 'Wait', 'Stoch %K': 'Wait', 'Awesome Osc.': 'Wait', 'ADX (14)': 'No Trend (15)', 'BBands Pos.': 'Mid',
         'EMA (20) vs Prezzo': 'Wait', 'SMA (50/200)': 'Buy', 'VWAP vs Prezzo': 'Wait'},
        {'Asset Type': 'Stock', 'Crypto Rank': None, 'Market Cap': 1.22e12, 'Nome Asset': 'Meta Platforms Inc.', 'Ticker': 'META', 'TradingViewSymbol': 'NASDAQ:META', 'Prezzo Attuale ($)': 480.12, 'Var. 1H (%)': -0.1, 'Var. 12H (%)': 0.0, 'Var. 24H (%)': -0.8, 'Var. 1W (%)': 0.2,
         'AI Signal': 'Neutral', 'OBV Signal': 'Wait', 'ATR Signal': 'Wait',
         'RSI (14)': 'Wait', 'StochRSI %K': 'Sell', 'MACD Signal': 'Wait', 'Stoch %K': 'Sell', 'Awesome Osc.': 'Wait', 'ADX (14)': 'Weak (19)', 'BBands Pos.': 'Mid',
         'EMA (20) vs Prezzo': 'Wait', 'SMA (50/200)': 'Wait', 'VWAP vs Prezzo': 'Sell'},
        {'Asset Type': 'Stock', 'Crypto Rank': None, 'Market Cap': 5.60e11, 'Nome Asset': 'Tesla, Inc.', 'Ticker': 'TSLA', 'TradingViewSymbol': 'NASDAQ:TSLA', 'Prezzo Attuale ($)': 177.45, 'Var. 1H (%)': -0.7, 'Var. 12H (%)': -1.5, 'Var. 24H (%)': -3.0, 'Var. 1W (%)': -6.5,
         'AI Signal': 'Strong Sell', 'OBV Signal': 'Sell', 'ATR Signal': 'Sell',
         'RSI (14)': 'Sell', 'StochRSI %K': 'Sell', 'MACD Signal': 'Sell', 'Stoch %K': 'Sell', 'Awesome Osc.': 'Sell', 'ADX (14)': 'Strong (42)', 'BBands Pos.': 'Lower',
         'EMA (20) vs Prezzo': 'Sell', 'SMA (50/200)': 'Sell', 'VWAP vs Prezzo': 'Sell'},
        {'Asset Type': 'Stock', 'Crypto Rank': None, 'Market Cap': 2.20e8, 'Nome Asset': 'Rigetti Computing (GTI)', 'Ticker': 'RGTI', 'TradingViewSymbol': 'NASDAQ:RGTI', 'Prezzo Attuale ($)': 1.52, 'Var. 1H (%)': -0.5, 'Var. 12H (%)': -1.0, 'Var. 24H (%)': -1.2, 'Var. 1W (%)': -3.5,
         'AI Signal': 'Sell', 'OBV Signal': 'Sell', 'ATR Signal': 'Wait',
         'RSI (14)': 'Buy', 'StochRSI %K': 'Buy', 'MACD Signal': 'Sell', 'Stoch %K': 'Buy', 'Awesome Osc.': 'Sell', 'ADX (14)': 'Weak (17)', 'BBands Pos.': 'Lower',
         'EMA (20) vs Prezzo': 'Sell', 'SMA (50/200)': 'Sell', 'VWAP vs Prezzo': 'Sell'},
        {'Asset Type': 'Stock', 'Crypto Rank': None, 'Market Cap': 2.10e9, 'Nome Asset': 'IonQ Inc. (Quantum)', 'Ticker': 'IONQ', 'TradingViewSymbol': 'NYSE:IONQ', 'Prezzo Attuale ($)': 10.30, 'Var. 1H (%)': 0.0, 'Var. 12H (%)': -0.2, 'Var. 24H (%)': 0.1, 'Var. 1W (%)': -1.0,
         'AI Signal': 'Neutral', 'OBV Signal': 'Wait', 'ATR Signal': 'Wait',
         'RSI (14)': 'Wait', 'StochRSI %K': 'Wait', 'MACD Signal': 'Wait', 'Stoch %K': 'Wait', 'Awesome Osc.': 'Wait', 'ADX (14)': 'No Trend (12)', 'BBands Pos.': 'Mid',
         'EMA (20) vs Prezzo': 'Wait', 'SMA (50/200)': 'Wait', 'VWAP vs Prezzo': 'Wait'},
        {'Asset Type': 'ETF', 'Crypto Rank': None, 'Market Cap': 5.50e8, 'Nome Asset': 'ProSh Volatil ST Fut (UVXY)', 'Ticker': 'UVXY', 'TradingViewSymbol': 'AMEX:UVXY', 'Prezzo Attuale ($)': 8.50, 'Var. 1H (%)': 1.0, 'Var. 12H (%)': 2.5, 'Var. 24H (%)': 5.1, 'Var. 1W (%)': 10.0,
         'AI Signal': 'Buy', 'OBV Signal': 'Buy', 'ATR Signal': 'Buy',
         'RSI (14)': 'Sell', 'StochRSI %K': 'Sell', 'MACD Signal': 'Buy', 'Stoch %K': 'Sell', 'Awesome Osc.': 'Buy', 'ADX (14)': 'Trend (25)', 'BBands Pos.': 'Upper',
         'EMA (20) vs Prezzo': 'Buy', 'SMA (50/200)': 'Wait', 'VWAP vs Prezzo': 'Buy'},
        {'Asset Type': 'ETF', 'Crypto Rank': None, 'Market Cap': 2.21e10, 'Nome Asset': 'ProSh UltraPro QQQ (TQQQ)', 'Ticker': 'TQQQ', 'TradingViewSymbol': 'NASDAQ:TQQQ', 'Prezzo Attuale ($)': 55.60, 'Var. 1H (%)': 0.4, 'Var. 12H (%)': 1.1, 'Var. 24H (%)': 1.5, 'Var. 1W (%)': 4.0,
         'AI Signal': '🔥 Strong Buy', 'OBV Signal': 'Buy', 'ATR Signal': 'Buy',
         'RSI (14)': 'Buy', 'StochRSI %K': 'Buy', 'MACD Signal': 'Buy', 'Stoch %K': 'Buy', 'Awesome Osc.': 'Buy', 'ADX (14)': 'Strong (38)', 'BBands Pos.': 'Upper',
         'EMA (20) vs Prezzo': 'Buy', 'SMA (50/200)': 'Buy', 'VWAP vs Prezzo': 'Buy'},
    ]
    df = pd.DataFrame(data)
    asset_type_order = {'Crypto': 0, 'Stock': 1, 'ETF': 2}
    df['AssetTypeSort'] = df['Asset Type'].map(asset_type_order)
    df['PrimarySortKey'] = df.apply(
        lambda row: row['Crypto Rank'] if row['Asset Type'] == 'Crypto' else -row['Market Cap'], 
        axis=1
    )
    df.sort_values(by=['AssetTypeSort', 'PrimarySortKey'], ascending=[True, True], inplace=True)
    df.drop(columns=['Asset Type', 'Crypto Rank', 'Market Cap', 'AssetTypeSort', 'PrimarySortKey'], inplace=True, errors='ignore')
    return df

def apply_cell_styles(val, column_name=""):
    """Determina gli attributi CSS color e font-weight per una cella. Usa i nomi di colonna come sono nel DataFrame passato allo Styler."""
    color_css = ""
    font_weight_css = ""

    # Gestione Variazioni Percentuali (valore numerico)
    if isinstance(val, (int, float)) and "%" in column_name:
        if val > 0: color_css = 'color: green'
        elif val < 0: color_css = 'color: red'
        else: color_css = 'color: gray'

    # Gestione Segnali Testuali
    elif isinstance(val, str):
        val_upper = val.upper() # Per controlli case-insensitive
        
        # Utilizza i nomi delle colonne come appaiono nel DataFrame che stai stilando (df_to_display_styled)
        # Cioè, i nomi RINOMINATI (es. 'AI Signal', 'ADX', 'BB Pos.')
        if column_name == 'AI Signal':
            if 'STRONG BUY' in val_upper: color_css = 'color: darkgreen'; font_weight_css = 'font-weight: bold'
            elif 'BUY' in val_upper: color_css = 'color: green'; font_weight_css = 'font-weight: bold'
            elif 'STRONG SELL' in val_upper: color_css = 'color: darkred'; font_weight_css = 'font-weight: bold'
            elif 'SELL' in val_upper: color_css = 'color: red'; font_weight_css = 'font-weight: bold'
            elif 'NEUTRAL' in val_upper: color_css = 'color: gray'
        
        elif column_name == 'ADX': # Nome rinominato
            if 'STRONG' in val_upper or 'TREND' in val_upper: color_css = 'color: green'
            elif 'WEAK' in val_upper or 'NO TREND' in val_upper: color_css = 'color: gray'
            else: color_css = 'color: gray'
        
        elif column_name == 'BB Pos.': # Nome rinominato
            if 'UPPER' in val_upper: color_css = 'color: red'
            elif 'LOWER' in val_upper: color_css = 'color: green'
            elif 'MID' in val_upper: color_css = 'color: gray'
        
        # Per tutti gli altri indicatori con segnali Buy/Sell/Wait
        # (OBV, ATR, RSI, SRSI %K, MACD, Stoch K, AO, EMA20/P, SMA50/200, VWAP/P)
        # Questi nomi sono quelli rinominati
        else:
            if 'BUY' in val_upper: color_css = 'color: green'; font_weight_css = 'font-weight: bold'
            elif 'SELL' in val_upper: color_css = 'color: red'; font_weight_css = 'font-weight: bold'
            elif 'WAIT' in val_upper or 'NEUTRAL' in val_upper: color_css = 'color: gray'
    
    final_style = []
    if color_css: final_style.append(color_css)
    if font_weight_css: final_style.append(font_weight_css)
    
    return '; '.join(final_style) if final_style else None


# --- Interfaccia Utente Streamlit ---
st.set_page_config(layout="wide", page_title="Indicatori Trading Dashboard")
st.title("🔥📊 Dashboard Indicatori Crypto & Stocks")
st.caption(f"Versione: 0.1.4 | Data: {datetime.now().strftime('%Y-%m-%d')}")

df_data_processed = get_fictional_data()

# Crea colonna Link TradingView come testo Markdown
df_data_processed['TV Link Markdown'] = df_data_processed['TradingViewSymbol'].apply(
    lambda x: f"<a href='https://www.tradingview.com/chart/?symbol={x}' target='_blank' style='text-decoration:none; color:inherit; font-size: 1.1em;'>📈</a>"
)
df_data_processed.drop(columns=['TradingViewSymbol'], inplace=True, errors='ignore')

# Colonne da visualizzare e loro ordine
# Questi sono i nomi originali che il DataFrame ha in questo momento
cols_to_display_order = [
    'Nome Asset', 'Ticker', 'TV Link Markdown', 'Prezzo Attuale ($)',
    'Var. 1H (%)', 'Var. 12H (%)', 'Var. 24H (%)', 'Var. 1W (%)',
    'AI Signal', 'OBV Signal', 'ATR Signal',
    'RSI (14)', 'StochRSI %K', 'MACD Signal', 'Stoch %K', 'Awesome Osc.',
    'ADX (14)', 'BBands Pos.',
    'EMA (20) vs Prezzo', 'SMA (50/200)', 'VWAP vs Prezzo'
]
df_for_styling = df_data_processed[cols_to_display_order].copy()

# Rinomina colonne per la visualizzazione (header tabella)
# Questa mappa usa i nomi attuali di df_for_styling come chiavi
rename_map_for_display_headers = {
    'Prezzo Attuale ($)': 'Prezzo ($)', 'TV Link Markdown': '📈',
    'Awesome Osc.': 'AO', 'StochRSI %K': 'SRSI %K', 'MACD Signal': 'MACD', 'Stoch %K': 'Stoch K',
    'ADX (14)': 'ADX', 'BBands Pos.': 'BB Pos.', 'OBV Signal': 'OBV', 'ATR Signal': 'ATR',
    'EMA (20) vs Prezzo': 'EMA20/P', 'SMA (50/200)': 'SMA50/200', 'VWAP vs Prezzo': 'VWAP/P'
}
df_for_styling.rename(columns=rename_map_for_display_headers, inplace=True)


# Definisci i formattatori testuali (per %, $)
# Applica ai nomi delle colonne *dopo* la ridenominazione (quelli in df_for_styling.columns)
formatters = {}
for col_header in df_for_styling.columns:
    if "%" in col_header:
         formatters[col_header] = lambda x: f"{x:+.1f}%" if isinstance(x, (int, float)) else x
    elif col_header == 'Prezzo ($)':
        formatters[col_header] = "${:,.2f}"

# Applica lo Styler
styled_df = df_for_styling.style

# Applica stili di colore/peso cella per cella
# La funzione apply_cell_styles ora usa i nomi delle colonne di df_for_styling (quelli rinominati)
for col_name_in_styled_df in df_for_styling.columns:
    # Non applicare lo styling basato su valore alla colonna dei link TV
    if col_name_in_styled_df != '📈':
        styled_df = styled_df.apply(
            lambda series: series.map(lambda val: apply_cell_styles(val, column_name=series.name)),
            subset=[col_name_in_styled_df]
        )

styled_df = styled_df.format(formatters)

styled_df = styled_df.set_properties(**{'text-align': 'center'}, subset=df_for_styling.columns.drop(['Nome Asset', 'Prezzo ($)']))
styled_df = styled_df.set_properties(**{'text-align': 'right'}, subset=['Prezzo ($)'])
styled_df = styled_df.set_properties(**{'text-align': 'left'}, subset=['Nome Asset'])
styled_df = styled_df.set_table_styles([
    {'selector': 'th', 'props': [('text-align', 'center'), ('background-color', '#f0f2f6'), ('padding', '0.2rem'), ('font-size', '0.75em')]},
    {'selector': 'td', 'props': [('padding', '0.2rem 0.3rem'), ('font-size', '0.75em')]},
])

st.markdown("#### Segnali Tecnici Aggregati e Individuali")
# Usare unsafe_allow_html=True per permettere il rendering del link HTML nella colonna '📈'
st.dataframe(styled_df, use_container_width=True, hide_index=True, unsafe_allow_html=True)


# --- Legenda Indicatori ---
# (come versione 0.1.3, assicurandosi che i nomi brevi siano usati consistentemente)
st.subheader("📜 Legenda Dettagliata Indicatori e Colonne")
st.markdown("---")
st.markdown("##### Informazioni Generali & Link")
st.markdown("""
- **Nome Asset**: Nome completo dell'azione o criptovaluta/ETF.
- **Ticker**: Simbolo univoco dell'asset sul mercato.
- **📈**: Link all'analisi grafica dell'asset su TradingView (l'icona è cliccabile).
- **Prezzo ($)**: Ultimo prezzo registrato per l'asset, espresso in USD.
""")
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
st.caption(f"File: app.py | Versione: 0.1.4 | Ultima Modifica: {datetime.now().strftime('%Y-%m-%d')}")


# FILE_FOOTER_START
# End of file: app.py
# Version: 0.1.4
# Last Modified: 2024-03-19
# FILE_FOOTER_END
