# FILE_VERSION_START
# Project: CryptoAndStocksIndicators
# File: app.py
# Version: 0.1.0
# Date: 2024-03-18
# Author: [Il Tuo Nome/Nickname]
# Description: Ordinamento Crypto/Stocks, Link TradingView, colonne fittizie OBV & ATR.
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
    Include Asset Type, Crypto Rank (per crypto), Market Cap (per stocks, per ordinamento), OBV, ATR.
    """
    # Market Cap fittizi per l'ordinamento delle stocks (valori più alti = rank più basso per l'ordinamento)
    # Crypto Rank fittizi per le crypto
    data = [
        # Crypto
        {'Asset Type': 'Crypto', 'Crypto Rank': 1, 'Market Cap': 1.35e12, 'Nome Asset': 'Bitcoin', 'Ticker': 'BTC', 'TradingViewSymbol': 'BTCUSD', 'Prezzo Attuale ($)': 68500.50, 'Var. 1H (%)': 0.8, 'Var. 12H (%)': 2.0, 'Var. 24H (%)': 1.5, 'Var. 1W (%)': 3.0,
         'AI Signal': 'Buy', 'OBV Signal': 'Buy', 'ATR (14)': 1500.50,
         'RSI (14)': 'Buy', 'StochRSI %K': 'Wait', 'MACD Signal': 'Buy', 'Stoch %K': 'Wait', 'Awesome Osc.': 'Buy', 'ADX (14)': 'Strong (40)', 'BBands Pos.': 'Mid',
         'EMA (20) vs Prezzo': 'Buy', 'SMA (50/200)': 'Buy', 'VWAP vs Prezzo': 'Buy'},
        {'Asset Type': 'Crypto', 'Crypto Rank': 2, 'Market Cap': 4.50e11, 'Nome Asset': 'Ethereum', 'Ticker': 'ETH', 'TradingViewSymbol': 'ETHUSD', 'Prezzo Attuale ($)': 3750.00, 'Var. 1H (%)': 0.3, 'Var. 12H (%)': 1.0, 'Var. 24H (%)': 0.8, 'Var. 1W (%)': 2.5,
         'AI Signal': 'Buy', 'OBV Signal': 'Wait', 'ATR (14)': 80.20,
         'RSI (14)': 'Wait', 'StochRSI %K': 'Buy', 'MACD Signal': 'Buy', 'Stoch %K': 'Buy', 'Awesome Osc.': 'Buy', 'ADX (14)': 'Trend (30)', 'BBands Pos.': 'Upper',
         'EMA (20) vs Prezzo': 'Buy', 'SMA (50/200)': 'Buy', 'VWAP vs Prezzo': 'Buy'},

        # Stocks (Market Cap più alti per farli venire dopo le crypto se ordiniamo per un rank combinato)
        {'Asset Type': 'Stock', 'Crypto Rank': 99999, 'Market Cap': 3.12e12, 'Nome Asset': 'Microsoft Corp.', 'Ticker': 'MSFT', 'TradingViewSymbol': 'NASDAQ:MSFT', 'Prezzo Attuale ($)': 420.55, 'Var. 1H (%)': 0.1, 'Var. 12H (%)': 0.5, 'Var. 24H (%)': 0.2, 'Var. 1W (%)': 1.5,
         'AI Signal': '🔥 Strong Buy', 'OBV Signal': 'Buy', 'ATR (14)': 5.30,
         'RSI (14)': 'Wait', 'StochRSI %K': 'Buy', 'MACD Signal': 'Buy', 'Stoch %K': 'Wait', 'Awesome Osc.': 'Buy', 'ADX (14)': 'Trend (28)', 'BBands Pos.': 'Mid',
         'EMA (20) vs Prezzo': 'Buy', 'SMA (50/200)': 'Buy', 'VWAP vs Prezzo': 'Buy'},
        {'Asset Type': 'Stock', 'Crypto Rank': 99999, 'Market Cap': 2.63e12, 'Nome Asset': 'Apple Inc.', 'Ticker': 'AAPL', 'TradingViewSymbol': 'NASDAQ:AAPL', 'Prezzo Attuale ($)': 170.34, 'Var. 1H (%)': -0.2, 'Var. 12H (%)': -0.8, 'Var. 24H (%)': -0.5, 'Var. 1W (%)': -2.0,
         'AI Signal': 'Sell', 'OBV Signal': 'Sell', 'ATR (14)': 2.10,
         'RSI (14)': 'Sell', 'StochRSI %K': 'Sell', 'MACD Signal': 'Sell', 'Stoch %K': 'Sell', 'Awesome Osc.': 'Sell', 'ADX (14)': 'Weak (18)', 'BBands Pos.': 'Upper',
         'EMA (20) vs Prezzo': 'Sell', 'SMA (50/200)': 'Wait', 'VWAP vs Prezzo': 'Sell'},
        {'Asset Type': 'Stock', 'Crypto Rank': 99999, 'Market Cap': 2.20e12, 'Nome Asset': 'NVIDIA Corp.', 'Ticker': 'NVDA', 'TradingViewSymbol': 'NASDAQ:NVDA', 'Prezzo Attuale ($)': 880.27, 'Var. 1H (%)': 0.5, 'Var. 12H (%)': 1.2, 'Var. 24H (%)': 2.1, 'Var. 1W (%)': 5.3,
         'AI Signal': '🔥 Strong Buy', 'OBV Signal': 'Buy', 'ATR (14)': 30.55,
         'RSI (14)': 'Buy', 'StochRSI %K': 'Buy', 'MACD Signal': 'Buy', 'Stoch %K': 'Buy', 'Awesome Osc.': 'Buy', 'ADX (14)': 'Strong (35)', 'BBands Pos.': 'Upper',
         'EMA (20) vs Prezzo': 'Buy', 'SMA (50/200)': 'Buy', 'VWAP vs Prezzo': 'Buy'},
        {'Asset Type': 'Stock', 'Crypto Rank': 99999, 'Market Cap': 1.75e12, 'Nome Asset': 'Alphabet Inc.', 'Ticker': 'GOOGL', 'TradingViewSymbol': 'NASDAQ:GOOGL', 'Prezzo Attuale ($)': 140.10, 'Var. 1H (%)': 0.0, 'Var. 12H (%)': 0.1, 'Var. 24H (%)': 0.7, 'Var. 1W (%)': 0.5,
         'AI Signal': 'Neutral', 'OBV Signal': 'Wait', 'ATR (14)': 1.80,
         'RSI (14)': 'Wait', 'StochRSI %K': 'Wait', 'MACD Signal': 'Wait', 'Stoch %K': 'Wait', 'Awesome Osc.': 'Wait', 'ADX (14)': 'No Trend (15)', 'BBands Pos.': 'Mid',
         'EMA (20) vs Prezzo': 'Wait', 'SMA (50/200)': 'Buy', 'VWAP vs Prezzo': 'Wait'},
        {'Asset Type': 'Stock', 'Crypto Rank': 99999, 'Market Cap': 1.82e12, 'Nome Asset': 'Amazon.com Inc.', 'Ticker': 'AMZN', 'TradingViewSymbol': 'NASDAQ:AMZN', 'Prezzo Attuale ($)': 175.80, 'Var. 1H (%)': -0.3, 'Var. 12H (%)': -0.5, 'Var. 24H (%)': -1.0, 'Var. 1W (%)': -1.2,
         'AI Signal': 'Strong Sell', 'OBV Signal': 'Sell', 'ATR (14)': 2.50,
         'RSI (14)': 'Sell', 'StochRSI %K': 'Sell', 'MACD Signal': 'Sell', 'Stoch %K': 'Sell', 'Awesome Osc.': 'Sell', 'ADX (14)': 'Trend (26)', 'BBands Pos.': 'Lower',
         'EMA (20) vs Prezzo': 'Sell', 'SMA (50/200)': 'Wait', 'VWAP vs Prezzo': 'Sell'},
        {'Asset Type': 'Stock', 'Crypto Rank': 99999, 'Market Cap': 1.22e12, 'Nome Asset': 'Meta Platforms', 'Ticker': 'META', 'TradingViewSymbol': 'NASDAQ:META', 'Prezzo Attuale ($)': 480.12, 'Var. 1H (%)': -0.1, 'Var. 12H (%)': 0.0, 'Var. 24H (%)': -0.8, 'Var. 1W (%)': 0.2,
         'AI Signal': 'Neutral', 'OBV Signal': 'Wait', 'ATR (14)': 7.10,
         'RSI (14)': 'Wait', 'StochRSI %K': 'Sell', 'MACD Signal': 'Wait', 'Stoch %K': 'Sell', 'Awesome Osc.': 'Wait', 'ADX (14)': 'Weak (19)', 'BBands Pos.': 'Mid',
         'EMA (20) vs Prezzo': 'Wait', 'SMA (50/200)': 'Wait', 'VWAP vs Prezzo': 'Sell'},
        {'Asset Type': 'ETF', 'Crypto Rank': 99999, 'Market Cap': 2.21e10, 'Nome Asset': 'UltraPro QQQ', 'Ticker': 'TQQQ', 'TradingViewSymbol': 'NASDAQ:TQQQ', 'Prezzo Attuale ($)': 55.60, 'Var. 1H (%)': 0.4, 'Var. 12H (%)': 1.1, 'Var. 24H (%)': 1.5, 'Var. 1W (%)': 4.0,
         'AI Signal': '🔥 Strong Buy', 'OBV Signal': 'Buy', 'ATR (14)': 1.20,
         'RSI (14)': 'Buy', 'StochRSI %K': 'Buy', 'MACD Signal': 'Buy', 'Stoch %K': 'Buy', 'Awesome Osc.': 'Buy', 'ADX (14)': 'Strong (38)', 'BBands Pos.': 'Upper',
         'EMA (20) vs Prezzo': 'Buy', 'SMA (50/200)': 'Buy', 'VWAP vs Prezzo': 'Buy'},
        {'Asset Type': 'Stock', 'Crypto Rank': 99999, 'Market Cap': 5.60e11, 'Nome Asset': 'Tesla, Inc.', 'Ticker': 'TSLA', 'TradingViewSymbol': 'NASDAQ:TSLA', 'Prezzo Attuale ($)': 177.45, 'Var. 1H (%)': -0.7, 'Var. 12H (%)': -1.5, 'Var. 24H (%)': -3.0, 'Var. 1W (%)': -6.5,
         'AI Signal': 'Strong Sell', 'OBV Signal': 'Sell', 'ATR (14)': 8.60,
         'RSI (14)': 'Sell', 'StochRSI %K': 'Sell', 'MACD Signal': 'Sell', 'Stoch %K': 'Sell', 'Awesome Osc.': 'Sell', 'ADX (14)': 'Strong (42)', 'BBands Pos.': 'Lower',
         'EMA (20) vs Prezzo': 'Sell', 'SMA (50/200)': 'Sell', 'VWAP vs Prezzo': 'Sell'},
        {'Asset Type': 'Stock', 'Crypto Rank': 99999, 'Market Cap': 2.10e9, 'Nome Asset': 'IonQ Inc.', 'Ticker': 'IONQ', 'TradingViewSymbol': 'NYSE:IONQ', 'Prezzo Attuale ($)': 10.30, 'Var. 1H (%)': 0.0, 'Var. 12H (%)': -0.2, 'Var. 24H (%)': 0.1, 'Var. 1W (%)': -1.0,
         'AI Signal': 'Neutral', 'OBV Signal': 'Wait', 'ATR (14)': 0.50,
         'RSI (14)': 'Wait', 'StochRSI %K': 'Wait', 'MACD Signal': 'Wait', 'Stoch %K': 'Wait', 'Awesome Osc.': 'Wait', 'ADX (14)': 'No Trend (12)', 'BBands Pos.': 'Mid',
         'EMA (20) vs Prezzo': 'Wait', 'SMA (50/200)': 'Wait', 'VWAP vs Prezzo': 'Wait'},
        {'Asset Type': 'ETF', 'Crypto Rank': 99999, 'Market Cap': 5.50e8, 'Nome Asset': 'Volatil ST Fut', 'Ticker': 'UVXY', 'TradingViewSymbol': 'AMEX:UVXY', 'Prezzo Attuale ($)': 8.50, 'Var. 1H (%)': 1.0, 'Var. 12H (%)': 2.5, 'Var. 24H (%)': 5.1, 'Var. 1W (%)': 10.0,
         'AI Signal': 'Buy', 'OBV Signal': 'Buy', 'ATR (14)': 0.80,
         'RSI (14)': 'Sell', 'StochRSI %K': 'Sell', 'MACD Signal': 'Buy', 'Stoch %K': 'Sell', 'Awesome Osc.': 'Buy', 'ADX (14)': 'Trend (25)', 'BBands Pos.': 'Upper',
         'EMA (20) vs Prezzo': 'Buy', 'SMA (50/200)': 'Wait', 'VWAP vs Prezzo': 'Buy'},
        {'Asset Type': 'Stock', 'Crypto Rank': 99999, 'Market Cap': 2.20e8, 'Nome Asset': 'Rigetti Comp.', 'Ticker': 'RGTI', 'TradingViewSymbol': 'NASDAQ:RGTI', 'Prezzo Attuale ($)': 1.52, 'Var. 1H (%)': -0.5, 'Var. 12H (%)': -1.0, 'Var. 24H (%)': -1.2, 'Var. 1W (%)': -3.5,
         'AI Signal': 'Sell', 'OBV Signal': 'Sell', 'ATR (14)': 0.15,
         'RSI (14)': 'Buy', 'StochRSI %K': 'Buy', 'MACD Signal': 'Sell', 'Stoch %K': 'Buy', 'Awesome Osc.': 'Sell', 'ADX (14)': 'Weak (17)', 'BBands Pos.': 'Lower',
         'EMA (20) vs Prezzo': 'Sell', 'SMA (50/200)': 'Sell', 'VWAP vs Prezzo': 'Sell'},
    ]
    df = pd.DataFrame(data)

    # Logica di Ordinamento: Crypto per Crypto Rank, Stocks per Market Cap (decrescente)
    # Assegna un valore di ordinamento per tipo di asset per mettere Crypto prima
    asset_type_order = {'Crypto': 0, 'Stock': 1, 'ETF': 2} # ETF dopo le stocks
    df['AssetTypeSort'] = df['Asset Type'].map(asset_type_order)

    # Per le stocks/ETF, vogliamo ordinare per Market Cap decrescente, quindi usiamo -Market Cap
    # Per le crypto, usiamo Crypto Rank
    df['PrimarySortKey'] = df.apply(
        lambda row: row['Crypto Rank'] if row['Asset Type'] == 'Crypto' else -row['Market Cap'],
        axis=1
    )
    df.sort_values(by=['AssetTypeSort', 'PrimarySortKey'], ascending=[True, True], inplace=True)
    
    # Rimuovere colonne usate solo per l'ordinamento se non strettamente necessarie per la visualizzazione
    # df.drop(columns=['Asset Type', 'Crypto Rank', 'Market Cap', 'AssetTypeSort', 'PrimarySortKey'], inplace=True, errors='ignore')
    # Per ora le teniamo per debug, ma poi 'Market Cap', 'Crypto Rank', 'AssetTypeSort', 'PrimarySortKey' possono essere droppate
    # 'Asset Type' potrebbe essere utile da mantenere.
    return df

def determine_style(val, column_name=""):
    color = ""
    font_weight = ""
    if isinstance(val, str):
        if "AI Signal" in column_name:
            if 'Strong Buy' in val: color = 'darkgreen'; font_weight = 'bold'
            elif 'Buy' in val: color = 'green'; font_weight = 'bold'
            elif 'Strong Sell' in val: color = 'darkred'; font_weight = 'bold'
            elif 'Sell' in val: color = 'red'; font_weight = 'bold'
            elif 'Neutral' in val: color = 'gray'
        elif "ADX" in column_name:
            try:
                adx_numeric = float(val.split('(')[-1].replace(')', ''))
                if adx_numeric > 20: color = 'green'
                else: color = 'gray'
            except: color = 'gray'
        elif "BB Pos." in column_name:
            if 'Upper' in val: color = 'red'
            elif 'Lower' in val: color = 'green'
            elif 'Mid' in val: color = 'gray'
        elif "OBV Signal" in column_name: # OBV
            if 'Buy' in val: color = 'green'; font_weight = 'bold'
            elif 'Sell' in val: color = 'red'; font_weight = 'bold'
            elif 'Wait' in val: color = 'gray'
        else: # Altri indicatori testuali
            val_cap = val.capitalize()
            if 'Buy' in val_cap: color = 'green'; font_weight = 'bold'
            elif 'Sell' in val_cap: color = 'red'; font_weight = 'bold'
            elif 'Wait' in val_cap or 'Neutral' in val_cap: color = 'gray'
    elif isinstance(val, (int, float)): # Per variazioni % e ATR
        if "%" in column_name: # Variazioni %
            if val > 0: color = 'green'
            elif val < 0: color = 'red'
            else: color = 'gray'
        elif "ATR" in column_name: # ATR (solo valore, nessun colore specifico di segnale)
            pass # Nessun colore specifico per ATR, usa il default
            
    style_parts = []
    if color: style_parts.append(f'color: {color}')
    if font_weight: style_parts.append(f'font-weight: {font_weight}')
    return '; '.join(style_parts) if style_parts else None

def generate_tradingview_link(symbol):
    """Genera un link a TradingView per il simbolo dato."""
    # Questo è un esempio, i prefissi (NASDAQ:, CRYPTOCAP:, etc.) potrebbero dover essere
    # gestiti in modo più intelligente in base al tipo di asset o all'exchange.
    # Per crypto, spesso è TickerUSD (es. BTCUSD). Per stocks, Exchange:Ticker.
    base_url = "https://www.tradingview.com/chart/?symbol="
    return f"{base_url}{symbol}"


# --- Interfaccia Utente Streamlit ---
st.set_page_config(layout="wide", page_title="Indicatori Trading Dashboard")
st.title("🔥📊 Dashboard Indicatori Crypto & Stocks")
st.caption(f"Versione: 0.1.0 | Data: {datetime.now().strftime('%Y-%m-%d')}")

df_data_processed = get_fictional_data() # Ora contiene Asset Type, Crypto Rank, Market Cap, TV Symbol

# Aggiungi colonna HTML per il link a TradingView
# Usiamo markdown per i link
df_data_processed['Link Analisi'] = df_data_processed['TradingViewSymbol'].apply(
    lambda x: f"[TV 📈](https://www.tradingview.com/chart/?symbol={x})"
)


# Definizione e Ridenominazione Colonne
# Colonne da visualizzare e loro ordine (nomi originali da df_data_processed)
original_display_cols_ordered = [
    'Nome Asset', 'Ticker', 'Link Analisi', 'Prezzo Attuale ($)',
    'Var. 1H (%)', 'Var. 12H (%)', 'Var. 24H (%)', 'Var. 1W (%)',
    'AI Signal', 'OBV Signal', 'ATR (14)',
    'RSI (14)', 'StochRSI %K', 'MACD Signal', 'Stoch %K', 'Awesome Osc.',
    'ADX (14)', 'BBands Pos.',
    'EMA (20) vs Prezzo', 'SMA (50/200)', 'VWAP vs Prezzo'
]
df_display = df_data_processed[original_display_cols_ordered].copy()

# Rinomina colonne per la visualizzazione (se necessario)
df_display.rename(columns={
    'Prezzo Attuale ($)': 'Prezzo ($)',
    'Awesome Osc.': 'AO', 'StochRSI %K': 'SRSI %K', 'MACD Signal': 'MACD', 'Stoch %K': 'Stoch K',
    'ADX (14)': 'ADX', 'BBands Pos.': 'BB Pos.', 'OBV Signal': 'OBV', 'ATR (14)': 'ATR',
    'EMA (20) vs Prezzo': 'EMA20/P', 'SMA (50/200)': 'SMA50/200', 'VWAP vs Prezzo': 'VWAP/P'
}, inplace=True)


# Liste di colonne rinominate per styling e formattazione
renamed_price_col = ['Prezzo ($)']
renamed_var_cols = ['Var. 1H (%)', 'Var. 12H (%)', 'Var. 24H (%)', 'Var. 1W (%)']
renamed_ai_signal_col = ['AI Signal']
# Aggiorna queste liste con i nomi rinominati esatti che usi
renamed_oscillator_cols = ['RSI (14)', 'SRSI %K', 'MACD', 'Stoch K', 'AO']
renamed_trend_strength_vol_cols = ['ADX', 'BB Pos.', 'OBV', 'ATR'] # Aggiunti OBV, ATR
renamed_ma_cols = ['EMA20/P', 'SMA50/200', 'VWAP/P']

cols_to_style = renamed_var_cols + renamed_ai_signal_col + renamed_oscillator_cols + \
                renamed_trend_strength_vol_cols + renamed_ma_cols

# Definisci i formattatori
formatters = {}
for col in renamed_var_cols:
    formatters[col] = lambda x: f"{x:+.1f}%" if isinstance(x, (int, float)) else x
formatters[renamed_price_col[0]] = "${:,.2f}"
if 'ATR' in df_display.columns: # Formattazione per ATR
    formatters['ATR'] = lambda x: f"{x:.2f}" if isinstance(x, (int, float)) else x


# Applica lo styling e poi la formattazione
# Usiamo apply per colonna per passare il nome della colonna alla funzione di stile
styled_df = df_display.style.set_table_styles([
    {'selector': 'th', 'props': [('text-align', 'center'), ('background-color', '#f0f2f6'), ('padding', '0.2rem'), ('font-size', '0.78em')]}, # Font header ulteriormente ridotto
    {'selector': 'td', 'props': [('padding', '0.2rem 0.3rem'), ('font-size', '0.78em')]}, # Font celle ulteriormente ridotto
])

for col_name in df_display.columns:
    if col_name in cols_to_style:
        styled_df = styled_df.apply(lambda s: s.map(lambda x: determine_style(x, column_name=col_name)), subset=[col_name])

styled_df = styled_df.format(formatters)

# Proprietà generali della tabella
styled_df = styled_df.set_properties(**{'text-align': 'center'}, subset=cols_to_style + ['Ticker', 'Link Analisi']) \
                     .set_properties(**{'text-align': 'right'}, subset=renamed_price_col) \
                     .set_properties(**{'text-align': 'left'}, subset=['Nome Asset'])


st.markdown("#### Segnali Tecnici Aggregati e Individuali")
# Per renderizzare HTML/Markdown nei link, dobbiamo passare escape=False a to_html
# e usare st.markdown. Questo però sovrascrive parte dello styling Pandas.
# Alternativa: `column_config` se usassimo `st.data_editor` o `st.dataframe` per la colonna link.
# Per ora, `st.dataframe` renderizzerà il markdown del link direttamente.
st.dataframe(styled_df, use_container_width=True, hide_index=True,
             # unsafe_allow_html=True # Per renderizzare HTML se lo Styler lo producesse
            )


# --- Legenda Indicatori ---
st.subheader("📜 Legenda Dettagliata Indicatori e Colonne")
st.markdown("---")
# ... (Legenda espansa, inclusi OBV e ATR)
st.markdown("##### Informazioni Generali & Link")
st.markdown("""
- **Nome Asset**: Nome completo dell'azione o criptovaluta/ETF.
- **Ticker**: Simbolo univoco dell'asset sul mercato.
- **Link Analisi**: Link diretto (📈) alla pagina dell'asset su TradingView per un'analisi grafica approfondita.
- **Prezzo ($)**: Ultimo prezzo registrato per l'asset, espresso in USD.
""")

st.markdown("##### Variazioni di Prezzo (Momentum a Breve Termine)")
st.markdown("""
- **Var. 1H (%)**: Variazione percentuale del prezzo nelle ultime 1 ora.
- **Var. 12H (%)**: Variazione percentuale del prezzo nelle ultime 12 ore.
- **Var. 24H (%)**: Variazione percentuale del prezzo nelle ultime 24 ore.
- **Var. 1W (%)**: Variazione percentuale del prezzo nell'ultima settimana.
*Verde indica un aumento (+), Rosso una diminuzione (-), Grigio per variazioni nulle (0.0%).*
""")

st.markdown("##### Segnale di Sintesi AI")
st.markdown("""
- **AI Signal**: Un segnale di trading di sintesi (<span style='color:darkgreen; font-weight:bold;'>🔥 Strong Buy</span>, <span style='color:green; font-weight:bold;'>Buy</span>, <span style='color:gray;'>Neutral</span>, <span style='color:red; font-weight:bold;'>Sell</span>, <span style='color:darkred; font-weight:bold;'>Strong Sell</span>).
    - *Descrizione*: Valuta e aggrega i segnali dei singoli indicatori tecnici.
    - *Utilità*: Fornisce una rapida valutazione complessiva. *Nota: è un ausilio, non una garanzia.*
""", unsafe_allow_html=True)

st.markdown("##### Indicatori di Volume, Momentum e Ipercomprato/Ipervenduto")
st.markdown("""
- **OBV** (On-Balance Volume Signal):
    - *Descrizione*: Indicatore di momentum che usa il flusso di volume per predire cambiamenti nel prezzo. Un OBV crescente suggerisce accumulo (pressione di acquisto), un OBV decrescente suggerisce distribuzione (pressione di vendita).
    - *Segnali Base*: <span style='color:green; font-weight:bold;'>BUY</span> se l'OBV mostra un trend rialzista o breakout. <span style='color:red; font-weight:bold;'>SELL</span> se OBV mostra trend ribassista o breakdown. <span style='color:gray;'>WAIT</span> in assenza di segnali chiari.
    - *Utilità*: Può confermare trend di prezzo o segnalare divergenze (es. prezzo sale ma OBV scende).
- **RSI (14)** (Relative Strength Index):
    - *Descrizione*: Misura velocità e cambiamento dei movimenti di prezzo. Scala 0-100.
    - *Segnali Base*: <30 (ipervenduto, <span style='color:green; font-weight:bold;'>BUY</span>), >70 (ipercomprato, <span style='color:red; font-weight:bold;'>SELL</span>), 30-70 (<span style='color:gray;'>WAIT</span>).
- **SRSI %K** (Stochastic RSI %K):
    - *Descrizione*: Stocastico applicato all'RSI. Più sensibile.
    - *Segnali Base (%K)*: <20 (<span style='color:green; font-weight:bold;'>BUY</span>), >80 (<span style='color:red; font-weight:bold;'>SELL</span>), 20-80 (<span style='color:gray;'>WAIT</span>).
- **MACD** (Moving Average Convergence Divergence - Crossover):
    - *Descrizione*: Relazione tra due EMA del prezzo.
    - *Segnali Base*: <span style='color:green; font-weight:bold;'>BUY</span> MACD sopra Segnale. <span style='color:red; font-weight:bold;'>SELL</span> MACD sotto Segnale. Altrimenti (<span style='color:gray;'>WAIT</span>).
- **Stoch K** (Stochastic Oscillator %K):
    - *Descrizione*: Prezzo di chiusura vs range di prezzo. Scala 0-100.
    - *Segnali Base (%K)*: <20 (<span style='color:green; font-weight:bold;'>BUY</span>), >80 (<span style='color:red; font-weight:bold;'>SELL</span>), 20-80 (<span style='color:gray;'>WAIT</span>).
- **AO** (Awesome Oscillator):
    - *Descrizione*: Momentum del mercato (SMA5 mediana vs SMA34 mediana).
    - *Segnali Base*: <span style='color:green; font-weight:bold;'>BUY</span> AO sopra zero. <span style='color:red; font-weight:bold;'>SELL</span> AO sotto zero. Altrimenti (<span style='color:gray;'>WAIT</span>).
""", unsafe_allow_html=True)

st.markdown("##### Indicatori di Forza del Trend & Volatilità")
st.markdown("""
- **ADX** (Average Directional Index):
    - *Descrizione*: Forza del trend (non direzione). Scala 0-100.
    - *Interpretazione*: >20 (<span style='color:green;'>Trend</span>), <20 (<span style='color:gray;'>No/Weak Trend</span>).
- **BB Pos.** (Bollinger Bands Position):
    - *Descrizione*: Prezzo vs SMA20 +/- 2 dev. std.
    - *Interpretazione*: <span style='color:green;'>Lower</span>, <span style='color:gray;'>Mid</span>, <span style='color:red;'>Upper</span>.
- **ATR** (Average True Range - 14 periodi):
    - *Descrizione*: Misura la volatilità del mercato. Calcola il range medio "vero" su 14 periodi. Mostrato come valore assoluto.
    - *Utilità*: Non dà segnali di direzione, ma indica quanto un asset si muove tipicamente. Utile per dimensionare stop-loss o target di profitto. Un ATR crescente indica volatilità crescente.
""", unsafe_allow_html=True)

st.markdown("##### M E D I E   M O B I L I")
st.markdown("""
- **EMA20/P** (Prezzo vs EMA 20): <span style='color:green; font-weight:bold;'>BUY</span> P > EMA, <span style='color:red; font-weight:bold;'>SELL</span> P < EMA. Altrimenti (<span style='color:gray;'>WAIT</span>).
- **SMA50/200** (SMA Crossover 50/200): <span style='color:green; font-weight:bold;'>BUY</span> Golden Cross, <span style='color:red; font-weight:bold;'>SELL</span> Death Cross. Altrimenti (<span style='color:gray;'>WAIT</span>).
- **VWAP/P** (Prezzo vs VWAP): <span style='color:green; font-weight:bold;'>BUY</span> P > VWAP, <span style='color:red; font-weight:bold;'>SELL</span> P < VWAP. Altrimenti (<span style='color:gray;'>WAIT</span>).
""", unsafe_allow_html=True)

# --- Sezione Error Logs ---
# (come prima)
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
st.caption(f"File: app.py | Versione: 0.1.0 | Ultima Modifica: {datetime.now().strftime('%Y-%m-%d')}")


# FILE_FOOTER_START
# End of file: app.py
# Version: 0.1.0
# Last Modified: 2024-03-18
# FILE_FOOTER_END
