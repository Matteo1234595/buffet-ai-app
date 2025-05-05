import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd

# Impostazioni pagina
st.set_page_config(page_title="Buffett AI", layout="centered")

# Titolo e introduzione
st.title("📈 Buffett AI – Analisi d'investimento")
st.markdown("""
Questa app ti aiuta a valutare un'azienda secondo i criteri fondamentali usati da Warren Buffett.
Inserisci il **ticker** (es: AAPL, MSFT, KO, BRK-B) per vedere se è un buon investimento.
""")

# Input utente
ticker = st.text_input("🎯 Inserisci il simbolo dell'azienda (ticker):", value="AAPL")

if ticker:
    try:
        # Estrazione dati da Yahoo Finance
        stock = yf.Ticker(ticker)
        info = stock.info

        # Estrazione indicatori fondamentali
        name = info.get("longName", "Nome non disponibile")
        price = info.get("currentPrice")
        pe = info.get("trailingPE")
        roe = info.get("returnOnEquity", 0) * 100 if info.get("returnOnEquity") else None
        debt = info.get("debtToEquity")
        fcf = info.get("freeCashflow")

        # Mostra i dati
        st.subheader(f"📊 Dati fondamentali: {name}")
        st.markdown(f"""
        - **Prezzo attuale:** ${price}  
        - **P/E Ratio:** {pe}  
        - **ROE:** {roe:.2f}%  
        - **Debito/Equity:** {debt}  
        - **Free Cash Flow:** {fcf}
        """)

        # Calcolo Buffett Score
        score = 0
        if pe and 8 < pe < 25: score += 1
        if roe and roe > 15: score += 1
        if debt and debt < 100: score += 1
        if fcf and fcf > 0: score += 1

        st.metric("💡 Buffett Score", f"{score}/4")

        # Raccomandazione
        if score == 4:
            st.success("✅ Raccomandazione: **BUY** – Ottima azienda secondo i criteri Buffett")
        elif score >= 2:
            st.warning("ℹ️ Raccomandazione: **HOLD** – Azienda solida, ma con qualche rischio")
        else:
            st.error("❌ Raccomandazione: **SELL** – Non rispetta i principi del valore")

        # Grafico prezzo ultimi 6 mesi
        st.subheader("📈 Andamento del prezzo (ultimi 6 mesi)")
        hist = stock.history(period="6mo")
        st.line_chart(hist["Close"])

    except Exception as e:
        st.error(f"Errore durante l'analisi del ticker: {e}")
