from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title="BI Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# Título
st.title("📊 BI Analytics Dashboard")
st.markdown(
    "Dashboard interativo para análise de vendas e desempenho comercial."
)

# Caminho do CSV
arquivo_csv = Path(__file__).resolve().parent / "vendas.csv"

if not arquivo_csv.
