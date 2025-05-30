# FILE_VERSION_START
# Project: CryptoAndStocksIndicators
# File: app.py
# Version: 0.0.1
# Date: 2024-03-15
# Author: [Il Tuo Nome/Nickname]
# Description: Applicazione Streamlit principale per la dashboard degli indicatori (Struttura Iniziale con Dati Fittizi).
# FILE_VERSION_END

import streamlit as st
import pandas as pd
from datetime import datetime

# --- Configurazione Iniziale e Stato Sessione per Error Logs ---
if 'error_logs' not in st.session_state:
    st.session_state.error_logs = []

# --- Funzioni Helper (da implementare successivamente con dati reali) ---
def get_fictional_data():
    """
    Genera dati fittizi per la tabella.
    In futuro, questa funzione sarà sostituita da chiamate API reali.
    """
    data = [
        {'Rank': 1, 'Nome Asset': 'Microsoft Corp.', 'Ticker': 'MSFT', 'Market Cap ($)': '3.12 T', 'Prezzo Attuale ($)': 420.55, 'Var. 24H (%)': 0.2, 'RSI (14)': 'Wait', 'StochRSI (14,14,3,3) %K': 'Buy'},
        {'Rank': 2, 'Nome Asset': 'Apple Inc.', 'Ticker': 'AAPL', 'Market Cap ($)': '2.63 T', 'Prezzo Attuale ($)': 170.34, 'Var. 24H (%)': -0.5, 'RSI (14)': 'Sell', 'StochRSI (14,14,3,3) %K': 'Sell'},
        {'Rank': 3, 'Nome Asset': 'NVIDIA Corp.', 'Ticker': 'NVDA', 'Market Cap ($)': '2.20 T', 'Prezzo Attuale ($)': 880.27, 'Var. 24H (%)': 2.1, 'RSI (14)': 'Buy', 'StochRSI (14,14,3,3) %K': 'Buy'},
        {'Rank': 4, 'Nome Asset': 'Alphabet Inc. (Google)', 'Ticker': 'GOOGL', 'Market Cap ($)': '1.75 T', 'Prezzo Attuale ($)': 140.10, 'Var. 24H (%)': 0.7, 'RSI (14)': 'Wait', 'StochRSI (14,14,3,3) %K': 'Wait'},
        {'Rank': 5, 'Nome Asset': 'Amazon.com Inc.', 'Ticker': 'AMZN', 'Market Cap ($)': '1.82 T', 'Prezzo Attuale ($)': 175.80, 'Var. 24H (%)': -1.0, 'RSI (14)': 'Sell', 'StochRSI (14,14,3,3) %K': 'Sell'},
        {'Rank': 6, 'Nome Asset': 'Bitcoin', 'Ticker': 'BTC', 'Market Cap ($)': '1.35 T', 'Prezzo Attuale ($)': 68500.50, 'Var. 24H (%)': 1.5, 'RSI (14)': 'Buy', 'StochRSI (14,14,3,3) %K': 'Wait'},
        {'Rank': 7, 'Nome Asset': 'Meta Platforms Inc.', 'Ticker': 'META', 'Market Cap ($)': '1.22 T', 'Prezzo Attuale ($)': 480.12, 'Var. 24H (%)': -0.8, 'RSI (14)': 'Wait', 'StochRSI (14,14,3,3) %K': 'Sell'},
        {'Rank': 8, 'Nome Asset': 'Ethereum', 'Ticker': 'ETH', 'Market Cap ($)': '450.2 B', 'Prezzo Attuale ($)': 3750.00, 'Var. 24H (%)': 0.8, 'RSI (14)': 'Wait', 'StochRSI (14,14,3,3) %K': 'Buy'},
        {'Rank': 9, 'Nome Asset': 'ProSh UltraPro QQQ', 'Ticker': 'TQQQ', 'Market Cap ($)': '22.1 B', 'Prezzo Attuale ($)': 55.60, 'Var. 24H (%)': 1.5, 'RSI (14)': 'Buy', 'StochRSI (14,14,3,3) %K': 'Buy'},
        {'Rank': 10, 'Nome Asset': 'Tesla, Inc.', 'Ticker': 'TSLA', 'Market Cap ($)': '560.5 B', 'Prezzo Attuale ($)': 177.45, 'Var. 24H (%)': -3.0, 'RSI (14)': 'Sell', 'StochRSI (14,14,3,3) %K': 'Sell'},
        {'Rank': 11, 'Nome Asset': 'IonQ Inc.', 'Ticker': 'IONQ', 'Market Cap ($)': '2.1 B', 'Prezzo Attuale ($)': 10.30, 'Var. 24H (%)': 0.1, 'RSI (14)': 'Wait', 'StochRSI (14,14,3,3) %K': 'Wait'},
        {'Rank': 12, 'Nome Asset': 'ProSh Volatil ST Fut', 'Ticker': 'UVXY', 'Market Cap ($)': '550 M', 'Prezzo Attuale ($)': 8.50, 'Var. 24H (%)': 5.1, 'RSI (14)': 'Sell', 'StochRSI (14,14,3,3) %K': 'Sell'},
        {'Rank': 13, 'Nome Asset': 'Rigetti Computing', 'Ticker': 'RGTI', 'Market Cap ($)': '220 M', 'Prezzo Attuale ($)': 1.52, 'Var. 24H (%)': -1.2, 'RSI (14)': 'Buy', 'StochRSI (14,14,3,3) %K': 'Buy'},
    ]
    df = pd.DataFrame(data)
    # Assicuriamoci che 'Rank' sia la prima colonna e che sia ordinato per essa (anche se già lo è dai dati fittizi)
    # df = df.set_index('Rank', drop=False) # Non necessario se 'Rank' è solo per visualizzazione e non indice Pandas
    df = df.sort_values(by='Rank')
    return df

def style_signals(val):
    """Applica stili condizionali per i segnali Buy/Sell/Wait."""
    color = 'inherit' # Default per Wait o valori non stringa
    font_weight = 'normal'
    if isinstance(val, str):
        if 'Buy' in val.capitalize(): # Rende il controllo case-insensitive per "Buy"
            color = 'green'
            font_weight = 'bold'
        elif 'Sell' in val.capitalize(): # Rende il controllo case-insensitive per "Sell"
            color = 'red'
            font_weight = 'bold'
        elif 'Wait' in val.capitalize(): # Rende il controllo case-insensitive per "Wait"
            color = 'gray'
            # font_weight = 'bold' # Opzionale se vuoi Wait in grassetto
    return f'color: {color}; font-weight: {font_weight};'


# --- Interfaccia Utente Streamlit ---
st.set_page_config(layout="wide", page_title="Indicatori Trading Dashboard")
st.title("📊 Dashboard Indicatori Crypto & Stocks")
st.caption(f"Versione: 0.0.1 | Data: {datetime.now().strftime('%Y-%m-%d')}")


# Carica i dati (fittizi per ora)
df_data = get_fictional_data()

# Definisci le colonne da formattare e le colonne degli indicatori
price_cols = ['Prezzo Attuale ($)']
percentage_cols = ['Var. 24H (%)']
indicator_cols = ['RSI (14)', 'StochRSI (14,14,3,3) %K'] # Aggiungi qui altre colonne di indicatori

# Creazione dizionario per la formattazione
formatters = {}
for col in price_cols:
    if col in df_data.columns:
        formatters[col] = "${:,.2f}" # Formato valuta
for col in percentage_cols:
    if col in df_data.columns:
        formatters[col] = "{:+.1f}%" # Formato percentuale con segno


# Applica lo styling
# Nota: `subset` specifica a quali colonne applicare lo styling.
styled_df = df_data.style.apply(lambda x: x.map(style_signals), subset=indicator_cols) \
                           .format(formatters) \
                           .set_properties(**{'text-align': 'center'}, subset=indicator_cols + percentage_cols) \
                           .set_properties(**{'text-align': 'right'}, subset=price_cols) \
                           .set_table_styles([{'selector': 'th', 'props': [('text-align', 'center')]}])


# Visualizza la tabella
st.dataframe(styled_df, use_container_width=True, hide_index=True) # hide_index=True se 'Rank' è una colonna normale

# --- Legenda Indicatori ---
st.subheader("📜 Legenda Indicatori")
st.markdown("---") # Linea separatrice

st.markdown("""
#### Relative Strength Index (RSI)
- **Cos'è:** Un oscillatore di momentum che misura la velocità e il cambiamento dei movimenti di prezzo. L'RSI oscilla tra 0 e 100.
- **Come Funziona:** Calcolato sulla base delle perdite e dei guadagni medi su un determinato periodo (tipicamente 14 periodi).
- **Come Viene Usato (Segnali Base in Tabella):**
    - **<span style='color:green; font-weight:bold;'>BUY</span>:** RSI < 30. Indica condizioni di "ipervenduto".
    - **<span style='color:red; font-weight:bold;'>SELL</span>:** RSI > 70. Indica condizioni di "ipercomprato".
    - **<span style='color:gray;'>WAIT</span>:** RSI tra 30 e 70. Zona neutrale.
- **Utilità e Sfumature Professionali:**
    - Utile per identificare potenziali inversioni. I trader professionisti cercano **divergenze** e contestualizzano con il **trend primario**.
""", unsafe_allow_html=True)

st.markdown("""
#### Stochastic RSI (SRSI)
- **Cos'è:** Applica lo Stochastic Oscillator ai valori dell'RSI. Più sensibile dell'RSI.
- **Come Funziona:** Genera valori %K e %D tra 0 e 100.
- **Come Viene Usato (Segnali Base in Tabella, basati su %K):**
    - **<span style='color:green; font-weight:bold;'>BUY</span>:** SRSI %K < 20. Indica RSI "ipervenduto".
    - **<span style='color:red; font-weight:bold;'>SELL</span>:** SRSI %K > 80. Indica RSI "ipercomprato".
    - **<span style='color:gray;'>WAIT</span>:** SRSI %K tra 20 e 80. Zona neutrale.
- **Utilità e Sfumature Professionali:**
    - Utile per segnali a breve termine. I trader professionisti guardano ai **crossover %K/%D** e lo usano con cautela in mercati laterali.
""", unsafe_allow_html=True)

# --- Sezione Error Logs ---
st.subheader("⚠️ Error Logs")
st.markdown("---") # Linea separatrice

# Contenitore espandibile per i log
with st.expander("Mostra/Nascondi Error Logs", expanded=False):
    if 'error_logs' in st.session_state and st.session_state.error_logs:
        for i, log_entry in enumerate(reversed(st.session_state.error_logs)):
            st.error(f"{len(st.session_state.error_logs) - i}. {log_entry}")
    else:
        st.info("Nessun errore registrato finora.")

    # Bottone per simulare un errore (per testare la sezione log)
    if st.button("Simula Errore"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        asset_involved = "TEST_ASSET"
        function_name = "test_function"
        error_message = "Questo è un errore di test simulato."
        log_entry_content = f"[{timestamp}] Asset: {asset_involved} | Funzione: {function_name} | Errore: {error_message}"
        st.session_state.error_logs.append(log_entry_content)
        st.rerun() # Ricarica la pagina per vedere il log

    if st.button("Clear Error Logs"):
        st.session_state.error_logs = []
        st.rerun()

# --- Footer del File ---
st.markdown("---")
st.caption(f"File: app.py | Versione: 0.0.1 | Ultima Modifica: {datetime.now().strftime('%Y-%m-%d')}")

# FILE_FOOTER_START
# End of file: app.py
# Version: 0.0.1
# Last Modified: 2024-03-15
# FILE_FOOTER_END
