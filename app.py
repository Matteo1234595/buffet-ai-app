import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd

st.set_page_config(page_title="Buffett AI", layout="centered")
st.title("📈 Buffett AI - Analisi Azienda")

ticker = st.text_input("Inserisci il ticker aziendale (es: AAPL, MSFT)", value="AAPL")

if ticker:
    stock = yf.Ticker(ticker)
    info = stock.info

    st.subheader(f"{info.get('longName', 'Nome non trovato')}")
    price = info.get("currentPrice")
    pe = info.get("trailingPE")
    roe = info.get("returnOnEquity", 0) * 100 if info.get("returnOnEquity") else None
    debt = info.get("debtToEquity")
    fcf = info.get("freeCashflow")

    st.markdown(f"""
    **Prezzo attuale:** ${price}  
    **P/E Ratio:** {pe}  
    **ROE (%):** {roe:.2f}  
    **Debito/Equity:** {debt}  
    **Free Cash Flow:** {fcf}
    """)

    score = 0
    if pe and 8 < pe < 25: score += 1
    if roe and roe > 15: score += 1
    if debt and debt < 100: score += 1
    if fcf and fcf > 0: score += 1

    st.metric(label="Buffett Score", value=f"{score}/4")

    if score == 4:
        st.success("✅ Consiglio: **BUY**")
    elif score >= 2:
        st.warning("ℹ️ Consiglio: **HOLD**")
    else:
        st.error("❌ Consiglio: **SELL**")

    st.subheader("📉 Prezzo ultimi 6 mesi")
    hist = stock.history(period="6mo")
    st.line_chart(hist["Close"])
